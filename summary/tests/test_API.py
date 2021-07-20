from django.conf import settings

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL, is_active=True)
        organization = cls.baker.make(
            "organization.Organization", members=[cls.user], status="accepted"
        )
        project = cls.baker.make(
            "project.Project",
            organization=organization,
            users=[cls.user],
            status="accepted",
        )
        survey = cls.baker.make("survey.Survey", project=project)
        statement = cls.baker.make("statement.Statement")
        survey_result = cls.baker.make(
            "summary.SurveyResult",
            survey=survey,
            statement=statement,
        )
        cls.survey_result_list_url = cls.reverse(
            "survey-result-list", kwargs={"version": "v1"}
        )
        cls.survey_result_detail_url = cls.reverse(
            "survey-result-detail", kwargs={"version": "v1", "pk": survey_result.pk}
        )

    def test_survey_result_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_result_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_survey_result_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.survey_result_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
