# SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

import asyncio
import errno
import json
import shutil
import socket
import sys
import threading
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
    async def fake(ip, lookups=None):
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

    assert device.errors == ["Error checking port 22: bad socket"]
    assert device.services[0].state == "unknown"
    assert not device.alive


async def test_probe_budget_stops_a_stalled_probe(monkeypatch):
    async def stalls(host, port, timeout):
        await asyncio.sleep(60)

    stub_probes(monkeypatch, stalls)
    scanner_ = NetworkScanner(services=[ServiceSpec("ssh", 22)], timeout=0.05)
    device = await scanner_.scan_device("10.0.0.1")

    assert device.errors == ["Error checking port 22: probe timed out"]
    assert device.services[0].state == "unknown"


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
    assert fake_nmap.calls == []  # refused before nmap ran


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
        "example.com\n",
        "host\n.example",
        "a.b\n",
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


# --- nmap backend: the nmap executable is the system boundary, replaced by a
# script that records its argv and prints canned XML.

FAKE_NMAP = """\
import json, os, sys, time
with open(os.environ["FAKE_NMAP_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
time.sleep(float(os.environ.get("FAKE_NMAP_SLEEP", "0")))
up = json.loads(os.environ.get("FAKE_NMAP_UP", "[]"))
hosts = "".join(
    f'<host><status state="up"/><address addr="{a}" addrtype="ipv4"/></host>' for a in up
)
sys.stdout.write(os.environ.get("FAKE_NMAP_XML") or f"<nmaprun>{hosts}</nmaprun>")
sys.exit(int(os.environ.get("FAKE_NMAP_EXIT", "0")))
"""


class FakeNmap:
    def __init__(self, tmp_path, monkeypatch):
        self.log = tmp_path / "nmap-calls.jsonl"
        self.monkeypatch = monkeypatch
        script = tmp_path / "nmap"
        script.write_text(f"#!{sys.executable}\n{FAKE_NMAP}")
        script.chmod(0o755)
        monkeypatch.setattr(scanner.shutil, "which", lambda name: str(script))
        monkeypatch.setenv("FAKE_NMAP_LOG", str(self.log))
        self.up([])

    def up(self, addresses):
        self.monkeypatch.setenv("FAKE_NMAP_UP", json.dumps(addresses))

    def set(self, name, value):
        self.monkeypatch.setenv(f"FAKE_NMAP_{name}", value)

    @property
    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text().splitlines()]


@pytest.fixture
def fake_nmap(tmp_path, monkeypatch):
    return FakeNmap(tmp_path, monkeypatch)


SWEEP = ["-sn", "-T4", "--host-timeout", "30s", "-oX", "-"]


async def test_nmap_backend_only_probes_swept_hosts(fake_nmap, monkeypatch):
    fake_nmap.up(["10.0.0.1"])
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
    assert fake_nmap.calls == [[*SWEEP, "10.0.0.0/30"]]


async def test_nmap_backend_hostname_target_matches_by_ip(fake_nmap, monkeypatch):
    fake_nmap.up(["93.184.216.34"])

    async def filtered(host, port, timeout):
        return "filtered"

    def fake_getaddrinfo(host, port, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]

    stub_probes(monkeypatch, filtered)
    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)
    devices = await NetworkScanner(backend="nmap").scan_network("example.com")

    assert devices[0].alive
    assert fake_nmap.calls == [[*SWEEP, "example.com"]]


async def test_nmap_full_prefix_is_one_process_with_scaled_deadline(fake_nmap, monkeypatch):
    deadlines = []
    real = scanner._run_nmap

    async def spy(executable, hosts, ipv6, deadline):
        deadlines.append(deadline)
        return await real(executable, hosts, ipv6, deadline)

    monkeypatch.setattr(scanner, "_run_nmap", spy)
    network = "10.0.0.0/23"
    targets = scanner.expand_targets(network)
    assert len(targets) == 510
    await scanner.nmap_sweep(targets, network)
    assert fake_nmap.calls == [[*SWEEP, network]]
    assert deadlines == [70]


async def test_nmap_partial_lists_stay_in_fixed_batches(fake_nmap):
    network = "10.0.0.0/23"
    targets = scanner.expand_targets(network)[:-1]
    await scanner.nmap_sweep(targets, network)
    calls = fake_nmap.calls
    assert [len(call) - len(SWEEP) for call in calls] == [256, 253]
    assert all("/" not in arg for call in calls for arg in call[len(SWEEP) :])


async def test_nmap_ipv6_targets_add_the_ipv6_flag(fake_nmap):
    await scanner.nmap_sweep(["::1"], "::/126")
    assert fake_nmap.calls == [["-6", *SWEEP, "::1"]]


