from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

from neatplus.tests import FullTestCase


class TestAdmin(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_pass = get_user_model().objects.make_random_password(length=12)
        user = cls.baker.make(
            settings.AUTH_USER_MODEL, is_superuser=True, is_staff=True, is_active=True
        )
        user.set_password(cls.user_pass)
        user.save()
        cls.user = get_user_model().objects.get(username=user.username)

    def test_admin_changelist_view(self):
        self.client.login(username=self.user.username, password=self.user_pass)
        for model, _ in admin.site._registry.items():
            self.baker.make(model, _quantity=3)
            url = self.reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
            )
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                self.status_code.HTTP_200_OK,
                msg=f"Test failed for url {url}",
            )

    def test_admin_add_view(self):
        self.client.login(username=self.user.username, password=self.user_pass)
        for model, modeladmin in admin.site._registry.items():
            url = self.reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_add"
            )
            request = self.factory.get(url)
            request.user = self.user
            if modeladmin.has_add_permission(request):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    self.status_code.HTTP_200_OK,
                    msg=f"Test failed for url {url}",
                )

    def test_admin_delete_view(self):
        self.client.login(username=self.user.username, password=self.user_pass)
        for model, modeladmin in admin.site._registry.items():
            object_id = self.baker.make(model).id
            url = self.reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_delete",
                args=(object_id,),
            )
            request = self.factory.get(url)
            request.user = self.user
            if modeladmin.has_delete_permission(request):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    self.status_code.HTTP_200_OK,
                    msg=f"Test failed for url {url}",
                )

    def test_admin_change_view(self):
        self.client.login(username=self.user.username, password=self.user_pass)
        for model, modeladmin in admin.site._registry.items():
            object_id = self.baker.make(model).id
            url = self.reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_change",
                args=(object_id,),
            )
            request = self.factory.get(url)
            request.user = self.user
            if modeladmin.has_change_permission(request):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    self.status_code.HTTP_200_OK,
                    msg=f"Test failed for url {url}",
                )
