# End-to-End Testing Guide

## Overview

netprobe includes comprehensive end-to-end tests that use real Docker containers running actual SSH, SNMP, and MySQL services. This ensures the scanner works correctly against real services, not just mocked responses.

## Quick Start

```bash
# Run all E2E tests
make test-e2e

# Or manually
docker-compose -f docker-compose.test.yml up -d
pytest test_e2e.py -v -m e2e
docker-compose -f docker-compose.test.yml down
```

## Test Infrastructure

### Docker Services

The E2E tests spin up 5 Docker containers on a private network (`172.20.0.0/16`):

| Service | IP | Ports | Description |
|---------|-----|-------|-------------|
| **ssh-server** | 172.20.0.10 | 2222 | OpenSSH server only |
| **mysql-server** | 172.20.0.11 | 3306 | MySQL 8.0 server only |
| **snmp-server** | 172.20.0.12 | 161/udp | SNMP daemon only |
| **combined-server** | 172.20.0.13 | 22, 3306, 161 | All three services |
| **empty-server** | 172.20.0.14 | none | No services (for negative tests) |

### Network Configuration

```
Network: 172.20.0.0/16
Subnet for tests: 172.20.0.0/24
```

## Test Coverage

### Unit Tests (`test_netprobe.py`)
- Device dataclass creation
- Scanner initialization
- Localhost scanning
- JSON/CSV export
- Error handling
- **11 tests** covering core functionality

### E2E Tests (`test_e2e.py`)
- Real service detection (SSH, MySQL, SNMP)
- Network-wide scanning
- Service isolation testing
- Export functionality with real data
- Concurrent scanning performance
- Docker environment health checks
- **15 tests** covering real-world scenarios

## Running Tests

### All Tests
```bash
# Run everything (unit + E2E)
make test-all

# With coverage
pytest test_netprobe.py test_e2e.py -v --cov=. --cov-report=html
```

### Unit Tests Only
```bash
make test-unit
# or
pytest test_netprobe.py -v
```

### E2E Tests Only
```bash
make test-e2e
# or
docker-compose -f docker-compose.test.yml up -d
sleep 20  # Wait for services
pytest test_e2e.py -v -m e2e
docker-compose -f docker-compose.test.yml down
```

### Individual E2E Test
```bash
# Start environment
make docker-up

# Run specific test
pytest test_e2e.py::test_scan_mysql_server -v -m e2e

# Cleanup
make docker-down
```

## Manual Testing

### Start Test Environment
```bash
make docker-up

# Or manually
docker-compose -f docker-compose.test.yml up -d
sleep 20
```

### Verify Services
```bash
# Check running containers
docker ps --filter name=test-

# Check logs
docker-compose -f docker-compose.test.yml logs -f

# Test connectivity
nmap -p 3306 172.20.0.11  # MySQL server
nmap -p 161 -sU 172.20.0.12  # SNMP server (UDP)
```

### Scan Test Network
```bash
# Scan single server
python netprobe.py scan 172.20.0.11 -v

# Scan entire test network
python netprobe.py scan 172.20.0.0/28

# Save results
python netprobe.py scan 172.20.0.0/28 -o test-results.json
```

### Cleanup
```bash
make docker-down

# Or manually
docker-compose -f docker-compose.test.yml down
```

## CI/CD Integration

The GitHub Actions CI automatically runs:

1. **Lint** - Ruff formatting and style checks
2. **Unit Tests** - On Python 3.12 & 3.13, Ubuntu & macOS
3. **E2E Tests** - On Ubuntu with Docker
4. **Type Check** - mypy static analysis

See `.github/workflows/ci.yml` for details.

## Writing New E2E Tests

### Test Template
```python
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_my_feature(docker_environment):
    """Test description."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(MYSQL_SERVER_IP)

    assert device.mysql is True
    # Additional assertions...
```

### Fixtures

