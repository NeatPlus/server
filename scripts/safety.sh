#!/bin/sh
poetry export --dev -E asgi --without-hashes | safety check --stdin