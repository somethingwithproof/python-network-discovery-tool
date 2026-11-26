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
[![Python compatibility](https://img.shields.io/badge/Python-3.12%E2%80%933.14-blue)](../../../.github/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/python-network-discovery-tool/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/15324/badge)](https://www.bestpractices.dev/en/projects/15324)
[![Strict typing](https://img.shields.io/badge/mypy-strict-blue)](../../../pyproject.toml)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · **Igbo** · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus bụ ngwaọrụ Python CLI maka ndepụta ọrụ a pụrụ imeghachi ugboro ugboro na netwọk ndị ị na-achịkwa.
Ọ na-edekọ ihe ngwaọrụ dị iche iche na-ekpughe, tụnyere nchọpụta n'oge dị iche iche, ma mepụta
skripti mbubata Kadupul. Nkwado azụ ndabere na-eji soketi asyncio n'enweghị ikike root;
nchọpụta Nmap nke nhọrọ nwere ike ịchọpụta ngwaọrụ ndị karịrị pọtụ ọrụ a haziri.

## Ihe kpatara hostcensus

Akụkọ pọtụ e mere naanị otu ugboro anaghị akọwa ma nchọpụta na-esote ọ gbanwere ma ọ bụ
na o nwere ọdịda nkịtị. hostcensus na-ejikọta ọnọdụ ọrụ doro anya, nnyocha nwere oke, profaịlụ
nnyocha a pụrụ iji mee ihe ọzọ, na akụkọ ihe mere eme dị na kọmputa gị. Ndị ọrụ nwere ike imeghachi otu oke ahụ, nyochaa
mmejọ, ma mata ọdịiche dị n'etiti nchọpụta na-edochaghị anya na mgbanwe ndị e kwadoro.

- **Ihe akaebe ọrụ:** njirimara SSH, ekele mbido MySQL, isiokwu HTTP, nchọpụta asambodo
  TLS, na nchọpụta SNMP ma ọ bụ ajụjụ system-MIB nke nwere nzere.
- **Oke a pụrụ imeghachi:** profaịlụ TOML nwere aha, mwepụ a na-agbakwunye, ọrụ a pụrụ
  ịhazi, oke ngwaọrụ/nnyocha, na ndị ọrụ azụ nwere oke.
- **Nlele tupu okporo ụzọ netwọk:** nlele mbido mpaghara na-akwado ebe a na-achọ, ngwaọrụ, ohere
  ebe ntinye, schema akụkọ ihe mere eme, na ngwugwu TLS CA a haziri.
- **Akụkọ ihe mere eme nke ndepụta:** foto SQLite nwere njikwa azụmahịa na-echekwa nchọpụta niile;
  ntụnyere na-eme ka ọdịda nnyocha na ọnọdụ a na-amaghị doo anya.
- **Mpụta na-arụkọ ọrụ ọnụ:** akụkọ terminal, JSON na CSV, foto faịlụ nwere ụdị,
  na skripti mbubata Kadupul.

CI na-ekpuchi Python 3.12, 3.13 na 3.14 na Linux na macOS, gbakwunyere ụlọ nyocha njikọta
Compose a na-achịkwa. Koodu ahụ na-eji aha ụdị ọgbara ọhụrụ, nsonaazụ nlele mbido nwere ụdị,
profaịlụ nwere oghere nke naanị mkpụrụokwu igodo na nhicha async a haziri ahazi ka ọ na-edobe
ụdị oge ọrụ ndị ahụ. Hụ [Ntụnye ụdị na ntọhapụ](../../../docs/releasing.md) maka nkwekọrịta ndakọrịta
SemVer na usoro ntọhapụ GitHub. Akara ntọhapụ na-akọwa
ihe ndị e bipụtara, ọ bụghị checkout a: mkpado kachasị ọhụrụ e bipụtara ugbu a bụ
`v0.3.0`, ebe checkout a na-eji ụdị ngwugwu `3.0.0`. Wụnye site na checkout a
ka i wee jiri atụmatụ ndepụta a kọwara ebe a.

Malite na [nwụnye](#install), mesịa [profaịlụ na akụkọ ihe mere eme](#inventory-profiles-preflight-and-local-history).
Maka nkọwa njikọta, hụ [akara mkpịsị aka ọrụ](#fingerprints),
[ntụnyere faịlụ](#inventory-diff), na [mbupụ Kadupul](#kadupul-export).

<a name="install"></a>

## Nwụnye

A chọrọ Python 3.12 ma ọ bụ nke ọhụrụ; Python 3.12–3.14 bụ ndepụta a nwalere. Site na
checkout a, wụnye ndabere oge ọrụ a kpọchiri akpọchi:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Maka nchọpụta ngwaọrụ Nmap nke nhọrọ, wụnye mmemme Nmap site n'iji njikwa ngwugwu
nke usoro gị; ọ dịghị ngwugwu Python ọzọ dị mkpa. A na-enyocha mpụta XML nke Nmap site na
defusedxml, nke bụ ndabere isi, ya mere a na-ajụ mgbasawanye ihe. hostcensus na-agba
`nmap` a hụrụ na `PATH` kpọmkwem site na ndepụta arụmụka a kapịrị ọnụ, oge njedebe nke na-eto
dị ka oke prefix si dị, na oke mpụta 64 MiB. A chọghị Nmap maka nkwado azụ ndabere.

## Ịkwaga site na netprobe

hostcensus bụ aha ọhụrụ nke netprobe, nke e wepụtara na 3.0.0. E bipụtaghị ọrụ a
na PyPI n'okpuru aha ọ bụla n'ime abụọ ahụ, ya mere nwụnye si na checkout ma ọ bụ ntọhapụ
GitHub. Ebe nchekwa GitHub ka na-edobe aha ya.

| Nke mbụ | Ugbu a | Ndakọrịta |
| --- | --- | --- |
| Nkesa `netprobe` | `hostcensus` | Wụnye ọzọ site na checkout; ọ dịghị ngwugwu nwere aha ochie. |
| Iwu `netprobe` | `hostcensus` | `netprobe` ka na-agba ma na-ebipụta otu ahịrị nkwụsị na stderr. Koodu ọpụpụ na stdout agbanweghị. A ga-ewepụ ya na ntọhapụ isi na-esote. |
| Mgbanwe gburugburu `NETPROBE_*` | `HOSTCENSUS_*` | A na-eji mgbanwe `NETPROBE_*` mgbe a na-atọghị ejima ya `HOSTCENSUS_*`, nwere otu ịdọ aka na ntị stderr nke na-akpọ aha mgbanwe ndị ahụ mana ọ dịghị mgbe ọ na-akpọ ọnụahịa ha. `HOSTCENSUS_*` na-emeri mgbe a tọrọ ha abụọ. A ga-ewepụ ya na ntọhapụ isi na-esote. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Mgbanwe na-emebi ndakọrịta.** Enweghị shim mbubata a wụnyere; melite mbubata gị. |
| Mkpado onyonyo Docker `network-discovery:test` (naanị CI) na onye ọrụ container `netprobe` | `hostcensus:test`, onye ọrụ `hostcensus` | E bipụtaghị onyonyo registry ọ bụla. Wulite onyonyo ahụ ọzọ ma jiri ebe ntinye `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | A ka na-eji faịlụ dị adị nwere aha ndabere ochie, nwere ịdọ aka na ntị, ma ọ bụrụ na aha ọhụrụ ahụ adịghị. Ụzọ `--config` na `--history` a kpọrọ aha kpọmkwem anaghị emetụta. |
| Akụkọ na foto nwere `"format": "netprobe-report"` ma ọ bụ `"netprobe-snapshot"`, na ubi `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` na `export` ka na-ebu faịlụ e dere n'okpuru aha ochie, ma JSON Schema ndị e bipụtara na-anabata mkpụrụokwu abụọ ahụ. Faịlụ ọhụrụ na-eji aha ọhụrụ. Nchekwa data akụkọ ihe mere eme SQLite agbanweghị ma na-ebu dị ka ọ dị na mbụ. |
| Skripti Kadupul sitere na `netprobe export` | Skripti sitere na `hostcensus export` | Skripti ochie ka na-arụ ọrụ ma ka na-agụ `NETPROBE_SNMP_*` mgbe ha na-agba. Skripti ọhụrụ na-agụ `HOSTCENSUS_SNMP_*`. |

## Ihe atụ ngwa ngwa

Gbaa site na container nnwale nke ụlọ nyocha njikọta a kọwara n'okpuru Mmepe; e belatara mpụta ya:

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

## Koodu ọpụpụ

| Iwu | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | e dekọrọ nchọpụta/akụkọ | nlele mbido/nkwado azụ, akụkọ ihe mere eme, ma ọ bụ ide akụkọ/foto dara | ebe a na-achọ, nhọrọ, ntọala, ma ọ bụ oke adịghị mma | - | e ruru `--deadline`; e dere akụkọ na-ezughị ezu, a mafere akụkọ ihe mere eme na foto |
| `preflight` | nlele gafere | nlele mpaghara dara | ebe a na-achọ/ntọala adịghị mma ma ọ bụ ebe ntinye na-emegiderịta onwe ha | - | - |
| `profiles` | e depụtara profaịlụ ndị a kwadoro | - | ntọala ma ọ bụ nhọrọ a na-apụghị ịgụ/adịghị mma | - | - |
| `history` | e depụtara nchịkọta | akụkọ ihe mere eme na-efu, adịghị mma, ma ọ bụ a na-akwadoghị | nhọrọ CLI adịghị mma | - | - |
| `compare` | e mepụtara ntụnyere, gụnyere mgbe mgbanwe dị | akụkọ ihe mere eme a na-apụghị ịgụ, oke/usoro na-adabaghị, ma ọ bụ ọdịda ide | nhọrọ CLI adịghị mma | - | - |
| `diff` | enweghị mgbanwe | a pụghị ide faịlụ `-o` | ntinye na-efu, a na-apụghị ịgụ ma ọ bụ a na-akwadoghị, ma ọ bụ nnyocha na-ezughị ezu n'enweghị `--allow-partial` | a hụrụ mgbanwe, nchọpụta a na-akwadoghị, ma ọ bụ nnyocha na-ezughị ezu | - |
| `export` | e dere skripti | a pụghị ide skripti | ntinye a na-apụghị ịgụ, nnyocha na-ezughị ezu n'enweghị `--allow-partial`, ma ọ bụ data a na-apụghị ibupụ n'enweghị nsogbu | - | - |

## Nhazi koodu

| Modul | Ọrụ ya |
| --- | --- |
| `cli.py` | Nhọrọ iwu, mkpebi profaịlụ, nlele mbido, nnyocha na ide akụkọ |
| `scanner.py`, `probes.py` | Mgbasawanye ebe a na-achọ, ndị ọrụ azụ nwere oke, nchọpụta ngwaọrụ na nchọpụta ọrụ |
| `config.py`, `profiles.py` | Nkọwa ọrụ na profaịlụ ndepụta a kwadoro |
| `models.py`, `output.py` | Ụdị nsonaazụ na ngosipụta terminal/JSON/CSV |
| `history.py`, `diff.py` | Akụkọ ihe mere eme SQLite na ntụnyere foto faịlụ nwere ụdị |
| `preflight.py` | Nlele mpaghara na nchọta ụdị Nmap nwere oke |
| `export.py` | Skripti mbubata Kadupul a kwadoro ma tinye n'akara ngụ |

Nchọpụta ọrụ ọ bụla na-edekọ ọnọdụ ya iche na njirimara ọ na-akpọsa.
Ọgụgụ na oge njedebe nwere oke; mmejọ pụrụ iche nke nnyocha na-anọgide na mmejọ ngwaọrụ. Akụkọ
ihe mere eme SQLite na-eji azụmahịa, nhicha njikọ doro anya, na ụzọ ndepụta na ntụnyere
nke naanị ọgụgụ. Nzuzo SNMP na-abata naanị site na mgbanwe gburugburu ma ọ bụ faịlụ
nzuzo; akụkọ ihe mere eme nke ndepụta na-echekwa ntọala ndị na-abụghị nzuzo dị irè. Hụ
[Nhazi usoro](../../../docs/architecture.md) maka usoro nnyocha, oke ya na oke ntụkwasị obi
ya, na [SECURITY.md](../../../SECURITY.md#authorized-use) maka ojiji e nyere ikike.


## Ojiji

Nyochaa naanị netwọk ndị ị na-achịkwa.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Nhọrọ | Pụtara ya |
| --- | --- |
| `NETWORK` | CIDR, IP, ma ọ bụ aha nnabata; ọ bụ nhọrọ mgbe e jiri `--profile`. A na-ajụ njirimara oke IPv6. |
| `-o, --output PATH` | Dee akụkọ. Ụdị ya na-agbaso ndọtị faịlụ (`.json`, `.csv`); ndọtị ndị ọzọ na-alaghachi na JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Manye ụdị akụkọ. O nweghị mmetụta ma a na-ejighị `--output`. `.sh` na-ahọrọ `kadupul`. |
| `-v, --verbose` | Ndekọ nchọpụta nsogbu. |
| `-q, --quiet` | Zobe nsonaazụ, ọganihu na ndekọ ozi; ịdọ aka na ntị na mmejọ ka na-apụta na stderr. |
| `--backend asyncio\|nmap` | Nchọpụta ngwaọrụ. `asyncio` (ndabere) na-enyocha pọtụ ọrụ kpọmkwem; `nmap` na-ebu ụzọ gbaa nnyocha ping nmap ma chọọ mmemme `nmap` na `PATH`. |
| `--timeout SECONDS` | Oge echere maka nnyocha ndị na-atọghị oge nke ha (ndabere 1.0). Nnyocha njikọ e wunyere na-eji 0.3s belụsọ ma tebụl ọrụ tọrọ `timeout`. |
| `--concurrency N` | Nnyocha ndị na-agba n'otu oge (ndabere 256). |
| `--deadline SECONDS` | Kwụsị nnyocha niile, gụnyere nnyocha nmap, mgbe oge a gachara (ndabere 3600, kachasị 604800; gburugburu `HOSTCENSUS_DEADLINE`). A na-ede ngwaọrụ ndị gụchara n'akụkọ ahụ nwere `"complete": false`, anaghị ede akụkọ ihe mere eme ma ọ bụ foto, ma `scan` na-apụ na koodu 4. |
| `--config PATH` | Nkọwa ọrụ TOML na ntọala `[profiles]` nwere aha nke nhọrọ. |
| `--profile NAME` | Jiri profaịlụ nwere aha; na-alaghachi na `hostcensus.toml` mgbe e wepụrụ `--config`. |
| `--exclude IP/CIDR` | Gbakwunye mwepụ; meghachi dị ka ọ dị mkpa. Ngwaọrụ IPv4 e wepụrụ na-ewepụkwa adreesị IPv6 ndị na-eru ya: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) na 6to4. A na-emeso ebe a na-achọ na mwepụ IPv4-mapped dị ka adreesị IPv4 ha na-anọchite anya. |
| `--max-hosts N` | Oke adreesị a na-elele tupu mwepụ (ndabere/oke siri ike 65,536). |
| `--history PATH` | Dekọọ nnyocha zuru ezu n'ime nchekwa data akụkọ ihe mere eme SQLite nke nhọrọ. |
| `--services NAMES` | Ndepụta aha ọrụ e kewara na kọma a ga-elele, n'usoro ahụ (ndabere: niile). |
| `--ports SPEC` | Ndepụta e kewara na kọma nke `NAME=PORT` (kwagharịa ọrụ) ma ọ bụ `PORT` (gbakwunye nlele TCP nkịtị a kpọrọ `tcp-PORT`). |
| `--snmp-community-file PATH` | Faịlụ ji obodo SNMPv2c maka ajụjụ system MIB. Gburugburu: `HOSTCENSUS_SNMP_COMMUNITY` (ọnụahịa ya) ma ọ bụ `HOSTCENSUS_SNMP_COMMUNITY_FILE` (ụzọ ya). |
| `--snmp-user` | Onye ọrụ SNMPv3. Gburugburu: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (ndabere), `SHA224`, `SHA256`, `SHA384`, `SHA512` na faịlụ ji okwuntughe. Gburugburu: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ma ọ bụ `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (ndabere), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` na faịlụ ji okwuntughe. Gburugburu: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ma ọ bụ `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Deekwa foto nwere ụdị maka `hostcensus diff`. |
| `--tls-ca-file PATH` | Kwenye asambodo HTTPS megide ngwugwu PEM a kama ụlọ ahịa usoro. Gburugburu: `HOSTCENSUS_TLS_CA_FILE`. |

Site na ndabere, a na-elele ngwaọrụ ọ bụla maka SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) na HTTPS (TCP 443). A na-anwale pọtụ TCP site na njikọ zuru oke. A na-anwale SNMP site na arịrịọ nchọpụta injin SNMPv3, nke onye ọrụ SNMPv3 ọ bụla ga-aza n'enweghị nzere; nnyocha a agaghị achọpụta ndị ọrụ na-asụ naanị v1/v2c. Site na nkwado azụ asyncio, a na-agụ ngwaọrụ dị ka nke dị ndụ mgbe nnyocha ọ bụla nwetara azịza, gụnyere njikọ a jụrụ ajụ, ya mere ngwaọrụ na-atụfu nnyocha ọ bụla nwere `alive=false` na mmejọ "Host is down"; nke a egosighị na ọ gbanyụrụ n'ezie. Site na `--backend nmap`, nmap na-ekpebi ngwaọrụ ndị dị ndụ (ICMP dị ka root, TCP 80/443 ma ọ bụghị ya).

<a name="fingerprints"></a>

### Akara mkpịsị aka ọrụ

A na-ewepụta akara mkpịsị aka nke ọrụ ọ bụla mepere emepe site n'ihe o zigara tupu nbanye ọ bụla. Ọ dịghị ihe na-akwado njirimara belụsọ ajụjụ SNMP, ma ọ bụ naanị mgbe i nyere nzere.

| Nnyocha | Ihe ọ na-agụ | `version` | Igodo `details` |
| --- | --- | --- | --- |
| `ssh` | ahịrị njirimara RFC 4253 | ngwanrọ, dị ka `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | nkwụrịta mbụ MySQL/MariaDB | ụdị ihe nkesa | `server_version`, `flavor`, `auth_plugin`, ma ọ bụ `error_code`/`error` |
| `http` | azịza `HEAD /` | isiokwu `Server` | `status`, `server` |
| `https` | nkwụrịta TLS, asambodo, `HEAD /` | isiokwu `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | nchọpụta SNMPv3; nwere nzere, GET nke sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; nwere nzere `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ma ọ bụ `snmp_error` |

A na-edozi ebe a na-achọ bụ aha nnabata otu ugboro maka ngwaọrụ ọ bụla ma nnyocha ọ bụla na-ejikọ na adreesị ahụ, nke e dekọrọ dị ka `address` na nsonaazụ; a na-eji aha ahụ naanị maka TLS SNI, nkwenye asambodo na isiokwu HTTP `Host`. Aha na-adịghị edozi na-enye ọnọdụ `unknown` na mmejọ `Cannot resolve`. A na-edobe aha reverse DNS naanị mgbe ha nwere mkpụrụedemede aha nnabata, ma kachasị nchọta 16 na-agba n'otu oge. HTTPS na-eji nkwenye asambodo na aha nnabata megide ụlọ ahịa usoro ma ọ bụ `--tls-ca-file`. A na-ebu ụlọ ahịa ntụkwasị obi otu ugboro maka nnyocha ahụ ma jiri ya mee ihe ọzọ maka nnyocha HTTPS ọ bụla. A na-atụ oge njikọ TCP na nkwụrịta TLS iche iche, ya mere pọtụ na-anabata njikọ mana na-akwụsị nkwụrịta bụ `open` nwere `tls_error`, ọ bụghị `filtered`. Ọ bụrụ na nkwenye daa, nsonaazụ ahụ na-edekọ `cert_verified: false` na `cert_verify_error`; ọ naghị anwale ọzọ site na ntọala adịghị ike ma ọ bụ ziga arịrịọ HTTP. A na-achịkọta nkọwa asambodo na isiokwu HTTP naanị mgbe nkwenye gara nke ọma. Nye ngwugwu CA ziri ezi maka ọrụ CA nkeonwe. Akụkọ ochie nwere ike ịnwe `cert_read_unverified`, nke nnyocha dị ugbu a anaghịzi emepụta.

A na-agụ nzuzo SNMP naanị site na mgbanwe gburugburu ma ọ bụ site na faịlụ (`--snmp-*-file`, ma ọ bụ mgbanwe `HOSTCENSUS_SNMP_*_FILE` kwekọrọ), ọ dịghị mgbe ọ bụla site na ọnụahịa ahịrị iwu, nke ndị ọrụ mpaghara ndị ọzọ nwere ike ịhụ na ndepụta usoro. `--snmp-community`, `--snmp-auth-key` na `--snmp-priv-key` nwere ọnụahịa na-apụ na koodu 2 ma kpọọ aha ihe nnọchi. Faịlụ nzuzo ga-abụ UTF-8 na-abụghị efu nke kachasị baịtị 4096; a na-eleghara otu ahịrị ọhụrụ dị n'azụ anya, ma ịtọ ma mgbanwe ma faịlụ maka otu nzuzo ahụ bụ mmejọ. Mmejọ na-akpọ aha faịlụ ahụ mana ọ dịghị mgbe ọ na-ebipụta ọdịnaya ya. Akụkọ nnyocha na akụkọ ihe mere eme anaghị etinye ọnụahịa nzere n'ebumnuche. Onye mbupụ nwere nhọrọ `--include-credentials` dị iche ma doo anya nke a kọwara n'okpuru. Obodo na-ahọrọ SNMPv2c; onye ọrụ na-ahọrọ SNMPv3, nwere nkwenye njirimara mgbe e nyere igodo nkwenye na nzuzo mgbe e nyere igodo abụọ ahụ (`snmp_security_level` na-edekọ nke ọ bụ). hostcensus na-ajụ, site na koodu ọpụpụ 2, ijikọta obodo na onye ọrụ v3, iji igodo nzuzo n'enweghị igodo nkwenye, ma ọ bụ iji igodo n'enweghị onye ọrụ, ma ọ dịghị mgbe ọ na-anwale ajụjụ v3 dara ada ọzọ site na v2c ma ọ bụ ọkwa nchekwa dị ala. Ndị ọrụ na-asụ naanị v1/v2c na-eleghara nchọpụta v3 na-enweghị nzere anya, ya mere ha na-apụta dị ka ndị mepere emepe naanị mgbe e nyere obodo.

A na-ebelata ederede banner ka ọ bụrụ naanị mkpụrụedemede a pụrụ ibipụta ma kpọchie ya na mkpụrụedemede 256 tupu e chekwaa ya ma ọ bụ gosi ya. Ọgụgụ nwekwara oke: 4 KiB n'ahịrị ọ bụla, 4 KiB maka ekele mbido MySQL, 16 KiB nke isiokwu HTTP. A na-ebipụ ID injin SNMP karịrị okteti 32 tupu e chekwaa ya. HTTP na HTTPS na-eziga isiokwu Host nwere adreesị IPv6 n'ime mkpuchi akụkụ anọ yana pọtụ mgbe ọ bụghị 80 ma ọ bụ 443. A na-etinye mbido n'ọkpụrụkpụ CSV ndị na-amalite site na ihe na-akpalite usoro mgbakọ spreadsheet ka ọkpụrụkpụ ahụ wee nọgide dị ka ederede.

### Oke

Otu ọsọ na-anabata kachasị adreesị 65,536, ọrụ 64, na nnyocha 524,288 (ngwaọrụ mụbara site n'ọrụ); arịrịọ buru ibu karịa nke a na-apụ na koodu 2 tupu e ziga ihe ọ bụla. A kpọchiri `--concurrency` na soketi 4096. Nnyocha ọ bụla nwere oge njedebe siri ike nke okpukpu anọ nke oge nke ya. Nnyocha njikọ (`tcp`, `ssh`, `mysql`, `http`) na-eji sekọnd 0.3 belụsọ ma ọrụ ahụ tọrọ `timeout`. SNMP na HTTPS na-eji `--timeout` (ndabere 1.0) mgbe ha na-atọghị otu. A na-akọ nnyocha ruru oge njedebe dị ka `unknown` nwere "probe timed out" na `errors`. Ọdịda soketi mpaghara (dị ka agwụla nke nkọwa faịlụ) bụkwa `unknown` ma e dekọọ mmejọ ahụ; ha anaghị agụ dị ka pọtụ e jiri nzacha ma ọ bụ ngwaọrụ gbanyụrụ. Tupu ịnyocha, hostcensus na-ebuli oke dị nro nke faịlụ mepere emepe gaa n'oke siri ike iji dabaa na `--concurrency` gbakwunyere nkọwa 64; mgbe ọ na-apụghị, nlele mbido `open files` na-ada ma `scan` na-apụ na 1 tupu iziga okporo ụzọ netwọk. Nchọpụta Nmap na-eji oge ngwaọrụ sekọnd 30. A na-enyefe nmap prefix n'ụdị CIDR, ma nnyocha na-ada na ọpụpụ 1 mgbe nmap kọrọ adreesị dị nta karịa ndị e nyere ya (dị ka aha ọ na-apụghị idozi) kama ịkọ ngwaọrụ dị ka ndị gbanyụrụ. A na-edozi ebe a na-achọ bụ aha nnabata otu ugboro ma nye nmap adreesị ahụ, ka nchọpụta na nnyocha wee ruo otu igwe ahụ. Prefix zuru ezu bụ otu usoro nmap nke oge njedebe usoro okpuru ya bụ sekọnd 35 maka adreesị 256 ọ bụla, e buliri elu. Nnyocha nwere mwepụ na-eji nkebi ngwaọrụ 256 na oge njedebe sekọnd 35 maka nkebi ọ bụla. Imepụta ndị ọrụ azụ nwere oke n'adabereghị na oke ogologo. Reverse DNS na ndozi aha nnabata nwere oge njedebe sekọnd abụọ dị iche; a na-ahapụ oku ndozi na-adịghị alọghachi na eri nke ya, ka ọ ghara idobe hostcensus ka ọ na-agba gafee oke ndị a. Kachasị nchọta 16 na-agba n'otu oge, ma oku a hapụrụ na-ejide oghere ya ruo mgbe ọ lọghachiri, ya mere ọnụọgụ eri kpọchiri akpọchi na-anọgide n'oke; ọ bụrụ na 16 niile kwụsịrị, nchọta ndị ga-abịa mgbe e mesịrị na-echere n'ahịrị maka oghere na mpụga oge njedebe sekọnd abụọ ahụ (nke na-amalite ozugbo oghere tọgbọrọ chakoo) ruo mgbe `--deadline` kwụsịrị nnyocha ahụ. `NetworkScanner` e jiri dị ka ọba akwụkwọ n'enweghị `deadline` nwere ike ichere oghere dị otú ahụ ruo mgbe ebighị ebi. `--deadline` (ndabere otu awa) na-ejide ọsọ niile n'elu ndị a.

### Ịhazi ọrụ

Enwere ike ịgbanwe ọrụ site na faịlụ TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` bụ otu n'ime `tcp`, `ssh`, `mysql`, `http`, `https` ma ọ bụ `snmp` ma na-alaghachi na aha ọrụ ahụ mgbe ọ bụ nnyocha, ma ọ bụghị ya `tcp`. Naanị `snmp` na-eji UDP. Aha ọrụ bụ obere mkpụrụedemede, ọnụọgụgụ, `-` na `_`. Ọrụ abụọ apụghị ikerịta otu pọtụ na protocol; akụkọ ihe mere eme na-edekọ otu ọnọdụ maka ụzọ abụọ ahụ. `timeout` bụ nhọrọ, na sekọnd, ma opekampe 0.05. Nnyocha ụdị njikọ (`tcp`, `ssh`, `mysql`, `http`) na-eji sekọnd 0.3 dị ka ndabere. `snmp` na `https` na-eji `--timeout` nke nnyocha mgbe ọrụ ahụ na-atọghị `timeout`. `--timeout` anaghị anọchi oge ọrụ ahụ nweburu.

Akụkọ JSON bụ akwụkwọ nwere ụdị (`"format": "hostcensus-report"`, `"version": 1`) nke na-edekọ ebe a na-achọ, ọrụ a nyochara na ntọala n'akụkụ `devices`; `--format json` n'enweghị `-o` na-ede akụkọ ahụ na stdout kama tebụl. Mpụta JSON ọ bụla nwere schema e bipụtara; hụ [Mpụta JSON](../../../docs/json-output.md). Ngwaọrụ na-edobe ubi mbụ `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` na `errors` ma tinye ndepụta `services` nwere `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, ma ọ bụ `unknown` mgbe nnyocha dara na mpaghara ma ọ bụ ruo oge njedebe ya), `version` na `details` nke nnyocha ọ bụla. Mpụta CSV na-enweta kọlụm `services` na `versions` n'azụ maka ndị mepere emepe. Boolean `ssh`, `snmp` na `mysql` na-agbaso ọrụ nwere kpọmkwem aha ndị ahụ.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Profaịlụ ndepụta, nlele mbido, na akụkọ ihe mere eme mpaghara

Profaịlụ nwere aha na-ekerịta faịlụ TOML yana nkọwa `[services]` dị adị. Detuo
[hostcensus.example.toml](../../../hostcensus.example.toml) gaa na `hostcensus.toml` ma tọọ netwọk
ndị ị na-achịkwa:

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

`preflight` na-edozi nhọrọ na profaịlụ kpọmkwem dị ka `scan` si eme, gụnyere
`--concurrency` maka nlele faịlụ mepere emepe, ya mere nlele mbido gafere pụtara na `scan` ga-amalite
site n'otu atụmatụ ahụ.

Profaịlụ na-anabata `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, na `max_hosts`. `services` na `ports` na-eji usoro ndepụta e kewara na kọma
dị adị. Nhọrọ CLI doro anya na-anọchi ntọala profaịlụ; nhọrọ `--exclude` a meghachiri
na-agbakwunye na mwepụ profaịlụ. Netwọk a kpọrọ aha kpọmkwem yana `--profile` ga-adị
n'ime oke IP/CIDR nke profaịlụ ahụ. A ka na-akwado aha nnabata maka nnyocha
kpọmkwem, mana a pụghị ijikọta ha na mwepụ IP. Oke ngwaọrụ na-arụ ọrụ tupu
mwepụ; oke nnyocha niile ka na-arụ ọrụ mgbe e mesịrị. A na-ewepụ ngwaọrụ e wepụrụ
na ma nlele ọrụ ma nchọpụta Nmap nke nhọrọ.

Nnyocha ọ bụla na-eme nlele mbido mpaghara tupu okporo ụzọ netwọk ebe a na-achọ: oke
ebe a na-achọ/nnyocha, ohere ebe ntinye, nnweta mmemme/mkpuchi Nmap nke nhọrọ, schema akụkọ
ihe mere eme, na ngwugwu TLS CA a haziri. `preflight` na-akọ JSON ma ọ naghị enyocha
ebe a na-achọ ma ọ bụ mepụta nchekwa data akụkọ ihe mere eme. Ọ na-ede faịlụ nwanne nwa oge iji nwalee
ohere ebe ntinye n'agbanweghị ọdịnaya dị adị. Nkwado azụ asyncio ndabere
ka na-achọghị Nmap ma ọ bụ root. Ụzọ ebe ntinye ga-adị iche na ibe ha
na ntọala ntinye, gụnyere njikọ siri ike; a na-ajụ symlink ebe ntinye.
Nlele dara ada na-eweghachi 1; oke/ntọala adịghị mma na-eweghachi 2.

Ide akụkọ na mbupụ chọrọ nkwado `O_NOFOLLOW`. Na usoro ndị na-enweghị ya,
gụnyere Windows, ide ndị a na-ada n'emegheghị ma ọ bụ n'ebelataghị ebe ntinye ahụ.
Akụkọ ọhụrụ na skripti mbupụ bụ naanị onye nwe ya (ọnọdụ 0600); iji nke ọhụrụ dochie faịlụ dị adị na-edobe
ikike ya. Ide na paịpụ nwere aha na-enweghị onye na-agụ na-ada ozugbo kama ichere. A na-emepụtakwa nchekwa data `--history` ọhụrụ dị ka naanị onye nwe ya; nke dị adị na-edobe ọnọdụ ya. Ozi ndekọ na-aga na stderr mgbe niile, ya mere stdout na-ebu naanị nsonaazụ. Mbupụ nwere nzere na-amanye ọnọdụ 0600 mgbe niile.

Akụkọ ihe mere eme bụ nhọrọ ma na-emeju foto JSON dị adị na iwu `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Jiri ID sitere na `history`; ihe atụ ahụ na-eche na ọ bụ nchekwa data ọhụrụ. A na-echekwa foto
site n'azụmahịa nwere oge mmalite/ngwụcha UTC, ụdị ngwugwu, ntọala ndị na-abụghị nzuzo dị irè,
nchịkọta, na nchọpụta ngwaọrụ/ọrụ niile, gụnyere mmejọ nke ngwaọrụ ọ bụla.
A na-edobe nchọpụta ngwaọrụ na-ezughị ezu. A naghị echekwa ọsọ a kagburu. A na-echekwa
nkwekọrịta akụkọ, foto, mbupụ, na koodu ọpụpụ nnyocha dị adị.

`history` na-edepụta nchịkọta JSON n'agụghị data ngwaọrụ akụkọ ihe mere eme niile.
`compare` na-agụ nnyocha abụọ e chekwara, chọọ njirimara ebe a na-achọ na pọtụ a họọrọ
yiri ibe ha, ma kọọ mgbanwe nzaghachi, ọnọdụ, na ọnọdụ pọtụ. ID nnyocha mbụ
ga-ebu ụzọ tupu ID nke mgbe e mesịrị. Mgbe nnyocha abụọ ahụ dekọrọ `timeout` ma ọ bụ `backend`
ma ọnụahịa ndị ahụ dị iche, akụkọ ahụ na-edepụta ịdọ aka na ntị ma ka na-atụnyere
nchọpụta ndị ahụ. Oge echere dị iche nwere ike ime ka pọtụ e jiri nzacha dị ka nke mepere emepe. A na-akara mmejọ nnyocha
na nchọpụta pọtụ a na-amaghị dị ka nke na-edochaghị anya kama imeso ha dị ka
mfu ma ọ bụ mmechi a kwadoro: ngwaọrụ nwere mmejọ na-apụta na `uncertain_hosts`, ma
mgbanwe pọtụ ọ bụla gụnyere `unknown` (gụnyere unknown na nnyocha abụọ ahụ) na-apụta
na `unconfirmed_ports` kama `port_changes`, belụsọ pọtụ mepere emepe na nnyocha
nke mgbe e mesịrị, nke bụ mgbanwe pọtụ. `compare` na `diff` na-ekewa pọtụ site n'otu iwu ahụ.
`no_longer_responding` pụtara enweghị nzaghachi, ọ bụghị ihe akaebe na e wepụrụ ngwaọrụ ahụ.
Koodu ọpụpụ nnyocha 0 ekweghị nkwa na ngwaọrụ ọ bụla zara: lelee mmejọ nke ngwaọrụ ọ bụla. Ọganihu ntụnyere na-eweghachi 0 ma mgbanwe dị ma ọ dịghị; `diff` faịlụ dị adị
na-edobe nkwekọrịta koodu ọpụpụ 3 ya. Akụkọ ihe mere eme a na-akwadoghị ma ọ bụ nke mebiri emebi na-eweghachi 1.

Akụkọ ihe mere eme na-echekwa ozi ndepụta, ya mere họrọ folda mpaghara e chekwara
nke ọma. Faịlụ profaịlụ na ntọala e chekwara enweghị nzuzo SNMP;
njikwa nzere na-aga n'ihu site na nhọrọ oge ọrụ/gburugburu dị adị.

<a name="inventory-diff"></a>

## Ntụnyere ndepụta (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Foto bụ JSON nwere `format: "hostcensus-snapshot"`, `version: 1`, ụdị hostcensus, oge mmepụta UTC, ebe a na-achọ, `timeout` na `backend` nke nnyocha mgbe nnyocha ahụ dekọrọ ha, ọrụ a nyochara, na ngwaọrụ ndị dị ndụ n'otu ọdịdị dị ka akụkọ `-o`. A na-ahapụ ngwaọrụ ndị gbanyụrụ. `diff` na-anabatakwa akụkọ JSON `scan -o` nkịtị, gụnyere ndị sitere tupu ubi `services` adịrị.

`diff` na-akọ ngwaọrụ ọhụrụ na ndị furu efu, pọtụ mepere ma ọ bụ mechie na ngwaọrụ dị n'abụọ ahụ, na ọrụ ndị `version` ha gbanwere. A naghị atụnyere pọtụ a nyochara naanị n'otu n'ime nnyocha abụọ ahụ, ma ịdọ aka na ntị na-ekwu otu ahụ. Nchọpụta dara ada anaghị apụta dị ka "enweghị mgbanwe": pọtụ bụ `unknown` na nnyocha ọ bụla n'ime abụọ ahụ ma na-emegheghị na nke mgbe e mesịrị ka a na-edepụta n'okpuru `unconfirmed`, ọ bụghị `closed`, nwere `before` nke `open`, `unknown` ma ọ bụ `not-open` (a nyochara ma mechie ma ọ bụ tinye nzacha) na `after` nke `unknown` ma ọ bụ `not-open`; a na-akọ pọtụ mepere emepe ugbu a n'okpuru `opened` ọbụna ma ọ bụrụ na nnyocha mbụ dara. A na-edepụta ngwaọrụ nke nnyocha ya niile dara n'enweghị azịza na nnyocha ọ bụla n'ime abụọ ahụ n'okpuru `unsettled_hosts` (nwere `before`/`after` nke `up`, `uncertain` ma ọ bụ `absent`, gụnyere mgbe ọ dara na nnyocha abụọ ahụ ma ọ bụ na-efu na faịlụ nke ọzọ) kama `vanished_hosts`; ọ bụrụ na o zaa na nnyocha mgbe e mesịrị, a na-akọkwa ya dị ka ngwaọrụ ọhụrụ nwere pọtụ ya mepere emepe. Foto na-edobe ngwaọrụ ndị ahụ dara ada n'ihi nke a. Ịdọ aka na ntị na-apụtakwa mgbe ebe a na-achọ dị iche, yana mgbe faịlụ abụọ ahụ dekọrọ timeout ma ọ bụ backend ma ọnụahịa ndị ahụ dị iche. `-o PATH` na-edekwa ụdị JSON gaa na faịlụ.

Akụkọ sitere na nnyocha nke `--deadline` kwụsịrị (`"complete": false`) na-edepụta naanị ngwaọrụ o ruru, ya mere `diff` na `export` na-ajụ ya na koodu ọpụpụ 2. `--allow-partial` na-anabata ya nwere ịdọ aka na ntị na stderr: `diff` na-edepụta ngwaọrụ ndị nnyocha na-ezughị ezu ahụ edepụtaghị ma ọlị n'okpuru `unsettled_hosts` dị ka `unscanned` kama nke furu efu (ngwaọrụ o depụtara dị ka nke gbanyụrụ ka bụ nke furu efu), na-atọ `partial` ka ọ bụrụ eziokwu ma ọ dịghị mgbe ọ na-akọ enweghị mgbanwe, ma `export` na-ede ịdọ aka na ntị n'isiokwu skripti ahụ.

Koodu ọpụpụ `diff`: `0` enweghị mgbanwe, `3` a hụrụ mgbanwe, nchọpụta a na-apụghị ikwenye, ma ọ bụ ntinye na-ezughị ezu (`changed` bụ eziokwu mgbe ọ bụla ndepụta ọ bụla, gụnyere `unsettled_hosts` na `unconfirmed`, na-abụghị efu, ma ọ bụ `partial` bụ eziokwu), `2` faịlụ na-efu, a na-apụghị ịgụ, abụghị foto a kwadoro, ma ọ bụ ezughị ezu n'enweghị `--allow-partial`, `1` a pụghị ide faịlụ `-o`.

<a name="kadupul-export"></a>

## Mbupụ Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (ngalaba nke Cacti 1.2.31) enweghị mbubata faịlụ ngwaọrụ n'ọtụtụ. Ụzọ ya a kwadoro iji gbakwunye ngwaọrụ site na skripti bụ `cli/add_device.php`, otu ngwaọrụ maka oku ọ bụla, nwere arụmụka `--option=value`. `hostcensus export` na-ede skripti POSIX `sh` nke oku ndị ahụ:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Ngwaọrụ ọ bụla dị ndụ na-aghọ `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Ngwaọrụ ebe ajụjụ SNMP nke nnyocha gara nke ọma na-enweta `--version=2 --community=...` ma ọ bụ `--version=3 --username=... --authproto=... --password=...` (gbakwunyere `--privproto`/`--privpass` maka authPriv), `--port` na `--avail=snmp`. Mbupụ SNMPv3 chọrọ `--snmp-user`, ma a na-ajụ noAuthNoPriv n'ihi na `add_device.php` chọrọ okwuntughe v3.
- Ngwaọrụ ndị ọzọ na-enweta `--version=0 --avail=ping`, nwere `--ping_method=tcp --ping_port=` pọtụ TCP mbụ mepere emepe, ma ọ bụ ICMP ma ọ bụrụ na ọ dịghị.
- `--notes` na-edepụta ọrụ mepere emepe na ụdị ha. `--description` bụ aha reverse-DNS mgbe ọ dị mfe (mkpụrụedemede, ọnụọgụgụ, `.`, `_`, `-`), ma ọ bụghị ya IP, ma a na-eme ya ka ọ pụrụ iche, n'ihi na `add_device.php` na-emeso nkọwa dị adị dị ka mmelite na ngwaọrụ ahụ.

A na-akwado ọnụahịa ọ bụla ma tinye ya n'akara ngụ shell site na `shlex.quote`. Site na ndabere, anaghị ede nzuzo SNMP ọ bụla: skripti ahụ na-agbasa `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ma ọ bụ `HOSTCENSUS_SNMP_PRIV_KEY` n'oge ọsọ ma kwụsị ma ọ bụrụ na a tọghị otu. `--include-credentials` na-ede ọnụahịa sitere na mgbanwe gburugburu ndị ahụ n'ime skripti ahụ kama, mepụta ya n'ọnọdụ 0600, ma dekọọ ịdọ aka na ntị. `add_device.php` n'onwe ya na-ebipụta obodo ahụ ma na-anata nzuzo dị ka arụmụka, nke a na-ahụ na ndepụta usoro nke ihe nkesa Kadupul mgbe oku ọ bụla na-agba.

`add_device.php` na-apụ na 1 maka oyiri na mmejọ; skripti ahụ na-aga n'ihu, gụọ ọdịda, ma pụọ na 1 ma ọ bụrụ na e tinyeghị ngwaọrụ ọ bụla. ID template sitere na `php cli/add_device.php --list-host-templates`. Koodu ọpụpụ `export`: `0` e dere ya, `2` ntinye a na-apụghị ịgụ, nnyocha na-ezughị ezu n'enweghị `--allow-partial`, ma ọ bụ data a na-apụghị ibupụ n'enweghị nsogbu, `1` a pụghị ide skripti ahụ.

## Ntụnye ụdị na usoro ntọhapụ

hostcensus na-agbaso [Semantic Versioning](https://semver.org/spec/v2.0.0.html): ndozi
ndakọrịta na-abawanye ụdị patch, atụmatụ/nkwụsị ndakọrịta na-abawanye
ụdị minor, ma mgbanwe na-emebi ndakọrịta na-abawanye ụdị major.
Iwu na nhọrọ, koodu ọpụpụ na JSON schema bụ nkwekọrịta ọha;
omume a kwụsịrị ka na-arụ ọrụ ruo na ntọhapụ major na-esote, belụsọ ma
ndozi nchekwa chọrọ ịgbanwe ya ngwa ngwa (ndekọ mgbanwe na-ekwu ihe kpatara ya).

release-please na-emeghe PR ntọhapụ site na isiokwu Conventional Commit dị na `main`,
na-ebuli `pyproject.toml`, `uv.lock` na `CHANGES.md`. Ijikọta ya na-emepụta
mkpado `vMAJOR.MINOR.PATCH` na ntọhapụ GitHub ndepụta, nke CI na-etinye wheel a nwalere,
nkesa koodu isi iyi na checksums; GitHub na-echekwa nkwenye nwulite maka
faịlụ ndị ahụ site na API nkwenye ya. Onye nlekọta na-enyocha ma bipụta
ndepụta ahụ ozugbo e tinyere faịlụ ndị ahụ. A naghị anọchi ntọhapụ ọ bụla.

Mbipụta ntụkwasị obi PyPI bụ nhọrọ ma chọọ ikike nwe ọrụ, onye mbipụta
a tụkwasịrị obi na gburugburu `pypi`. Ọ na-ebipụta otu ihe ntọhapụ a lelere
n'ewuliteghị ọzọ ma ọ bụ chekwaa token API. Ntọhapụ nwere mkpado n'ebe nchekwa ọha
a na-emepụta nkwenye ihe GitHub; ngalaba nkeonwe chọrọ atụmatụ a kwadoro
na nhọrọ doro anya. Hụ
[ntuziaka ntọhapụ zuru ezu](../../../docs/releasing.md) maka nhazi, iwu ziri ezi na nnwale ọzọ.

## Mmepe

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Ngwaọrụ mmepe dị n'ime otu ndabere [PEP 735](https://peps.python.org/pep-0735/)
n'ime `pyproject.toml` (`dev`, `fuzz`, `build`), ya mere ha anaghị apụta na
metadata ngwugwu e bipụtara. `uv.lock` bụ naanị faịlụ mkpọchi; CI na-awụnye site na
`uv sync --locked` ma daa mgbe faịlụ mkpọchi ahụ mere ochie. Họrọ onye ntụgharị site na
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), ma ọ bụ Python 3.12+ ọ bụla.

CI na-amanye oke mkpuchi ngwugwu nke 90%. Nnwale nkeji gụnyere ihe nkesa loopback
a na-achịkwa na ikpe profaịlụ/akụkọ ihe mere eme/onye nkwado ntọhapụ na-enweghị ịntanetị; ụlọ nyocha Compose na-agba
OpenSSH, MariaDB, nginx na net-snmp na akwa mmiri dịpụrụ adịpụ. Gbaa ya site na
`make test-integration`. Hụ [CONTRIBUTING.md](../../../CONTRIBUTING.md) na
[ngwaọrụ ntọhapụ](../../../scripts/README.md).

Container oge ọrụ na-agba dị ka UID/GID 10001 n'enweghị folda ụlọ, enweghị nbanye
shell na enweghị pip, ma nwee ike ide na `/app/output`. Nye onye ọrụ ahụ ohere ide na
folda mpụta ọ bụla e tinyere. Ọ chọghị ikike pụrụ iche ma na-arụ ọrụ na
usoro faịlụ root nke naanị ọgụgụ, ya mere ọ nwere ike ịgba dị ka:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap na-eji omume nchọpụta TCP ya na-enweghị ikike pụrụ iche na container a. CI na-eme ka
nwulite onyonyo daa n'ihe egwu HIGH ma ọ bụ CRITICAL ọ bụla a pụrụ idozi nke Trivy kọrọ.

## Nlele agbụ ọkọnọ

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
na-agba na main nakwa kwa izu, bipụta akara ya n'ezie, ma bulite nchọpụta na nnyocha
koodu GitHub. A kpọchiri Actions na ntọala container site na hash a na-apụghị ịgbanwe; a na-edozi
ndabere Python na `uv.lock`. Ọdịda Bandit na-eme ka CI daa, ma Atheris fuzzing nwere oke
na-anwale ndị nyocha SSH, MySQL, HTTP, asambodo na SNMPv3 BER
n'enweghị ohere netwọk.

Scorecard na-atụkwa ọrụ nyocha akụkọ ihe mere eme, ụdị dị iche iche nke ndị nyere aka, na
mmalite ntọhapụ. Akara ndị ahụ na-egosipụta ihe akaebe dị adị; ha abụghị nkwupụta
na nlele ọchịchị ma ọ bụ ntọhapụ akụkọ ihe mere eme ọ bụla zuru oke. Hụ
[SECURITY.md](../../../SECURITY.md) na [mmalite ntọhapụ](../../../docs/releasing.md).

## Ntụgharị asụsụ mpaghara

Ozi CLI na tebụl nchịkọta/ntụnyere terminal na-akwado asụsụ mpaghara 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) n'enweghị ndabere oge ọrụ ọzọ ọ bụla. Mkpebi na-asọpụrụ `--lang`, mesịa `LC_ALL`, `LC_MESSAGES`, na `LANG`, na-alaghachi na `en`. JSON schema, kọlụm CSV, na skripti mbupụ anaghị agbanwe n'asụsụ mpaghara niile.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Ntụnye aka

Ntụnye aka kwesịrị ịgụnye ikpe a pụrụ imeghachi, chekwaa nkwekọrịta CLI na
ụdị data e dere ede, ma gafee nlele mma dị n'elu. Hụ
[CONTRIBUTING.md](../../../CONTRIBUTING.md) maka usoro ọrụ mmepe na
[ntuziaka ntọhapụ](../../../docs/releasing.md) maka mkpebi ndakọrịta na ntụnye ụdị.

## Ọnọdụ nchekwa na ikike

Hụ [SECURITY.md](../../../SECURITY.md) maka akụkọ nzuzo na ụdị a kwadoro.
hostcensus nwere ikike n'okpuru [Ikike MIT](../../../LICENSE).

Isiokwu koodu isi iyi na-eji njirimara SPDX ma na-echekwa otuto ndị nyere aka sitere na akụkọ
ihe mere eme Git. Hụ [AUTHORS.md](../../../AUTHORS.md) maka ntụnye otuto. Nnwale njide baịnarị na
faịlụ mkpọchi e mepụtara na-eji faịlụ `.license` dị n'akụkụ; ederede MIT dị na `LICENSES/MIT.txt`.
