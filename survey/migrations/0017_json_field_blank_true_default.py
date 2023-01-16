# Generated by Django 3.2.16 on 2023-01-16 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0016_remove_question_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='mitigation',
            field=models.JSONField(blank=True, default=list, verbose_name='mitigations'),
        ),
        migrations.AlterField(
            model_name='option',
            name='opportunity',
            field=models.JSONField(blank=True, default=list, verbose_name='opportunities'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='config',
            field=models.JSONField(blank=True, default=dict, verbose_name='config'),
        ),
    ]
