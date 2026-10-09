# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Inventory history/profile/preflight regressions; no target scans."""

import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass, field
from unittest.mock import AsyncMock, MagicMock

import pytest
from typer.testing import CliRunner

from netprobe import cli, history
from netprobe import preflight as checks
from netprobe.cli import app
from netprobe.models import Device, Service
from netprobe.profiles import ConfigError, Profile, load_profiles
from netprobe.scanner import expand_targets, nmap_sweep


@dataclass
class Observation:
    ip: str
    alive: bool = False
    hostname: str = ""
    status: str = "unknown"
    port_states: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)


@pytest.fixture
def history_store(tmp_path):
    store = history.HistoryStore(tmp_path / "history.sqlite3")
    store.initialize()
    return store


def save_snapshot(store, devices, ports=None):
    from dataclasses import asdict

    metadata = {"ports": ["22/tcp"] if ports is None else ports, "schema_version": 1}
    return store.save(metadata, [asdict(device) for device in devices], history.utc_now())


def test_history_roundtrip_and_readonly_queries(history_store):
    first = save_snapshot(
        history_store, [Observation("127.0.0.1", hostname="värd", errors=["timeout"])]
    )
    second = save_snapshot(history_store, [Observation("127.0.0.1", alive=True, status="up")])
    snapshots = history_store.list_scans(1)
    assert [snapshot["id"] for snapshot in snapshots] == [second]
    snapshot = history_store.get(first)
    assert snapshot["devices"][0]["hostname"] == "värd"
    assert snapshot["devices"][0]["errors"] == ["timeout"]
    assert snapshot["started_at"].endswith("+00:00")
    assert history_store.get(second)["devices"][0]["alive"]
    with pytest.raises(ValueError, match="not found"):
        history_store.get(999)


def test_history_failed_serialization_does_not_write_partial_snapshot(history_store):
    prepared_argument_0 = object()
    prepared_argument_1 = history.utc_now()
    with pytest.raises(TypeError):
        history_store.save({"not_json": prepared_argument_0}, [], prepared_argument_1)
    assert history_store.list_scans() == []


def test_history_rejects_foreign_database_without_modifying_it(tmp_path):
    path = tmp_path / "other.sqlite3"
    with closing(sqlite3.connect(path)) as connection, connection:
        connection.execute("CREATE TABLE other (id INTEGER)")
    original = path.read_bytes()
    prepared_argument_0 = history.HistoryStore(path)
    with pytest.raises(ValueError, match="supported"):
        prepared_argument_0.initialize()
    assert path.read_bytes() == original


def test_history_read_command_never_creates_database(tmp_path):
    path = tmp_path / "missing.sqlite3"
    result = CliRunner().invoke(app, ["history", "--history", str(path)])
    assert result.exit_code == 1
    assert not path.exists()


def test_history_schema_version_rejected(history_store):
    with closing(sqlite3.connect(history_store.path)) as connection, connection:
        connection.execute("PRAGMA user_version = 99")
    with pytest.raises(ValueError, match="supported"):
        history_store.get(1)


def test_compare_port_changes_and_responsiveness(history_store):
    first = save_snapshot(
        history_store,
        [
            Observation("127.0.0.1", alive=True, status="up", port_states={"22/tcp": "closed"}),
            Observation("127.0.0.2", status="unresponsive", errors=["no response"]),
            Observation("127.0.0.3", alive=True, status="up", port_states={"22/tcp": "open"}),
        ],
    )
    second = save_snapshot(
        history_store,
        [
            Observation("127.0.0.1", alive=True, status="up", port_states={"22/tcp": "open"}),
            Observation("127.0.0.2", alive=True, status="up", port_states={"22/tcp": "closed"}),
            Observation("127.0.0.3", status="unresponsive", errors=["no response"]),
        ],
    )
    report = history.compare_scans(history_store.get(first), history_store.get(second))
    assert report["newly_responsive"] == ["127.0.0.2"]
    assert report["no_longer_responding"] == ["127.0.0.3"]
    assert report["uncertain_hosts"] == ["127.0.0.2", "127.0.0.3"]
    assert report["port_changes"] == [
        {"ip": "127.0.0.1", "port": "22/tcp", "before": "closed", "after": "open"}
    ]


