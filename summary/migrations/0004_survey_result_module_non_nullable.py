# Generated by Django 3.2.8 on 2021-11-08 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0001_initial'),
        ('summary', '0003_populate_module_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresult',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='context.module'),
        ),
    ]
