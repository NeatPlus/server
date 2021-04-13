from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class QuestionContext(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class QuestionCategory(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=50)
    context = models.ForeignKey(
        QuestionContext, on_delete=models.PROTECT, related_name="categories"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Question Categories"


class Question(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(blank=True, null=True, default=None)
    can_select_multiple_answer = models.BooleanField(default=False)
    category = models.ForeignKey(
        QuestionCategory, on_delete=models.PROTECT, related_name="questions"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Answer(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name="answers"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass
