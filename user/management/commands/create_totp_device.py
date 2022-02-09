from base64 import b32encode

import qrcode
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django_otp.plugins.otp_totp.models import TOTPDevice


class Command(BaseCommand):
    help = "Create TOTP device for user"

    def add_arguments(self, parser):
        parser.add_argument(
            "user_id",
            type=int,
            help="ID of user that TOTP device belongs to",
        )
        parser.add_argument("device_name", help="Human redable name of device")
        parser.add_argument(
            "--print-full-url", action="store_true", help="Print full config url"
        )
        parser.add_argument("--print-ascii", action="store_true", help="Print ascii")

    def handle(self, *args, **options):
        user_id = options["user_id"]
        device_name = options["device_name"]
        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            raise CommandError(f"User {user_id} doesn't exists")
        totp_device = TOTPDevice.objects.create(user=user, name=device_name)
        self.stdout.write(
            self.style.SUCCESS(b32encode(totp_device.bin_key).decode("UTF-8"))
        )
        if options["print_full_url"]:
            self.stdout.write(self.style.SUCCESS(totp_device.config_url))
        if options["print_ascii"]:
            img = qrcode.QRCode()
            img.add_data(totp_device.config_url)
            img.print_ascii()
