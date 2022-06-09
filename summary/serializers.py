from rest_framework import serializers

from neatplus.serializers import UserModelSerializer

from .models import SurveyResult, SurveyResultFeedback


class SurveyResultSerializer(UserModelSerializer):
    class Meta:
        model = SurveyResult
        fields = "__all__"


class WritableSurveyResultSerializer(SurveyResultSerializer):
    class Meta:
        model = SurveyResult
        exclude = ("survey",)


class SurveyResultFeedbackSerializer(UserModelSerializer):
    survey_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SurveyResultFeedback
        fields = "__all__"

    def get_survey_title(self, obj):
        return obj.survey_result.survey.title


class WritableSurveyResultFeedbackSerializer(SurveyResultFeedbackSerializer):
    class Meta:
        model = SurveyResultFeedback
        exclude = ("actual_score", "status", "is_baseline")
