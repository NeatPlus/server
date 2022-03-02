from rest_framework import serializers

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


class StatementTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementTopic
        fields = "__all__"


class StatementTagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementTagGroup
        fields = "__all__"


class StatementTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementTag
        fields = "__all__"


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = "__all__"


class MitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mitigation
        fields = "__all__"


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = "__all__"


class QuestionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStatement
        fields = "__all__"


class OptionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionStatement
        fields = "__all__"


class UploadQuestionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStatement
        exclude = ("statement", "version")


class UploadOptionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionStatement
        exclude = ("statement", "version")


class UploadWeightageSerializer(serializers.Serializer):
    version = serializers.CharField()
    questions = UploadQuestionStatementSerializer(many=True)
    options = UploadOptionStatementSerializer(many=True)


class ActivateVersionSerializer(serializers.Serializer):
    version = serializers.CharField()
