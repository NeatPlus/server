from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Option, Question, QuestionGroup, Survey, SurveyAnswer


@admin.register(QuestionGroup)
class QuestionGroupAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "move_up_down_links")
    search_fields = (
        "code",
        "title",
    )


class OptionInline(admin.StackedInline):
    model = Option
    extra = 0


@admin.register(Question)
class QuestionAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = (
        "code",
        "title",
        "group",
        "answer_type",
        "module",
        "is_required",
        "move_up_down_links",
    )
    autocomplete_fields = ("group", "module")
    search_fields = (
        "code",
        "title",
    )
    inlines = (OptionInline,)


@admin.register(Option)
class OptionAdmin(
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


class ProjectAutoCompleteFilter(AutocompleteFilter):
    title = "Project"
    field_name = "project"


@admin.register(Survey)
class SurveyAdmin(UserStampedModelAdmin, OrderedModelAdmin):
    list_display = ("title", "project", "is_shared_publicly", "move_up_down_links")
    list_filter = (ProjectAutoCompleteFilter,)
    autocomplete_fields = ("project",)
    search_fields = ("title",)


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(UserStampedModelAdmin):
    list_display = ("question", "survey", "answer")
    autocomplete_fields = ("question", "survey", "options")
