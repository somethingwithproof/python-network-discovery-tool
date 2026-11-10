# SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT
# SPDX-FileContributor: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com> (automated contribution)

# Python 3.14 slim (Debian 13), pinned by digest. The tag stays in the reference so
# Dependabot keeps tracking the slim image rather than the full one.
FROM python:3.14-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
# Build backends are locked; every install rejects source builds.
RUN uv sync --locked --no-dev --group build --no-build --no-install-project \
    && uv build --wheel --no-build-isolation --out-dir /wheels \
    && uv sync --locked --no-dev --no-build --no-install-project \
    && uv pip install --python .venv/bin/python --no-build --no-deps /wheels/*.whl

FROM python:3.14-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS runtime
LABEL org.opencontainers.image.title="netprobe" \
      org.opencontainers.image.description="Service inventory for networks you administer" \
      org.opencontainers.image.source="https://github.com/somethingwithproof/python-network-discovery-tool" \
      org.opencontainers.image.licenses="MIT"
# The runtime needs only Python, the locked virtualenv and nmap. pip,
# setuptools and the package lists are removed so nothing in the image can
# install code at run time, and the user has no home directory or shell.
# Take Debian security fixes newer than the pinned base before adding nmap.
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends nmap \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
    && rm -rf /usr/local/lib/python3.*/site-packages/pip* \
        /usr/local/lib/python3.*/site-packages/setuptools* \
        /usr/local/lib/python3.*/ensurepip /usr/local/bin/pip* \
    && useradd --no-create-home --home-dir /nonexistent --shell /usr/sbin/nologin \
        --uid 10001 --user-group netprobe \
    && mkdir -p /app/output && chown netprobe:netprobe /app/output
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
# Numeric so Kubernetes runAsNonRoot can verify it without resolving names.
USER 10001:10001
ENTRYPOINT ["netprobe"]
CMD ["--help"]
