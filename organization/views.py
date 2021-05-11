from django.db.models import Q
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neatplus.views import UserStampedModelUpdateMixin

from .models import Organization, Project
from .permissions import CanEditProjectOrReadOnly, IsProjectOrganizationAdmin
from .serializers import (
    CreateOrganizationProjectSerializer,
    OrganizationSerializer,
    ProjectSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

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
    serializer_class = ProjectSerializer

    def get_queryset(self):
        current_user = self.request.user
        organizations = Organization.objects.filter(
            Q(admins=current_user) | Q(members=current_user)
        )
        return Project.objects.filter(
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
                & Q(is_accepted_by_admin=True)
            )
        )

    @action(
        methods=["post"], detail=True, permission_classes=[IsProjectOrganizationAdmin]
    )
    def accept(self, request, *args, **kwargs):
        project = self.get_object()
        if not project.is_accepted_by_admin:
            project.is_accepted_by_admin = True
            project.save()
        return Response({"detail": "Project successfully accepted"})

    @action(
        methods=["post"], detail=True, permission_classes=[IsProjectOrganizationAdmin]
    )
    def reject(self, request, *args, **kwargs):
        project = self.get_object()
        if not project.is_accepted_by_admin:
            project.is_accepted_by_admin = False
            project.save()
        return Response({"detail": "Project successfully rejected"})
