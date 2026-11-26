# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Tests for 48-locale i18n support in hostcensus."""

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

CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z0-9_]+\}")
runner = CliRunner()


@pytest.fixture(autouse=True)
def _reset_locale(monkeypatch: pytest.MonkeyPatch):
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        monkeypatch.delenv(var, raising=False)
    set_locale(None)
    yield
    set_locale(None)


def test_all_48_locales_load_with_key_and_placeholder_parity() -> None:
    assert len(SUPPORTED_LOCALES) == 48
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


def test_bcms_locales_are_distinct_and_use_expected_scripts() -> None:
    bs = load_catalog("bs")
    hr = load_catalog("hr")
    sr = load_catalog("sr")

    # Bosnian and Croatian catalogs must be genuinely distinct
    differing_bs_hr = [k for k in bs if bs[k] != hr[k]]
    assert len(differing_bs_hr) >= 20

    # Serbian catalog must use Serbian Cyrillic across its messages
    cyrillic_values = [k for k, v in sr.items() if CYRILLIC_RE.search(v)]
    assert len(cyrillic_values) == len(sr)

    # Bosnian and Croatian must use Latin script (no Cyrillic)
    assert not any(CYRILLIC_RE.search(v) for v in bs.values())
    assert not any(CYRILLIC_RE.search(v) for v in hr.values())


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
        ("zh-TW-x-test", "zh-TW"),
        ("zh-HK-x-test", "zh-TW"),
        ("zh-Hant-TW", "zh-TW"),
        ("zh-Hans-TW", "zh-CN"),
        ("zh_CN.UTF-8", "zh-CN"),
        ("zh", "zh-CN"),
        ("pt_BR.UTF-8", "pt-BR"),
        ("pt_PT", "pt-BR"),
        ("x-test", "en"),
        ("ar_EG.UTF-8", "ar-EG"),
        ("ar-MA-u-nu-latn", "ar-MA"),
        ("ar-Arab-EG", "ar-EG"),
        ("ar-Arab-SA", "ar"),
        ("fr_MA.UTF-8", "fr-MA"),
        ("fr-SN-x-test", "fr-SN"),
        ("fr_CA.UTF-8", "fr"),
        ("af", "af-ZA"),
        ("am_ET.UTF-8", "am-ET"),
        ("ha", "ha-NG"),
        ("ig", "ig-NG"),
        ("mg", "mg-MG"),
        ("rw", "rw-RW"),
        ("so", "so-SO"),
        ("sw_KE.UTF-8", "sw-KE"),
        ("xh", "xh-ZA"),
        ("yo", "yo-NG"),
        ("zu", "zu-ZA"),
        ("bn_BD.UTF-8", "bn"),
        ("fa_IR", "fa"),
        ("iw", "he"),
        ("mr_IN", "mr"),
        ("ta_IN", "ta"),
        ("te_IN", "te"),
        ("th_TH", "th"),
        ("ur_PK", "ur"),
        ("ms_MY.UTF-8", "ms"),
        ("tl_PH.UTF-8", "fil"),
        ("bs", "bs"),
        ("bs-BA", "bs"),
        ("bs_BA.UTF-8", "bs"),
        ("bs-Latn-BA", "bs"),
        ("hr", "hr"),
        ("hr-HR", "hr"),
        ("hr_HR.UTF-8", "hr"),
        ("sr", "sr"),
        ("sr-RS", "sr"),
        ("sr_RS.UTF-8", "sr"),
        ("sr_RS@latin", "sr"),
        ("sr-Cyrl", "sr"),
        ("sr-Cyrl-RS", "sr"),
        ("sr-Latn", "sr"),
        ("sr-Latn-RS", "sr"),
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
