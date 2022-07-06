# Generated by Django 3.2.13 on 2022-06-23 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('context', '0003_increase_code_max_length'),
        ('survey', '0016_remove_question_module'),
        ('statement', '0010_add_question_group_to_weightage'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatementFormula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('formula', models.TextField(verbose_name='formula')),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formulas', to='context.module', verbose_name='module')),
                ('question_group', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formulas', to='survey.questiongroup', verbose_name='question group')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formulas', to='statement.statement', verbose_name='statement')),
                ('updated_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
        ),
        migrations.AddConstraint(
            model_name='statementformula',
            constraint=models.UniqueConstraint(condition=models.Q(('question_group__isnull', False)), fields=('question_group', 'statement'), name='one_formula_question_group_statement'),
        ),
        migrations.AddConstraint(
            model_name='statementformula',
            constraint=models.UniqueConstraint(condition=models.Q(('question_group__isnull', True)), fields=('statement',), name='one_formula_statement'),
        ),
    ]