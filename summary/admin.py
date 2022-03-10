from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from neatplus.admin import UserStampedModelAdmin

from .models import SurveyResult


@admin.register(SurveyResult)
class SurveyResultAdmin(UserStampedModelAdmin):
    list_display = ("statement", "survey", "module", "question_group", "score")
    autocomplete_fields = ("statement", "survey", "module", "question_group")

    class Meta:
        verbose_name = _("survey result")
        verbose_plural_name = _("survey results")
