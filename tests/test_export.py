import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from netprobe import cli
from netprobe.config import DEFAULT_SERVICES
from netprobe.diff import write_snapshot
from netprobe.export import ExportError, KadupulOptions, kadupul_script, write_script
from netprobe.models import Device, Service

runner = CliRunner()


def device(ip, *services, hostname=""):
    return {
        "ip": ip,
        "alive": True,
        "hostname": hostname,
        "services": [
            {"name": n, "port": p, "protocol": proto, "state": "open", "version": v, "details": d}
            for n, p, proto, v, d in services
        ],
    }


SSH = ("ssh", 22, "tcp", "OpenSSH_10.0", {})
SNMP_V2 = ("snmp", 161, "udp", "Linux lab", {"snmp_version": "2c"})
SNMP_V3 = (
    "snmp",
    161,
    "udp",
    "Linux lab",
    {"snmp_version": "3", "snmp_security_level": "authPriv"},
)
SNMP_V3_AUTH = ("snmp", 161, "udp", "", {"snmp_version": "3", "snmp_security_level": "authNoPriv"})


def run_script(tmp_path: Path, script: str, env: dict[str, str] | None = None):
    """Run the script with a stub `php` that records each argv; return the argv lists."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    log = tmp_path / "calls.jsonl"
    stub = bin_dir / "php"
    stub.write_text(
        f"#!{sys.executable}\nimport json, sys\n"
        f"open({str(log)!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
    )
    stub.chmod(0o755)
    path = tmp_path / "import.sh"
    path.write_text(script)
    result = subprocess.run(
        ["sh", str(path)],
        env={"PATH": f"{bin_dir}:/usr/bin:/bin", "KADUPUL_ROOT": "/opt/kadupul", **(env or {})},
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
    return result, calls


def test_v2c_device_references_env_and_runs(tmp_path):
    script = kadupul_script(
        [device("10.0.0.5", SSH, SNMP_V2, hostname="sw1.lab")], KadupulOptions(), "t"
    )

    assert "NETPROBE_SNMP_COMMUNITY" in script
    result, calls = run_script(tmp_path, script, {"NETPROBE_SNMP_COMMUNITY": "pub lic"})
    assert result.returncode == 0, result.stderr
    assert calls == [
        [
            "/opt/kadupul/cli/add_device.php",
            "--description=sw1.lab",
            "--ip=10.0.0.5",
            "--template=0",
            "--version=2",
            "--community=pub lic",
            "--port=161",
            "--avail=snmp",
            "--notes=netprobe: ssh:22/tcp OpenSSH_10.0; snmp:161/udp Linux lab",
        ]
    ]


def test_script_refuses_to_run_without_the_secret(tmp_path):
    script = kadupul_script([device("10.0.0.5", SNMP_V2)], KadupulOptions(), "t")
    result, calls = run_script(tmp_path, script)

    assert result.returncode != 0
    assert "set NETPROBE_SNMP_COMMUNITY" in result.stderr
    assert calls == []


def test_v3_authpriv(tmp_path):
    opts = KadupulOptions(
        snmp_user="ops", auth_protocol="SHA256", priv_protocol="AES256", template=7
    )
    script = kadupul_script([device("10.0.0.6", SNMP_V3)], opts, "t")
    env = {"NETPROBE_SNMP_AUTH_KEY": "a uth'key", "NETPROBE_SNMP_PRIV_KEY": "pr$iv"}
    result, calls = run_script(tmp_path, script, env)

    assert result.returncode == 0, result.stderr
    args = calls[0][1:]
    assert args[:4] == ["--description=10.0.0.6", "--ip=10.0.0.6", "--template=7", "--version=3"]
    for expected in (
        "--username=ops",
        "--authproto=SHA256",
        "--password=a uth'key",
        "--privproto=AES256",
        "--privpass=pr$iv",
    ):
        assert expected in args


def test_v3_authnopriv_uses_quoted_none(tmp_path):
    (tmp_path / "--privproto=N").write_text("")  # would match an unquoted [None] glob
    script = kadupul_script(
        [device("10.0.0.6", SNMP_V3_AUTH)], KadupulOptions(snmp_user="ops"), "t"
    )
    _, calls = run_script(tmp_path, script, {"NETPROBE_SNMP_AUTH_KEY": "authpass1"})

    assert "--privproto=[None]" in calls[0]
    assert not any(a.startswith("--privpass") for a in calls[0])


def test_v3_without_user_or_auth_is_refused():
    with pytest.raises(ExportError, match="--snmp-user"):
        kadupul_script([device("10.0.0.6", SNMP_V3)], KadupulOptions(), "t")
    no_auth = ("snmp", 161, "udp", "", {"snmp_version": "3", "snmp_security_level": "noAuthNoPriv"})
    with pytest.raises(ExportError, match="needs SNMPv3 auth"):
        kadupul_script([device("10.0.0.6", no_auth)], KadupulOptions(snmp_user="ops"), "t")


def test_non_snmp_hosts_use_tcp_or_icmp_ping(tmp_path):
    devices = [
        device("10.0.0.7", ("http", 8080, "tcp", "", {})),
        device("10.0.0.8"),
        {"ip": "10.0.0.9", "alive": False},
    ]
    _, calls = run_script(tmp_path, kadupul_script(devices, KadupulOptions(), "t"))

    assert calls[0][4:] == [
        "--version=0",
        "--avail=ping",
        "--ping_method=tcp",
        "--ping_port=8080",
        "--notes=netprobe: http:8080/tcp",
    ]
    assert calls[1][4:] == ["--version=0", "--avail=ping", "--ping_method=icmp"]
    assert len(calls) == 2


def test_hostile_scan_data_stays_inside_arguments(tmp_path):
    canary = tmp_path / "pwned"
    evil = f"$(touch {canary})"
    devices = [
        device(
            "10.0.0.10", ("http", 80, "tcp", f"nginx'; touch {canary}; '`id`", {}), hostname=evil
        ),
        device("10.0.0.11", hostname="dup.lab"),
        device("10.0.0.12", hostname="dup.lab"),
    ]
    result, calls = run_script(tmp_path, kadupul_script(devices, KadupulOptions(), f"x\n{evil}"))

    assert result.returncode == 0, result.stderr
    assert not canary.exists()
    assert calls[0][1] == "--description=10.0.0.10"  # unsafe hostname falls back to the IP
    assert calls[0][-1].startswith("--notes=netprobe: http:80/tcp nginx'; touch ")
    assert [c[1] for c in calls[1:]] == ["--description=dup.lab", "--description=dup.lab-10.0.0.12"]


def test_failed_adds_make_the_script_fail(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "php").write_text("#!/bin/sh\nexit 1\n")
    (bin_dir / "php").chmod(0o755)
    path = tmp_path / "s.sh"
    path.write_text(kadupul_script([device("10.0.0.1"), device("10.0.0.2")], KadupulOptions(), "t"))
    result = subprocess.run(
        ["sh", str(path)],
        env={"PATH": f"{bin_dir}:/usr/bin:/bin"},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "2 device(s) not added" in result.stderr


@pytest.mark.parametrize(
    ("devices", "opts", "message"),
    [
        ([device("-oX")], KadupulOptions(), "Invalid target"),
        (
            [device("10.0.0.1", ("snmp", 1, "udp", "", {"snmp_version": "2c"}))],
            KadupulOptions(),
            "outside",
        ),
    ],
)
def test_invalid_data_is_refused(devices, opts, message):
    with pytest.raises(ExportError, match=message):
        kadupul_script(devices, opts, "t")


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"template": -1}, "template"),
        ({"snmp_user": "a b"}, "user names"),
        ({"auth_protocol": "X"}, "protocol"),
    ],
)
def test_bad_options(kwargs, message):
    with pytest.raises(ExportError, match=message):
        KadupulOptions(**kwargs)


def test_include_credentials_embeds_quoted_literals(tmp_path):
    opts = KadupulOptions(community="it's", include_credentials=True)
    script = kadupul_script([device("10.0.0.5", SNMP_V2)], opts, "t")

    assert "WARNING: this file contains SNMP credentials" in script
    assert "NETPROBE_SNMP_COMMUNITY" not in script
    _, calls = run_script(tmp_path, script)
    assert "--community=it's" in calls[0]


def test_include_credentials_without_value_is_refused():
    with pytest.raises(ExportError, match="needs a value for --community"):
        kadupul_script([device("10.0.0.5", SNMP_V2)], KadupulOptions(include_credentials=True), "t")


def test_write_script_modes(tmp_path):
    secret = tmp_path / "secret.sh"
    secret.write_text("old")
    secret.chmod(0o644)
    write_script(secret, "x", secret=True)
    write_script(tmp_path / "plain.sh", "y", secret=False)

    assert stat.S_IMODE(secret.stat().st_mode) == 0o600
    assert secret.read_text() == "x"


# --- CLI


def snapshot(tmp_path):
    devices = [
        Device(
            ip="10.0.0.5",
            alive=True,
            hostname="sw1",
            services=[Service("snmp", 161, "udp", "open", "Linux", {"snmp_version": "2c"})],
        ),
        Device(
            ip="10.0.0.6", alive=True, services=[Service("ssh", 22, "tcp", "open", "OpenSSH_10.0")]
        ),
    ]
    path = tmp_path / "snap.json"
    write_snapshot(path, "10.0.0.0/29", DEFAULT_SERVICES, devices)
    return path


def test_cli_export_without_credentials(tmp_path, monkeypatch, caplog):
    monkeypatch.setenv("NETPROBE_SNMP_COMMUNITY", "c0mmunity")
    out = tmp_path / "import.sh"
    result = runner.invoke(
        cli.app, ["export", str(snapshot(tmp_path)), "-o", str(out), "--template", "3"]
    )

    assert result.exit_code == 0, result.output
    text = out.read_text()
    assert "c0mmunity" not in text and "c0mmunity" not in caplog.text
    assert "--template=3" in text
    assert "cli/add_device.php" in text


def test_cli_export_with_credentials(tmp_path, monkeypatch, caplog):
    monkeypatch.setenv("NETPROBE_SNMP_COMMUNITY", "c0mmunity")
    out = tmp_path / "import.sh"
    result = runner.invoke(
        cli.app, ["export", str(snapshot(tmp_path)), "-o", str(out), "--include-credentials"]
    )

    assert result.exit_code == 0, result.output
    assert "--community=c0mmunity" in out.read_text()
    assert stat.S_IMODE(os.stat(out).st_mode) == 0o600
    assert "contains SNMP credentials" in caplog.text
    assert "c0mmunity" not in caplog.text + result.output


@pytest.mark.parametrize(
    "args",
    [["--include-credentials"], ["--template", "-1"]],
)
def test_cli_export_refusals_exit_2(tmp_path, monkeypatch, args):
    monkeypatch.delenv("NETPROBE_SNMP_COMMUNITY", raising=False)
    result = runner.invoke(
        cli.app, ["export", str(snapshot(tmp_path)), "-o", str(tmp_path / "x.sh"), *args]
    )
    assert result.exit_code == 2


def test_cli_export_bad_input_and_unwritable_output(tmp_path):
    assert (
        runner.invoke(
            cli.app, ["export", str(tmp_path / "none.json"), "-o", str(tmp_path / "x.sh")]
        ).exit_code
        == 2
    )
    out = tmp_path / "missing" / "x.sh"
    assert (
        runner.invoke(cli.app, ["export", str(snapshot(tmp_path)), "-o", str(out)]).exit_code == 1
    )


def test_cli_scan_writes_kadupul_script_from_sh_extension(tmp_path):
    from test_cli import patched_scanner

    out = tmp_path / "import.sh"
    devices = [Device(ip="10.0.0.6", alive=True, services=[Service("ssh", 22, "tcp", "open")])]
    with patched_scanner(devices):
        result = runner.invoke(cli.app, ["scan", "10.0.0.6", "-q", "-o", str(out)])

    assert result.exit_code == 0, result.output
    assert "--ping_port=22" in out.read_text()


def test_cli_scan_kadupul_export_error_exits_2(tmp_path):
    from test_cli import patched_scanner

    devices = [
        Device(
            ip="10.0.0.6",
            alive=True,
            services=[
                Service(
                    "snmp",
                    161,
                    "udp",
                    "open",
                    "",
                    {"snmp_version": "3", "snmp_security_level": "authPriv"},
                )
            ],
        )
    ]
    with patched_scanner(devices):
        result = runner.invoke(
            cli.app, ["scan", "10.0.0.6", "-q", "-f", "kadupul", "-o", str(tmp_path / "x.txt")]
        )

    assert result.exit_code == 2
    assert "--snmp-user" in result.output
