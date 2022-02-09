#!/bin/sh
poetry install
if [ "$CELERY_WORKER" = "true" ]
then
    if [ -z "$CELERY_QUEUES" ]
    then
        poetry run celery -A neatplus worker -l info
    else
        poetry run celery -A neatplus worker -l info -Q "$CELERY_QUEUES"
    fi
else
    poetry run ./manage.py collectstatic --no-input
    poetry run ./manage.py migrate --no-input
    poetry run ./manage.py import_default_email_template
    poetry run ./manage.py runserver_plus 0.0.0.0:8000 || poetry run ./manage.py runserver 0.0.0.0:8000
fi
