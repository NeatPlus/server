from rest_framework import serializers

from .models import Mitigation, Opportunity, Statement, StatementTopic


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
