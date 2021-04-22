from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator

from neatplus.auth_validators import CustomASCIIUsernameValidator
from neatplus.fields import LowerCharField, LowerEmailField


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
