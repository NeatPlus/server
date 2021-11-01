from django.core.validators import FileExtensionValidator
from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class StatementTopic(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    icon = models.FileField(
        upload_to="statement/statement_topic/icons",
        validators=[FileExtensionValidator(allowed_extensions=["svg", "png"])],
        null=True,
        blank=True,
        default=None,
    )
    description = models.TextField(null=True, blank=True, default=None)
    context = models.ForeignKey(
        "context.Context", on_delete=models.PROTECT, related_name="statement_topics"
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class StatementTagGroup(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class StatementTag(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(
        "StatementTagGroup", on_delete=models.CASCADE, related_name="tags"
    )

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class Statement(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)
    topic = models.ForeignKey(
        "StatementTopic", on_delete=models.PROTECT, related_name="statements"
    )
    tags = models.ManyToManyField(
        "StatementTag",
        related_name="statements",
    )
    questions = models.ManyToManyField(
        "survey.Question", related_name="statements", through="QuestionStatement"
    )
    options = models.ManyToManyField(
        "survey.Option", related_name="statements", through="OptionStatement"
    )
    is_experimental = models.BooleanField(default=False)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Mitigation(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, related_name="mitigations"
    )
    options = models.ManyToManyField(
        "survey.Option", related_name="mitigations", through="OptionMitigation"
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Opportunity(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, related_name="opportunities"
    )
    options = models.ManyToManyField(
        "survey.Option", related_name="opportunities", through="OptionOpportunity"
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Opportunities"


class QuestionStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    question = models.ForeignKey("survey.Question", on_delete=models.CASCADE)
    statement = models.ForeignKey("Statement", on_delete=models.CASCADE)
    weightage = models.FloatField()

    def __str__(self):
        return (
            "Question:"
            + str(self.question.pk)
            + "-"
            + "Statement:"
            + str(self.statement.pk)
        )

    class Meta(OrderedModel.Meta):
        pass


class OptionStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    option = models.ForeignKey("survey.Option", on_delete=models.CASCADE)
    statement = models.ForeignKey("Statement", on_delete=models.CASCADE)
    weightage = models.FloatField()

    def __str__(self):
        return (
            "Option:"
            + str(self.option.pk)
            + "-"
            + "Statement:"
            + str(self.statement.pk)
        )

    class Meta(OrderedModel.Meta):
        pass


class OptionMitigation(UserStampedModel, TimeStampedModel, OrderedModel):
    option = models.ForeignKey("survey.Option", on_delete=models.CASCADE)
    mitigation = models.ForeignKey("Mitigation", on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Option:"
            + str(self.option.pk)
            + "-"
            + "Mitigation:"
            + str(self.mitigation.pk)
        )

    class Meta(OrderedModel.Meta):
        pass


class OptionOpportunity(UserStampedModel, TimeStampedModel, OrderedModel):
    option = models.ForeignKey("survey.Option", on_delete=models.CASCADE)
    opportunity = models.ForeignKey("Opportunity", on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Option:"
            + str(self.option.pk)
            + "-"
            + "Opportunity:"
            + str(self.opportunity.pk)
        )

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Option Opportunities"
