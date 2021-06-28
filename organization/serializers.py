from rest_framework import serializers

from .models import Organization, OrganizationMemberRequest


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class CreateOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ("admins", "members")


class OrganizationMemberRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMemberRequest
        fields = "__all__"
