from rest_framework import viewsets

from .filters import ResourceFilter
from .models import FrequentlyAskedQuestion, Resource, ResourceTag
from .serializers import (
    FrequentlyAskedQuestionSerializer,
    ResourceSerializer,
    ResourceTagSerializer,
)


class FrequentlyAskedQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FrequentlyAskedQuestion.objects.all()
    serializer_class = FrequentlyAskedQuestionSerializer


class ResourceTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResourceTag.objects.all()
    serializer_class = ResourceTagSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filterset_class = ResourceFilter
