from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel

from neatplus.models import TimeStampedModel, UserStampedModel


class Project(TimeStampedModel, UserStampedModel, OrderedModel):
    class VisibilityChoice(models.TextChoices):
        PUBLIC = "public", _("Public")
        PUBLIC_WITHIN_ORGANIZATION = "public_within_organization", _(
            "Public Within Organization"
        )
        PRIVATE = "private", _("Private")

    class StatusChoice(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
        default=None,
        verbose_name=_("organization"),
    )
    visibility = models.CharField(
        _("visibility"), max_length=26, choices=VisibilityChoice.choices
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="projects",
        through="ProjectUser",
        through_fields=("project", "user"),
        verbose_name=_("users"),
    )
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING,
        editable=False,
    )
    context = models.ForeignKey(
        "context.Context",
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("context"),
    )
    share_analytics_with_neat = models.BooleanField(
        _("share analytics with NEAT"), default=False
    )

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.title

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
            if "organization" in changed_fields:
                self.status = "pending"
                changed_fields.append("status")
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)


class ProjectUser(UserStampedModel, TimeStampedModel):
    class SurveyPermissionChoice(models.TextChoices):
        WRITE = "write", _("Write")
        READ_ONLY = "read_only", _("Read Only")

    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, verbose_name=_("project")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user")
    )
    permission = models.CharField(
        _("permission"),
        max_length=9,
        choices=SurveyPermissionChoice.choices,
        default=SurveyPermissionChoice.READ_ONLY,
    )
