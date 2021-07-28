from django_filters.rest_framework import FilterSet

from .models import LegalDocument, Resource


class LegalDocumentFilter(FilterSet):
    class Meta:
        model = LegalDocument
        fields = {"document_type": ["exact"]}


class ResourceFilter(FilterSet):
    class Meta:
        model = Resource
        fields = {
            "resource_type": ["exact"],
            "tags": ["exact"],
        }
