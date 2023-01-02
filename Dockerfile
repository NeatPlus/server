# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM ubuntu:20.04 as base

# non interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# install requiremnts for python3.10 install
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    software-properties-common \
    git

# Add deadsnakes ppa
RUN add-apt-repository ppa:deadsnakes/ppa -y

# install python3.10
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python-is-python3

FROM base as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# add poetry home to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# OS dependencies for installing poetry and project dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libsqlite3-mod-spatialite

# Install pip
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python3.10

# install virtualenv
RUN pip3.10 install -U virtualenv

# Add gis ppa
RUN add-apt-repository ppa:ubuntugis/ppa -y

# install gdal
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    gdal-bin

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3.10

# testing stage
FROM python-base as testing

WORKDIR /code

ENTRYPOINT ["/code/docker/entrypoint.test.sh"]

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
