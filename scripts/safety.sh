#!/bin/sh
poetry export --with=dev -E asgi --without-hashes | poetry run safety check --stdin
