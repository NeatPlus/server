from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        statement_topic = cls.baker.make("summary.StatementTopic")
        statement = cls.baker.make("summary.Statement")
        mitigation = cls.baker.make("summary.Mitigation")
        opportunity = cls.baker.make("summary.Opportunity")
        cls.statement_topic_list_url = cls.reverse(
            "statement-topic-list", kwargs={"version": "v1"}
        )
        cls.statement_topic_detail_url = cls.reverse(
            "statement-topic-detail", kwargs={"version": "v1", "pk": statement_topic.pk}
        )
        cls.statement_list_url = cls.reverse("statement-list", kwargs={"version": "v1"})
        cls.statement_detail_url = cls.reverse(
            "statement-detail", kwargs={"version": "v1", "pk": statement.pk}
        )
        cls.mitigation_list_url = cls.reverse(
            "mitigation-list", kwargs={"version": "v1"}
        )
        cls.mitigation_detail_url = cls.reverse(
            "mitigation-detail", kwargs={"version": "v1", "pk": mitigation.pk}
        )
        cls.opportunity_list_url = cls.reverse(
            "opportunity-list", kwargs={"version": "v1"}
        )
        cls.opportunity_detail_url = cls.reverse(
            "opportunity-detail", kwargs={"version": "v1", "pk": opportunity.pk}
        )

    def test_statement_topic_list(self):
        response = self.client.get(self.statement_topic_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_topic_detail(self):
        response = self.client.get(self.statement_topic_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_list(self):
        response = self.client.get(self.statement_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_detail(self):
        response = self.client.get(self.statement_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_mitigation_list(self):
        response = self.client.get(self.mitigation_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_mitigation_detail(self):
        response = self.client.get(self.mitigation_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_opportunity_list(self):
        response = self.client.get(self.opportunity_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_opportunity_detail(self):
        response = self.client.get(self.opportunity_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
