from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class QuestionGroup(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)
    skip_logic = models.TextField(_("skip logic"), null=True, blank=True, default=None)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class AnswerTypeChoices(models.TextChoices):
    BOOLEAN = "boolean", _("Boolean")
    DATE = "date", _("Date")
    DESCRIPTION = "description", _("Description")
    SINGLE_IMAGE = "single_image", _("Single Image")
    MULTIPLE_IMAGE = "multiple_image", _("Multiple Image")
    LOCATION = "location", _("Location")
    NUMBER = "number", _("Number")
    TEXT = "text", _("Text")
    SINGLE_OPTION = "single_option", _("Single Option")
    MULTIPLE_OPTION = "multiple_option", _("Multiple Option")


class Question(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    description = RichTextUploadingField(
        _("description"), blank=True, null=True, default=None
    )
    hints = models.TextField(_("hints"), blank=True, null=True, default=None)
    answer_type = models.CharField(
        _("answer type"), max_length=15, choices=AnswerTypeChoices.choices
    )
    group = models.ForeignKey(
        "QuestionGroup",
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("question group"),
    )
    module = models.ForeignKey(
        "context.Module",
        on_delete=models.PROTECT,
        related_name="questions",
        null=True,
        blank=True,
        default=None,
        verbose_name=_("module"),
    )
    is_required = models.BooleanField(_("required"), default=True)
    skip_logic = models.TextField(_("skip logic"), null=True, blank=True, default=None)
    acronym = models.CharField(
        _("acronym"), max_length=100, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Option(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("question"),
    )
    mitigation = models.JSONField(_("mitigations"))
    opportunity = models.JSONField(_("opportunities"))

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Survey(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)
    project = models.ForeignKey(
        "project.Project",
        on_delete=models.CASCADE,
        related_name="surveys",
        verbose_name=_("project"),
    )
    config = models.JSONField(_("config"), default=dict)
    is_shared_publicly = models.BooleanField(_("shared publicly"), default=False)
    shared_link_identifier = models.CharField(
        _("shared link identifier"),
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        default=None,
        editable=False,
    )

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class SurveyAnswer(UserStampedModel, TimeStampedModel):
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        verbose_name=_("question"),
    )
    survey = models.ForeignKey(
        "Survey",
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("survey"),
    )
    answer = models.TextField(_("answer"), null=True, blank=True, default=None)
    answer_type = models.CharField(
        _("answer type"), max_length=15, choices=AnswerTypeChoices.choices
    )
    options = models.ManyToManyField("Option", blank=True, verbose_name=_("options"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "survey"],
                name="unique_survey_question",
            ),
        ]
