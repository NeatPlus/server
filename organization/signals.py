from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import get_template

from .models import Organization, OrganizationMemberRequest


@receiver(post_save, sender=Organization)
def send_organization_acceptance_change_change_mail(
    sender, instance, created, **kwargs
):
    update_fields = kwargs.get("update_fields")
    if update_fields and "status" in update_fields:
        if instance.status == "accepted":
            email_template = get_template("accept_organization.txt")
            subject = "Organization acceptance mail"
        elif instance.status == "rejected":
            email_template = get_template("reject_organization.txt")
            subject = "Organization rejection mail"
        else:
            return
        for admin in instance.admins.all():
            context = {"organization": instance, "admin": admin}
            message = email_template.render(context)
            admin.email_user(subject, message)
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
        for admin in instance.organization.admins.all():
            email_template = get_template("new_member_request.txt")
            context = {"admin": admin, "member_request": instance}
            message = email_template.render(context)
            admin.email_user("New member request mail", message)
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
            email_template = get_template("accept_member_request.txt")
            subject = "Member request acceptance mail"
        elif instance.status == "rejected":
            email_template = get_template("reject_member_request.txt")
            subject = "Member request rejection mail"
        else:
            return
        context = {"member_request": instance}
        message = email_template.render(context)
        instance.created_by.email_user(subject, message)
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
