# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

import json

import pytest
from conftest import validator
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


def snap(
    tmp_path,
    name,
    devices,
    services=DEFAULT_SERVICES,
    target="10.0.0.0/24",
    timeout=None,
    backend=None,
):
    path = tmp_path / name
    write_snapshot(path, target, services, devices, timeout=timeout, backend=backend)
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


def test_snapshot_records_timeout_and_backend(tmp_path):
    path = snap(tmp_path, "a.json", [], timeout=0.3, backend="asyncio")
    document = json.loads(path.read_text())
    assert document["timeout"] == 0.3
    assert document["backend"] == "asyncio"
    loaded = load_inventory(path)
    assert loaded.timeout == 0.3
    assert loaded.backend == "asyncio"


def test_diff_warns_when_timeout_or_backend_differ(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH)], timeout=0.3, backend="asyncio")
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH)], timeout=1.0, backend="nmap")
    result = compare(load_inventory(old), load_inventory(new))
    assert not result.changed
    assert result.warnings == [
        "timeouts differ: 0.3 vs 1.0",
        "backends differ: asyncio vs nmap",
        "timeouts differ for 161/udp: 0.3 vs 1.0",
        "timeouts differ for 443/tcp: 0.3 vs 1.0",
    ]


def test_old_snapshots_without_settings_do_not_warn(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH)])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH)], timeout=1.0, backend="nmap")
    result = compare(load_inventory(old), load_inventory(new))
    assert result.warnings == []


@pytest.mark.parametrize("old_budget", ["missing", None, 0.8, 0.3])
def test_snapshot_compares_effective_service_timeout(tmp_path, old_budget):
    services = (ServiceSpec("ssh", 22, "tcp", "ssh", timeout=0.3),)
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH)], services=services, timeout=1.0)
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH)], services=services, timeout=1.0)
    document = json.loads(old.read_text())
    if old_budget == "missing":
        del document["services"][0]["timeout"]
    else:
        document["services"][0]["timeout"] = old_budget
    old.write_text(json.dumps(document))
    result = compare(load_inventory(old), load_inventory(new))
    effective = 1.0 if old_budget in ("missing", None) else old_budget
    expected = [] if effective == 0.3 else [f"timeouts differ for 22/tcp: {effective} vs 0.3"]
    assert result.warnings == expected
    assert not result.changed


def test_identical_snapshots_have_no_changes(tmp_path):
    a = snap(tmp_path, "a.json", [host("10.0.0.1", SSH)])
    b = snap(tmp_path, "b.json", [host("10.0.0.1", SSH)])

    result = compare(load_inventory(a), load_inventory(b))
    assert not result.changed
    assert result.warnings == []


def test_service_rename_does_not_change_port_state(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", HTTP)])
    renamed = ("web", *HTTP[1:])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", renamed)])
    result = runner.invoke(cli.app, ["diff", str(old), str(new), "--format", "json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["changed"] is False


def test_service_rename_preserves_version_change(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", HTTP)])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", ("web", 80, "tcp", "new"))])
    result = compare(load_inventory(old), load_inventory(new))
    assert result.opened == result.closed == []
    assert [(c.name, c.old_version, c.version) for c in result.version_changes] == [
        ("web", HTTP[3], "new")
    ]


@pytest.mark.parametrize("reverse", [False, True])
def test_duplicate_port_services_keep_their_identity(tmp_path, reverse):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", HTTP, ("web", 80, "tcp", "other"))])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", HTTP)])
    if reverse:
        old, new = new, old
    result = compare(load_inventory(old), load_inventory(new))
    changes = result.opened if reverse else result.closed
    assert [(c.name, c.port) for c in changes] == [("web", 80)]
    assert (result.closed if reverse else result.opened) == []
    assert result.version_changes == []


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


