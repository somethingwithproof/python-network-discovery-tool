"""Tests for netprobe - Modern network scanner."""

import asyncio
import json
import threading
from unittest.mock import MagicMock, patch

import pytest
from rich.progress import Progress
from typer.testing import CliRunner

import netprobe
from netprobe import Device, NetworkScanner, app, cli, print_results, save_csv, save_json
from netprobe import scanner as scanner_module


def test_device_creation():
    """Test Device dataclass creation."""
    device = Device(ip="192.168.1.1")
    assert device.ip == "192.168.1.1"
    assert not device.alive
    assert not device.ssh
    assert device.errors == []


def test_device_with_services():
    """Test Device with services enabled."""
    device = Device(
        ip="192.168.1.10", alive=True, ssh=True, snmp=True, mysql=False, hostname="server.local"
    )
    assert device.alive
    assert device.ssh
    assert device.snmp
    assert not device.mysql
    assert device.hostname == "server.local"


@pytest.mark.asyncio
async def test_scanner_initialization():
    """Test NetworkScanner initialization."""
    scanner = NetworkScanner()
    assert scanner.nm is not None


@pytest.mark.asyncio
async def test_check_alive_localhost():
    """Test alive check on localhost."""
    scanner = NetworkScanner()
    # Localhost should always be up
    alive = await asyncio.to_thread(scanner._check_alive, "127.0.0.1")
    assert alive is True


@pytest.mark.asyncio
async def test_scan_localhost():
    """Test scanning localhost."""
    scanner = NetworkScanner()
    device = await scanner.scan_device("127.0.0.1")

    assert device.ip == "127.0.0.1"
    assert device.alive is True
    # SSH might or might not be running locally
    assert isinstance(device.ssh, bool)


@pytest.mark.asyncio
async def test_scan_invalid_ip():
    """Test scanning invalid IP gracefully handles errors."""
    scanner = NetworkScanner()
    device = await scanner.scan_device("999.999.999.999")

    assert device.ip == "999.999.999.999"
    assert not device.alive


def test_save_json(tmp_path):
    """Test JSON export."""
    devices = [
        Device(ip="192.168.1.1", alive=True, ssh=True),
        Device(ip="192.168.1.2", alive=False),
    ]

    output_file = tmp_path / "test.json"
    save_json(devices, output_file)

    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert len(data) == 2
    assert data[0]["ip"] == "192.168.1.1"
    assert data[0]["ssh"] is True


def test_save_csv(tmp_path):
    """Test CSV export."""
    devices = [
        Device(ip="192.168.1.1", alive=True, ssh=True, hostname="server"),
        Device(ip="192.168.1.2", alive=False),
    ]

    output_file = tmp_path / "test.csv"
    save_csv(devices, output_file)

    assert output_file.exists()
    content = output_file.read_text()
    assert "192.168.1.1" in content
    assert "192.168.1.2" in content
    assert "server" in content


@pytest.mark.asyncio
async def test_scan_network_single_ip():
    """Test scanning a single IP address."""
    scanner = NetworkScanner()
    devices = await scanner.scan_network("127.0.0.1")

    assert len(devices) == 1
    assert devices[0].ip == "127.0.0.1"
    assert devices[0].alive is True


@pytest.mark.asyncio
async def test_scan_network_invalid():
    """Test scanning with invalid network raises error."""
    scanner = NetworkScanner()

    with pytest.raises(ValueError, match="Invalid network format"):
        await scanner.scan_network("999.999.999.999/24")


@pytest.mark.asyncio
async def test_concurrent_scanning():
    """Test that multiple hosts can be scanned concurrently."""
    scanner = NetworkScanner()
    # Scan a small range including localhost
    devices = await scanner.scan_network("127.0.0.0/30")

    # Should return 2 hosts (127.0.0.1 and 127.0.0.2)
    assert len(devices) == 2
    # At least localhost should be alive
    alive_count = sum(1 for d in devices if d.alive)
    assert alive_count >= 1


