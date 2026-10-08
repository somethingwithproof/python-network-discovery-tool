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
SSH, DB, SNMP, QUIET = "172.30.57.10", "172.30.57.11", "172.30.57.12", "172.30.57.14"


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

    assert open_names(devices[SSH]) == {"ssh"} and devices[SSH]["ssh"] is True
    assert open_names(devices[DB]) == {"mysql"} and devices[DB]["mysql"] is True
    assert open_names(devices[SNMP]) == {"snmp"} and devices[SNMP]["snmp"] is True
    assert devices[QUIET]["alive"] is True
    assert open_names(devices[QUIET]) == set()
    assert devices["172.30.57.13"]["alive"] is False


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
