from django_filters.rest_framework import FilterSet

from neatplus.filters import M2MInFilter

from .models import LegalDocument, Resource, ResourceTag


class LegalDocumentFilter(FilterSet):
    class Meta:
        model = LegalDocument
        fields = {"document_type": ["exact"]}


class ResourceFilter(FilterSet):
    tags__in = M2MInFilter(
        queryset=ResourceTag.objects.all(),
        field_name="tags",
        distinct=True,
    )

    class Meta:
        model = Resource
        fields = {
            "resource_type": ["exact"],
            "tags": ["exact"],
        }
