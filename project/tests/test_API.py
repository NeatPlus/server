from django.conf import settings
from model_bakery import random_gen

from neatplus.tests import FullTestCase
from project.models import ProjectUser


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        (
            cls.admin_user,
            cls.user,
            cls.project_created_user,
            cls.organization_user,
        ) = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True, _quantity=4)
        cls.organization = cls.baker.make(
            "organization.Organization",
            admins=[cls.admin_user],
            members=[cls.organization_user],
            status="accepted",
        )
        cls.project = cls.baker.make(
            "project.Project",
            organization=cls.organization,
            created_by=cls.project_created_user,
            users=[cls.user],
            status="accepted",
        )
        cls.pending_project = cls.baker.make(
            "project.Project",
            organization=cls.organization,
            created_by=cls.project_created_user,
            users=[cls.user],
            status="pending",
        )
        cls.project_list_url = cls.reverse("project-list", kwargs={"version": "v1"})
        cls.project_detail_url = cls.reverse(
            "project-detail", kwargs={"version": "v1", "pk": cls.project.pk}
        )
        cls.pending_project_detail_url = cls.reverse(
            "project-detail", kwargs={"version": "v1", "pk": cls.pending_project.pk}
        )

    def test_non_authenticated_project_access(self):
        response = self.client.get(self.project_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_403_FORBIDDEN, response.json()
        )

    def test_project_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.project_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_project_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.project_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_pending_project_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.pending_project_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
        self.client.force_authenticate(self.organization_user)
        response = self.client.get(self.pending_project_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_404_NOT_FOUND, response.json()
        )

    def test_pending_requests(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse("project-pending-requests", kwargs={"version": "v1"})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_organization_admin_project_users(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "project-users", kwargs={"version": "v1", "pk": self.project.pk}
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_project_creator_project_users(self):
        self.client.force_authenticate(self.project_created_user)
        url = self.reverse(
            "project-users", kwargs={"version": "v1", "pk": self.project.pk}
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_normal_user_project_users(self):
        self.client.force_authenticate(self.user)
        url = self.reverse(
            "project-users", kwargs={"version": "v1", "pk": self.project.pk}
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_403_FORBIDDEN, response.json()
        )

    def test_organization_admin_edit_project(self):
        self.client.force_authenticate(self.admin_user)
        data = {"title": "update_project"}
        response = self.client.patch(self.project_detail_url, data=data)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_project_creator_edit_project(self):
        self.client.force_authenticate(self.project_created_user)
        data = {"title": "update_project_by_created_by"}
        response = self.client.patch(self.project_detail_url, data=data)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_normal_user_edit_project(self):
        self.client.force_authenticate(self.user)
        data = {"title": "update_project_by_normal_user"}
        response = self.client.patch(self.project_detail_url, data=data)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_403_FORBIDDEN, response.json()
        )

    def test_project_creator_project_accept(self):
        self.client.force_authenticate(self.project_created_user)
        url = self.reverse(
            "project-accept",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_403_FORBIDDEN, response.json()
        )

    def test_organization_admin_project_accept(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "project-accept",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_project_creator_project_reject(self):
        self.client.force_authenticate(self.project_created_user)
        url = self.reverse(
            "project-reject",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_403_FORBIDDEN, response.json()
        )

    def test_organization_admin_project_reject(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "project-reject",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_project_user_modification(self):
        self.client.force_authenticate(self.project_created_user)
        first_user, second_user = self.baker.make(settings.AUTH_USER_MODEL, _quantity=2)
        url = self.reverse(
            "project-update-or-add-users",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        data = [
            {"user": first_user.username, "permission": "write"},
            {"user": second_user.username},
        ]
        post_response = self.client.post(url, data=data, format="json")
        self.assertEqual(
            post_response.status_code,
            self.status_code.HTTP_200_OK,
            post_response.json(),
        )
        self.assertEqual(
            ProjectUser.objects.get(project=self.project, user=first_user).permission,
            "write",
        )
        self.assertEqual(
            ProjectUser.objects.get(project=self.project, user=second_user).permission,
            "read_only",
        )

    def test_project_user_deletion(self):
        self.client.force_authenticate(self.project_created_user)
        first_user, second_user, third_user = self.baker.make(
            settings.AUTH_USER_MODEL, _quantity=3
        )
        url = self.reverse(
            "project-remove-users",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        data = [
            {"user": first_user.username},
            {"user": second_user.username},
        ]
        post_response = self.client.post(url, data=data, format="json")
        self.assertEqual(
            post_response.status_code,
            self.status_code.HTTP_200_OK,
            post_response.json(),
        )

    def test_project_access_level(self):
        url = self.reverse(
            "project-access-level",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        # admin user
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
        self.assertEqual(response.json()["accessLevel"], "organization_admin")
        # project user
        self.client.force_authenticate(self.project_created_user)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
        self.assertEqual(response.json()["accessLevel"], "owner")
        # normal user
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
        self.assertEqual(response.json()["accessLevel"], "read_only")

    def test_project_survey_creation(self):
        url = self.reverse(
            "project-create-survey", kwargs={"version": "v1", "pk": self.project.pk}
        )
        module = self.baker.make("context.Module")
        data = {"title": random_gen.gen_string(255), "modules": [module.pk]}
        self.client.force_authenticate(self.project_created_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(
            response.status_code, self.status_code.HTTP_201_CREATED, response.json()
        )

    def test_project_creation(self):
        self.client.force_authenticate(self.user)
        context = self.baker.make("context.Context")
        data = {
            "title": "sample_project",
            "description": "Description goes here",
            "visibility": "private",
            "context": context.pk,
        }
        post_response = self.client.post(self.project_list_url, data=data)
        self.assertEqual(
            post_response.status_code,
            self.status_code.HTTP_201_CREATED,
            post_response.json(),
        )

    def test_project_creation_fail_for_visibility(self):
        self.client.force_authenticate(self.user)
        context = self.baker.make("context.Context")
        data = {
            "title": "sample_project",
            "description": "Description goes here",
            "visibility": "public_within_organization",
            "context": context.pk,
        }
        post_response = self.client.post(self.project_list_url, data=data)
        self.assertEqual(
            post_response.status_code,
            self.status_code.HTTP_400_BAD_REQUEST,
            post_response.json(),
        )
