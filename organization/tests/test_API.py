from django.conf import settings

from neatplus.tests import FullTestCase


class TestAPI(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        organization = cls.baker.make(
            "organization.Organization",
        )
        cls.organization_list_url = cls.reverse(
            "organization-list", kwargs={"version": "v1"}
        )
        cls.organization_detail_url = cls.reverse(
            "organization-detail", kwargs={"version": "v1", "pk": organization.pk}
        )

    def test_organization_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.organization_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_organization_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.organization_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
