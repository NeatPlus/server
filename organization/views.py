from typing import OrderedDict

from django.db.models import Q
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from neatplus.views import UserStampedModelUpdateMixin

from .filters import OrganizationFilter, ProjectFilter
from .models import Organization, Project, ProjectUser
from .permissions import CanEditProjectOrReadOnly, IsProjectOrganizationAdmin
from .serializers import (
    AccessLevelResponseSerializer,
    CreateOrganizationProjectSerializer,
    OrganizationSerializer,
    ProjectSerializer,
    ProjectUsersDetailSerializer,
    RemoveProjectUserSerializer,
    UpdateOrCreateUserSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=CreateOrganizationProjectSerializer,
    )
    def create_project(self, request, *args, **kwargs):
        organization = self.get_object()
        current_user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(created_by=current_user, organization=organization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    UserStampedModelUpdateMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [CanEditProjectOrReadOnly]
    filterset_class = ProjectFilter

    def get_serializer_class(self):
        if self.name and self.serializer_class:
            return self.serializer_class
        if self.action == "retrieve":
            current_user = self.request.user
            obj = self.get_object()
            if (
                obj.created_by == current_user
                or current_user in obj.organization.admins.all()
            ):
                return ProjectUsersDetailSerializer
        return ProjectSerializer

    def get_queryset(self):
        current_user = self.request.user
        organizations = Organization.objects.filter(
            Q(admins=current_user) | Q(members=current_user)
        )
        return (
            Project.objects.filter(
                Q(created_by=current_user)
                | Q(organization__admins=current_user)
                | (
                    (
                        Q(visibility="public")
                        | (
                            Q(visibility="public_within_organization")
                            & Q(organization__in=organizations)
                        )
                        | Q(users=current_user)
                    )
                    & Q(status="accepted")
                )
            )
            .distinct()
            .prefetch_related("organization__admins")
        )

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsProjectOrganizationAdmin],
        serializer_class=serializers.Serializer,
    )
    def accept(self, request, *args, **kwargs):
        project = self.get_object()
        if project.status != "accepted":
            project.status = "accepted"
            project.save()
        return Response({"detail": "Project successfully accepted"})

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsProjectOrganizationAdmin],
        serializer_class=serializers.Serializer,
    )
    def reject(self, request, *args, **kwargs):
        project = self.get_object()
        if project.status != "rejected":
            project.status = "rejected"
            project.save()
        return Response({"detail": "Project successfully rejected"})

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanEditProjectOrReadOnly],
        serializer_class=UpdateOrCreateUserSerializer,
    )
    def update_or_add_users(self, request, *args, **kwargs):
        project = self.get_object()
        data = request.data

        if isinstance(data, dict):
            serializer = self.get_serializer(data=data)
        else:
            serializer = self.get_serializer(data=data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        if isinstance(validated_data, OrderedDict):
            validated_data = [validated_data]

        for validated_datum in validated_data:
            user_obj = validated_datum.pop("user")
            ProjectUser.objects.update_or_create(
                project=project, user=user_obj, defaults=validated_datum
            )
        return Response({"detail": "Successfully modified users list for project"})

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[CanEditProjectOrReadOnly],
        serializer_class=RemoveProjectUserSerializer,
    )
    def remove_users(self, request, *args, **kwargs):
        project = self.get_object()
        data = request.data

        if isinstance(data, dict):
            serializer = self.get_serializer(data=data)
        else:
            serializer = self.get_serializer(data=data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        if isinstance(validated_data, OrderedDict):
            validated_data = [validated_data]

        for validated_datum in validated_data:
            user_obj = validated_datum.pop("user")
            project.users.remove(user_obj)
        return Response({"detail": "Successfully removed users from project"})

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=AccessLevelResponseSerializer,
    )
    def access_level(self, request, *args, **kwargs):
        project = self.get_object()
        user = self.request.user
        if user in project.organization.admins.all():
            access_level = "organization_admin"
        elif user == project.created_by:
            access_level = "owner"
        elif user in project.users.all():
            permission = ProjectUser.objects.get(user=user, project=project).permission
            if permission == "write":
                access_level = "write"
            else:
                access_level = "read_only"
        else:
            access_level = "visibility_access"
        data = {"access_level": access_level}
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.data)
