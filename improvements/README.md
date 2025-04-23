# Network Discovery Tool

A network discovery tool that uses Nmap to identify if SSH, Ping, SNMP, and MySQL are running on various connected devices in a network.

## Features

- Scan networks or individual devices
- Check for SSH, SNMP, and MySQL services
- Generate reports in HTML, CSV, Excel, or JSON formats
- Store device information in JSON files or Redis
- Send notifications via email or console
- Asynchronous scanning for improved performance
- Comprehensive error handling and logging
- Optimized for large networks with efficient data storage

## Installation

### From PyPI

```bash
pip install network-discovery
```

### From Source

```bash
git clone https://github.com/thomasvincent/python-network-discovery-tool.git
cd python-network-discovery-tool
pip install -e .
```

## Requirements

- Python 3.7 or higher
- Nmap (must be installed on the system)
- Other dependencies are installed automatically

## Usage

### Command Line Interface

```bash
# Scan a network
network-discovery 192.168.1.0/24

# Scan a single device
network-discovery 192.168.1.1

# Generate a CSV report
network-discovery 192.168.1.0/24 -f csv

# Enable verbose output
network-discovery 192.168.1.0/24 -v

# Specify output directory
network-discovery 192.168.1.0/24 -o /path/to/output

# Specify template directory for HTML reports
network-discovery 192.168.1.0/24 -t /path/to/templates

# Disable report generation
network-discovery 192.168.1.0/24 --no-report

# Disable notifications
network-discovery 192.168.1.0/24 --no-notification

# Disable device storage
network-discovery 192.168.1.0/24 --no-repository

# Specify repository file
network-discovery 192.168.1.0/24 --repository-file /path/to/devices.json

# Send email notifications
network-discovery 192.168.1.0/24 --email --smtp-username user@example.com --smtp-password password --email-recipient admin@example.com
```

### Python API

```python
import asyncio
from network_discovery.core.discovery import DeviceDiscoveryService
from network_discovery.infrastructure.scanner import NmapDeviceScanner
from network_discovery.infrastructure.repository import JsonFileRepository
from network_discovery.infrastructure.notification import ConsoleNotificationService
from network_discovery.infrastructure.report import ReportGenerator

async def main():
    # Configure services
    scanner = NmapDeviceScanner()
    repository = JsonFileRepository("devices.json")
    notification_service = ConsoleNotificationService()
    report_service = ReportGenerator("./output", "./templates")

    # Create discovery service
    discovery_service = DeviceDiscoveryService(
        scanner, repository, notification_service, report_service
    )

    # Scan a network
    devices = await discovery_service.discover_network("192.168.1.0/24")
    
    # Generate a report
    report_path = discovery_service.generate_report("html")
    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Output

The tool can generate reports in the following formats:

- HTML: A web page with a table of devices and their status
- CSV: A comma-separated values file with device information
- Excel: An Excel spreadsheet with device information
- JSON: A JSON file with device information

## Architecture

The tool follows a layered architecture:

- **Domain Layer**: Contains the core domain models (`Device`, `DeviceManager`)
- **Application Layer**: Defines interfaces for services
- **Infrastructure Layer**: Provides implementations for services (scanner, repository, notification, report)
- **Interface Layer**: Provides the CLI and API interfaces

## Improvements

Recent improvements include:

- **Performance**: Optimized for large networks with efficient data storage
- **Error Handling**: More specific exception handling and consistent logging
- **Input Validation**: Better validation of network inputs and configuration
- **Repository**: Improved Redis and JSON file repositories for better performance
- **CLI**: Enhanced command-line interface with more options and better error feedback
- **Testing**: Comprehensive test coverage for all components

## Development

### Setup Development Environment

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run Linters

```bash
flake8 src tests
black src tests
isort src tests
mypy src tests
```

### Run Tox

```bash
tox
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## Security

Please see the [SECURITY.md](SECURITY.md) file for details on reporting security issues.