async def test_nmap_deadline_is_an_error_not_host_down(fake_nmap, monkeypatch):
    fake_nmap.set("SLEEP", "5")
    monkeypatch.setattr(scanner, "NMAP_TIMEOUT", 0.3)
    with pytest.raises(BackendUnavailableError, match=r"no result within 0\.3s"):
        await scanner.nmap_sweep(["127.0.0.1"], "127.0.0.1")


async def test_nmap_failure_status_is_an_error(fake_nmap):
    fake_nmap.set("EXIT", "1")
    with pytest.raises(BackendUnavailableError, match="exited with status 1"):
        await scanner.nmap_sweep(["127.0.0.1"], "127.0.0.1")


async def test_nmap_oversized_output_is_refused(fake_nmap, monkeypatch):
    monkeypatch.setattr(scanner, "NMAP_MAX_OUTPUT", 64)
    fake_nmap.up([f"10.0.0.{i}" for i in range(1, 9)])
    with pytest.raises(BackendUnavailableError, match="exceeded 64 bytes"):
        await scanner.nmap_sweep(["10.0.0.1"], "10.0.0.1")


@pytest.mark.parametrize(
    "document",
    [
        b"not xml",
        b'<?xml version="1.0"?><!DOCTYPE r [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;&a;&a;">]>'
        b"<nmaprun>&b;</nmaprun>",
        b'<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
        b"<nmaprun>&x;</nmaprun>",
    ],
)
def test_nmap_xml_parser_rejects_malformed_and_entity_documents(document):
    with pytest.raises(BackendUnavailableError, match="unreadable XML"):
        scanner.parse_nmap_hosts(document)


def test_nmap_xml_parser_reads_only_up_hosts():
    document = (
        b"<nmaprun>"
        b'<host><status state="up"/><address addr="aa:bb:cc:dd:ee:ff" addrtype="mac"/>'
        b'<address addr="10.0.0.1" addrtype="ipv4"/></host>'
        b'<host><status state="down"/><address addr="10.0.0.2" addrtype="ipv4"/></host>'
        b'<host><address addr="10.0.0.3" addrtype="ipv4"/></host>'
        b'<host><status state="up"/><address addr="::1" addrtype="ipv6"/></host>'
        b"</nmaprun>"
    )
    assert scanner.parse_nmap_hosts(document) == ["10.0.0.1", "::1"]


def test_nmap_backend_needs_the_executable(monkeypatch):
    monkeypatch.setattr(scanner.shutil, "which", lambda name: None)
    with pytest.raises(BackendUnavailableError, match="no nmap executable"):
        NetworkScanner(backend="nmap")


@pytest.mark.skipif(shutil.which("nmap") is None, reason="nmap not installed")
async def test_real_nmap_sweep_of_loopback():
    assert await scanner.nmap_sweep(["127.0.0.1"], "127.0.0.1") == {"127.0.0.1"}


async def test_service_budget_replaces_the_scan_timeout(monkeypatch):
    seen: list[float] = []

    async def grab(host, port, timeout):
        seen.append(timeout)
        return "closed"

    stub_probes(monkeypatch, grab)
    await NetworkScanner(
        timeout=1.0,
        services=[
            ServiceSpec("ssh", 22, "tcp", "ssh", 0.3),
            ServiceSpec("https", 443, "tcp", "https"),
        ],
    ).scan_device("127.0.0.1")
    assert seen == [0.3, 1.0]


def test_host_key_never_falls_back_to_a_different_ip():
    assert scanner._host_key(["10.0.0.9"], "10.0.0.1") is None
    assert scanner._host_key(["10.0.0.9"], "10.0.0.9") == "10.0.0.9"
    assert scanner._host_key(["10.0.0.9", "10.0.0.8"], "name.example") is None


async def test_local_socket_exhaustion_is_unknown_not_down(monkeypatch):
    async def exhausted(host, port, **kwargs):
        raise OSError(errno.EMFILE, "Too many open files")

    monkeypatch.setattr(asyncio, "open_connection", exhausted)
    device = await NetworkScanner(services=[ServiceSpec("ssh", 22, "tcp", "ssh")]).scan_device(
        "10.0.0.1"
    )

    assert device.services[0].state == "unknown"
    assert not device.alive
    assert device.errors == ["Error checking port 22: [Errno 24] Too many open files"]


async def test_unknown_probe_does_not_hide_an_answer(monkeypatch):
    async def mixed(host, port, timeout):
        if port == 22:
            raise RuntimeError("bad socket")
        return "closed"

    stub_probes(monkeypatch, mixed)
    services = [ServiceSpec("ssh", 22), ServiceSpec("http", 80)]
    device = await NetworkScanner(services=services).scan_device("10.0.0.1")

    assert device.alive
    assert [s.state for s in device.services] == ["unknown", "closed"]


