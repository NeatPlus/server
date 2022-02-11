import string

from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from .models import UserOldPassword

DEFAULT_CHARACTER_CLASSES = [
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits,
    string.punctuation,
]


class CharacterClassValidator:
    def __init__(self, character_classes=DEFAULT_CHARACTER_CLASSES, minimum_class=3):
        self.character_classes = character_classes
        self.minimum_class = minimum_class

    def validate(self, password, user=None):
        present_class_count = 0
        for character_class in self.character_classes:
            if any(char in character_class for char in password):
                present_class_count += 1
            if present_class_count == self.minimum_class:
                return None
        raise ValidationError(
            ngettext_lazy(
                "Minimum %(minimum_class)d character class missing from password",
                "Minimum %(minimum_class)d character classes missing from password",
                self.minimum_class,
            ),
            code="password_class_missing",
            params={
                "minimum_class": self.minimum_class,
            },
        )

    def get_help_text(self):
        return ngettext_lazy(
            "Password must contain minimum {minimum_class} character class from {character_classes}",
            "Password must contain minimum {minimum_class} character classes from {character_classes}",
            self.minimum_class,
        ).format(
            minimum_class=self.minimum_class, character_classes=self.character_classes
        )


class OldPasswordValidator:
    def __init__(self, count=5):
        self.count = count

    def validate(self, password, user=None):
        if user is None:
            return None
        user_old_passwords = UserOldPassword.objects.filter(user=user).order_by(
            "-created_at"
        )[: self.count]
        for user_old_password in user_old_passwords:
            is_old_password = check_password(password, user_old_password.password)
            if is_old_password:
                raise ValidationError(
                    ngettext_lazy(
                        "Cannot use last %(count)d password",
                        "Cannot use last %(count)d passwords",
                        self.count,
                    ),
                    code="password_resuse",
                    params={"count": self.count},
                )

    def password_changed(self, password, user=None):
        if user is None:
            return None
        hashed_password = make_password(password)
        UserOldPassword.objects.create(user=user, password=hashed_password)

    def get_help_text(self):
        return ngettext_lazy(
            "Your password must not contain last {count} password",
            "Your password must not contain last {count} password",
            self.count,
        ).format(count=self.count)
