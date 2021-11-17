from rest_framework import permissions

from project.models import ProjectUser


class CanWriteSurvey(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        user = request.user
        if project.organization:
            return (
                user == obj.created_by
                or user in project.organization.admins.all()
                or ProjectUser.objects.filter(
                    project=project, user=user, permission="write"
                ).exists()
            )
        else:
            return (
                user == obj.created_by
                or ProjectUser.objects.filter(
                    project=project, user=user, permission="write"
                ).exists()
            )


class CanWriteSurveyOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        project = obj.project
        user = request.user
        if project.organization:
            return (
                user == obj.created_by
                or user in project.organization.admins.all()
                or ProjectUser.objects.filter(
                    project=project, user=user, permission="write"
                ).exists()
            )
        else:
            return (
                user == obj.created_by
                or ProjectUser.objects.filter(
                    project=project, user=user, permission="write"
                ).exists()
            )
