from django.conf import settings

from neatplus.tests import FullTestCase


class APITest(FullTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        questions = cls.baker.make("survey.Question", _quantity=3)
        options = cls.baker.make("survey.Option", _quantity=3)
        statement_topic = cls.baker.make("statement.StatementTopic")
        statement_tag_group = cls.baker.make("statement.StatementTagGroup")
        statement_tag = cls.baker.make(
            "statement.StatementTag", group=statement_tag_group
        )
        cls.statement = cls.baker.make(
            "statement.Statement",
            topic=statement_topic,
            tags=[statement_tag],
            questions=questions,
            options=options,
        )
        cls.mitigation = cls.baker.make(
            "statement.Mitigation", statement=cls.statement, options=options
        )
        cls.opportunity = cls.baker.make(
            "statement.Opportunity", statement=cls.statement, options=options
        )
        question_statement = cls.baker.make("statement.QuestionStatement")
        option_statement = cls.baker.make("statement.OptionStatement")
        option_mitigation = cls.baker.make("statement.OptionMitigation")
        option_opportunity = cls.baker.make("statement.OptionOpportunity")

        cls.statement_topic_list_url = cls.reverse(
            "statement-topic-list", kwargs={"version": "v1"}
        )
        cls.statement_topic_detail_url = cls.reverse(
            "statement-topic-detail", kwargs={"version": "v1", "pk": statement_topic.pk}
        )

        cls.statement_tag_group_list_url = cls.reverse(
            "statement-tag-group-list", kwargs={"version": "v1"}
        )
        cls.statement_tag_group_detail_url = cls.reverse(
            "statement-tag-group-detail",
            kwargs={"version": "v1", "pk": statement_tag_group.pk},
        )
        cls.statement_tag_list_url = cls.reverse(
            "statement-tag-list", kwargs={"version": "v1"}
        )
        cls.statement_tag_detail_url = cls.reverse(
            "statement-tag-detail", kwargs={"version": "v1", "pk": statement_tag.pk}
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
        response = self.client.get(self.statement_topic_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_topic_detail(self):
        response = self.client.get(self.statement_topic_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_tag_group_list(self):
        response = self.client.get(self.statement_tag_group_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_tag_group_detail(self):
        response = self.client.get(self.statement_tag_group_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_tag_list(self):
        response = self.client.get(self.statement_tag_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_statement_tag_detail(self):
        response = self.client.get(self.statement_tag_detail_url)
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

    def test_question_statement_list(self):
        response = self.client.get(self.question_statement_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_question_statement_detail(self):
        response = self.client.get(self.question_statement_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_statement_list(self):
        response = self.client.get(self.option_statement_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_statement_detail(self):
        response = self.client.get(self.option_statement_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_mitigation_list(self):
        response = self.client.get(self.option_mitigation_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_mitigation_detail(self):
        response = self.client.get(self.option_mitigation_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_opportunity_list(self):
        response = self.client.get(self.option_opportunity_list_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)

    def test_option_opportunity_detail(self):
        response = self.client.get(self.option_opportunity_detail_url)
        self.assertEqual(response.status_code, self.status_code.HTTP_200_OK)
