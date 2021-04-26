from rest_framework import serializers


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
