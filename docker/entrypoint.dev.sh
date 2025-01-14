#!/bin/sh
# uv sync will also take care of the "dev" dependency
# Optional, we can also use "uv sync --group dev"
uv sync --frozen --no-install-project
if [ "$CELERY_WORKER" = "true" ]
then
    if [ -z "$CELERY_QUEUES" ]
    then
        uv run celery -A neatplus worker -l info
    else
        uv run celery -A neatplus worker -l info -Q "$CELERY_QUEUES"
    fi
else
    uv run manage.py collectstatic --no-input
    uv run manage.py makemigrations
    uv run manage.py migrate --no-input
    uv run manage.py import_default_email_template
    uv run manage.py runserver_plus 0.0.0.0:8000 || uv run manage.py runserver 0.0.0.0:8000
fi