def test_file_limit_is_raised_toward_the_hard_limit(monkeypatch):
    import resource

    calls = []
    monkeypatch.setattr(resource, "getrlimit", lambda kind: (256, 4096))
    monkeypatch.setattr(resource, "setrlimit", lambda kind, limits: calls.append(limits))

    scanner.ensure_file_limit(256)

    assert calls == [(256 + scanner.FD_HEADROOM, 4096)]


def test_file_limit_refuses_concurrency_beyond_the_hard_limit(monkeypatch):
    import resource

    calls = []
    monkeypatch.setattr(resource, "getrlimit", lambda kind: (256, 300))
    monkeypatch.setattr(resource, "setrlimit", lambda kind, limits: calls.append(limits))

    with pytest.raises(ValueError, match=r"--concurrency 256 needs 320 open files .* 300"):
        scanner.ensure_file_limit(256)
    assert calls == [(300, 300)]


async def test_scan_network_checks_the_file_limit_before_probing(monkeypatch):
    import resource

    monkeypatch.setattr(resource, "getrlimit", lambda kind: (64, 64))
    monkeypatch.setattr(resource, "setrlimit", pytest.fail)
    probed = []

    async def never(host, port, timeout):
        probed.append(host)
        return "open"

    stub_probes(monkeypatch, never)
    scanner_ = NetworkScanner(services=[ServiceSpec("ssh", 22)], concurrency=16)
    with pytest.raises(ValueError, match="open files"):
        await scanner_.scan_network("10.0.0.1")
    assert probed == []


async def test_hostname_target_is_resolved_once_and_pinned(monkeypatch):
    lookups = []

    def fake_getaddrinfo(host, port, **kwargs):
        lookups.append(host)
        # A rebinding answer would differ on the next lookup; only the first is used.
        address = "192.0.2.10" if len(lookups) == 1 else "127.0.0.1"
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 0))]

    seen = []

    async def probe(host, port, ctx):
        seen.append((host, ctx.server_name))
        return ProbeResult("closed")

    for name, (_, protocol) in list(probes.PROBES.items()):
        monkeypatch.setitem(probes.PROBES, name, (probe, protocol))
    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)
    services = [ServiceSpec("ssh", 22), ServiceSpec("http", 80), ServiceSpec("https", 443)]
    device = await NetworkScanner(services=services).scan_device("web.example")

    assert lookups == ["web.example"]
    assert seen == [("192.0.2.10", "web.example")] * 3
    assert device.ip == "web.example"
    assert device.address == "192.0.2.10"


async def test_unresolvable_hostname_is_unknown_not_down(monkeypatch):
    def fail(host, port, **kwargs):
        raise socket.gaierror(socket.EAI_NONAME, "Name or service not known")

    monkeypatch.setattr(socket, "getaddrinfo", fail)
    device = await NetworkScanner(services=[ServiceSpec("ssh", 22)]).scan_device("gone.example")

    assert [s.state for s in device.services] == ["unknown"]
    assert device.errors == [
        f"Cannot resolve gone.example: [Errno {socket.EAI_NONAME}] Name or service not known"
    ]
    assert not device.alive


@pytest.mark.parametrize(
    ("ptr", "expected"),
    [
        ("host.example.", "host.example"),
        ("_gateway", "_gateway"),
        ("xn--hst-cna.example", "xn--hst-cna.example"),
        ("h\u00f4st.example", ""),
        ("evil\x1b[2Jname", ""),
        ("[bold]x[/bold]", ""),
        ("a" * 300, ""),
    ],
)
async def test_reverse_dns_names_are_plain_hostnames(monkeypatch, ptr, expected):
    monkeypatch.undo()  # drop the autouse stub for this test
    with patch("socket.gethostbyaddr", return_value=(ptr, [], ["10.0.0.1"])):
        assert await scanner.resolve_hostname("10.0.0.1") == expected


async def test_reverse_dns_deadline_starts_after_a_lookup_slot_frees(monkeypatch):
    monkeypatch.undo()
    # Three serial lookups take 1.2s against a 1.0s deadline: a deadline that
    # included queueing would expire the third, while each lookup alone
    # leaves 0.6s of slack for slow CI thread scheduling.
    monkeypatch.setattr(scanner, "HOSTNAME_TIMEOUT", 1.0)

    def slow(ip):
        import time

        time.sleep(0.4)
        return ("host.example", [], [ip])

    monkeypatch.setattr(socket, "gethostbyaddr", slow)
    one_slot = asyncio.Semaphore(1)
    names = await asyncio.gather(
        *(scanner.resolve_hostname("10.0.0.1", one_slot) for _ in range(3))
    )

    assert names == ["host.example"] * 3


