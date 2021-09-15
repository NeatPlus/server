from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class QuestionGroup(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    skip_logic = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class AnswerTypeChoices(models.TextChoices):
    BOOLEAN = "boolean"
    DATE = "date"
    DESCRIPTION = "description"
    SINGLE_IMAGE = "single_image"
    MULTIPLE_IMAGE = "multiple_image"
    LOCATION = "location"
    NUMBER = "number"
    TEXT = "text"
    SINGLE_OPTION = "single_option"
    MULTIPLE_OPTION = "multiple_option"


class Question(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    description = RichTextUploadingField(blank=True, null=True, default=None)
    hints = models.TextField(blank=True, null=True, default=None)
    answer_type = models.CharField(max_length=15, choices=AnswerTypeChoices.choices)
    group = models.ForeignKey(
        "QuestionGroup", on_delete=models.CASCADE, related_name="questions"
    )
    module = models.ForeignKey(
        "context.Module",
        on_delete=models.PROTECT,
        related_name="questions",
        null=True,
        blank=True,
        default=None,
    )
    is_required = models.BooleanField(default=True)
    skip_logic = models.TextField(null=True, blank=True, default=None)
    acronym = models.CharField(max_length=100, null=True, blank=True, default=None)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Option(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="options"
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Survey(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    config = models.JSONField(default=dict)
    is_shared_publicly = models.BooleanField(default=False)
    shared_link_identifier = models.CharField(
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
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    survey = models.ForeignKey(
        "Survey", on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.TextField(null=True, blank=True, default=None)
    answer_type = models.CharField(max_length=15, choices=AnswerTypeChoices.choices)
    options = models.ManyToManyField("Option", blank=True)
