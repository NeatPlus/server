from django_filters.filters import CharFilter
from django_filters.rest_framework.filterset import FilterSet

from .models import (
    Mitigation,
    Opportunity,
    OptionStatement,
    QuestionStatement,
    Statement,
    StatementFormula,
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
        fields = {"title": ["exact"], "statements": ["exact"], "options": ["exact"]}


class OpportunityFilter(FilterSet):
    class Meta:
        model = Opportunity
        fields = {"title": ["exact"], "statements": ["exact"], "options": ["exact"]}


class StatementFormulaFilter(FilterSet):
    version = CharFilter(label="version", method="get_version")

    class Meta:
        model = StatementFormula
        fields = {
            "statement": ["exact"],
            "question_group": ["exact"],
            "module": ["exact"],
            "is_active": ["exact"],
        }

    def get_version(self, queryset, name, value):
        if value == "latest":
            draft_statement_formulas = queryset.filter(version="draft")
            draft_statements = draft_statement_formulas.values_list(
                "statement", flat=True
            )
            queryset_id = list(draft_statement_formulas.values_list("id", flat=True))
            queryset_id.extend(
                list(
                    queryset.filter(is_active=True)
                    .exclude(statement__in=draft_statements)
                    .values_list("id", flat=True)
                )
            )
            return queryset.filter(id__in=queryset_id)
        return queryset.filter(version=value)


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
            draft_question_statements = queryset.filter(version="draft")
            draft_statements = draft_question_statements.values_list(
                "statement", flat=True
            )
            queryset_id = list(draft_question_statements.values_list("id", flat=True))
            queryset_id.extend(
                list(
                    queryset.filter(is_active=True)
                    .exclude(statement__in=draft_statements)
                    .values_list("id", flat=True)
                )
            )
            return queryset.filter(id__in=queryset_id)
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
            draft_option_statements = queryset.filter(version="draft")
            draft_statements = draft_option_statements.values_list(
                "statement", flat=True
            )
            queryset_id = list(draft_option_statements.values_list("id", flat=True))
            queryset_id.extend(
                list(
                    queryset.filter(is_active=True)
                    .exclude(statement__in=draft_statements)
                    .values_list("id", flat=True)
                )
            )
            return queryset.filter(id__in=queryset_id)
        return queryset.filter(version=value)
