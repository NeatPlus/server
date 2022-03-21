from rest_framework import permissions


class IsOrganizationAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.admins.all()


class IsMemberRequestOrganizationAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.organization.admins.all()


class IsOrganizationAdminOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user in obj.admins.all()
        )
