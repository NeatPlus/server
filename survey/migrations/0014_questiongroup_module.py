# Generated by Django 3.2.12 on 2022-03-23 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0003_increase_code_max_length'),
        ('survey', '0013_option_mitigation_opportunity_json_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiongroup',
            name='module',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='question_groups', to='context.module', verbose_name='module'),
        ),
    ]