def test_compare_errors_and_unknown_states_are_not_disappearances(history_store):
    first = save_snapshot(
        history_store,
        [Observation("127.0.0.1", alive=True, status="up", port_states={"22/tcp": "open"})],
    )
    second = save_snapshot(
        history_store,
        [
            Observation(
                "127.0.0.1", status="error", errors=["timeout"], port_states={"22/tcp": "unknown"}
            )
        ],
    )
    report = history.compare_scans(history_store.get(first), history_store.get(second))
    assert report["no_longer_responding"] == []
    assert report["newly_responsive"] == []
    assert report["port_changes"] == []
    assert report["uncertain_hosts"] == ["127.0.0.1"]


@pytest.mark.parametrize("changed", ["targets", "ports"])
def test_compare_different_scope_rejected(history_store, changed):
    first = save_snapshot(history_store, [Observation("127.0.0.1")])
    second = save_snapshot(
        history_store,
        [Observation("127.0.0.2" if changed == "targets" else "127.0.0.1")],
        ports=["443/tcp"] if changed == "ports" else None,
    )
    prepared_argument_0 = history_store.get(first)
    prepared_argument_1 = history_store.get(second)
    with pytest.raises(ValueError, match="different targets"):
        history.compare_scans(prepared_argument_0, prepared_argument_1)
    prepared_argument_0 = history_store.get(second)
    prepared_argument_1 = history_store.get(first)
    with pytest.raises(ValueError, match="Earlier scan"):
        history.compare_scans(prepared_argument_0, prepared_argument_1)


def test_compare_cannot_overwrite_history(history_store):
    first = save_snapshot(history_store, [Observation("127.0.0.1")])
    second = save_snapshot(history_store, [Observation("127.0.0.1")])
    result = CliRunner().invoke(
        app,
        [
            "compare",
            str(first),
            str(second),
            "--history",
            str(history_store.path),
            "-o",
            str(history_store.path),
        ],
    )
    assert result.exit_code == 1
    assert "overwrite" in result.output
    assert len(history_store.list_scans()) == 2


@pytest.mark.parametrize(
    "corruption", ["duplicate_ip", "unknown_port", "invalid_metadata", "bad_state"]
)
def test_corrupt_history_fails_closed(history_store, corruption):
    from dataclasses import asdict

    scan_id = save_snapshot(history_store, [Observation("127.0.0.1")])
    device = asdict(Observation("127.0.0.1"))
    devices, metadata = [device], {"ports": ["22/tcp"], "schema_version": 1}
    if corruption == "duplicate_ip":
        devices.append(device.copy())
    elif corruption == "unknown_port":
        device["port_states"] = {"443/tcp": "open"}
    elif corruption == "invalid_metadata":
        metadata["schema_version"] = 99
    else:
        device["port_states"] = {"22/tcp": "invented"}
    with closing(sqlite3.connect(history_store.path)) as connection, connection:
        connection.execute(
            "UPDATE scans SET devices=?, metadata=? WHERE id=?",
            (json.dumps(devices), json.dumps(metadata), scan_id),
        )
    with pytest.raises(ValueError):
        history_store.get(scan_id)


def test_history_summary_does_not_load_device_payload(history_store):
    scan_id = save_snapshot(history_store, [Observation("127.0.0.1", alive=True, status="up")])
    with closing(sqlite3.connect(history_store.path)) as connection, connection:
        connection.execute("UPDATE scans SET devices='invalid' WHERE id=?", (scan_id,))
    result = CliRunner().invoke(app, ["history", "--history", str(history_store.path)])
    assert result.exit_code == 0
    assert json.loads(result.output)[0]["responsive"] == 1
    with pytest.raises(ValueError):
        history_store.get(scan_id)


