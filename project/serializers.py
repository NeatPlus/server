from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from neatplus.serializers import UserModelSerializer
from organization.serializers import OrganizationSerializer
from user.serializers import UserSerializer

from .models import Project, ProjectUser


class ProjectUserSerializer(UserModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectUser
        exclude = ("project",)


class ProjectSerializer(UserModelSerializer):
    created_by = UserSerializer()
    organization_title = serializers.SerializerMethodField(read_only=True)
    is_admin_or_owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

    def get_organization_title(self, obj):
        if obj.organization:
            return obj.organization.title

    def get_is_admin_or_owner(self, obj):
        current_user = self.context["request"].user
        is_created_by = current_user == obj.created_by
        if obj.organization:
            return is_created_by or current_user in obj.organization.admins.all()
        else:
            return is_created_by

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CreateProjectSerializer(UserModelSerializer):
    class Meta:
        model = Project
        exclude = ("users",)

    def validate(self, attrs):
        data = super().validate(attrs)
        organization_obj = data.get("organization")
        if organization_obj:
            if organization_obj.status != "accepted":
                raise serializers.ValidationError(
                    {
                        "organization": _(
                            "Cannot create project for not accepted organization"
                        )
                    }
                )
        else:
            if data["visibility"] == "public_within_organization":
                raise serializers.ValidationError(
                    {
                        "visibility": _(
                            "No organization project cannot have public_within_organization visibility"
                        )
                    }
                )
        return data


class UpsertProjectUserSerializer(UserModelSerializer):
    class Meta:
        model = ProjectUser
        exclude = ("project",)


class RemoveProjectUserSerializer(UserModelSerializer):
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
            ("visibility", "visibility"),
        ]
    )
