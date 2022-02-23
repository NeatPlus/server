# Generated by Django 3.2.12 on 2022-02-10 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0002_add_verbose_name'),
        ('organization', '0008_add_verbose_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0003_project_share_analytics_with_neat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='context',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='context.context', verbose_name='context'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='organization.organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='project',
            name='share_analytics_with_neat',
            field=models.BooleanField(default=False, verbose_name='share analytics with NEAT'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', editable=False, max_length=8, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', through='project.ProjectUser', to=settings.AUTH_USER_MODEL, verbose_name='users'),
        ),
        migrations.AlterField(
            model_name='project',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('public_within_organization', 'Public Wiithin Organization'), ('private', 'Private')], max_length=26, verbose_name='visibility'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='permission',
            field=models.CharField(choices=[('write', 'Write'), ('read_only', 'Read Only')], default='read_only', max_length=9, verbose_name='permission'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]