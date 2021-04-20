from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Mitigation, Opportunity, Statement


@admin.register(Statement)
class StatementAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "code",
        "title",
        "hints",
        "move_up_down_links",
    )
    search_fields = (
        "code",
        "title",
    )


@admin.register(Mitigation)
class MitigationAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "code",
        "title",
        "hints",
        "move_up_down_links",
    )
    search_fields = (
        "code",
        "title",
    )


@admin.register(Opportunity)
class OpportunityAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "code",
        "title",
        "hints",
        "move_up_down_links",
    )
    search_fields = (
        "code",
        "title",
    )
