from rest_framework import permissions

from project.models import ProjectUser

CREATE_METHOD = "POST"


class IsProjectOrganizationAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.organization.admins.all()


class CanEditProject(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by
            or request.user in obj.organization.admins.all()
        )


class CanEditProjectOrReadAndCreateOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.method == CREATE_METHOD
        ):
            return True
        return (
            request.user == obj.created_by
            or request.user in obj.organization.admins.all()
        )


class CanCreateSurveyForProject(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by
            or request.user in obj.organization.admins.all()
            or ProjectUser.objects.filter(
                project=obj, user=request.user, permission="write"
            ).exists()
        )
