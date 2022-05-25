#!/bin/sh
poetry export --dev -E asgi --without-hashes | poetry run safety check --stdin
