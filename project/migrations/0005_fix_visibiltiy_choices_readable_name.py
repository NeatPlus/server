# Generated by Django 3.2.12 on 2022-02-16 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_add_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('public_within_organization', 'Public Within Organization'), ('private', 'Private')], max_length=26, verbose_name='visibility'),
        ),
    ]
