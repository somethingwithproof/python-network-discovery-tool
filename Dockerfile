# SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT
# SPDX-FileContributor: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com> (automated contribution)

# Python 3.14 slim-bookworm, pinned by digest.
FROM python@sha256:f17ec845ebdd4f3347431579e1c22eaeec82913f039f2a54b937c7ff870bacdb AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
# Build backends are locked; every install rejects source builds.
RUN uv sync --locked --no-dev --group build --no-build --no-install-project \
    && uv build --wheel --no-build-isolation --out-dir /wheels \
    && uv sync --locked --no-dev --extra nmap --no-build --no-install-project \
    && uv pip install --python .venv/bin/python --no-build --no-deps /wheels/*.whl

FROM python@sha256:f17ec845ebdd4f3347431579e1c22eaeec82913f039f2a54b937c7ff870bacdb AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends nmap \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 netprobe \
    && mkdir -p /app/output && chown netprobe:netprobe /app/output
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER netprobe
ENTRYPOINT ["netprobe"]
CMD ["--help"]
