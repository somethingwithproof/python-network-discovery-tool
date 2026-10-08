"""Service definitions: built-in defaults, TOML config and CLI selection."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from netprobe.models import ServiceSpec
from netprobe.probes import PROBES


class ConfigError(ValueError):
    """A service definition or selection is invalid."""


def _spec(name: str, port: int, probe: str) -> ServiceSpec:
    return ServiceSpec(name, port, PROBES[probe][1], probe)


DEFAULT_SERVICES: tuple[ServiceSpec, ...] = (
    _spec("ssh", 22, "ssh"),
    _spec("snmp", 161, "snmp"),
    _spec("mysql", 3306, "mysql"),
    _spec("http", 80, "http"),
    _spec("https", 443, "https"),
)

# Names end up in CSV cells and in exported shell scripts, so keep them plain.
_NAME = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")


def _check_port(port: object, where: str) -> int:
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ConfigError(f"{where}: port must be an integer from 1 to 65535, got {port!r}")
    return port


def _check_name(name: str, where: str) -> str:
    if not _NAME.match(name):
        raise ConfigError(f"{where}: invalid service name {name!r}")
    return name


def load_services(path: Path) -> tuple[ServiceSpec, ...]:
    """Merge the [services] table from a TOML file over the defaults.

    Example:
        [services.ssh-alt]
        port = 2222
        probe = "ssh"

    A service named like a built-in replaces it; `probe` defaults to the
    service name when that is a known probe, else "tcp".
    """
    try:
        document = tomllib.loads(path.read_text())
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as e:
        raise ConfigError(f"cannot read config {path}: {e}") from e

    table = document.get("services", {})
    if not isinstance(table, dict):
        raise ConfigError(f"{path}: [services] must be a table")

    services = {s.name: s for s in DEFAULT_SERVICES}
    for name, entry in table.items():
        where = f"{path}: services.{name}"
        _check_name(name, where)
        if not isinstance(entry, dict):
            raise ConfigError(f"{where} must be a table")
        unknown = set(entry) - {"port", "probe"}
        if unknown:
            raise ConfigError(f"{where}: unknown keys {sorted(unknown)}")
        probe = entry.get("probe", name if name in PROBES else "tcp")
        if probe not in PROBES:
            raise ConfigError(f"{where}: unknown probe {probe!r} (known: {', '.join(PROBES)})")
        services[name] = _spec(name, _check_port(entry.get("port"), where), probe)
    return tuple(services.values())


def select_services(
    services: tuple[ServiceSpec, ...], names: str | None, ports: str | None
) -> tuple[ServiceSpec, ...]:
    """Apply --services (keep these names) and --ports (override or add ports).

    --ports takes a comma list of NAME=PORT, which moves a service, or a bare
    PORT, which adds a plain TCP connect check named tcp-PORT.
    """
    by_name = {s.name: s for s in services}
    if names:
        wanted = [n.strip() for n in names.split(",") if n.strip()]
        missing = [n for n in wanted if n not in by_name]
        if missing:
            raise ConfigError(
                f"unknown service(s) {', '.join(missing)} (known: {', '.join(by_name)})"
            )
        by_name = {n: by_name[n] for n in wanted}

    for item in (ports or "").split(","):
        item = item.strip()
        if not item:
            continue
        name, sep, value = item.rpartition("=")
        if not value.isdigit():
            raise ConfigError(f"--ports: expected PORT or NAME=PORT, got {item!r}")
        port = _check_port(int(value), "--ports")
        if sep:
            if name not in by_name:
                raise ConfigError(f"--ports: unknown service {name!r}")
            spec = by_name[name]
            by_name[name] = ServiceSpec(spec.name, port, spec.protocol, spec.probe)
        else:
            by_name[f"tcp-{port}"] = _spec(f"tcp-{port}", port, "tcp")

    if not by_name:
        raise ConfigError("no services selected")
    return tuple(by_name.values())
