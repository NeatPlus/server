from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        question_group = cls.baker.make("survey.QuestionGroup")
        question = cls.baker.make("survey.Question", group=question_group)
        option = cls.baker.make("survey.Option", question=question)
        cls.question_group_list_url = cls.reverse(
            "question-group-list", kwargs={"version": "v1"}
        )
        cls.question_group_detail_url = cls.reverse(
            "question-group-detail", kwargs={"version": "v1", "pk": question_group.pk}
        )
        cls.question_list_url = cls.reverse("question-list", kwargs={"version": "v1"})
        cls.question_detail_url = cls.reverse(
            "question-detail", kwargs={"version": "v1", "pk": question.pk}
        )
        cls.option_list_url = cls.reverse("option-list", kwargs={"version": "v1"})
        cls.option_detail_url = cls.reverse(
            "option-detail", kwargs={"version": "v1", "pk": option.pk}
        )

    def test_question_group_list(self):
        response = self.client.get(self.question_group_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_question_group_detail(self):
        response = self.client.get(self.question_group_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_question_list(self):
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_question_detail(self):
        response = self.client.get(self.question_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_list(self):
        response = self.client.get(self.option_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_detail(self):
        response = self.client.get(self.option_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
