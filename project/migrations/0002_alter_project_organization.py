# Generated by Django 3.2.4 on 2021-06-29 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_organization_member_request_status'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='organization.organization'),
        ),
    ]
