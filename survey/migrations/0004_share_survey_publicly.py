# Generated by Django 3.2.5 on 2021-07-14 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_survey_config'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questiongroup',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='survey',
            name='is_shared_publicly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='survey',
            name='shared_link_identifier',
            field=models.CharField(blank=True, default=None, editable=False, max_length=10, null=True, unique=True),
        ),
    ]
