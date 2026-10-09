<!--
SPDX-FileCopyrightText: 2024-2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Security policy

## Supported versions

Security fixes target the current `main` branch and the latest published release
when the affected code is present there. Older releases are not maintained.
The current packaged implementation is 3.0.0; the last published legacy release is
v0.3.0. Use the checkout for current inventory features and security fixes.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/somethingwithproof/python-network-discovery-tool/security/advisories/new)
to contact the maintainer privately. Include the affected revision, a reproducible
example, impact, and any proposed fix. Do not put credentials or exploit details
in public issues. Ordinary bugs belong in the issue tracker.

We aim to acknowledge reports within seven days. This is a best-effort maintainer
response target, not a service-level guarantee. Confirmed issues are coordinated
privately, fixed on main, and documented in the changelog or a security advisory.

## Scanner boundaries

Scan only networks you administer or have permission to test. Probe deadlines,
host/service caps, and preflight checks bound work; they do not grant authorization.
HTTPS certificate and hostname verification must succeed before collecting HTTP
headers or certificate details. Use `--tls-ca-file` for a private CA.

SNMP secrets come from runtime options or environment variables; prefer the latter
so they do not appear in the local process list. Inventory reports and history
store observations and non-secret settings. Explicit credential exports write
owner-only scripts but still expose arguments to Kadupul during execution.
Protect history databases, reports, and exported scripts as network inventory.

See [the release process](docs/releasing.md) for checksums, provenance, and
trusted-publisher requirements. CI runs regression tests, Bandit, typing, and
SonarCloud analysis. [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
tracks repository and workflow security practices.
