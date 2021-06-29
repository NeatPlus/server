from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone

from neatplus.auth_validators import CustomASCIIUsernameValidator
from neatplus.fields import LowerCharField, LowerEmailField
from neatplus.managers import CustomUserManager
from neatplus.models import TimeStampedModel

from .tasks import background_send_mail


class User(AbstractUser):
    username_validator = CustomASCIIUsernameValidator()

    # Abstract user modification
    username = LowerCharField(
        "username",
        max_length=20,
        unique=True,
        help_text="Required. Length can be between 5 to 20. Letters, digits and ./-/_ only.",
        validators=[
            username_validator,
            MinLengthValidator(limit_value=5),
        ],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = LowerEmailField(
        "email address",
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    is_active = models.BooleanField(
        "active",
        default=False,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )

    # Custom
    organization = models.CharField(max_length=255, null=True, blank=True, default=None)
    role = models.CharField(max_length=50, null=True, blank=True, default=None)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.pk:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    old_val = getattr(old, field_name)
                    new_val = getattr(self, field_name)
                    if hasattr(field, "is_custom_lower_field"):
                        if field.is_custom_lower_field():
                            new_val = new_val.lower()
                    if old_val != new_val:
                        changed_fields.append(field_name)
                except Exception:
                    pass
            if "email" in changed_fields:
                self.is_active = False
                changed_fields.append("is_active")
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)

    def notify(
        self,
        actor,
        verb,
        notification_type=None,
        timestamp=timezone.now(),
        action_object=None,
        target=None,
        description=None,
    ):
        """
        Create notification for user.

        Notifications are actually actions events, which are categorized by four main components.

        Actor. The object that performed the activity.
        Verb. The verb phrase that identifies the action of the activity.
        Action Object. (Optional) The object linked to the action itself.
        Target. (Optional) The object to which the activity was performed.

        Actor, Action Object and Target are GenericForeignKeys to any arbitrary Django object.
        An action is a description of an action that was performed (Verb) at some instant in time by some Actor on some
        optional Target that results in an Action Object getting created/updated/deleted

        Use '{actor} {verb} {action_object(optional)} on {target(optional)}' as description if description is not provided
        """
        if not description:
            extra_content = ""
            if action_object:
                extra_content += f" {action_object}"
            if target:
                extra_content += f" on {target}"

        description = f"{actor} {verb}{extra_content}"
        NotificationModel = apps.get_model("notification", "Notification")
        NotificationModel.objects.create(
            recipient=self,
            actor_content_object=actor,
            verb=verb,
            description=description,
            notification_type=notification_type,
            timestamp=timestamp,
            action_object_content_object=action_object,
            target_content_object=target,
        )

    def celery_email_user(self, subject, message, from_email=None, **kwargs):
        background_send_mail.delay(
            self.pk, subject, message, from_email=from_email, **kwargs
        )


class PasswordResetPin(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_pin",
    )
    no_of_incorrect_attempts = models.PositiveIntegerField(default=0)
    pin = models.PositiveIntegerField(
        validators=[MinLengthValidator(6), MaxLengthValidator(6)]
    )
    pin_expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    identifier = models.CharField(max_length=16)


class EmailConfirmationPin(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_confirm_pin",
    )
    no_of_incorrect_attempts = models.PositiveIntegerField(default=0)
    pin = models.PositiveIntegerField(
        validators=[MinLengthValidator(6), MaxLengthValidator(6)]
    )
    pin_expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
