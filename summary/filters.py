from django_filters.rest_framework import FilterSet

from summary.models import SurveyResult, SurveyResultFeedback


class SurveyResultFilter(FilterSet):
    class Meta:
        model = SurveyResult
        fields = {
            "survey": ["exact"],
            "survey__project": ["exact"],
            "statement": ["exact"],
            "question_group": ["exact"],
            "score": ["exact"],
        }


class SurveyResultFeedbackFilter(FilterSet):
    class Meta:
        model = SurveyResultFeedback
        fields = {
            "survey_result": ["exact"],
            "survey_result__survey": ["exact"],
            "survey_result__survey__project": ["exact"],
            "survey_result__statement": ["exact"],
            "status": ["exact"],
            "is_baseline": ["exact"],
        }
