from django.apps import apps
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from model_bakery import random_gen

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        users = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True, _quantity=4)
        cls.activated_initial_password = get_user_model().objects.make_random_password(
            length=12
        )
        users[0].set_password(cls.activated_initial_password)
        users[0].save()
        cls.activated_user = authenticate(
            username=users[0].username, password=cls.activated_initial_password
        )

    def test_list_users(self):
        self.client.force_authenticate(self.activated_user)
        url = self.reverse("user-list", kwargs={"version": "v1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_user_me_get(self):
        self.client.force_authenticate(self.activated_user)
        url = self.reverse("user-me", kwargs={"version": "v1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_user_me_patch(self):
        self.client.force_authenticate(self.activated_user)
        self.assertTrue(self.activated_user.is_active)
        new_name = random_gen.gen_string(max_length=20)
        data = {"first_name": new_name, "password": self.activated_initial_password}
        url = self.reverse("user-me", kwargs={"version": "v1"})
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        updated_user = get_user_model().objects.get(pk=self.activated_user.pk)
        self.assertEqual(updated_user.first_name, new_name)

    def test_user_change_password(self):
        user = self.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        user_initial_password = get_user_model().objects.make_random_password(length=12)
        user.set_password(user_initial_password)
        user.save()
        user = authenticate(username=user.username, password=user_initial_password)
        self.assertIsNotNone(user)
        self.client.force_authenticate(user)
        new_password = get_user_model().objects.make_random_password(length=12)
        data = {
            "old_password": user_initial_password,
            "new_password": new_password,
            "re_new_password": new_password,
        }
        url = self.reverse("user-change-password", kwargs={"version": "v1"})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        user = authenticate(username=user.username, password=new_password)
        self.assertIsNotNone(user)

    def test_user_email_verify(self):
        non_activated_user_pass = get_user_model().objects.make_random_password(
            length=12
        )
        non_activated_user_username = random_gen.gen_string(15)
        user_data = {
            "username": non_activated_user_username,
            "email": random_gen.gen_email(),
            "first_name": random_gen.gen_string(150),
            "last_name": random_gen.gen_string(150),
            "password": non_activated_user_pass,
            "re_password": non_activated_user_pass,
            "organization": random_gen.gen_string(255),
            "role": random_gen.gen_string(50),
        }
        url = self.reverse("user-register", kwargs={"version": "v1"})
        response = self.client.post(url, data=user_data)
        self.assertEqual(response.status_code, self.status_code.HTTP_201_CREATED)
        non_activated_user = get_user_model().objects.get(
            username=non_activated_user_username
        )
        url = self.reverse("user-email-confirm", kwargs={"version": "v1"})
        user = authenticate(
            username=non_activated_user.username, password=non_activated_user_pass
        )
        self.assertIsNone(user)
        email_verify_pin = (
            apps.get_model("user", "EmailConfirmationPin")
            .objects.get(user=non_activated_user)
            .pin
        )
        response = self.client.post(
            url,
            data={
                "username": non_activated_user.username,
                "pin": email_verify_pin,
            },
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        email_verified = get_user_model().objects.get(
            username=non_activated_user.username
        )
        self.assertTrue(email_verified.check_password(non_activated_user_pass))

    def test_password_reset_flow(self):
        user = self.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        password_reset_url = self.reverse(
            "user-password-reset", kwargs={"version": "v1"}
        )
        password_reset_verify_url = self.reverse(
            "user-password-reset-verify", kwargs={"version": "v1"}
        )
        password_reset_change_url = self.reverse(
            "user-password-reset-change", kwargs={"version": "v1"}
        )
        password_reset_send = self.client.post(
            password_reset_url, data={"username": user.username}
        )
        self.assertEqual(password_reset_send.status_code, self.status_code.HTTP_200_OK)
        password_reset_pin = (
            apps.get_model("user", "PasswordResetPin").objects.get(user=user).pin
        )
        password_reset_verify = self.client.post(
            password_reset_verify_url,
            data={"username": user.username, "pin": password_reset_pin},
        )
        self.assertEqual(
            password_reset_verify.status_code, self.status_code.HTTP_200_OK
        )
        identifier = password_reset_verify.json()["identifier"]
        new_pass = "secure^78@12"
        password_reset_change = self.client.post(
            password_reset_change_url,
            data={
                "username": user.username,
                "identifier": identifier,
                "password": new_pass,
                "re_password": new_pass,
            },
        )
        self.assertEqual(
            password_reset_change.status_code, self.status_code.HTTP_200_OK
        )
        user = authenticate(username=user.username, password=new_pass)
        self.assertIsNotNone(user)

    def test_email_change_flow(self):
        self.client.force_authenticate(self.activated_user)
        email_change_url = self.reverse("user-email-change", kwargs={"version": "v1"})
        email_change_verify_url = self.reverse(
            "user-email-change-verify", kwargs={"version": "v1"}
        )
        new_email = random_gen.gen_email().lower()
        email_change_data = {
            "new_email": new_email,
            "password": self.activated_initial_password,
        }
        email_change_response = self.client.post(
            email_change_url, data=email_change_data
        )
        self.assertEqual(
            email_change_response.status_code, self.status_code.HTTP_200_OK
        )
        email_change_pin = (
            apps.get_model("user", "EmailChangePin")
            .objects.get(user=self.activated_user)
            .pin
        )
        email_change_verify_data = {"pin": email_change_pin}
        email_change_verify_response = self.client.post(
            email_change_verify_url, data=email_change_verify_data
        )
        self.assertEqual(
            email_change_verify_response.status_code, self.status_code.HTTP_200_OK
        )
        user = get_user_model().objects.get(pk=self.activated_user.pk)
        self.assertEqual(new_email, user.email)
