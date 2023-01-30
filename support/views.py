from rest_framework import viewsets

from .filters import LegalDocumentFilter, ResourceFilter
from .models import (
    Action,
    FrequentlyAskedQuestion,
    LegalDocument,
    Resource,
    ResourceTag,
)
from .serializers import (
    ActionSerializer,
    FrequentlyAskedQuestionSerializer,
    LegalDocumentSerializer,
    ResourceSerializer,
    ResourceTagSerializer,
)


class LegalDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegalDocument.objects.all()
    serializer_class = LegalDocumentSerializer
    filterset_class = LegalDocumentFilter


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
    search_fields = ["title", "description"]


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
