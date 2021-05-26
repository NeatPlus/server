from rest_framework import viewsets

from neatplus.views import UserStampedModelViewSetMixin

from .filters import OrganizationFilter
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter
