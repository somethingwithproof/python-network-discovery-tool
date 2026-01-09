# Network Device Discovery Tool

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

A command-line tool for scanning network devices to check SSH, SNMP, MySQL, and ICMP (ping) connectivity. Import device lists from Excel spreadsheets and export scan results.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output](#output)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multi-protocol scanning** — Check ping, SSH, SNMP, and MySQL connectivity
- **Excel integration** — Import device lists and export scan results to `.xlsx` files
- **Concurrent execution** — Parallel scanning with configurable worker threads
- **Persistent storage** — SQLite database for device records and scan history
- **Security-focused** — Strict SSH host key checking enabled by default

## Requirements

- Python 3.14 or later
- System libraries:
  - `net-snmp` for SNMP scanning
  - `libmysqlclient` for MySQL scanning

## Installation

### Install System Dependencies

**macOS:**

```bash
brew install net-snmp mysql-client
```

**Ubuntu/Debian:**

```bash
sudo apt-get install libsnmp-dev libmysqlclient-dev
```

**RHEL/CentOS:**

```bash
sudo yum install net-snmp-devel mysql-devel
```

### Install the Package

```bash
git clone https://github.com/thomasvincent/python-auto-discover-network-Device-Management.git
cd python-auto-discover-network-Device-Management
pip install -e .
```

## Quick Start

1. Create an Excel file (`devices.xlsx`) with your devices:

   | A (Hostname) | C (IP Address) | D (SNMP Community) |
   |--------------|----------------|-------------------|
   | server1      | 192.168.1.10   | public            |
   | server2      | 192.168.1.11   | private           |

2. Run the discovery:

   ```bash
   network-discover devices.xlsx
   ```

3. View results in the generated `YYYY-MM-DD_check.xlsx` file.

## Usage

```bash
network-discover [OPTIONS] INPUTFILE
```

### Arguments

| Argument | Description |
|----------|-------------|
| `INPUTFILE` | Path to the Excel file containing device information (required) |

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output PATH` | Output Excel file path | `<date>_check.xlsx` |
| `-w, --workers N` | Number of concurrent scan workers | `10` |
| `-d, --database PATH` | SQLite database file path | `devices.db` |
| `-v, --verbose` | Enable debug logging | Disabled |
| `--no-ssh-strict` | Disable SSH host key verification | Enabled |
| `--version` | Show version and exit | — |
| `--help` | Show help message and exit | — |

### Examples

```bash
# Basic scan
network-discover devices.xlsx

# Custom output file with 20 workers
network-discover devices.xlsx -o results.xlsx -w 20

# Verbose mode with relaxed SSH checking
network-discover devices.xlsx -v --no-ssh-strict
```

## Configuration

### Input File Format

The input Excel file must contain device information in specific columns:

| Column | Field | Required | Default |
|--------|-------|----------|---------|
| A | Hostname | Yes | — |
| C | IP address | No | Uses hostname |
| D | SNMP community string | No | `public` |
| I | MySQL username | No | — |
| J | MySQL password | No | — |

> **Note:** Row 1 is assumed to be a header row and is skipped during import.

### Environment Variables

Configure SSH connection settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `SSH_USER` | Username for SSH connections | `root` |
| `SSH_KEY_FILE` | Path to SSH known_hosts file | `~/.ssh/known_hosts` |
| `SSH_STRICT_HOST_KEY` | Enable strict host key checking | `true` |

Configure email notifications (optional):

| Variable | Description |
|----------|-------------|
| `EMAIL_FROM` | Sender email address |
| `EMAIL_TO` | Recipient email address |
| `EMAIL_USERNAME` | SMTP authentication username |
| `EMAIL_PASSWORD` | SMTP authentication password |
| `EMAIL_SMTP_SERVER` | SMTP server in `host:port` format |

## Output

### Excel Report

The tool generates an Excel file (`YYYY-MM-DD_check.xlsx`) with the following columns:

| Column | Description | Values |
|--------|-------------|--------|
| name | Device hostname | String |
| managementip | Device IP address | IP address |
| state | Ping connectivity | `up` or `down` |
| snmp | SNMP accessibility | `open` or `closed` |
| ssh | SSH accessibility | `open` or `closed` |
| mysql | MySQL accessibility | `open` or `closed` |
| errors | Scan error messages | String (semicolon-separated) |

### SQLite Database

Device records are stored in `devices.db` for querying and historical tracking.

## Documentation

For detailed documentation, see the [docs/](docs/) directory:

- [Getting Started](docs/getting-started.md) — Installation and basic usage
- [API Reference](docs/api.md) — Module and class documentation
- [Contributing](docs/contributing.md) — Development setup and guidelines

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Development installation
pip install -e ".[dev]"

# Run linter
ruff check .

# Run type checker
mypy .

# Run tests
pytest
```

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
