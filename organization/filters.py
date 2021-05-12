from django_filters.rest_framework import FilterSet

from .models import Organization, Project


class OrganizationFilter(FilterSet):
    class Meta:
        model = Organization
        fields = {"title": ["exact"], "admins": ["exact"], "members": ["exact"]}


class ProjectFilter(FilterSet):
    class Meta:
        model = Project
        fields = {
            "title": ["exact"],
            "organization": ["exact"],
            "visibility": ["exact"],
            "status": ["exact"],
        }
