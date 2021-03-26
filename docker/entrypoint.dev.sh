#!/bin/sh
if [ "$CELERY_WORKER" = "true" ]
then
    celery -A neatplus worker -l info
else
    poetry install --no-dev
    python3 manage.py collectstatic --no-input
    python3 manage.py migrate --no-input
    python3 manage.py runserver 0.0.0.0:8000
fi
