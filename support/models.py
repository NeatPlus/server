from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.gis.db.models import PointField
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

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class Action(UserStampedModel, TimeStampedModel, OrderedModel):
    title = models.CharField(max_length=255)
    context = models.ForeignKey(
        "context.Context",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        default=None,
        related_name="actions",
    )
    organization = models.CharField(max_length=255)
    summary = models.TextField()
    description = RichTextUploadingField()
    point = PointField()

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass
