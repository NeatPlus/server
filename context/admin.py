from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import Context, Module


@admin.register(Context)
class ContextAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "move_up_down_links")
    search_fields = (
        "code",
        "title",
    )

    class Meta:
        verbose_name = _("context")
        verbose_plural_name = _("contexts")


@admin.register(Module)
class ModuleAdmin(
    UserStampedModelAdmin,
    TranslationAdmin,
    OrderedModelAdmin,
):
    list_display = ("code", "title", "context", "move_up_down_links")
    autocomplete_fields = ("context",)
    search_fields = (
        "code",
        "title",
    )

    class Meta:
        verbose_name = _("module")
        verbose_plural_name = _("modules")
