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
        is_created_by = request.user == obj.created_by
        if obj.organization:
            return is_created_by or request.user in obj.organization.admins.all()
        else:
            return is_created_by


class CanEditProjectOrReadOnly(CanEditProject):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)


class CanCreateSurveyForProject(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organization:
            return (
                request.user == obj.created_by
                or request.user in obj.organization.admins.all()
                or ProjectUser.objects.filter(
                    project=obj, user=request.user, permission="write"
                ).exists()
            )
        else:
            return (
                request.user == obj.created_by
                or ProjectUser.objects.filter(
                    project=obj, user=request.user, permission="write"
                ).exists()
            )
