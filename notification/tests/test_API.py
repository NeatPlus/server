from django.conf import settings

from neatplus.tests import FullTestCase


class TestAPI(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = cls.baker.make(
            settings.AUTH_USER_MODEL, is_superuser=True, is_active=True
        )
        cls.user = user
        notifications = cls.baker.make(
            "notification.Notification", recipient=user, _quantity=5
        )
        cls.notification = notifications.pop()
        cls.notification_list_url = cls.reverse(
            "notification-list", kwargs={"version": "v1"}
        )
        cls.notification_detail_url = cls.reverse(
            "notification-detail", kwargs={"version": "v1", "pk": cls.notification.pk}
        )

    def test_get_notification_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(
            self.notification_list_url,
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_get_notification_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(
            self.notification_detail_url,
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_get_notification_unread_count(self):
        self.client.force_authenticate(self.user)
        url = self.reverse("notification-unread-count", kwargs={"version": "v1"})
        response = self.client.get(
            url,
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_get_notification_mark_as_read(self):
        self.client.force_authenticate(self.user)
        url = self.reverse(
            "notification-mark-as-read",
            kwargs={"version": "v1", "pk": self.notification.pk},
        )
        response = self.client.post(
            url,
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_get_notification_mark_all_as_read(self):
        self.client.force_authenticate(self.user)
        url = self.reverse("notification-mark-all-as-read", kwargs={"version": "v1"})
        response = self.client.post(
            url,
        )
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
