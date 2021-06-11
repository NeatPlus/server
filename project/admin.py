from django.contrib import admin
from django.http.response import HttpResponseRedirect
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
    change_form_template = "project_change_form.html"

    def response_change(self, request, obj):
        if "_reject_project" in request.POST:
            obj.status = "rejected"
            obj.save()
            self.message_user(request, "Project rejected")
            return HttpResponseRedirect(".")
        if "_accept_project" in request.POST:
            obj.status = "accepted"
            obj.save()
            self.message_user(request, "Project accepted")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(ProjectUser)
class ProjectUserAdmin(UserStampedModelAdmin):
    list_display = ("project", "user", "permission")
    autocomplete_fields = ("project", "user")
