#!/bin/sh
# TODO: remove safety ignore ids after pyproject.toml is updated to use 2.0.0 of django-oauth-toolkit
poetry export --dev -E asgi --without-hashes | poetry run safety check --stdin --ignore 47012 --ignore 47853
