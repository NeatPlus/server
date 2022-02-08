from django.conf import settings
from django.contrib.auth import get_user_model

from neatplus.tests import FullTestCase
from neatplus.utils import gen_random_password


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = cls.baker.make(
            settings.AUTH_USER_MODEL, is_superuser=True, is_active=True
        )
        cls.user_pass = gen_random_password(user=user)
        user.set_password(cls.user_pass)
        user.save()
        cls.user = user

    def test_username_jwt_login(self):
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
