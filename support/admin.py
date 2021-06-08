from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin
from ordered_model.models import OrderedModel

from neatplus.admin import UserStampedModelAdmin

from .models import Action, FrequentlyAskedQuestion, Resource, ResourceTag


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(
    UserStampedModelAdmin, OrderedModelAdmin, TranslationAdmin
):
    list_display = ("question", "move_up_down_links")


@admin.register(ResourceTag)
class ResourceTagAdmin(UserStampedModelAdmin, OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")
    search_fields = ("title",)


@admin.register(Resource)
class ResourceAdmin(UserStampedModelAdmin, OrderedModelAdmin, TranslationAdmin):
    list_display = (
        "title",
        "resource_type",
        "video_url",
        "attachment",
        "move_up_down_links",
    )
    autocomplete_fields = ("tags",)


@admin.register(Action)
class ActionAdmin(UserStampedModelAdmin, OrderedModelAdmin, TranslationAdmin):
    list_display = ("title", "context", "organization", "point", "move_up_down_links")
    autocomplete_fields = ("context",)
