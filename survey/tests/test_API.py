from django.conf import settings
from model_bakery import random_gen

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL)
        organization = cls.baker.make(
            "organization.Organization", members=[cls.user], status="accepted"
        )
        project = cls.baker.make(
            "project.Project",
            organization=organization,
            users=[cls.user],
            status="accepted",
        )
        question_group = cls.baker.make("survey.QuestionGroup")
        question = cls.baker.make(
            "survey.Question", group=question_group, answer_type="single_option"
        )
        option = cls.baker.make("survey.Option", question=question)
        survey = cls.baker.make("survey.Survey", project=project)
        survey_answer = cls.baker.make(
            "survey.SurveyAnswer",
            survey=survey,
            answer_type="single_option",
            question=question,
            options=[option],
        )
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

    def test_share_survey(self):
        self.client.force_authenticate(self.user)
        survey = self.baker.make("survey.Survey", created_by=self.user)
        url = self.reverse(
            "survey-share-link", kwargs={"version": "v1", "pk": survey.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_unshare_survey(self):
        self.client.force_authenticate(self.user)
        survey = self.baker.make(
            "survey.Survey",
            created_by=self.user,
            is_shared_publicly=True,
            shared_link_identifier=random_gen.gen_string(10),
        )
        url = self.reverse(
            "survey-unshare-link", kwargs={"version": "v1", "pk": survey.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_update_share_survey(self):
        self.client.force_authenticate(self.user)
        survey_1 = self.baker.make(
            "survey.Survey",
            created_by=self.user,
            is_shared_publicly=True,
            shared_link_identifier=random_gen.gen_string(10),
        )
        url = self.reverse(
            "survey-update-link", kwargs={"version": "v1", "pk": survey_1.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        survey_2 = self.baker.make(
            "survey.Survey",
            created_by=self.user,
        )
        url = self.reverse(
            "survey-update-link", kwargs={"version": "v1", "pk": survey_2.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_400_BAD_REQUEST)

    def test_get_identifier_survey(self):
        shared_link_identifier = random_gen.gen_string(10)
        survey = self.baker.make(
            "survey.Survey",
            is_shared_publicly=True,
            shared_link_identifier=shared_link_identifier,
        )
        url = self.reverse(
            "survey-identifier",
            kwargs={
                "version": "v1",
                "shared_link_identifier": shared_link_identifier,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
        survey.is_shared_publicly = False
        survey.save()
        url = self.reverse(
            "survey-identifier",
            kwargs={
                "version": "v1",
                "shared_link_identifier": shared_link_identifier,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.status_code.HTTP_404_NOT_FOUND)
