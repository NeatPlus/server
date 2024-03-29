# Generated by Django 3.2.12 on 2022-03-10 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_option_mitigation_opportunity_json_field'),
        ('summary', '0006_surveyresult_unique_module_survey_statement'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='surveyresult',
            name='unique_module_survey_statement',
        ),
        migrations.AddField(
            model_name='surveyresult',
            name='question_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='survey.questiongroup', verbose_name='question group'),
        ),
        migrations.AddConstraint(
            model_name='surveyresult',
            constraint=models.UniqueConstraint(condition=models.Q(('question_group__isnull', True)), fields=('statement', 'survey', 'module'), name='unique_module_survey_statement'),
        ),
        migrations.AddConstraint(
            model_name='surveyresult',
            constraint=models.UniqueConstraint(condition=models.Q(('question_group__isnull', False)), fields=('statement', 'survey', 'module', 'question_group'), name='unique_module_survey_question_group_statement'),
        ),
    ]
