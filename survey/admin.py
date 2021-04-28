from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import (
    Answer,
    AnswerMitigation,
    AnswerOpportunity,
    AnswerStatement,
    Question,
    QuestionCategory,
    QuestionContext,
)


@admin.register(QuestionContext)
class QuestionContextAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "move_up_down_links")
    search_fields = (
        "code",
        "title",
    )


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "context", "move_up_down_links")
    autocomplete_fields = ("context",)
    search_fields = (
        "code",
        "title",
    )


@admin.register(Question)
class QuestionAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = (
        "code",
        "title",
        "hints",
        "category",
        "can_select_multiple_answer",
        "move_up_down_links",
    )
    autocomplete_fields = ("category",)
    search_fields = (
        "code",
        "title",
    )


@admin.register(Answer)
class AnswerAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "question", "move_up_down_links")
    autocomplete_fields = ("question",)
    search_fields = (
        "code",
        "title",
    )


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
