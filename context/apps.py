from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContextConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "context"
    verbose_name = _("context")
