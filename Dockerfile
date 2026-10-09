# SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT
# SPDX-FileContributor: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com> (automated contribution)

# Python 3.14 slim-bookworm, pinned by digest.
FROM python@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83 AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
# Source-only python-nmap is built explicitly from the same verified artifact
# as uv.lock. Build backends are locked; all other installs reject source builds.
ADD --checksum=sha256:f75af6b91dd8e3b0c31f869db32163f62ada686945e5b7c25f84bc0f7fad3b64 https://files.pythonhosted.org/packages/f7/1b/8e6b3d1461331e4e8600faf099e7c62ba3c1603987dafdd558681fb8ba37/python-nmap-0.7.1.tar.gz /tmp/python-nmap.tar.gz
RUN uv sync --locked --group build --no-build --no-install-project \
    && uv build --wheel --no-build-isolation --out-dir /wheels \
    && uv build --wheel --no-build-isolation --out-dir /wheels /tmp/python-nmap.tar.gz \
    && uv sync --locked --extra nmap --no-build --no-install-project --no-install-package python-nmap \
    && uv pip install --python .venv/bin/python --no-build --no-deps /wheels/*.whl

FROM python@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83 AS runtime
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