def test_two_services_on_one_port_are_compared_apart(tmp_path):
    old = snap(
        tmp_path,
        "old.json",
        [host("10.0.0.1", ("http", 80, "tcp", "nginx"), ("alt", 80, "tcp", "caddy"))],
    )
    new = snap(
        tmp_path,
        "new.json",
        [host("10.0.0.1", ("http", 80, "tcp", "nginx"), ("alt", 80, "tcp", "caddy-2"))],
    )

    result = compare(load_inventory(old), load_inventory(new))

    assert [
        (change.name, change.version, change.old_version) for change in result.version_changes
    ] == [("alt", "caddy-2", "caddy")]
    assert result.opened == []
    assert result.closed == []


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
        (
            '{"format": "netprobe-snapshot", "version": 1, "services": [], "devices": [], '
            '"timeout": "slow"}',
            "timeout must be a number",
        ),
        (
            '{"format": "netprobe-snapshot", "version": 1, "services": [], "devices": [], '
            '"backend": 1}',
            "backend must be a string",
        ),
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


def failed_host(ip, *ports, alive=False, opened=()):
    """A device whose probes on `ports` failed; `opened` services still answered."""
    services = [Service(n, p, proto, "unknown") for n, p, proto in ports]
    services += [Service(n, p, proto, "open", v) for n, p, proto, v in opened]
    return Device(ip=ip, alive=alive, services=services, errors=["probe timed out"])


SSH_PORT = ("ssh", 22, "tcp")
HTTP_PORT = ("http", 80, "tcp")


def diff_exit(old, new):
    return runner.invoke(cli.app, ["diff", str(old), str(new), "-f", "json"])


def test_open_port_now_unknown_is_unconfirmed_not_closed(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH, HTTP)])
    new = snap(tmp_path, "new.json", [failed_host("10.0.0.1", SSH_PORT, alive=True, opened=[HTTP])])

    result = compare(load_inventory(old), load_inventory(new))

    assert result.closed == []
    assert [(u.ip, u.port, u.before, u.after) for u in result.unconfirmed] == [
        ("10.0.0.1", 22, "open", "unknown")
    ]
    assert result.changed
    outcome = diff_exit(old, new)
    assert outcome.exit_code == 3
    assert json.loads(outcome.output)["unconfirmed"][0]["after"] == "unknown"


def test_unknown_port_now_open_is_reported_opened(tmp_path):
    old = snap(tmp_path, "old.json", [failed_host("10.0.0.1", SSH_PORT, alive=True, opened=[HTTP])])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH, HTTP)])

    result = compare(load_inventory(old), load_inventory(new))

    assert [(c.ip, c.port) for c in result.opened] == [("10.0.0.1", 22)]
    assert result.unconfirmed == []
    assert diff_exit(old, new).exit_code == 3


def test_port_unknown_in_both_scans_needs_attention(tmp_path):
    old = snap(tmp_path, "old.json", [failed_host("10.0.0.1", SSH_PORT, alive=True, opened=[HTTP])])
    new = snap(tmp_path, "new.json", [failed_host("10.0.0.1", SSH_PORT, alive=True, opened=[HTTP])])

    result = compare(load_inventory(old), load_inventory(new))

    assert [(u.port, u.before, u.after) for u in result.unconfirmed] == [(22, "unknown", "unknown")]
    assert result.opened == result.closed == []
    assert diff_exit(old, new).exit_code == 3


def test_host_with_uncertain_baseline_now_open_is_reported_new(tmp_path):
    old = snap(tmp_path, "old.json", [failed_host("10.0.0.1", SSH_PORT)])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH, HTTP)])

    result = compare(load_inventory(old), load_inventory(new))

    assert [h["ip"] for h in result.new_hosts] == ["10.0.0.1"]
    assert [s["port"] for s in result.new_hosts[0]["services"]] == [22, 80]
    assert result.unsettled_hosts == [{"ip": "10.0.0.1", "before": "uncertain", "after": "up"}]
    assert diff_exit(old, new).exit_code == 3


def test_host_with_only_failed_probes_is_unsettled_not_vanished(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH)])
    new = snap(tmp_path, "new.json", [failed_host("10.0.0.1", SSH_PORT)])

    assert [d["ip"] for d in json.loads(new.read_text())["devices"]] == ["10.0.0.1"]
    result = compare(load_inventory(old), load_inventory(new))

    assert result.vanished_hosts == []
    assert result.unsettled_hosts == [{"ip": "10.0.0.1", "before": "up", "after": "uncertain"}]
    outcome = diff_exit(old, new)
    assert outcome.exit_code == 3
    assert json.loads(outcome.output)["changed"] is True


