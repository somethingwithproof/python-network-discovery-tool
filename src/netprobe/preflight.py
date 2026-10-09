"""Local-only checks performed before target scanning."""

from __future__ import annotations

import asyncio
import importlib.util
import shutil
import sqlite3
import ssl
from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal, TypedDict

from netprobe.history import HistoryStore, check_writable_path
from netprobe.models import ServiceSpec
from netprobe.scanner import MAX_PROBES, expand_targets


class Check(TypedDict):
    check: str
    status: Literal["ok", "error"]
    detail: str


class PreflightResult(TypedDict):
    target: str
    host_count: int
    services: list[dict[str, Any]]
    backend: str
    checks: list[Check]


async def _nmap_version(executable: str) -> str:
    # Fixed argv, no shell; a bounded read and deadline keep local checks bounded.
    async with asyncio.timeout(5):
        process = await asyncio.create_subprocess_exec(
            executable,
            "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        try:
            if process.stdout is None:
                raise ValueError("Nmap version output unavailable")
            output = await process.stdout.read(4096)
            await process.wait()
            first_line = output.decode("utf-8").splitlines()[0] if output else ""
            if process.returncode or not first_line.startswith("Nmap version "):
                raise ValueError("Nmap version check failed")
            return first_line[:200]
        finally:
            if process.returncode is None:
                process.kill()
                await process.communicate()


def nmap_version(executable: str) -> str:
    return asyncio.run(_nmap_version(executable))


def paths_overlap(first: Path, second: Path) -> bool:
    return first.resolve() == second.resolve() or (
        first.exists() and second.exists() and first.samefile(second)
    )


def check_plan(
    network: str,
    specs: tuple[ServiceSpec, ...],
    backend: str,
    max_hosts: int,
    exclusions: list[str],
    destinations: list[Path],
    config: Path | None = None,
    history: Path | None = None,
    tls_ca_file: Path | None = None,
) -> PreflightResult:
    targets = expand_targets(network, max_hosts, exclusions)
    if len(targets) * len(specs) > MAX_PROBES:
        raise ValueError(
            f"Scan too large: {len(targets)} hosts x {len(specs)} services (max {MAX_PROBES} probes)"
        )
    if any(
        paths_overlap(first, second)
        for index, first in enumerate(destinations)
        for second in destinations[index + 1 :]
    ):
        raise ValueError("Report, snapshot, and history must use different paths")
    if config is not None and any(paths_overlap(path, config) for path in destinations):
        raise ValueError("Destinations must not overwrite the configuration")
    checks: list[Check] = [
        {"check": "targets", "status": "ok", "detail": f"{len(targets)} hosts after exclusions"}
    ]
    if backend == "nmap":
        checks.append(check_nmap())
    checks.extend(check_destination(path) for path in destinations)
    if history is not None:
        checks.extend(check_history(history))
    if tls_ca_file is not None:
        checks.append(check_ca(tls_ca_file))
    return {
        "target": network,
        "host_count": len(targets),
        "services": [asdict(spec) for spec in specs],
        "backend": backend,
        "checks": checks,
    }


def check_nmap() -> Check:
    executable = shutil.which("nmap")
    if executable is None or importlib.util.find_spec("nmap") is None:
        return {
            "check": "nmap",
            "status": "error",
            "detail": "nmap backend requires the executable and python-nmap extra",
        }
    try:
        version = nmap_version(executable)
        return {"check": "nmap", "status": "ok", "detail": version[:200]}
    except (OSError, ValueError) as exc:
        return {"check": "nmap", "status": "error", "detail": str(exc)}


def check_destination(path: Path) -> Check:
    try:
        check_writable_path(path)
        return {"check": str(path), "status": "ok", "detail": "Destination writable"}
    except ValueError as exc:
        return {"check": str(path), "status": "error", "detail": f"cannot write destination: {exc}"}


def check_history(path: Path) -> list[Check]:
    try:
        HistoryStore(path).validate_existing()
        return []
    except (ValueError, sqlite3.Error) as exc:
        return [{"check": "history schema", "status": "error", "detail": str(exc)}]


def check_ca(path: Path) -> Check:
    try:
        ssl.create_default_context(cafile=str(path))
        return {"check": "TLS CA", "status": "ok", "detail": "CA bundle readable"}
    except (OSError, ValueError) as exc:
        return {"check": "TLS CA", "status": "error", "detail": str(exc)}
