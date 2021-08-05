from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import get_template
from django.utils import timezone

from neatplus.utils import gen_random_number

from .models import EmailConfirmationPin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_email_confiramtion_pin(sender, instance, created, **kwargs):
    if created:
        six_digit_pin = gen_random_number(6)
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
        email_confirm_object, _ = EmailConfirmationPin.objects.update_or_create(
            user=instance,
            defaults={
                "pin": six_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
            },
        )
        email_template = get_template("email_confirm.txt")
        context = {"user": instance, "email_confirm_object": email_confirm_object}
        message = email_template.render(context)
        instance.celery_email_user("Email confirmation mail", message)
