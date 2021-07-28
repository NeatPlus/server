from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.gis.db.models import PointField
from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import TimeStampedModel, UserStampedModel


class LegalDocumentTypeChoice(models.TextChoices):
    TERMS_AND_CONDITIONS = "terms-and-conditions"
    PRIVACY_POLICY = "privacy-policy"


class LegalDocument(UserStampedModel, TimeStampedModel):

    document_type = models.CharField(
        max_length=20, choices=LegalDocumentTypeChoice.choices, unique=True
    )
    description = RichTextField()

    def __str__(self):
        return self.document_type

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
