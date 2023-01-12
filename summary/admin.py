from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from neatplus.admin import UserStampedModelAdmin

from .models import SurveyResult, SurveyResultFeedback


class SurveyAutoCompleteFilter(AutocompleteFilter):
    title = "survey"
    field_name = "survey"


class StatementAutoCompleteFilter(AutocompleteFilter):
    title = "statement"
    field_name = "statement"


@admin.register(SurveyResult)
class SurveyResultAdmin(UserStampedModelAdmin):
    list_display = ("statement", "survey", "module", "question_group", "score")
    autocomplete_fields = ("statement", "survey", "module", "question_group")
    search_fields = ("__str__",)
    list_filter = (SurveyAutoCompleteFilter, StatementAutoCompleteFilter)

    class Meta:
        verbose_name = _("survey result")
        verbose_plural_name = _("survey results")


@admin.register(SurveyResultFeedback)
class SurveyResultFeedbackAdmin(UserStampedModelAdmin):
    list_display = (
        "survey_result",
        "actual_score",
        "expected_score",
        "status",
        "is_baseline",
    )
    autocomplete_fields = ("survey_result",)

    class Meta:
        verbose_name = _("survey result feeback")
        verbose_plural_name = _("survey result feedbacks")
