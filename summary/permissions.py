from rest_framework import permissions

from project.models import ProjectUser


class CanAcknowledgeSurveyResultFeedback(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        project = obj.survey_result.survey.project
        user = request.user
        if project.organization:
            return (
                user in project.organization.admins.all()
                or ProjectUser.objects.filter(
                    project=project, user=user, permission="write"
                ).exists()
            )
        else:
            return ProjectUser.objects.filter(
                project=project, user=user, permission="write"
            ).exists()


class CanAddBaselineFeedback(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.has_perm("summary.add_baseline_feedback")


class CanWriteSurveyResultOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        project = obj.survey.project
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