def test_unchanged_scans_still_exit_zero(tmp_path):
    old = snap(tmp_path, "old.json", [host("10.0.0.1", SSH, HTTP)])
    new = snap(tmp_path, "new.json", [host("10.0.0.1", SSH, HTTP)])

    outcome = diff_exit(old, new)

    assert outcome.exit_code == 0
    report = json.loads(outcome.output)
    assert report["changed"] is False
    assert report["unsettled_hosts"] == report["unconfirmed"] == []


def test_host_failing_in_both_scans_is_unsettled(tmp_path):
    old = snap(tmp_path, "old.json", [failed_host("10.0.0.1", SSH_PORT)])
    new = snap(tmp_path, "new.json", [failed_host("10.0.0.1", SSH_PORT)])

    result = compare(load_inventory(old), load_inventory(new))

    assert result.unsettled_hosts == [
        {"ip": "10.0.0.1", "before": "uncertain", "after": "uncertain"}
    ]
    assert diff_exit(old, new).exit_code == 3


def up_host(ip, **states):
    """An answering host whose services have the given states, e.g. http="closed"."""
    ports = {"ssh": (22, "tcp"), "http": (80, "tcp"), "mysql": (3306, "tcp")}
    return Device(
        ip=ip,
        alive=True,
        services=[Service(name, *ports[name], state) for name, state in states.items()],
    )


def changed_exit(old, new):
    """The CLI's JSON diff, checked against the published schema, and its exit code."""
    outcome = diff_exit(old, new)
    document = json.loads(outcome.output)
    validator("diff").validate(document)
    return document, outcome.exit_code


def test_host_absent_before_and_uncertain_now_is_unsettled(tmp_path):
    old = snap(tmp_path, "old.json", [])
    new = snap(tmp_path, "new.json", [failed_host("10.0.0.1", SSH_PORT)])

    result = compare(load_inventory(old), load_inventory(new))

    assert result.unsettled_hosts == [{"ip": "10.0.0.1", "before": "absent", "after": "uncertain"}]
    assert result.new_hosts == result.vanished_hosts == []
    assert result.changed
    document, status = changed_exit(old, new)
    assert (document["changed"], status) == (True, 3)


def test_host_uncertain_before_and_absent_now_is_unsettled(tmp_path):
    old = snap(tmp_path, "old.json", [failed_host("10.0.0.1", SSH_PORT)])
    new = snap(tmp_path, "new.json", [])

    result = compare(load_inventory(old), load_inventory(new))

    assert result.unsettled_hosts == [{"ip": "10.0.0.1", "before": "uncertain", "after": "absent"}]
    assert result.new_hosts == result.vanished_hosts == []
    document, status = changed_exit(old, new)
    assert (document["changed"], status) == (True, 3)


@pytest.mark.parametrize("state", ["closed", "filtered"])
def test_port_not_open_now_unknown_is_unconfirmed(tmp_path, state):
    old = snap(tmp_path, "old.json", [up_host("10.0.0.1", ssh="open", http=state)])
    new = snap(tmp_path, "new.json", [up_host("10.0.0.1", ssh="open", http="unknown")])

    result = compare(load_inventory(old), load_inventory(new))

    assert [(u.name, u.port, u.before, u.after) for u in result.unconfirmed] == [
        ("http", 80, "not-open", "unknown")
    ]
    assert result.opened == result.closed == []
    document, status = changed_exit(old, new)
    assert (document["changed"], status) == (True, 3)


@pytest.mark.parametrize("state", ["closed", "filtered"])
def test_port_unknown_now_not_open_is_unconfirmed(tmp_path, state):
    old = snap(tmp_path, "old.json", [up_host("10.0.0.1", ssh="open", http="unknown")])
    new = snap(tmp_path, "new.json", [up_host("10.0.0.1", ssh="open", http=state)])

    result = compare(load_inventory(old), load_inventory(new))

    assert [(u.name, u.port, u.before, u.after) for u in result.unconfirmed] == [
        ("http", 80, "unknown", "not-open")
    ]
    document, status = changed_exit(old, new)
    assert (document["changed"], status) == (True, 3)


