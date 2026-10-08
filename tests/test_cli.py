import json
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
    factory.assert_called_once_with(backend="nmap", timeout=0.5, concurrency=8)


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
