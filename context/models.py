from django.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class Context(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Module(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    context = models.ForeignKey(
        "Context",
        on_delete=models.PROTECT,
        related_name="modules",
        verbose_name=_("context"),
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass
