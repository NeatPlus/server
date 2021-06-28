from rest_framework import permissions


class IsMemberRequestOrganizationAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.organization.admins.all()
