from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from support.models import EmailTemplate

from .models import Organization, OrganizationMemberRequest


@receiver(post_save, sender=Organization)
def send_organization_acceptance_change_mail(sender, instance, created, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields and "status" in update_fields:
        if instance.status == "accepted":
            email = EmailTemplate.objects.get(identifier="accept_organization")
        elif instance.status == "rejected":
            email = EmailTemplate.objects.get(identifier="reject_organization")
        else:
            return
        for admin in instance.admins.all().distinct():
            subject, html_message, text_message = email.get_email_contents(
                {"organization": instance, "admin": admin}
            )
            admin.celery_email_user(subject, text_message, html_message=html_message)
            admin.notify(
                instance.updated_by,
                instance.status,
                action_object=instance,
                notification_type=f"organization_{instance.status}",
            )


@receiver(post_save, sender=OrganizationMemberRequest)
def send_new_member_request_organization_admin(sender, instance, created, **kwargs):
    if created or "status" in kwargs["update_fields"]:
        if not created and instance.status != "pending":
            return
        for admin in instance.organization.admins.all().distinct():
            subject, html_message, text_message = EmailTemplate.objects.get(
                identifier="new_member_request"
            ).get_email_contents({"admin": admin, "member_request": instance})
            admin.celery_email_user(subject, text_message, html_message=html_message)
            admin.notify(
                instance.created_by,
                "created",
                action_object=instance,
                target=instance.organization,
                notification_type="new_member_request",
            )


@receiver(post_save, sender=OrganizationMemberRequest)
def send_member_request_acceptance_change_mail(sender, instance, created, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields and "status" in update_fields:
        if instance.status == "accepted":
            subject, html_message, text_message = EmailTemplate.objects.get(
                identifier="accept_member_request"
            ).get_email_contents({"member_request": instance})
        elif instance.status == "rejected":
            subject, html_message, text_message = EmailTemplate.objects.get(
                identifier="reject_member_request"
            ).get_email_contents({"member_request": instance})
        else:
            return
        instance.created_by.celery_email_user(
            subject, text_message, html_message=html_message
        )
        instance.created_by.notify(
            instance.organization,
            instance.status,
            notification_type=f"member_request_{instance.status}",
        )


@receiver(post_save, sender=OrganizationMemberRequest)
def change_organization_members_list(sender, instance, created, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields and "status" in update_fields:
        if instance.status == "accepted":
            instance.organization.members.add(instance.user)
        elif instance.status == "rejected":
            instance.organization.members.remove(instance.user)
        else:
            return
