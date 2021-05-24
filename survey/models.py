from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class QuestionGroup(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.code + " " + self.title


class AnswerTypeChoices(models.TextChoices):
    CHECK_BOX = "check_box"
    DATE = "date"
    DESCRIPTION = "description"
    IMAGE = "image"
    LOCATION = "location"
    NUMBER = "number"
    SINGLE_OPTION = "single_option"
    MULTIPLE_OPTION = "multiple_option"


class Question(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):

    title = models.TextField()
    description = models.TextField(blank=True, null=True, default=None)
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

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Option(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="options"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Survey(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class SurveyAnswer(UserStampedModel, TimeStampedModel):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    survey = models.ForeignKey("Survey", on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True, default=None)
    answer_type = models.CharField(max_length=15, choices=AnswerTypeChoices.choices)
    options = models.ManyToManyField("Option", blank=True)
