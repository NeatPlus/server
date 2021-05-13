from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from neatplus.models import TimeStampedModel


class Notification(TimeStampedModel):
    # recipient
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE,
    )

    # actor related
    actor_content_type = models.ForeignKey(
        ContentType,
        related_name="notify_actor",
        on_delete=models.CASCADE,
    )
    actor_object_id = models.PositiveIntegerField(null=True, blank=True)
    actor_content_object = GenericForeignKey("actor_content_type", "actor_object_id")

    # notification related
    verb = models.CharField(max_length=100)
    description = models.TextField()
    notification_type = models.CharField(max_length=50, default="default")
    timestamp = models.DateTimeField(default=timezone.now)

    # action object related
    action_object_content_type = models.ForeignKey(
        ContentType,
        related_name="notify_action_object",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    action_object_object_id = models.PositiveIntegerField(null=True, blank=True)
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
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_content_object = GenericForeignKey("target_content_type", "target_object_id")

    has_read = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ("-created_at",)
