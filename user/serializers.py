from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_recaptcha.fields import ReCaptchaV3Field
from rest_framework import serializers

from neatplus.serializers import UserModelSerializer

from .models import User


class UserSerializer(UserModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class PrivateUserSerializer(UserSerializer):
    email = serializers.EmailField(read_only=True)
    password = serializers.CharField(write_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "organization",
            "role",
            "has_accepted_terms_and_privacy_policy",
            "password",
            "permissions",
        )

    def validate(self, attrs):
        password = attrs.pop("password", None)
        if not password:
            raise serializers.ValidationError({"password": _("Password field missing")})
        user = self.context["request"].user
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"password": _("Invalid password for user")}
            )
        return super().validate(attrs)

    def get_permissions(self, obj):
        return obj.get_all_permissions()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("old_password")
        user = self.context["request"].user
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"old_password": _("Invalid password for user")}
            )
        if attrs["new_password"] != attrs["re_new_password"]:
            raise serializers.ValidationError(
                {"error": _("New password and re new password doesn't match")}
            )
        return super().validate(attrs)


class UserNameSerializer(serializers.Serializer):
    username = serializers.CharField()


class EmailChangeSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password")
        new_email = attrs.get("new_email")
        user = self.context["request"].user
        if User.objects.filter(email=new_email).exists():
            raise serializers.ValidationError({"new_email": _("Email is already used")})
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"password": _("Invalid password for user")}
            )
        return super().validate(attrs)


class EmailChangePinVerifySerializer(serializers.Serializer):
    pin = serializers.IntegerField()


class PinVerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    pin = serializers.IntegerField()


class PasswordResetPasswordChangeSerializer(serializers.Serializer):
    username = serializers.CharField()
    identifier = serializers.CharField()
    password = serializers.CharField()
    re_password = serializers.CharField()


class UserRegisterSerializer(UserSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    re_password = serializers.CharField()
    organization = serializers.CharField()
    role = serializers.CharField()

    class Meta(UserSerializer.Meta):
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "re_password",
            "organization",
            "role",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError(
                {"error": _("Password and re_password doesn't match")}
            )
        return super().validate(attrs)


class RecaptchaEnabledUserRegisterSerializer(UserRegisterSerializer):
    recaptcha = ReCaptchaV3Field(action="register")

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + ("recaptcha",)

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return super().validate(attrs)


CurrentlyEnabledUserRegisterSerializer = (
    RecaptchaEnabledUserRegisterSerializer
    if settings.ENABLE_RECAPTCHA
    else UserRegisterSerializer
)


class UploadImageSerializer(serializers.Serializer):
    file = serializers.ImageField()


class SessionLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
