# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Tests for 20-locale i18n support in hostcensus."""

from __future__ import annotations

import re

import pytest
from typer.testing import CliRunner

from hostcensus import cli
from hostcensus.i18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    detect_locale,
    get_locale,
    load_catalog,
    normalize_locale,
    set_locale,
    t,
)
from hostcensus.models import Device
from hostcensus.output import print_results

PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z0-9_]+\}")
runner = CliRunner()


@pytest.fixture(autouse=True)
def _reset_locale(monkeypatch: pytest.MonkeyPatch):
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        monkeypatch.delenv(var, raising=False)
    set_locale(None)
    yield
    set_locale(None)


def test_all_20_locales_load_with_key_and_placeholder_parity() -> None:
    assert len(SUPPORTED_LOCALES) == 20
    en = load_catalog(DEFAULT_LOCALE)
    assert len(en) > 0
    for locale in SUPPORTED_LOCALES:
        catalog = load_catalog(locale)
        assert set(catalog.keys()) == set(en.keys()), locale
        for key, en_val in en.items():
            assert catalog[key].strip(), (locale, key)
            assert sorted(PLACEHOLDER_RE.findall(catalog[key])) == sorted(
                PLACEHOLDER_RE.findall(en_val)
            ), (locale, key)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, "en"),
        ("", "en"),
        ("C", "en"),
        ("POSIX", "en"),
        ("de_DE.UTF-8", "de"),
        ("zh_TW", "zh-TW"),
        ("zh_HK.UTF-8", "zh-TW"),
        ("zh-Hant-TW", "zh-TW"),
        ("zh_CN.UTF-8", "zh-CN"),
        ("zh", "zh-CN"),
        ("pt_BR.UTF-8", "pt-BR"),
        ("pt_PT", "pt-BR"),
        ("xx_YY", "en"),
    ],
)
def test_normalize_locale(raw: str | None, expected: str) -> None:
    assert normalize_locale(raw) == expected


def test_env_precedence_and_override(monkeypatch: pytest.MonkeyPatch) -> None:
    assert detect_locale() == "en"
    monkeypatch.setenv("LANG", "es_ES.UTF-8")
    assert detect_locale() == "es"
    monkeypatch.setenv("LC_MESSAGES", "ja_JP.UTF-8")
    assert detect_locale() == "ja"
    monkeypatch.setenv("LC_ALL", "fr_FR.UTF-8")
    assert detect_locale() == "fr"
    assert detect_locale("de") == "de"

    assert set_locale("id") == "id"
    assert get_locale() == "id"
    assert set_locale(None) == "fr"
    assert get_locale() == "fr"


def test_cli_lang_flag_and_localized_output(capsys: pytest.CaptureFixture[str]) -> None:
    assert t("output.no_alive_hosts") == "No alive hosts found"
    assert t("unknown.key") == "unknown.key"

    result = runner.invoke(cli.app, ["--lang", "de", "version"])
    assert result.exit_code == 0
    assert t("cli.version_tagline", locale="de") in result.output

    set_locale("fr")
    print_results([Device(ip="10.0.0.1")])
    assert t("output.no_alive_hosts", locale="fr") in capsys.readouterr().out
