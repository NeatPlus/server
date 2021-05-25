from rest_framework import serializers

from .models import Option, Question, QuestionGroup


class QuestionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionGroup
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"
