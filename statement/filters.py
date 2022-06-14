from django_filters.filters import CharFilter
from django_filters.rest_framework.filterset import FilterSet

from .models import (
    Mitigation,
    Opportunity,
    OptionStatement,
    QuestionStatement,
    Statement,
    StatementTag,
    StatementTagGroup,
    StatementTopic,
)


class StatementTopicFilter(FilterSet):
    class Meta:
        model = StatementTopic
        fields = {"title": ["exact"], "context": ["exact"]}


class StatementTagGroupFilter(FilterSet):
    class Meta:
        model = StatementTagGroup
        fields = {"title": ["exact"]}


class StatementTagFilter(FilterSet):
    class Meta:
        model = StatementTag
        fields = {"title": ["exact"], "group": ["exact"]}


class StatementFilter(FilterSet):
    class Meta:
        model = Statement
        fields = {
            "title": ["exact"],
            "topic": ["exact"],
            "tags": ["exact"],
            "questions": ["exact"],
            "options": ["exact"],
        }


class MitigationFilter(FilterSet):
    class Meta:
        model = Mitigation
        fields = {
            "title": ["exact"],
            "statement": ["exact"],
        }


class OpportunityFilter(FilterSet):
    class Meta:
        model = Opportunity
        fields = {
            "title": ["exact"],
            "statement": ["exact"],
        }


class QuestionStatementFilter(FilterSet):
    version = CharFilter(label="version", method="get_version")

    class Meta:
        model = QuestionStatement
        fields = {
            "statement": ["exact"],
            "question": ["exact"],
            "is_active": ["exact"],
            "question_group": ["exact"],
        }

    def get_version(self, queryset, name, value):
        if value == "latest":
            if queryset.filter(version="draft").exists():
                return queryset.filter(version="draft")
            return queryset.filter(is_active=True)
        return queryset.filter(version=value)


class OptionStatementFilter(FilterSet):
    version = CharFilter(label="version", method="get_version")

    class Meta:
        model = OptionStatement
        fields = {
            "statement": ["exact"],
            "option": ["exact"],
            "is_active": ["exact"],
            "question_group": ["exact"],
        }

    def get_version(self, queryset, name, value):
        if value == "latest":
            if queryset.filter(version="draft").exists():
                return queryset.filter(version="draft")
            return queryset.filter(is_active=True)
        return queryset.filter(version=value)
