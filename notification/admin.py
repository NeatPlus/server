from django.contrib import admin

from neatplus.admin import UserStampedModelAdmin

from .models import Notice, Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "actor_content_object",
        "action_object_content_object",
        "target_content_object",
        "notification_type",
        "has_read",
    )
    autocomplete_fields = ("recipient",)


@admin.register(Notice)
class NoticeAdmin(UserStampedModelAdmin):
    list_display = ("title", "notice_type", "is_active")
