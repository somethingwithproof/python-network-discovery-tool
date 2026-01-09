# Getting Started

## Prerequisites

- Python 3.12 or later
- SNMP libraries (net-snmp) for SNMP scanning
- MySQL client libraries for MySQL scanning

### System Dependencies

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

## Installation

### From Source

```bash
git clone https://github.com/thomasvincent/python-auto-discover-network-Device-Management.git
cd python-auto-discover-network-Device-Management
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Basic Usage

### Prepare Input File

Create an Excel file (`devices.xlsx`) with device information:

| Column A | Column C | Column D | Column I | Column J |
|----------|----------|----------|----------|----------|
| hostname | ip_addr  | snmp_community | mysql_user | mysql_pass |
| server1  | 10.0.0.1 | public   | root     | secret   |
| server2  | 10.0.0.2 | private  |          |          |

### Run Discovery

```bash
# Basic scan
network-discover devices.xlsx

# With options
network-discover devices.xlsx -o results.xlsx -w 20 -v
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output Excel file path |
| `-w, --workers` | Number of concurrent workers (default: 10) |
| `-d, --database` | SQLite database path (default: devices.db) |
| `-v, --verbose` | Enable debug logging |
| `--no-ssh-strict` | Disable SSH host key verification |

## Environment Variables

Configure SSH and email settings via environment variables:

```bash
export SSH_USER=admin
export SSH_KEY_FILE=/path/to/known_hosts
export SSH_STRICT_HOST_KEY=true
```

## Output

After scanning, you'll have:

1. **Excel file** (`<date>_check.xlsx`): Scan results in spreadsheet format
2. **SQLite database** (`devices.db`): Full device records for querying

### Result Columns

| Column | Values |
|--------|--------|
| name | Device hostname |
| managementip | Device IP address |
| state | `up` or `down` (ping result) |
| snmp | `open` or `closed` |
| ssh | `open` or `closed` |
| mysql | `open` or `closed` |
| errors | Any scan errors |

## Troubleshooting

### Installation Issues

**Error: `snimpy` installation fails**

Ensure SNMP development libraries are installed:

```bash
# macOS
brew install net-snmp

# Ubuntu/Debian
sudo apt-get install libsnmp-dev

# RHEL/CentOS
sudo yum install net-snmp-devel
```

**Error: `mysqlclient` installation fails**

Ensure MySQL client libraries are installed:

```bash
# macOS
brew install mysql-client
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"

# Ubuntu/Debian
sudo apt-get install libmysqlclient-dev

# RHEL/CentOS
sudo yum install mysql-devel
```

### Scan Issues

**All devices show as "down"**

1. Verify network connectivity: `ping <device-ip>`
2. Check firewall rules allow ICMP
3. Increase timeout: edit `ScanConfig.ping_timeout`

**SSH scans fail with "Host key verification failed"**

By default, strict host key checking is enabled. Options:

1. Add host keys to known_hosts: `ssh-keyscan <host> >> ~/.ssh/known_hosts`
2. Disable strict checking (less secure): `--no-ssh-strict`

**SNMP scans fail**

1. Verify SNMP is enabled on the device
2. Check the community string matches
3. Ensure UDP port 161 is not blocked
4. Try SNMPv1 if v2c fails (edit config)

**MySQL scans fail with "Access denied"**

1. Verify credentials in the Excel file
2. Check the MySQL user has remote access permissions
3. Ensure TCP port 3306 is not blocked

### Performance Issues

**Scans are slow**

1. Increase worker count: `-w 50`
2. Reduce timeouts in `ScanConfig`
3. Ensure network latency is acceptable

**Memory usage is high**

1. Reduce worker count: `-w 5`
2. Process devices in smaller batches

### Getting Help

If issues persist:

1. Run with verbose logging: `-v`
2. Check the error messages in the output
3. Open an issue on [GitHub](https://github.com/thomasvincent/python-auto-discover-network-Device-Management/issues)
