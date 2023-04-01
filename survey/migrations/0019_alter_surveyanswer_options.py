# Generated by Django 3.2.18 on 2023-03-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0018_remove_option_json_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyanswer',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='survey_answers', to='survey.Option', verbose_name='options'),
        ),
    ]