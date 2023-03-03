# Generated by Django 3.2.18 on 2023-03-03 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement', '0015_add_options_field_mitigation_opportunity'),
    ]

    operations = [
        migrations.AddField(
            model_name='mitigation',
            name='implementor',
            field=models.CharField(blank=True, choices=[('local', 'Local'), ('regional', 'Regional'), ('hq', 'HQ'), ('all', 'All')], default=None, max_length=8, null=True, verbose_name='implementor'),
        ),
        migrations.AddField(
            model_name='mitigation',
            name='priority',
            field=models.CharField(blank=True, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default=None, max_length=6, null=True, verbose_name='priority'),
        ),
        migrations.AddField(
            model_name='mitigation',
            name='rank',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='rank'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='implementor',
            field=models.CharField(blank=True, choices=[('local', 'Local'), ('regional', 'Regional'), ('hq', 'HQ'), ('all', 'All')], default=None, max_length=8, null=True, verbose_name='implementor'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='priority',
            field=models.CharField(blank=True, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default=None, max_length=6, null=True, verbose_name='priority'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='rank',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='rank'),
        ),
    ]