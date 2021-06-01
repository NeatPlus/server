#!/bin/sh
poetry install
poetry run ./manage.py collectstatic --no-input
poetry run ./manage.py test -v 3
