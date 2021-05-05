from rest_framework import serializers

from .models import Organization, Project


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class CreateOrganizationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ("organization",)