class FakeNmap:
    """Stand-in for nmap.PortScanner, the system boundary around the nmap binary."""

    def __init__(self, hosts=None, raise_on_scan=False):
        self.hosts = hosts or {}
        self.raise_on_scan = raise_on_scan
        self.scans = []

    def scan(self, hosts=None, arguments=None):
        if self.raise_on_scan:
            raise RuntimeError("nmap failed")
        self.scans.append((hosts, arguments))

    def all_hosts(self):
        return list(self.hosts)

    def __getitem__(self, ip):
        return self.hosts[ip]


def make_host(state="up", tcp=None, udp=None):
    host = MagicMock()
    host.state.return_value = state
    protocols = {"tcp": tcp, "udp": udp}
    host.get.side_effect = lambda key, default=None: protocols.get(key) or default
    return host


def scanner_with(fake):
    scanner = NetworkScanner.__new__(NetworkScanner)
    scanner._new_scanner = lambda: fake
    scanner.nm = fake
    return scanner


def test_check_alive_states():
    up = scanner_with(FakeNmap({"10.0.0.1": make_host("up")}))
    down = scanner_with(FakeNmap({"10.0.0.1": make_host("down")}))
    missing = scanner_with(FakeNmap())

    assert up._check_alive("10.0.0.1") is True
    assert down._check_alive("10.0.0.1") is False
    assert missing._check_alive("10.0.0.1") is False


def test_check_alive_swallows_nmap_errors():
    assert scanner_with(FakeNmap(raise_on_scan=True))._check_alive("10.0.0.1") is False


@pytest.mark.asyncio
async def test_check_port_open_closed_and_missing():
    host = make_host(tcp={22: {"state": "open"}, 3306: {"state": "closed"}})
    scanner = scanner_with(FakeNmap({"10.0.0.1": host}))

    assert await scanner._check_port("10.0.0.1", 22) is True
    assert await scanner._check_port("10.0.0.1", 3306) is False
    assert await scanner._check_port("10.0.0.1", 161) is False
    assert await scanner._check_port("10.0.0.2", 22) is False


@pytest.mark.asyncio
async def test_check_port_nmap_error_returns_false():
    scanner = scanner_with(FakeNmap(raise_on_scan=True))
    assert await scanner._check_port("10.0.0.1", 22) is False


def test_get_hostname():
    scanner = scanner_with(FakeNmap())
    with patch("socket.gethostbyaddr", return_value=("host.example", [], ["10.0.0.1"])):
        assert scanner._get_hostname("10.0.0.1") == "host.example"
    with patch("socket.gethostbyaddr", side_effect=OSError):
        assert scanner._get_hostname("10.0.0.1") == ""


@pytest.mark.asyncio
async def test_scan_device_down_records_error():
    scanner = scanner_with(FakeNmap())
    device = await scanner.scan_device("10.0.0.1")

    assert not device.alive
    assert device.errors == ["Host is down"]


@pytest.mark.asyncio
async def test_scan_device_reports_services_and_hostname():
    host = make_host(tcp={22: {"state": "open"}}, udp={161: {"state": "open"}})
    scanner = scanner_with(FakeNmap({"10.0.0.1": host}))

    with (
        patch.object(scanner_module.os, "geteuid", return_value=0),
        patch.object(scanner, "_get_hostname", return_value="box.example"),
    ):
        device = await scanner.scan_device("10.0.0.1")

    assert device.alive
    assert device.ssh and device.snmp
    assert not device.mysql
    assert device.hostname == "box.example"
    assert device.errors == []


@pytest.mark.asyncio
async def test_scan_device_records_port_errors_and_hostname_failure():
    scanner = scanner_with(FakeNmap({"10.0.0.1": make_host()}))

    async def boom(ip, port):
        raise RuntimeError(f"bad {port}")

    with (
        patch.object(scanner_module.os, "geteuid", return_value=0),
        patch.object(scanner, "_check_port", side_effect=boom),
        patch.object(scanner, "_get_hostname", side_effect=OSError("no dns")),
    ):
        device = await scanner.scan_device("10.0.0.1")

    assert device.alive
    assert device.hostname == ""
    assert len(device.errors) == 3
    assert device.errors[0].startswith("Error checking port 22")


