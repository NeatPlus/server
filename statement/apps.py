from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "statement"
    verbose_name = _("statement")
