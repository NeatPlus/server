from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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

    class Meta:
        verbose_name = _("organization")
        verbose_plural_name = _("organizations")


@admin.register(OrganizationMemberRequest)
class OrganizationMemberRequestAdmin(UserStampedModelAdmin, AcceptRejectModelAdmin):
    list_display = ("created_at", "user", "organization", "status")
    autocomplete_fields = ("user", "organization")
    change_form_template = "organization_member_request_change_form.html"

    class Meta:
        verbose_name = _("organization member request")
        verbose_plural_name = _("organization member requests")
