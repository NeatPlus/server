from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer

from .models import Project, ProjectUser


class ProjectUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectUser
        exclude = ("project",)


class ProjectSerializer(serializers.ModelSerializer):
    is_admin_or_owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

    def get_is_admin_or_owner(self, obj):
        current_user = self.context["request"].user
        return (
            current_user == obj.created_by
            or current_user in obj.organization.admins.all()
        )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ("users",)


class UpsertProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        exclude = ("project",)


class RemoveProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ("user",)


class AccessLevelResponseSerializer(serializers.Serializer):
    access_level = serializers.ChoiceField(
        choices=[
            ("organization_admin", "organization_admin"),
            ("owner", "owner"),
            ("write", "write"),
            ("read_only", "read_only"),
            ("visibility_level", "visibility_level"),
        ]
    )
