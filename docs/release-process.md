<!--
SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Release process

The current process is documented in [Versioning and releases](releasing.md):
release-please opens a release PR from Conventional Commits, merging it creates
the `vMAJOR.MINOR.PATCH` tag and a draft GitHub release with tested, attested
artifacts, and a maintainer publishes the draft, which can trigger PyPI trusted
publishing of those same files.

The legacy GitFlow/development-version workflow and `scripts/release.py prepare`
are retired.
