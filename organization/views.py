from django.db.models import Q
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.views import UserStampedModelViewSetMixin
from project.models import Project
from project.serializers import CreateProjectSerializer

from .filters import OrganizationFilter
from .models import Organization, OrganizationMemberRequest
from .permissions import (
    IsMemberRequestOrganizationAdmin,
    IsOrganizationAdminOrReadOrCreateOnly,
)
from .serializers import (
    CreateOrganizationSerializer,
    OrganizationMemberRequestSerializer,
    OrganizationSerializer,
)


class OrganizationViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    filterset_class = OrganizationFilter
    permission_classes = [IsOrganizationAdminOrReadOrCreateOnly]

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
                "detail": serializers.CharField(default="Successfully created project")
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
            {"detail": "Successfully created project"}, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        responses=inline_serializer(
            name="OrganizationMemberRequestResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="Successfully requested member access"
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
            user=user, organization=organization, created_by=self.request.user
        )
        return Response(
            {"detail": "Successfully requested member access"},
            status=status.HTTP_200_OK,
        )


class OrganizationMemberRequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrganizationMemberRequestSerializer
    permission_classes = [IsMemberRequestOrganizationAdmin]

    def get_queryset(self):
        return OrganizationMemberRequest.objects.filter(
            organization__admins=self.request.user
        )

    @extend_schema(
        responses=inline_serializer(
            name="OrganizationMemeberRequestAcceptResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="Member request successfully accepted"
                )
            },
        )
    )
    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.Serializer,
    )
    def accept(self, request, *args, **kwargs):
        member_request = self.get_object()
        if member_request.status != "accepted":
            member_request.updated_by = request.user
            member_request.status = "accepted"
            member_request.save()
        return Response({"detail": "Member request successfully accepted"})

    @extend_schema(
        responses=inline_serializer(
            name="OrganizationMemeberRequestRejectResponseSerializer",
            fields={
                "detail": serializers.CharField(
                    default="Member request successfully rejected"
                )
            },
        )
    )
    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.Serializer,
    )
    def reject(self, request, *args, **kwargs):
        member_request = self.get_object()
        if member_request.status != "rejected":
            member_request.updated_by = request.user
            member_request.status = "rejected"
            member_request.save()
        return Response({"detail": "Member request successfully rejected"})
