import json

import pytest
from typer.testing import CliRunner

from netprobe import cli
from netprobe.config import DEFAULT_SERVICES
from netprobe.diff import (
    SNAPSHOT_VERSION,
    SnapshotError,
    compare,
    load_inventory,
    write_snapshot,
)
from netprobe.models import Device, Service, ServiceSpec

runner = CliRunner()


def host(ip, *services, hostname=""):
    return Device(
        ip=ip,
        alive=True,
        hostname=hostname,
        services=[Service(n, p, proto, "open", v) for n, p, proto, v in services],
    )


SSH = ("ssh", 22, "tcp", "OpenSSH_9.6")
SSH_NEW = ("ssh", 22, "tcp", "OpenSSH_10.0")
HTTP = ("http", 80, "tcp", "nginx/1.28.3")
DB = ("mysql", 3306, "tcp", "11.4.13-MariaDB")


def snap(tmp_path, name, devices, services=DEFAULT_SERVICES, target="10.0.0.0/24"):
    path = tmp_path / name
    write_snapshot(path, target, services, devices)
    return path


def test_snapshot_format(tmp_path):
    path = snap(tmp_path, "a.json", [host("10.0.0.1", SSH), Device(ip="10.0.0.2")])
    document = json.loads(path.read_text())

    assert document["format"] == "netprobe-snapshot"
    assert document["version"] == SNAPSHOT_VERSION
    assert document["created"].endswith("+00:00")
    assert document["target"] == "10.0.0.0/24"
    assert [s["name"] for s in document["services"]] == ["ssh", "snmp", "mysql", "http", "https"]
    assert [d["ip"] for d in document["devices"]] == ["10.0.0.1"]  # down hosts are dropped


def test_identical_snapshots_have_no_changes(tmp_path):
    a = snap(tmp_path, "a.json", [host("10.0.0.1", SSH)])
    b = snap(tmp_path, "b.json", [host("10.0.0.1", SSH)])

    result = compare(load_inventory(a), load_inventory(b))
    assert not result.changed
    assert result.warnings == []


def test_every_kind_of_change(tmp_path):
    old = snap(
        tmp_path,
        "old.json",
        [host("10.0.0.2", SSH, HTTP), host("10.0.0.10", SSH), host("10.0.0.3", DB)],
    )
    new = snap(
        tmp_path,
        "new.json",
        [
            host("10.0.0.2", SSH_NEW, DB),
            host("10.0.0.9", HTTP, hostname="web"),
            host("10.0.0.10", SSH),
        ],
    )
    result = compare(load_inventory(old), load_inventory(new)).to_dict()

    assert result["changed"] is True
    assert [h["ip"] for h in result["new_hosts"]] == ["10.0.0.9"]
    assert result["new_hosts"][0]["services"] == [
        {"name": "http", "port": 80, "protocol": "tcp", "version": "nginx/1.28.3"}
    ]
    assert [h["ip"] for h in result["vanished_hosts"]] == ["10.0.0.3"]
    assert [(c["ip"], c["name"], c["port"]) for c in result["opened"]] == [
        ("10.0.0.2", "mysql", 3306)
    ]
    assert [(c["ip"], c["name"], c["old_version"]) for c in result["closed"]] == [
        ("10.0.0.2", "http", "nginx/1.28.3")
    ]
    assert result["version_changes"] == [
        {
            "ip": "10.0.0.2",
            "name": "ssh",
            "port": 22,
            "protocol": "tcp",
            "version": "OpenSSH_10.0",
            "old_version": "OpenSSH_9.6",
        }
    ]


def test_hosts_sorted_numerically(tmp_path):
    old = snap(tmp_path, "old.json", [])
    new = snap(
        tmp_path, "new.json", [host(ip) for ip in ("10.0.0.10", "10.0.0.9", "box.example", "::1")]
    )

    ips = [h["ip"] for h in compare(load_inventory(old), load_inventory(new)).new_hosts]
    assert ips == ["10.0.0.9", "10.0.0.10", "::1", "box.example"]


