from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

ADDITIONAL_USER_FIELDS = (
    (_("Additional Fields"), {"fields": ("organization", "role")}),
)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "organization",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
