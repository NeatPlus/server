from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from project.utils import read_allowed_project_for_user
from summary.permissions import (
    CanAcknowledgeSurveyResultFeedback,
    CanWriteSurveyResultOrReadOnly,
)
from survey.models import Survey

from .filters import SurveyResultFeedbackFilter, SurveyResultFilter
from .models import SurveyResult, SurveyResultFeedback
from .serializers import (
    SurveyResultFeedbackSerializer,
    SurveyResultSerializer,
    WritableSurveyResultFeedbackSerializer,
)


class SurveyResultViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveyResultSerializer
    permission_classes = [CanWriteSurveyResultOrReadOnly]
    filterset_class = SurveyResultFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        surveys = Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )
        return SurveyResult.objects.filter(survey__in=surveys)

    @extend_schema(
        responses=inline_serializer(
            name="AddSurveyResultFeedbackResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully added survey result feedback")
                )
            },
        ),
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=WritableSurveyResultFeedbackSerializer,
    )
    def add_feedback(self, request, *args, **kwargs):
        survey_result = self.get_object()
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        SurveyResultFeedback.objects.create(
            created_by=user,
            survey_result=survey_result,
            actual_score=survey_result.score,
            **serializer.data
        )
        return Response(
            {"detail": _("Successfully added survey result feedback")},
            status=status.HTTP_201_CREATED,
        )


class SurveyResultFeedbackViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveyResultFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = SurveyResultFeedbackFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        surveys = Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )
        return SurveyResultFeedback.objects.filter(survey_result__survey__in=surveys)

    @extend_schema(
        responses=inline_serializer(
            name="AcknowledgeSurveyResultFeedbackResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully acknowledged survey result feedback")
                )
            },
        ),
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanAcknowledgeSurveyResultFeedback],
        serializer_class=serializers.Serializer,
    )
    def acknowledge(self, request, *args, **kwargs):
        survey_result_feedback = self.get_object()
        survey_result_feedback.status = SurveyResultFeedback.StatusChoice.ACKNOWLEDGED
        survey_result_feedback.updated_by = self.request.user
        survey_result_feedback.save()
        return Response(
            {"detail": _("Successfully acknowledged survey result feedback")},
            status=status.HTTP_200_OK,
        )
