from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=False, methods=["get"], serializer_class=serializers.Serializer)
    def unread_count(self, request, *args, **kwargs):
        return Response(
            {
                "unread_count": Notification.objects.filter(
                    recipient=self.request.user, has_read=False
                ).count()
            }
        )

    @action(detail=False, methods=["post"], serializer_class=serializers.Serializer)
    def mark_all_as_read(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=self.request.user, has_read=False).update(
            has_read=True
        )
        return Response(
            {"detail": "Successfully marked all notification as read"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None, *args, **kwargs):
        notification = self.get_object()
        Notification.objects.filter(pk=notification.pk).update(has_read=True)
        return Response({"detail": "Successfully marked as read"})