@pytest.mark.asyncio
async def test_scan_device_unexpected_error_is_captured():
    scanner = scanner_with(FakeNmap())
    with patch.object(scanner, "_check_alive", side_effect=RuntimeError("kaboom")):
        device = await scanner.scan_device("10.0.0.1")

    assert device.errors == ["Scan error: kaboom"]


@pytest.mark.asyncio
async def test_scan_network_expands_cidr_and_updates_progress():
    scanner = scanner_with(FakeNmap())
    seen = []

    async def fake_scan(ip):
        seen.append(ip)
        return Device(ip=ip)

    with patch.object(scanner, "scan_device", side_effect=fake_scan), Progress() as progress:
        devices = await scanner.scan_network("10.0.0.0/30", progress)

    assert sorted(seen) == ["10.0.0.1", "10.0.0.2"]
    assert len(devices) == 2
    assert progress.tasks[0].completed == 2


def test_save_csv_joins_errors(tmp_path):
    out = tmp_path / "out.csv"
    save_csv([Device(ip="10.0.0.1", errors=["a", "b"])], out)

    assert "a; b" in out.read_text()


def test_print_results_no_alive_hosts(capsys):
    print_results([Device(ip="10.0.0.1")])
    assert "No alive hosts found" in capsys.readouterr().out


def test_print_results_summary(capsys):
    print_results([Device(ip="10.0.0.1", alive=True, ssh=True, mysql=True, hostname="db")])
    out = capsys.readouterr().out

    assert "10.0.0.1" in out
    assert "SSH servers: 1" in out
    assert "SNMP devices: 0" in out
    assert "MySQL servers: 1" in out


runner = CliRunner()


def patched_scanner(devices):
    scanner = MagicMock()

    async def scan_network(network, progress=None):
        return devices

    scanner.scan_network = scan_network
    return patch.object(cli, "NetworkScanner", return_value=scanner)


def test_cli_version():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "v2.0.0" in result.output


@pytest.mark.parametrize(
    ("args", "suffix"),
    [(["-o"], ".json"), (["-o"], ".csv"), (["-o"], ".txt"), (["-f", "csv", "-o"], ".json")],
)
def test_cli_scan_writes_report(tmp_path, args, suffix):
    out = tmp_path / f"report{suffix}"
    with patched_scanner([Device(ip="10.0.0.1", alive=True)]):
        result = runner.invoke(app, ["scan", "10.0.0.1", "--quiet", "--verbose", *args, str(out)])

    assert result.exit_code == 0, result.output
    text = out.read_text()
    if suffix == ".csv" or "csv" in args:
        assert text.startswith("ip,alive")
    else:
        assert json.loads(text)[0]["ip"] == "10.0.0.1"


def test_cli_scan_prints_table_without_output_file():
    with patched_scanner([Device(ip="10.0.0.1", alive=True, ssh=True)]):
        result = runner.invoke(app, ["scan", "10.0.0.1"])

    assert result.exit_code == 0
    assert "10.0.0.1" in result.output


@pytest.mark.parametrize(
    "target", ["127.0.0.1", "::1", "example.com", "host-1.lab.example", "localhost"]
)
def test_validate_target_accepts(target):
    assert netprobe.validate_target(target) == target


@pytest.mark.parametrize(
    "target",
    [
        "",
        "-oN/tmp/out",
        "--script=banner",
        "host name",
        "a;b",
        "999.999.999.999",
        "1.2.3",
        "-bad.example",
        "bad-.example",
        "a" * 64 + ".example",
        ("a." * 130) + "com",
    ],
)
def test_validate_target_rejects(target):
    with pytest.raises(ValueError, match="Invalid target"):
        netprobe.validate_target(target)


@pytest.mark.asyncio
async def test_scan_device_rejects_option_like_target_without_running_nmap():
    scanner = scanner_with(FakeNmap())
    device = await scanner.scan_device("--script=banner")

    assert not device.alive
    assert "Invalid target" in device.errors[0]
    assert scanner.nm.scans == []


@pytest.mark.asyncio
async def test_scan_network_rejects_option_like_target():
    with pytest.raises(ValueError, match="Invalid network format"):
        await scanner_with(FakeNmap()).scan_network("-sS")


