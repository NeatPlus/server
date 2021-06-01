import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db.models import Q
from django.template.loader import get_template
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.utils import random_N_digit_number, random_N_length_string

from .models import EmailConfirmationPin, PasswordResetPin
from .serializers import (
    ChangePasswordSerializer,
    PasswordResetPasswordChangeSerializer,
    PinVerifySerializer,
    PrivateUserSerializer,
    UploadImageSerializer,
    UserNameSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

UserModel = get_user_model()


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserModel.objects.filter(is_active=True)

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
        responses=inline_serializer(
            name="ChangePasswordResponseSerializer",
            fields={
                "detail": serializers.CharField(default="Password successfully updated")
            },
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
        old_password = data["old_password"]
        new_password = data["new_password"]
        re_new_password = data["re_new_password"]
        if re_new_password != new_password:
            return Response(
                {"error": "New password and re new password doesn't match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(old_password):
            return Response(
                {"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        return Response({"detail": "Password successfully updated"})

    @extend_schema(
        responses=inline_serializer(
            name="RegisterUserResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="User successfully registered and email send to user's email address"
                )
            },
        )
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=UserRegisterSerializer,
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        if data["re_password"] != data["password"]:
            return Response(
                {"error": "Password and re_password doesn't match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_exists = UserModel.objects.filter_by_username(data["username"]).exists()
        if user_exists:
            return Response(
                {"error": "User with username/email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PrivateUserSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_password = data.pop("re_password")
        try:
            validate_password(password=user_password)
        except ValidationError as e:
            errors = list(e.messages)
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        UserModel.objects.create_user(**data)
        return Response(
            {
                "detail": "User successfully registered and email send to user's email address"
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=inline_serializer(
            name="PasswordResetResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="Password reset email successfully send"
                )
            },
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
        user = UserModel.objects.filter_by_username(username, is_active=True).first()
        if not user:
            return Response(
                {
                    "error": "No active user present for username/email your account may be blocked"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        random_6_digit_pin = random_N_digit_number(6)
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
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
        user = UserModel.objects.filter_by_username(username, is_active=True).first()
        if not user:
            return Response(
                {"error": "No active user present for username/email"},
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

    @extend_schema(
        responses=inline_serializer(
            name="PasswordResetChangeResponseSerializer",
            fields={
                "detail": serializers.CharField(default="Password successfully changed")
            },
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
        user = UserModel.objects.filter_by_username(username, is_active=True).first()
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

    @extend_schema(
        responses=inline_serializer(
            name="EmailConfirmResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="Email confirmation mail successfully send"
                )
            },
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
        user = UserModel.objects.filter_by_username(username).first()
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
        active_for_one_hour = timezone.now() + timezone.timedelta(hours=1)
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

    @extend_schema(
        responses=inline_serializer(
            name="EmailConfirmVerifyResponseSerializer",
            fields={
                "detail": serializers.CharField(default="Email successfully confirmed")
            },
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
        user = UserModel.objects.filter_by_username(username, is_active=False).first()
        if not user:
            return Response(
                {"error": "No inactive user present for username"},
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
        upload_path = os.path.join("user_uploaded_file", f"{username}", file.name)
        saved_file = default_storage.save(upload_path, file)
        url = request.build_absolute_uri(default_storage.url(saved_file))
        data = {"name": saved_file, "url": url}
        return Response(data)
