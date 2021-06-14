from django.conf import settings

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.baker.make(settings.AUTH_USER_MODEL)
        questions = cls.baker.make("survey.Question", _quantity=3)
        options = cls.baker.make("survey.Option", _quantity=3)
        statement_topic = cls.baker.make("summary.StatementTopic")
        cls.statement = cls.baker.make(
            "summary.Statement",
            topic=statement_topic,
            questions=questions,
            options=options,
        )
        cls.mitigation = cls.baker.make(
            "summary.Mitigation", statement=cls.statement, options=options
        )
        cls.opportunity = cls.baker.make(
            "summary.Opportunity", statement=cls.statement, options=options
        )
        question_statement = cls.baker.make("summary.QuestionStatement")
        option_statement = cls.baker.make("summary.OptionStatement")
        option_mitigation = cls.baker.make("summary.OptionMitigation")
        option_opportunity = cls.baker.make("summary.OptionOpportunity")

        cls.statement_topic_list_url = cls.reverse(
            "statement-topic-list", kwargs={"version": "v1"}
        )
        cls.statement_topic_detail_url = cls.reverse(
            "statement-topic-detail", kwargs={"version": "v1", "pk": statement_topic.pk}
        )

        cls.statement_list_url = cls.reverse("statement-list", kwargs={"version": "v1"})
        cls.statement_detail_url = cls.reverse(
            "statement-detail", kwargs={"version": "v1", "pk": cls.statement.pk}
        )

        cls.mitigation_list_url = cls.reverse(
            "mitigation-list", kwargs={"version": "v1"}
        )
        cls.mitigation_detail_url = cls.reverse(
            "mitigation-detail", kwargs={"version": "v1", "pk": cls.mitigation.pk}
        )

        cls.opportunity_list_url = cls.reverse(
            "opportunity-list", kwargs={"version": "v1"}
        )
        cls.opportunity_detail_url = cls.reverse(
            "opportunity-detail", kwargs={"version": "v1", "pk": cls.opportunity.pk}
        )

        cls.question_statement_list_url = cls.reverse(
            "question-statement-list", kwargs={"version": "v1"}
        )
        cls.question_statement_detail_url = cls.reverse(
            "question-statement-detail",
            kwargs={"version": "v1", "pk": question_statement.pk},
        )

        cls.option_statement_list_url = cls.reverse(
            "option-statement-list", kwargs={"version": "v1"}
        )
        cls.option_statement_detail_url = cls.reverse(
            "option-statement-detail",
            kwargs={"version": "v1", "pk": option_statement.pk},
        )

        cls.option_mitigation_list_url = cls.reverse(
            "option-mitigation-list", kwargs={"version": "v1"}
        )
        cls.option_mitigation_detail_url = cls.reverse(
            "option-mitigation-detail",
            kwargs={"version": "v1", "pk": option_mitigation.pk},
        )

        cls.option_opportunity_list_url = cls.reverse(
            "option-opportunity-list", kwargs={"version": "v1"}
        )
        cls.option_opportunity_detail_url = cls.reverse(
            "option-opportunity-detail",
            kwargs={"version": "v1", "pk": option_opportunity.pk},
        )

    def test_statement_topic_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.statement_topic_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_topic_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.statement_topic_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.statement_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.statement_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_mitigation_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.mitigation_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_mitigation_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.mitigation_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_opportunity_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.opportunity_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_opportunity_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.opportunity_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_question_statement_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.question_statement_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_question_statement_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.question_statement_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_statement_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.option_statement_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_statement_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.option_statement_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_mitigation_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.option_mitigation_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_mitigation_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.option_mitigation_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_opportunity_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.option_opportunity_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_opportunity_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.option_opportunity_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
