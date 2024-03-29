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


class PriorityTypeChoice(models.TextChoices):
    HIGH = "high", _("High")
    MEDIUM = "medium", _("Medium")
    LOW = "low", _("Low")


class ImplementorTypeChoice(models.TextChoices):
    LOCAL = "local", _("Local")
    REGIONAL = "regional", _("Regional")
    HQ = "hq", _("HQ")
    ALL = "all", _("All")


class Mitigation(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    statements = models.ManyToManyField(
        "Statement",
        related_name="mitigations",
        verbose_name=_("statements"),
        blank=True,
    )
    options = models.ManyToManyField(
        "survey.Option",
        related_name="mitigations",
        verbose_name=_("options"),
        blank=True,
    )
    priority = models.CharField(
        _("priority"),
        max_length=6,
        choices=PriorityTypeChoice.choices,
        null=True,
        blank=True,
        default=None,
    )
    implementor = models.CharField(
        _("implementor"),
        max_length=8,
        choices=ImplementorTypeChoice.choices,
        null=True,
        blank=True,
        default=None,
    )
    rank = models.PositiveIntegerField(_("rank"), null=True, blank=True, default=None)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        pass


class Opportunity(CodeModel, UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"))
    statements = models.ManyToManyField(
        "Statement",
        related_name="opportunities",
        verbose_name=_("statements"),
        blank=True,
    )
    options = models.ManyToManyField(
        "survey.Option",
        related_name="opportunities",
        verbose_name=_("options"),
        blank=True,
    )
    priority = models.CharField(
        _("priority"),
        max_length=6,
        choices=PriorityTypeChoice.choices,
        null=True,
        blank=True,
        default=None,
    )
    implementor = models.CharField(
        _("implementor"),
        max_length=8,
        choices=ImplementorTypeChoice.choices,
        null=True,
        blank=True,
        default=None,
    )
    rank = models.PositiveIntegerField(_("rank"), null=True, blank=True, default=None)

    def __str__(self):
        return self.code + "-" + self.title

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "opportunities"


class StatementFormula(UserStampedModel, TimeStampedModel):
    statement = models.ForeignKey(
        "Statement",
        on_delete=models.CASCADE,
        verbose_name=_("statement"),
        related_name="formulas",
    )
    question_group = models.ForeignKey(
        "survey.QuestionGroup",
        on_delete=models.CASCADE,
        verbose_name=_("question group"),
        related_name="formulas",
        null=True,
        blank=True,
        default=None,
    )
    module = models.ForeignKey(
        "context.Module",
        on_delete=models.CASCADE,
        verbose_name=_("module"),
        related_name="formulas",
    )
    formula = models.TextField(_("formula"))
    version = models.CharField(_("version"), max_length=255)
    is_active = models.BooleanField(_("active"), default=False, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["statement", "version"],
                condition=models.Q(question_group__isnull=True),
                name="one_version_formula_statement",
            ),
            models.UniqueConstraint(
                fields=["statement"],
                condition=models.Q(is_active=True)
                & models.Q(question_group__isnull=True),
                name="one_active_version_formula_statement",
            ),
            models.UniqueConstraint(
                fields=["question_group", "statement", "version"],
                condition=models.Q(question_group__isnull=False),
                name="one_version_formula_question_group_statement",
            ),
            models.UniqueConstraint(
                fields=["question_group", "statement"],
                condition=models.Q(is_active=True)
                & models.Q(question_group__isnull=False),
                name="one_active_formula_question_group_statement",
            ),
        ]


class QuestionStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    question = models.ForeignKey(
        "survey.Question", on_delete=models.CASCADE, verbose_name=_("question")
    )
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, verbose_name=_("statement")
    )
    question_group = models.ForeignKey(
        "survey.QuestionGroup",
        on_delete=models.CASCADE,
        verbose_name=_("question group"),
        null=True,
        blank=True,
        default=None,
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
                condition=models.Q(question_group__isnull=True),
                name="unique_version_question_statement",
            ),
            models.UniqueConstraint(
                fields=["question", "statement"],
                condition=models.Q(is_active=True)
                & models.Q(question_group__isnull=True),
                name="one_active_question_statement",
            ),
            models.UniqueConstraint(
                fields=["question", "statement", "question_group", "version"],
                condition=models.Q(question_group__isnull=False),
                name="unique_version_question_question_group_statement",
            ),
            models.UniqueConstraint(
                fields=["question", "statement", "question_group"],
                condition=models.Q(is_active=True)
                & models.Q(question_group__isnull=False),
                name="one_active_question_question_group_statement",
            ),
        ]


class OptionStatement(UserStampedModel, TimeStampedModel, OrderedModel):
    option = models.ForeignKey(
        "survey.Option", on_delete=models.CASCADE, verbose_name=_("option")
    )
    statement = models.ForeignKey(
        "Statement", on_delete=models.CASCADE, verbose_name=_("statement")
    )
    question_group = models.ForeignKey(
        "survey.QuestionGroup",
        on_delete=models.CASCADE,
        verbose_name=_("question group"),
        null=True,
        blank=True,
        default=None,
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
                condition=models.Q(question_group__isnull=True),
                name="unique_version_option_statement",
            ),
            models.UniqueConstraint(
                fields=["option", "statement"],
                condition=models.Q(is_active=True)
                & models.Q(question_group__isnull=True),
                name="one_active_option_statement",
            ),
            models.UniqueConstraint(
                fields=["option", "statement", "question_group", "version"],
                condition=models.Q(question_group__isnull=False),
                name="unique_version_option_question_group_statement",
            ),
            models.UniqueConstraint(
                fields=["option", "statement", "question_group"],
                condition=models.Q(is_active=True)
                & models.Q(question_group__isnull=False),
                name="one_active_option_question_group_statement",
            ),
        ]
