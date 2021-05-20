from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Project, ProjectUser


@admin.register(Project)
class ProjectAdmin(UserStampedModelAdmin, OrderedModelAdmin):
    list_display = (
        "title",
        "organization",
        "visibility",
        "status",
        "context",
        "move_up_down_links",
    )
    autocomplete_fields = ("organization", "users", "context")
    search_fields = ("title",)


@admin.register(ProjectUser)
class ProjectUserAdmin(UserStampedModelAdmin):
    list_display = ("project", "user", "permission")
    autocomplete_fields = ("project", "user")
