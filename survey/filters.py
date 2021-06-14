from django_filters.rest_framework import FilterSet

from .models import Option, Question, Survey, SurveyAnswer


class QuestionFilter(FilterSet):
    class Meta:
        model = Question
        fields = {
            "title": ["exact"],
            "answer_type": ["exact"],
            "group": ["exact"],
            "module": ["exact"],
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
