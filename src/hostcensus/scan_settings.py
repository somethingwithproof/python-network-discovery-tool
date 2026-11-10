# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Settings and ordering shared by snapshots, history and their comparisons."""

from __future__ import annotations

import ipaddress
import math
from dataclasses import dataclass, field
from enum import StrEnum
from importlib.metadata import version as _package_version
from typing import Any

# The one place the installed version is read; reports, snapshots, history
# and generated scripts all record it.
HOSTCENSUS_VERSION = _package_version("hostcensus")


def host_sort_key(value: str) -> tuple[int, int, str]:
    """IPv4 numerically, then IPv6, then hostnames alphabetically."""
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return 99, 0, value
    return address.version, int(address), ""


# A probe failed or timed out, so the port's state was not observed.
UNKNOWN = "unknown"


class PortTransition(StrEnum):
    """How one port's observation changed between two scans."""

    UNCHANGED = "unchanged"
    OPENED = "opened"
    CLOSED = "closed"
    # Between two observed states that are both not open, e.g. closed -> filtered.
    CHANGED = "changed"
    # A failed observation on either side that does not leave the port open.
    UNCONFIRMED = "unconfirmed"


def port_transition(before: str, after: str) -> PortTransition:
    """Classify a port's state in two scans; `diff` and `compare` both use this.

    A port open now is news even when the earlier probe failed. Any other
    transition with a failed observation is unconfirmed, never unchanged:
    a failed probe proves nothing, so it cannot show that nothing changed.
    """
    if after == "open" and before != "open":
        return PortTransition.OPENED
    if UNKNOWN in (before, after):
        return PortTransition.UNCONFIRMED
    if before == after:
        return PortTransition.UNCHANGED
    return PortTransition.CLOSED if before == "open" else PortTransition.CHANGED


@dataclass(frozen=True, slots=True)
class RecordedSettings:
    """What a stored scan says about how it ran; None or empty when not recorded."""

    target: str = ""
    timeout: float | None = None
    backend: str | None = None
    service_timeouts: dict[str, float] = field(default_factory=dict)


def setting_warnings(old: RecordedSettings, new: RecordedSettings) -> list[str]:
    """Warn when both scans recorded a setting and the values differ.

    Missing values are older files. A difference changes what a result can
    mean, so the comparison still runs and says so.
    """
    warnings = [
        f"{label} differ: {before} vs {after}"
        for label, before, after in (
            ("targets", old.target or None, new.target or None),
            ("timeouts", old.timeout, new.timeout),
            ("backends", old.backend, new.backend),
        )
        if before is not None and after is not None and before != after
    ]
    warnings.extend(timeout_warnings(old.service_timeouts, new.service_timeouts))
    return warnings


def effective_timeouts(metadata: dict[str, Any]) -> dict[str, float]:
    """Use the scan timeout for older services without an explicit budget."""
    budgets: dict[str, float] = {}
    services = metadata.get("services", [])
    if not isinstance(services, list):
        return budgets
    for service in services:
        if not isinstance(service, dict):
            continue
        port, protocol = service.get("port"), service.get("protocol")
        budget = service.get("timeout")
        if budget is None:
            budget = metadata.get("timeout")
        if (
            type(port) is int
            and 1 <= port <= 65535
            and protocol in ("tcp", "udp")
            and isinstance(budget, (int, float))
            and not isinstance(budget, bool)
            and math.isfinite(budget)
            and budget > 0
        ):
            budgets[f"{port}/{protocol}"] = float(budget)
    return budgets


def timeout_warnings(before: dict[str, float], after: dict[str, float]) -> list[str]:
    """Warn only for services with a known budget in both scans."""
    return [
        f"timeouts differ for {port}: {before[port]} vs {after[port]}"
        for port in sorted(before.keys() & after.keys())
        if before[port] != after[port]
    ]
