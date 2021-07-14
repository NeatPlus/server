from rest_framework import permissions

CREATE_METHOD = "POST"


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or request.user == obj.created_by
        )
