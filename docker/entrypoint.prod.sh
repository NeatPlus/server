#!/bin/sh
#!/bin/sh
if [ "$CELERY_WORKER" = "true" ]
then
    if [ -z "$CELERY_QUEUES" ]
    then
        celery -A neatplus worker -l info
    else
        celery -A neatplus worker -l info -Q "$CELERY_QUEUES"
    fi
else
    python3 manage.py collectstatic --no-input
    python3 manage.py migrate --no-input
    gunicorn neatplus.asgi:application -k uvicorn.workers.UvicornWorker
fi
