from django_filters.filters import NumberFilter
from django_filters.rest_framework import FilterSet

from .models import Option, Question, QuestionGroup, Survey, SurveyAnswer


class QuestionGroupFilter(FilterSet):
    class Meta:
        model = QuestionGroup
        fields = {"module": ["exact"]}


class QuestionFilter(FilterSet):
    # Added at 2022-03-23. Added for backward compatibility.
    # TODO: Remove it after some time if frontend is not using
    module = NumberFilter(field_name="group__module", lookup_expr="exact")

    class Meta:
        model = Question
        fields = {
            "title": ["exact"],
            "answer_type": ["exact"],
            "group": ["exact"],
            "group__module": ["exact"],
            "is_required": ["exact"],
        }


class OptionFilter(FilterSet):
    class Meta:
        model = Option
        fields = {
            "question": ["exact"],
        }


class SurveyFilter(FilterSet):
    class Meta:
        model = Survey
        fields = {"project": ["exact"], "title": ["exact"]}


class SurveyAnswerFilter(FilterSet):
    class Meta:
        model = SurveyAnswer
        fields = {
            "survey": ["exact"],
            "survey__project": ["exact"],
            "question": ["exact"],
            "answer_type": ["exact"],
        }
