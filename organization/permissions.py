from django.db.models import Q
from rest_framework import permissions

from .models import Organization


class CanEditProject(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user == obj.created_by
            or request.user in obj.organization.admins.all()
        )
