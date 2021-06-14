from django.db import models


class LowerCharField(models.CharField):
    def get_prep_value(self, value):
        return super().get_prep_value(value).lower()

    def is_custom_lower_field(self):
        return True


class LowerEmailField(models.EmailField):
    def get_prep_value(self, value):
        return super().get_prep_value(value).lower()

    def is_custom_lower_field(self):
        return True


class LowerTextField(models.TextField):
    def get_prep_value(self, value):
        return super().get_prep_value(value).lower()

    def is_custom_lower_field(self):
        return True
