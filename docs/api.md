# API Reference

This document provides reference documentation for all public modules, classes, and functions.

## Table of Contents

- [devices module](#devices-module)
- [database module](#database-module)
- [spreadsheet module](#spreadsheet-module)
- [mail module](#mail-module)
- [discovery module](#discovery-module)

---

## devices module

Core device scanning functionality.

### Device

Represents a network device that can be scanned for service availability.

```python
from devices import Device, ScanConfig

device = Device(
    id=1,
    host="server1.example.com",
    ip="10.0.0.1",
    snmp_community="public",
    mysql_user="root",
    _mysql_password="secret",
)

# Scan all services
config = ScanConfig()
results = device.scan_all(config)

# Check status
print(device.status)  # DeviceStatus.UP or DeviceStatus.DOWN
print(device.alive)   # True/False
print(device.ssh)     # True/False
print(device.snmp)    # True/False
print(device.mysql)   # True/False
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique device identifier |
| `host` | `str` | Hostname |
| `ip` | `str` | IP address |
| `snmp_community` | `str` | SNMP community string |
| `mysql_user` | `str` | MySQL username |
| `alive` | `bool` | Ping result |
| `ssh` | `bool` | SSH accessibility |
| `snmp` | `bool` | SNMP accessibility |
| `mysql` | `bool` | MySQL accessibility |
| `errors` | `list[str]` | Scan error messages |

### ScanConfig

Configuration for network scanning operations.

```python
from devices import ScanConfig

config = ScanConfig(
    ssh_user="admin",              # SSH username
    ssh_timeout=3,                 # SSH connection timeout (seconds)
    ping_timeout=20,               # Ping timeout (seconds)
    snmp_timeout=2,                # SNMP timeout (seconds)
    snmp_version=2,                # SNMP version (1 or 2)
    mysql_timeout=5,               # MySQL connection timeout (seconds)
    ssh_strict_host_key=True,      # Strict SSH host key checking
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ssh_user` | `str` | `"root"` | SSH username |
| `ssh_timeout` | `int` | `3` | SSH timeout in seconds |
| `ping_timeout` | `int` | `20` | Ping timeout in seconds |
| `snmp_timeout` | `int` | `2` | SNMP timeout in seconds |
| `snmp_version` | `int` | `2` | SNMP protocol version |
| `mysql_timeout` | `int` | `5` | MySQL timeout in seconds |
| `ssh_strict_host_key` | `bool` | `True` | Enable strict host key checking |

### ScanResult

Result of a network scan operation.

```python
result = device.scan_ping()
print(result.success)     # True/False
print(result.scan_type)   # ScanType.PING
print(result.error)       # Error message if failed
print(result.data)        # Additional scan data
```

### validate_host

Validates and sanitizes a hostname or IP address.

```python
from devices import validate_host, ValidationError

try:
    host = validate_host("server1.example.com")
except ValidationError as e:
    print(f"Invalid host: {e}")
```

**Raises:** `ValidationError` if the hostname contains invalid characters.

---

## database module

SQLite database storage for device data.

### Database

SQLite database for storing network device information.

```python
from database import Database

db = Database("devices.db")
db.create_table()

# Insert devices
db.insert_device(device)
db.insert_devices([device1, device2])

# Query devices
all_devices = db.get_all_devices()
device = db.get_device(1)
device = db.get_device_by_host("server1")

# Update and delete
db.update_device(device)
db.delete_device(1)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `create_table(drop_existing=False)` | Create the devices table |
| `insert_device(device)` | Insert a single device |
| `insert_devices(devices)` | Insert multiple devices |
| `get_device(id)` | Get device by ID |
| `get_device_by_host(host)` | Get device by hostname |
| `get_all_devices()` | Get all devices |
| `update_device(device)` | Update device record |
| `delete_device(id)` | Delete device by ID |

### Exporter

Export device data to various formats.

```python
from database import Exporter

exporter = Exporter(devices=devices)
exporter.to_csv("devices.csv")
exporter.to_html("devices.html")
```

### Importer

Import device data from various formats.

```python
from database import Importer, Database

db = Database("devices.db")
importer = Importer(database=db)
count = importer.from_csv("devices.csv")
```

---

## spreadsheet module

Excel spreadsheet import/export functionality.

### import_from_excel

Import devices from an Excel spreadsheet.

```python
from spreadsheet import import_from_excel

devices = import_from_excel("devices.xlsx")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `spreadsheet_path` | `str \| Path` | Path to Excel file |

**Returns:** `list[Device]` — List of imported devices.

**Raises:** `FileNotFoundError` if the file does not exist.

### export_to_excel

Export devices to an Excel spreadsheet.

```python
from spreadsheet import export_to_excel

output_path = export_to_excel(devices, "results.xlsx")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `devices` | `list[Device]` | Devices to export |
| `spreadsheet_path` | `str \| Path \| None` | Output path (auto-generated if None) |
| `send_email` | `bool` | Send results via email |

**Returns:** `Path` — Path to the output file.

### SpreadsheetImporter

Class-based interface for importing devices.

```python
from spreadsheet import SpreadsheetImporter, ColumnConfig

config = ColumnConfig(host='A', ip='C', snmp_community='D')
importer = SpreadsheetImporter(file_path="devices.xlsx", column_config=config)
devices = importer.import_devices()
```

### SpreadsheetExporter

Class-based interface for exporting devices.

```python
from spreadsheet import SpreadsheetExporter, ExportConfig

config = ExportConfig(include_header=True, auto_width=True)
exporter = SpreadsheetExporter(devices=devices, export_config=config)
output_path = exporter.export("results.xlsx")
```

---

## mail module

Email notifications for scan results.

### send

Send an email with a file attachment.

```python
from mail import send

# Requires EMAIL_* environment variables
send("results.xlsx", "Network Scan Results")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | `str \| Path` | File to attach |
| `subject` | `str \| None` | Email subject |

**Environment variables required:**

- `EMAIL_FROM` — Sender email address
- `EMAIL_TO` — Recipient email address
- `EMAIL_USERNAME` — SMTP username
- `EMAIL_PASSWORD` — SMTP password
- `EMAIL_SMTP_SERVER` — SMTP server (`host:port`)

### EmailSender

Full-featured email sender class.

```python
from mail import EmailSender, EmailConfig

config = EmailConfig(
    email_from="sender@example.com",
    email_to="recipient@example.com",
    username="sender@example.com",
    password="app-password",
    smtp_server="smtp.gmail.com:587",
)

sender = EmailSender(config=config)
sender.send_email("results.xlsx", "Scan Results")
```

---

## discovery module

CLI orchestrator for device discovery.

### main

Main entry point for the CLI.

```python
from discovery import main

# Run with command-line arguments
exit_code = main(["devices.xlsx", "-v", "-w", "20"])
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `argv` | `list[str] \| None` | Command-line arguments |

**Returns:** `int` — Exit code (0 for success).

### scan_devices

Scan multiple devices concurrently.

```python
from discovery import scan_devices
from devices import ScanConfig

config = ScanConfig()
scanned = scan_devices(devices, config, max_workers=20)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `devices` | `list[Device]` | — | Devices to scan |
| `config` | `ScanConfig` | — | Scan configuration |
| `max_workers` | `int` | `10` | Maximum concurrent workers |

**Returns:** `list[Device]` — Scanned devices with results.

### DiscoveryStats

Statistics from a discovery run.

```python
from discovery import DiscoveryStats

stats = DiscoveryStats.from_devices(scanned_devices)
print(stats.total)   # Total devices
print(stats.alive)   # Devices responding to ping
print(stats.ssh)     # Devices with SSH open
print(stats.snmp)    # Devices with SNMP open
print(stats.mysql)   # Devices with MySQL open
print(stats.errors)  # Devices with errors
```
