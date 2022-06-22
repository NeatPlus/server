from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.views import UserStampedModelViewSetMixin

from .filters import (
    MitigationFilter,
    OpportunityFilter,
    OptionStatementFilter,
    QuestionStatementFilter,
    StatementFilter,
    StatementFormulaFilter,
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
    StatementFormula,
    StatementTag,
    StatementTagGroup,
    StatementTopic,
)
from .serializers import (
    ActivateDraftVersionSerializer,
    ActivateVersionSerializer,
    CreateStatementFormulaSerializer,
    MitigationSerializer,
    OpportunitySerializer,
    OptionStatementSerializer,
    QuestionStatementSerializer,
    StatementFormulaSerializer,
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


class StatementViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
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
                question_group = data.pop("question_group", None)

                QuestionStatement.objects.filter(
                    statement=statement, question_group=question_group, version="draft"
                ).delete()

                for question_statement_data in data["questions"]:
                    QuestionStatement.objects.create(
                        **question_statement_data,
                        question_group=question_group,
                        statement=statement,
                        version="draft",
                        created_by=user,
                    )

                OptionStatement.objects.filter(
                    statement=statement, question_group=question_group, version="draft"
                ).delete()
                for option_statement_data in data["options"]:
                    OptionStatement.objects.create(
                        **option_statement_data,
                        question_group=question_group,
                        statement=statement,
                        version="draft",
                    )

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
            name="UploadFormulaResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully created formula for statement")
                )
            },
        )
    )
    @action(
        detail=True,
        methods=["post"],
        serializer_class=CreateStatementFormulaSerializer,
    )
    def create_formula(self, request, *args, **kwargs):
        statement = self.get_object()
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        question_group = data.pop("question_group", None)
        obj, created = StatementFormula.objects.update_or_create(
            statement=statement, question_group=question_group, defaults=data
        )
        if created:
            obj.created_by = user
        else:
            obj.updated_by = user
        obj.save()
        return Response(
            {"detail": _("Successfully created formula for statement")},
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
        question_group = data.pop("question_group", None)
        if not QuestionStatement.objects.filter(
            version=version, statement=statement, question_group=question_group
        ).exists():
            return Response(
                {"error": _("No question statements found for this version")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not OptionStatement.objects.filter(
            version=version, statement=statement, question_group=question_group
        ).exists():
            return Response(
                {"error": _("No option statements found for this version")},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        question_group = data.pop("question_group", None)
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


class StatementFormulaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementFormulaSerializer
    queryset = StatementFormula.objects.all()
    filterset_class = StatementFormulaFilter


class QuestionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionStatementSerializer
    queryset = QuestionStatement.objects.all()
    filterset_class = QuestionStatementFilter


class OptionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionStatementSerializer
    queryset = OptionStatement.objects.all()
    filterset_class = OptionStatementFilter
