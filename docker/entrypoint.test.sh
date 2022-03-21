#!/bin/sh
poetry install --no-root
poetry run ./manage.py collectstatic --no-input
poetry run ./manage.py test -v 3
