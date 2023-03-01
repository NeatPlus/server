from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from context.models import Module
from neatplus.serializers import UserModelSerializer
from survey.models import QuestionGroup

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


class StatementTopicSerializer(UserModelSerializer):
    class Meta:
        model = StatementTopic
        fields = "__all__"


class StatementTagGroupSerializer(UserModelSerializer):
    class Meta:
        model = StatementTagGroup
        fields = "__all__"


class StatementTagSerializer(UserModelSerializer):
    class Meta:
        model = StatementTag
        fields = "__all__"


class StatementSerializer(UserModelSerializer, FlexFieldsModelSerializer):
    class Meta:
        model = Statement
        fields = "__all__"
        expandable_fields = {
            "mitigations": ("statement.MitigationSerializer", {"many": True}),
            "opportunities": ("statement.OpportunitySerializer", {"many": True}),
        }


class MitigationSerializer(UserModelSerializer):
    class Meta:
        model = Mitigation
        fields = "__all__"


class OpportunitySerializer(UserModelSerializer):
    class Meta:
        model = Opportunity
        fields = "__all__"


class StatementFormulaSerializer(UserModelSerializer):
    class Meta:
        model = StatementFormula
        fields = "__all__"


class QuestionStatementSerializer(UserModelSerializer):
    class Meta:
        model = QuestionStatement
        exclude = ("created_by", "updated_by", "created_at", "modified_at")
        read_only_fields = ("statement", "version", "question_group")


class OptionStatementSerializer(UserModelSerializer):
    class Meta:
        model = OptionStatement
        exclude = ("created_by", "updated_by", "created_at", "modified_at")
        read_only_fields = ("statement", "version", "question_group")


class UploadWeightageSerializer(serializers.Serializer):
    question_group = serializers.PrimaryKeyRelatedField(
        queryset=QuestionGroup.objects.all(), allow_null=True
    )
    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), required=False
    )
    questions = QuestionStatementSerializer(many=True)
    options = OptionStatementSerializer(many=True)
    formula = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class ActivateVersionSerializer(serializers.Serializer):
    version = serializers.CharField()
    question_group = serializers.PrimaryKeyRelatedField(
        queryset=QuestionGroup.objects.all(), allow_null=True, required=False
    )


class ActivateDraftVersionSerializer(serializers.Serializer):
    question_group = serializers.PrimaryKeyRelatedField(
        queryset=QuestionGroup.objects.all(), allow_null=True, required=False
    )
