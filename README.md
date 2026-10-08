# netprobe

[![CI configuration](https://img.shields.io/badge/CI-configured-blue)](./.github/workflows/ci.yml)
[![Python requirement](https://img.shields.io/badge/Python_requirement-%3E%3D3.12-blue)](./pyproject.toml)

A Python network-discovery CLI with terminal, JSON, and CSV output. The package in [src/netprobe](src/netprobe) defines the scan orchestration, device representation, output writers, and CLI options.

## Architecture and scope

- A Typer CLI provides `scan` and `version` commands.
- Rich renders terminal output; dedicated functions write JSON and CSV.
- The implementation uses network/service checks and the dependencies declared in [pyproject.toml](pyproject.toml).

## Install and inspect

Python 3.12 or newer is required. From this checkout:

```bash
uv venv
uv pip install -e ".[dev]"
.venv/bin/netprobe --help
.venv/bin/netprobe scan --help
```

Inspect the options and required platform tools before using the scanner on networks you administer. This README does not claim verified compatibility with every target service or environment.

## Usage

Requirements: permission to scan the target. Scan only networks you administer. No root and no nmap are needed by default.

```bash
netprobe scan 192.168.1.0/24              # table of alive hosts
netprobe scan 192.168.1.1 -o results.json # JSON report
netprobe scan 10.0.0.0/24 -o report.csv   # CSV report
netprobe scan 10.0.0.0/24 -q -o out.json  # no table, file only
```

| Option | Meaning |
| --- | --- |
| `NETWORK` | CIDR range, IP address, or hostname. Ranges over 65536 addresses are rejected. |
| `-o, --output PATH` | Write a report. The format follows the extension (`.json`, `.csv`); other extensions fall back to JSON. |
| `-f, --format json\|csv\|auto` | Force the report format. Has no effect without `--output`. |
| `-v, --verbose` | Debug logging. |
| `-q, --quiet` | Suppress the results table. |
| `--backend asyncio\|nmap` | Host discovery. `asyncio` (default) probes the service ports directly; `nmap` runs an nmap ping sweep first and needs `pip install 'netprobe[nmap]'` plus the `nmap` binary. |
| `--timeout SECONDS` | Wait per probe (default 1.0). |
| `--concurrency N` | Probes in flight at once (default 256). |
| `--config PATH` | TOML file whose `[services]` table adds or replaces services. |
| `--services NAMES` | Comma list of service names to check, in that order (default: all). |
| `--ports SPEC` | Comma list of `NAME=PORT` (move a service) or `PORT` (add a plain TCP check named `tcp-PORT`). |
| `--snmp-community` | SNMPv2c community for the system MIB query. Env: `NETPROBE_SNMP_COMMUNITY`. |
| `--snmp-user` | SNMPv3 user. Env: `NETPROBE_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key` | `MD5`, `SHA` (default), `SHA224`, `SHA256`, `SHA384`, `SHA512` and the passphrase. Env: `NETPROBE_SNMP_AUTH_PROTOCOL`, `NETPROBE_SNMP_AUTH_KEY`. |
| `--snmp-priv-protocol`, `--snmp-priv-key` | `DES`, `AES` (default), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` and the passphrase. Env: `NETPROBE_SNMP_PRIV_PROTOCOL`, `NETPROBE_SNMP_PRIV_KEY`. |
| `--save-snapshot PATH` | Also write a versioned snapshot for `netprobe diff`. |
| `--tls-ca-file PATH` | Verify HTTPS certificates against this PEM bundle instead of the system store. Env: `NETPROBE_TLS_CA_FILE`. |

By default each host is checked for SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) and HTTPS (TCP 443). TCP ports are tested with a full connect. SNMP is tested with an SNMPv3 engine-discovery request, which any SNMPv3 agent must answer without credentials; agents that only speak v1/v2c will not be detected by this probe. With the asyncio backend a host counts as alive when any probe gets an answer, including a refused connection, so a host that drops every probe is reported down. With `--backend nmap`, nmap decides which hosts are alive (ICMP as root, TCP 80/443 otherwise).

### Fingerprints

Each open service is fingerprinted from what it sends before any login. Nothing authenticates except the SNMP query, and only when you supply credentials.

| Probe | Reads | `version` | `details` keys |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 identification line | software, e.g. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | MySQL/MariaDB initial handshake | server version | `server_version`, `flavor`, `auth_plugin`, or `error_code`/`error` |
| `http` | `HEAD /` response | `Server` header | `status`, `server` |
| `https` | TLS handshake, certificate, `HEAD /` | `Server` header | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 discovery; with credentials, GET of sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; with credentials `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, or `snmp_error` |

HTTPS certificates are verified first, against the system store or `--tls-ca-file`. If verification fails, the failure is recorded in `cert_verified: false` and `cert_verify_error`, and the certificate is then read over an unverified connection so it can still be inventoried; such results carry `cert_read_unverified: true`. Nothing is sent over that connection except the `HEAD` request.

SNMP credentials are read from options or environment variables. Prefer the environment variables: command-line values are visible to other local users in the process list. Credentials are never logged or written to any output. A community selects SNMPv2c; a user selects SNMPv3, with authentication when an auth key is given and privacy when both keys are given (`snmp_security_level` records which). netprobe refuses, with exit code 2, to combine a community with a v3 user, to use a privacy key without an auth key, or to use keys without a user, and it never retries a failed v3 query with v2c or a lower security level. Passing a secret as an option logs a warning naming the matching environment variable. Agents that only speak v1/v2c ignore the credential-free v3 discovery, so they show as open only when a community is supplied.

Banner text is reduced to printable characters and capped at 256 characters before it is stored or shown. Reads are bounded too: 4 KiB per line, 4 KiB for a MySQL greeting, 16 KiB of HTTP headers.

### Limits

One run accepts at most 65,536 addresses, 64 services, and 524,288 probes (hosts times services); larger requests exit with code 2 before anything is sent. `--concurrency` is capped at 4096 sockets. Every probe, including the nmap-backend and SNMP paths, has a hard deadline of four times `--timeout`; a probe that hits it is reported as `filtered` with "probe timed out" in `errors`.

### Configuring services

Services can be changed with a TOML file:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` is one of `tcp`, `ssh`, `mysql`, `http`, `https` or `snmp` and defaults to the service name when that is a probe, else `tcp`. Only `snmp` uses UDP. Service names are lowercase letters, digits, `-` and `_`.

Results keep the original `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` and `errors` fields and add a `services` list with each probe's `name`, `port`, `protocol`, `state` (`open`, `closed` or `filtered`), `version` and `details`. CSV output gains trailing `services` and `versions` columns for the open ones. The `ssh`, `snmp` and `mysql` booleans follow the services with exactly those names.

Exit codes: `0` success, `1` the nmap backend is unavailable or the report could not be written, `2` invalid target, option or config file.

## Inventory diff

```bash
netprobe scan 10.0.0.0/24 -q --save-snapshot monday.json
netprobe scan 10.0.0.0/24 -q --save-snapshot tuesday.json
netprobe diff monday.json tuesday.json             # table
netprobe diff monday.json tuesday.json -f json     # JSON on stdout
```

A snapshot is JSON with `format: "netprobe-snapshot"`, `version: 1`, the netprobe version, the UTC creation time, the target, the services that were probed, and the alive hosts in the same shape as the `-o` report. Down hosts are left out. `diff` also accepts plain `scan -o` JSON reports, including ones from before the `services` field existed.

`diff` reports new and vanished hosts, ports that opened or closed on hosts present in both, and services whose `version` changed. Ports that were probed in only one of the two scans are not compared, and a warning says so; a warning also appears when the targets differ. `-o PATH` writes the JSON form to a file as well.

`diff` exit codes: `0` no changes, `3` changes found, `2` a file is missing, unreadable or not a supported snapshot, `1` the `-o` file could not be written.

## Development

```bash
.venv/bin/python -m pytest
.venv/bin/mypy
```

Integration tests run against a docker compose lab (OpenSSH, MariaDB, nginx with a self-signed certificate, net-snmp) on the private subnet 172.30.57.0/24, from a tester container on the same network: `make test-integration`. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [release scripts](scripts/README.md) for other workflows.

## Security and license status

See [SECURITY.md](SECURITY.md). Package metadata declares MIT, but this checkout has no `LICENSE` file. Confirm the intended license grant before redistribution.
