# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.13-bookworm AS python-base

RUN  apt-get update \
    && apt-get install --no-install-recommends -y\
    libsqlite3-mod-spatialite \
    binutils \
    libproj-dev \
    gdal-bin

# non interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.0.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    CODE_PATH="/code"

# add poetry home to path
ENV PATH="$POETRY_HOME/bin:$PYSETUP_PATH/.venv/bin/:$PATH"

FROM python-base AS builder-base

RUN apt-get install --no-install-recommends -y \
    software-properties-common \
    curl \
    build-essential

RUN curl -sSL https://install.python-poetry.org | python

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --without=dev --no-root

# testing stage
FROM python-base AS testing

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $CODE_PATH

ENTRYPOINT ["/code/docker/entrypoint.test.sh"]

# development stage
FROM python-base AS development

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $CODE_PATH

ENTRYPOINT ["/code/docker/entrypoint.dev.sh"]

# production stage
FROM builder-base AS production-build

RUN poetry install --no-root --without=dev --extras asgi

# production stage
FROM python-base AS production

COPY --from=production-build $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $CODE_PATH

COPY . $CODE_PATH

ENTRYPOINT [ "/code/docker/entrypoint.prod.sh"]
