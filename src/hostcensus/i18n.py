# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Zero-dependency localization support for hostcensus."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from importlib import resources

DEFAULT_LOCALE = "en"

SUPPORTED_LOCALES: tuple[str, ...] = (
    "en",
    "de",
    "es",
    "fr",
    "it",
    "pt-BR",
    "nl",
    "ru",
    "uk",
    "ja",
    "ko",
    "zh-CN",
    "zh-TW",
    "ar",
    "hi",
    "pl",
    "tr",
    "sv",
    "vi",
    "id",
    "af-ZA",
    "am-ET",
    "ar-EG",
    "ar-MA",
    "fr-MA",
    "fr-SN",
    "ha-NG",
    "ig-NG",
    "mg-MG",
    "rw-RW",
    "so-SO",
    "sw-KE",
    "xh-ZA",
    "yo-NG",
    "zu-ZA",
    "bn",
    "fa",
    "he",
    "mr",
    "ta",
    "te",
    "th",
    "ur",
    "ms",
    "fil",
)

_LOCALE_BY_LOWER: dict[str, str] = {loc.lower(): loc for loc in SUPPORTED_LOCALES}
_PRIMARY_ALIASES: dict[str, str] = {
    "af": "af-ZA",
    "am": "am-ET",
    "ha": "ha-NG",
    "ig": "ig-NG",
    "iw": "he",
    "mg": "mg-MG",
    "pt": "pt-BR",
    "rw": "rw-RW",
    "so": "so-SO",
    "sw": "sw-KE",
    "tl": "fil",
    "xh": "xh-ZA",
    "yo": "yo-NG",
    "zu": "zu-ZA",
}
_ZH_TRADITIONAL_REGIONS = frozenset({"tw", "hk", "mo"})
_active_locale: str | None = None


def normalize_locale(raw: str | None) -> str:
    """Resolve a POSIX or BCP 47 locale tag to a supported locale code."""
    if not raw:
        return DEFAULT_LOCALE
    cleaned = raw.strip().split(".", 1)[0].split("@", 1)[0]
    if not cleaned or cleaned.upper() in {"C", "POSIX"}:
        return DEFAULT_LOCALE
    base_parts: list[str] = []
    for part in cleaned.replace("_", "-").lower().split("-"):
        if len(part) == 1:
            break
        base_parts.append(part)
    if not base_parts:
        return DEFAULT_LOCALE
    tag = "-".join(base_parts)
    if tag in _LOCALE_BY_LOWER:
        return _LOCALE_BY_LOWER[tag]
    primary = base_parts[0]
    if primary == "zh":
        subtags = set(base_parts[1:])
        if "hans" in subtags:
            return "zh-CN"
        if "hant" in subtags or subtags & _ZH_TRADITIONAL_REGIONS:
            return "zh-TW"
        return "zh-CN"
    if len(base_parts) >= 3:
        lang_region = f"{primary}-{base_parts[2]}"
        if lang_region in _LOCALE_BY_LOWER:
            return _LOCALE_BY_LOWER[lang_region]
    if primary in _PRIMARY_ALIASES:
        return _PRIMARY_ALIASES[primary]
    return _LOCALE_BY_LOWER.get(primary, DEFAULT_LOCALE)


def detect_locale(explicit: str | None = None) -> str:
    """Detect locale using explicit > LC_ALL > LC_MESSAGES > LANG > en."""
    if explicit:
        return normalize_locale(explicit)
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var)
        if value:
            return normalize_locale(value)
    return DEFAULT_LOCALE


def set_locale(locale: str | None) -> str:
    """Set or clear the process-wide locale override."""
    global _active_locale
    if locale is None:
        _active_locale = None
        return detect_locale()
    _active_locale = normalize_locale(locale)
    return _active_locale


def get_locale() -> str:
    """Return the active locale code."""
    if _active_locale is not None:
        return _active_locale
    return detect_locale()


@lru_cache(maxsize=len(SUPPORTED_LOCALES))
def load_catalog(locale: str) -> dict[str, str]:
    """Load the message catalog for a normalized locale."""
    resolved = normalize_locale(locale)
    path = resources.files("hostcensus").joinpath("locales", f"{resolved}.json")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in loaded.items()}


def t(key: str, *, locale: str | None = None, **kwargs: object) -> str:
    """Translate a message key with optional format arguments."""
    target = normalize_locale(locale) if locale is not None else get_locale()
    template = load_catalog(target).get(key)
    if template is None:
        template = load_catalog(DEFAULT_LOCALE).get(key, key)
    return template.format(**kwargs) if kwargs else template
