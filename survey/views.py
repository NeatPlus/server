from collections import Counter, defaultdict

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from context.models import Module
from neatplus.serializers import get_detail_inline_serializer
from neatplus.utils import gen_random_string
from neatplus.views import UserStampedModelViewSetMixin
from project.utils import read_allowed_project_for_user
from statement.models import Mitigation, Opportunity
from summary.models import SurveyResult
from summary.serializers import SurveyResultSerializer

from .filters import OptionFilter, QuestionFilter, SurveyAnswerFilter, SurveyFilter
from .models import Option, Question, QuestionGroup, Survey, SurveyAnswer
from .permissions import CanWriteSurvey, CanWriteSurveyOrReadOnly
from .serializers import (
    MitigationOpportunityInsightSerializer,
    OptionSerializer,
    QuestionGroupSerializer,
    QuestionSerializer,
    SharedSurveySerializer,
    SurveyAnswerSerializer,
    SurveySerializer,
    WritableSurveyAnswerSerializer,
)


class QuestionGroupViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuestionGroupSerializer
    queryset = QuestionGroup.objects.all()


class QuestionViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().select_related("group__module")
    filterset_class = QuestionFilter


class OptionViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    filterset_class = OptionFilter


class SurveyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveySerializer
    permission_classes = [CanWriteSurveyOrReadOnly]
    filterset_class = SurveyFilter

    def get_queryset(self):
        # if self.action value is identifier then queryset can be none since
        # that api can be accessed by anyone.
        # Not setting it to none will cause survey/identifier/<survey_identifier>
        # API to fail with 500 error code for non authenticated user
        if self.action == "identifier":
            return Survey.objects.none()
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        return Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )

    @extend_schema(
        responses=inline_serializer(
            name="SurveyShareLinkResponseSerializer",
            fields={"shared_link_identifier": serializers.CharField()},
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanWriteSurvey],
        serializer_class=serializers.Serializer,
    )
    def share_link(self, request, *args, **kwargs):
        survey = self.get_object()
        survey.is_shared_publicly = True
        if not survey.shared_link_identifier:
            shared_link_identifier = gen_random_string(10)
            while Survey.objects.filter(
                shared_link_identifier=shared_link_identifier
            ).first():
                shared_link_identifier = gen_random_string(10)
            survey.shared_link_identifier = shared_link_identifier
        else:
            shared_link_identifier = survey.shared_link_identifier
        survey.save()
        return Response({"shared_link_identifier": shared_link_identifier})

    @extend_schema(
        responses=inline_serializer(
            name="SurveyUpdateLinkResponseSerializer",
            fields={"shared_link_identifier": serializers.CharField()},
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanWriteSurvey],
        serializer_class=serializers.Serializer,
    )
    def update_link(self, request, *args, **kwargs):
        survey = self.get_object()
        if survey.is_shared_publicly:
            shared_link_identifier = gen_random_string(10)
            while Survey.objects.filter(
                shared_link_identifier=shared_link_identifier
            ).first():
                shared_link_identifier = gen_random_string(10)
            survey.shared_link_identifier = shared_link_identifier
            survey.save()
            return Response({"shared_link_identifier": shared_link_identifier})
        else:
            return Response(
                {"error": _("Cannot update link of not shared survey")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        responses=get_detail_inline_serializer(
            "SurveyUnShareLinkResponseSerializer",
            _("Successfully unshared survey"),
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanWriteSurvey],
        serializer_class=serializers.Serializer,
    )
    def unshare_link(self, request, *args, **kwargs):
        survey = self.get_object()
        survey.is_shared_publicly = False
        survey.shared_link_identifier = None
        survey.save()
        return Response({"detail": _("Successfully unshared survey")})

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=SharedSurveySerializer,
        url_path=r"identifier/(?P<shared_link_identifier>[^/.]+)",
    )
    def identifier(self, request, *args, **kwargs):
        identifier = kwargs.get("shared_link_identifier")
        survey = Survey.objects.filter(
            shared_link_identifier=identifier, is_shared_publicly=True
        ).first()
        if survey:
            serializer = self.get_serializer(survey)
            return Response(serializer.data)
        else:
            return Response(
                {"error": _("Identifier not found")}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        request=WritableSurveyAnswerSerializer(many=True),
        responses=get_detail_inline_serializer(
            "AddSurveyAnswerResponseSerializer", _("Successfully added survey answers")
        ),
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanWriteSurvey],
        serializer_class=WritableSurveyAnswerSerializer,
    )
    def add_answers(self, request, *args, **kwargs):
        survey = self.get_object()
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for validated_datum in serializer.validated_data:
                    options = validated_datum.pop("options", None)
                    question = validated_datum.pop("question")
                    survey_answer, created = SurveyAnswer.objects.update_or_create(
                        survey=survey, question=question, defaults=validated_datum
                    )
                    if created:
                        survey_answer.created_by = user
                    else:
                        survey_answer.updated_by = user
                    survey_answer.save()
                    if options:
                        survey_answer.options.set(options)
        except Exception:
            return Response(
                {"error": _("Failed to add answers for survey")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": _("Successfully added survey answers")},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        request=SurveyResultSerializer(many=True),
        responses=get_detail_inline_serializer(
            "AddSurveyResultResponseSerializer", _("Successfully added survey results")
        ),
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanWriteSurvey],
        serializer_class=SurveyResultSerializer,
    )
    def add_results(self, request, *args, **kwargs):
        survey = self.get_object()
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for validated_datum in serializer.validated_data:
                    statement = validated_datum.pop("statement")
                    module = validated_datum.pop("module")
                    question_group = validated_datum.pop("question_group", None)
                    survey_result, created = SurveyResult.objects.update_or_create(
                        survey=survey,
                        statement=statement,
                        module=module,
                        question_group=question_group,
                        defaults=validated_datum,
                    )
                    if created:
                        survey_result.created_by = user
                    else:
                        survey_result.updated_by = user
                    survey_result.save()
        except Exception:
            return Response(
                {"error": _("Failed to create survey result due to invalid data")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": _("Successfully added survey results")},
            status=status.HTTP_201_CREATED,
        )


class SurveyAnswerViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveyAnswerSerializer
    permission_classes = [CanWriteSurveyOrReadOnly]
    filterset_class = SurveyAnswerFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        surveys = Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )
        return SurveyAnswer.objects.filter(survey__in=surveys)


class MitigationOpportunityInsightAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get("survey")
        module_id = self.request.query_params.get("module")

        if not survey_id:
            return Response(
                {"error": _("Missing survey")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not module_id:
            return Response(
                {"error": _("Missing module")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        survey = Survey.objects.filter(id=survey_id).first()
        if not survey:
            return Response(
                {"error": _("Invalid survey id")}, status=status.HTTP_400_BAD_REQUEST
            )

        module = Module.objects.filter(id=module_id).first()
        if not module:
            return Response(
                {"error": _("Invalid module id")}, status=status.HTTP_400_BAD_REQUEST
            )

        mitigation_counter = Counter()
        submitted_answer_mitigations = defaultdict(float)
        for mitigation in Mitigation.objects.filter(
            options__survey_answers__survey=survey
        ):
            if mitigation.rank:
                submitted_answer_mitigations[mitigation.id] += 1 / mitigation.rank
                mitigation_counter[mitigation.id] += 1
        mitigation_score = SurveyResult.objects.filter(
            module=module,
            survey=survey,
            statement__options__mitigations__isnull=False,
        ).values_list("statement__options__mitigations", "score")
        mitigation_scores = {}
        for mitigation, score in mitigation_score:
            if mitigation in submitted_answer_mitigations:
                old_score = mitigation_scores.get(
                    mitigation, submitted_answer_mitigations[mitigation]
                )
                mitigation_scores[mitigation] = old_score + score
                mitigation_counter[mitigation] += 1
        important_mitigation = sorted(
            mitigation_scores, key=mitigation_scores.get, reverse=True
        )[:20]
        repeated_mitigation = [
            i[0]
            for i in mitigation_counter.most_common(25)
            if i[0] not in important_mitigation
        ][:5]
        mitigation_dict = {
            "important": Mitigation.objects.filter(
                id__in=important_mitigation
            ).values_list("title", flat=True),
            "repeated": Mitigation.objects.filter(
                id__in=repeated_mitigation
            ).values_list("title", flat=True),
        }

        opportunity_counter = Counter()
        submitted_answer_opportunities = defaultdict(float)
        for opportunity in Opportunity.objects.filter(
            options__survey_answers__survey=survey
        ):
            if opportunity.rank:
                submitted_answer_opportunities[opportunity.id] += 1 / opportunity.rank
                opportunity_counter[opportunity.id] += 1
        opportunity_score = SurveyResult.objects.filter(
            module=module,
            survey=survey,
            statement__options__opportunities__isnull=False,
        ).values_list("statement__options__opportunities", "score")
        opportunity_scores = {}
        for opportunity, score in opportunity_score:
            if opportunity in submitted_answer_opportunities:
                old_score = opportunity_scores.get(
                    opportunity, submitted_answer_opportunities[opportunity]
                )
                opportunity_scores[opportunity] = old_score + score
                opportunity_counter[opportunity] += 1
        important_opportunity = sorted(
            opportunity_scores, key=opportunity_scores.get, reverse=True
        )[:20]
        repeated_opportunity = [
            i[0]
            for i in opportunity_counter.most_common(25)
            if i[0] not in important_opportunity
        ][:5]
        opportunity_dict = {
            "important": Opportunity.objects.filter(
                id__in=important_opportunity
            ).values_list("title", flat=True),
            "repeated": Opportunity.objects.filter(
                id__in=repeated_opportunity
            ).values_list("title", flat=True),
        }

        response = {"mitigations": mitigation_dict, "opportunities": opportunity_dict}

        serializer = MitigationOpportunityInsightSerializer(data=response)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
