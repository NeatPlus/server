# Generated by Django 3.2.8 on 2021-11-01 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement', '0002_statement_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='is_experimental',
            field=models.BooleanField(default=False),
        ),
    ]
