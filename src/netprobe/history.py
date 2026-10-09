# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Opt-in SQLite inventory snapshots and comparisons that preserve uncertainty."""

from __future__ import annotations

import ipaddress
import json
import os
import sqlite3
import tempfile
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from netprobe.scanner import validate_target

type JSONDocument = dict[str, Any]
type SnapshotRow = tuple[Any, ...]

HISTORY_APPLICATION_ID = 0x4E505242
HISTORY_SCHEMA_VERSION = 1
SUMMARY_ERROR = "Invalid snapshot summary"
PORT_ERROR = "Invalid snapshot port selection"
OBSERVATION_ERROR = "Invalid snapshot observations"


def check_writable_path(path: Path) -> None:
    """Check output access using a temporary sibling, leaving the destination intact."""
    if path.is_symlink():
        raise ValueError(f"Destination must not be a symbolic link: {path}")
    if path.exists() and (not path.is_file() or not os.access(path, os.W_OK)):
        raise ValueError(f"Destination is not a writable regular file: {path}")
    try:
        with tempfile.TemporaryFile(dir=path.parent) as stream:
            stream.write(b"netprobe preflight\n")
            stream.flush()
    except OSError as exc:
        raise ValueError(f"Destination directory is not writable: {path.parent}: {exc}") from exc


