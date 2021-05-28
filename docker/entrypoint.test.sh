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
    poetry run ./manage.py test -v 3
fi
