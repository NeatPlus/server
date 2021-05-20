from django_filters.rest_framework import FilterSet

from .models import Organization


class OrganizationFilter(FilterSet):
    class Meta:
        model = Organization
        fields = {"title": ["exact"], "admins": ["exact"], "members": ["exact"]}
