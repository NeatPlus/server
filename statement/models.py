from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel

from neatplus.models import CodeModel, TimeStampedModel, UserStampedModel


class StatementTopic(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)
    icon = models.FileField(
        _("icon"),
        upload_to="statement/statement_topic/icons",
        validators=[FileExtensionValidator(allowed_extensions=["svg", "png"])],
        null=True,
        blank=True,
        default=None,
    )
    description = models.TextField(
        _("description"), null=True, blank=True, default=None
    )
    context = models.ForeignKey(
        "context.Context",
        on_delete=models.PROTECT,
        related_name="statement_topics",
        verbose_name=_("context"),
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class StatementTagGroup(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class StatementTag(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(_("title"), max_length=255)
    group = models.ForeignKey(
        "StatementTagGroup",
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name=_("statement tag group"),
    )

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class Statement(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    hints = models.TextField(_("hints"), null=True, blank=True, default=None)
    topic = models.ForeignKey(
        "StatementTopic",
        on_delete=models.PROTECT,
        related_name="statements",
        verbose_name=_("statement topic"),
    )
    tags = models.ManyToManyField(
        "StatementTag", related_name="statements", verbose_name=_("statement tags")
    )
    questions = models.ManyToManyField(
        "survey.Question",
        related_name="statements",
        through="QuestionStatement",
        verbose_name=_("questions"),
    )
    options = models.ManyToManyField(
        "survey.Option",
        related_name="statements",
        through="OptionStatement",
        verbose_name=_("options"),
    )
    is_experimental = models.BooleanField(_("experimental"), default=False)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Mitigation(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    statement = models.ForeignKey(
        "Statement",
        on_delete=models.CASCADE,
        related_name="mitigations",
        verbose_name=_("statement"),
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Opportunity(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    statement = models.ForeignKey(
        "Statement",
        on_delete=models.CASCADE,
        related_name="opportunities",
        verbose_name=_("statement"),
    )

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Opportunities"


class QuestionStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    question = models.ForeignKey(
        "survey.Question", on_delete=models.CASCADE, verbose_name=_("question")
    )
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, verbose_name=_("statement")
    )
    weightage = models.FloatField(_("weightage"))
    version = models.CharField(_("version"), max_length=255)
    is_active = models.BooleanField(_("active"), default=False, editable=False)

    def __str__(self):
        return (
            "Question:"
            + str(self.question.pk)
            + "-"
            + "Statement:"
            + str(self.statement.pk)
        )

    class Meta(OrderedModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["question", "statement", "version"],
                name="unique_version_question_statement",
            ),
            models.UniqueConstraint(
                fields=["question", "statement"],
                condition=models.Q(is_active=True),
                name="one_active_question_statement",
            ),
        ]


class OptionStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    option = models.ForeignKey(
        "survey.Option", on_delete=models.CASCADE, verbose_name=_("option")
    )
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, verbose_name=_("statement")
    )
    weightage = models.FloatField(_("weightage"))
    version = models.CharField(_("version"), max_length=255)
    is_active = models.BooleanField(_("active"), default=False, editable=False)

    def __str__(self):
        return (
            "Option:"
            + str(self.option.pk)
            + "-"
            + "Statement:"
            + str(self.statement.pk)
        )

    class Meta(OrderedModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["option", "statement", "version"],
                name="unique_version_option_statement",
            ),
            models.UniqueConstraint(
                fields=["option", "statement"],
                condition=models.Q(is_active=True),
                name="one_active_option_statement",
            ),
        ]
