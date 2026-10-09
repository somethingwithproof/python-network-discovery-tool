# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

import json

from netprobe.models import Device, Service
from netprobe.output import print_results, save_csv, save_json


def sample() -> list[Device]:
    return [
        Device(
            ip="192.168.1.1",
            alive=True,
            ssh=True,
            hostname="server",
            services=[
                Service("ssh", 22, "tcp", "open", "OpenSSH_10.0", {"protocol": "2.0"}),
                Service("mysql", 3306, "tcp", "closed"),
            ],
        ),
        Device(ip="192.168.1.2", alive=False, errors=["Host is down"]),
    ]


def test_device_defaults():
    device = Device(ip="192.168.1.1")
    assert (device.alive, device.ssh, device.snmp, device.mysql) == (False, False, False, False)
    assert device.errors == []
    assert device.services == []


def test_save_json_keeps_legacy_fields_and_adds_services(tmp_path):
    out = tmp_path / "test.json"
    save_json(sample(), out)

    data = json.loads(out.read_text())
    assert list(data[0])[:7] == ["ip", "alive", "ssh", "snmp", "mysql", "hostname", "errors"]
    assert data[0]["ssh"] is True
    assert data[0]["services"][0] == {
        "name": "ssh",
        "port": 22,
        "protocol": "tcp",
        "state": "open",
        "version": "OpenSSH_10.0",
        "details": {"protocol": "2.0"},
    }


def test_save_csv(tmp_path):
    out = tmp_path / "test.csv"
    save_csv(sample(), out)

    lines = out.read_text().splitlines()
    assert lines[0] == "ip,alive,ssh,snmp,mysql,hostname,errors,services,versions"
    assert lines[1] == "192.168.1.1,True,True,False,False,server,,ssh:22/tcp,ssh=OpenSSH_10.0"
    assert lines[2] == "192.168.1.2,False,False,False,False,,Host is down,,"


def test_save_csv_joins_errors(tmp_path):
    out = tmp_path / "out.csv"
    save_csv([Device(ip="10.0.0.1", errors=["a", "b"])], out)

    assert "a; b" in out.read_text()


def test_print_results_no_alive_hosts(capsys):
    print_results([Device(ip="10.0.0.1")])
    assert "No alive hosts found" in capsys.readouterr().out


def test_print_results_lists_other_open_services(capsys):
    device = Device(
        ip="10.0.0.1",
        alive=True,
        services=[Service("https", 443, "tcp", "open"), Service("http", 80, "tcp", "closed")],
    )
    print_results([device])
    out = capsys.readouterr().out

    assert "https:443" in out
    assert "http:80" not in out
    assert "https: 1" in out


def test_print_results_escapes_network_supplied_text(capsys):
    device = Device(
        ip="10.0.0.1",
        alive=True,
        hostname="[red]evil[/red]",
        services=[Service("http", 80, "tcp", "open", "[bold]nginx[/bold]")],
    )
    print_results([device])
    out = capsys.readouterr().out

    assert "[red]evil" in out
    assert "[bold]nginx" in out


def test_print_results_summary(capsys):
    print_results([Device(ip="10.0.0.1", alive=True, ssh=True, mysql=True, hostname="db")])
    out = capsys.readouterr().out

    assert "10.0.0.1" in out
    assert "SSH servers: 1" in out
    assert "SNMP devices: 0" in out
    assert "MySQL servers: 1" in out
