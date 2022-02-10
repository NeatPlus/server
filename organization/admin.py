from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from neatplus.admin import AcceptRejectModelAdmin, UserStampedModelAdmin

from .models import Organization, OrganizationMemberRequest


@admin.register(Organization)
class OrganizationAdmin(
    DraggableMPTTAdmin, UserStampedModelAdmin, AcceptRejectModelAdmin
):
    list_display = ("tree_actions", "indented_title", "title", "status", "parent")
    autocomplete_fields = ("admins", "members", "parent")
    search_fields = ("title",)
    change_form_template = "organization_change_form.html"


@admin.register(OrganizationMemberRequest)
class OrganizationMemberRequestAdmin(UserStampedModelAdmin, AcceptRejectModelAdmin):
    list_display = ("created_at", "user", "organization", "status")
    autocomplete_fields = ("user", "organization")
    change_form_template = "organization_member_request_change_form.html"
