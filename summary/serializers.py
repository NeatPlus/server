from rest_framework import serializers

from neatplus.serializers import UserModelSerializer

from .models import SurveyResult, SurveyResultFeedback


class SurveyResultSerializer(UserModelSerializer):
    contains_baseline_feedback = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SurveyResult
        fields = "__all__"
        read_only_fields = ("survey",)

    def get_contains_baseline_feedback(self, obj):
        return obj.feedbacks.filter(is_baseline=True).exists()


class SurveyResultFeedbackSerializer(UserModelSerializer):
    survey_title = serializers.SerializerMethodField(read_only=True)
    survey_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SurveyResultFeedback
        fields = "__all__"
        read_only_fields = ("actual_score", "status", "is_baseline")

    def get_survey_title(self, obj):
        return obj.survey_result.survey.title

    def get_survey_id(self, obj):
        return obj.survey_result.survey.id


class BaselineSurveyResultFeedbackSerializer(SurveyResultFeedbackSerializer):
    class Meta(SurveyResultFeedbackSerializer.Meta):
        read_only_fields = ("status", "is_baseline")
