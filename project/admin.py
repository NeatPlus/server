from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import AcceptRejectModelAdmin, UserStampedModelAdmin

from .models import Project, ProjectUser


class OrganizationAutoCompleteFilter(AutocompleteFilter):
    title = "Organization"
    field_name = "organization"


@admin.register(Project)
class ProjectAdmin(UserStampedModelAdmin, OrderedModelAdmin, AcceptRejectModelAdmin):
    list_display = (
        "created_at",
        "created_by",
        "title",
        "organization",
        "visibility",
        "status",
        "context",
        "move_up_down_links",
    )
    list_filter = (OrganizationAutoCompleteFilter,)
    autocomplete_fields = ("organization", "users", "context")
    search_fields = ("title",)
    change_form_template = "project_change_form.html"

    class Meta:
        verbose_name = _("project")
        verbose_plural_name = _("projects")


@admin.register(ProjectUser)
class ProjectUserAdmin(UserStampedModelAdmin):
    list_display = ("project", "user", "permission")
    autocomplete_fields = ("project", "user")

    class Meta:
        verbose_name = _("project user")
        verbose_plural_name = _("project users")
