from django.conf import settings

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        organization = cls.baker.make(
            "organization.Organization", admins=[cls.user], status="accepted"
        )
        project = cls.baker.make(
            "project.Project",
            organization=organization,
            users=[cls.user],
            status="accepted",
        )
        survey = cls.baker.make("survey.Survey", project=project)
        statement = cls.baker.make("statement.Statement")
        cls.survey_result = cls.baker.make(
            "summary.SurveyResult",
            survey=survey,
            statement=statement,
        )
        cls.survey_result_feedback = cls.baker.make(
            "summary.SurveyResultFeedback", survey_result=cls.survey_result
        )
        cls.survey_result_list_url = cls.reverse(
            "survey-result-list", kwargs={"version": "v1"}
        )
        cls.survey_result_detail_url = cls.reverse(
            "survey-result-detail", kwargs={"version": "v1", "pk": cls.survey_result.pk}
        )
        cls.survey_result_feedback_list_url = cls.reverse(
            "survey-result-feedback-list", kwargs={"version": "v1"}
        )
        cls.survey_result_feedback_detail_url = cls.reverse(
            "survey-result-feedback-detail",
            kwargs={"version": "v1", "pk": cls.survey_result_feedback.pk},
        )

    def test_survey_result_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_result_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_result_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_result_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_result_add_feedback(self):
        self.client.force_authenticate(self.user)
        url = self.reverse(
            "survey-result-add-feedback",
            kwargs={
                "version": "v1",
            },
        )
        data = [
            {
                "survey_result": self.survey_result.pk,
                "expected_score": 0.7,
                "comment": self.baker.random_gen.gen_text(),
            }
        ]
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(
            response.status_code, self.status_code.HTTP_201_CREATED, response.json()
        )

    def test_survey_result_add_baseline_feedback(self):
        super_user = self.baker.make(
            settings.AUTH_USER_MODEL, is_active=True, is_superuser=True
        )
        self.client.force_authenticate(super_user)
        url = self.reverse(
            "survey-result-add-baseline-feedback",
            kwargs={"version": "v1"},
        )
        data = [
            {
                "survey_result": self.survey_result.pk,
                "expected_score": 0.12,
                "comment": self.baker.random_gen.gen_text(),
            }
        ]
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(
            response.status_code, self.status_code.HTTP_201_CREATED, response.json()
        )

    def test_survey_result_feedback_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_result_feedback_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_result_feedback_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_result_feedback_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_result_feedback_acknowledge(self):
        self.client.force_authenticate(self.user)
        url = self.reverse(
            "survey-result-feedback-acknowledge",
            kwargs={"version": "v1", "pk": self.survey_result_feedback.pk},
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_survey_insight(self):
        self.client.force_authenticate(self.user)
        url = self.reverse(
            "survey-insight",
            kwargs={"version": "v1"},
            params={
                "statement": self.survey_result.statement.pk,
                "module": self.survey_result.module.pk,
            },
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
