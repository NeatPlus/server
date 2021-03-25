import functools
import os

from celery import Celery
from django.conf import settings
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neatplus.settings")

app = Celery("neatplus")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


def perform_task(function, *args, **kwargs):
    if settings.ENABLE_CELERY:
        function.delay(*args, **kwargs)
    else:
        function(*args, **kwargs)


def no_simultaneous_execution(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if settings.ENABLE_CELERY:
            cache_key = f"running-task-{self.name}-{self.request.id}-{args}-{kwargs}"
            if not cache.get(cache_key):
                cache.set(cache_key, "lock", timeout=None)
                try:
                    f(self, *args, **kwargs)
                except Exception as e:
                    cache.delete(cache_key)
                    raise e
                finally:
                    cache.delete(cache_key)
        else:
            f(self, *args, **kwargs)

    return wrapper
