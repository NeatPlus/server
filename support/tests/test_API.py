from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        frequently_asked_question = cls.baker.make("support.FrequentlyAskedQuestion")
        cls.frequently_asked_question_list_url = cls.reverse(
            "frequently-asked-question-list", kwargs={"version": "v1"}
        )
        cls.frequently_asked_question_detail_url = cls.reverse(
            "frequently-asked-question-detail",
            kwargs={"version": "v1", "pk": frequently_asked_question.pk},
        )

    def test_frequently_asked_question_list(self):
        response = self.client.get(self.frequently_asked_question_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_frequently_asked_question_detail(self):
        response = self.client.get(self.frequently_asked_question_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
