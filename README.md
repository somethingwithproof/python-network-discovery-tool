# netprobe

[![CI configuration](https://img.shields.io/badge/CI-configured-blue)](./.github/workflows/ci.yml)
[![Python requirement](https://img.shields.io/badge/Python_requirement-%3E%3D3.12-blue)](./pyproject.toml)

A Python network-discovery CLI with terminal, JSON, and CSV output. The checked-in [netprobe.py](netprobe.py) defines the scan orchestration, device representation, output writers, and CLI options.

## Architecture and scope

- A Typer CLI provides `scan` and `version` commands.
- Rich renders terminal output; dedicated functions write JSON and CSV.
- The implementation uses network/service checks and the dependencies declared in [pyproject.toml](pyproject.toml).

This repository also retains development tooling and historical modules. Earlier claims that the entire repository consists of one file, or that the rewrite has demonstrated performance improvements, do not describe the evidence available here.

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

Requirements: the `nmap` binary on `PATH`, and permission to scan the target. Scan only networks you administer.

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

Each alive host is checked for SSH (TCP 22), MySQL (TCP 3306) and SNMP (UDP 161). The SNMP check is a UDP scan, which nmap only runs as root; without root it is skipped and the host's `errors` field says so. A port counts as open only when nmap reports state `open`; `open|filtered` UDP results are not counted.

Exit codes: `0` success, `1` nmap missing or the report could not be written, `2` invalid target.

## Development

```bash
.venv/bin/python -m pytest
```

The test configuration and dependencies are declared in [pyproject.toml](pyproject.toml). See [E2E-TESTING.md](E2E-TESTING.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [release scripts](scripts/README.md) for additional workflows.

## Security and license status

See [SECURITY.md](SECURITY.md). Package metadata declares MIT, but this checkout has no `LICENSE` file. Confirm the intended license grant before redistribution.
