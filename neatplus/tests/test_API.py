from django.conf import settings

from neatplus.tests import APIFullTestCase


class TestAPI(APIFullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = cls.baker.make(
            settings.AUTH_USER_MODEL, is_superuser=True, is_active=True
        )
        cls.user_pass = "adminpass@123!$"
        user.set_password(cls.user_pass)
        user.save()
        cls.user = user

    def test_jwt_login(self):
        jwt_create_url = self.reverse("jwt-create", kwargs={"version": "v1"})
        response = self.client.post(
            jwt_create_url,
            data={"username": self.user.username, "password": self.user_pass},
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_email_jwt_login(self):
        jwt_create_url = self.reverse("jwt-create", kwargs={"version": "v1"})
        response = self.client.post(
            jwt_create_url,
            data={"username": self.user.email, "password": self.user_pass},
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
