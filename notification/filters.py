from django_filters.rest_framework import FilterSet

from .models import Notice, Notification


class NotificationFilter(FilterSet):
    class Meta:
        model = Notification
        fields = {
            "has_read": ["exact"],
            "notification_type": ["exact"],
            "actor_content_type__model": ["exact"],
            "timestamp": ["gte", "lte"],
            "target_content_type__model": ["exact"],
            "action_object_content_type__model": ["exact"],
        }


class NoticeFilter(FilterSet):
    class Meta:
        model = Notice
        fields = {"title": ["exact"], "notice_type": ["exact"]}
