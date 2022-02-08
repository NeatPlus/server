from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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

    class Meta:
        verbose_name = _("notification")
        verbose_plural_name = _("notifications")


@admin.register(Notice)
class NoticeAdmin(UserStampedModelAdmin):
    list_display = ("title", "notice_type", "is_active")

    class Meta:
        verbose_name = _("notice")
        verbose_plural_name = _("notices")
