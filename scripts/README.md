<!--
SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Release tooling

[`release.py`](release.py) prepares and validates releases for the current
`src/netprobe` package. It never commits, tags, pushes, creates releases, or uploads
packages.

```bash
mise exec python@3.14 -- python scripts/release.py prepare minor --dry-run
mise exec python@3.14 -- python scripts/release.py prepare minor
mise exec python@3.14 -- python scripts/release.py check
mise exec python@3.14 -- python scripts/release.py check --tag v3.1.0
```

Preparation updates `pyproject.toml`, the matching `uv.lock` entry, and `CHANGES.md`.
Use `major`, `minor`, `patch`, or an explicit stable/prerelease version. Checksum
and distribution validation options are shown by `check --help`.

See [Versioning and releases](../docs/releasing.md) for the compatibility policy,
reviewed preparation PR, tag build, draft promotion, provenance, and optional PyPI
trusted publishing. This replaces the legacy GitFlow/release helpers.
