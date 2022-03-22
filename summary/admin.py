from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from neatplus.admin import UserStampedModelAdmin

from .models import SurveyResult, SurveyResultFeedback


@admin.register(SurveyResult)
class SurveyResultAdmin(UserStampedModelAdmin):
    list_display = ("statement", "survey", "module", "question_group", "score")
    autocomplete_fields = ("statement", "survey", "module", "question_group")
    search_fields = ("__str__",)

    class Meta:
        verbose_name = _("survey result")
        verbose_plural_name = _("survey results")


@admin.register(SurveyResultFeedback)
class SurveyResultAdmin(UserStampedModelAdmin):
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
