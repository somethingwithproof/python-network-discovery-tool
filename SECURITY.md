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

## Authorized use

netprobe sends TCP connections, HTTP and TLS requests, SNMP requests and, with
`--backend nmap`, nmap host discovery to every address in its target. Run it only
against networks you administer or have written permission to test, and keep
that permission's scope in a profile so repeated scans stay inside it:

- Put the agreed range in a named profile and its exclusions in `exclusions`;
  `--exclude` on the command line can only add to them.
- Run `netprobe preflight` first. It checks the plan locally and sends nothing.
- Keep `--max-hosts`, `--concurrency` and `--deadline` as small as the job allows,
  and agree the scan window with whoever operates the network. Probes are
  ordinary connections, but intrusion detection may still report them.
- Do not use SNMP credentials outside the systems they were issued for.

Probe deadlines, host/service caps, the scan deadline and preflight checks bound
the work netprobe does; they do not grant authorization.

## Scanner boundaries

HTTPS certificate and hostname verification must succeed before collecting HTTP
headers or certificate details. Use `--tls-ca-file` for a private CA.

SNMP secrets come only from environment variables or secret files (`--snmp-*-file`),
never from command-line values, so they do not appear in the local process list. Inventory reports and history
store observations and non-secret settings. Explicit credential exports write
owner-only scripts but still expose arguments to Kadupul during execution.
Protect history databases, reports, and exported scripts as network inventory.

See [the release process](docs/releasing.md) for checksums, provenance, and
trusted-publisher requirements. CI runs regression tests, Bandit, typing, and
SonarCloud analysis. [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
tracks repository and workflow security practices.
