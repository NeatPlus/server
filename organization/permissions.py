from rest_framework import permissions

from neatplus.permissions import CREATE_METHOD


class IsMemberRequestOrganizationAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.organization.admins.all()


class IsOrganizationAdminOrReadOrCreateOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == CREATE_METHOD
            or request.user in obj.organization.admins.all()
        )
