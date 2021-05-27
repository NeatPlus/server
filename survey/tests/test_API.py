from django.conf import settings

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL)
        organization = cls.baker.make("organization.Organization", members=[cls.user])
        project = cls.baker.make(
            "project.Project",
            organization=organization,
            users=[cls.user],
            status="accepted",
        )
        question_group = cls.baker.make("survey.QuestionGroup")
        question = cls.baker.make("survey.Question", group=question_group)
        option = cls.baker.make("survey.Option", question=question)
        survey = cls.baker.make("survey.Survey", project=project)
        survey_answer = cls.baker.make("survey.SurveyAnswer", survey=survey)
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
        cls.survey_list_url = cls.reverse("survey-list", kwargs={"version": "v1"})
        cls.survey_detail_url = cls.reverse(
            "survey-detail", kwargs={"version": "v1", "pk": survey.pk}
        )
        cls.survey_answer_list_url = cls.reverse(
            "survey-answer-list", kwargs={"version": "v1"}
        )
        cls.survey_answer_detail_url = cls.reverse(
            "survey-answer-detail", kwargs={"version": "v1", "pk": survey_answer.pk}
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

    def test_survey_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_survey_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_survey_answer_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_answer_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_survey_answer_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_answer_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
