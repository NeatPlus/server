from django.contrib import admin

from neatplus.admin import AcceptRejectModelAdmin, UserStampedModelAdmin

from .models import Organization, OrganizationMemberRequest


@admin.register(Organization)
class OrganizationAdmin(UserStampedModelAdmin, AcceptRejectModelAdmin):
    list_display = ("title", "status")
    autocomplete_fields = ("admins", "members")
    search_fields = ("title",)
    change_form_template = "organization_change_form.html"


@admin.register(OrganizationMemberRequest)
class OrganizationMemberRequestAdmin(UserStampedModelAdmin, AcceptRejectModelAdmin):
    list_display = ("created_at", "user", "organization", "status")
    autocomplete_fields = ("user", "organization")
    change_form_template = "organization_member_request_change_form.html"
