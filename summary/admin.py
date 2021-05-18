from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import (
    AnswerMitigation,
    AnswerOpportunity,
    AnswerStatement,
    Mitigation,
    Opportunity,
    Statement,
    StatementTopic,
)


@admin.register(StatementTopic)
class StatementTopicAdmin(UserStampedModelAdmin, TranslationAdmin, OrderedModelAdmin):
    list_display = ("title", "context", "move_up_down_links")
    search_fields = ("title",)
    autocomplete_fields = ("context",)


@admin.register(Statement)
class StatementAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = (
        "code",
        "topic",
        "title",
        "move_up_down_links",
    )
    search_fields = (
        "code",
        "title",
    )
    autocomplete_fields = ("topic",)


@admin.register(Mitigation)
class MitigationAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = (
        "code",
        "statement",
        "title",
        "move_up_down_links",
    )
    search_fields = (
        "code",
        "title",
    )
    autocomplete_fields = ("statement",)


@admin.register(Opportunity)
class OpportunityAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = (
        "code",
        "statement",
        "title",
        "move_up_down_links",
    )
    search_fields = (
        "code",
        "title",
    )
    autocomplete_fields = ("statement",)


@admin.register(AnswerStatement)
class AnswerStatementAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("answer", "statement", "move_up_down_links")
    autocomplete_fields = ("answer", "statement")


@admin.register(AnswerMitigation)
class AnswerMitigationAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("answer", "mitigation", "move_up_down_links")
    autocomplete_fields = ("answer", "mitigation")


@admin.register(AnswerOpportunity)
class AnswerOpportunityAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("answer", "opportunity", "move_up_down_links")
    autocomplete_fields = ("answer", "opportunity")
