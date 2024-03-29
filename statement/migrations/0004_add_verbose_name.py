# Generated by Django 3.2.12 on 2022-02-10 14:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0002_add_verbose_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0010_add_verbose_name'),
        ('statement', '0003_statement_is_experimental'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='optionopportunity',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='options',
            field=models.ManyToManyField(related_name='mitigations', through='statement.OptionMitigation', to='survey.Option', verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mitigations', to='statement.statement', verbose_name='statement'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='title',
            field=models.TextField(verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='title_en',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='title_es',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='title_fr',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='mitigation',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='options',
            field=models.ManyToManyField(related_name='opportunities', through='statement.OptionOpportunity', to='survey.Option', verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='statement.statement', verbose_name='statement'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='title',
            field=models.TextField(verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='title_en',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='title_es',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='title_fr',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='optionmitigation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='optionmitigation',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='optionmitigation',
            name='mitigation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statement.mitigation', verbose_name='mitigation'),
        ),
        migrations.AlterField(
            model_name='optionmitigation',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='optionmitigation',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.option', verbose_name='option'),
        ),
        migrations.AlterField(
            model_name='optionmitigation',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='optionopportunity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='optionopportunity',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='optionopportunity',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='optionopportunity',
            name='opportunity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statement.opportunity', verbose_name='opportunity'),
        ),
        migrations.AlterField(
            model_name='optionopportunity',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.option', verbose_name='option'),
        ),
        migrations.AlterField(
            model_name='optionopportunity',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.option', verbose_name='option'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statement.statement', verbose_name='statement'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='optionstatement',
            name='weightage',
            field=models.FloatField(verbose_name='weightage'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.question', verbose_name='question'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statement.statement', verbose_name='statement'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='questionstatement',
            name='weightage',
            field=models.FloatField(verbose_name='weightage'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='hints',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='hints'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='hints_en',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='hints'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='hints_es',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='hints'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='hints_fr',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='hints'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='is_experimental',
            field=models.BooleanField(default=False, verbose_name='experimental'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='options',
            field=models.ManyToManyField(related_name='statements', through='statement.OptionStatement', to='survey.Option', verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='questions',
            field=models.ManyToManyField(related_name='statements', through='statement.QuestionStatement', to='survey.Question', verbose_name='questions'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='tags',
            field=models.ManyToManyField(related_name='statements', to='statement.StatementTag', verbose_name='statement tags'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='title',
            field=models.TextField(verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='title_en',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='title_es',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='title_fr',
            field=models.TextField(null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='statements', to='statement.statementtopic', verbose_name='statement topic'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='statement.statementtaggroup', verbose_name='statement tag group'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='title_es',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='title_fr',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtag',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='title_es',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='title_fr',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtaggroup',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='context',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='statement_topics', to='context.context', verbose_name='context'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='description',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='description_en',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='description_es',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='description_fr',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='icon',
            field=models.FileField(blank=True, default=None, null=True, upload_to='statement/statement_topic/icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png'])], verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='title_es',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='title_fr',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='statementtopic',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
    ]
