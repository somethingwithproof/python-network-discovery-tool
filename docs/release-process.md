# Release process

The current process is documented in [Versioning and releases](releasing.md).
It uses a reviewed version-preparation PR, a validated `vMAJOR.MINOR.PATCH` tag
build, a draft GitHub release, maintainer promotion, and optional PyPI trusted
publishing of the existing artifacts.

The legacy GitFlow/development-version workflow is retired. Use
`scripts/release.py prepare --help` and the current release guide rather than
older commands for the removed `network_discovery` package.
