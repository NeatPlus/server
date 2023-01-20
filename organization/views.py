from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.serializers import get_detail_inline_serializer
from neatplus.views import UserStampedModelViewSetMixin
from project.models import Project
from project.serializers import ProjectSerializer
from user.models import User
from user.serializers import UserSerializer

from .filters import OrganizationFilter, OrganizationMemberRequestFilter
from .models import Organization, OrganizationMemberRequest
from .permissions import (
    IsMemberRequestOrganizationAdmin,
    IsOrganizationAdmin,
    IsOrganizationAdminOrReadOnly,
)
from .serializers import (
    ListOrganizationUserSerializer,
    OrganizationMemberRequestSerializer,
    OrganizationSerializer,
    OrganizationUserSerializer,
)


class OrganizationViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    filterset_class = OrganizationFilter
    permission_classes = [IsOrganizationAdminOrReadOnly]
    serializer_class = OrganizationSerializer
    search_fields = [
        "title",
    ]

    def get_queryset(self):
        authenticated_user = self.request.user
        if authenticated_user.is_authenticated:
            filter_statement = Q(status="accepted") | Q(created_by=self.request.user)
        else:
            filter_statement = Q(status="accepted")
        return Organization.objects.filter(filter_statement).prefetch_related(
            "admins",
            "members",
        )

    @extend_schema(
        responses=get_detail_inline_serializer(
            "OrganizationProjectCreateResponseSerializer",
            _("Successfully created project"),
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=ProjectSerializer,
    )
    def create_project(self, request, *args, **kwargs):
        organization = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        Project.objects.create(
            **validated_data, organization=organization, created_by=self.request.user
        )
        return Response(
            {"detail": _("Successfully created project")},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=get_detail_inline_serializer(
            "OrganizationMemberRequestResponseSerializer",
            _("Successfully requested member access"),
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=serializers.Serializer,
    )
    def member_request(self, request, *args, **kwargs):
        organization = self.get_object()
        user = self.request.user
        OrganizationMemberRequest.objects.create(
            user=user, organization=organization, created_by=user
        )
        return Response(
            {"detail": _("Successfully requested member access")},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsOrganizationAdmin],
        serializer_class=ListOrganizationUserSerializer,
    )
    def users(self, request, *args, **kwargs):
        organization = self.get_object()
        users = []
        user_serializer_class = UserSerializer
        for admin in organization.admins.all():
            admin_data = user_serializer_class(admin).data
            users.append({"user": admin_data, "role": "admin"})
        for member in organization.members.all():
            member_data = user_serializer_class(member).data
            users.append({"user": member_data, "role": "member"})
        serializer = self.get_serializer(data=users, many=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.data)

    @extend_schema(
        request=OrganizationUserSerializer(many=True),
        responses=get_detail_inline_serializer(
            "OrganizationAddUserSerializer", _("Successfully added all valid users")
        ),
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsOrganizationAdmin],
        serializer_class=OrganizationUserSerializer,
    )
    def update_or_add_users(self, request, *args, **kwargs):
        organization = self.get_object()
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for validated_datum in serializer.validated_data:
                    user = User.objects.filter(username=validated_datum["user"]).first()
                    if user:
                        if validated_datum["role"] == "admin":
                            organization.admins.add(user)
                            organization.members.remove(user)
                        elif validated_datum["role"] == "member":
                            organization.members.add(user)
                            organization.admins.remove(user)
        except Exception:
            return Response(
                {"error": _("Failed to add users to organization")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": _("Successfully added all valid users")})

    @extend_schema(
        request=OrganizationUserSerializer(many=True),
        responses=get_detail_inline_serializer(
            "OrganizationAddUserSerializer", _("Successfully removed all valid users")
        ),
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsOrganizationAdmin],
        serializer_class=OrganizationUserSerializer,
    )
    def remove_users(self, request, *args, **kwargs):
        organization = self.get_object()
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for validated_datum in serializer.validated_data:
                    user = User.objects.filter(username=validated_datum["user"]).first()
                    if user:
                        if validated_datum["role"] == "admin":
                            organization.admins.remove(user)
                        elif validated_datum["role"] == "member":
                            organization.members.remove(user)
        except Exception:
            return Response(
                {"error": _("Failed to remove users from organization")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": _("Successfully removed all valid users")})


class OrganizationMemberRequestViewSet(
    mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet
):
    serializer_class = OrganizationMemberRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = OrganizationMemberRequestFilter

    def get_queryset(self):
        user = self.request.user
        return (
            OrganizationMemberRequest.objects.filter(
                Q(organization__admins=user) | Q(user=user)
            )
            .prefetch_related("organization__admins")
            .distinct()
        )

    @extend_schema(
        responses=get_detail_inline_serializer(
            "OrganizationMemberRequestAcceptResponseSerializer",
            _("Member request successfully accepted"),
        )
    )
    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.Serializer,
        permission_classes=[IsMemberRequestOrganizationAdmin],
    )
    def accept(self, request, *args, **kwargs):
        member_request = self.get_object()
        if member_request.status != "accepted":
            member_request.updated_by = request.user
            member_request.status = "accepted"
            member_request.save()
        return Response({"detail": _("Member request successfully accepted")})

    @extend_schema(
        responses=get_detail_inline_serializer(
            "OrganizationMemberRequestRejectResponseSerializer",
            _("Member request successfully rejected"),
        )
    )
    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.Serializer,
        permission_classes=[IsMemberRequestOrganizationAdmin],
    )
    def reject(self, request, *args, **kwargs):
        member_request = self.get_object()
        if member_request.status != "rejected":
            member_request.updated_by = request.user
            member_request.status = "rejected"
            member_request.save()
        return Response({"detail": _("Member request successfully rejected")})
