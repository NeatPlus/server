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
    is_organization_admin = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationMemberRequest
        fields = "__all__"

    def get_is_organization_admin(self, obj):
        return self.context["request"].user in obj.organization.admins.all()
