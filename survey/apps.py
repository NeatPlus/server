from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SurveyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "survey"
    verbose_name = _("survey")
