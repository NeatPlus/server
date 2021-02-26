# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.9.1-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# add poetry home to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# OS dependencies for buling poetry and python dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# development stage
FROM python-base as development

WORKDIR /code

ENTRYPOINT ["/code/docker/entrypoint.dev.sh"]


# production stage
FROM python-base as production

WORKDIR /code

COPY . /code/

# install all dependencies
RUN poetry install --no-dev --extras asgi

ENTRYPOINT [ "/code/docker/entrypoint.prod.sh"]
