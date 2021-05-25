from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import TimeStampedModel, UserStampedModel


class FrequentlyAskedQuestion(UserStampedModel, TimeStampedModel, OrderedModel):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta(OrderedModel.Meta):
        pass
