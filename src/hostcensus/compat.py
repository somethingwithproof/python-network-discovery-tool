# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Support for the project's former name, netprobe.

Everything here exists so installs and files from before the rename keep
working. It is removed in the next major release.
"""

from __future__ import annotations

import os
import sys
from collections.abc import MutableMapping
from pathlib import Path

ENV_PREFIX = "HOSTCENSUS_"
LEGACY_ENV_PREFIX = "NETPROBE_"

DEFAULT_PROFILE_CONFIG = Path("hostcensus.toml")
LEGACY_PROFILE_CONFIG = Path("netprobe.toml")
DEFAULT_HISTORY = Path("hostcensus-history.sqlite3")
LEGACY_HISTORY = Path("netprobe-history.sqlite3")

_warned: set[str] = set()


def _warn_once(key: str, message: str) -> None:
    if key not in _warned:
        _warned.add(key)
        print(f"warning: {message}", file=sys.stderr)


def promote_legacy_env(environ: MutableMapping[str, str] | None = None) -> list[str]:
    """Copy NETPROBE_* settings to HOSTCENSUS_* unless HOSTCENSUS_* is already set.

    The only place that knows the old variable names exist, so every lookup
    afterwards, whether by Typer's `envvar=` or by `get_env`, reads HOSTCENSUS_*
    alone. The warning names variables and never their values. Returns the
    legacy names that were found.
    """
    env = os.environ if environ is None else environ
    legacy = sorted(name for name in env if name.startswith(LEGACY_ENV_PREFIX))
    for name in legacy:
        env.setdefault(ENV_PREFIX + name.removeprefix(LEGACY_ENV_PREFIX), env[name])
    if legacy:
        names = ", ".join(legacy)
        _warn_once(
            "env:" + names,
            f"{names} is deprecated; use the {ENV_PREFIX}* name instead "
            f"(HOSTCENSUS_* wins when both are set; {LEGACY_ENV_PREFIX}* support "
            "is removed in the next major release)",
        )
    return legacy


def get_env(suffix: str, environ: MutableMapping[str, str] | None = None) -> str | None:
    """Read HOSTCENSUS_<suffix>, falling back to the deprecated NETPROBE_<suffix>."""
    env = os.environ if environ is None else environ
    promote_legacy_env(env)
    return env.get(ENV_PREFIX + suffix)


def default_path(path: Path, current: Path, legacy: Path) -> Path:
    """Resolve a default file name, keeping a file that still has its old name.

    Only the unchanged default is rewritten; an explicit path is returned as given.
    """
    if path == current and not current.exists() and legacy.exists():
        _warn_once(
            f"path:{legacy}",
            f"using {legacy}; rename it to {current} (the {legacy} default is "
            "removed in the next major release)",
        )
        return legacy
    return path


def legacy_main() -> None:
    """Entry point of the deprecated `netprobe` command."""
    from hostcensus.cli import app

    print(
        "warning: the `netprobe` command is deprecated; use `hostcensus` "
        "(`netprobe` is removed in the next major release)",
        file=sys.stderr,
    )
    app()
