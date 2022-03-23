from django.conf import settings
from model_bakery import random_gen

from neatplus.tests import FullTestCase
from summary.models import SurveyResult
from survey.models import SurveyAnswer


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
        module = cls.baker.make("context.Module")
        question_group = cls.baker.make("survey.QuestionGroup", module=module)
        cls.question = cls.baker.make(
            "survey.Question",
            group=question_group,
            answer_type="single_option",
        )
        option = cls.baker.make("survey.Option", question=cls.question)
        cls.survey = cls.baker.make(
            "survey.Survey", project=project, created_by=cls.user
        )
        survey_answer = cls.baker.make(
            "survey.SurveyAnswer",
            survey=cls.survey,
            answer_type="single_option",
            question=cls.question,
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
            "question-detail", kwargs={"version": "v1", "pk": cls.question.pk}
        )
        cls.option_list_url = cls.reverse("option-list", kwargs={"version": "v1"})
        cls.option_detail_url = cls.reverse(
            "option-detail", kwargs={"version": "v1", "pk": option.pk}
        )
        cls.survey_list_url = cls.reverse("survey-list", kwargs={"version": "v1"})
        cls.survey_detail_url = cls.reverse(
            "survey-detail", kwargs={"version": "v1", "pk": cls.survey.pk}
        )
        cls.survey_answer_list_url = cls.reverse(
            "survey-answer-list", kwargs={"version": "v1"}
        )
        cls.survey_answer_detail_url = cls.reverse(
            "survey-answer-detail", kwargs={"version": "v1", "pk": survey_answer.pk}
        )

    def test_question_group_list(self):
        response = self.client.get(self.question_group_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_question_group_detail(self):
        response = self.client.get(self.question_group_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_question_list(self):
        response = self.client.get(self.question_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_question_detail(self):
        response = self.client.get(self.question_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_option_list(self):
        response = self.client.get(self.option_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_option_detail(self):
        response = self.client.get(self.option_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_answer_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_answer_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_answer_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_answer_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_share_survey(self):
        self.client.force_authenticate(self.user)
        survey = self.baker.make("survey.Survey", created_by=self.user)
        url = self.reverse(
            "survey-share-link", kwargs={"version": "v1", "pk": survey.pk}
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

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
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

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
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
        survey_2 = self.baker.make(
            "survey.Survey",
            created_by=self.user,
        )
        url = self.reverse(
            "survey-update-link", kwargs={"version": "v1", "pk": survey_2.pk}
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_400_BAD_REQUEST, response.json()
        )

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
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
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
        self.assertEqual(
            response.status_code, self.status_code.HTTP_404_NOT_FOUND, response.json()
        )

    def test_add_survey_answers(self):
        url = self.reverse(
            "survey-add-answers", kwargs={"version": "v1", "pk": self.survey.pk}
        )
        question_1 = self.baker.make("survey.Question", answer_type="location")
        question_2 = self.baker.make("survey.Question", answer_type="number")
        question_3 = self.baker.make("survey.Question", answer_type="boolean")
        question_4 = self.baker.make("survey.Question", answer_type="single_option")
        question_4_option = self.baker.make("survey.Option", question=question_4)
        question_5 = self.baker.make("survey.Question", answer_type="multiple_option")
        question_5_option_1 = self.baker.make("survey.Option", question=question_5)
        question_5_option_2 = self.baker.make("survey.Option", question=question_5)
        data = [
            {
                "question": question_1.pk,
                "answer": '{"type": "Point", "coordinates": [5.000000, 23.000000]}',
                "answerType": "location",
            },
            {
                "question": question_2.pk,
                "answer": 2,
                "answerType": "number",
            },
            {
                "question": question_3.pk,
                "answer": "true",
                "answerType": "boolean",
            },
            {
                "question": question_4.pk,
                "answerType": "single_option",
                "options": [question_4_option.pk],
            },
            {
                "question": question_5.pk,
                "answerType": "multiple_option",
                "options": [question_5_option_1.pk, question_5_option_2.pk],
            },
        ]
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(
            response.status_code, self.status_code.HTTP_201_CREATED, response.json()
        )
        self.assertTrue(
            SurveyAnswer.objects.filter(
                question=question_2.pk, answer="2", survey=self.survey.pk
            ).exists()
        )
        self.assertTrue(
            SurveyAnswer.objects.filter(
                question=question_3.pk, answer="true", survey=self.survey.pk
            ).exists()
        )
        update_data = [
            {
                "question": question_3.pk,
                "answer": "false",
                "answerType": "boolean",
            },
        ]
        update_response = self.client.post(url, data=update_data, format="json")
        self.assertEqual(
            update_response.status_code,
            self.status_code.HTTP_201_CREATED,
            update_response.json(),
        )
        self.assertTrue(
            SurveyAnswer.objects.filter(
                question=question_2.pk, answer="2", survey=self.survey.pk
            ).exists()
        )
        self.assertTrue(
            SurveyAnswer.objects.filter(
                question=question_3.pk, answer="false", survey=self.survey.pk
            ).exists()
        )

    def test_add_survey_results(self):
        url = self.reverse(
            "survey-add-results", kwargs={"version": "v1", "pk": self.survey.pk}
        )
        statement_1, statement_2 = self.baker.make("statement.Statement", _quantity=2)
        data = [
            {
                "statement": statement_1.pk,
                "score": 0.90,
                "module": self.question.group.module.pk,
            },
            {
                "statement": statement_2.pk,
                "score": 0.67,
                "module": self.question.group.module.pk,
            },
        ]
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(
            response.status_code, self.status_code.HTTP_201_CREATED, response.json()
        )
        self.assertTrue(
            SurveyResult.objects.filter(
                statement=statement_1.pk,
                module=self.question.group.module.pk,
                survey=self.survey.pk,
                score=0.90,
            ).exists()
        )
        self.assertTrue(
            SurveyResult.objects.filter(
                statement=statement_2.pk,
                module=self.question.group.module.pk,
                survey=self.survey.pk,
                score=0.67,
            ).exists()
        )
        update_data = [
            {
                "statement": statement_2.pk,
                "score": 0.37,
                "module": self.question.group.module.pk,
            },
        ]
        update_response = self.client.post(url, data=update_data, format="json")
        self.assertEqual(
            update_response.status_code,
            self.status_code.HTTP_201_CREATED,
            update_response.json(),
        )
        self.assertTrue(
            SurveyResult.objects.filter(
                statement=statement_1.pk,
                module=self.question.group.module.pk,
                survey=self.survey.pk,
                score=0.90,
            ).exists()
        )
        self.assertTrue(
            SurveyResult.objects.filter(
                statement=statement_2.pk,
                module=self.question.group.module.pk,
                survey=self.survey.pk,
                score=0.37,
            ).exists()
        )
