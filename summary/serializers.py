from rest_framework import serializers

from .models import (
    Mitigation,
    Opportunity,
    OptionMitigation,
    OptionOpportunity,
    OptionStatement,
    QuestionStatement,
    Statement,
    StatementTopic,
)


class StatementTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementTopic
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


class OptionMitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionMitigation
        fields = "__all__"


class OptionOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionOpportunity
        fields = "__all__"