async def test_expired_lookup_keeps_its_slot_until_the_resolver_returns(monkeypatch):
    import threading

    monkeypatch.undo()
    monkeypatch.setattr(scanner, "HOSTNAME_TIMEOUT", 0.1)
    release = threading.Event()

    def stuck(ip):
        release.wait(5)
        return ("late.example", [], [ip])

    monkeypatch.setattr(socket, "gethostbyaddr", stuck)
    one_slot = asyncio.Semaphore(1)

    assert await scanner.resolve_hostname("10.0.0.1", one_slot) == ""
    assert one_slot.locked()  # the resolver thread is still running
    release.set()
    async with asyncio.timeout(5):
        while one_slot.locked():
            await asyncio.sleep(0.01)


def finishes_within(seconds, run):
    """Run a blocking call on a thread; True if it returned in time."""
    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    worker.join(seconds)
    return not worker.is_alive()


@pytest.fixture
def hung_resolver(monkeypatch):
    """Make reverse and forward lookups block until the test ends."""
    monkeypatch.undo()  # drop the autouse reverse DNS stub
    release = threading.Event()

    def hang(*args, **kwargs):
        release.wait(30)
        raise OSError("released")

    monkeypatch.setattr(socket, "gethostbyaddr", hang)
    monkeypatch.setattr(socket, "getaddrinfo", hang)
    yield
    release.set()


@pytest.mark.parametrize("target", ["127.0.0.1", "stuck.example"])
def test_abandoned_lookups_do_not_hold_the_event_loop_open(hung_resolver, monkeypatch, target):
    # 127.0.0.1 answers closed, so its reverse lookup runs; the name hangs in getaddrinfo.
    monkeypatch.setattr(scanner, "HOSTNAME_TIMEOUT", 0.1)
    scanner_ = NetworkScanner(services=[ServiceSpec("ssh", closed_port())])
    devices = []

    def run():
        devices.append(asyncio.run(scanner_.scan_device(target)))

    assert finishes_within(3, run)
    assert devices[0].hostname == ""


def test_cli_deadline_bounds_wall_time_with_a_hung_resolver(hung_resolver, monkeypatch, tmp_path):
    from typer.testing import CliRunner

    from netprobe import cli

    monkeypatch.setattr(scanner, "HOSTNAME_TIMEOUT", 60)
    report = tmp_path / "report.json"
    outcome = []
    arguments = ["scan", "stuck.example", "--deadline", "1", "-q", "-o", str(report)]

    def run():
        outcome.append(CliRunner().invoke(cli.app, arguments))

    assert finishes_within(4, run)
    assert outcome[0].exit_code == cli.EXIT_INCOMPLETE
    assert json.loads(report.read_text())["complete"] is False


async def test_deadline_stops_the_scan_and_keeps_finished_hosts(monkeypatch):
    async def first_fast(host, port, timeout):
        if host != "10.0.0.1":
            await asyncio.sleep(30)
        return "open"

    stub_probes(monkeypatch, first_fast)
    scanner_ = NetworkScanner(
        services=[ServiceSpec("ssh", 22, timeout=30)], concurrency=1, deadline=0.3
    )
    loop = asyncio.get_running_loop()
    started = loop.time()
    with pytest.raises(scanner.ScanDeadlineError, match=r"0\.3s deadline") as caught:
        await scanner_.scan_network("10.0.0.0/30")

    assert loop.time() - started < 5
    assert [d.ip for d in caught.value.devices] == ["10.0.0.1"]


async def test_deadline_covers_the_nmap_sweep(fake_nmap):
    fake_nmap.set("SLEEP", "20")
    scanner_ = NetworkScanner(backend="nmap", deadline=0.5)
    loop = asyncio.get_running_loop()
    started = loop.time()
    with pytest.raises(scanner.ScanDeadlineError) as caught:
        await scanner_.scan_network("10.0.0.0/30")

    assert loop.time() - started < 5
    assert caught.value.devices == []


async def test_scan_without_deadline_runs_to_completion(monkeypatch):
    async def closed(host, port, timeout):
        return "closed"

    stub_probes(monkeypatch, closed)
    devices = await NetworkScanner(services=[ServiceSpec("ssh", 22)]).scan_network("10.0.0.0/30")
    assert [d.ip for d in devices] == ["10.0.0.1", "10.0.0.2"]


@pytest.mark.parametrize("deadline", [0, -1, float("inf"), float("nan")])
def test_deadline_must_be_positive_and_finite(deadline):
    with pytest.raises(ValueError, match="deadline must be positive"):
        NetworkScanner(deadline=deadline)
