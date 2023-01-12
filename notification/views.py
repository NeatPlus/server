from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.serializers import get_detail_inline_serializer

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
        queryset = self.filter_queryset(self.get_queryset().filter(has_read=False))
        data = {"unread_count": queryset.count()}
        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data)

    @extend_schema(
        responses=get_detail_inline_serializer(
            "MarkAllAsReadResponseSerializer",
            _("Successfully marked all notification as read"),
        )
    )
    @action(detail=False, methods=["post"], serializer_class=serializers.Serializer)
    def mark_all_as_read(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(has_read=False))
        queryset.update(has_read=True, modified_at=timezone.now())
        return Response(
            {"detail": _("Successfully marked all notification as read")},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses=get_detail_inline_serializer(
            "MarkAsReadResponseSerializer", _("Successfully marked as read")
        )
    )
    @action(detail=True, methods=["post"], serializer_class=serializers.Serializer)
    def mark_as_read(self, request, pk=None, *args, **kwargs):
        notification = self.get_object()
        notification.has_read = True
        notification.modified_at = timezone.now()
        notification.save()
        return Response({"detail": _("Successfully marked as read")})


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    filterset_class = NoticeFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(notice_type="public")
        return queryset
