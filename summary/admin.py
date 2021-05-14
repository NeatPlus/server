from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Mitigation, Opportunity, Statement, StatementTopic


@admin.register(StatementTopic)
class StatementTopicAdmin(UserStampedModelAdmin, TranslationAdmin, OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")
    search_fields = ("title",)


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
