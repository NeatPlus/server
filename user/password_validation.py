import string

from django.core.exceptions import ImproperlyConfigured, ValidationError

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
            f"Minimum {self.minimum_class} character class missing from password",
            code="password_class_missing",
            params={
                "character_classes": self.character_classes,
                "minimum_class": self.minimum_class,
            },
        )

    def get_help_text(self):
        return f"Password must contain minimum {self.minimum_class} character classes from {self.character_classes}"
