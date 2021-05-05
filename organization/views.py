from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Organization, Project
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
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(created_by=current_user, organization=organization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        current_user = self.request.user
        organizations = Organization.objects.filter(
            Q(admins=current_user) | Q(members=current_user)
        )
        return Project.objects.filter(
            Q(visibility="public")
            | (
                Q(visibility="public_within_organization")
                & Q(organization__in=organizations)
            )
            | Q(users=current_user)
            | Q(created_by=current_user)
        )
