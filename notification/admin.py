from django.contrib import admin

from .models import Notification


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
