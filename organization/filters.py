from django_filters.rest_framework import FilterSet

from .models import Organization, OrganizationMemberRequest


class OrganizationFilter(FilterSet):
    class Meta:
        model = Organization
        fields = {"title": ["exact"]}


class OrganizationMemberRequestFilter(FilterSet):
    class Meta:
        model = OrganizationMemberRequest
        fields = {"user": ["exact"], "organization": ["exact"], "status": ["exact"]}
