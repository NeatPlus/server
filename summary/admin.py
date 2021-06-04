from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import (
    Mitigation,
    Opportunity,
    OptionMitigation,
    OptionOpportunity,
    OptionStatement,
    QuestionStatement,
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


@admin.register(QuestionStatement)
class QuestionStatementAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("question", "statement", "move_up_down_links")
    autocomplete_fields = ("question", "statement")


@admin.register(OptionStatement)
class OptionStatementAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("option", "statement", "move_up_down_links")
    autocomplete_fields = ("option", "statement")


@admin.register(OptionMitigation)
class OptionMitigationAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("option", "mitigation", "move_up_down_links")
    autocomplete_fields = ("option", "mitigation")


@admin.register(OptionOpportunity)
class OptionOpportunityAdmin(
    UserStampedModelAdmin,
    OrderedModelAdmin,
):
    list_display = ("option", "opportunity", "move_up_down_links")
    autocomplete_fields = ("option", "opportunity")
