# Generated by Django 3.2.4 on 2021-06-22 06:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]