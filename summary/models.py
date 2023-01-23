from django.db import models
from django.utils.translation import gettext_lazy as _

from neatplus.models import TimeStampedModel, UserStampedModel


class SurveyResult(UserStampedModel, TimeStampedModel):
    statement = models.ForeignKey(
        "statement.Statement", on_delete=models.CASCADE, verbose_name=_("statement")
    )
    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name=_("survey"),
    )
    module = models.ForeignKey(
        "context.Module",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name=_("module"),
    )
    question_group = models.ForeignKey(
        "survey.QuestionGroup",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name=_("question group"),
        null=True,
        blank=True,
        default=None,
    )
    score = models.FloatField(_("score"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["statement", "survey", "module"],
                condition=models.Q(question_group__isnull=True),
                name="unique_module_survey_statement",
            ),
            models.UniqueConstraint(
                fields=["statement", "survey", "module", "question_group"],
                condition=models.Q(question_group__isnull=False),
                name="unique_module_survey_question_group_statement",
            ),
        ]
        permissions = [("add_baseline_feedback", _("Can add baseline feedback"))]

    def __str__(self):
        return self.statement.code + "-" + str(self.survey) + "-" + str(self.module)

    def save(self, *args, **kwargs):
        if self.pk:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    old_val = getattr(old, field_name)
                    new_val = getattr(self, field_name)
                    if hasattr(field, "is_custom_lower_field"):
                        if field.is_custom_lower_field():
                            new_val = new_val.lower()
                    if old_val != new_val:
                        changed_fields.append(field_name)
                except Exception:
                    pass
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)


class SurveyResultFeedback(UserStampedModel, TimeStampedModel):
    class StatusChoice(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACKNOWLEDGED = "acknowledged", _("Acknowledged")

    survey_result = models.ForeignKey(
        "SurveyResult",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name=_("survey result"),
    )
    actual_score = models.FloatField(_("actual score"))
    expected_score = models.FloatField(_("expected score"))
    comment = models.TextField(_("comment"), null=True, blank=True, default=None)
    status = models.CharField(
        max_length=12, choices=StatusChoice.choices, default=StatusChoice.PENDING
    )
    is_baseline = models.BooleanField(_("baseline"), default=False)