def test_unchanged_closed_and_filtered_ports_exit_zero(tmp_path):
    devices = [up_host("10.0.0.1", ssh="open", http="closed", mysql="filtered")]
    old = snap(tmp_path, "old.json", devices)
    new = snap(tmp_path, "new.json", devices)

    document, status = changed_exit(old, new)

    assert (document["changed"], status) == (False, 0)


@pytest.mark.parametrize(
    ("port", "protocol"), [(True, "tcp"), (0, "tcp"), (70000, "tcp"), ("22", "tcp"), (22, "sctp")]
)
def test_snapshot_with_impossible_endpoint_is_rejected(tmp_path, port, protocol):
    path = snap(tmp_path, "s.json", [host("10.0.0.1", SSH)])
    document = json.loads(path.read_text())
    document["devices"][0]["services"][0].update(port=port, protocol=protocol)
    path.write_text(json.dumps(document))

    with pytest.raises(SnapshotError, match="invalid service endpoint"):
        load_inventory(path)
    result = CliRunner().invoke(cli.app, ["export", str(path), "-o", str(tmp_path / "x.sh")])
    assert result.exit_code == 2, result.output


def test_versioned_report_is_read_like_a_snapshot(tmp_path):
    from netprobe.output import save_json

    report = tmp_path / "report.json"
    devices = [host("10.0.0.1", SSH), Device("10.0.0.2", errors=["Host is down"])]
    save_json(devices, report, network="10.0.0.0/30", services=DEFAULT_SERVICES, timeout=1.0)
    inventory = load_inventory(report)

    assert list(inventory.hosts) == ["10.0.0.1"]
    assert inventory.target == "10.0.0.0/30"
    assert inventory.timeout == 1.0
    assert inventory.probed == {(s.port, s.protocol) for s in DEFAULT_SERVICES}
    snapshot = snap(tmp_path, "s.json", [host("10.0.0.1", SSH)], target="10.0.0.0/30", timeout=1.0)
    assert not compare(inventory, load_inventory(snapshot)).changed


# --- untrusted file contents

ESC = "\x1b[2J\x1b]0;owned\x07"
CSI = "\x9b31m"


def tampered(tmp_path, filename, **fields):
    """A valid snapshot of 10.0.0.1 with the given device or service fields replaced."""
    path = snap(tmp_path, filename, [host("10.0.0.1", SSH)])
    document = json.loads(path.read_text())
    device = document["devices"][0]
    device.update({k: v for k, v in fields.items() if k in ("ip", "hostname")})
    device["services"][0].update({k: v for k, v in fields.items() if k in ("name", "version")})
    document.update({k: v for k, v in fields.items() if k in ("target", "backend")})
    path.write_text(json.dumps(document))
    return path


def test_loaded_text_is_stripped_of_control_characters(tmp_path):
    old = tampered(
        tmp_path,
        "old.json",
        hostname=f"web{ESC}",
        name=f"[bold red]ssh{CSI}",
        version=f"Open{ESC}SSH",
        target=f"10.0.0.0/24{ESC}",
        backend=f"nmap{ESC}",
    )
    new = snap(tmp_path, "new.json", [], backend="asyncio")

    result = runner.invoke(cli.app, ["diff", str(old), str(new)])

    assert result.exit_code == 3
    assert (
        "\x1b" not in result.output and "\x9b" not in result.output and "\x07" not in result.output
    )
    # Markup from the file is printed literally, not interpreted.
    assert "[bold red]ssh" in result.output
    inventory = load_inventory(old)
    assert inventory.hosts["10.0.0.1"].hostname.startswith("web")
    assert all(c.isprintable() for c in inventory.target + inventory.hosts["10.0.0.1"].hostname)
    [(_, _, name)] = inventory.hosts["10.0.0.1"].open
    assert name.isprintable()


@pytest.mark.parametrize(
    "ip", [f"10.0.0.1{ESC}", "[red]10.0.0.1[/red]", "-oX", "10.0.0.1 10.0.0.2", "fe80::1%en0", 7]
)
def test_snapshot_with_unsafe_address_is_refused_by_every_reader(tmp_path, ip):
    path = tampered(tmp_path, "bad.json", ip=ip)

    with pytest.raises(SnapshotError, match=r"invalid stored address|Invalid target|scope"):
        load_inventory(path)
    good = snap(tmp_path, "good.json", [host("10.0.0.1", SSH)])
    assert runner.invoke(cli.app, ["diff", str(good), str(path)]).exit_code == 2
    exported = runner.invoke(cli.app, ["export", str(path), "-o", str(tmp_path / "x.sh")])
    assert exported.exit_code == 2
    assert not (tmp_path / "x.sh").exists()


