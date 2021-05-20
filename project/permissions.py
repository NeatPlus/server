from django.db.models import Q
from rest_framework import permissions

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


class CanEditProjectOrReadOrCreateOnly(permissions.IsAuthenticated):
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
