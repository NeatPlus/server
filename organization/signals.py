from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import get_template

from .models import Project


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
