from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class Statement(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Mitigation(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Opportunity(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField()
    hints = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Opportunities"
