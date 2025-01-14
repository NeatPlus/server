# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

#  Creating a python base with shared dependencies
FROM python:3.13-bookworm AS python-base

# non interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# Install essential tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    libsqlite3-mod-spatialite \
    binutils \
    libproj-dev \
    gdal-bin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED=1 \
    CODE_PATH="/code" \
    VENV_PATH="/code/.venv" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

FROM python-base AS builder

# Install curl and uv
RUN apt-get install -y curl && \
    curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/download/0.5.15/uv-installer.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR $CODE_PATH

COPY pyproject.toml uv.lock ./

# Install core dependencies
RUN uv sync --frozen --no-dev

# Development stage
FROM python-base AS development

WORKDIR $CODE_PATH

# Copy dependencies and source code
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder $VENV_PATH $VENV_PATH
COPY . $CODE_PATH

# Use development entrypoint
ENTRYPOINT ["/code/docker/entrypoint.dev.sh"]

# Testing stage
FROM python-base AS testing

WORKDIR $CODE_PATH

# Copy dependencies and source code
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder $VENV_PATH $VENV_PATH
COPY . $CODE_PATH

# Use testing entrypoint
ENTRYPOINT ["/code/docker/entrypoint.test.sh"]

# Production build stage
FROM builder AS production-build

WORKDIR $CODE_PATH

RUN uv sync --frozen --no-dev --extra production



# Production stage
FROM python-base AS production

WORKDIR $CODE_PATH

COPY --from=production-build $VENV_PATH $VENV_PATH
COPY . $CODE_PATH

ENV PATH="$VENV_PATH/bin:$PATH"

ENTRYPOINT [ "/code/docker/entrypoint.prod.sh"]
