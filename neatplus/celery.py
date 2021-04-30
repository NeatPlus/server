import functools
import os

from celery import Celery
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neatplus.settings")

app = Celery("neatplus")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


def no_simultaneous_execution(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
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

    return wrapper
