from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class Context(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass


class Module(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    context = models.ForeignKey(
        "Context", on_delete=models.PROTECT, related_name="modules"
    )

    def __str__(self):
        return self.code + " " + self.title

    class Meta(OrderedModel.Meta):
        pass
