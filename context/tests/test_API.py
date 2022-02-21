from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        context = cls.baker.make("context.Context")
        module = cls.baker.make("context.Module")
        cls.context_list_url = cls.reverse("context-list", kwargs={"version": "v1"})
        cls.context_detail_url = cls.reverse(
            "context-detail", kwargs={"version": "v1", "pk": context.pk}
        )
        cls.module_list_url = cls.reverse("module-list", kwargs={"version": "v1"})
        cls.module_detail_url = cls.reverse(
            "module-detail", kwargs={"version": "v1", "pk": module.pk}
        )

    def test_context_list(self):
        response = self.client.get(self.context_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_context_detail(self):
        response = self.client.get(self.context_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_module_list(self):
        response = self.client.get(self.module_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_module_detail(self):
        response = self.client.get(self.module_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
