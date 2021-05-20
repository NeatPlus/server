from django.conf import settings
from django.db import models

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
