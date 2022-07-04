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
    created_by = UserSerializer(read_only=True)
    organization_title = serializers.SerializerMethodField(read_only=True)
    is_admin_or_owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("users",)

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

    def validate(self, attrs):
        data = super().validate(attrs)
        request_method = self.context["request"].method

        if request_method == "POST":
            organization_obj = data.get("organization")
            visibility = data.get("visibility")
        else:
            instance = self.instance
            if "organization" in data.keys():
                organization_obj = data.get("organization")
            else:
                organization_obj = instance.organization
            if "visibility" in data.keys():
                visibility = data.get("visibility")
            else:
                visibility = instance.visibility

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
            if visibility == "public_within_organization":
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
