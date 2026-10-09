"""Scans of the docker compose lab in tests/integration/compose.yml.

These run only inside the lab's tester container (NETPROBE_LAB=1), and only
ever scan the lab subnet.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from netprobe.cli import app

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("NETPROBE_LAB") != "1", reason="needs the compose lab"),
]

LAB = "172.30.57.8/29"  # .9 to .14: the service containers
SSH, DB, SNMP, WEB, QUIET = (f"172.30.57.{n}" for n in (10, 11, 12, 13, 14))


def scan(tmp_path: Path, *args: str) -> dict[str, dict[str, object]]:
    out = tmp_path / "scan.json"
    result = CliRunner().invoke(app, ["scan", LAB, "-q", "-o", str(out), *args])
    assert result.exit_code == 0, result.output
    return {d["ip"]: d for d in json.loads(out.read_text())}


def open_names(device: dict[str, object]) -> set[str]:
    services = device["services"]
    assert isinstance(services, list)
    return {s["name"] for s in services if s["state"] == "open"}


@pytest.mark.parametrize("backend", ["asyncio", "nmap"])
def test_lab_services_found(tmp_path, backend):
    devices = scan(tmp_path, "--backend", backend, "--timeout", "2")

    assert open_names(devices[SSH]) == {"ssh"}
    assert devices[SSH]["ssh"] is True
    assert open_names(devices[DB]) == {"mysql"}
    assert devices[DB]["mysql"] is True
    assert open_names(devices[SNMP]) == {"snmp"}
    assert devices[SNMP]["snmp"] is True
    assert open_names(devices[WEB]) == {"http", "https"}
    assert devices[QUIET]["alive"] is True
    assert open_names(devices[QUIET]) == set()
    assert devices["172.30.57.9"]["alive"] is False


def test_lab_config_and_port_selection(tmp_path):
    config = tmp_path / "netprobe.toml"
    config.write_text('[services.db]\nport = 3306\nprobe = "mysql"\n')
    devices = scan(
        tmp_path, "--config", str(config), "--services", "ssh,db", "--ports", "ssh=2222,8080"
    )

    db = devices[DB]
    assert [s["name"] for s in db["services"]] == ["ssh", "db", "tcp-8080"]
    assert open_names(db) == {"db"}
    assert open_names(devices[SSH]) == set()  # sshd listens on 22, not 2222


def service(device: dict[str, object], name: str) -> dict[str, object]:
    services = device["services"]
    assert isinstance(services, list)
    return next(s for s in services if s["name"] == name)


def test_lab_fingerprints_without_credentials(tmp_path):
    devices = scan(tmp_path, "--timeout", "2")

    ssh = service(devices[SSH], "ssh")
    assert str(ssh["version"]).startswith("OpenSSH_")
    assert ssh["details"]["protocol"] == "2.0"

    db = service(devices[DB], "mysql")
    assert db["details"]["flavor"] == "MariaDB"
    assert str(db["version"]).startswith("11.4.")

    http = service(devices[WEB], "http")
    assert str(http["version"]).startswith("nginx/")
    https = service(devices[WEB], "https")
    assert https["details"]["cert_verified"] is False
    assert "self-signed" in https["details"]["cert_verify_error"]
    assert "cert_read_unverified" not in https["details"]
    assert "cert_sans" not in https["details"]
    assert https["version"] == ""

    snmp = service(devices[SNMP], "snmp")
    assert snmp["state"] == "open"
    assert snmp["details"]["engine_id"].startswith("80001f88")
    assert "sys_name" not in snmp["details"]


@pytest.mark.parametrize(
    "env",
    [
        {"NETPROBE_SNMP_COMMUNITY": "netprobe-test"},
        {
            "NETPROBE_SNMP_USER": "netprobe",
            "NETPROBE_SNMP_AUTH_KEY": "netprobe-auth",
            "NETPROBE_SNMP_PRIV_KEY": "netprobe-priv",
        },
    ],
    ids=["v2c", "v3-authpriv"],
)
def test_lab_snmp_system_mib(tmp_path, monkeypatch, env):
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    out = tmp_path / "scan.json"
    result = CliRunner().invoke(
        app, ["scan", SNMP, "-q", "-o", str(out), "--services", "snmp", "--timeout", "2"]
    )
    assert result.exit_code == 0, result.output

    snmp = json.loads(out.read_text())[0]["services"][0]
    assert snmp["details"]["sys_name"] == "snmp-lab"
    assert snmp["details"]["sys_object_id"] == "1.3.6.1.4.1.8072.3.2.10"
    assert snmp["details"]["snmp_version"] == ("3" if "NETPROBE_SNMP_USER" in env else "2c")
    if "NETPROBE_SNMP_USER" in env:
        assert snmp["details"]["snmp_security_level"] == "authPriv"
    assert snmp["version"].startswith("Linux")
    for value in ("netprobe-test", "netprobe-auth", "netprobe-priv"):
        assert value not in out.read_text()


def test_lab_snmp_wrong_key_is_reported(tmp_path, monkeypatch):
    monkeypatch.setenv("NETPROBE_SNMP_USER", "netprobe")
    monkeypatch.setenv("NETPROBE_SNMP_AUTH_KEY", "not-the-key")
    out = tmp_path / "scan.json"
    CliRunner().invoke(app, ["scan", SNMP, "-q", "-o", str(out), "--services", "snmp"])

    snmp = json.loads(out.read_text())[0]["services"][0]
    assert snmp["state"] == "open"
    assert "digest" in snmp["details"]["snmp_error"].lower()


def test_lab_snapshot_diff(tmp_path, monkeypatch):
    monkeypatch.setenv("NETPROBE_SNMP_COMMUNITY", "netprobe-test")
    runner = CliRunner()
    small, full = tmp_path / "small.json", tmp_path / "full.json"
    for target, path in ((SSH, small), (LAB, full)):
        result = runner.invoke(
            app,
            ["scan", target, "-q", "--services", "ssh,http,snmp", "--save-snapshot", str(path)],
        )
        assert result.exit_code == 0, result.output
    assert "netprobe-test" not in full.read_text()

    assert runner.invoke(app, ["diff", str(full), str(full)]).exit_code == 0

    changed = runner.invoke(app, ["diff", str(small), str(full), "--format", "json"])
    assert changed.exit_code == 3
    report = json.loads(changed.output)
    assert [h["ip"] for h in report["new_hosts"]] == [DB, SNMP, WEB, QUIET]
    snmp_host = report["new_hosts"][1]["services"]
    assert snmp_host[0]["name"] == "snmp"
    assert snmp_host[0]["version"].startswith("Linux")


def test_lab_kadupul_export(tmp_path, monkeypatch):
    from test_export import run_script

    monkeypatch.setenv("NETPROBE_SNMP_COMMUNITY", "netprobe-test")
    runner = CliRunner()
    snap = tmp_path / "lab.json"
    scanned = runner.invoke(
        app, ["scan", LAB, "-q", "--timeout", "2", "--save-snapshot", str(snap)]
    )
    assert scanned.exit_code == 0, scanned.output

    script = tmp_path / "import.sh"
    exported = runner.invoke(app, ["export", str(snap), "-o", str(script), "--template", "1"])
    assert exported.exit_code == 0, exported.output
    assert "netprobe-test" not in script.read_text()

    result, calls = run_script(
        tmp_path, script.read_text(), {"NETPROBE_SNMP_COMMUNITY": "netprobe-test"}
    )
    assert result.returncode == 0, result.stderr
    by_ip = {next(a for a in c if a.startswith("--ip="))[5:]: c for c in calls}
    assert sorted(by_ip) == sorted([SSH, DB, SNMP, WEB, QUIET])
    assert "--community=netprobe-test" in by_ip[SNMP]
    assert "--version=2" in by_ip[SNMP]
    assert "--ping_port=22" in by_ip[SSH]
    assert "--ping_method=icmp" in by_ip[QUIET]
