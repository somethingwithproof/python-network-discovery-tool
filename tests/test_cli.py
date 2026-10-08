import json
import socket
from importlib.metadata import version
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from netprobe import cli
from netprobe.models import Device
from netprobe.scanner import BackendUnavailableError

runner = CliRunner()


def patched_scanner(devices):
    scanner = MagicMock()

    async def scan_network(network, progress=None):
        return devices

    scanner.scan_network = scan_network
    return patch.object(cli, "NetworkScanner", return_value=scanner)


def test_cli_version():
    result = runner.invoke(cli.app, ["version"])

    assert result.exit_code == 0
    assert f"v{version('netprobe')}" in result.output


@pytest.mark.parametrize(
    ("args", "suffix"),
    [(["-o"], ".json"), (["-o"], ".csv"), (["-o"], ".txt"), (["-f", "csv", "-o"], ".json")],
)
def test_cli_scan_writes_report(tmp_path, args, suffix):
    out = tmp_path / f"report{suffix}"
    with patched_scanner([Device(ip="10.0.0.1", alive=True)]):
        result = runner.invoke(
            cli.app, ["scan", "10.0.0.1", "--quiet", "--verbose", *args, str(out)]
        )

    assert result.exit_code == 0, result.output
    text = out.read_text()
    if suffix == ".csv" or "csv" in args:
        assert text.startswith("ip,alive")
    else:
        assert json.loads(text)[0]["ip"] == "10.0.0.1"


def test_cli_scan_prints_table_without_output_file():
    with patched_scanner([Device(ip="10.0.0.1", alive=True, ssh=True)]):
        result = runner.invoke(cli.app, ["scan", "10.0.0.1"])

    assert result.exit_code == 0
    assert "10.0.0.1" in result.output


def test_cli_passes_engine_options():
    with patched_scanner([]) as factory:
        result = runner.invoke(
            cli.app,
            ["scan", "10.0.0.1", "--backend", "nmap", "--timeout", "0.5", "--concurrency", "8"],
        )

    assert result.exit_code == 0, result.output
    kwargs = factory.call_args.kwargs
    assert (kwargs["backend"], kwargs["timeout"], kwargs["concurrency"]) == ("nmap", 0.5, 8)
    assert [s.name for s in kwargs["services"]] == ["ssh", "snmp", "mysql", "http", "https"]


def test_cli_service_selection_reaches_scanner(tmp_path):
    config = tmp_path / "netprobe.toml"
    config.write_text("[services.redis]\nport = 6379\n")
    with patched_scanner([]) as factory:
        result = runner.invoke(
            cli.app,
            [
                "scan",
                "10.0.0.1",
                "--config",
                str(config),
                "--services",
                "ssh,redis",
                "--ports",
                "ssh=2222,8080",
            ],
        )

    assert result.exit_code == 0, result.output
    specs = factory.call_args.kwargs["services"]
    assert [(s.name, s.port, s.probe) for s in specs] == [
        ("ssh", 2222, "ssh"),
        ("redis", 6379, "tcp"),
        ("tcp-8080", 8080, "tcp"),
    ]


@pytest.mark.parametrize(
    "args", [["--services", "telnet"], ["--ports", "ssh=0"], ["--config", "/nonexistent.toml"]]
)
def test_cli_bad_service_options_exit_2(args):
    result = runner.invoke(cli.app, ["scan", "10.0.0.1", *args])

    assert result.exit_code == 2
    assert "Error:" in result.output


def test_cli_rejects_zero_concurrency():
    result = runner.invoke(cli.app, ["scan", "10.0.0.1", "--concurrency", "0"])
    assert result.exit_code == 2


def test_cli_invalid_network_exits_2_with_message():
    result = runner.invoke(cli.app, ["scan", "999.1.1.1/24"])

    assert result.exit_code == 2
    assert "Invalid network format" in result.output
    assert "Traceback" not in result.output


def test_cli_unavailable_backend_exits_1():
    with patch.object(
        cli, "NetworkScanner", side_effect=BackendUnavailableError("nmap is not available")
    ):
        result = runner.invoke(cli.app, ["scan", "127.0.0.1", "--backend", "nmap"])

    assert result.exit_code == 1
    assert "nmap is not available" in result.output


def test_cli_unwritable_output_exits_1(tmp_path):
    out = tmp_path / "missing-dir" / "report.json"
    with patched_scanner([Device(ip="10.0.0.1", alive=True)]):
        result = runner.invoke(cli.app, ["scan", "10.0.0.1", "--quiet", "-o", str(out)])

    assert result.exit_code == 1
    assert "cannot write" in result.output


