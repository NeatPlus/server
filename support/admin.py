from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from neatplus.admin import UserStampedModelAdmin

from .models import (
    Action,
    EmailTemplate,
    FrequentlyAskedQuestion,
    LegalDocument,
    Resource,
    ResourceTag,
)


@admin.register(LegalDocument)
class LegalDocumentAdmin(UserStampedModelAdmin, TranslationAdmin):
    list_display = ("document_type",)

    class Meta:
        verbose_name = _("legal document")
        verbose_plural_name = _("legal documents")


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(
    UserStampedModelAdmin, OrderedModelAdmin, TranslationAdmin
):
    list_display = ("question", "move_up_down_links")

    class Meta:
        verbose_name = _("frequently asked question")
        verbose_plural_name = _("frequently asked questions")


@admin.register(ResourceTag)
class ResourceTagAdmin(UserStampedModelAdmin, OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")
    search_fields = ("title",)

    class Meta:
        verbose_name = _("resource")
        verbose_plural_name = _("resource tags")


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

    class Meta:
        verbose_name = _("resource")
        verbose_plural_name = _("resources")


@admin.register(Action)
class ActionAdmin(UserStampedModelAdmin, OrderedModelAdmin, TranslationAdmin):
    list_display = ("title", "context", "organization", "point", "move_up_down_links")
    autocomplete_fields = ("context",)

    class Meta:
        verbose_name = _("action")
        verbose_plural_name = _("actions")


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("identifier",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Meta:
        verbose_name = _("email template")
        verbose_plural_name = _("email templates")
