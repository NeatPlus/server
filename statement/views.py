from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import (
    MitigationFilter,
    OpportunityFilter,
    OptionMitigationFilter,
    OptionOpportunityFilter,
    OptionStatementFilter,
    QuestionStatementFilter,
    StatementFilter,
    StatementTagFilter,
    StatementTagGroupFilter,
    StatementTopicFilter,
)
from .models import (
    Mitigation,
    Opportunity,
    OptionMitigation,
    OptionOpportunity,
    OptionStatement,
    QuestionStatement,
    Statement,
    StatementTag,
    StatementTagGroup,
    StatementTopic,
)
from .serializers import (
    ActivateVersionSerializer,
    MitigationSerializer,
    OpportunitySerializer,
    OptionMitigationSerializer,
    OptionOpportunitySerializer,
    OptionStatementSerializer,
    QuestionStatementSerializer,
    StatementSerializer,
    StatementTagGroupSerializer,
    StatementTagSerializer,
    StatementTopicSerializer,
    UploadWeightageSerializer,
)


class StatementTopicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTopicSerializer
    queryset = StatementTopic.objects.all()
    filterset_class = StatementTopicFilter


class StatementTagGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTagGroupSerializer
    queryset = StatementTagGroup.objects.all()
    filterset_class = StatementTagGroupFilter


class StatementTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTagSerializer
    queryset = StatementTag.objects.all()
    filterset_class = StatementTagFilter


class StatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementSerializer
    queryset = Statement.objects.all()
    filterset_class = StatementFilter

    @extend_schema(
        responses=inline_serializer(
            name="UploadWeightageResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully uploaded weightage for statement")
                )
            },
        )
    )
    @action(
        detail=True,
        methods=["post"],
        serializer_class=UploadWeightageSerializer,
    )
    def upload_weightage(self, request, *args, **kwargs):
        statement = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        version = data["version"]
        try:
            with transaction.atomic():
                for question_statement_data in data["questions"]:
                    QuestionStatement.objects.create(
                        **question_statement_data, statement=statement, version=version
                    )
                for option_statement_data in data["options"]:
                    OptionStatement.objects.create(
                        **option_statement_data, statement=statement, version=version
                    )
        except Exception as e:
            return Response(
                {"error": _("Failed to upload weightage for statement")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": _("Successfully uploaded weightage for statement")},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=inline_serializer(
            name="ActivateVersionResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully activate new version")
                )
            },
        )
    )
    @action(
        detail=True,
        methods=["post"],
        serializer_class=ActivateVersionSerializer,
    )
    def activate_version(self, request, *args, **kwargs):
        statement = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        version = data["version"]
        with transaction.atomic():
            QuestionStatement.objects.filter(statement=statement).exclude(
                version=version
            ).update(is_active=False)
            QuestionStatement.objects.filter(statement=statement).filter(
                version=version
            ).update(is_active=True)
            OptionStatement.objects.filter(statement=statement).exclude(
                version=version
            ).update(is_active=False)
            OptionStatement.objects.filter(statement=statement).filter(
                version=version
            ).update(is_active=True)
        return Response({"detail": _("Successfully activate new version")})


class MitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MitigationSerializer
    queryset = Mitigation.objects.all()
    filterset_class = MitigationFilter


class OpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()
    filterset_class = OpportunityFilter


class QuestionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionStatementSerializer
    queryset = QuestionStatement.objects.all()
    filterset_class = QuestionStatementFilter


class OptionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionStatementSerializer
    queryset = OptionStatement.objects.all()
    filterset_class = OptionStatementFilter


class OptionMitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionMitigationSerializer
    queryset = OptionMitigation.objects.all()
    filterset_class = OptionMitigationFilter


class OptionOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionOpportunitySerializer
    queryset = OptionOpportunity.objects.all()
    filterset_class = OptionOpportunityFilter
