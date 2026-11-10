# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Support for files, variables and commands from before the rename to hostcensus."""

from __future__ import annotations

import json
import subprocess
import sys
from importlib.metadata import entry_points
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from conftest import FIXTURES, validator
from jsonschema import ValidationError
from typer.testing import CliRunner

from hostcensus import cli, compat
from hostcensus.diff import compare, load_inventory
from hostcensus.models import Device

runner = CliRunner()
NETPROBE = "NETPROBE_SNMP_USER"
HOSTCENSUS = "HOSTCENSUS_SNMP_USER"


@pytest.fixture
def clean_env(monkeypatch):
    for name in list(compat.os.environ):
        if name.startswith(("NETPROBE_", "HOSTCENSUS_")):
            monkeypatch.delenv(name)


# --- environment variables ----------------------------------------------------


def test_env_new_name_only(clean_env, monkeypatch, capsys):
    monkeypatch.setenv(HOSTCENSUS, "new")
    assert compat.get_env("SNMP_USER") == "new"
    assert capsys.readouterr().err == ""


def test_env_old_name_only_is_used_and_warns_once_without_the_value(clean_env, monkeypatch, capsys):
    monkeypatch.setenv(NETPROBE, "s3cret-value")
    assert compat.get_env("SNMP_USER") == "s3cret-value"
    assert compat.get_env("SNMP_USER") == "s3cret-value"
    err = capsys.readouterr().err
    assert err.count("warning:") == 1
    assert NETPROBE in err
    assert "s3cret-value" not in err


def test_env_both_set_prefers_the_new_name(clean_env, monkeypatch):
    monkeypatch.setenv(NETPROBE, "old")
    monkeypatch.setenv(HOSTCENSUS, "new")
    assert compat.get_env("SNMP_USER") == "new"
    assert compat.os.environ[NETPROBE] == "old"


def test_env_neither_set(clean_env, capsys):
    assert compat.get_env("SNMP_USER") is None
    assert capsys.readouterr().err == ""


def test_env_lookup_leaves_a_caller_supplied_mapping_alone_of_other_names(clean_env):
    environ = {"NETPROBE_A": "1", "OTHER": "2"}
    assert compat.promote_legacy_env(environ) == ["NETPROBE_A"]
    assert environ == {"NETPROBE_A": "1", "HOSTCENSUS_A": "1", "OTHER": "2"}


def test_cli_honours_old_variables_through_typer_options(tmp_path, clean_env, monkeypatch, capsys):
    key = tmp_path / "auth"
    key.write_text("auth-passphrase")
    monkeypatch.setenv("NETPROBE_SNMP_AUTH_KEY_FILE", str(key))
    monkeypatch.setenv("NETPROBE_SNMP_USER", "ops")
    scanner = MagicMock()

    async def scan_network(network, progress=None):
        return [Device(ip="10.0.0.1", alive=True)]

    scanner.scan_network = scan_network
    with patch.object(cli, "NetworkScanner", return_value=scanner) as factory:
        result = runner.invoke(cli.app, ["scan", "10.0.0.1"])

    assert result.exit_code == 0, result.output
    snmp = factory.call_args.kwargs["snmp"]
    assert (snmp.user, snmp.auth_key) == ("ops", "auth-passphrase")
    assert "auth-passphrase" not in result.output + capsys.readouterr().err


def test_cli_new_variable_beats_old_one(clean_env, monkeypatch):
    monkeypatch.setenv(NETPROBE, "old")
    monkeypatch.setenv(HOSTCENSUS, "new")
    scanner = MagicMock()

    async def scan_network(network, progress=None):
        return []

    scanner.scan_network = scan_network
    with patch.object(cli, "NetworkScanner", return_value=scanner) as factory:
        key = "HOSTCENSUS_SNMP_AUTH_KEY"
        monkeypatch.setenv(key, "k" * 12)
        result = runner.invoke(cli.app, ["scan", "10.0.0.1"])

    assert result.exit_code == 0, result.output
    assert factory.call_args.kwargs["snmp"].user == "new"


def test_export_reads_the_old_variable_for_included_credentials(tmp_path, clean_env, monkeypatch):
    from hostcensus.config import DEFAULT_SERVICES
    from hostcensus.diff import write_snapshot
    from hostcensus.models import Service

    monkeypatch.setenv("NETPROBE_SNMP_COMMUNITY", "c0mmunity")
    snapshot = tmp_path / "snap.json"
    device = Device(
        ip="10.0.0.5",
        alive=True,
        services=[Service("snmp", 161, "udp", "open", "Linux", {"snmp_version": "2c"})],
    )
    write_snapshot(snapshot, "10.0.0.5", DEFAULT_SERVICES, [device])
    out = tmp_path / "import.sh"
    result = runner.invoke(
        cli.app, ["export", str(snapshot), "-o", str(out), "--include-credentials"]
    )
    assert result.exit_code == 0, result.output
    assert "--community=c0mmunity" in out.read_text()


