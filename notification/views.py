from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import NoticeFilter, NotificationFilter
from .models import Notice, Notification
from .serializers import (
    NoticeSerializer,
    NotificationSerializer,
    UnReadCountResponseSerializer,
)


class NotificationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = NotificationFilter

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(
        detail=False, methods=["get"], serializer_class=UnReadCountResponseSerializer
    )
    def unread_count(self, request, *args, **kwargs):
        data = {
            "unread_count": Notification.objects.filter(
                recipient=self.request.user, has_read=False
            ).count()
        }
        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data)

    @extend_schema(
        responses=inline_serializer(
            name="MarkAllAsReadResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="Successfully marked all notification as read"
                )
            },
        )
    )
    @action(detail=False, methods=["post"], serializer_class=serializers.Serializer)
    def mark_all_as_read(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=self.request.user, has_read=False).update(
            has_read=True, modified_at=timezone.now()
        )
        return Response(
            {"detail": "Successfully marked all notification as read"},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses=inline_serializer(
            name="MarkAsReadResponseSerializer",
            fields={
                "detail": serializers.CharField(default="Successfully marked as read")
            },
        )
    )
    @action(detail=True, methods=["post"], serializer_class=serializers.Serializer)
    def mark_as_read(self, request, pk=None, *args, **kwargs):
        notification = self.get_object()
        Notification.objects.filter(pk=notification.pk).update(
            has_read=True, modified_at=timezone.now()
        )
        return Response({"detail": "Successfully marked as read"})


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    filterset_class = NoticeFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(notice_type="public")
        return queryset