@pytest.fixture
def config(tmp_path):
    path = tmp_path / "profiles.toml"
    path.write_text("""[profiles.lab]
network = "127.0.0.0/29"
exclusions = ["127.0.0.2"]
services = "ssh"
ports = "ssh=2222"
concurrency = 2
timeout = 0.5
max_hosts = 8
""")
    return path


@pytest.fixture
def scanner(monkeypatch):
    mocked = MagicMock()
    mocked.scan_network = AsyncMock(return_value=[Device("127.0.0.1", alive=True)])
    factory = MagicMock(return_value=mocked)
    monkeypatch.setattr(cli, "NetworkScanner", factory)
    return mocked, factory


def test_profiles_and_cli_precedence(config, scanner):
    result = CliRunner().invoke(cli.app, ["profiles", "--config", str(config)])
    assert result.exit_code == 0
    assert json.loads(result.output)["lab"]["concurrency"] == 2
    _mocked, factory = scanner
    result = CliRunner().invoke(
        cli.app,
        [
            "scan",
            "127.0.0.0/29",
            "--profile",
            "lab",
            "--config",
            str(config),
            "--timeout",
            "0.8",
            "--exclude",
            "127.0.0.1",
            "-q",
        ],
    )
    assert result.exit_code == 0, result.output
    options = factory.call_args.kwargs
    assert options["timeout"] == 0.8
    assert options["concurrency"] == 2
    assert options["exclusions"] == ["127.0.0.2/32", "127.0.0.1"]
    assert options["services"][0].port == 2222


@pytest.mark.parametrize(
    "settings",
    [
        {"network": "bad"},
        {"network": "::1%en0"},
        {"network": "127.0.0.1", "concurrency": True},
        {"network": "127.0.0.1", "max_hosts": 0},
        {"network": "127.0.0.1", "backend": "shell"},
        {"network": "127.0.0.1", "timeout": float("nan")},
        {"network": "127.0.0.1", "timeout": "1"},
        {"network": "127.0.0.1", "services": []},
        {"network": "127.0.0.1", "exclusions": "127.0.0.1"},
        {"network": "127.0.0.1", "exclusions": ["hostname"]},
    ],
)
def test_profile_setting_validation(settings):
    with pytest.raises(ConfigError):
        Profile(**settings)


@pytest.mark.parametrize(
    "text",
    [
        "profiles=1",
        "[profiles.lab]\ntimeout=1",
        "[profiles.lab]\nnetwork='127.0.0.1'\nscript='x'",
        "[other]\na=1",
        "malformed=",
    ],
)
def test_bad_profile_config(tmp_path, text):
    path = tmp_path / "bad.toml"
    path.write_text(text)
    with pytest.raises(ConfigError):
        load_profiles(path)


def test_profile_scopes(config, scanner):
    for target in ("10.0.0.1", "::1", "example.com"):
        result = CliRunner().invoke(
            cli.app, ["scan", target, "--profile", "lab", "--config", str(config)]
        )
        assert result.exit_code == 2
    result = CliRunner().invoke(cli.app, ["scan", "--profile", "missing", "--config", str(config)])
    assert result.exit_code == 2
    scanner[1].assert_not_called()


