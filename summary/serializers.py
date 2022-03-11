from rest_framework import serializers

from .models import SurveyResult, SurveyResultFeedback


class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = "__all__"


class WritableSurveyResultSerializer(SurveyResultSerializer):
    class Meta:
        model = SurveyResult
        exclude = ("survey",)


class SurveyResultFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResultFeedback
        fields = "__all__"


class WritableSurveyResultFeedbackSerializer(SurveyResultFeedbackSerializer):
    class Meta:
        model = SurveyResultFeedback
        exclude = ("survey_result", "actual_score", "status")
