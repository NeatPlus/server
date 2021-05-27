from django_filters.rest_framework import FilterSet

from .models import Resource


class ResourceFilter(FilterSet):
    class Meta:
        model = Resource
        fields = {
            "resource_type": ["exact"],
            "tags": ["exact"],
        }
