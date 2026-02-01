# Multi-stage build for smaller final image
FROM python:3.13-slim AS builder

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up uv environment
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13

WORKDIR /app

# Copy all project files needed for installation
COPY pyproject.toml uv.lock* README.md ./
COPY src/ ./src/

# Install dependencies (mysql, redis, pdf - excluding snmp which has compatibility issues)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --extra mysql --extra redis --extra pdf 2>/dev/null || \
    uv sync --extra mysql --extra redis --extra pdf


# Production image
FROM python:3.13-slim AS production

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --from=builder /app/src ./src

# Copy templates
COPY templates ./templates

# Create output directory
RUN mkdir -p /app/output

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run as non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import network_discovery; print('OK')" || exit 1

ENTRYPOINT ["network-discovery"]
CMD ["--help"]


# Development image with full tooling
FROM python:3.13-slim AS development

# Install uv and system dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    git \
    curl \
    gcc \
    python3-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy all project files
COPY pyproject.toml uv.lock* README.md ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY templates/ ./templates/

# Install all dependencies including dev (excluding snmp which has compatibility issues)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --extra dev --extra mysql --extra redis --extra pdf 2>/dev/null || \
    uv sync --extra dev --extra mysql --extra redis --extra pdf

ENV PATH="/app/.venv/bin:$PATH"

# Default to bash for development
CMD ["/bin/bash"]
