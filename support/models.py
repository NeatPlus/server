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


class ResourceTag(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=50)

    class Meta(OrderedModel.Meta):
        pass


class Resource(UserStampedModel, TimeStampedModel, OrderedModel):
    class ResourceTypeChoices(models.TextChoices):
        ATTACHMENT = "attachment"
        VIDEO = "video"

    title = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.CharField(max_length=10, choices=ResourceTypeChoices.choices)
    video_url = models.URLField(null=True, blank=True, default=None)
    attachment = models.FileField(null=True, blank=True, default=None)
    tags = models.ManyToManyField("ResourceTag", related_name="resources")

    class Meta(OrderedModel.Meta):
        pass