def test_missing_target_and_default_profile_config(scanner, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert CliRunner().invoke(cli.app, ["scan"]).exit_code == 2
    assert CliRunner().invoke(cli.app, ["scan", "--profile", "absent"]).exit_code == 2
    assert CliRunner().invoke(cli.app, ["profiles"]).exit_code == 2
    scanner[1].assert_not_called()


def test_exclusion_target_expansion():
    assert expand_targets("127.0.0.0/29", exclusions=["127.0.0.2", "127.0.0.4/30"]) == [
        "127.0.0.1",
        "127.0.0.3",
    ]
    for args in [
        ("127.0.0.0/29", 2, []),
        ("127.0.0.1", 10, ["127.0.0.1"]),
        ("example.com", 10, ["127.0.0.1"]),
        ("::1%en0", 10, []),
    ]:
        with pytest.raises(ValueError):
            expand_targets(*args)


def test_preflight_no_traffic_and_no_database_creation(scanner, tmp_path):
    out = tmp_path / "report.json"
    out.write_text("existing")
    path = tmp_path / "history.sqlite3"
    result = CliRunner().invoke(
        cli.app, ["preflight", "127.0.0.1", "-o", str(out), "--history", str(path)]
    )
    assert result.exit_code == 0, result.output
    assert out.read_text() == "existing"
    assert not path.exists()
    scanner[1].assert_not_called()


def test_preflight_profile_and_failed_destination(config, scanner, tmp_path):
    result = CliRunner().invoke(cli.app, ["preflight", "--profile", "lab", "--config", str(config)])
    assert result.exit_code == 0
    assert json.loads(result.output)["host_count"] == 5
    result = CliRunner().invoke(
        cli.app, ["scan", "127.0.0.1", "-o", str(tmp_path / "missing" / "report.json")]
    )
    assert result.exit_code == 1
    scanner[1].assert_not_called()


def test_conflicting_destinations(config, scanner, history_store, tmp_path):
    alias = tmp_path / "alias.json"
    alias.hardlink_to(history_store.path)
    for args in [
        ["scan", "127.0.0.1", "-o", str(alias), "--history", str(history_store.path)],
        ["preflight", "--profile", "lab", "--config", str(config), "-o", str(config)],
    ]:
        result = CliRunner().invoke(cli.app, args)
        assert (
            result.exit_code == 2 and "different paths" in result.output
        ) or "overwrite" in result.output
    scanner[1].assert_not_called()


def test_missing_nmap_and_ca_stop_before_scanning(scanner, monkeypatch, tmp_path):
    monkeypatch.setattr(checks.shutil, "which", lambda _: None)
    result = CliRunner().invoke(cli.app, ["scan", "127.0.0.1", "--backend", "nmap"])
    assert result.exit_code == 1
    assert "requires" in result.output
    result = CliRunner().invoke(
        cli.app, ["scan", "127.0.0.1", "--tls-ca-file", str(tmp_path / "missing.pem")]
    )
    assert result.exit_code == 1
    assert "TLS CA" in result.output
    scanner[1].assert_not_called()


@pytest.mark.parametrize("failure", [None, "timeout", "error", "invalid"])
def test_nmap_version_preflight(monkeypatch, failure):
    monkeypatch.setattr(checks.shutil, "which", lambda _: "/mock/nmap")
    monkeypatch.setattr(checks.importlib.util, "find_spec", lambda _: object())

    def version(*args, **kwargs):
        if failure == "timeout":
            raise TimeoutError("nmap version deadline")
        if failure == "error":
            raise OSError("unavailable")
        if failure == "invalid":
            raise ValueError("Nmap version check failed")
        return "Nmap version 7.95"

    monkeypatch.setattr(checks, "nmap_version", version)
    result = CliRunner().invoke(cli.app, ["preflight", "127.0.0.1", "--backend", "nmap"])
    assert result.exit_code == (1 if failure else 0)


def test_history_cli_workflow(scanner, tmp_path):
    path = tmp_path / "history.sqlite3"
    mocked, _ = scanner
    mocked.scan_network.side_effect = [
        [Device("127.0.0.1", alive=True, services=[Service("ssh", 22, "tcp", "closed")])],
        [Device("127.0.0.1", alive=True, services=[Service("ssh", 22, "tcp", "open")])],
    ]
    runner = CliRunner()
    for _ in range(2):
        result = runner.invoke(
            cli.app, ["scan", "127.0.0.1", "--services", "ssh", "--history", str(path), "-q"]
        )
        assert result.exit_code == 0, result.output
    listed = runner.invoke(cli.app, ["history", "--history", str(path)])
    assert json.loads(listed.output)[0]["responsive"] == 1
    compared = runner.invoke(cli.app, ["compare", "1", "2", "--history", str(path)])
    assert compared.exit_code == 0
    assert json.loads(compared.output)["port_changes"][0]["after"] == "open"
    output = tmp_path / "changes.json"
    assert (
        runner.invoke(
            cli.app, ["compare", "1", "2", "--history", str(path), "-o", str(output)]
        ).exit_code
        == 0
    )
    assert json.loads(output.read_text())["port_changes"]
    assert (
        runner.invoke(
            cli.app, ["compare", "1", "2", "--history", str(path), "-o", str(path)]
        ).exit_code
        == 1
    )


def test_invalid_history_blocks_scan(scanner, tmp_path):
    path = tmp_path / "wrong.sqlite3"
    path.write_text("not a database")
    result = CliRunner().invoke(cli.app, ["scan", "127.0.0.1", "--history", str(path)])
    assert result.exit_code == 1
    assert "history schema" in result.output
    scanner[1].assert_not_called()


def test_nmap_exclusions_and_ipv6(monkeypatch):
    mocked = MagicMock()
    mocked.all_hosts.return_value = []
    monkeypatch.setattr("netprobe.scanner._nmap_scanner", lambda: mocked)
    nmap_sweep(["::1"], "::/126")
    assert mocked.scan.call_args.kwargs["hosts"] == "::1"
    assert mocked.scan.call_args.kwargs["arguments"].startswith("-6 ")
    assert mocked.scan.call_args.kwargs["timeout"] == 35


def test_nmap_timeout_is_an_error_not_host_down(monkeypatch):
    from netprobe.scanner import BackendUnavailableError

    mocked = MagicMock()
    mocked.scan.side_effect = TimeoutError("deadline")
    monkeypatch.setattr("netprobe.scanner._nmap_scanner", lambda: mocked)
    with pytest.raises(BackendUnavailableError, match="discovery failed"):
        nmap_sweep(["127.0.0.1"], "127.0.0.1")


async def test_bounded_workers_preserve_order(monkeypatch):
    import asyncio

    from netprobe.config import DEFAULT_SERVICES
    from netprobe.scanner import NetworkScanner

    engine = NetworkScanner(concurrency=2, services=DEFAULT_SERVICES[:1])
    active = peak = 0

    async def scan_device(ip, **kwargs):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.001)
        active -= 1
        return Device(ip)

    monkeypatch.setattr(engine, "scan_device", scan_device)
    devices = await engine.scan_network("127.0.0.0/29")
    assert [device.ip for device in devices] == expand_targets("127.0.0.0/29")
    assert peak == 2


