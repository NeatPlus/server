#!/bin/sh
if [ "$CELERY_WORKER" = "true" ]
then
    if [ -z "$CELERY_QUEUES" ]
    then
        poetry run celery -A neatplus worker -l info
    else
        poetry run celery -A neatplus worker -l info -Q "$CELERY_QUEUES"
    fi
else
    poetry run ./manage.py migrate --no-input
    poetry run gunicorn neatplus.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
fi
