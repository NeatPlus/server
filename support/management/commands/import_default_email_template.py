from base64 import b32encode

import qrcode
import yaml
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django_otp.plugins.otp_totp.models import TOTPDevice

from support.models import EmailTemplate


class Command(BaseCommand):
    help = "Import default email"

    def handle(self, *args, **options):
        with open("support/content/email.yaml") as yaml_file:
            email_object_contents = yaml.safe_load(yaml_file)
            for email_object_content in email_object_contents:
                fields = email_object_content["fields"]
                identifier = fields.pop("identifier")
                email, created = EmailTemplate.objects.get_or_create(
                    identifier=identifier, defaults=fields
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Imported email with identifier {email.identifier}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"EmailTemplate with identifier {email.identifier} already present"
                        )
                    )
