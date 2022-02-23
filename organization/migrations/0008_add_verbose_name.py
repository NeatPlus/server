# Generated by Django 3.2.12 on 2022-02-10 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0007_organization_mptt_rebuild'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='acronym',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='acronym'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='admins',
            field=models.ManyToManyField(related_name='admin_organizations', to=settings.AUTH_USER_MODEL, verbose_name='admins'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='organization/organization/logos', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_organizations', to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childerns', to='organization.organization', verbose_name='organization parent'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='point_of_contact',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='point of contact'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', editable=False, max_length=8, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_requests', to='organization.organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', editable=False, max_length=8, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='organizationmemberrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_requests', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]