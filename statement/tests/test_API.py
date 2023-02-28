from django.conf import settings

from neatplus.tests import FullTestCase
from statement.models import OptionStatement, QuestionStatement, StatementFormula


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
            "statement.Mitigation", statements=[cls.statement], options=options
        )
        cls.opportunity = cls.baker.make(
            "statement.Opportunity", statements=[cls.statement], options=options
        )
        cls.question_statement = cls.baker.make(
            "statement.QuestionStatement", version="initial", is_active=True
        )
        cls.option_statement = cls.baker.make(
            "statement.OptionStatement",
            statement=cls.question_statement.statement,
            version="initial",
            is_active=True,
        )
        cls.statement_formula = cls.baker.make(
            "statement.StatementFormula", statement=cls.statement
        )

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
        cls.statement_formula_list_url = cls.reverse(
            "statement-formula-list", kwargs={"version": "v1"}
        )
        cls.statement_formula_detail_url = cls.reverse(
            "statement-formula-detail",
            kwargs={"version": "v1", "pk": cls.statement_formula.pk},
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
            kwargs={"version": "v1", "pk": cls.question_statement.pk},
        )

        cls.option_statement_list_url = cls.reverse(
            "option-statement-list", kwargs={"version": "v1"}
        )
        cls.option_statement_detail_url = cls.reverse(
            "option-statement-detail",
            kwargs={"version": "v1", "pk": cls.option_statement.pk},
        )

    def test_statement_topic_list(self):
        response = self.client.get(self.statement_topic_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_topic_detail(self):
        response = self.client.get(self.statement_topic_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_tag_group_list(self):
        response = self.client.get(self.statement_tag_group_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_tag_group_detail(self):
        response = self.client.get(self.statement_tag_group_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_tag_list(self):
        response = self.client.get(self.statement_tag_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_tag_detail(self):
        response = self.client.get(self.statement_tag_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_list(self):
        response = self.client.get(self.statement_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_detail(self):
        response = self.client.get(self.statement_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_formula_list(self):
        response = self.client.get(self.statement_formula_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_statement_formula_detail(self):
        response = self.client.get(self.statement_formula_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_mitigation_list(self):
        response = self.client.get(self.mitigation_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_mitigation_detail(self):
        response = self.client.get(self.mitigation_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_opportunity_list(self):
        response = self.client.get(self.opportunity_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_opportunity_detail(self):
        response = self.client.get(self.opportunity_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_question_statement_list(self):
        response = self.client.get(self.question_statement_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_question_statement_detail(self):
        response = self.client.get(self.question_statement_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_option_statement_list(self):
        response = self.client.get(self.option_statement_list_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_option_statement_detail(self):
        response = self.client.get(self.option_statement_detail_url)
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_upload_weightage(self):
        user = self.baker.make(
            settings.AUTH_USER_MODEL, is_active=True, is_superuser=True
        )
        self.client.force_authenticate(user)
        statement = self.question_statement.statement
        module = self.baker.make("context.Module")
        url = self.reverse(
            "statement-upload-weightage",
            kwargs={"version": "v1", "pk": statement.pk},
        )
        data = {
            "question_group": None,
            "module": module.pk,
            "questions": [
                {
                    "question": self.question_statement.question.pk,
                    "weightage": self.baker.random_gen.gen_float(),
                }
            ],
            "options": [
                {
                    "option": self.option_statement.option.pk,
                    "weightage": self.baker.random_gen.gen_float(),
                }
            ],
            "formula": self.baker.random_gen.gen_text(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(
            response.status_code, self.status_code.HTTP_201_CREATED, response.json()
        )
        self.assertTrue(
            QuestionStatement.objects.filter(
                question=self.question_statement.question.pk,
                statement=statement.pk,
                version="draft",
            ).exists()
        )
        self.assertTrue(
            OptionStatement.objects.filter(
                option=self.option_statement.option.pk,
                statement=statement.pk,
                version="draft",
            ).exists()
        )
        self.assertTrue(
            StatementFormula.objects.filter(
                module=module.pk,
                statement=statement.pk,
                version="draft",
            ).exists()
        )

    def test_activate_version(self):
        user = self.baker.make(
            settings.AUTH_USER_MODEL, is_active=True, is_superuser=True
        )
        self.client.force_authenticate(user)
        statement = self.question_statement.statement
        url = self.reverse(
            "statement-activate-version",
            kwargs={"version": "v1", "pk": statement.pk},
        )
        version = self.baker.random_gen.gen_string(max_length=255)
        self.baker.make(
            "statement.QuestionStatement", statement=statement, version=version
        )
        self.baker.make(
            "statement.OptionStatement",
            statement=statement,
            version=version,
        )
        self.baker.make(
            "statement.StatementFormula", statement=statement, version=version
        )
        response = self.client.post(
            url,
            data={
                "version": version,
            },
            format="json",
        )
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )

    def test_activate_draft_version(self):
        user = self.baker.make(
            settings.AUTH_USER_MODEL, is_active=True, is_superuser=True
        )
        self.client.force_authenticate(user)
        statement = self.question_statement.statement
        url = self.reverse(
            "statement-activate-draft-version",
            kwargs={"version": "v1", "pk": statement.pk},
        )
        self.baker.make(
            "statement.QuestionStatement", statement=statement, version="draft"
        )
        self.baker.make(
            "statement.OptionStatement",
            statement=statement,
            version="draft",
        )
        self.baker.make(
            "statement.StatementFormula", statement=statement, version="draft"
        )
        response = self.client.post(url, format="json", data={})
        self.assertEqual(
            response.status_code, self.status_code.HTTP_200_OK, response.json()
        )
