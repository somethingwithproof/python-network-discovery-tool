# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Kadupul import script: one `php cli/add_device.php` call per discovered host.

Kadupul (a fork of Cacti 1.2.31) has no bulk device file import; its
supported path is cli/add_device.php, which takes one device per run as
`--option=value` arguments. This module writes a POSIX sh script of those
calls. Every value is validated and passed through shlex.quote.
"""

from __future__ import annotations

import os
import re
import shlex
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Any

from netprobe.probes import AUTH_PROTOCOLS, PRIV_PROTOCOLS, clean
from netprobe.scanner import validate_target

# add_device.php checks the SNMP port is from 2 to 65534.
KADUPUL_PORT_RANGE = range(2, 65535)
# Descriptions double as Kadupul's duplicate key, so keep them predictable.
_DESCRIPTION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
_PLAIN = re.compile(r"^[A-Za-z0-9._@-]{1,64}$")

ENV_COMMUNITY = "NETPROBE_SNMP_COMMUNITY"
ENV_AUTH_KEY = "NETPROBE_SNMP_AUTH_KEY"
ENV_PRIV_KEY = "NETPROBE_SNMP_PRIV_KEY"


class ExportError(ValueError):
    """The scan data or export options cannot produce a safe script."""


@dataclass(frozen=True)
class KadupulOptions:
    template: int = 0
    snmp_user: str | None = None
    auth_protocol: str = "SHA"
    priv_protocol: str = "AES"
    # Literal secrets, used only with include_credentials.
    community: str | None = None
    auth_key: str | None = None
    priv_key: str | None = None
    include_credentials: bool = False

    def __post_init__(self) -> None:
        if self.template < 0:
            raise ExportError("--template must be a Kadupul host template id (0 or more)")
        if self.snmp_user is not None and not _PLAIN.match(self.snmp_user):
            raise ExportError("SNMPv3 user names may use letters, digits and . _ @ - only")
        if self.auth_protocol not in AUTH_PROTOCOLS or self.priv_protocol not in PRIV_PROTOCOLS:
            raise ExportError("unknown SNMPv3 protocol")


def _secret(flag: str, env: str, value: str | None, opts: KadupulOptions) -> str:
    """A --flag=secret argument: the literal only on request, else an env reference."""
    if opts.include_credentials:
        if not value:
            raise ExportError(f"--include-credentials needs a value for {flag} (env {env})")
        return shlex.quote(f"{flag}={value}")
    # Expanded by the shell when the script runs; the value never touches this file.
    return f'"{flag}=${{{env}}}"'


def _description(device: dict[str, Any], seen: set[str]) -> str:
    hostname = str(device.get("hostname") or "")
    name = hostname if _DESCRIPTION.match(hostname) else str(device["ip"])
    # add_device.php treats an existing description as "update that device",
    # so two hosts must never share one.
    if name in seen:
        name = f"{name}-{device['ip']}"
    seen.add(name)
    return name


def _open(device: dict[str, Any]) -> list[dict[str, Any]]:
    services = device.get("services") or []
    return [s for s in services if isinstance(s, dict) and s.get("state") == "open"]


def device_arguments(
    device: dict[str, Any], opts: KadupulOptions, seen: set[str]
) -> tuple[list[str], set[str]]:
    """Return the add_device.php arguments for one device and the env vars they need."""
    try:
        ip = validate_target(str(device["ip"]))
    except ValueError as e:
        raise ExportError(str(e)) from e
    args = [
        shlex.quote(f"--description={_description(device, seen)}"),
        shlex.quote(f"--ip={ip}"),
        f"--template={opts.template}",
    ]
    needs: set[str] = set()
    services = _open(device)

    snmp = next(
        (s for s in services if (s.get("details") or {}).get("snmp_version") in ("2c", "3")),
        None,
    )
    if snmp is not None:
        snmp_args, needs = snmp_arguments(ip, snmp, opts)
        args += snmp_args
    else:
        args += ping_arguments(services)

    notes = "; ".join(
        f"{clean(str(s.get('name', '')), 32)}:{int(s['port'])}/{clean(str(s.get('protocol', '')), 3)}"
        + (f" {clean(str(s['version']), 80)}" if s.get("version") else "")
        for s in services
    )
    if notes:
        args.append(shlex.quote(f"--notes=netprobe: {notes}"))
    if opts.include_credentials:
        needs = set()
    return args, needs


def kadupul_script(devices: Iterable[dict[str, Any]], opts: KadupulOptions, source: str) -> str:
    """Render the sh script for every alive device."""
    seen: set[str] = set()
    needs: set[str] = set()
    calls: list[str] = []
    for device in devices:
        if not device.get("alive", True):
            continue
        args, env = device_arguments(device, opts, seen)
        needs |= env
        calls.append("add " + " ".join(args))

    header = [
        "#!/bin/sh",
        f"# Generated by netprobe {package_version('netprobe')} from {clean(source, 120)}",
        f"# at {datetime.now(UTC).isoformat(timespec='seconds')}.",
        "#",
        "# Run on the Kadupul server as the user that owns the install:",
        "#   KADUPUL_ROOT=/path/to/kadupul sh this-script.sh",
        "# Each line runs Kadupul's cli/add_device.php once. A device whose",
        "# description or IP already exists is reported and skipped by add_device.php.",
    ]
    if opts.include_credentials:
        header += [
            "#",
            "# WARNING: this file contains SNMP credentials. Keep it private and delete",
            "# it after use.",
        ]
    elif needs:
        header += [
            "#",
            "# SNMP secrets are not stored here; export these first:",
            *(f"#   {name}" for name in sorted(needs)),
            "# add_device.php echoes the community in its output, and arguments are",
            "# visible in the process list while each call runs.",
        ]
    body = [
        "set -u",
        'KADUPUL_ROOT="${KADUPUL_ROOT:-/var/www/html/kadupul}"',
        *(f': "${{{name}:?set {name} before running}}"' for name in sorted(needs)),
        "failed=0",
        'add() { php "$KADUPUL_ROOT/cli/add_device.php" "$@" || failed=$((failed + 1)); }',
        "",
        *calls,
        "",
        'if [ "$failed" -gt 0 ]; then echo "$failed device(s) not added" >&2; exit 1; fi',
    ]
    return "\n".join([*header, "", *body]) + "\n"


def write_script(path: Path, text: str, *, secret: bool) -> None:
    """Write the script; one holding credentials is created owner-only from the start."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(path, flags, 0o600 if secret else 0o644)
    if secret:
        # O_CREAT's mode does not apply to an existing file.
        os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(text)