**docker_environment** - Module-scoped fixture that:
- Starts docker-compose services
- Waits for services to be ready
- Yields for tests
- Cleans up containers on teardown

### Best Practices

1. **Use module scope** - `docker_environment` starts once for all E2E tests
2. **Mark tests** - Use `@pytest.mark.e2e` marker
3. **Async tests** - Use `@pytest.mark.asyncio` for async tests
4. **Realistic assertions** - Test actual behavior, not implementation details
5. **Fast tests** - Use concurrent scanning when testing multiple IPs

## Troubleshooting

### Services Not Starting
```bash
# Check Docker logs
docker-compose -f docker-compose.test.yml logs

# Restart environment
docker-compose -f docker-compose.test.yml down
docker-compose -f docker-compose.test.yml up -d
```

### Tests Hanging
```bash
# Increase wait time in test
# Edit test_e2e.py, increase sleep time:
time.sleep(30)  # Was 15

# Or check service health
docker inspect test-mysql-server --format='{{.State.Health.Status}}'
```

### Port Conflicts
```bash
# Check if ports are in use
lsof -i :3306
lsof -i :2222

# Kill conflicting services or change docker-compose ports
```

### Network Issues
```bash
# Verify Docker network
docker network ls
docker network inspect python-network-discovery-tool_test-network

# Test connectivity from host
ping 172.20.0.11
nmap -Pn 172.20.0.11
```

## Performance Benchmarks

Typical test execution times:

| Test Suite | Duration | Tests |
|------------|----------|-------|
| Unit Tests | ~3s | 11 |
| E2E Tests (full) | ~45s | 15 |
| E2E Tests (single) | ~5s | 1 |
| Docker Startup | ~20s | - |

## Example Test Run

```bash
$ make test-e2e

🐳 Starting Docker test environment...
[+] Running 6/6
 ✔ Network python-network-discovery-tool_test-network   Created
 ✔ Container test-empty-server                          Started
 ✔ Container test-snmp-server                           Started
 ✔ Container test-combined-server                       Started
 ✔ Container test-ssh-server                            Started
 ✔ Container test-mysql-server                          Started

⏳ Waiting for services to be ready...
✅ MySQL server is healthy

🧪 Running E2E tests...

test_e2e.py::test_scan_ssh_server PASSED           [  6%]
test_e2e.py::test_scan_mysql_server PASSED         [ 13%]
test_e2e.py::test_scan_snmp_server PASSED          [ 20%]
test_e2e.py::test_scan_combined_server PASSED      [ 26%]
test_e2e.py::test_scan_empty_server PASSED         [ 33%]
test_e2e.py::test_scan_entire_network PASSED       [ 40%]
test_e2e.py::test_service_detection_accuracy PASSED [ 46%]
test_e2e.py::test_json_export_e2e PASSED           [ 53%]
test_e2e.py::test_csv_export_e2e PASSED            [ 60%]
test_e2e.py::test_concurrent_scanning_performance PASSED [ 66%]
test_e2e.py::test_hostname_resolution PASSED       [ 73%]
test_e2e.py::test_error_handling_unreachable PASSED [ 80%]
test_e2e.py::test_network_scan_filters_alive_only PASSED [ 86%]
test_e2e.py::test_docker_environment_health PASSED [ 93%]

======================== 14 passed in 25.43s ========================

🧹 Cleaning up Docker environment...
[+] Running 6/6
 ✔ Container test-combined-server   Removed
 ✔ Container test-snmp-server       Removed
 ✔ Container test-mysql-server      Removed
 ✔ Container test-ssh-server        Removed
 ✔ Container test-empty-server      Removed
 ✔ Network test-network             Removed
```

## References

- **Docker Compose**: `docker-compose.test.yml`
- **E2E Tests**: `test_e2e.py`
- **Unit Tests**: `test_netprobe.py`
- **Makefile**: `Makefile`
- **CI Workflow**: `.github/workflows/ci.yml`
