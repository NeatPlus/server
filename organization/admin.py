from django.contrib import admin

from neatplus.admin import UserStampedModelAdmin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(UserStampedModelAdmin):
    list_display = ("title",)
    autocomplete_fields = ("admins", "members")
    search_fields = ("title",)
