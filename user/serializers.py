from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class PrivateUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ("username", "email", "first_name", "last_name")


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
