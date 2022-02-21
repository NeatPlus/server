from django.conf import settings

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        cls.organization = cls.baker.make(
            "organization.Organization", status="accepted", admins=[cls.admin_user]
        )
        cls.organization_member_request = cls.baker.make(
            "organization.OrganizationMemberRequest",
            organization=cls.organization,
            created_by=cls.user,
        )
        cls.organization_list_url = cls.reverse(
            "organization-list", kwargs={"version": "v1"}
        )
        cls.organization_detail_url = cls.reverse(
            "organization-detail", kwargs={"version": "v1", "pk": cls.organization.pk}
        )

        cls.organization_member_request_list_url = cls.reverse(
            "organization-member-request-list", kwargs={"version": "v1"}
        )
        cls.organization_member_request_detail_url = cls.reverse(
            "organization-member-request-detail",
            kwargs={"version": "v1", "pk": cls.organization_member_request.pk},
        )

    def test_organization_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.organization_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_organization_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.organization_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_organization_creation(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "sample_organization",
            "description": "Description goes here",
        }
        post_response = self.client.post(self.organization_list_url, data=data)
        self.assertEqual(
            post_response.status_code,
            self.status_code.HTTP_201_CREATED,
            post_response.json(),
        )

    def test_member_request(self):
        user = self.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        self.client.force_authenticate(user)
        url = self.reverse(
            "organization-member-request",
            kwargs={"version": "v1", "pk": self.organization.pk},
        )
        post_response = self.client.post(url)
        self.assertEqual(
            post_response.status_code,
            self.status_code.HTTP_200_OK,
            post_response.json(),
        )

    def test_organization_member_request_list(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.organization_member_request_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_organization_member_request_detail(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.organization_member_request_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_member_request_accept(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "organization-member-request-accept",
            kwargs={"version": "v1", "pk": self.organization_member_request.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_member_request_reject(self):
        self.client.force_authenticate(self.admin_user)
        url = self.reverse(
            "organization-member-request-reject",
            kwargs={"version": "v1", "pk": self.organization_member_request.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
