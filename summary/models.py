from django.core.validators import FileExtensionValidator
from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class StatementTopic(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    icon = models.FileField(
        upload_to="summary/statement_topic/icons",
        validators=[FileExtensionValidator(allowed_extensions=["svg", "png"])],
    )
    context = models.ForeignKey(
        "survey.Context", on_delete=models.PROTECT, related_name="statement_topics"
    )

    def __str__(self):
        return self.code + " " + self.title


class Statement(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)
    topic = models.ForeignKey(
        "StatementTopic", on_delete=models.PROTECT, related_name="statements"
    )
    answers = models.ManyToManyField(
        "survey.Answer", related_name="statements", through="AnswerStatement"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Mitigation(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, related_name="mitigations"
    )
    answers = models.ManyToManyField(
        "survey.Answer", related_name="mitigations", through="AnswerMitigation"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Opportunity(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, related_name="opportunities"
    )
    answers = models.ManyToManyField(
        "survey.Answer", related_name="opportunities", through="AnswerOpportunity"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Opportunities"


class AnswerStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    answer = models.ForeignKey("survey.Answer", on_delete=models.CASCADE)
    statement = models.ForeignKey("Statement", on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Answer:"
            + str(self.answer.pk)
            + "-"
            + "Statement:"
            + str(self.statement.pk)
        )

    class Meta(OrderedModel.Meta):
        pass


class AnswerMitigation(UserStampedModel, TimeStampedModel, OrderedModel):
    answer = models.ForeignKey("survey.Answer", on_delete=models.CASCADE)
    mitigation = models.ForeignKey("Mitigation", on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Answer:"
            + str(self.answer.pk)
            + "-"
            + "Mitigation:"
            + str(self.mitigation.pk)
        )

    class Meta(OrderedModel.Meta):
        pass


class AnswerOpportunity(UserStampedModel, TimeStampedModel, OrderedModel):
    answer = models.ForeignKey("survey.Answer", on_delete=models.CASCADE)
    opportunity = models.ForeignKey("Opportunity", on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Answer:"
            + str(self.answer.pk)
            + "-"
            + "Opportunity:"
            + str(self.opportunity.pk)
        )

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Answer Opportunities"
