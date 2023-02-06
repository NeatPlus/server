from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone

from neatplus.utils import gen_random_number
from support.models import EmailTemplate

from .models import EmailConfirmationPin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_email_confiramtion_pin(sender, instance, created, **kwargs):
    if created:
        six_digit_pin = gen_random_number(6)
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
        email_confirm_object, _created = EmailConfirmationPin.objects.update_or_create(
            user=instance,
            defaults={
                "pin": six_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
            },
        )
        subject, html_message, text_message = EmailTemplate.objects.get(
            identifier="email_confirm"
        ).get_email_contents(
            {"user": instance, "email_confirm_object": email_confirm_object}
        )
        instance.email_user(subject, text_message, html_message=html_message)