@pytest.mark.asyncio
async def test_scan_network_rejects_oversized_network():
    with pytest.raises(ValueError, match="Network too large"):
        await scanner_with(FakeNmap()).scan_network("10.0.0.0/8")


@pytest.mark.asyncio
async def test_scan_network_accepts_largest_allowed_network():
    scanner = scanner_with(FakeNmap())

    async def fake_scan(ip):
        return Device(ip)

    with patch.object(scanner, "scan_device", side_effect=fake_scan):
        devices = await scanner.scan_network("10.0.0.0/16")

    assert len(devices) == 65534


class PerCallPortScanner:
    """Fake nmap whose result lives on the instance, like python-nmap's PortScanner."""

    # Both scans must have written before either returns, so a shared instance
    # always shows the last write to whichever caller reads second.
    barrier = threading.Barrier(2, timeout=5)

    def __init__(self):
        self.open_port = None

    def scan(self, hosts=None, arguments=None):
        self.open_port = int(arguments.split("-p ")[1].split()[0])
        self.barrier.wait()

    def all_hosts(self):
        return ["10.0.0.1"]

    def __getitem__(self, ip):
        host = MagicMock()
        host.get.return_value = {self.open_port: {"state": "open"}}
        return host


@pytest.mark.asyncio
async def test_concurrent_port_checks_do_not_share_scan_state():
    """Each port must be judged from its own nmap result, not the last one written."""
    scanner = NetworkScanner.__new__(NetworkScanner)
    scanner._new_scanner = PerCallPortScanner

    results = await asyncio.gather(
        scanner._check_port("10.0.0.1", 22),
        scanner._check_port("10.0.0.1", 3306),
    )

    assert results == [True, True]


@pytest.mark.asyncio
async def test_udp_check_uses_udp_scan_and_results():
    fake = FakeNmap({"10.0.0.1": make_host(udp={161: {"state": "open"}})})
    scanner = scanner_with(fake)

    assert await scanner._check_port("10.0.0.1", 161, "udp") is True
    assert fake.scans[0][1].startswith("-sU -p 161")
    assert await scanner._check_port("10.0.0.1", 161, "tcp") is False


@pytest.mark.asyncio
async def test_snmp_skipped_without_root():
    scanner = scanner_with(FakeNmap({"10.0.0.1": make_host(tcp={22: {"state": "open"}})}))

    with (
        patch.object(scanner_module.os, "geteuid", return_value=1000),
        patch.object(scanner, "_get_hostname", return_value=""),
    ):
        device = await scanner.scan_device("10.0.0.1")

    assert device.ssh
    assert not device.snmp
    assert "SNMP check skipped: UDP scan requires root" in device.errors
    assert all("-sU" not in args for _, args in scanner.nm.scans)


def test_hostname_target_matches_single_result_by_ip():
    scanner = scanner_with(FakeNmap({"93.184.216.34": make_host("up")}))

    assert scanner._check_alive("example.com") is True


def test_ip_target_never_falls_back_to_a_different_host():
    scanner = scanner_with(FakeNmap({"10.0.0.9": make_host("up")}))

    assert scanner._check_alive("10.0.0.1") is False


def test_cli_invalid_network_exits_2_with_message():
    result = runner.invoke(app, ["scan", "999.1.1.1/24"])

    assert result.exit_code == 2
    assert "Invalid network format" in result.output
    assert "Traceback" not in result.output


def test_cli_missing_nmap_exits_1():
    with patch.object(
        cli, "NetworkScanner", side_effect=cli.nmap.PortScannerError("nmap not found")
    ):
        result = runner.invoke(app, ["scan", "127.0.0.1"])

    assert result.exit_code == 1
    assert "nmap is not available" in result.output


def test_cli_unwritable_output_exits_1(tmp_path):
    out = tmp_path / "missing-dir" / "report.json"
    with patched_scanner([Device(ip="10.0.0.1", alive=True)]):
        result = runner.invoke(app, ["scan", "10.0.0.1", "--quiet", "-o", str(out)])

    assert result.exit_code == 1
    assert "cannot write" in result.output
