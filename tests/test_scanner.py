import asyncio
import sys
import types
from typing import ClassVar
from unittest.mock import patch

import pytest
from conftest import closed_port, fixture_bytes
from rich.progress import Progress

from netprobe import probes, scanner
from netprobe.models import Device, ServiceSpec
from netprobe.probes import ProbeResult, SnmpCredentials
from netprobe.scanner import BackendUnavailableError, NetworkScanner


async def lab_services(tcp_server, udp_server, *, ssh=True, mysql=False, snmp=False):
    """ServiceSpecs pointing at local servers instead of the well-known ports."""
    ssh_port = await tcp_server(fixture_bytes("ssh-banner.bin")) if ssh else closed_port()
    mysql_port = (
        await tcp_server(fixture_bytes("mariadb-handshake.bin")) if mysql else closed_port()
    )
    if snmp:
        snmp_port, _ = await udp_server(fixture_bytes("snmpv3-report.bin"))
    else:
        snmp_port, _ = await udp_server(b"")
    return [
        ServiceSpec("ssh", ssh_port, "tcp", "ssh"),
        ServiceSpec("snmp", snmp_port, "udp", "snmp"),
        ServiceSpec("mysql", mysql_port, "tcp", "mysql"),
    ]


def stub_probes(monkeypatch, fn):
    """Replace every probe in the registry with fn(host, port, timeout) -> state."""

    async def probe(host, port, ctx):
        return ProbeResult(await fn(host, port, ctx.timeout))

    for name, (_, protocol) in list(probes.PROBES.items()):
        monkeypatch.setitem(probes.PROBES, name, (probe, protocol))


@pytest.fixture(autouse=True)
def no_reverse_dns(monkeypatch):
    async def fake(ip):
        return "box.example"

    monkeypatch.setattr(scanner, "resolve_hostname", fake)


async def test_scan_device_reports_services_and_legacy_flags(tcp_server, udp_server):
    services = await lab_services(tcp_server, udp_server, ssh=True, mysql=False, snmp=True)
    device = await NetworkScanner(services=services, timeout=0.5).scan_device("127.0.0.1")

    assert device.alive
    assert (device.ssh, device.snmp, device.mysql) == (True, True, False)
    assert device.hostname == "box.example"
    assert device.errors == []
    assert [(s.name, s.state, s.version) for s in device.services] == [
        ("ssh", "open", "OpenSSH_10.0"),
        ("snmp", "open", ""),
        ("mysql", "closed", ""),
    ]
    assert device.services[1].details == {"engine_id": "80001f88808aa1f93d7edcc66a00000000"}


async def test_closed_ports_still_mean_alive():
    services = [ServiceSpec("ssh", closed_port())]
    device = await NetworkScanner(services=services).scan_device("127.0.0.1")

    assert device.alive
    assert not device.ssh


async def test_no_answer_means_down(monkeypatch):
    async def silent(host, port, timeout):
        return "filtered"

    stub_probes(monkeypatch, silent)
    device = await NetworkScanner(services=[ServiceSpec("ssh", 22)]).scan_device("10.0.0.1")

    assert not device.alive
    assert device.hostname == ""
    assert device.errors == ["Host is down"]


async def test_probe_exception_is_recorded(monkeypatch):
    async def boom(host, port, timeout):
        raise RuntimeError("bad socket")

    stub_probes(monkeypatch, boom)
    device = await NetworkScanner(services=[ServiceSpec("ssh", 22)]).scan_device("10.0.0.1")

    assert device.errors[0] == "Error checking port 22: bad socket"
    assert device.services[0].state == "filtered"


async def test_probe_budget_stops_a_stalled_probe(monkeypatch):
    async def stalls(host, port, timeout):
        await asyncio.sleep(60)

    stub_probes(monkeypatch, stalls)
    scanner_ = NetworkScanner(services=[ServiceSpec("ssh", 22)], timeout=0.05)
    device = await scanner_.scan_device("10.0.0.1")

    assert device.errors[0] == "Error checking port 22: probe timed out"
    assert device.services[0].state == "filtered"


async def test_probe_errors_are_redacted(monkeypatch):
    async def leaky(host, port, timeout):
        raise RuntimeError("community s3cret-c rejected")

    stub_probes(monkeypatch, leaky)
    scanner_ = NetworkScanner(
        services=[ServiceSpec("snmp", 161, "udp", "snmp")],
        snmp=SnmpCredentials(community="s3cret-c"),
    )
    device = await scanner_.scan_device("10.0.0.1")

    assert device.errors[0] == "Error checking port 161: community *** rejected"


async def test_probe_cap_counts_hosts_times_services():
    services = [ServiceSpec(f"tcp-{p}", p) for p in range(1, 10)]
    prepared_argument_0 = NetworkScanner(services=services)
    with pytest.raises(ValueError, match="Scan too large: 65534 hosts x 9 services"):
        await prepared_argument_0.scan_network("10.0.0.0/16")


async def test_probe_cap_also_applies_to_nmap_backend(fake_nmap):
    services = [ServiceSpec(f"tcp-{p}", p) for p in range(1, 10)]
    prepared_argument_0 = NetworkScanner(backend="nmap", services=services)
    with pytest.raises(ValueError, match="Scan too large"):
        await prepared_argument_0.scan_network("10.0.0.0/16")
    assert FakePortScanner.calls == []  # refused before nmap ran


async def test_scan_device_rejects_option_like_target():
    device = await NetworkScanner().scan_device("--script=banner")

    assert not device.alive
    assert "Invalid target" in device.errors[0]
    assert device.services == []


