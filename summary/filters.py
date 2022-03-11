from django_filters.rest_framework import FilterSet

from summary.models import SurveyResult


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
