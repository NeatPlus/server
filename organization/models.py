from django.conf import settings
from django.db import models
from ordered_model.models import OrderedModel

from neatplus.models import TimeStampedModel, UserStampedModel


class Organization(TimeStampedModel, UserStampedModel):
    title = models.CharField(max_length=255, unique=True)
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="admin_organizations"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="member_organizations"
    )

    def __str__(self):
        return self.title


class Project(TimeStampedModel, UserStampedModel, OrderedModel):
    class VisibilityChoice(models.TextChoices):
        PUBLIC = "public"
        PUBLIC_WIITHIN_ORGANIZATION = "public_within_organization"
        PRIVATE = "private"

    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="projects"
    )
    visibility = models.CharField(max_length=26, choices=VisibilityChoice.choices)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")
    is_accepted_by_admin = models.BooleanField(default=False, editable=False)

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.title
