FROM python:3.14-slim-bookworm@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83 AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
# Locked artifact hashes cover runtime dependencies and the source-only Nmap
# wrapper. All package builds stay in this credential-free builder stage.
RUN uv sync --locked --extra nmap --no-editable

FROM python:3.14-slim-bookworm@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83 AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends nmap \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/output
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
ENTRYPOINT ["netprobe"]
CMD ["--help"]
