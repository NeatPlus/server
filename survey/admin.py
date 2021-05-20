from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Answer, Question, QuestionCategory


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "module", "move_up_down_links")
    autocomplete_fields = ("module",)
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
