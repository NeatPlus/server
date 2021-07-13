from django.db.models import Q, TextChoices
from django_filters.filters import ChoiceFilter
from django_filters.rest_framework import FilterSet

from .models import Project


class TabChoice(TextChoices):
    MY_PROJECT = "my_project"
    ORGANIZATION = "organization"
    PUBLIC = "public"


class ProjectFilter(FilterSet):

    tab = ChoiceFilter(label="tab", method="get_tab", choices=TabChoice.choices)

    class Meta:
        model = Project
        fields = {
            "title": ["exact"],
            "organization": ["exact"],
            "visibility": ["exact"],
            "status": ["exact"],
        }

    def get_tab(self, queryset, name, value):
        user = self.request.user
        my_projects = queryset.filter(Q(created_by=user) | Q(users=user))
        if value == TabChoice.MY_PROJECT:
            return my_projects
        my_projects_id = my_projects.values("id")
        organization_projects = queryset.filter(
            Q(organization__admins=user) | Q(visibility="public_within_organization")
        ).exclude(id__in=my_projects_id)
        if value == TabChoice.ORGANIZATION:
            return organization_projects
        organization_projects_id = organization_projects.values("id")
        if value == TabChoice.PUBLIC:
            return queryset.exclude(
                Q(id__in=organization_projects_id) | Q(id__in=my_projects_id)
            )
