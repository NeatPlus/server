from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Option, Question, QuestionGroup, Survey, SurveyAnswer


class ModuleAutoCompleteFilter(AutocompleteFilter):
    title = "module"
    field_name = "module"


@admin.register(QuestionGroup)
class QuestionGroupAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "module", "move_up_down_links")
    list_filter = (ModuleAutoCompleteFilter,)
    autocomplete_fields = ("module",)
    search_fields = (
        "code",
        "title",
    )

    class Meta:
        verbose_name = _("question group")
        verbose_plural_name = _("question groups")


class OptionInline(admin.StackedInline):
    model = Option
    extra = 0


class QuestionGroupAutoCompleteFilter(AutocompleteFilter):
    title = "group"
    field_name = "group"


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
        "is_required",
        "move_up_down_links",
    )
    list_filter = (QuestionGroupAutoCompleteFilter,)
    autocomplete_fields = ("group",)
    search_fields = (
        "code",
        "title",
    )
    inlines = (OptionInline,)

    class Meta:
        verbose_name = _("question")
        verbose_plural_name = _("questions")


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

    class Meta:
        verbose_name = _("option")
        verbose_plural_name = _("options")


class ProjectAutoCompleteFilter(AutocompleteFilter):
    title = "Project"
    field_name = "project"


@admin.register(Survey)
class SurveyAdmin(UserStampedModelAdmin, OrderedModelAdmin):
    list_display = ("title", "project", "is_shared_publicly", "move_up_down_links")
    list_filter = (ProjectAutoCompleteFilter,)
    autocomplete_fields = ("project",)
    search_fields = ("title",)

    class Meta:
        verbose_name = _("survey")
        verbose_plural_name = _("surveys")


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(UserStampedModelAdmin):
    list_display = ("question", "survey", "answer")
    autocomplete_fields = ("question", "survey", "options")

    class Meta:
        verbose_name = _("survey answer")
        verbose_plural_name = _("survey answers")
