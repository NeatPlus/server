from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from support.models import EmailTemplate
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
            subject, html_message, text_message = EmailTemplate.objects.get(
                identifier="new_project"
            ).get_email_contents({"admin": admin, "project": instance})
            admin.celery_email_user(subject, text_message, html_message=html_message)
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
            subject, html_message, text_message = EmailTemplate.objects.get(
                identifier="accept_project"
            ).get_email_contents({"project": instance})
        elif instance.status == "rejected":
            subject, html_message, text_message = EmailTemplate.objects.get(
                identifier="reject_project"
            ).get_email_contents({"project": instance})
        else:
            return
        context = {"project": instance}
        instance.created_by.celery_email_user(
            subject, text_message, html_message=html_message
        )
        instance.created_by.notify(
            instance.organization,
            instance.status,
            action_object=instance,
            notification_type=f"project_{instance.status}",
        )
