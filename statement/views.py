from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import (
    MitigationFilter,
    OpportunityFilter,
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
    OptionStatement,
    QuestionStatement,
    Statement,
    StatementTag,
    StatementTagGroup,
    StatementTopic,
)
from .serializers import (
    ActivateDraftVersionSerializer,
    ActivateVersionSerializer,
    MitigationSerializer,
    OpportunitySerializer,
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
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            with transaction.atomic():
                for question_statement_data in data["questions"]:
                    weightage = question_statement_data.pop("weightage")
                    question_group = question_statement_data.pop("question_group", None)
                    question_obj, created = QuestionStatement.objects.update_or_create(
                        **question_statement_data,
                        question_group=question_group,
                        statement=statement,
                        version="draft",
                        defaults={"weightage": weightage},
                    )
                    if created:
                        question_obj.created_by = user
                    else:
                        question_obj.updated_by = user
                    question_obj.save()
                for option_statement_data in data["options"]:
                    weightage = option_statement_data.pop("weightage")
                    question_group = option_statement_data.pop("question_group", None)
                    option_obj, created = OptionStatement.objects.update_or_create(
                        **option_statement_data,
                        question_group=question_group,
                        statement=statement,
                        version="draft",
                        defaults={"weightage": weightage},
                    )
                    if created:
                        option_obj.created_by = user
                    else:
                        option_obj.updated_by = user
                    option_obj.save()
        except Exception as e:
            print(e)
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
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        version = data["version"]
        question_group = data["question_group"]
        with transaction.atomic():
            QuestionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).exclude(version=version).update(is_active=False, updated_by=user)
            QuestionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).filter(version=version).update(is_active=True, updated_by=user)
            OptionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).exclude(version=version).update(is_active=False, updated_by=user)
            OptionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).filter(version=version).update(is_active=True, updated_by=user)
        return Response({"detail": _("Successfully activate new version")})

    @extend_schema(
        responses=inline_serializer(
            name="ActivateDraftVersionResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully activate draft version")
                )
            },
        )
    )
    @action(
        detail=True,
        methods=["post"],
        serializer_class=ActivateDraftVersionSerializer,
    )
    def activate_draft_version(self, request, *args, **kwargs):
        statement = self.get_object()
        user = self.request.user
        version = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        question_group = data["question_group"]
        with transaction.atomic():
            # Rename version to date time based version
            QuestionStatement.objects.filter(
                statement=statement, version="draft", question_group=question_group
            ).update(version=version)
            OptionStatement.objects.filter(
                statement=statement, version="draft", question_group=question_group
            ).update(version=version)
            # Make all old version inactive and new version active version
            QuestionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).exclude(version=version).update(is_active=False, updated_by=user)
            QuestionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).filter(version=version).update(is_active=True, updated_by=user)
            OptionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).exclude(version=version).update(is_active=False, updated_by=user)
            OptionStatement.objects.filter(
                statement=statement, question_group=question_group
            ).filter(version=version).update(is_active=True, updated_by=user)
        return Response({"detail": _("Successfully activate draft version")})


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
