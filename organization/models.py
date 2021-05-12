from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
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

    class StatusChoice(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="projects"
    )
    visibility = models.CharField(max_length=26, choices=VisibilityChoice.choices)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")
    status = models.CharField(
        max_length=8, choices=StatusChoice.choices, default="pending", editable=False
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
                    if getattr(old, field_name) != getattr(self, field_name):
                        changed_fields.append(field_name)
                except Exception as e:
                    pass
            kwargs["update_fields"] = changed_fields
            if "organization" in kwargs["update_fields"]:
                self.status = "pending"
        super().save(*args, **kwargs)


@receiver(post_save, sender=Project)
def send_new_project_organization_admin(sender, instance, created, **kwargs):
    if created:
        for admin in instance.organization.admins.all():
            email_template = get_template("new_project.txt")
            context = {"admin": admin, "project": instance}
            message = email_template.render(context)
            admin.email_user("New project mail", message)


@receiver(post_save, sender=Project)
def send_project_acceptance_change_mail(sender, instance, created, **kwargs):
    if not created and "status" in kwargs["update_fields"]:
        if instance.status == "accepted":
            email_template = get_template("accept_project.txt")
            subject = "Project acceptance mail"
        elif instance.status == "rejected":
            email_template = get_template("reject_project.txt")
            subject = "Project rejection mail"
        else:
            return
        context = {"project": instance}
        message = email_template.render(context)
        instance.created_by.email_user(subject, message)