def snmp_arguments(
    ip: str, snmp: dict[str, Any], opts: KadupulOptions
) -> tuple[list[str], set[str]]:
    args: list[str] = []
    needs: set[str] = set()
    port = int(snmp["port"])
    if port not in KADUPUL_PORT_RANGE:
        raise ExportError(f"{ip}: SNMP port {port} is outside Kadupul's 2-65534")
    details = snmp["details"]
    if details["snmp_version"] == "2c":
        args += ["--version=2", _secret("--community", ENV_COMMUNITY, opts.community, opts)]
        needs.add(ENV_COMMUNITY)
    else:
        if not opts.snmp_user:
            raise ExportError(f"{ip} answered SNMPv3; pass --snmp-user to export it")
        level = details.get("snmp_security_level", "")
        if level not in ("authNoPriv", "authPriv"):
            # add_device.php requires a v3 password, so noAuthNoPriv cannot be expressed.
            raise ExportError(f"{ip}: Kadupul needs SNMPv3 auth; scan used {level or 'none'}")
        args += [
            "--version=3",
            shlex.quote(f"--username={opts.snmp_user}"),
            f"--authproto={opts.auth_protocol}",
            _secret("--password", ENV_AUTH_KEY, opts.auth_key, opts),
        ]
        needs.add(ENV_AUTH_KEY)
        if level == "authPriv":
            args += [
                f"--privproto={opts.priv_protocol}",
                _secret("--privpass", ENV_PRIV_KEY, opts.priv_key, opts),
            ]
            needs.add(ENV_PRIV_KEY)
        else:
            # Quoted: unquoted [None] is a shell glob.
            args.append(shlex.quote("--privproto=[None]"))
    args += [f"--port={port}", "--avail=snmp"]
    return args, needs


def ping_arguments(services: list[dict[str, Any]]) -> list[str]:
    tcp = [service for service in services if service.get("protocol") == "tcp"]
    args = ["--version=0", "--avail=ping"]
    if tcp:
        args += ["--ping_method=tcp", f"--ping_port={int(tcp[0]['port'])}"]
    else:
        args.append("--ping_method=icmp")
    return args
