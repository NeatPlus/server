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
    score = models.FloatField(_("score"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["statement", "survey", "module"],
                name="unique_module_survey_statement",
            ),
        ]
