from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Answer, Question, QuestionCategory, QuestionContext


@admin.register(QuestionContext)
class QuestionContextAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
    SimpleHistoryAdmin,
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
    SimpleHistoryAdmin,
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
    SimpleHistoryAdmin,
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
    SimpleHistoryAdmin,
):
    list_display = ("code", "title", "question", "move_up_down_links")
    autocomplete_fields = ("question",)
    search_fields = (
        "code",
        "title",
    )