async def test_cancelled_worker_cannot_return_partial_results(monkeypatch):
    import asyncio

    from netprobe.scanner import NetworkScanner

    engine = NetworkScanner()
    monkeypatch.setattr(engine, "scan_device", AsyncMock(side_effect=asyncio.CancelledError))
    with pytest.raises(asyncio.CancelledError):
        await engine.scan_network("127.0.0.1")


@pytest.mark.parametrize("failure", [None, "empty", "timeout"])
async def test_async_version_check_bounded_read_and_cleanup(monkeypatch, failure):
    process = MagicMock()
    process.stdout.read = AsyncMock(return_value=b"Nmap version 7.95\n")
    process.wait = AsyncMock(return_value=0)
    process.communicate = AsyncMock(return_value=(b"", b""))
    process.returncode = 0
    if failure == "empty":
        process.stdout.read.return_value = b""
    if failure == "timeout":
        process.returncode = None
        process.stdout.read.side_effect = TimeoutError
    factory = AsyncMock(return_value=process)
    monkeypatch.setattr(checks.asyncio, "create_subprocess_exec", factory)
    if failure:
        with pytest.raises((TimeoutError, ValueError)):
            await checks._nmap_version("/mock/nmap")
    else:
        assert await checks._nmap_version("/mock/nmap") == "Nmap version 7.95"
    assert factory.call_args.args == ("/mock/nmap", "--version")
    process.stdout.read.assert_awaited_once_with(4096)
    if failure == "timeout":
        process.kill.assert_called_once()
        process.communicate.assert_awaited_once()
