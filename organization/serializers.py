from rest_framework import serializers

from neatplus.serializers import ExcludeUserStampedFieldSerializer, UserModelSerializer
from user.serializers import UserSerializer

from .models import Organization, OrganizationMemberRequest


class OrganizationSerializer(UserModelSerializer, ExcludeUserStampedFieldSerializer):
    is_admin = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        exclude = (
            "admins",
            "members",
        )

    def get_is_admin(self, obj):
        return self.context["request"].user in obj.admins.all()

    def get_is_member(self, obj):
        return self.context["request"].user in obj.members.all()


class OrganizationMemberRequestSerializer(UserModelSerializer):
    user = UserSerializer()
    is_organization_admin = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationMemberRequest
        fields = "__all__"

    def get_is_organization_admin(self, obj):
        return self.context["request"].user in obj.organization.admins.all()


class OrganizationUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    role = serializers.ChoiceField(choices=["admin", "member"])


class ListOrganizationUserSerializer(serializers.Serializer):
    user = serializers.DictField()
    role = serializers.ChoiceField(choices=["admin", "member"])
