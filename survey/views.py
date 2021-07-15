from django.db.models import Q
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.permissions import IsOwner, IsOwnerOrReadOnly
from neatplus.utils import gen_random_string
from neatplus.views import UserStampedModelViewSetMixin
from project.utils import read_allowed_project_for_user

from .filters import OptionFilter, QuestionFilter, SurveyAnswerFilter, SurveyFilter
from .models import Option, Question, QuestionGroup, Survey, SurveyAnswer
from .serializers import (
    OptionSerializer,
    QuestionGroupSerializer,
    QuestionSerializer,
    SharedSurveySerializer,
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


class SurveyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveySerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = SurveyFilter

    def get_queryset(self):
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
        permission_classes=[IsOwner],
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
        permission_classes=[IsOwner],
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
                {"error": "cannot update link of not shared survey"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        responses=inline_serializer(
            name="SurveyUnShareLinkResponseSerializer",
            fields={"detail": "Successfully unshared survey"},
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsOwner],
        serializer_class=serializers.Serializer,
    )
    def unshare_link(self, request, *args, **kwargs):
        survey = self.get_object()
        survey.is_shared_publicly = False
        survey.shared_link_identifier = None
        survey.save()
        return Response({"detail": "Successfully unshared survey"})

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
                {"error": "Identifier not found"}, status=status.HTTP_404_NOT_FOUND
            )


class SurveyAnswerViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SurveyAnswerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = SurveyAnswerFilter

    def get_queryset(self):
        current_user = self.request.user
        projects = read_allowed_project_for_user(current_user)
        surveys = Survey.objects.filter(
            Q(project__in=projects) | Q(created_by=current_user)
        )
        return SurveyAnswer.objects.filter(survey__in=surveys)