class HistoryStore:
    """Opt-in SQLite snapshots, stored atomically and compared only at equal scope."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def _connect(self, readonly: bool = False) -> sqlite3.Connection:
        if self.path.is_symlink():
            raise ValueError("History database must not be a symbolic link")
        if readonly:
            return sqlite3.connect(self.path.absolute().as_uri() + "?mode=ro", uri=True, timeout=5)
        return sqlite3.connect(self.path, timeout=5)

    @staticmethod
    def _validate(connection: sqlite3.Connection, allow_empty: bool = False) -> None:
        app_id = connection.execute("PRAGMA application_id").fetchone()[0]
        schema = connection.execute("PRAGMA user_version").fetchone()[0]
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        if allow_empty and app_id == 0 and schema == 0 and not tables:
            return
        if app_id != HISTORY_APPLICATION_ID or schema != HISTORY_SCHEMA_VERSION:
            raise ValueError("Not a supported netprobe history database")
        connection.execute(
            "SELECT id, started_at, finished_at, metadata, devices FROM scans LIMIT 0"
        )

    def validate_existing(self) -> None:
        if self.path.exists():
            with closing(self._connect(readonly=True)) as connection, connection:
                self._validate(connection, allow_empty=True)

    def initialize(self) -> None:
        check_writable_path(self.path)
        with closing(self._connect()) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            self._validate(connection, allow_empty=True)
            connection.execute("""CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY, started_at TEXT NOT NULL, finished_at TEXT NOT NULL,
                metadata TEXT NOT NULL, devices TEXT NOT NULL
            )""")
            connection.execute(f"PRAGMA application_id = {HISTORY_APPLICATION_ID}")
            connection.execute(f"PRAGMA user_version = {HISTORY_SCHEMA_VERSION}")

    def save(self, metadata: JSONDocument, devices: list[JSONDocument], started_at: str) -> int:
        metadata = {
            **metadata,
            "summary": {
                "hosts": len(devices),
                "responsive": sum(device["alive"] for device in devices),
                "hosts_with_errors": sum(bool(device["errors"]) for device in devices),
            },
        }
        raw_metadata, raw_devices = json.dumps(metadata), json.dumps(devices)
        self._decode((0, started_at, utc_now(), raw_metadata, raw_devices))
        with closing(self._connect()) as connection, connection:
            self._validate(connection)
            cursor = connection.execute(
                "INSERT INTO scans(started_at, finished_at, metadata, devices) VALUES (?, ?, ?, ?)",
                (started_at, utc_now(), raw_metadata, raw_devices),
            )
            if cursor.lastrowid is None:
                raise sqlite3.DatabaseError("Snapshot insert did not return an ID")
            return cursor.lastrowid

    def list_scans(self, limit: int = 20) -> list[JSONDocument]:
        with closing(self._connect(readonly=True)) as connection, connection:
            self._validate(connection)
            rows = connection.execute(
                "SELECT id, started_at, finished_at, metadata, devices FROM scans ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._decode(row) for row in rows]

    def list_summaries(self, limit: int = 20) -> list[JSONDocument]:
        # Do not load every device payload merely to list historical runs.
        with closing(self._connect(readonly=True)) as connection, connection:
            self._validate(connection)
            rows = connection.execute(
                "SELECT id, started_at, finished_at, metadata FROM scans ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        summaries = []
        for scan_id, started_at, finished_at, raw_metadata in rows:
            metadata = json.loads(raw_metadata)
            if not isinstance(metadata, dict) or metadata.get("schema_version") != 1:
                raise ValueError("Unsupported snapshot metadata schema")
            summary = validate_summary(metadata)
            summaries.append(
                {
                    "id": scan_id,
                    "started_at": started_at,
                    "finished_at": finished_at,
                    "metadata": metadata,
                    **summary,
                }
            )
        return summaries

    def get(self, scan_id: int) -> JSONDocument:
        with closing(self._connect(readonly=True)) as connection, connection:
            self._validate(connection)
            row = connection.execute(
                "SELECT id, started_at, finished_at, metadata, devices FROM scans WHERE id = ?",
                (scan_id,),
            ).fetchone()
        if row is None:
            raise ValueError(f"Scan {scan_id} not found")
        return self._decode(row)

    @staticmethod
    def _decode(row: SnapshotRow) -> JSONDocument:
        metadata, devices = json.loads(row[3]), json.loads(row[4])
        if not isinstance(metadata, dict) or metadata.get("schema_version") != 1:
            raise ValueError("Unsupported snapshot metadata schema")
        ports = validate_ports(metadata)
        if not isinstance(devices, list):
            raise ValueError(OBSERVATION_ERROR)
        seen: set[str] = set()
        for device in devices:
            validate_observation(device, ports, seen)
        return {
            "id": row[0],
            "started_at": row[1],
            "finished_at": row[2],
            "metadata": metadata,
            "devices": devices,
        }


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def compare_scans(before: JSONDocument, after: JSONDocument) -> JSONDocument:
    """Compare observations without inferring disappearance from failed scans."""
    if before["id"] >= after["id"]:
        raise ValueError("Earlier scan ID must be less than later scan ID")
    old = {device["ip"]: device for device in before["devices"]}
    new = {device["ip"]: device for device in after["devices"]}
    if old.keys() != new.keys() or before["metadata"]["ports"] != after["metadata"]["ports"]:
        raise ValueError("Cannot compare scans with different targets or selected ports")
    report: JSONDocument = {
        "before": before["id"],
        "after": after["id"],
        "newly_responsive": [],
        "no_longer_responding": [],
        "uncertain_hosts": [],
        "status_changes": [],
        "port_changes": [],
    }
    for ip in sorted(old, key=host_sort_key):
        compare_host_observations(report, ip, old[ip], new[ip])
    return report


def host_sort_key(value: str) -> tuple[int, int, str]:
    try:
        address = ipaddress.ip_address(value)
        return address.version, int(address), ""
    except ValueError:
        return 99, 0, value


def validate_summary(metadata: JSONDocument) -> JSONDocument:
    summary = metadata.get("summary", {})
    if not isinstance(summary, dict) or set(summary) != {
        "hosts",
        "responsive",
        "hosts_with_errors",
    }:
        raise ValueError(SUMMARY_ERROR)
    if any(type(count) is not int or count < 0 for count in summary.values()):
        raise ValueError(SUMMARY_ERROR)
    if summary["responsive"] > summary["hosts"] or summary["hosts_with_errors"] > summary["hosts"]:
        raise ValueError(SUMMARY_ERROR)
    return summary


def validate_ports(metadata: JSONDocument) -> list[str]:
    ports = metadata.get("ports")
    if not isinstance(ports, list) or not ports or len(ports) != len(set(ports)):
        raise ValueError(PORT_ERROR)
    for port in ports:
        if not isinstance(port, str):
            raise ValueError(PORT_ERROR)
        number, separator, protocol = port.partition("/")
        if (
            not separator
            or not number.isdecimal()
            or not 1 <= int(number) <= 65535
            or protocol not in ("tcp", "udp")
            or number != str(int(number))
        ):
            raise ValueError(PORT_ERROR)
    return ports


def validate_observation(device: Any, ports: list[str], seen: set[str]) -> None:
    states = {
        "open",
        "closed",
        "filtered",
        "unfiltered",
        "open|filtered",
        "closed|filtered",
        "unknown",
    }
    if not isinstance(device, dict):
        raise ValueError(OBSERVATION_ERROR)
    ip = device.get("ip")
    if not isinstance(ip, str) or "%" in ip or validate_target(ip) != ip or ip in seen:
        raise ValueError("Snapshot contains invalid or duplicate IP addresses")
    seen.add(ip)
    errors, observed = device.get("errors"), device.get("port_states")
    if (
        type(device.get("alive")) is not bool
        or device.get("status") not in ("up", "unknown", "error", "unresponsive")
        or not isinstance(errors, list)
        or any(not isinstance(error, str) for error in errors)
        or not isinstance(observed, dict)
        or not set(observed).issubset(ports)
        or any(state not in states for state in observed.values())
    ):
        raise ValueError(OBSERVATION_ERROR)


def compare_host_observations(
    report: JSONDocument, ip: str, previous: JSONDocument, current: JSONDocument
) -> None:
    if previous["status"] != current["status"]:
        report["status_changes"].append(
            {"ip": ip, "before": previous["status"], "after": current["status"]}
        )
    if previous["errors"] or current["errors"]:
        report["uncertain_hosts"].append(ip)
    if not previous["alive"] and current["alive"] and previous["status"] == "unresponsive":
        report["newly_responsive"].append(ip)
    if previous["alive"] and not current["alive"] and current["status"] == "unresponsive":
        report["no_longer_responding"].append(ip)
    for port in sorted(previous["port_states"].keys() & current["port_states"].keys()):
        old_state, new_state = previous["port_states"][port], current["port_states"][port]
        if old_state != new_state and "unknown" not in (old_state, new_state):
            report["port_changes"].append(
                {"ip": ip, "port": port, "before": old_state, "after": new_state}
            )
