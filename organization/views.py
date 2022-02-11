from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.views import UserStampedModelViewSetMixin
from project.models import Project
from project.serializers import CreateProjectSerializer

from .filters import OrganizationFilter, OrganizationMemberRequestFilter
from .models import Organization, OrganizationMemberRequest
from .permissions import IsMemberRequestOrganizationAdmin, IsOrganizationAdminOrReadOnly
from .serializers import (
    CreateOrganizationSerializer,
    OrganizationMemberRequestSerializer,
    OrganizationSerializer,
)


class OrganizationViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    filterset_class = OrganizationFilter
    permission_classes = [IsOrganizationAdminOrReadOnly]

    def get_queryset(self):
        authenticated_user = self.request.user
        if authenticated_user.is_authenticated:
            filter_statement = Q(status="accepted") | Q(created_by=self.request.user)
        else:
            filter_statement = Q(status="accepted")
        return Organization.objects.filter(filter_statement)

    def get_serializer_class(self):
        if self.name and self.serializer_class:
            return self.serializer_class
        if self.action == "create":
            return CreateOrganizationSerializer
        return OrganizationSerializer

    @extend_schema(
        responses=inline_serializer(
            name="OrganizationProjectCreateResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully created project")
                )
            },
        )
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=CreateProjectSerializer,
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
        responses=inline_serializer(
            name="OrganizationMemberRequestResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Successfully requested member access")
                )
            },
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
        responses=inline_serializer(
            name="OrganizationMemberRequestAcceptResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Member request successfully accepted")
                )
            },
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
        responses=inline_serializer(
            name="OrganizationMemberRequestRejectResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default=_("Member request successfully rejected")
                )
            },
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
