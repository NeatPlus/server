from django.db import transaction
from django.db.models import Avg, F, FloatField, Q, StdDev, Sum
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.serializers import get_detail_inline_serializer
from project.utils import read_allowed_project_for_user
from summary.permissions import (
    CanAcknowledgeSurveyResultFeedback,
    CanAddBaselineFeedback,
    CanWriteSurveyResultOrReadOnly,
)
from survey.models import Survey

from .filters import SurveyResultFeedbackFilter, SurveyResultFilter
from .models import SurveyResult, SurveyResultFeedback
from .serializers import (
    BaselineSurveyResultFeedbackSerializer,
    SurveyInsightSerializer,
    SurveyResultFeedbackSerializer,
    SurveyResultSerializer,
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
        request=SurveyResultFeedbackSerializer(many=True),
        responses=get_detail_inline_serializer(
            "AddSurveyResultFeedbackResponseSerializer",
            _("Successfully added survey result feedback"),
        ),
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=SurveyResultFeedbackSerializer,
    )
    def add_feedback(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                for data in serializer.validated_data:
                    survey_result = data.pop("survey_result")
                    survey_result_score = survey_result.score
                    SurveyResultFeedback.objects.create(
                        created_by=user,
                        survey_result=survey_result,
                        actual_score=survey_result_score,
                        is_baseline=False,
                        **data
                    )
        except Exception as e:
            print(e)
            return Response(
                {"detail": _("Failed to add survey result feedback")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": _("Successfully added survey result feedback")},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        request=BaselineSurveyResultFeedbackSerializer(many=True),
        responses=get_detail_inline_serializer(
            "AddBaselineSurveyResultFeedbackResponseSerializer",
            _("Successfully added baseline survey result feedback"),
        ),
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[CanAddBaselineFeedback],
        serializer_class=BaselineSurveyResultFeedbackSerializer,
    )
    def add_baseline_feedback(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                for data in serializer.validated_data:
                    survey_result = data.pop("survey_result")
                    (
                        survey_result_feedback,
                        created,
                    ) = SurveyResultFeedback.objects.update_or_create(
                        survey_result=survey_result,
                        is_baseline=True,
                        defaults=data,
                    )
                    if created:
                        survey_result_feedback.created_by = user
                    else:
                        survey_result_feedback.updated_by = user
                    survey_result_feedback.save()
        except Exception:
            return Response(
                {"detail": _("Failed to add baseline survey result feedback")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": _("Successfully added baseline survey result feedback")},
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
        return SurveyResultFeedback.objects.filter(
            survey_result__survey__in=surveys
        ).select_related("survey_result__survey")

    @extend_schema(
        responses=get_detail_inline_serializer(
            "AcknowledgeSurveyResultFeedbackResponseSerializer",
            _("Successfully acknowledged survey result feedback"),
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


class SurveyInsightAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        statement_id = self.request.query_params.get("statement")
        question_group_id = self.request.query_params.get("question_group")
        module_id = self.request.query_params.get("module")

        if not module_id:
            return Response(
                {"error": _("Missing module")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        baseline_survey_result_feedback = SurveyResultFeedback.objects.filter(
            is_baseline=True,
            survey_result__question_group_id=question_group_id,
            survey_result__module_id=module_id,
        )

        if statement_id:
            baseline_survey_result_feedback = baseline_survey_result_feedback.filter(
                survey_result__statement_id=statement_id
            )

        queryset = baseline_survey_result_feedback.values(
            statement=F("survey_result__statement")
        ).annotate(
            difference=Avg(
                F("expected_score") - F("actual_score"), output_field=FloatField()
            ),
            sum_of_square=Sum(
                (F("expected_score") - F("actual_score")) ** 2,
                output_field=FloatField(),
            ),
            standard_deviation=StdDev(
                F("expected_score") - F("actual_score"), output_field=FloatField()
            ),
        )

        serializer = SurveyInsightSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
