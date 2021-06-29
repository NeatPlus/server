from django.db import models

from neatplus.models import TimeStampedModel, UserStampedModel


class SurveyResult(UserStampedModel, TimeStampedModel):
    statement = models.ForeignKey("statement.Statement", on_delete=models.CASCADE)
    survey = models.ForeignKey(
        "survey.Survey", on_delete=models.CASCADE, related_name="results"
    )
    score = models.FloatField()
