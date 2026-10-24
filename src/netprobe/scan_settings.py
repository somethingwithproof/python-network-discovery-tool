# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Compare recorded probe budgets in snapshots and history."""

from __future__ import annotations

import math
from typing import Any


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
