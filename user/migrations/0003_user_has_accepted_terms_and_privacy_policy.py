# Generated by Django 3.2.5 on 2021-07-26 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_add_user_organization_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_accepted_terms_and_privacy_policy',
            field=models.BooleanField(default=True),
        ),
    ]