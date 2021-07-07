from django.db.models import Q
from rest_framework import mixins, permissions, viewsets

from neatplus.permissions import IsOwnerOrReadOnly
from project.utils import read_allowed_project_for_user
from survey.models import Survey

from .filters import SurveyResultFilter
from .models import SurveyResult
from .serializers import SurveyResultSerializer


class SurveyResultViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveyResultSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = SurveyResultFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        surveys = Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )
        return SurveyResult.objects.filter(survey__in=surveys)
