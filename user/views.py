import os

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.serializers import get_detail_inline_serializer
from neatplus.utils import gen_random_number, gen_random_string
from support.models import EmailTemplate

from .models import EmailChangePin, EmailConfirmationPin, PasswordResetPin, User
from .serializers import (
    ChangePasswordSerializer,
    CurrentlyEnabledUserRegisterSerializer,
    EmailChangePinVerifySerializer,
    EmailChangeSerializer,
    PasswordResetPasswordChangeSerializer,
    PinVerifySerializer,
    PrivateUserSerializer,
    UploadImageSerializer,
    UserNameSerializer,
    UserSerializer,
)


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_term = self.request.query_params.get("search", "")
        if len(search_term) < 3:
            return User.objects.none()
        return User.objects.filter(
            Q(username__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
        ).filter(is_active=True)

    @action(
        methods=[],
        detail=False,
        serializer_class=PrivateUserSerializer,
    )
    def me(self, request, *args, **kwargs):
        pass

    @me.mapping.get
    def get_me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.request.user, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses=get_detail_inline_serializer(
            "ChangePasswordResponseSerializer", _("Password successfully updated")
        )
    )
    @action(
        methods=["post"],
        detail=False,
        serializer_class=ChangePasswordSerializer,
        url_path="me/change_password",
    )
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        user = self.request.user
        new_password = data["new_password"]
        try:
            validate_password(password=new_password, user=user)
        except ValidationError as e:
            errors = list(e.messages)
            return Response(
                {"non_field_errors": errors}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response({"detail": _("Password successfully updated")})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "RegisterUserResponseSerializer",
            _("User successfully registered and email send to user's email address"),
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=CurrentlyEnabledUserRegisterSerializer,
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        user_exists = User.objects.filter_by_username(data["username"]).exists()
        if user_exists:
            return Response(
                {"error": _("User with username/email already exists")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data.pop("re_password")
        user_password = data.pop("password")
        try:
            validate_password(password=user_password)
        except ValidationError as e:
            errors = list(e.messages)
            return Response({"password": errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(**data)
        user.set_password(user_password)
        user.save()
        return Response(
            {
                "detail": _(
                    "User successfully registered and email send to user's email address"
                )
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=get_detail_inline_serializer(
            "PasswordResetResponseSerializer",
            _("Password reset email successfully send"),
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=UserNameSerializer,
    )
    def password_reset(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = User.objects.filter_by_username(username, is_active=True).first()
        if not user:
            return Response(
                {
                    "error": _(
                        "No active user present for username/email your account may be blocked"
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        random_6_digit_pin = gen_random_number(6)
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
        identifier = gen_random_string(length=16)
        password_reset_pin_object, _created = PasswordResetPin.objects.update_or_create(
            user=user,
            defaults={
                "pin": random_6_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
                "identifier": identifier,
            },
        )
        subject, html_message, text_message = EmailTemplate.objects.get(
            identifier="password_reset"
        ).get_email_contents(
            context={"user": user, "password_reset_object": password_reset_pin_object}
        )
        user.email_user(subject, text_message, html_message=html_message)
        return Response({"detail": _("Password reset email successfully send")})

    @extend_schema(
        responses=inline_serializer(
            name="PasswordResetVerifyResponseSerializer",
            fields={"identifier": serializers.CharField()},
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=PinVerifySerializer,
        url_path="password_reset/verify",
    )
    def password_reset_verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = User.objects.filter_by_username(username, is_active=True).first()
        if not user:
            return Response(
                {"error": _("No active user present for username/email")},
                status=status.HTTP_404_NOT_FOUND,
            )
        pin = data["pin"]
        current_time = timezone.now()
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
                        {"error": _("User is inactive")},
                        status=status.status.HTTP_400_BAD_REQUEST,
                    )
                elif user_only_password_reset_object.no_of_incorrect_attempts >= 5:
                    user.is_active = False
                    user.save()
                    return Response(
                        {"error": _("User is now inactive for trying too many times")},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_password_reset_object.pin != pin:
                    return Response(
                        {"error": _("Password reset pin is incorrect")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": _("Password reset pin has expired")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": _("No matching active user pin found")},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            password_reset_pin_object_identifier = password_reset_pin_object.identifier
            password_reset_pin_object.no_of_incorrect_attempts = 0
            password_reset_pin_object.save()
            return Response({"identifier": password_reset_pin_object_identifier})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "PasswordResetChangeResponseSerializer", _("Password successfully changed")
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=PasswordResetPasswordChangeSerializer,
        url_path="password_reset/change",
    )
    def password_reset_change(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = User.objects.filter_by_username(username, is_active=True).first()
        if not user:
            return Response(
                {"error": _("No active user present for username/email")},
                status=status.HTTP_404_NOT_FOUND,
            )
        identifier = data["identifier"]
        password = data["password"]
        re_password = data["re_password"]
        if re_password != password:
            return Response(
                {"error": _("Password and re_password doesn't match")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_time = timezone.now()
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
                        {"error": _("User is inactive")},
                        status=status.status.HTTP_400_BAD_REQUEST,
                    )
                elif user_only_password_reset_object.no_of_incorrect_attempts >= 5:
                    user.is_active = False
                    user.save()
                    return Response(
                        {"error": _("User is now inactive for trying too many times")},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_password_reset_object.identifier != identifier:
                    return Response(
                        {"error": _("Password reset identifier is incorrect")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": _("Password reset pin has expired")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": _("No matching active user pin found")},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            try:
                validate_password(password=password, user=user)
            except ValidationError as e:
                errors = list(e.messages)
                return Response(
                    {"password": errors}, status=status.HTTP_400_BAD_REQUEST
                )
            password_reset_pin_object.no_of_incorrect_attempts = 0
            password_reset_pin_object.is_active = False
            password_reset_pin_object.save()
            user.set_password(password)
            user.save()
            return Response({"detail": _("Password successfully changed")})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "EmailConfirmResponseSerializer",
            _("Email confirmation mail successfully sent"),
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=UserNameSerializer,
    )
    def email_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = User.objects.filter_by_username(username).first()
        if not user:
            return Response(
                {"error": _("No user present with given email address/username")},
                status=status.HTTP_404_NOT_FOUND,
            )
        email_confirm_pin = EmailConfirmationPin.objects.filter(user=user).first()
        if email_confirm_pin:
            if email_confirm_pin.no_of_incorrect_attempts >= 5:
                return Response(
                    {"error": _("User is inactive for trying too many times")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not email_confirm_pin.is_active:
                return Response(
                    {"error": _("Email address has already been confirmed")},
                    status=status.HTTP_404_NOT_FOUND,
                )
        random_6_digit_pin = gen_random_number(6)
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
        (
            email_confirm_pin_object,
            _created,
        ) = EmailConfirmationPin.objects.update_or_create(
            user=user,
            defaults={
                "pin": random_6_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
            },
        )
        subject, html_message, text_message = EmailTemplate.objects.get(
            identifier="email_confirm"
        ).get_email_contents(
            {"user": user, "email_confirm_object": email_confirm_pin_object}
        )
        user.email_user(subject, text_message, html_message=html_message)
        return Response({"detail": _("Email confirmation mail successfully sent")})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "EmailConfirmVerifyResponseSerializer", _("Email successfully confirmed")
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=PinVerifySerializer,
        url_path="email_confirm/verify",
    )
    def email_confirm_verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        username = data["username"]
        user = User.objects.filter_by_username(username, is_active=False).first()
        if not user:
            return Response(
                {"error": _("No inactive user present for username")},
                status=status.HTTP_404_NOT_FOUND,
            )
        pin = data["pin"]
        current_time = timezone.now()
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
                        {"error": _("Email is already confirmed for user")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user_only_email_confirm_mail_object.no_of_incorrect_attempts += 1
                user_only_email_confirm_mail_object.save()
                if user_only_email_confirm_mail_object.no_of_incorrect_attempts >= 5:
                    return Response(
                        {"error": _("User is now inactive for trying too many times")},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_email_confirm_mail_object.pin != pin:
                    return Response(
                        {"error": _("Email confirmation pin is incorrect")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": _("Email confirmation pin has expired")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": _("No matching active username/email found")},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            email_confirmation_mail_object.no_of_incorrect_attempts = 0
            email_confirmation_mail_object.is_active = False
            email_confirmation_mail_object.save()
            user.is_active = True
            user.save()
            return Response({"detail": _("Email successfully confirmed")})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "EmailChangeResponseSerializer", _("Email change mail successfully sent")
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=EmailChangeSerializer,
    )
    def email_change(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        user = self.request.user
        email_change_pin = EmailChangePin.objects.filter(user=user).first()
        if email_change_pin:
            if email_change_pin.no_of_incorrect_attempts >= 5:
                return Response(
                    {"error": _("User is inactive for trying too many times")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        random_6_digit_pin = gen_random_number(6)
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
        email_change_pin_object, _created = EmailChangePin.objects.update_or_create(
            user=user,
            defaults={
                "pin": random_6_digit_pin,
                "pin_expiry_time": active_for_one_hour,
                "is_active": True,
                "new_email": data["new_email"],
            },
        )
        subject, html_message, text_message = EmailTemplate.objects.get(
            identifier="email_change"
        ).get_email_contents({"email_change_object": email_change_pin_object})
        send_mail(
            subject,
            text_message,
            from_email=None,
            recipient_list=[email_change_pin_object.new_email],
            html_message=html_message,
        )
        return Response({"detail": _("Email change mail successfully sent")})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "EmailChangeVerifyResponseSerializer", _("Email successfully changed")
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=EmailChangePinVerifySerializer,
        url_path="email_change/verify",
    )
    def email_change_verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        user = self.request.user
        pin = data["pin"]
        current_time = timezone.now()
        email_change_mail_object = EmailChangePin.objects.filter(
            user=user,
            pin=pin,
            is_active=True,
            pin_expiry_time__gte=current_time,
        ).first()
        if not email_change_mail_object:
            user_only_email_change_mail_object = EmailChangePin.objects.filter(
                user=user
            ).first()
            if user_only_email_change_mail_object:
                if not user_only_email_change_mail_object.is_active:
                    return Response(
                        {"error": _("Email is already changed for user")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user_only_email_change_mail_object.no_of_incorrect_attempts += 1
                user_only_email_change_mail_object.save()
                if user_only_email_change_mail_object.no_of_incorrect_attempts >= 5:
                    return Response(
                        {"error": _("User is now inactive for trying too many times")},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )
                elif user_only_email_change_mail_object.pin != pin:
                    return Response(
                        {"error": _("Email change pin is incorrect")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": _("Email change pin has expired")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": _("No matching active change change request found")},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            if User.objects.filter(email=email_change_mail_object.new_email).exists():
                return Response(
                    {"error": _("email already used for account creation")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            email_change_mail_object.no_of_incorrect_attempts = 0
            email_change_mail_object.is_active = False
            email_change_mail_object.save()
            user.email = email_change_mail_object.new_email
            user.save()
            return Response({"detail": _("Email successfully changed")})

    @extend_schema(
        responses=inline_serializer(
            name="UploadImageResponseSerializer",
            fields={"name": serializers.CharField(), "url": serializers.URLField()},
        )
    )
    @action(methods=["post"], detail=False, serializer_class=UploadImageSerializer)
    def upload_image(self, request, *args, **kwargs):
        username = self.request.user.username
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        file = request.data["file"]
        upload_file_name = default_storage.get_valid_name(file.name)
        upload_path = os.path.join(
            "user_uploaded_file", f"{username}", upload_file_name
        )
        saved_file = default_storage.save(upload_path, file)
        url = request.build_absolute_uri(default_storage.url(saved_file))
        data = {"name": saved_file, "url": url}
        return Response(data)
