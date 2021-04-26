import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template

from neatplus.auth_validators import CustomASCIIUsernameValidator
from neatplus.fields import LowerCharField, LowerEmailField
from neatplus.managers import CustomUserManager
from neatplus.models import TimeStampedModel
from neatplus.utils import random_N_digit_number


class User(AbstractUser):
    username_validator = CustomASCIIUsernameValidator()

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
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.pk:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(self, field_name):
                        changed_fields.append(field_name)
                except Exception as e:
                    pass
            kwargs["update_fields"] = changed_fields
            if "email" in kwargs["update_fields"]:
                self.is_active = False
        super().save(*args, **kwargs)


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


@receiver(post_save, sender=get_user_model())
def send_email_confiramtion_pin(sender, instance, created, **kwargs):
    if created or "email" in kwargs["update_fields"]:
        six_digit_pin = random_N_digit_number(6)
        active_for_one_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
        email_confirm_object, _ = EmailConfirmationPin.objects.update_or_create(
            user=instance,
            defaults={
                "pin": six_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
            },
        )
        email_template = get_template("email_confirm.txt")
        context = {"user": instance, "email_confirm_object": email_confirm_object}
        message = email_template.render(context)
        instance.email_user("Email confirmation mail", message)
