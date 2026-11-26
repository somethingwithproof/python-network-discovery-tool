<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# hostcensus

[![CI](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/ci.yml)
[![Docker](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/docker-build.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/docker-build.yml)
[![Release workflow](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/release.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/release.yml)
[![Latest published release](https://img.shields.io/github/v/release/somethingwithproof/python-network-discovery-tool?label=published%20release)](https://github.com/somethingwithproof/python-network-discovery-tool/releases)
[![Bandit](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/bandit.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/bandit.yml)
[![Python compatibility](https://img.shields.io/badge/Python-3.12%E2%80%933.14-blue)](./.github/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/python-network-discovery-tool/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/15324/badge)](https://www.bestpractices.dev/en/projects/15324)
[![Strict typing](https://img.shields.io/badge/mypy-strict-blue)](./pyproject.toml)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · **Yorùbá** · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus jẹ́ ohun-èlò CLI ti Python fún ṣíṣe àkọsílẹ̀ àwọn iṣẹ́ tí a lè tún ṣe nígbà gbogbo lórí àwọn nẹ́tíwọ́ọ̀kì tí o ń ṣàkóso.
Ó ń ṣàkọsílẹ̀ ohun tí àwọn ẹ̀rọ ń fi hàn, ó ń fi àwọn àkíyèsí wé ara wọn ní àsìkò sí àsìkò, ó sì ń ṣẹ̀dá
àwọn ìwé-àṣẹ ìkówọlé Kadupul. Ètò-ìpìlẹ̀ àkọ́bẹ̀rẹ̀ ń lo àwọn sọ́kẹ́ẹ̀tì asyncio láìlo root;
ìwádìí Nmap tí ó jẹ́ àṣàyàn lè dá àwọn ẹ̀rọ agbàlejò mọ̀ rékọjá àwọn pọ́ọ̀tì iṣẹ́ tí a ṣètò.

## Kí nìdí hostcensus

Ìjábọ̀ pọ́ọ̀tì ẹ̀ẹ̀kan ṣoṣo kì í ṣàlàyé bóyá àkíyèsí tí ó tẹ̀lé e yí padà tàbí
kò kàn ṣàṣeyọrí. hostcensus ń so àwọn ipò iṣẹ́ tí ó ṣe kedere, àwọn ìwádìí tí ó ní ààlà, àwọn profáìlì
àyẹ̀wò tí a lè tún lò, àti ìtàn abẹ́lé pọ̀. Àwọn olùṣàkóso lè tún ààyè kan náà yẹ̀ wò, wọ́n lè ṣàyẹ̀wò
àwọn àṣìṣe, wọ́n sì lè ya àwọn àkíyèsí tí kò dájú sọ́tọ̀ kúrò lára àwọn ìyípadà tí a fìdí múlẹ̀.

- **Ẹ̀rí iṣẹ́:** ìdánimọ̀ SSH, ìkíni MySQL, àwọn àkọlé HTTP, àwọn àkíyèsí ìwé-ẹ̀rí
  TLS, àti ìwádìí SNMP tàbí àwọn ìbéèrè system-MIB tí ó ní ẹ̀rí-ìdánimọ̀.
- **Ààyè tí a lè tún ṣe:** àwọn profáìlì TOML tí a fún ní orúkọ, àwọn ìyọkúrò àfikún, àwọn iṣẹ́
  tí a lè ṣètò, ààlà ẹ̀rọ agbàlejò/ìwádìí, àti àwọn òṣìṣẹ́ tí ó ní ààlà.
- **Àyẹ̀wò ṣáájú ìrìn-àjò dátà:** àyẹ̀wò ìṣáájú abẹ́lé ń fìdí àwọn ibi-àfojúsùn, àwọn ohun-èlò, àǹfààní sí ibi-ìfipamọ́,
  àwòrán ìtàn, àti àwọn àkójọpọ̀ TLS CA tí a ṣètò múlẹ̀.
- **Ìtàn àkọsílẹ̀ iṣẹ́:** àwọn àwòrán SQLite oní-ìṣòwò ń tọ́jú gbogbo àwọn àkíyèsí;
  àwọn ìfiwéra ń jẹ́ kí àwọn ìkùnà ẹ̀rọ-àyẹ̀wò àti àwọn ipò àìmọ̀ máa hàn gbangba.
- **Èsì tí ó bá àwọn ètò mìíràn mu:** ìjábọ̀ lórí terminal, JSON àti CSV, àwọn àwòrán fáìlì tí ó ní ẹ̀dà,
  àti àwọn ìwé-àṣẹ ìkówọlé Kadupul.

CI bo Python 3.12, 3.13 àti 3.14 lórí Linux àti macOS, pẹ̀lú yàrá ìdánwò ìṣọ̀kan Compose
tí a ń ṣàkóso. Kóòdù náà ń lo àwọn orúkọ-ìrú òde-òní, àwọn èsì àyẹ̀wò ìṣáájú tí ó ní irú,
àwọn profáìlì slotted tí ó ń gba ọ̀rọ̀-kọ́kọ́rọ́ nìkan àti ìmọ́tótó async tí ó ní ètò nígbà tí ó ṣì ń pa àwọn
ẹ̀dà àṣẹ-ìṣiṣẹ́ wọ̀nyẹn mọ́. Wo [Ìṣàkóso ẹ̀dà àti àwọn ìtújáde](../../../docs/releasing.md) fún àdéhùn ìbámu SemVer
àti ìlànà ìtújáde GitHub. Àmì ìtújáde ń ṣàpèjúwe
àwọn ohun-ìtújáde tí a tẹ̀ jáde, kì í ṣe ẹ̀dà ibi-iṣẹ́ yìí: àmì ìtújáde tí ó ṣẹ̀ṣẹ̀ jáde lọ́wọ́lọ́wọ́ jẹ́
`v0.3.0`, nígbà tí ẹ̀dà ibi-iṣẹ́ yìí ń lo ẹ̀dà páákì `3.0.0`. Fi sórí ẹ̀rọ láti inú ẹ̀dà ibi-iṣẹ́ yìí
láti lo àwọn ẹ̀yà àkọsílẹ̀ iṣẹ́ tí a ṣàlàyé níbí.

Bẹ̀rẹ̀ pẹ̀lú [ìfisórí ẹ̀rọ](#install), lẹ́yìn náà [àwọn profáìlì àti ìtàn](#inventory-profiles-preflight-and-local-history).
Fún àlàyé ìṣọ̀kan, wo [àwọn ìtẹ̀ka iṣẹ́](#fingerprints),
[ìfiwéra fáìlì](#inventory-diff), àti [ìkójáde Kadupul](#kadupul-export).

## Ìfisórí ẹ̀rọ

A nílò Python 3.12 tàbí ẹ̀dà tuntun; Python 3.12 sí 3.14 ni àwọn ẹ̀dà tí a dán wò. Láti inú
ẹ̀dà ibi-iṣẹ́ yìí, fi àwọn ìgbẹ́kẹ̀lé àṣẹ-ìṣiṣẹ́ tí a tì pa sórí ẹ̀rọ:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Fún ìwádìí ẹ̀rọ agbàlejò Nmap tí ó jẹ́ àṣàyàn, fi ètò Nmap sórí ẹ̀rọ nípa lílo olùṣàkóso
páákì ti ètò rẹ; kò sí páákì Python àfikún tí a nílò. A ń tú èsì XML ti Nmap pẹ̀lú
defusedxml, ìgbẹ́kẹ̀lé pàtàkì kan, nítorí náà a kọ ìfẹ̀sí ohun-àkọsílẹ̀ (entity expansion). hostcensus ń ṣiṣẹ́
`nmap` tí a rí lórí `PATH` tààrà pẹ̀lú àtòjọ àwọn àríyànjiyàn tí ó dúró ṣinṣin, àkókò-ìparí tí ó ń pọ̀ sí i
pẹ̀lú ìwọ̀n ìṣáájú-àdírẹ́ẹ̀sì, àti ààlà èsì 64 MiB. A kò nílò Nmap fún ètò-ìpìlẹ̀ àkọ́bẹ̀rẹ̀.

## Ìyípadà láti netprobe

hostcensus ni orúkọ tuntun fún netprobe, tí a tú jáde ní 3.0.0. A kò tíì tẹ iṣẹ́ àkànṣe yìí
jáde sórí PyPI lábẹ́ orúkọ kankan nínú méjèèjì, nítorí náà àwọn ìfisórí ẹ̀rọ wá láti inú ẹ̀dà ibi-iṣẹ́ tàbí ìtújáde
GitHub. Ibi-ìpamọ́ GitHub pa orúkọ rẹ̀ mọ́.

| Tẹ́lẹ̀ | Báyìí | Ìbámu |
| --- | --- | --- |
| Ìpínkiri `netprobe` | `hostcensus` | Tún fi sórí ẹ̀rọ láti inú ẹ̀dà ibi-iṣẹ́; kò sí páákì orúkọ àtijọ́. |
| Àṣẹ `netprobe` | `hostcensus` | `netprobe` ṣì ń ṣiṣẹ́ ó sì ń tẹ ìlà ìkìlọ̀ ìfọwọ́rọ́sẹ́yìn kan jáde lórí stderr. Àwọn kóòdù ìjáde àti stdout kò yí padà. A ó yọ ọ́ kúrò ní ìtújáde ńlá tí ó tẹ̀lé e. |
| Àwọn oníyípadà àyíká `NETPROBE_*` | `HOSTCENSUS_*` | A ń lo oníyípadà `NETPROBE_*` nígbà tí ẹgbẹ́ rẹ̀ `HOSTCENSUS_*` kò bá ní iye, pẹ̀lú ìkìlọ̀ stderr kan tí ó dárúkọ àwọn oníyípadà náà ṣùgbọ́n kì í fi iye wọn hàn láéláé. `HOSTCENSUS_*` ló borí nígbà tí a bá ṣètò méjèèjì. A ó yọ ọ́ kúrò ní ìtújáde ńlá tí ó tẹ̀lé e. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Ìyípadà tí ń fọ́ ìbámu.** Kò sí ẹ̀rọ ìfọwọ́bọ̀ ìkówọlé tí a fi sí i; ṣe àtúnṣe àwọn ìkówọlé. |
| Àmì àwòrán Docker `network-discovery:test` (CI nìkan) àti olùlò kọ̀ǹténà `netprobe` | `hostcensus:test`, olùlò `hostcensus` | A kò tẹ àwòrán ibi-ìfipamọ́ kankan jáde rí. Tún àwòrán náà kọ kí o sì lo ibi-ìwọlé `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | A ṣì ń lo fáìlì tí ó wà tẹ́lẹ̀ pẹ̀lú orúkọ àkọ́bẹ̀rẹ̀ àtijọ́, pẹ̀lú ìkìlọ̀, níwọ̀n ìgbà tí orúkọ tuntun kò bá tíì sí. Àwọn ọ̀nà `--config` àti `--history` tí a sọ ní pàtó kò yí padà. |
| Àwọn ìjábọ̀ àti àwòrán pẹ̀lú `"format": "netprobe-report"` tàbí `"netprobe-snapshot"`, àti ààyè `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` àti `export` ṣì ń ṣí àwọn fáìlì tí a kọ lábẹ́ orúkọ àtijọ́, àti pé àwọn JSON Schema tí a tẹ̀ jáde ń gba ìkọ̀wé méjèèjì. Àwọn fáìlì tuntun ń lo àwọn orúkọ tuntun. Àwọn dátábéèsì ìtàn SQLite kò yí padà wọ́n sì ń ṣí bíi tẹ́lẹ̀. |
| Àwọn ìwé-àṣẹ Kadupul láti `netprobe export` | Àwọn ìwé-àṣẹ láti `hostcensus export` | Àwọn ìwé-àṣẹ àtijọ́ ń bá a lọ láti ṣiṣẹ́ wọ́n sì ṣì ń ka `NETPROBE_SNMP_*` nígbà tí wọ́n bá ṣiṣẹ́. Àwọn ìwé-àṣẹ tuntun ń ka `HOSTCENSUS_SNMP_*`. |

## Àpẹẹrẹ kíákíá

A ṣiṣẹ́ rẹ̀ láti inú kọ̀ǹténà olùdánwò ti yàrá ìdánwò ìṣọ̀kan tí a ṣàlàyé lábẹ́ Ìdàgbàsókè; a gé èsì rẹ̀ kúrú:

```console
$ hostcensus scan 172.30.57.8/29 --services ssh,http,snmp --save-snapshot after.json
┃ IP Address   ┃ Hostname       ┃ SSH ┃ SNMP ┃ MySQL ┃ Open services  ┃ Status ┃
│ 172.30.57.10 │ hostcensus-it-s… │ ✅  │  ❌  │  ❌   │ ssh:22         │ UP     │
│              │                │     │      │       │ OpenSSH_10.0   │        │
│ 172.30.57.13 │ hostcensus-it-w… │ ❌  │  ❌  │  ❌   │ http:80        │ UP     │
│              │                │     │      │       │ nginx/1.28.3   │        │

$ hostcensus diff before.json after.json; echo "exit=$?"
Warning: targets differ: 172.30.57.10 vs 172.30.57.8/29
│ new host │ 172.30.57.13 │ http:80/tcp  │ hostcensus-it-web-1.hostcensus-it_lab   │
exit=3

$ hostcensus export after.json -o kadupul-import.sh --template 1
$ grep 57.13 kadupul-import.sh
add --description=hostcensus-it-web-1.hostcensus-it_lab --ip=172.30.57.13 --template=1 --version=0 --avail=ping --ping_method=tcp --ping_port=80 '--notes=hostcensus: http:80/tcp nginx/1.28.3'
```

## Àwọn kóòdù ìjáde

| Àṣẹ | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | àwọn àkíyèsí/ìjábọ̀ ti wà ní àkọsílẹ̀ | àyẹ̀wò ìṣáájú/ètò-ìpìlẹ̀, ìtàn, tàbí kíkọ ìjábọ̀/àwòrán kùnà | ibi-àfojúsùn, àwọn àṣàyàn, ètò, tàbí àwọn ààlà tí kò tọ́ | - | `--deadline` ti pé; a kọ ìjábọ̀ apá kan, a fò ìtàn àti àwòrán |
| `preflight` | àwọn àyẹ̀wò yege | àyẹ̀wò abẹ́lé kùnà | ibi-àfojúsùn/ètò tí kò tọ́ tàbí àwọn ibi-ìfipamọ́ tí ó ta ko ara wọn | - | - |
| `profiles` | a tò àwọn profáìlì tí a fìdí rẹ̀ múlẹ̀ | - | ètò tàbí àṣàyàn tí kò ṣeé kà/tí kò tọ́ | - | - |
| `history` | a tò àwọn àkópọ̀ | ìtàn tí ó sọnù, tí kò tọ́, tàbí tí a kò ṣe àtìlẹ́yìn fún | àwọn àṣàyàn CLI tí kò tọ́ | - | - |
| `compare` | a ṣe ìfiwéra, títí kan nígbà tí ìyípadà bá wà | ìtàn tí kò ṣeé kà, ààyè/ìtòlẹ́sẹẹsẹ tí kò bá ara mu, tàbí ìkùnà kíkọ | àwọn àṣàyàn CLI tí kò tọ́ | - | - |
| `diff` | kò sí ìyípadà | a kò lè kọ fáìlì `-o` | ìtẹ̀wọlé tí ó sọnù, tí kò ṣeé kà tàbí tí a kò ṣe àtìlẹ́yìn fún, tàbí àyẹ̀wò tí kò pé láìsí `--allow-partial` | a rí ìyípadà, àwọn àkíyèsí tí a kò fìdí rẹ̀ múlẹ̀, tàbí àyẹ̀wò tí kò pé | - |
| `export` | a kọ ìwé-àṣẹ | a kò lè kọ ìwé-àṣẹ | ìtẹ̀wọlé tí kò ṣeé kà, àyẹ̀wò tí kò pé láìsí `--allow-partial`, tàbí dátà tí kò ṣeé kó jáde láìléwu | - | - |

## Ìṣètò

| Mọ́dúlù | Ojúṣe |
| --- | --- |
| `cli.py` | Àwọn àṣàyàn àṣẹ, ìpinnu profáìlì, àyẹ̀wò ìṣáájú, ṣíṣàyẹ̀wò àti ìjábọ̀ |
| `scanner.py`, `probes.py` | Ìfẹ̀sí ibi-àfojúsùn, àwọn òṣìṣẹ́ tí ó ní ààlà, ìwádìí ẹ̀rọ agbàlejò àti àwọn àkíyèsí iṣẹ́ |
| `config.py`, `profiles.py` | Àwọn ìtumọ̀ iṣẹ́ àti àwọn profáìlì àkọsílẹ̀ iṣẹ́ tí a fìdí rẹ̀ múlẹ̀ |
| `models.py`, `output.py` | Àwọn irú èsì àti ìfihàn terminal/JSON/CSV |
| `history.py`, `diff.py` | Ìtàn SQLite àti ìfiwéra àwòrán fáìlì tí ó ní ẹ̀dà |
| `preflight.py` | Àwọn àyẹ̀wò abẹ́lé àti ìwádìí ẹ̀dà Nmap tí ó ní ààlà |
| `export.py` | Àwọn ìwé-àṣẹ ìkówọlé Kadupul tí a fìdí rẹ̀ múlẹ̀ tí a sì fi àmì-ọ̀rọ̀ sí |

Àkíyèsí iṣẹ́ kọ̀ọ̀kan ń kọ ipò rẹ̀ sílẹ̀ lọ́tọ̀ kúrò lára ìdánimọ̀ tí ó pòkìkí.
Àwọn kíkà àti àwọn àkókò-ìparí ní ààlà; àwọn àṣìṣe ìwádìí ń wà nínú àwọn àṣìṣe ẹ̀rọ agbàlejò. Ìtàn
SQLite ń lo àwọn ìṣòwò (transactions), ìmọ́tótó ìsopọ̀ tí ó ṣe kedere, àti àwọn ọ̀nà àtòjọ àti
ìfiwéra kíkà-nìkan. Àwọn àṣírí SNMP ń wọlé nípasẹ̀ àwọn oníyípadà àyíká tàbí àwọn fáìlì àṣírí
nìkan; ìtàn àkọsílẹ̀ iṣẹ́ ń tọ́jú àwọn ètò tí kò ní àṣírí tí ó ń ṣiṣẹ́. Wo
[Ètò Ìṣẹ̀dá](../../../docs/architecture.md) fún ìlànà àyẹ̀wò, àwọn ààlà rẹ̀ àti àwọn ààlà
ìgbẹ́kẹ̀lé, àti [SECURITY.md](../../../SECURITY.md#authorized-use) fún lílo lábẹ́ àṣẹ.


## Lílo

Ṣe àyẹ̀wò àwọn nẹ́tíwọ́ọ̀kì tí o ń ṣàkóso nìkan.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Àṣàyàn | Ìtumọ̀ |
| --- | --- |
| `NETWORK` | CIDR, IP, tàbí orúkọ agbàlejò; ó jẹ́ àṣàyàn pẹ̀lú `--profile`. A ń kọ àwọn ìdánimọ̀ ààyè IPv6. |
| `-o, --output PATH` | Kọ ìjábọ̀ kan. Ìrísí rẹ̀ ń tẹ̀lé ìfàgùn orúkọ fáìlì (`.json`, `.csv`); àwọn ìfàgùn mìíràn ń padà sí JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Fi agbára yan ìrísí ìjábọ̀. Kò ní ipa láìsí `--output`. `.sh` ń yan `kadupul`. |
| `-v, --verbose` | Àkọsílẹ̀ ìwádìí àṣìṣe (debug). |
| `-q, --quiet` | Pa àwọn èsì, ìlọsíwájú àti àwọn àkọsílẹ̀ ìsọfúnni mọ́; àwọn ìkìlọ̀ àti àwọn àṣìṣe ṣì ń hàn lórí stderr. |
| `--backend asyncio\|nmap` | Ìwádìí ẹ̀rọ agbàlejò. `asyncio` (àkọ́bẹ̀rẹ̀) ń ṣèwádìí àwọn pọ́ọ̀tì iṣẹ́ tààrà; `nmap` ń kọ́kọ́ ṣe ìwádìí ping nmap ó sì nílò ètò `nmap` lórí `PATH`. |
| `--timeout SECONDS` | Àkókò ìdúró fún àwọn ìwádìí tí kò ṣètò àkókò tiwọn (àkọ́bẹ̀rẹ̀ 1.0). Àwọn ìwádìí ìsopọ̀ tí a kọ́ sínú ètò ń lo 0.3s àfi bí tábìlì iṣẹ́ bá ṣètò `timeout`. |
| `--concurrency N` | Àwọn ìwádìí tí ń lọ lọ́wọ́ lẹ́ẹ̀kan náà (àkọ́bẹ̀rẹ̀ 256). |
| `--deadline SECONDS` | Dá gbogbo àyẹ̀wò dúró, títí kan ìwádìí nmap, lẹ́yìn àkókò yìí (àkọ́bẹ̀rẹ̀ 3600, ó pọ̀ jù 604800; oníyípadà àyíká `HOSTCENSUS_DEADLINE`). Àwọn ẹ̀rọ agbàlejò tí ó parí ni a ń kọ sínú ìjábọ̀ pẹ̀lú `"complete": false`, a kò kọ ìtàn tàbí àwòrán kankan, `scan` sì ń jáde pẹ̀lú 4. |
| `--config PATH` | Àwọn ìtumọ̀ iṣẹ́ TOML àti àwọn ètò `[profiles]` tí a fún ní orúkọ tí ó jẹ́ àṣàyàn. |
| `--profile NAME` | Lo profáìlì tí a fún ní orúkọ; ó ń lo `hostcensus.toml` bí àkọ́bẹ̀rẹ̀ nígbà tí a bá fi `--config` sílẹ̀. |
| `--exclude IP/CIDR` | Fi ìyọkúrò kún un; tún ṣe bí ó ṣe yẹ. Ẹ̀rọ agbàlejò IPv4 tí a yọ kúrò tún ń yọ àwọn àdírẹ́ẹ̀sì IPv6 tí ó dé ọ̀dọ̀ rẹ̀ kúrò: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) àti 6to4. A ń wo àwọn ibi-àfojúsùn àti ìyọkúrò IPv4-mapped bíi àdírẹ́ẹ̀sì IPv4 tí wọ́n dúró fún. |
| `--max-hosts N` | Ààlà àdírẹ́ẹ̀sì tí a ń yẹ̀ wò ṣáájú àwọn ìyọkúrò (àkọ́bẹ̀rẹ̀/ààlà gíga jù lọ 65,536). |
| `--history PATH` | Kọ àyẹ̀wò tí ó parí sílẹ̀ nínú dátábéèsì ìtàn SQLite tí a yàn láti lò. |
| `--services NAMES` | Àtòjọ àwọn orúkọ iṣẹ́ tí a fi kọ́mà pín láti yẹ̀ wò, ní ìtòlẹ́sẹẹsẹ yẹn (àkọ́bẹ̀rẹ̀: gbogbo rẹ̀). |
| `--ports SPEC` | Àtòjọ tí a fi kọ́mà pín ti `NAME=PORT` (gbe iṣẹ́ kan lọ sí ibòmíràn) tàbí `PORT` (fi àyẹ̀wò TCP lásán tí a pè ní `tcp-PORT` kún un). |
| `--snmp-community-file PATH` | Fáìlì tí ó ní àwùjọ SNMPv2c fún ìbéèrè system MIB. Àyíká: `HOSTCENSUS_SNMP_COMMUNITY` (iye rẹ̀) tàbí `HOSTCENSUS_SNMP_COMMUNITY_FILE` (ọ̀nà rẹ̀). |
| `--snmp-user` | Olùlò SNMPv3. Àyíká: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (àkọ́bẹ̀rẹ̀), `SHA224`, `SHA256`, `SHA384`, `SHA512` àti fáìlì tí ó ní ọ̀rọ̀-ìgbaniwọlé. Àyíká: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` tàbí `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (àkọ́bẹ̀rẹ̀), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` àti fáìlì tí ó ní ọ̀rọ̀-ìgbaniwọlé. Àyíká: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` tàbí `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Tún kọ àwòrán tí ó ní ẹ̀dà fún `hostcensus diff`. |
| `--tls-ca-file PATH` | Fìdí àwọn ìwé-ẹ̀rí HTTPS múlẹ̀ lòdì sí àkójọpọ̀ PEM yìí dípò ibi-ìfipamọ́ ètò. Àyíká: `HOSTCENSUS_TLS_CA_FILE`. |

Ní àkọ́bẹ̀rẹ̀, a ń yẹ ẹ̀rọ agbàlejò kọ̀ọ̀kan wò fún SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) àti HTTPS (TCP 443). A ń dán àwọn pọ́ọ̀tì TCP wò pẹ̀lú ìsopọ̀ pípé. A ń dán SNMP wò pẹ̀lú ìbéèrè ìwádìí ẹ̀rọ SNMPv3, èyí tí aṣojú SNMPv3 èyíkéyìí gbọ́dọ̀ dáhùn láìsí ẹ̀rí-ìdánimọ̀; àwọn aṣojú tí ń sọ v1/v2c nìkan ni ìwádìí yìí kò ní rí. Pẹ̀lú ètò-ìpìlẹ̀ asyncio, a ka ẹ̀rọ agbàlejò sí alààyè nígbà tí ìwádìí èyíkéyìí bá rí ìdáhùn gbà, títí kan ìsopọ̀ tí a kọ̀, nítorí náà ẹ̀rọ agbàlejò tí ó bá da gbogbo ìwádìí nù ní `alive=false` àti àṣìṣe "Host is down"; èyí kò fi hàn pé ó ti pa ní ti gidi. Pẹ̀lú `--backend nmap`, nmap ló ń pinnu àwọn ẹ̀rọ agbàlejò tí ó wà láàyè (ICMP gẹ́gẹ́ bí root, TCP 80/443 bí kò bá rí bẹ́ẹ̀).

### Àwọn ìtẹ̀ka iṣẹ́

A ń ṣe ìtẹ̀ka iṣẹ́ kọ̀ọ̀kan tí ó ṣí sílẹ̀ láti inú ohun tí ó fi ránṣẹ́ ṣáájú ìwọlé èyíkéyìí. Kò sí ohun tí ń ṣe ìfìdímúlẹ̀ ìdánimọ̀ àfi ìbéèrè SNMP, àti nígbà tí o bá pèsè àwọn ẹ̀rí-ìdánimọ̀ nìkan.

| Ìwádìí | Ohun tí ó ń kà | `version` | Àwọn kọ́kọ́rọ́ `details` |
| --- | --- | --- | --- |
| `ssh` | Ìlà ìdánimọ̀ RFC 4253 | sọ́fítíwè, àpẹẹrẹ `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Ìbọwọ́lù àkọ́kọ́ ti MySQL/MariaDB | ẹ̀dà sáfà | `server_version`, `flavor`, `auth_plugin`, tàbí `error_code`/`error` |
| `http` | Ìdáhùn `HEAD /` | Àkọlé `Server` | `status`, `server` |
| `https` | Ìbọwọ́lù TLS, ìwé-ẹ̀rí, `HEAD /` | Àkọlé `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Ìwádìí SNMPv3; pẹ̀lú ẹ̀rí-ìdánimọ̀, GET ti sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; pẹ̀lú ẹ̀rí-ìdánimọ̀ `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, tàbí `snmp_error` |

A ń túmọ̀ ibi-àfojúsùn orúkọ agbàlejò lẹ́ẹ̀kan fún ẹ̀rọ agbàlejò kọ̀ọ̀kan, gbogbo ìwádìí sì ń sopọ̀ mọ́ àdírẹ́ẹ̀sì yẹn, tí a kọ sílẹ̀ bí `address` nínú àwọn èsì; a ń lo orúkọ náà fún TLS SNI, ìfìdímúlẹ̀ ìwé-ẹ̀rí àti àkọlé `Host` ti HTTP nìkan. Orúkọ tí kò bá lè túmọ̀ ń fúnni ní àwọn ipò `unknown` àti àṣìṣe `Cannot resolve`. A ń pa àwọn orúkọ DNS ìpadàbọ̀ mọ́ nígbà tí wọ́n bá ní àwọn lẹ́tà orúkọ agbàlejò nìkan, àti pé ìwádìí 16 ló pọ̀ jù tí ń ṣiṣẹ́ lẹ́ẹ̀kan náà. HTTPS ń lo ìfìdímúlẹ̀ ìwé-ẹ̀rí àti orúkọ agbàlejò lòdì sí ibi-ìfipamọ́ ètò tàbí `--tls-ca-file`. A ń gbé ibi-ìfipamọ́ ìgbẹ́kẹ̀lé wọlé lẹ́ẹ̀kan fún àyẹ̀wò náà a sì ń tún un lò fún gbogbo ìwádìí HTTPS. A ń ṣàkóso àkókò ìsopọ̀ TCP àti ìbọwọ́lù TLS lọ́tọ̀ọ̀tọ̀, nítorí náà pọ́ọ̀tì tí ó gba ìsopọ̀ ṣùgbọ́n tí ó dá ìbọwọ́lù dúró jẹ́ `open` pẹ̀lú `tls_error`, kì í ṣe `filtered`. Tí ìfìdímúlẹ̀ bá kùnà, èsì náà ń kọ `cert_verified: false` àti `cert_verify_error` sílẹ̀; kì í tún gbìyànjú pẹ̀lú àwọn ètò tí kò lágbára tàbí kí ó fi ìbéèrè HTTP ránṣẹ́. A ń kó àlàyé ìwé-ẹ̀rí àti àwọn àkọlé HTTP jọ lẹ́yìn tí ìfìdímúlẹ̀ bá ṣàṣeyọrí nìkan. Pèsè àkójọpọ̀ CA tí ó tọ́ fún àwọn iṣẹ́ CA àdáni. Àwọn ìjábọ̀ àtijọ́ lè ní `cert_read_unverified`, èyí tí àwọn ìwádìí lọ́wọ́lọ́wọ́ kò tún ń mú jáde mọ́.

A ń ka àwọn àṣírí SNMP láti inú àwọn oníyípadà àyíká tàbí láti inú àwọn fáìlì (`--snmp-*-file`, tàbí oníyípadà `HOSTCENSUS_SNMP_*_FILE` tí ó bá a mu) nìkan, kì í ṣe láti inú àwọn iye ìlà-àṣẹ rárá, èyí tí àwọn olùlò abẹ́lé mìíràn lè rí nínú àtòjọ ìlànà. `--snmp-community`, `--snmp-auth-key` àti `--snmp-priv-key` pẹ̀lú iye kan ń jáde pẹ̀lú kóòdù 2 wọ́n sì ń dárúkọ ohun tí ó rọ́pò wọn. Fáìlì àṣírí gbọ́dọ̀ jẹ́ UTF-8 tí kò ṣófo tí kò ju báìtì 4096 lọ; a ń fojú fo ìlà-tuntun ìparí kan, àti pé ṣíṣètò oníyípadà àti fáìlì fún àṣírí kan náà jẹ́ àṣìṣe. Àwọn àṣìṣe ń dárúkọ fáìlì náà ṣùgbọ́n wọn kì í tẹ àkóónú rẹ̀ jáde láéláé. Àwọn ìjábọ̀ àyẹ̀wò àti ìtàn kì í mọ̀ọ́mọ̀ ní àwọn iye ẹ̀rí-ìdánimọ̀ nínú. Olùkójáde ní àṣàyàn `--include-credentials` ọ̀tọ̀ tí ó ṣe kedere tí a ṣàlàyé ní ìsàlẹ̀. Àwùjọ kan ń yan SNMPv2c; olùlò kan ń yan SNMPv3, pẹ̀lú ìfìdímúlẹ̀ ìdánimọ̀ nígbà tí a bá fúnni ní kọ́kọ́rọ́ ìfìdímúlẹ̀ àti àṣírí nígbà tí a bá fúnni ní kọ́kọ́rọ́ méjèèjì (`snmp_security_level` ń kọ èyí tí ó jẹ́ sílẹ̀). hostcensus ń kọ̀, pẹ̀lú kóòdù ìjáde 2, láti so àwùjọ pọ̀ mọ́ olùlò v3, láti lo kọ́kọ́rọ́ àṣírí láìsí kọ́kọ́rọ́ ìfìdímúlẹ̀, tàbí láti lo àwọn kọ́kọ́rọ́ láìsí olùlò, kò sì ní tún ìbéèrè v3 tí ó kùnà gbìyànjú pẹ̀lú v2c tàbí ìpele ààbò tí ó rẹlẹ̀ jù. Àwọn aṣojú tí ń sọ v1/v2c nìkan ń fojú fo ìwádìí v3 tí kò ní ẹ̀rí-ìdánimọ̀, nítorí náà wọ́n ń hàn bí ṣíṣí nígbà tí a bá pèsè àwùjọ kan nìkan.

A ń dín ọ̀rọ̀ àsíá kù sí àwọn lẹ́tà tí ó ṣeé tẹ̀ jáde a sì ń pa á mọ́ ní lẹ́tà 256 ṣáájú kí a tó tọ́jú rẹ̀ tàbí fi hàn. Àwọn kíkà náà ní ààlà pẹ̀lú: 4 KiB fún ìlà kọ̀ọ̀kan, 4 KiB fún ìkíni MySQL, 16 KiB ti àwọn àkọlé HTTP. A ń gé ID ẹ̀rọ SNMP tí ó gùn ju àwọn ọ́kítẹ́ẹ̀tì 32 lọ ṣáájú kí a tó tọ́jú rẹ̀. HTTP àti HTTPS ń fi àkọlé Host ránṣẹ́ pẹ̀lú àdírẹ́ẹ̀sì IPv6 nínú àkámọ́ onígun àti pẹ̀lú pọ́ọ̀tì nígbà tí kì í bá ṣe 80 tàbí 443. Àwọn sẹ́ẹ̀lì CSV tí ó bẹ̀rẹ̀ pẹ̀lú ohun-ìtànṣán fọ́múlà ìwé-ìṣirò ni a ń fi àmì síwájú wọn kí sẹ́ẹ̀lì náà lè dúró bí ọ̀rọ̀.

### Àwọn ààlà

Ìṣiṣẹ́ kan ń gba ó pọ̀ jù àdírẹ́ẹ̀sì 65,536, iṣẹ́ 64, àti ìwádìí 524,288 (àwọn ẹ̀rọ agbàlejò ní ìlọ́po àwọn iṣẹ́); àwọn ìbéèrè tí ó tóbi jù ń jáde pẹ̀lú kóòdù 2 ṣáájú kí a tó fi ohunkóhun ránṣẹ́. `--concurrency` ní ààlà àwọn sọ́kẹ́ẹ̀tì 4096. Ìwádìí kọ̀ọ̀kan ní àkókò-ìparí líle tí ó jẹ́ ìlọ́po mẹ́rin àkókò tirẹ̀. Àwọn ìwádìí ìsopọ̀ (`tcp`, `ssh`, `mysql`, `http`) ń lo ìṣẹ́jú-àáyá 0.3 àfi bí iṣẹ́ yẹn bá ṣètò `timeout`. SNMP àti HTTPS ń lo `--timeout` (àkọ́bẹ̀rẹ̀ 1.0) nígbà tí wọn kò bá ṣètò ọ̀kan. Ìwádìí tí ó bá dé àkókò-ìparí ni a ń ròyìn bí `unknown` pẹ̀lú "probe timed out" nínú `errors`. Àwọn ìkùnà sọ́kẹ́ẹ̀tì abẹ́lé (fún àpẹẹrẹ píparí àwọn olùtọ́ka fáìlì) tún jẹ́ `unknown` pẹ̀lú àṣìṣe tí a kọ sílẹ̀; wọn kì í jẹ́ pọ́ọ̀tì tí a sẹ́ tàbí ẹ̀rọ agbàlejò tí ó pa láéláé. Ṣáájú ìwádìí, hostcensus ń gbé ààlà rírọrùn fáìlì ṣíṣí sókè sí ààlà líle láti gba `--concurrency` pẹ̀lú olùtọ́ka 64; nígbà tí kò bá lè ṣe bẹ́ẹ̀, àyẹ̀wò ìṣáájú `open files` ń kùnà, `scan` sì ń jáde pẹ̀lú 1 ṣáájú kí ó tó fi ìrìn-àjò dátà ránṣẹ́. Ìwádìí Nmap ń lo ìpẹ̀kun àkókò ẹ̀rọ agbàlejò ìṣẹ́jú-àáyá 30. A ń fi ìṣáájú-àdírẹ́ẹ̀sì ránṣẹ́ sí nmap ní ìrísí CIDR, ìwádìí sì ń kùnà pẹ̀lú ìjáde 1 nígbà tí nmap bá ròyìn àdírẹ́ẹ̀sì tí ó kéré ju èyí tí a fún un lọ (fún àpẹẹrẹ orúkọ tí kò lè túmọ̀) dípò kí ó sàmì sí àwọn ẹ̀rọ agbàlejò bí èyí tí ó pa. A ń túmọ̀ ibi-àfojúsùn orúkọ agbàlejò lẹ́ẹ̀kan a sì ń fún nmap ní àdírẹ́ẹ̀sì yẹn, kí ìwádìí àti àwọn àyẹ̀wò lè dé orí ẹ̀rọ kan náà. Ìṣáájú-àdírẹ́ẹ̀sì pípé jẹ́ ìlànà nmap kan tí àkókò-ìparí ìlànà-abẹ́ rẹ̀ jẹ́ ìṣẹ́jú-àáyá 35 fún gbogbo àdírẹ́ẹ̀sì 256, tí a yí sókè. Àwọn ìwádìí pẹ̀lú ìyọkúrò ń lo àkójọ àwọn ẹ̀rọ agbàlejò 256 àti àkókò-ìparí ìṣẹ́jú-àáyá 35 fún àkójọ kọ̀ọ̀kan. Ìṣẹ̀dá òṣìṣẹ́ ní ààlà láìgbára lé ìwọ̀n ààyè. DNS ìpadàbọ̀ àti ìtúmọ̀ orúkọ agbàlejò ní àkókò-ìparí ìṣẹ́jú-àáyá méjì ọ̀tọ̀; ìpè olùtúmọ̀ tí kì í padà láéláé ni a ń fi sílẹ̀ lórí okùn tirẹ̀, kí ó má baà jẹ́ kí hostcensus ṣiṣẹ́ rékọjá àwọn ààlà wọ̀nyí. Ó pọ̀ jù ìwádìí 16 ló ń ṣiṣẹ́ lẹ́ẹ̀kan náà, ìpè tí a fi sílẹ̀ sì ń pa ààyè rẹ̀ mọ́ títí yóò fi padà, kí iye àwọn okùn tí ó dì mọ́lẹ̀ lè ní ààlà; tí gbogbo 16 bá dì mọ́lẹ̀, àwọn ìwádìí tí ó tẹ̀lé e ń tò lẹ́sẹẹsẹ fún ààyè kan lẹ́yìn àkókò-ìparí ìṣẹ́jú-àáyá méjì (èyí tí ó bẹ̀rẹ̀ ní kété tí ààyè kan bá ṣófo) títí `--deadline` yóò fi dá àyẹ̀wò náà dúró. `NetworkScanner` tí a lò bí ilé-ìkàwé láìsí `deadline` lè dúró de irú ààyè bẹ́ẹ̀ títí láé. `--deadline` (àkọ́bẹ̀rẹ̀ wákàtí kan) ń fi ààlà sí gbogbo ìṣiṣẹ́ náà lórí àwọn wọ̀nyí.

### Ṣíṣètò àwọn iṣẹ́

A lè yí àwọn iṣẹ́ padà pẹ̀lú fáìlì TOML kan:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` jẹ́ ọ̀kan lára `tcp`, `ssh`, `mysql`, `http`, `https` tàbí `snmp` ó sì ń lo orúkọ iṣẹ́ bí àkọ́bẹ̀rẹ̀ nígbà tí yẹn bá jẹ́ ìwádìí, bí kò bá rí bẹ́ẹ̀ `tcp`. `snmp` nìkan ló ń lo UDP. Àwọn orúkọ iṣẹ́ jẹ́ àwọn lẹ́tà kékeré, àwọn nọ́ńbà, `-` àti `_`. Iṣẹ́ méjì kò lè pín pọ́ọ̀tì àti ìlànà ìbánisọ̀rọ̀ kan náà; ìtàn ń kọ ipò kan sílẹ̀ fún méjèèjì yẹn. `timeout` jẹ́ àṣàyàn, ní ìṣẹ́jú-àáyá, ó sì kéré tán 0.05. Àwọn ìwádìí irú ìsopọ̀ (`tcp`, `ssh`, `mysql`, `http`) ń lo ìṣẹ́jú-àáyá 0.3 bí àkọ́bẹ̀rẹ̀. `snmp` àti `https` ń lo `--timeout` ti àyẹ̀wò nígbà tí iṣẹ́ náà kò bá ṣètò `timeout`. `--timeout` kì í rọ́pò àkókò tí iṣẹ́ náà ti ní tẹ́lẹ̀.

Àwọn ìjábọ̀ JSON jẹ́ àwọn àkọsílẹ̀ tí ó ní ẹ̀dà (`"format": "hostcensus-report"`, `"version": 1`) tí ó ń kọ ibi-àfojúsùn, àwọn iṣẹ́ tí a ṣèwádìí àti àwọn ètò sílẹ̀ lẹ́gbẹ̀ẹ́ `devices`; `--format json` láìsí `-o` ń kọ ìjábọ̀ náà sí stdout dípò tábìlì. Gbogbo èsì JSON ní àwòrán (schema) tí a tẹ̀ jáde; wo [Èsì JSON](../../../docs/json-output.md). Àwọn ẹ̀rọ ń pa àwọn ààyè àtijọ́ `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` àti `errors` mọ́ wọ́n sì ń fi àtòjọ `services` kún un pẹ̀lú `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, tàbí `unknown` nígbà tí ìwádìí bá kùnà ní abẹ́lé tàbí dé àkókò-ìparí rẹ̀), `version` àti `details` ti ìwádìí kọ̀ọ̀kan. Èsì CSV ń gba àwọn ọ̀wọ́n ìparí `services` àti `versions` fún àwọn tí ó ṣí sílẹ̀. Àwọn iye òótọ́/irọ́ `ssh`, `snmp` àti `mysql` ń tẹ̀lé àwọn iṣẹ́ tí ó ní àwọn orúkọ wọ̀nyẹn gan-an.


## Àwọn profáìlì àkọsílẹ̀ iṣẹ́, àyẹ̀wò ìṣáájú, àti ìtàn abẹ́lé

Àwọn profáìlì tí a fún ní orúkọ ń pín fáìlì TOML kan náà pẹ̀lú àwọn ìtumọ̀ `[services]` tí ó wà tẹ́lẹ̀. Ṣe àdàkọ
[hostcensus.example.toml](../../../hostcensus.example.toml) sí `hostcensus.toml` kí o sì ṣètò àwọn nẹ́tíwọ́ọ̀kì
tí o ń ṣàkóso:

```toml
[profiles.office]
network = "192.168.1.0/24"
exclusions = ["192.168.1.1"]
services = "ssh,http,https,mysql"
concurrency = 32
timeout = 1.0
max_hosts = 256
backend = "asyncio"
```

```bash
hostcensus profiles --config hostcensus.toml
hostcensus preflight --profile office --config hostcensus.toml
hostcensus scan --profile office --config hostcensus.toml -o report.json
```

`preflight` ń túmọ̀ àwọn àṣàyàn àti profáìlì gẹ́gẹ́ bí `scan` ti ń ṣe, títí kan
`--concurrency` fún àyẹ̀wò fáìlì ṣíṣí, nítorí náà àyẹ̀wò ìṣáájú tí ó yege túmọ̀ sí pé `scan` yóò
bẹ̀rẹ̀ pẹ̀lú ètò kan náà.

Àwọn profáìlì ń gba `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, àti `max_hosts`. `services` àti `ports` ń lo ìlànà àtòjọ kọ́mà
tí ó wà tẹ́lẹ̀. Àwọn àṣàyàn CLI tí a sọ ní pàtó ń borí àwọn ètò profáìlì; àwọn àṣàyàn `--exclude` tí a tún ṣe
ń fi kún àwọn ìyọkúrò profáìlì. Nẹ́tíwọ́ọ̀kì tí a sọ ní pàtó pẹ̀lú `--profile` gbọ́dọ̀ wà
nínú ààyè IP/CIDR ti profáìlì yẹn. A ṣì ń ṣe àtìlẹ́yìn fún àwọn orúkọ agbàlejò fún àwọn àyẹ̀wò
tààrà, ṣùgbọ́n a kò lè so wọ́n pọ̀ mọ́ àwọn ìyọkúrò IP. Àwọn ààlà ẹ̀rọ agbàlejò ń ṣiṣẹ́ ṣáájú
àwọn ìyọkúrò; ààlà gbogbo ìwádìí ṣì ń ṣiṣẹ́ lẹ́yìn náà. A ń yọ àwọn ẹ̀rọ agbàlejò tí a yọ kúrò
nínú àwọn àyẹ̀wò iṣẹ́ àti ìwádìí Nmap tí ó jẹ́ àṣàyàn.

Gbogbo àyẹ̀wò ń ṣe àwọn àyẹ̀wò ìṣáájú abẹ́lé ṣáájú ìrìn-àjò dátà sí ibi-àfojúsùn: àwọn ààlà ibi-àfojúsùn/ìwádìí,
àǹfààní sí ibi-ìfipamọ́, wíwà ètò/ìbò Nmap tí ó jẹ́ àṣàyàn, àwòrán ìtàn,
àti àkójọpọ̀ TLS CA tí a ṣètò. `preflight` ń ròyìn ní JSON kì í sì í ṣàyẹ̀wò
àwọn ibi-àfojúsùn tàbí ṣẹ̀dá dátábéèsì ìtàn. Ó ń kọ fáìlì ẹgbẹ́ kan fún ìgbà díẹ̀ láti dán
àǹfààní ibi-ìfipamọ́ wò láìyí àkóónú tí ó wà tẹ́lẹ̀ padà. Ètò-ìpìlẹ̀ asyncio àkọ́bẹ̀rẹ̀
kò ṣì nílò Nmap tàbí root. Àwọn ọ̀nà ibi-ìfipamọ́ gbọ́dọ̀ yàtọ̀ sí ara
wọn àti sí ètò ìtẹ̀wọlé, títí kan àwọn ìjápọ̀ líle (hard links); a ń kọ àwọn ìjápọ̀ àmì (symlinks) ibi-ìfipamọ́. Àwọn àyẹ̀wò tí ó kùnà ń dá 1 padà; ààyè/ètò tí kò tọ́ ń dá 2 padà.

Kíkọ ìjábọ̀ àti ìkójáde nílò àtìlẹ́yìn `O_NOFOLLOW`. Lórí àwọn ètò tí kò ní i,
títí kan Windows, àwọn kíkọ wọ̀nyí ń kùnà láìṣí tàbí gé ibi-ìfipamọ́ kúrú.
Àwọn ìjábọ̀ tuntun àti àwọn ìwé-àṣẹ ìkójáde wà fún oní rẹ̀ nìkan (ipò 0600); rírọ́pò fáìlì tí ó wà tẹ́lẹ̀ ń pa àwọn
àṣẹ rẹ̀ mọ́. Kíkọ sí inú páìpù tí a fún ní orúkọ tí kò ní olùkà ń kùnà lẹ́sẹ̀kẹsẹ̀ dípò kí ó máa dúró. A tún ń ṣẹ̀dá dátábéèsì `--history` tuntun fún oní rẹ̀ nìkan; èyí tí ó wà tẹ́lẹ̀ ń pa ipò rẹ̀ mọ́. Àwọn ìfiránṣẹ́ àkọsílẹ̀ ń lọ sí stderr nígbà gbogbo, kí stdout lè gbé àwọn èsì nìkan. Àwọn ìkójáde tí ó ní àwọn ẹ̀rí-ìdánimọ̀ ń fi ipò 0600 ṣiṣẹ́ nígbà gbogbo.

Ìtàn jẹ́ ohun tí a yàn láti lò ó sì ń ṣe àfikún sí àwọn àwòrán JSON tí ó wà tẹ́lẹ̀ àti àṣẹ `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Lo àwọn ID láti `history`; àpẹẹrẹ náà ń rò pé dátábéèsì tuntun ni. A ń tọ́jú àwọn àwòrán
ní ọ̀nà oní-ìṣòwò pẹ̀lú àwọn àkókò ìbẹ̀rẹ̀/ìparí UTC, ẹ̀dà páákì, àwọn ètò tí kò ní àṣírí tí ó ń ṣiṣẹ́,
àwọn àkópọ̀, àti gbogbo àwọn àkíyèsí ẹ̀rọ agbàlejò/iṣẹ́, títí kan àwọn àṣìṣe fún ẹ̀rọ agbàlejò kọ̀ọ̀kan.
A ń pa àwọn àkíyèsí ẹ̀rọ agbàlejò tí kò pé mọ́. A kì í tọ́jú àwọn ìṣiṣẹ́ tí a fagi lé. A pa àwọn àdéhùn
kóòdù ìjáde ìjábọ̀, àwòrán, ìkójáde, àti àyẹ̀wò tí ó wà tẹ́lẹ̀ mọ́.

`history` ń tò àwọn àkópọ̀ JSON láìka gbogbo dátà ẹ̀rọ ìtàn.
`compare` ń ka àwọn àyẹ̀wò méjì tí a tọ́jú, ó nílò ìdánimọ̀ ibi-àfojúsùn kan náà àti àwọn pọ́ọ̀tì tí a yàn
kan náà, ó sì ń ròyìn ìdáhùn, ipò, àti àwọn ìyípadà ipò pọ́ọ̀tì. ID àyẹ̀wò àkọ́kọ́
gbọ́dọ̀ ṣáájú ID tí ó tẹ̀lé e. Nígbà tí àyẹ̀wò méjèèjì bá kọ `timeout` tàbí `backend` sílẹ̀
tí àwọn iye wọ̀nyẹn sì yàtọ̀, ìjábọ̀ náà ń fi ìkìlọ̀ hàn ó sì ṣì ń fi àwọn
àkíyèsí náà wé ara wọn. Àkókò ìdúró tí ó yàtọ̀ lè jẹ́ kí pọ́ọ̀tì tí a sẹ́ hàn bí èyí tí ó ṣí. Àwọn àṣìṣe ẹ̀rọ-àyẹ̀wò
àti àwọn àkíyèsí pọ́ọ̀tì àìmọ̀ ni a ń sàmì sí bí èyí tí kò dájú dípò kí a wò wọ́n bí
ìparẹ́ tàbí títìpa tí a fìdí múlẹ̀: àwọn ẹ̀rọ agbàlejò tí ó ní àṣìṣe ń hàn nínú `uncertain_hosts`, àti
gbogbo ìyípadà pọ́ọ̀tì tí ó kan `unknown` (títí kan àìmọ̀ nínú àyẹ̀wò méjèèjì) ni a ń tò
nínú `unconfirmed_ports` dípò `port_changes`, àfi pọ́ọ̀tì tí ó ṣí nínú
àyẹ̀wò tí ó tẹ̀lé e, èyí tí ó jẹ́ ìyípadà pọ́ọ̀tì. `compare` àti `diff` ń pín àwọn pọ́ọ̀tì sí ìsọ̀rí pẹ̀lú òfin kan náà.
`no_longer_responding` túmọ̀ sí àìsí ìdáhùn, kì í ṣe ẹ̀rí yíyọ ẹ̀rọ kúrò.
Kóòdù ìjáde àyẹ̀wò 0 kò ṣèlérí pé gbogbo ẹ̀rọ agbàlejò ló dáhùn: yẹ àwọn àṣìṣe fún ẹ̀rọ agbàlejò kọ̀ọ̀kan wò. Àṣeyọrí ìfiwéra ń dá 0 padà bóyá ìyípadà wà tàbí kò sí; fáìlì `diff` tí ó wà tẹ́lẹ̀
ń pa àdéhùn kóòdù ìjáde 3 rẹ̀ mọ́. Ìtàn tí a kò ṣe àtìlẹ́yìn fún tàbí tí ó bàjẹ́ ń dá 1 padà.

Ìtàn ń tọ́jú ìsọfúnni àkọsílẹ̀ iṣẹ́, nítorí náà yan àpò ìwé abẹ́lé tí a dáàbò bo dáadáa.
Àwọn fáìlì profáìlì àti àwọn ètò tí a tọ́jú kò ní àwọn ẹ̀rí-ìdánimọ̀ SNMP nínú;
ìtọ́jú ẹ̀rí-ìdánimọ̀ ń bá a lọ nípasẹ̀ àwọn àṣàyàn/àyíká àṣẹ-ìṣiṣẹ́ tí ó wà tẹ́lẹ̀.

## Ìyàtọ̀ àkọsílẹ̀ iṣẹ́

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Àwòrán jẹ́ JSON pẹ̀lú `format: "hostcensus-snapshot"`, `version: 1`, ẹ̀dà hostcensus, àkókò ìṣẹ̀dá UTC, ibi-àfojúsùn, `timeout` àti `backend` ti àyẹ̀wò nígbà tí àyẹ̀wò bá kọ wọ́n sílẹ̀, àwọn iṣẹ́ tí a ṣèwádìí, àti àwọn ẹ̀rọ agbàlejò alààyè ní ìrísí kan náà bí ìjábọ̀ `-o`. A fi àwọn ẹ̀rọ agbàlejò tí ó pa sílẹ̀. `diff` tún ń gba àwọn ìjábọ̀ JSON `scan -o` lásán, títí kan àwọn ti ṣáájú kí ààyè `services` tó wà.

`diff` ń ròyìn àwọn ẹ̀rọ agbàlejò tuntun àti èyí tí ó pòórá, àwọn pọ́ọ̀tì tí ó ṣí tàbí tì pa lórí àwọn ẹ̀rọ agbàlejò tí ó wà nínú méjèèjì, àti àwọn iṣẹ́ tí `version` wọn yí padà. A kì í fi àwọn pọ́ọ̀tì tí a ṣèwádìí nínú ọ̀kan ṣoṣo nínú àyẹ̀wò méjèèjì wé ara wọn, ìkìlọ̀ kan sì ń sọ bẹ́ẹ̀. Àwọn àkíyèsí tí ó kùnà kì í hàn bí "kò sí ìyípadà" láéláé: pọ́ọ̀tì tí ó jẹ́ `unknown` nínú ọ̀kankan nínú àyẹ̀wò méjèèjì tí kò sì ṣí nínú èyí tí ó tẹ̀lé e ni a ń tò lábẹ́ `unconfirmed`, kì í ṣe `closed`, pẹ̀lú `before` ti `open`, `unknown` tàbí `not-open` (tí a ṣèwádìí tí ó sì tì pa tàbí sẹ́) àti `after` ti `unknown` tàbí `not-open`; pọ́ọ̀tì tí ó ṣí báyìí ni a ń ròyìn lábẹ́ `opened` kódà bí ìwádìí àkọ́kọ́ bá kùnà. Ẹ̀rọ agbàlejò tí gbogbo ìwádìí rẹ̀ kùnà láìsí ìdáhùn nínú ọ̀kankan nínú àyẹ̀wò méjèèjì ni a ń tò lábẹ́ `unsettled_hosts` (pẹ̀lú `before`/`after` ti `up`, `uncertain` tàbí `absent`, títí kan nígbà tí ó bá kùnà nínú àyẹ̀wò méjèèjì tàbí tí ó bá sọnù nínú fáìlì kejì) dípò `vanished_hosts`; tí ó bá dáhùn nínú àyẹ̀wò tí ó tẹ̀lé e a tún ń ròyìn rẹ̀ bí ẹ̀rọ agbàlejò tuntun pẹ̀lú àwọn pọ́ọ̀tì rẹ̀ tí ó ṣí. Àwọn àwòrán ń pa àwọn ẹ̀rọ agbàlejò tí ó kùnà wọ̀nyẹn mọ́ nítorí ìdí yìí. Ìkìlọ̀ kan tún ń hàn nígbà tí àwọn ibi-àfojúsùn bá yàtọ̀, àti nígbà tí fáìlì méjèèjì bá kọ ìpẹ̀kun àkókò tàbí ètò-ìpìlẹ̀ sílẹ̀ tí àwọn iye wọ̀nyẹn sì yàtọ̀. `-o PATH` tún ń kọ ìrísí JSON sí inú fáìlì kan pẹ̀lú.

Ìjábọ̀ láti inú àyẹ̀wò tí `--deadline` dá dúró (`"complete": false`) ń tò àwọn ẹ̀rọ agbàlejò tí ó dé ọ̀dọ̀ wọn nìkan, nítorí náà `diff` àti `export` ń kọ̀ ọ́ pẹ̀lú kóòdù ìjáde 2. `--allow-partial` ń gbà á pẹ̀lú ìkìlọ̀ kan lórí stderr: `diff` wá ń tò àwọn ẹ̀rọ agbàlejò tí àyẹ̀wò tí kò pé náà kò tò rárá lábẹ́ `unsettled_hosts` gẹ́gẹ́ bí `unscanned` dípò èyí tí ó pòórá (ẹ̀rọ agbàlejò tí ó tò bí èyí tí ó pa ṣì jẹ́ èyí tí ó pòórá), ó ń ṣètò `partial` sí òótọ́ (true) kì í sì í ròyìn pé kò sí ìyípadà láéláé, `export` sì ń kọ ìkìlọ̀ kan sínú àkọlé ìwé-àṣẹ náà.

Àwọn kóòdù ìjáde `diff`: `0` kò sí ìyípadà, `3` a rí ìyípadà, àwọn àkíyèsí tí a kò lè fìdí rẹ̀ múlẹ̀, tàbí ìtẹ̀wọlé tí kò pé (`changed` jẹ́ òótọ́ nígbàkúgbà tí àtòjọ èyíkéyìí, títí kan `unsettled_hosts` àti `unconfirmed`, kò bá ṣófo, tàbí `partial` bá jẹ́ òótọ́), `2` fáìlì kan sọnù, kò ṣeé kà, kì í ṣe àwòrán tí a ṣe àtìlẹ́yìn fún, tàbí kò pé láìsí `--allow-partial`, `1` a kò lè kọ fáìlì `-o`.

## Ìkójáde Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (ẹ̀ka kan láti Cacti 1.2.31) kò ní ìkówọlé fáìlì ẹ̀rọ lọ́pọ̀. Ọ̀nà tí ó ṣe àtìlẹ́yìn fún láti fi àwọn ẹ̀rọ kún un láti inú ìwé-àṣẹ ni `cli/add_device.php`, ẹ̀rọ kan fún ìpè kọ̀ọ̀kan, pẹ̀lú àwọn àríyànjiyàn `--option=value`. `hostcensus export` ń kọ ìwé-àṣẹ POSIX `sh` ti àwọn ìpè wọ̀nyẹn:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Ẹ̀rọ agbàlejò alààyè kọ̀ọ̀kan ń di `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Àwọn ẹ̀rọ agbàlejò tí ìbéèrè SNMP ti àyẹ̀wò náà ti ṣàṣeyọrí lórí wọn ń gba `--version=2 --community=...` tàbí `--version=3 --username=... --authproto=... --password=...` (pẹ̀lú `--privproto`/`--privpass` fún authPriv), `--port` àti `--avail=snmp`. Ìkójáde SNMPv3 nílò `--snmp-user`, a sì kọ noAuthNoPriv nítorí `add_device.php` nílò ọ̀rọ̀-ìgbaniwọlé v3.
- Àwọn ẹ̀rọ agbàlejò mìíràn ń gba `--version=0 --avail=ping`, pẹ̀lú `--ping_method=tcp --ping_port=` pọ́ọ̀tì TCP àkọ́kọ́ tí ó ṣí, tàbí ICMP bí kò bá sí kankan.
- `--notes` ń tò àwọn iṣẹ́ tí ó ṣí àti àwọn ẹ̀dà wọn. `--description` jẹ́ orúkọ DNS ìpadàbọ̀ nígbà tí ó bá rọrùn (àwọn lẹ́tà, àwọn nọ́ńbà, `.`, `_`, `-`), bí kò bá rí bẹ́ẹ̀ IP, a sì ń jẹ́ kí ó jẹ́ àkànṣe, nítorí `add_device.php` ń wo àpèjúwe tí ó wà tẹ́lẹ̀ bí àtúnṣe sí ẹ̀rọ yẹn.

A ń fìdí gbogbo iye múlẹ̀ a sì ń fi àmì-ọ̀rọ̀ shell sí i pẹ̀lú `shlex.quote`. Ní àkọ́bẹ̀rẹ̀ a kì í kọ àṣírí SNMP kankan: ìwé-àṣẹ náà ń fẹ̀ `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` tàbí `HOSTCENSUS_SNMP_PRIV_KEY` ní àkókò ìṣiṣẹ́ ó sì ń dúró tí ọ̀kan kò bá ní iye. `--include-credentials` ń kọ àwọn iye láti inú àwọn oníyípadà àyíká wọ̀nyẹn sínú ìwé-àṣẹ náà dípò bẹ́ẹ̀, ó ń ṣẹ̀dá rẹ̀ pẹ̀lú ipò 0600, ó sì ń kọ ìkìlọ̀ sílẹ̀. `add_device.php` fúnra rẹ̀ ń tẹ àwùjọ náà jáde ó sì ń gba àwọn àṣírí bí àríyànjiyàn, èyí tí ó hàn nínú àtòjọ ìlànà sáfà Kadupul nígbà tí ìpè kọ̀ọ̀kan bá ń ṣiṣẹ́.

`add_device.php` ń jáde pẹ̀lú 1 fún àwọn ẹ̀dà-méjì àti àwọn àṣìṣe; ìwé-àṣẹ náà ń bá a lọ, ó ń ka àwọn ìkùnà, ó sì ń jáde pẹ̀lú 1 bí a kò bá fi ẹ̀rọ èyíkéyìí kún un. Àwọn ID àwòṣe ń wá láti `php cli/add_device.php --list-host-templates`. Àwọn kóòdù ìjáde `export`: `0` ti kọ, `2` ìtẹ̀wọlé tí kò ṣeé kà, àyẹ̀wò tí kò pé láìsí `--allow-partial`, tàbí dátà tí kò ṣeé kó jáde láìléwu, `1` a kò lè kọ ìwé-àṣẹ náà.

## Ìṣàkóso ẹ̀dà àti ìlànà ìtújáde

hostcensus ń tẹ̀lé [Semantic Versioning](https://semver.org/spec/v2.0.0.html): àwọn àtúnṣe
tí ó bá ara mu ń fi kún ẹ̀dà àtúnṣe kékeré (patch), àwọn ẹ̀yà tuntun/ìfọwọ́rọ́sẹ́yìn tí ó bá ara mu ń fi kún
ẹ̀dà kékeré (minor), àti àwọn ìyípadà tí ó fọ́ ìbámu ń fi kún ẹ̀dà ńlá (major).
Àwọn àṣẹ àti àṣàyàn, àwọn kóòdù ìjáde àti àwọn JSON schema ni àdéhùn gbogbogbòò;
ìwà tí a fọwọ́rọ́sẹ́yìn ń bá a lọ láti ṣiṣẹ́ títí di ìtújáde ńlá tí ó tẹ̀lé e, àfi bí
àtúnṣe ààbò kan bá nílò yíyí i padà ní kùtùkùtù (àkọsílẹ̀ ìyípadà yóò wá sọ ìdí rẹ̀).

release-please ń ṣí PR ìtújáde láti inú àwọn àkọlé Conventional Commit lórí `main`,
tí ń gbé `pyproject.toml`, `uv.lock` àti `CHANGES.md` sókè. Síso ó pọ̀ ń ṣẹ̀dá
àmì `vMAJOR.MINOR.PATCH` àti àkọ́kọ́ ìtújáde GitHub, sí èyí tí CI ń so wheel tí a dán wò,
ìpínkiri orísun àti àwọn checksum mọ́; GitHub ń tọ́jú àwọn ẹ̀rí ìkọ́lé fún
àwọn fáìlì wọ̀nyẹn nípasẹ̀ API ẹ̀rí rẹ̀. Olùtọ́jú kan ń ṣàyẹ̀wò ó sì ń tẹ
àkọ́kọ́ náà jáde ní kété tí a bá so àwọn fáìlì mọ́ ọn. A kì í rọ́pò àwọn ìtújáde láéláé.

Ìtẹ̀jáde ìgbẹ́kẹ̀lé PyPI jẹ́ ohun tí a yàn láti lò ó sì nílò ìjẹ́-oní iṣẹ́ àkànṣe, olùtẹ̀jáde
tí a gbẹ́kẹ̀lé àti àyíká `pypi`. Ó ń tẹ àwọn ohun-ìtújáde kan náà tí a ti yẹ̀ wò jáde
láìtún kọ́ tàbí tọ́jú àmì API. Àwọn ìtújáde tí a fún ní àmì nínú ibi-ìpamọ́ gbogbogbòò yìí
ń ṣẹ̀dá àwọn ẹ̀rí ohun-ìtújáde GitHub; àwọn ẹ̀ka àdáni nílò ètò tí a ṣe àtìlẹ́yìn fún
àti yíyàn ní pàtó. Wo
[ìtọ́sọ́nà ìtújáde pípé](../../../docs/releasing.md) fún ìṣètò, àwọn àṣẹ pàtó àti àwọn àtúngbìyànjú.

## Ìdàgbàsókè

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Àwọn ohun-èlò ìdàgbàsókè wà nínú àwọn ẹgbẹ́ ìgbẹ́kẹ̀lé [PEP 735](https://peps.python.org/pep-0735/)
nínú `pyproject.toml` (`dev`, `fuzz`, `build`), nítorí náà wọn kì í hàn nínú
dátà-àlàyé páákì tí a tẹ̀ jáde láéláé. `uv.lock` ni fáìlì ìtìpa kan ṣoṣo; CI ń fi sórí ẹ̀rọ pẹ̀lú
`uv sync --locked` ó sì ń kùnà nígbà tí fáìlì ìtìpa náà bá ti di àtijọ́. Yan olùtúmọ̀ pẹ̀lú
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), tàbí Python 3.12+ èyíkéyìí.

CI ń fi ààlà ìbòrí páákì 90% ṣiṣẹ́. Àwọn ìdánwò ẹyọkan ní àwọn sáfà loopback tí a ń ṣàkóso
àti àwọn ọ̀ràn profáìlì/ìtàn/olùfìdímúlẹ̀-ìtújáde láìsí ìkànnì; yàrá ìdánwò Compose ń ṣiṣẹ́
OpenSSH, MariaDB, nginx àti net-snmp lórí afárá tí a yà sọ́tọ̀. Ṣiṣẹ́ rẹ̀ pẹ̀lú
`make test-integration`. Wo [CONTRIBUTING.md](../../../CONTRIBUTING.md) àti
[àwọn ohun-èlò ìtújáde](../../../scripts/README.md).

Kọ̀ǹténà àṣẹ-ìṣiṣẹ́ ń ṣiṣẹ́ gẹ́gẹ́ bí UID/GID 10001 láìsí àpò ìwé ilé, láìsí ìwọlé shell
àti láìsí pip, ó sì lè kọ sí `/app/output`. Fún olùlò yẹn ní àǹfààní kíkọ sí
àpò ìwé èsì èyíkéyìí tí a so mọ́ ọn. Kò nílò àwọn agbára àfikún kankan ó sì ń ṣiṣẹ́ pẹ̀lú
ètò fáìlì root kíkà-nìkan, nítorí náà ó lè ṣiṣẹ́ bí:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap ń lo ìwà ìwádìí TCP aláìní-àǹfààní-àkànṣe rẹ̀ nínú kọ̀ǹténà yìí. CI ń jẹ́ kí
ìkọ́lé àwòrán kùnà lórí àléébù HIGH tàbí CRITICAL èyíkéyìí tí ó ṣeé tún ṣe tí Trivy bá ròyìn.

## Àwọn àyẹ̀wò ẹ̀wọ̀n ìpèsè

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
ń ṣiṣẹ́ lórí main àti lọ́sọ̀ọ̀sẹ̀, ó ń tẹ àmì rẹ̀ gidi jáde, ó sì ń gbé àwọn àwárí sórí àyẹ̀wò kóòdù
GitHub. A so àwọn Actions àti àwọn ìpìlẹ̀ kọ̀ǹténà mọ́ àwọn hash tí kò lè yí padà; a túmọ̀ àwọn ìgbẹ́kẹ̀lé Python
nínú `uv.lock`. Àwọn ìkùnà Bandit ń jẹ́ kí CI kùnà, àti ìdánwò fuzzing Atheris tí ó ní ààlà
ń dán àwọn olùtú SSH, MySQL, HTTP, ìwé-ẹ̀rí àti SNMPv3 BER wò
láìsí ìsopọ̀ nẹ́tíwọ́ọ̀kì.

Scorecard tún ń wọn iṣẹ́ àtúnyẹ̀wò ìtàn, oríṣiríṣi àwọn olùkópa, àti
orísun ìtújáde. Àwọn àmì wọ̀nyẹn ń fi ẹ̀rí gidi hàn; wọn kì í ṣe ìtẹnumọ́
pé gbogbo àyẹ̀wò ìṣàkóso tàbí ìtújáde ìtàn ti pé. Wo
[SECURITY.md](../../../SECURITY.md) àti [orísun ìtújáde](../../../docs/releasing.md).

## Ìyípadà sí èdè ìbílẹ̀

Àwọn ìfiránṣẹ́ CLI àti àwọn tábìlì àkópọ̀/ìyàtọ̀ lórí terminal ń ṣe àtìlẹ́yìn fún àwọn èdè ìbílẹ̀ 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) láìsí ìgbẹ́kẹ̀lé àṣẹ-ìṣiṣẹ́ àfikún kankan. Ìpinnu èdè ń bọ̀wọ̀ fún `--lang`, lẹ́yìn náà `LC_ALL`, `LC_MESSAGES`, àti `LANG`, tí ó ń padà sí `en`. Àwọn JSON schema, àwọn ọ̀wọ́n CSV, àti àwọn ìwé-àṣẹ ìkójáde kò yí padà ní gbogbo àwọn èdè ìbílẹ̀.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Ìkópa

Àwọn àfikún gbọ́dọ̀ ní ọ̀ràn tí a lè tún ṣe, kí wọ́n pa àwọn àdéhùn CLI àti
ìrísí-dátà tí a kọ sílẹ̀ mọ́, kí wọ́n sì yege nínú àwọn àyẹ̀wò dídára tí ó wà lókè. Wo
[CONTRIBUTING.md](../../../CONTRIBUTING.md) fún ìlànà ìṣiṣẹ́ ìdàgbàsókè àti
[ìtọ́sọ́nà ìtújáde](../../../docs/releasing.md) fún àwọn ìpinnu ìbámu àti ìṣàkóso ẹ̀dà.

## Ipò ààbò àti ìwé-àṣẹ ìlò

Wo [SECURITY.md](../../../SECURITY.md) fún ìjábọ̀ àdáni àti àwọn ẹ̀dà tí a ṣe àtìlẹ́yìn fún.
A fún hostcensus ní ìwé-àṣẹ lábẹ́ [Ìwé-àṣẹ MIT](../../../LICENSE).

Àwọn àkọlé orísun ń lo àwọn ìdánimọ̀ SPDX wọ́n sì ń pa iyì àwọn olùkópa mọ́ láti inú ìtàn
Git. Wo [AUTHORS.md](../../../AUTHORS.md) fún ìtọ́kasí olùkópa. Àwọn ìgbàwọlé ìdánwò oní-méjì àti
fáìlì ìtìpa tí a ṣẹ̀dá ń lo àwọn fáìlì `.license` tí ó sún mọ́ wọn; ọ̀rọ̀ MIT wà nínú `LICENSES/MIT.txt`.
