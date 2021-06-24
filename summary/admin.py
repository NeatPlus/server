from django.contrib import admin

from neatplus.admin import UserStampedModelAdmin

from .models import SurveyResult


@admin.register(SurveyResult)
class SurveyResultAdmin(UserStampedModelAdmin):
    list_display = ("statement", "survey", "score")
    autocomplete_fields = ("statement", "survey")
