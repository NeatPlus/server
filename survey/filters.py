from django_filters.rest_framework import FilterSet

from .models import Option, Question


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
