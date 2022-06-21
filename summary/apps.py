from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SummaryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summary"
    verbose_name = _("summary")

    def ready(self):
        from summary import signals
