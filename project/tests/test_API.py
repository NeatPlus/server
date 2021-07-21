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
        self.assertEqual(response.status_code, self.status_code.HTTP_403_FORBIDDEN)

    def test_project_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.project_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_project_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.project_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_pending_project_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.pending_project_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        self.client.force_authenticate(self.organization_user)
        response = self.client.get(self.pending_project_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_404_NOT_FOUND)

    def test_organization_admin_project_users(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "project-users", kwargs={"version": "v1", "pk": self.project.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_project_creator_project_users(self):
        self.client.force_authenticate(self.project_created_user)
        url = self.reverse(
            "project-users", kwargs={"version": "v1", "pk": self.project.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_normal_user_project_users(self):
        self.client.force_authenticate(self.user)
        url = self.reverse(
            "project-users", kwargs={"version": "v1", "pk": self.project.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_403_FORBIDDEN)

    def test_organization_admin_edit_project(self):
        self.client.force_authenticate(self.admin_user)
        data = {"title": "update_project"}
        response = self.client.patch(self.project_detail_url, data=data)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_project_creator_edit_project(self):
        self.client.force_authenticate(self.project_created_user)
        data = {"title": "update_project_by_created_by"}
        response = self.client.patch(self.project_detail_url, data=data)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_normal_user_edit_project(self):
        self.client.force_authenticate(self.user)
        data = {"title": "update_project_by_normal_user"}
        response = self.client.patch(self.project_detail_url, data=data)
        self.assertEqual(response.status_code, self.status_code.HTTP_403_FORBIDDEN)

    def test_project_creator_project_accept(self):
        self.client.force_authenticate(self.project_created_user)
        url = self.reverse(
            "project-accept",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_403_FORBIDDEN)

    def test_organization_admin_project_accept(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "project-accept",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_project_creator_project_reject(self):
        self.client.force_authenticate(self.project_created_user)
        url = self.reverse(
            "project-reject",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_403_FORBIDDEN)

    def test_organization_admin_project_reject(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "project-reject",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_project_user_modification(self):
        self.client.force_authenticate(self.project_created_user)
        first_user, second_user = self.baker.make(settings.AUTH_USER_MODEL, _quantity=2)
        url = self.reverse(
            "project-update-or-add-users",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        multiple_data = [
            {"user": first_user.pk, "permission": "write"},
            {"user": second_user.pk},
        ]
        multiple_post_response = self.client.post(
            url, data=multiple_data, format="json"
        )
        self.assertEqual(
            multiple_post_response.status_code, self.status_code.HTTP_200_OK
        )
        self.assertEqual(
            ProjectUser.objects.get(project=self.project, user=first_user).permission,
            "write",
        )
        self.assertEqual(
            ProjectUser.objects.get(project=self.project, user=second_user).permission,
            "read_only",
        )

        single_data = {"user": second_user.pk, "permission": "write"}
        single_post_response = self.client.post(url, data=single_data)
        self.assertEqual(single_post_response.status_code, self.status_code.HTTP_200_OK)
        self.assertEqual(
            ProjectUser.objects.get(project=self.project, user=first_user).permission,
            "write",
        )
        self.assertEqual(
            ProjectUser.objects.get(project=self.project, user=second_user).permission,
            "write",
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
        multiple_data = [
            {"user": first_user.pk},
            {"user": second_user.pk},
        ]
        multiple_post_response = self.client.post(
            url, data=multiple_data, format="json"
        )
        self.assertEqual(
            multiple_post_response.status_code, self.status_code.HTTP_200_OK
        )

        single_data = {"user": third_user.pk}
        single_post_response = self.client.post(url, data=single_data)
        self.assertEqual(single_post_response.status_code, self.status_code.HTTP_200_OK)

    def test_project_access_level(self):
        url = self.reverse(
            "project-access-level",
            kwargs={"version": "v1", "pk": self.project.pk},
        )
        # admin user
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        self.assertEqual(response.json()["accessLevel"], "organization_admin")
        # project user
        self.client.force_authenticate(self.project_created_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        self.assertEqual(response.json()["accessLevel"], "owner")
        # normal user
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        self.assertEqual(response.json()["accessLevel"], "read_only")

    def test_project_survey_creation(self):
        url = self.reverse(
            "project-create-survey", kwargs={"version": "v1", "pk": self.project.pk}
        )
        question_1 = self.baker.make("survey.Question", answer_type="location")
        question_2 = self.baker.make("survey.Question", answer_type="number")
        question_3 = self.baker.make("survey.Question", answer_type="boolean")
        question_4 = self.baker.make("survey.Question", answer_type="single_option")
        question_4_option = self.baker.make("survey.Option", question=question_4)
        question_5 = self.baker.make("survey.Question", answer_type="multiple_option")
        question_5_option_1 = self.baker.make("survey.Option", question=question_5)
        question_5_option_2 = self.baker.make("survey.Option", question=question_5)
        statement = self.baker.make("statement.Statement")
        data = {
            "title": random_gen.gen_string(255),
            "answers": [
                {
                    "question": question_1.pk,
                    "answer": '{"type": "Point", "coordinates": [5.000000, 23.000000]}',
                    "answerType": "location",
                },
                {
                    "question": question_2.pk,
                    "answer": 2,
                    "answerType": "number",
                },
                {
                    "question": question_3.pk,
                    "answer": "true",
                    "answerType": "boolean",
                },
                {
                    "question": question_4.pk,
                    "answerType": "single_option",
                    "options": [question_4_option.pk],
                },
                {
                    "question": question_5.pk,
                    "answerType": "multiple_option",
                    "options": [question_5_option_1.pk, question_5_option_2.pk],
                },
            ],
            "results": [
                {
                    "statement": statement.pk,
                    "score": 0.90,
                },
            ],
        }
        self.client.force_authenticate(self.project_created_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, self.status_code.HTTP_201_CREATED)

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
        self.assertEqual(post_response.status_code, self.status_code.HTTP_201_CREATED)

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
            post_response.status_code, self.status_code.HTTP_400_BAD_REQUEST
        )
