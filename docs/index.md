# Network Device Discovery Tool

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

A command-line tool for scanning network devices to check SSH, SNMP, MySQL, and ICMP (ping) connectivity.

## Features

| Feature | Description |
|---------|-------------|
| Multi-protocol scanning | Check ping, SSH, SNMP, and MySQL connectivity |
| Excel integration | Import device lists and export scan results to `.xlsx` files |
| Concurrent execution | Parallel scanning with configurable worker threads |
| Persistent storage | SQLite database for device records and scan history |
| Security-focused | Strict SSH host key checking enabled by default |

## Quick Start

```bash
# Install
pip install -e .

# Run discovery
network-discover devices.xlsx

# View results in YYYY-MM-DD_check.xlsx
```

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | Installation and basic usage |
| [API Reference](api.md) | Module and class documentation |
| [Contributing](../CONTRIBUTING.md) | Development setup and guidelines |

## Requirements

- Python 3.14 or later
- System SNMP libraries (`net-snmp`)
- MySQL client libraries (`libmysqlclient`)

## License

This project is licensed under the [Apache License 2.0](../LICENSE).
