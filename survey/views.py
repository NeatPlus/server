from django.db.models import Q
from rest_framework import permissions, viewsets

from neatplus.views import UserStampedModelViewSetMixin
from project.utils import read_allowed_project_for_user

from .filters import OptionFilter, QuestionFilter, SurveyAnswerFilter, SurveyFilter
from .models import Option, Question, QuestionGroup, Survey, SurveyAnswer
from .serializers import (
    OptionSerializer,
    QuestionGroupSerializer,
    QuestionSerializer,
    SurveyAnswerSerializer,
    SurveySerializer,
)


class QuestionGroupViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuestionGroupSerializer
    queryset = QuestionGroup.objects.all()


class QuestionViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_class = QuestionFilter


class OptionViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    filterset_class = OptionFilter


class SurveyViewSet(UserStampedModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = SurveyFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        return Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )


class SurveyAnswerViewSet(UserStampedModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SurveyAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = SurveyAnswerFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        surveys = Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )
        return SurveyAnswer.objects.filter(survey__in=surveys)