@pytest.mark.parametrize(
    ("kwargs", "message"), [({"concurrency": 0}, "concurrency"), ({"timeout": 0}, "timeout")]
)
def test_scanner_rejects_bad_limits(kwargs, message):
    with pytest.raises(ValueError, match=message):
        NetworkScanner(**kwargs)


async def test_scan_network_expands_cidr_and_updates_progress(monkeypatch):
    seen = []

    async def fake_scan(self, ip, **kwargs):
        seen.append(ip)
        return Device(ip=ip)

    monkeypatch.setattr(NetworkScanner, "scan_device", fake_scan)
    with Progress() as progress:
        devices = await NetworkScanner().scan_network("10.0.0.0/30", progress)

    assert sorted(seen) == ["10.0.0.1", "10.0.0.2"]
    assert [d.ip for d in devices] == ["10.0.0.1", "10.0.0.2"]
    assert progress.tasks[0].completed == 2


async def test_scan_network_single_localhost(tcp_server, udp_server):
    services = await lab_services(tcp_server, udp_server)
    devices = await NetworkScanner(services=services).scan_network("127.0.0.1")

    assert len(devices) == 1
    assert devices[0].alive
    assert devices[0].ssh


@pytest.mark.parametrize(
    ("network", "message"),
    [
        ("999.999.999.999/24", "Invalid network format"),
        ("-sS", "Invalid network format"),
        ("10.0.0.0/8", "Network too large"),
    ],
)
async def test_scan_network_rejects_bad_targets(network, message):
    prepared_argument_0 = NetworkScanner()
    with pytest.raises(ValueError, match=message):
        await prepared_argument_0.scan_network(network)


async def test_scan_network_accepts_largest_allowed_network(monkeypatch):
    async def fake_scan(self, ip, **kwargs):
        return Device(ip)

    monkeypatch.setattr(NetworkScanner, "scan_device", fake_scan)
    devices = await NetworkScanner().scan_network("10.0.0.0/16")

    assert len(devices) == 65534


@pytest.mark.parametrize(
    "target", ["127.0.0.1", "::1", "example.com", "host-1.lab.example", "localhost"]
)
def test_validate_target_accepts(target):
    assert scanner.validate_target(target) == target


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
        scanner.validate_target(target)


async def test_resolve_hostname(monkeypatch):
    monkeypatch.undo()  # drop the autouse stub for this test
    with patch("socket.gethostbyaddr", return_value=("host.example", [], ["10.0.0.1"])):
        assert await scanner.resolve_hostname("10.0.0.1") == "host.example"
    with patch("socket.gethostbyaddr", side_effect=OSError):
        assert await scanner.resolve_hostname("10.0.0.1") == ""


# --- nmap backend: python-nmap is the system boundary, replaced by a fake module.


class FakeHost:
    def __init__(self, state):
        self._state = state

    def state(self):
        return self._state


class FakePortScanner:
    hosts: ClassVar[dict[str, str]] = {}
    calls: ClassVar[list[tuple[str, str]]] = []

    def scan(self, hosts, arguments, timeout=None):
        self.calls.append((hosts, arguments))

    def all_hosts(self):
        return list(self.hosts)

    def __getitem__(self, ip):
        return FakeHost(self.hosts[ip])


@pytest.fixture
def fake_nmap(monkeypatch):
    module = types.ModuleType("nmap")
    module.PortScanner = FakePortScanner
    module.PortScannerError = type("PortScannerError", (Exception,), {})
    FakePortScanner.hosts = {}
    FakePortScanner.calls = []
    monkeypatch.setitem(sys.modules, "nmap", module)
    return module


async def test_nmap_backend_only_probes_swept_hosts(fake_nmap, monkeypatch):
    monkeypatch.setattr(FakePortScanner, "hosts", {"10.0.0.1": "up", "10.0.0.2": "down"})
    probed = []

    async def closed(host, port, timeout):
        probed.append(host)
        return "filtered"

    stub_probes(monkeypatch, closed)
    devices = await NetworkScanner(backend="nmap").scan_network("10.0.0.0/30")

    assert [d.alive for d in devices] == [True, False]
    assert devices[0].errors == []
    assert devices[1].errors == ["Host is down"]
    assert set(probed) == {"10.0.0.1"}
    assert FakePortScanner.calls[-1] == ("10.0.0.0/30", "-sn -T4 --host-timeout 30s")


async def test_nmap_backend_hostname_target_matches_by_ip(fake_nmap, monkeypatch):
    monkeypatch.setattr(FakePortScanner, "hosts", {"93.184.216.34": "up"})

    async def filtered(host, port, timeout):
        return "filtered"

    stub_probes(monkeypatch, filtered)
    devices = await NetworkScanner(backend="nmap").scan_network("example.com")

    assert devices[0].alive


def test_host_key_never_falls_back_to_a_different_ip():
    assert scanner._host_key(["10.0.0.9"], "10.0.0.1") is None
    assert scanner._host_key(["10.0.0.9"], "10.0.0.9") == "10.0.0.9"
    assert scanner._host_key(["10.0.0.9", "10.0.0.8"], "name.example") is None


def test_nmap_backend_without_python_nmap(monkeypatch):
    monkeypatch.setitem(sys.modules, "nmap", None)
    with pytest.raises(BackendUnavailableError, match="netprobe\\[nmap\\]"):
        NetworkScanner(backend="nmap")


def test_nmap_backend_without_binary(fake_nmap, monkeypatch):
    def missing():
        raise fake_nmap.PortScannerError("nmap program was not found in path")

    monkeypatch.setattr(fake_nmap, "PortScanner", missing)
    with pytest.raises(BackendUnavailableError, match="nmap is not available"):
        NetworkScanner(backend="nmap")
