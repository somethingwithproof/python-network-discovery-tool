# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""The public CLI contract, exercised through real `python -m netprobe` processes.

Each command's streams, exit codes and JSON documents are what scripts depend
on, and the versioning policy treats a change to any of them as breaking.
Every probe goes to listeners this module opens on 127.0.0.1.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
from dataclasses import dataclass
from importlib.metadata import entry_points, version
from pathlib import Path

import pytest
import typer
from conftest import validator

from netprobe import cli

# Typer forces colour under CI (GITHUB_ACTIONS, FORCE_COLOR); the contract is
# the text, not its styling.
ANSI = re.compile(r"\x1b\[[0-9;]*m")
COMMANDS = ("scan", "preflight", "profiles", "history", "compare", "diff", "export", "version")


def netprobe(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    # A clean environment, so the caller's NETPROBE_* settings cannot leak in.
    env = {k: v for k, v in os.environ.items() if not k.startswith("NETPROBE_")}
    return subprocess.run(
        [sys.executable, "-m", "netprobe", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
        timeout=120,
        check=False,
    )


def listener() -> socket.socket:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen()
    return sock


@dataclass(frozen=True)
class Lab:
    root: Path
    config: Path
    stdout_report: str
    report: Path
    open_snapshot: Path
    closed_snapshot: Path
    history: Path


@pytest.fixture(scope="module")
def lab(tmp_path_factory: pytest.TempPathFactory) -> Lab:
    """Two real loopback scans: the lab port open, then closed."""
    root = tmp_path_factory.mktemp("contract")
    config, history = root / "lab.toml", root / "history.sqlite3"
    scan = ("scan", "127.0.0.1", "--config", str(config), "--services", "lab")
    with listener() as server:
        config.write_text(f"[services.lab]\nport = {server.getsockname()[1]}\n")
        on_stdout = netprobe(*scan, "--format", "json", cwd=root)
        assert on_stdout.returncode == 0, on_stdout.stderr
        first = netprobe(
            *scan,
            *("-o", "report.json", "--save-snapshot", "open.json", "--history", str(history)),
            cwd=root,
        )
        assert first.returncode == 0, first.stderr
    second = netprobe(*scan, "--save-snapshot", "closed.json", "--history", str(history), cwd=root)
    assert second.returncode == 0, second.stderr
    return Lab(
        root,
        config,
        on_stdout.stdout,
        root / "report.json",
        root / "open.json",
        root / "closed.json",
        history,
    )


def test_every_command_is_covered_by_this_contract() -> None:
    registered = typer.main.get_command(cli.app).commands  # type: ignore[attr-defined]
    assert set(registered) == set(COMMANDS)


def test_console_script_runs_the_typer_app() -> None:
    (script,) = entry_points(group="console_scripts", name="netprobe")
    assert script.value == "netprobe.cli:app"
    assert script.load() is cli.app


@pytest.mark.parametrize("command", COMMANDS)
def test_help_goes_to_stdout_and_exits_0(command: str, tmp_path: Path) -> None:
    result = netprobe(command, "--help", cwd=tmp_path)
    assert result.returncode == 0
    assert f"Usage: python -m netprobe {command} " in ANSI.sub("", result.stdout)
    assert result.stderr == ""


@pytest.mark.parametrize("command", COMMANDS)
def test_unknown_option_exits_2_with_nothing_on_stdout(command: str, tmp_path: Path) -> None:
    result = netprobe(command, "--no-such-option", cwd=tmp_path)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "No such option" in ANSI.sub("", result.stderr)


def test_version_flag_prints_name_and_version(tmp_path: Path) -> None:
    result = netprobe("--version", cwd=tmp_path)
    assert result.returncode == 0
    assert result.stdout == f"netprobe {version('netprobe')}\n"


def test_json_report_on_stdout(lab: Lab) -> None:
    report = json.loads(lab.stdout_report)
    validator("report").validate(report)
    assert report["complete"] is True
    assert report["devices"][0]["services"][0]["state"] == "open"


def test_written_report_and_snapshots_validate(lab: Lab) -> None:
    validator("report").validate(json.loads(lab.report.read_text()))
    for snapshot in (lab.open_snapshot, lab.closed_snapshot):
        validator("snapshot").validate(json.loads(snapshot.read_text()))


@pytest.mark.parametrize(
    ("args", "schema", "status"),
    [
        (("history",), "history", 0),
        (("compare", "1", "2"), "compare", 0),
        (("diff", "open.json", "open.json", "-f", "json"), "diff", 0),
        (("diff", "open.json", "closed.json", "-f", "json"), "diff", 3),
        (("preflight", "127.0.0.1", "--config", "lab.toml", "--services", "lab"), "preflight", 0),
    ],
)
def test_json_commands_write_one_valid_document(
    lab: Lab, args: tuple[str, ...], schema: str, status: int
) -> None:
    if args[0] in ("history", "compare"):
        args = (*args, "--history", str(lab.history))
    result = netprobe(*args, cwd=lab.root)
    assert result.returncode == status, result.stderr
    validator(schema).validate(json.loads(result.stdout))


def test_profiles_lists_the_shipped_example(tmp_path: Path) -> None:
    example = Path(__file__).parents[1] / "netprobe.example.toml"
    result = netprobe("profiles", "--config", str(example), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)


def test_export_writes_a_script(lab: Lab) -> None:
    result = netprobe("export", "report.json", "-o", "add.sh", cwd=lab.root)
    assert result.returncode == 0, result.stderr
    script = (lab.root / "add.sh").read_text()
    assert script.startswith("#!/bin/sh\n")
    assert "add_device.php" in script


@pytest.mark.parametrize(
    ("args", "status"),
    [
        (("scan", "-bad.example"), 2),
        (("scan", "10.0.0.0/8"), 2),
        (("scan", "127.0.0.1", "--deadline", "0"), 2),
        (("diff", "absent.json", "absent.json"), 2),
        (("export", "absent.json", "-o", "add.sh"), 2),
        (("history", "--history", "absent.sqlite3"), 1),
        (("compare", "1", "9", "--history", "history.sqlite3"), 1),
        (("profiles", "--config", "absent.toml"), 2),
    ],
)
def test_failures_exit_with_documented_status_and_empty_stdout(
    lab: Lab, args: tuple[str, ...], status: int
) -> None:
    result = netprobe(*args, cwd=lab.root)
    assert result.returncode == status, result.stderr
    assert result.stdout == ""
    assert result.stderr


def test_deadline_exit_4_writes_an_incomplete_report(tmp_path: Path) -> None:
    # The listener accepts but never answers, so the HTTP probe would wait its
    # whole five-second timeout; the one-second deadline stops it first.
    with listener() as silent:
        port = silent.getsockname()[1]
        (tmp_path / "slow.toml").write_text(
            f"[services.slow]\nport = {port}\nprobe = 'http'\ntimeout = 5\n"
        )
        result = netprobe(
            *("scan", "127.0.0.1", "--config", "slow.toml", "--services", "slow"),
            *("--deadline", "1", "-o", "partial.json", "--save-snapshot", "snap.json"),
            cwd=tmp_path,
        )

    assert result.returncode == 4, result.stderr
    assert "deadline" in result.stderr
    report = json.loads((tmp_path / "partial.json").read_text())
    validator("report").validate(report)
    assert report["complete"] is False
    assert report["devices"] == []
    assert not (tmp_path / "snap.json").exists()