# --- incomplete scans


def report(tmp_path, name, devices, *, complete):
    from netprobe.output import save_json

    path = tmp_path / name
    save_json(devices, path, network="10.0.0.0/30", services=DEFAULT_SERVICES, complete=complete)
    return path


def test_diff_refuses_an_incomplete_report_by_default(tmp_path):
    full = report(
        tmp_path, "full.json", [host("10.0.0.1", SSH), host("10.0.0.2", SSH)], complete=True
    )
    partial = report(tmp_path, "partial.json", [host("10.0.0.1", SSH)], complete=False)

    for args in ([full, partial], [partial, full]):
        outcome = runner.invoke(cli.app, ["diff", *map(str, args), "-f", "json"])
        assert outcome.exit_code == 2
        assert "complete: false" in outcome.output
        assert "--allow-partial" in outcome.output
        assert "{" not in outcome.stdout


def test_allow_partial_marks_unreached_hosts_unsettled(tmp_path):
    full = report(
        tmp_path, "full.json", [host("10.0.0.1", SSH), host("10.0.0.2", SSH)], complete=True
    )
    partial = report(tmp_path, "partial.json", [host("10.0.0.1", SSH)], complete=False)

    outcome = runner.invoke(
        cli.app, ["diff", str(full), str(partial), "-f", "json", "--allow-partial"]
    )

    assert outcome.exit_code == 3
    document = json.loads(outcome.stdout)
    validator("diff").validate(document)
    assert document["partial"] is True
    assert document["changed"] is True
    assert document["vanished_hosts"] == []
    assert document["unsettled_hosts"] == [{"ip": "10.0.0.2", "before": "up", "after": "unscanned"}]
    assert any("incomplete scan" in warning for warning in document["warnings"])


def test_allow_partial_still_reports_hosts_it_reached_as_down_vanished(tmp_path):
    up = [host("10.0.0.1", SSH), host("10.0.0.2", SSH)]
    full = report(tmp_path, "full.json", up, complete=True)
    reached = [host("10.0.0.1", SSH), Device("10.0.0.2", errors=["Host is down"])]
    partial = report(tmp_path, "partial.json", reached, complete=False)

    result = compare(load_inventory(full), load_inventory(partial, allow_partial=True))

    assert [h["ip"] for h in result.vanished_hosts] == ["10.0.0.2"]
    assert result.unsettled_hosts == []
    assert result.partial
    assert result.changed


def test_allow_partial_never_reports_no_change(tmp_path):
    partial = report(tmp_path, "partial.json", [host("10.0.0.1", SSH)], complete=False)

    outcome = runner.invoke(cli.app, ["diff", str(partial), str(partial), "--allow-partial"])

    assert outcome.exit_code == 3
    assert "No changes" not in outcome.output


def test_export_refuses_an_incomplete_report_unless_allowed(tmp_path):
    partial = report(tmp_path, "partial.json", [host("10.0.0.1", SSH)], complete=False)
    script = tmp_path / "import.sh"

    refused = runner.invoke(cli.app, ["export", str(partial), "-o", str(script)])
    assert refused.exit_code == 2
    assert "--allow-partial" in refused.output
    assert not script.exists()

    allowed = runner.invoke(cli.app, ["export", str(partial), "-o", str(script), "--allow-partial"])
    assert allowed.exit_code == 0
    text = script.read_text()
    assert "# WARNING: the scan stopped at its deadline" in text
    assert "--ip=10.0.0.1" in text


def test_report_with_non_boolean_complete_is_malformed(tmp_path):
    path = report(tmp_path, "r.json", [host("10.0.0.1", SSH)], complete=True)
    document = json.loads(path.read_text())
    document["complete"] = "false"
    path.write_text(json.dumps(document))

    with pytest.raises(SnapshotError, match="complete must be a boolean"):
        load_inventory(path)
