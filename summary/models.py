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

    def __str__(self):
        return self.code + " " + self.title


class Statement(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)
    topic = models.ForeignKey(
        "StatementTopic", on_delete=models.PROTECT, related_name="statements"
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

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Opportunities"
