from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import FrequentlyAskedQuestion


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(
    UserStampedModelAdmin, OrderedModelAdmin, TranslationAdmin
):
    list_display = ("question", "move_up_down_links")
