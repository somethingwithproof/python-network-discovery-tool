# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Named inventory profiles layered over existing service configuration."""

from __future__ import annotations

import ipaddress
import math
import tomllib
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

from netprobe.config import ConfigError
from netprobe.scanner import DEFAULT_CONCURRENCY, DEFAULT_TIMEOUT, MAX_CONCURRENCY, MAX_HOSTS

type IPNetwork = ipaddress.IPv4Network | ipaddress.IPv6Network
type ProfileSettings = dict[str, Any]


@dataclass(slots=True, kw_only=True)
class Profile:
    network: str
    backend: str = "asyncio"
    timeout: float = DEFAULT_TIMEOUT
    concurrency: int = DEFAULT_CONCURRENCY
    max_hosts: int = MAX_HOSTS
    services: str | None = None
    ports: str | None = None
    exclusions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.network, str) or "%" in self.network:
            raise ConfigError("profile network must be an IP or CIDR without a scope identifier")
        try:
            self.network = str(ipaddress.ip_network(self.network, strict=False))
        except ValueError as exc:
            raise ConfigError("profile network must be an IP or CIDR") from exc
        if self.backend not in ("asyncio", "nmap"):
            raise ConfigError("profile backend must be asyncio or nmap")
        if (
            type(self.timeout) not in (int, float)
            or not math.isfinite(self.timeout)
            or self.timeout < 0.05
        ):
            raise ConfigError("profile timeout must be finite and at least 0.05 seconds")
        if type(self.concurrency) is not int or not 1 <= self.concurrency <= MAX_CONCURRENCY:
            raise ConfigError(f"profile concurrency must be from 1 to {MAX_CONCURRENCY}")
        if type(self.max_hosts) is not int or not 1 <= self.max_hosts <= MAX_HOSTS:
            raise ConfigError(f"profile max_hosts must be from 1 to {MAX_HOSTS}")
        for value in (self.services, self.ports):
            if value is not None and not isinstance(value, str):
                raise ConfigError("profile services and ports must be comma-separated strings")
        if not isinstance(self.exclusions, list):
            raise ConfigError("profile exclusions must be a list of IPs or CIDRs")
        self.exclusions = [str(parse_exclusion(value)) for value in self.exclusions]


def parse_exclusion(value: str) -> IPNetwork:
    if not isinstance(value, str) or "%" in value:
        raise ConfigError("exclusions must be IPs or CIDRs without scope identifiers")
    try:
        return ipaddress.ip_network(value, strict=False)
    except ValueError as exc:
        raise ConfigError(f"invalid exclusion: {value!r}") from exc


def load_profiles(path: Path) -> dict[str, Profile]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ConfigError(f"cannot read config {path}: {exc}") from exc
    if set(data) - {"services", "profiles"}:
        raise ConfigError("profile config permits only [services] and [profiles] tables")
    entries = data.get("profiles", {})
    if not isinstance(entries, dict):
        raise ConfigError("[profiles] must be a table")
    result = {}
    for name, settings in entries.items():
        if (
            not isinstance(settings, dict)
            or "network" not in settings
            or set(settings) - {entry.name for entry in fields(Profile)}
        ):
            raise ConfigError(f"profile {name!r} requires network and only supported settings")
        result[name] = Profile(**settings)
    return result


def resolve_profile(
    network: str | None, config: Path | None, name: str | None, overrides: ProfileSettings
) -> ProfileSettings:
    settings = selected_profile(config, name, network) if name is not None else {}
    if network is not None:
        settings["network"] = network
    if "network" not in settings:
        raise ConfigError("provide a target or select --profile")
    for key, value in overrides.items():
        if value is not None:
            settings[key] = settings.get(key, []) + value if key == "exclusions" else value
    return settings


def selected_profile(config: Path | None, name: str, network: str | None) -> ProfileSettings:
    if config is None:
        raise ConfigError("select a profile configuration with --config")
    available = load_profiles(config)
    if name not in available:
        raise ConfigError(f"unknown profile {name!r}; available: {', '.join(available)}")
    settings = asdict(available[name])
    if network is not None:
        validate_profile_target(network, settings["network"])
    return settings


def validate_profile_target(network: str, scope: str) -> None:
    try:
        requested = ipaddress.ip_network(network, strict=False)
        approved = ipaddress.ip_network(scope)
    except ValueError as exc:
        raise ConfigError("profile target override must be an IP or CIDR") from exc
    if requested.version != approved.version or (
        requested.network_address not in approved or requested.broadcast_address not in approved
    ):
        raise ConfigError("target must be contained in the profile network")
