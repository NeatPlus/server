import datetime

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.template.loader import get_template
from rest_framework import permissions, status, views
from rest_framework.response import Response

from neatplus.utils import random_N_digit_number, random_N_length_string

from .models import EmailConfirmationPin, PasswordResetPin
from .serializers import (
    PasswordResetPasswordChangeSerializer,
    PinVerifySerializer,
    UserNameSerializer,
    UserRegisterSerializer,
)


class UserRegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Payload data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        re_password = data["re_password"]
        if re_password != password:
            return Response(
                {"error": "Password and re_password doesn't match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_exists = get_user_model().objects.filter_by_username(username).exists()
        if user_exists:
            return Response(
                {"error": "User with username/email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        _ = get_user_model().objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        return Response(
            {
                "detail": "User successfully registered and email send to user's email address"
            }
        )


class PasswordResetPinSendView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = UserNameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Payload data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = (
            get_user_model()
            .objects.filter_by_username(username, is_active=True)
            .first()
        )
        if not user:
            return Response(
                {
                    "error": "No active user present for username/email your account may be blocked"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        random_6_digit_pin = random_N_digit_number(6)
        active_for_one_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
        identifier = random_N_length_string(16)
        password_reset_pin_object, _ = PasswordResetPin.objects.update_or_create(
            user=user,
            defaults={
                "pin": random_6_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
                "identifier": identifier,
            },
        )
        template = get_template("password_reset.txt")
        message = template.render(
            {"user": user, "password_reset_object": password_reset_pin_object}
        )
        user.email_user("Password reset pin", message)
        return Response({"detail": "Password reset email successfully send"})


class PasswordResetPinVerifyView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = PinVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Payload data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = (
            get_user_model()
            .objects.filter_by_username(username, is_active=True)
            .first()
        )
        if not user:
            return Response(
                {"error": "No active user present for username/email"},
                status=status.HTTP_404_NOT_FOUND,
            )
        pin = data["pin"]
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        password_reset_pin_object = PasswordResetPin.objects.filter(
            user=user,
            user__is_active=True,
            pin=pin,
            is_active=True,
            pin_expiry_time__gte=current_time,
        ).first()
        if not password_reset_pin_object:
            user_only_password_reset_object = PasswordResetPin.objects.filter(
                user=user
            ).first()
            if user_only_password_reset_object:
                user_only_password_reset_object.no_of_incorrect_attempts += 1
                user_only_password_reset_object.save()
                if not user.is_active:
                    return Response(
                        {"error": "User is inactive"},
                        status=status.status.HTTP_400_BAD_REQUEST,
                    )
                elif user_only_password_reset_object.no_of_incorrect_attempts >= 5:
                    user.is_active = False
                    user.save()
                    return Response(
                        {"error": "User is now inactive for trying too many times"},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_password_reset_object.pin != pin:
                    return Response(
                        {"error": "Password reset pin is incorrect"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": "Password reset pin has expired"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": "No matching active user pin found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            password_reset_pin_object_identifier = password_reset_pin_object.identifier
            password_reset_pin_object.no_of_incorrect_attempts = 0
            password_reset_pin_object.save()
            return Response({"identifier": password_reset_pin_object_identifier})


class PasswordResetPasswordChangeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = PasswordResetPasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Payload data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = (
            get_user_model()
            .objects.filter_by_username(username, is_active=True)
            .first()
        )
        if not user:
            return Response(
                {"error": "No active user present for username/email"},
                status=status.HTTP_404_NOT_FOUND,
            )
        identifier = data["identifier"]
        password = data["password"]
        re_password = data["re_password"]
        if re_password != password:
            return Response(
                {"error": "Password and re_password doesn't match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        password_reset_pin_object = PasswordResetPin.objects.filter(
            user=user,
            user__is_active=True,
            identifier=identifier,
            is_active=True,
            pin_expiry_time__gte=current_time,
        ).first()
        if not password_reset_pin_object:
            user_only_password_reset_object = PasswordResetPin.objects.filter(
                user=user
            ).first()
            if user_only_password_reset_object:
                user_only_password_reset_object.no_of_incorrect_attempts += 1
                user_only_password_reset_object.save()
                if not user.is_active:
                    return Response(
                        {"error": "User is inactive"},
                        status=status.status.HTTP_400_BAD_REQUEST,
                    )
                elif user_only_password_reset_object.no_of_incorrect_attempts >= 5:
                    user.is_active = False
                    user.save()
                    return Response(
                        {"error": "User is now inactive for trying too many times"},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_password_reset_object.identifier != identifier:
                    return Response(
                        {"error": "Password reset identifier is incorrect"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": "Password reset pin has expired"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": "No matching active user pin found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            password_reset_pin_object.no_of_incorrect_attempts = 0
            password_reset_pin_object.is_active = False
            password_reset_pin_object.save()
            try:
                validate_password(password=password, user=user)
            except ValidationError as e:
                errors = list(e.messages)
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({"detail": "Password successfully changed"})


class EmailConfirmPinSendView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = UserNameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Payload data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = get_user_model().objects.filter_by_username(username).first()
        if not user:
            return Response(
                {"error": "No user present with given email address/username"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.email_confirm_pin:
            if user.email_confirm_pin.no_of_incorrect_attempts >= 5:
                return Response(
                    {"error": "User is inactive for trying too many times"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        email_confirm_pin = EmailConfirmationPin.objects.filter(user=user)
        random_6_digit_pin = random_N_digit_number(6)
        active_for_one_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
        if not email_confirm_pin.first().is_active:
            return Response(
                {"error": "Email address has already been confirmed"},
                status=status.HTTP_404_NOT_FOUND,
            )
        email_confirm_pin_object, _ = EmailConfirmationPin.objects.update_or_create(
            user=user,
            defaults={
                "pin": random_6_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
            },
        )
        template = get_template("email_confirm.txt")
        context = {"user": user, "email_confirm_object": email_confirm_pin_object}
        message = template.render(context)
        user.email_user("Email confirmation mail", message)
        return Response({"detail": "Email confirmation mail successfully send"})


class EmailConfirmPinVerifyView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = PinVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Payload data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = (
            get_user_model()
            .objects.filter_by_username(username, is_active=False)
            .first()
        )
        if not user:
            return Response(
                {"error": "No inactive user present for username"},
                status=status.HTTP_404_NOT_FOUND,
            )
        pin = data["pin"]
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        email_confirmation_mail_object = EmailConfirmationPin.objects.filter(
            user=user,
            pin=pin,
            is_active=True,
            pin_expiry_time__gte=current_time,
        ).first()
        if not email_confirmation_mail_object:
            user_only_email_confirm_mail_object = EmailConfirmationPin.objects.filter(
                user=user
            ).first()
            if user_only_email_confirm_mail_object:
                if not user_only_email_confirm_mail_object.is_active:
                    return Response(
                        {"error": "Email is already confirmed for user"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user_only_email_confirm_mail_object.no_of_incorrect_attempts += 1
                user_only_email_confirm_mail_object.save()
                if user_only_email_confirm_mail_object.no_of_incorrect_attempts >= 5:
                    return Response(
                        {"error": "User is now inactive for trying too many times"},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_email_confirm_mail_object.pin != pin:
                    return Response(
                        {"error": "Email confirmation pin is incorrect"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": "Email confirmation pin has expired"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": "No matching active username/email found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            email_confirmation_mail_object.no_of_incorrect_attempts = 0
            email_confirmation_mail_object.is_active = False
            email_confirmation_mail_object.save()
            user.is_active = True
            user.save()
            return Response({"detail": "Email successfully confirmed"})
