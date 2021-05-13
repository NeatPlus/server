from rest_framework import serializers

from .models import Organization, Project, ProjectUser


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class ProjectUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        exclude = ("project",)


class ProjectDetailSerializer(serializers.ModelSerializer):
    users = ProjectUserDetailSerializer(
        source="projectuser_set", many=True, read_only=True
    )

    class Meta:
        model = Project
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class CreateOrganizationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ("organization", "users")


class UpdateOrCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        exclude = ("project",)


class RemoveProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ("user",)
