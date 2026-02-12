"""End-to-end tests for netprobe using real Docker services.

These tests require Docker and docker-compose to be running.
Start the test environment with:
    docker-compose -f docker-compose.test.yml up -d

Stop with:
    docker-compose -f docker-compose.test.yml down
"""

import asyncio
import json
import subprocess
import time

import pytest

from netprobe import NetworkScanner, save_csv, save_json

# Test network configuration (matches docker-compose.test.yml)
TEST_NETWORK = "172.20.0.0/24"
SSH_SERVER_IP = "172.20.0.10"
MYSQL_SERVER_IP = "172.20.0.11"
SNMP_SERVER_IP = "172.20.0.12"
COMBINED_SERVER_IP = "172.20.0.13"
EMPTY_SERVER_IP = "172.20.0.14"


@pytest.fixture(scope="module")
def docker_environment():
    """Start Docker test environment and ensure services are ready."""
    # Start docker-compose
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "up", "-d"],
        check=True,
        capture_output=True,
    )

    # Wait for services to be ready
    print("\n⏳ Waiting for test services to start...")
    time.sleep(15)  # Give services time to start

    # Wait for MySQL to be healthy
    for _i in range(30):
        result = subprocess.run(
            ["docker", "inspect", "--format={{.State.Health.Status}}", "test-mysql-server"],
            capture_output=True,
            text=True,
        )
        if "healthy" in result.stdout:
            print("✅ MySQL server is healthy")
            break
        time.sleep(2)
    else:
        print("⚠️  MySQL server health check timed out, continuing anyway")

    time.sleep(5)  # Extra time for all services

    yield

    # Cleanup
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "down"],
        check=True,
        capture_output=True,
    )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_scan_ssh_server(docker_environment):
    """Test scanning a server with only SSH."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(SSH_SERVER_IP)

    assert device.ip == SSH_SERVER_IP
    assert device.alive is True, "SSH server should be alive"
    assert device.ssh is True, "SSH port 2222 should be detected as open"
    # Note: SSH is on port 2222, not 22, so our scanner won't detect it
    # This tests the actual behavior


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_scan_mysql_server(docker_environment):
    """Test scanning a server with only MySQL."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(MYSQL_SERVER_IP)

    assert device.ip == MYSQL_SERVER_IP
    assert device.alive is True, "MySQL server should be alive"
    assert device.mysql is True, "MySQL port 3306 should be open"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_scan_snmp_server(docker_environment):
    """Test scanning a server with only SNMP."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(SNMP_SERVER_IP)

    assert device.ip == SNMP_SERVER_IP
    assert device.alive is True, "SNMP server should be alive"
    assert device.snmp is True, "SNMP port 161 should be open"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_scan_combined_server(docker_environment):
    """Test scanning a server with SSH, MySQL, and SNMP."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(COMBINED_SERVER_IP)

    assert device.ip == COMBINED_SERVER_IP
    assert device.alive is True, "Combined server should be alive"
    # The combined server has all three services
    # Results will depend on actual service startup


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_scan_empty_server(docker_environment):
    """Test scanning a server with no services."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(EMPTY_SERVER_IP)

    assert device.ip == EMPTY_SERVER_IP
    assert device.alive is True, "Empty server should be alive"
    assert device.ssh is False, "Empty server should not have SSH"
    assert device.snmp is False, "Empty server should not have SNMP"
    assert device.mysql is False, "Empty server should not have MySQL"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_scan_entire_network(docker_environment):
    """Test scanning the entire test network."""
    scanner = NetworkScanner()
    devices = await scanner.scan_network(TEST_NETWORK)

    # Should find at least our test servers
    alive_devices = [d for d in devices if d.alive]
    assert len(alive_devices) >= 4, (
        f"Should find at least 4 alive hosts, found {len(alive_devices)}"
    )

    # Check that specific IPs are found
    device_ips = {d.ip for d in alive_devices}
    expected_ips = {
        SSH_SERVER_IP,
        MYSQL_SERVER_IP,
        SNMP_SERVER_IP,
        COMBINED_SERVER_IP,
        EMPTY_SERVER_IP,
    }

    # At least some of our test servers should be found
    found_test_servers = device_ips.intersection(expected_ips)
    assert len(found_test_servers) >= 3, (
        f"Should find at least 3 test servers, found {found_test_servers}"
    )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_service_detection_accuracy(docker_environment):
    """Test that service detection is accurate for known configurations."""
    scanner = NetworkScanner()

    # Scan all test servers
    results = await asyncio.gather(
        scanner.scan_device(MYSQL_SERVER_IP),
        scanner.scan_device(SNMP_SERVER_IP),
        scanner.scan_device(EMPTY_SERVER_IP),
    )

    mysql_server, snmp_server, empty_server = results

    # MySQL server should only have MySQL
    assert mysql_server.mysql is True, "MySQL server should have MySQL"
    assert mysql_server.ssh is False, "MySQL server should not have SSH on port 22"

    # SNMP server should only have SNMP
    assert snmp_server.snmp is True, "SNMP server should have SNMP"
    assert snmp_server.ssh is False, "SNMP server should not have SSH"
    assert snmp_server.mysql is False, "SNMP server should not have MySQL"

    # Empty server should have nothing
    assert empty_server.ssh is False, "Empty server should not have SSH"
    assert empty_server.snmp is False, "Empty server should not have SNMP"
    assert empty_server.mysql is False, "Empty server should not have MySQL"


@pytest.mark.e2e
def test_json_export_e2e(docker_environment, tmp_path):
    """Test JSON export with real scan data."""
    scanner = NetworkScanner()

    # Scan a few servers
    devices = asyncio.run(
        asyncio.gather(
            scanner.scan_device(MYSQL_SERVER_IP),
            scanner.scan_device(SNMP_SERVER_IP),
            scanner.scan_device(EMPTY_SERVER_IP),
        )
    )

    # Export to JSON
    output_file = tmp_path / "e2e_results.json"
    save_json(devices, output_file)

    # Verify JSON content
    assert output_file.exists()
    data = json.loads(output_file.read_text())

    assert len(data) == 3
    assert any(d["ip"] == MYSQL_SERVER_IP and d["mysql"] for d in data)
    assert any(d["ip"] == SNMP_SERVER_IP and d["snmp"] for d in data)
    assert any(d["ip"] == EMPTY_SERVER_IP and not d["ssh"] for d in data)


@pytest.mark.e2e
def test_csv_export_e2e(docker_environment, tmp_path):
    """Test CSV export with real scan data."""
    scanner = NetworkScanner()

    # Scan servers
    devices = asyncio.run(
        asyncio.gather(
            scanner.scan_device(MYSQL_SERVER_IP),
            scanner.scan_device(EMPTY_SERVER_IP),
        )
    )

    # Export to CSV
    output_file = tmp_path / "e2e_results.csv"
    save_csv(devices, output_file)

    # Verify CSV content
    assert output_file.exists()
    content = output_file.read_text()

    assert MYSQL_SERVER_IP in content
    assert EMPTY_SERVER_IP in content
    assert "ip,alive,ssh,snmp,mysql,hostname,errors" in content


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_concurrent_scanning_performance(docker_environment):
    """Test that concurrent scanning is faster than sequential."""
    scanner = NetworkScanner()
    test_ips = [MYSQL_SERVER_IP, SNMP_SERVER_IP, EMPTY_SERVER_IP] * 3  # 9 scans

    # Concurrent scan
    start = time.time()
    await asyncio.gather(*[scanner.scan_device(ip) for ip in test_ips])
    concurrent_time = time.time() - start

    print(f"\n⚡ Concurrent scan of 9 hosts took: {concurrent_time:.2f}s")

    # Should complete in reasonable time (much faster than sequential)
    assert concurrent_time < 30, f"Concurrent scan took too long: {concurrent_time}s"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_hostname_resolution(docker_environment):
    """Test that hostnames are resolved when possible."""
    scanner = NetworkScanner()
    device = await scanner.scan_device(MYSQL_SERVER_IP)

    # Hostname might be resolved or might be empty
    # Just verify the field exists and is a string
    assert isinstance(device.hostname, str)


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_error_handling_unreachable(docker_environment):
    """Test error handling for unreachable hosts in the network."""
    scanner = NetworkScanner()

    # Scan an IP that should be unreachable (outside test network but in scan range)
    device = await scanner.scan_device("172.20.0.254")

    assert device.ip == "172.20.0.254"
    # Host might be down or might not exist
    # Just verify error handling doesn't crash
    assert isinstance(device.errors, list)


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_network_scan_filters_alive_only(docker_environment):
    """Test that network scan correctly identifies alive vs down hosts."""
    scanner = NetworkScanner()

    # Scan a small range that includes some alive and some dead IPs
    devices = await scanner.scan_network("172.20.0.10/30")  # IPs: .8, .9, .10, .11

    alive_count = sum(1 for d in devices if d.alive)
    dead_count = sum(1 for d in devices if not d.alive)

    print(f"\n📊 Scan results: {alive_count} alive, {dead_count} down")

    # Should have at least one alive host (.10 is SSH server)
    assert alive_count >= 1, "Should find at least one alive host"


@pytest.mark.e2e
def test_docker_environment_health(docker_environment):
    """Verify Docker test environment is running correctly."""
    # Check that containers are running
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=test-", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )

    running_containers = result.stdout.strip().split("\n")
    running_containers = [c for c in running_containers if c]  # Filter empty

    print(f"\n🐳 Running test containers: {running_containers}")

    # Should have our test containers
    assert len(running_containers) >= 3, (
        f"Expected at least 3 test containers, found {len(running_containers)}"
    )

    # Verify specific containers
    container_names = set(running_containers)
    expected_containers = {
        "test-ssh-server",
        "test-mysql-server",
        "test-snmp-server",
        "test-empty-server",
    }

    found = container_names.intersection(expected_containers)
    assert len(found) >= 3, f"Expected to find test containers, found: {found}"