@pytest.mark.parametrize(
    "secrets",
    [
        {"NETPROBE_SNMP_COMMUNITY": "community-s3cret"},
        {
            "NETPROBE_SNMP_USER": "netprobe",
            "NETPROBE_SNMP_AUTH_KEY": "auth-s3cret",
            "NETPROBE_SNMP_PRIV_KEY": "priv-s3cret",
        },
    ],
    ids=["v2c", "v3"],
)
def test_cli_snmp_secrets_reach_probe_but_never_output(tmp_path, monkeypatch, caplog, secrets):
    for name, value in secrets.items():
        monkeypatch.setenv(name, value)
    out = tmp_path / "scan.json"

    # A bound UDP socket that never answers: the real SNMP GET runs and times out.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as agent:
        agent.bind(("127.0.0.1", 0))
        port = agent.getsockname()[1]
        result = runner.invoke(
            cli.app,
            [
                *("scan", "127.0.0.1", "-v", "-o", str(out), "--timeout", "0.2"),
                *(
                    "--services",
                    "snmp",
                    "--ports",
                    f"snmp={port}",
                    "--snmp-priv-protocol",
                    "AES256",
                ),
            ],
        )

    assert result.exit_code == 0, result.output
    service = json.loads(out.read_text())[0]["services"][0]
    assert "No SNMP response" in service["details"]["snmp_error"]
    everything = out.read_text() + result.output + caplog.text
    for name, value in secrets.items():
        if name != "NETPROBE_SNMP_USER":
            assert value not in everything
    assert "process list" not in caplog.text  # env vars do not trigger the warning


def test_cli_warns_when_secret_given_as_option(caplog):
    with patched_scanner([]):
        result = runner.invoke(cli.app, ["scan", "10.0.0.1", "--snmp-community", "c0mmunity"])

    assert result.exit_code == 0, result.output
    assert "visible in the process list" in caplog.text
    assert "NETPROBE_SNMP_COMMUNITY" in caplog.text
    assert "c0mmunity" not in caplog.text


@pytest.mark.parametrize(
    "args",
    [
        ["--snmp-community", "c", "--snmp-user", "u"],
        ["--snmp-user", "u", "--snmp-priv-key", "privpass1"],
        ["--snmp-auth-key", "authpass1"],
    ],
    ids=["v2c-and-v3", "priv-without-auth", "key-without-user"],
)
def test_cli_refuses_ambiguous_or_weakened_snmp(args):
    result = runner.invoke(cli.app, ["scan", "10.0.0.1", *args])

    assert result.exit_code == 2
    assert "Error:" in result.output


def test_tracebacks_never_show_locals():
    assert cli.app.pretty_exceptions_show_locals is False


def test_cli_rejects_excessive_concurrency():
    result = runner.invoke(cli.app, ["scan", "10.0.0.1", "--concurrency", "100000"])
    assert result.exit_code == 2


def test_cli_rejects_scan_over_probe_cap():
    result = runner.invoke(cli.app, ["scan", "10.0.0.0/16", "--ports", "1,2,3,4,5"])

    assert result.exit_code == 2
    assert "Scan too large" in result.output


def test_cli_scanner_receives_snmp_and_tls_settings(tmp_path):
    with patched_scanner([]) as factory:
        result = runner.invoke(
            cli.app,
            [
                *("scan", "10.0.0.1", "--snmp-user", "ops", "--snmp-auth-protocol", "SHA512"),
                *("--tls-ca-file", str(tmp_path / "ca.pem")),
            ],
        )

    assert result.exit_code == 0, result.output
    kwargs = factory.call_args.kwargs
    assert kwargs["snmp"].user == "ops"
    assert kwargs["snmp"].auth_protocol == "SHA512"
    assert kwargs["tls_ca_file"] == str(tmp_path / "ca.pem")


def test_cli_rejects_unknown_auth_protocol():
    result = runner.invoke(cli.app, ["scan", "10.0.0.1", "--snmp-auth-protocol", "CRC32"])
    assert result.exit_code == 2


def test_cli_scan_saves_snapshot(tmp_path):
    out = tmp_path / "snap.json"
    with patched_scanner([Device(ip="10.0.0.1", alive=True), Device(ip="10.0.0.2")]):
        result = runner.invoke(
            cli.app, ["scan", "10.0.0.0/30", "-q", "--services", "ssh", "--save-snapshot", str(out)]
        )

    assert result.exit_code == 0, result.output
    document = json.loads(out.read_text())
    assert document["target"] == "10.0.0.0/30"
    assert [s["name"] for s in document["services"]] == ["ssh"]
    assert [d["ip"] for d in document["devices"]] == ["10.0.0.1"]


def test_cli_scan_unwritable_snapshot_exits_1(tmp_path):
    with patched_scanner([]):
        result = runner.invoke(
            cli.app, ["scan", "10.0.0.1", "-q", "--save-snapshot", str(tmp_path / "no" / "s.json")]
        )
    assert result.exit_code == 1
