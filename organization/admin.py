from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Organization, Project, ProjectUser


@admin.register(Organization)
class OrganizationAdmin(UserStampedModelAdmin):
    list_display = ("title",)
    autocomplete_fields = ("admins", "members")
    search_fields = ("title",)


@admin.register(Project)
class ProjectAdmin(UserStampedModelAdmin, OrderedModelAdmin):
    list_display = (
        "title",
        "organization",
        "visibility",
        "status",
        "move_up_down_links",
    )
    autocomplete_fields = ("organization", "users")
    search_fields = ("title",)


@admin.register(ProjectUser)
class ProjectUserAdmin(UserStampedModelAdmin):
    list_display = ("project", "user", "permission")
    autocomplete_fields = ("project", "user")
