from rest_framework import serializers

from neatplus.serializers import UserModelSerializer
from survey.models import QuestionGroup

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


class StatementSerializer(UserModelSerializer):
    class Meta:
        model = Statement
        fields = "__all__"


class MitigationSerializer(UserModelSerializer):
    class Meta:
        model = Mitigation
        fields = "__all__"


class OpportunitySerializer(UserModelSerializer):
    class Meta:
        model = Opportunity
        fields = "__all__"


class QuestionStatementSerializer(UserModelSerializer):
    class Meta:
        model = QuestionStatement
        exclude = ("created_by", "updated_by", "created_at", "modified_at")


class OptionStatementSerializer(UserModelSerializer):
    class Meta:
        model = OptionStatement
        exclude = ("created_by", "updated_by", "created_at", "modified_at")


class UploadQuestionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStatement
        exclude = ("statement", "version", "question_group")


class UploadOptionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionStatement
        exclude = ("statement", "version", "question_group")


class UploadWeightageSerializer(serializers.Serializer):
    question_group = serializers.PrimaryKeyRelatedField(
        queryset=QuestionGroup.objects.all(), allow_null=True, required=False
    )
    questions = UploadQuestionStatementSerializer(many=True)
    options = UploadOptionStatementSerializer(many=True)


class ActivateVersionSerializer(serializers.Serializer):
    version = serializers.CharField()
    question_group = serializers.PrimaryKeyRelatedField(
        queryset=QuestionGroup.objects.all(), allow_null=True, required=False
    )


class ActivateDraftVersionSerializer(serializers.Serializer):
    question_group = serializers.PrimaryKeyRelatedField(
        queryset=QuestionGroup.objects.all(), allow_null=True, required=False
    )
