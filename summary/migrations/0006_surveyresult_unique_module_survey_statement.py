# Generated by Django 3.2.12 on 2022-02-24 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0005_add_verbose_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='surveyresult',
            constraint=models.UniqueConstraint(fields=('statement', 'survey', 'module'), name='unique_module_survey_statement'),
        ),
    ]