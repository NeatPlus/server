# Generated by Django 3.2.4 on 2021-06-24 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0002_add_skip_logic'),
        ('statement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('score', models.FloatField()),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statement.statement')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='survey.survey')),
                ('updated_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
