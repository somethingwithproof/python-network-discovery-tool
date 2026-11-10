<!--
SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Release tooling

[`release.py`](release.py) validates releases for the `src/netprobe` package. It
never commits, tags, pushes, creates releases, or uploads packages; release-please
prepares versions and `CHANGES.md`.

```bash
mise exec python@3.14 -- python scripts/release.py check
mise exec python@3.14 -- python scripts/release.py check --tag v3.1.0
```

`check` confirms that `pyproject.toml`, netprobe's `uv.lock` entry, the tag and a
dated `CHANGES.md` section agree. Checksum and distribution validation options are
shown by `check --help`.

See [Versioning and releases](../docs/releasing.md) for the compatibility and
deprecation policy, release-please, the tag build, draft promotion, provenance,
and optional PyPI trusted publishing.
