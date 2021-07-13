from rest_framework import permissions

from project.models import ProjectUser


class CanAcceptRejectProject(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organization:
            return request.user in obj.organization.admins.all()
        else:
            return request.user.is_superuser


class CanEditProject(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by
            or request.user in obj.organization.admins.all()
        )


class CanEditProjectOrReadOrCreateOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
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
