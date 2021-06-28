from django.db.models import Q

from organization.models import Organization

from .models import Project


def read_allowed_project_for_user(user):
    organizations = Organization.objects.filter(status="accepted").filter(
        Q(admins=user) | Q(members=user)
    )
    return Project.objects.filter(
        Q(created_by=user)
        | Q(organization__admins=user)
        | (
            (
                Q(visibility="public")
                | (
                    Q(visibility="public_within_organization")
                    & Q(organization__in=organizations)
                )
            )
            & Q(status="accepted")
        )
        | Q(users=user)
    ).distinct()
