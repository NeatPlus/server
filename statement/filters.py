from django_filters.rest_framework.filterset import FilterSet

from .models import (
    Mitigation,
    Opportunity,
    OptionMitigation,
    OptionOpportunity,
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
            "options": ["exact"],
        }


class OpportunityFilter(FilterSet):
    class Meta:
        model = Opportunity
        fields = {
            "title": ["exact"],
            "statement": ["exact"],
            "options": ["exact"],
        }


class QuestionStatementFilter(FilterSet):
    class Meta:
        model = QuestionStatement
        fields = {
            "statement": ["exact"],
            "question": ["exact"],
            "version": ["exact"],
            "is_active": ["exact"],
        }


class OptionStatementFilter(FilterSet):
    class Meta:
        model = OptionStatement
        fields = {
            "statement": ["exact"],
            "option": ["exact"],
            "version": ["exact"],
            "is_active": ["exact"],
        }


class OptionMitigationFilter(FilterSet):
    class Meta:
        model = OptionMitigation
        fields = {
            "mitigation": ["exact"],
            "option": ["exact"],
        }


class OptionOpportunityFilter(FilterSet):
    class Meta:
        model = OptionOpportunity
        fields = {
            "opportunity": ["exact"],
            "option": ["exact"],
        }
