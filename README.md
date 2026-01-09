# Network Device Discovery Tool

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
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
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multi-protocol scanning** — Check ping, SSH, SNMP, and MySQL connectivity
- **Excel integration** — Import device lists and export scan results to `.xlsx` files
- **Concurrent execution** — Parallel scanning with configurable worker threads
- **Persistent storage** — SQLite database for device records
- **Security-focused** — Strict SSH host key checking enabled by default

## Requirements

- Python 3.12 or later
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
| `--no-ping-gate` | Scan SSH/SNMP/MySQL even if ping fails | Disabled |
| `--keep-db` | Preserve existing database instead of recreating | Disabled |
| `--timeout SECONDS` | Override timeout for all scan operations | Protocol defaults |
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

# Scan firewalled networks (don't skip services if ping fails)
network-discover devices.xlsx --no-ping-gate

# Fast scan with 5-second timeout and 50 workers
network-discover devices.xlsx --timeout 5 -w 50

# Preserve database between runs
network-discover devices.xlsx --keep-db
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
| `SSH_KNOWN_HOSTS_FILE` | Path to SSH known_hosts file | `~/.ssh/known_hosts` |
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

Device records are stored in `devices.db` for querying.

> **Note:** By default, the database is recreated on each run. Use `--keep-db` to preserve existing data.

## Troubleshooting

### Common Issues

**"No devices found in input file"**
- Ensure your Excel file has data starting from row 2 (row 1 is treated as header)
- Check that column A contains hostnames or IP addresses

**SSH scans failing with "Host key verification failed"**
- Add the target hosts to your `~/.ssh/known_hosts` file first
- Or use `--no-ssh-strict` (less secure, not recommended for production)

**SNMP scans timing out**
- Verify the SNMP community string is correct
- Check that SNMP is enabled on the target device
- Ensure UDP port 161 is not blocked by firewalls

**Scans taking too long**
- Increase worker count with `-w 50` for faster parallel scanning
- Use `--timeout 5` to reduce individual scan timeouts
- For large networks, consider scanning in smaller batches

**All services showing "closed" even though they're running**
- Use `--no-ping-gate` if your network blocks ICMP ping
- Check that the services are listening on standard ports

### Debug Mode

For detailed troubleshooting, enable verbose logging:

```bash
network-discover devices.xlsx -v 2>&1 | tee scan.log
```

## Security

### Best Practices

1. **SSH Host Key Verification**: Keep strict host key checking enabled (default) to prevent MITM attacks. Only use `--no-ssh-strict` in controlled test environments.

2. **Credential Protection**:
   - MySQL passwords and SNMP community strings are read from the input Excel file
   - These credentials are NOT stored in the database for security
   - Keep your input Excel files in a secure location with appropriate permissions

3. **Network Considerations**:
   - Only scan networks you own or have explicit authorization to test
   - Be aware that aggressive scanning may trigger security alerts
   - Consider using `--timeout` and `-w` settings appropriate for your network

4. **File Permissions**: Secure your configuration files:
   ```bash
   chmod 600 devices.xlsx  # Restrict access to input file with credentials
   ```

### Environment Variable Security

When using environment variables for email configuration:
- Avoid storing passwords in shell history
- Use a `.env` file with restricted permissions
- Consider using a secrets manager for production deployments

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
