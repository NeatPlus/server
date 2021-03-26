#!/bin/sh
if [ "$CELERY_WORKER" = "true" ]
then
    celery -A neatplus worker -l info
else
    python3 manage.py collectstatic --no-input
    python3 manage.py migrate --no-input
    gunicorn neatplus.asgi:application -k uvicorn.workers.UvicornWorker
fi
