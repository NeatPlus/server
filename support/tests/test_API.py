from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        legal_document = cls.baker.make("support.LegalDocument")
        frequently_asked_question = cls.baker.make("support.FrequentlyAskedQuestion")
        resource_tag = cls.baker.make("support.ResourceTag")
        resource = cls.baker.make("support.Resource")
        action = cls.baker.make("support.Action")
        cls.legal_document_list_url = cls.reverse(
            "legal-document-list", kwargs={"version": "v1"}
        )
        cls.legal_document_detail_url = cls.reverse(
            "legal-document-detail",
            kwargs={"version": "v1", "pk": legal_document.pk},
        )
        cls.frequently_asked_question_list_url = cls.reverse(
            "frequently-asked-question-list", kwargs={"version": "v1"}
        )
        cls.frequently_asked_question_detail_url = cls.reverse(
            "frequently-asked-question-detail",
            kwargs={"version": "v1", "pk": frequently_asked_question.pk},
        )
        cls.resource_tag_list_url = cls.reverse(
            "resource-tag-list", kwargs={"version": "v1"}
        )
        cls.resource_tag_detail_url = cls.reverse(
            "resource-tag-detail",
            kwargs={"version": "v1", "pk": resource_tag.pk},
        )
        cls.resource_list_url = cls.reverse("resource-list", kwargs={"version": "v1"})
        cls.resource_detail_url = cls.reverse(
            "resource-detail",
            kwargs={"version": "v1", "pk": resource.pk},
        )
        cls.action_list_url = cls.reverse("action-list", kwargs={"version": "v1"})
        cls.action_detail_url = cls.reverse(
            "action-detail",
            kwargs={"version": "v1", "pk": action.pk},
        )

    def test_legal_document_list(self):
        response = self.client.get(self.legal_document_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_legal_document_detail(self):
        response = self.client.get(self.legal_document_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_frequently_asked_question_list(self):
        response = self.client.get(self.frequently_asked_question_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_frequently_asked_question_detail(self):
        response = self.client.get(self.frequently_asked_question_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_resource_tag_list(self):
        response = self.client.get(self.resource_tag_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_resource_tag_detail(self):
        response = self.client.get(self.resource_tag_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_resource_list(self):
        response = self.client.get(self.resource_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_resource_detail(self):
        response = self.client.get(self.resource_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_action_list(self):
        response = self.client.get(self.action_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_action_detail(self):
        response = self.client.get(self.action_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
