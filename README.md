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

By default each host is checked for SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) and HTTPS (TCP 443). TCP ports are tested with a full connect. SNMP is tested with an SNMPv3 engine-discovery request, which any SNMPv3 agent must answer without credentials; agents that only speak v1/v2c will not be detected by this probe. With the asyncio backend a host counts as alive when any probe gets an answer, including a refused connection, so a host that drops every probe is reported down. With `--backend nmap`, nmap decides which hosts are alive (ICMP as root, TCP 80/443 otherwise).

Services can be changed with a TOML file:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` is one of `tcp`, `ssh`, `mysql`, `http`, `https` or `snmp` and defaults to the service name when that is a probe, else `tcp`. Only `snmp` uses UDP. Service names are lowercase letters, digits, `-` and `_`.

Results keep the original `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` and `errors` fields and add a `services` list with each probe's `name`, `port`, `protocol` and `state` (`open`, `closed` or `filtered`). CSV output gains a trailing `services` column listing the open ones. The `ssh`, `snmp` and `mysql` booleans follow the services with exactly those names.

Exit codes: `0` success, `1` the nmap backend is unavailable or the report could not be written, `2` invalid target, option or config file.

## Development

```bash
.venv/bin/python -m pytest
.venv/bin/mypy
```

Integration tests run against a docker compose lab (OpenSSH, MariaDB, net-snmp) on the private subnet 172.30.57.0/24, from a tester container on the same network: `make test-integration`. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [release scripts](scripts/README.md) for other workflows.

## Security and license status

See [SECURITY.md](SECURITY.md). Package metadata declares MIT, but this checkout has no `LICENSE` file. Confirm the intended license grant before redistribution.