# --- default file names -------------------------------------------------------


def test_default_path_keeps_a_file_that_still_has_the_old_name(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    old = compat.LEGACY_HISTORY
    new = compat.DEFAULT_HISTORY
    assert compat.default_path(new, new, old) == new  # neither exists
    old.write_text("")
    assert compat.default_path(new, new, old) == old
    assert "rename it" in capsys.readouterr().err
    new.write_text("")
    assert compat.default_path(new, new, old) == new  # the new name wins
    explicit = Path("elsewhere.sqlite3")
    assert compat.default_path(explicit, new, old) == explicit


def test_profiles_still_reads_netprobe_toml_by_default(tmp_path, monkeypatch):
    example = Path(__file__).parents[1] / "hostcensus.example.toml"
    monkeypatch.chdir(tmp_path)
    Path("netprobe.toml").write_text(example.read_text())
    result = runner.invoke(cli.app, ["profiles"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)


# --- persisted documents ------------------------------------------------------


@pytest.mark.parametrize("name", ["report", "snapshot"])
def test_files_written_under_the_old_name_still_load(name):
    path = FIXTURES / f"netprobe-{name}.json"
    document = json.loads(path.read_text())
    assert document["format"] == f"netprobe-{name}"
    assert "netprobe_version" in document
    validator(name, published=True).validate(document)
    inventory = load_inventory(path)
    assert inventory.target == "127.0.0.1"
    assert set(inventory.hosts) == {"127.0.0.1"}


def test_diff_compares_an_old_snapshot_with_a_new_one(tmp_path):
    old = load_inventory(FIXTURES / "netprobe-snapshot.json")
    new_path = tmp_path / "new.json"
    new_path.write_text(
        (FIXTURES / "netprobe-snapshot.json")
        .read_text()
        .replace("netprobe-snapshot", "hostcensus-snapshot")
        .replace("netprobe_version", "hostcensus_version")
    )
    assert not compare(old, load_inventory(new_path)).changed


def test_cli_diff_accepts_old_files(tmp_path):
    path = FIXTURES / "netprobe-snapshot.json"
    result = runner.invoke(cli.app, ["diff", str(path), str(path), "-f", "json"])
    assert result.exit_code == 0, result.output
    document = json.loads(result.stdout)
    assert document["format"] == "hostcensus-diff"
    validator("diff").validate(document)


@pytest.mark.parametrize("name", ["report", "snapshot", "diff", "preflight", "history", "compare"])
def test_published_schemas_name_both_spellings_of_the_format(name):
    spellings = validator(name, published=True).schema["properties"]["format"]["enum"]
    assert spellings == [f"hostcensus-{name}", f"netprobe-{name}"]


def test_a_scan_document_needs_one_version_field_but_either_will_do():
    check = validator("report", published=True)
    old = json.loads((FIXTURES / "netprobe-report.json").read_text())
    check.validate(old)
    check.validate(
        {**{k: v for k, v in old.items() if k != "netprobe_version"}, "hostcensus_version": "3.0.0"}
    )
    with pytest.raises(ValidationError, match="is not valid under any of the given schemas"):
        check.validate({k: v for k, v in old.items() if k != "netprobe_version"})


# --- deprecated command -------------------------------------------------------


def test_netprobe_console_script_is_the_deprecated_alias():
    (script,) = entry_points(group="console_scripts", name="netprobe")
    assert script.value == "hostcensus.compat:legacy_main"


def run_legacy(*args: str) -> subprocess.CompletedProcess[str]:
    code = "import sys; sys.argv[0] = 'netprobe'; from hostcensus.compat import legacy_main; legacy_main()"
    return subprocess.run(
        [sys.executable, "-c", code, *args], capture_output=True, text=True, check=False
    )


def run_current(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "hostcensus", *args], capture_output=True, text=True, check=False
    )


@pytest.mark.parametrize(
    "args",
    [
        ["--version"],
        ["profiles", "--config", "/nonexistent/hostcensus.toml"],
        ["scan", "bad target"],
    ],
    ids=["version", "error-exit", "usage-exit"],
)
def test_legacy_command_matches_hostcensus_apart_from_one_stderr_line(args):
    old, new = run_legacy(*args), run_current(*args)
    assert (old.returncode, old.stdout) == (new.returncode, new.stdout)
    lines = old.stderr.splitlines()
    assert lines[0].startswith("warning: the `netprobe` command is deprecated; use `hostcensus`")
    assert sum("deprecated" in line for line in lines) == 1
