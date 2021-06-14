from django_filters.rest_framework import filters
from django_filters.rest_framework.filterset import FilterSet

from .models import Mitigation, Opportunity, Statement, StatementTopic


class StatementTopicFilter(FilterSet):
    class Meta:
        model = StatementTopic
        fields = {"title": ["exact"], "context": ["exact"]}


class StatementFilter(FilterSet):
    class Meta:
        model = Statement
        fields = {
            "title": ["exact"],
            "topic": ["exact"],
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
