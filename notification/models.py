from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from neatplus.models import TimeStampedModel, UserStampedModel


class Notification(TimeStampedModel):
    # recipient
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE,
        verbose_name=_("recipient"),
    )

    # actor related
    actor_content_type = models.ForeignKey(
        ContentType,
        related_name="notify_actor",
        on_delete=models.CASCADE,
        verbose_name=_("actor content type"),
    )
    actor_object_id = models.PositiveIntegerField(
        _("actor object id"), null=True, blank=True
    )
    actor_content_object = GenericForeignKey("actor_content_type", "actor_object_id")

    # notification related
    verb = models.CharField(_("verb"), max_length=100)
    description = models.TextField(_("description"))
    notification_type = models.CharField(
        _("notification type"), max_length=50, default="default"
    )
    timestamp = models.DateTimeField(_("timestamp"), default=timezone.now)

    # action object related
    action_object_content_type = models.ForeignKey(
        ContentType,
        related_name="notify_action_object",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("action object content type"),
    )
    action_object_object_id = models.PositiveIntegerField(
        _("action object object id"), null=True, blank=True
    )
    action_object_content_object = GenericForeignKey(
        "action_object_content_type", "action_object_object_id"
    )

    # target related
    target_content_type = models.ForeignKey(
        ContentType,
        related_name="notify_target",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("target content type"),
    )
    target_object_id = models.PositiveIntegerField(
        _("target object id"), null=True, blank=True
    )
    target_content_object = GenericForeignKey("target_content_type", "target_object_id")

    has_read = models.BooleanField(_("read"), default=False, editable=False)

    class Meta:
        ordering = ("-created_at",)


class Notice(UserStampedModel, TimeStampedModel):
    class NoticeTypeChoice(models.TextChoices):
        USER = "user"
        PUBLIC = "public"

    title = models.CharField(_("title"), max_length=255)
    description = RichTextField(_("description"), blank=True, null=True, default=None)
    notice_type = models.CharField(
        _("notice type"),
        max_length=6,
        default="public",
        choices=NoticeTypeChoice.choices,
    )
    is_active = models.BooleanField(_("active"), default=True)

    def __str__(self):
        return self.title