def test_ports_probed_in_only_one_scan_are_ignored(tmp_path):
    ssh_only = (ServiceSpec("ssh", 22, "tcp", "ssh"),)
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH, HTTP)])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH)], services=ssh_only, target="10.0.0.1")
    result = compare(load_inventory(old), load_inventory(new))

    assert not result.changed
    assert result.warnings[0] == "targets differ: 10.0.0.0/24 vs 10.0.0.1"
    assert "80/tcp" in result.warnings[1]


def test_plain_reports_and_legacy_booleans(tmp_path):
    old = tmp_path / "old.json"
    old.write_text(
        json.dumps([{"ip": "10.0.0.1", "alive": True, "ssh": True, "snmp": False, "mysql": False}])
    )
    new = tmp_path / "new.json"
    new.write_text(
        json.dumps(
            [
                {
                    "ip": "10.0.0.1",
                    "alive": True,
                    "services": [
                        {"name": "ssh", "port": 22, "protocol": "tcp", "state": "open"},
                        {"name": "mysql", "port": 3306, "protocol": "tcp", "state": "open"},
                    ],
                },
                {"ip": "10.0.0.2", "alive": False},
            ]
        )
    )
    result = compare(load_inventory(old), load_inventory(new))

    assert [(c.ip, c.port) for c in result.opened] == [("10.0.0.1", 3306)]
    assert result.new_hosts == []


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("not json", "cannot read"),
        ('{"format": "other"}', "not a netprobe snapshot"),
        ('{"format": "netprobe-snapshot", "version": 99}', "version 99 is not supported"),
        ('{"format": "netprobe-snapshot", "version": 1}', "malformed"),
        ('[{"hostname": "x"}]', "without an ip"),
        ('[{"ip": "10.0.0.1", "services": [{"state": "open"}]}]', "malformed"),
    ],
)
def test_bad_inputs(tmp_path, content, message):
    path = tmp_path / "bad.json"
    path.write_text(content)
    with pytest.raises(SnapshotError, match=message):
        load_inventory(path)


def test_missing_file(tmp_path):
    with pytest.raises(SnapshotError, match="cannot read"):
        load_inventory(tmp_path / "absent.json")


# --- CLI


def test_cli_diff_exit_codes_and_json(tmp_path):
    a = snap(tmp_path, "a.json", [host("10.0.0.1", SSH)])
    b = snap(tmp_path, "b.json", [host("10.0.0.1", SSH_NEW)])

    same = runner.invoke(cli.app, ["diff", str(a), str(a)])
    assert same.exit_code == 0
    assert "No changes" in same.output

    changed = runner.invoke(cli.app, ["diff", str(a), str(b), "--format", "json"])
    assert changed.exit_code == 3
    assert json.loads(changed.output)["version_changes"][0]["version"] == "OpenSSH_10.0"


def test_cli_diff_table_and_output_file(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.2", SSH, HTTP), host("10.0.0.3", DB)])
    new = snap(tmp_path, "new.json", [host("10.0.0.2", SSH_NEW, DB), host("10.0.0.9", HTTP)])
    out = tmp_path / "diff.json"
    result = runner.invoke(cli.app, ["diff", str(old), str(new), "-o", str(out)])

    assert result.exit_code == 3
    for word in ("new host", "vanished host", "opened", "closed", "OpenSSH_9.6 -> OpenSSH_10.0"):
        assert word in result.output
    assert json.loads(out.read_text())["changed"] is True


def test_cli_diff_unreadable_input_exits_2(tmp_path):
    result = runner.invoke(cli.app, ["diff", str(tmp_path / "a"), str(tmp_path / "b")])
    assert result.exit_code == 2
    assert "cannot read" in result.output


def test_cli_diff_unwritable_output_exits_1(tmp_path):
    a = snap(tmp_path, "a.json", [])
    result = runner.invoke(cli.app, ["diff", str(a), str(a), "-o", str(tmp_path / "no" / "x.json")])
    assert result.exit_code == 1


def test_cli_diff_warnings_are_shown(tmp_path):
    a = snap(tmp_path, "a.json", [], target="10.0.0.0/24")
    b = snap(tmp_path, "b.json", [], target="10.0.1.0/24")
    result = runner.invoke(cli.app, ["diff", str(a), str(b)])

    assert result.exit_code == 0
    assert "targets differ" in result.output
