from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "organization", "role")


class PrivateUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "organization",
            "role",
            "has_accepted_terms_and_privacy_policy",
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()


class UserNameSerializer(serializers.Serializer):
    username = serializers.CharField()


class PinVerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    pin = serializers.IntegerField()


class PasswordResetPasswordChangeSerializer(serializers.Serializer):
    username = serializers.CharField()
    identifier = serializers.CharField()
    password = serializers.CharField()
    re_password = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    re_password = serializers.CharField()
    organization = serializers.CharField()
    role = serializers.CharField()


class UploadImageSerializer(serializers.Serializer):
    file = serializers.ImageField()
