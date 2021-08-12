from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import get_template

from user.models import User

from .models import Project


@receiver(post_save, sender=Project)
def send_new_project_notification_to_admin(sender, instance, created, **kwargs):
    if created or "status" in kwargs["update_fields"]:
        if not created and instance.status != "pending":
            return
        if instance.organization:
            admins = instance.organization.admins.all()
        else:
            admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            email_template = get_template("mail/new_project.txt")
            context = {"admin": admin, "project": instance}
            message = email_template.render(context)
            admin.celery_email_user("New project mail", message)
            admin.notify(
                instance.created_by,
                "created",
                action_object=instance,
                target=instance.organization,
                notification_type="new_project",
            )


@receiver(post_save, sender=Project)
def send_project_acceptance_change_mail(sender, instance, created, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields and "status" in update_fields:
        if instance.status == "accepted":
            email_template = get_template("mail/accept_project.txt")
            subject = "Project acceptance mail"
        elif instance.status == "rejected":
            email_template = get_template("mail/reject_project.txt")
            subject = "Project rejection mail"
        else:
            return
        context = {"project": instance}
        message = email_template.render(context)
        instance.created_by.celery_email_user(subject, message)
        instance.created_by.notify(
            instance.organization,
            instance.status,
            action_object=instance,
            notification_type=f"project_{instance.status}",
        )
