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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · **Kinyarwanda** · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus ni igikoresho cya Python cyo ku murongo w'amabwiriza (CLI) gifasha gukora ibarura rya serivisi rishobora gusubirwamo ku miyoboro uyobora.
Gikora inyandiko y'ibyo ibikoresho bigaragaza, kikagereranya ibyabonetse mu bihe bitandukanye, kandi kigakora script zo kwinjiza amakuru muri Kadupul. Uburyo bw'ibanze bukoresha socket za asyncio bitabaye ngombwa kugira uburenganzira bwa root; uburyo bwo guhitamo bwo gushakisha hakoreshejwe Nmap bushobora kumenya imashini zirenze port za serivisi zashyizweho.

## Impamvu yo gukoresha hostcensus

Raporo ya port ikozwe rimwe gusa ntigaragaza niba igenzura rikurikiraho ryahindutse cyangwa niba ryananiwe gukora. hostcensus ihuza imiterere isobanutse ya serivisi, isuzuma rifite imipaka, imyirondoro y'igenzura yongera gukoreshwa, n'amateka abitswe aho ukorera. Abayobora imiyoboro bashobora gusubiramo igice kimwe cy'igenzura, bakagenzura amakosa, kandi bagatandukanya ibyabonetse bitizewe n'impinduka zemejwe.

- **Ibimenyetso bya serivisi:** kumenya SSH, indamutso za MySQL, imitwe ya HTTP, isuzuma ry'ibyemezo bya TLS, hamwe no gushakisha SNMP cyangwa ibibazo bya system-MIB bikoresha amakuru yo kwinjira.
- **Igice cy'igenzura gisubirwamo:** imyirondoro ya TOML ifite amazina, ibikurwamo byongerwaho, serivisi zigenwa, imipaka y'imashini n'amasuzuma, n'imirimo ikorera rimwe ifite umupaka (bounded workers).
- **Igenzura mbere yo kohereza amakuru ku muyoboro:** isuzuma rya mbere (preflight) ribera aho ukorera ryemeza intego, ibikoresho, uburenganzira bwo kwandika aho amakuru ajya, imiterere y'amateka, n'ibitsinda bya TLS CA byashyizweho.
- **Amateka y'ibarura:** snapshot za SQLite zikozwe mu buryo bwa transaction zibika ibyabonetse byose; igereranya rigaragaza amakosa y'igenzura n'imiterere itazwi.
- **Ibisubizo bikorana n'ibindi bikoresho:** raporo zo kuri terminal, iza JSON n'iza CSV, snapshot z'amadosiye zifite verisiyo, na script zo kwinjiza amakuru muri Kadupul.

CI ikorera kuri Python 3.12, 3.13 na 3.14 kuri Linux na macOS, wongeyeho laboratwari y'igerageza ihujwe ya Compose igenzurwa. Kode ikoresha uburyo bugezweho bwa type aliases, ibisubizo bya preflight bifite ubwoko, imyirondoro ya slotted ikoresha keyword-only, n'uburyo butunganyije bwo gusukura async igumana izo verisiyo za runtime. Reba [Kugena verisiyo n'isohora](../../../docs/releasing.md) kugira ngo ubone amasezerano yo guhuza ya SemVer n'uburyo bwo gusohora kuri GitHub. Ikirango cy'isohora (release badge) kivuga amadosiye yasohowe yatangajwe, si ibiri muri iyi kopi: tagi iheruka gutangazwa ubu ni `v0.3.0`, mu gihe iyi kopi ikoresha verisiyo ya paki ya `3.0.0`. Shyiramo uvanye muri iyi kopi kugira ngo ukoreshe ibikorwa by'ibarura bisobanurwa hano.

Tangirira ku [gushyiramo](#install), hanyuma [imyirondoro n'amateka](#inventory-profiles-preflight-and-local-history).
Ku bisobanuro byo guhuza n'ibindi, reba [ibimenyetso biranga serivisi](#fingerprints),
[igereranya ry'amadosiye](#inventory-diff), na [kohereza muri Kadupul](#kadupul-export).

## Gushyiramo

Python 3.12 cyangwa verisiyo nshya irakenewe; Python 3.12 kugeza 3.14 ni yo yageragejwe. Uvanye muri iyi kopi y'ububiko, shyiramo ibisabwa bya runtime byafunzwe:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Kugira ngo ukoreshe uburyo bwo guhitamo bwo gushakisha imashini na Nmap, shyiramo porogaramu ya Nmap ukoresheje umuyobozi wa paki wa sisitemu yawe; nta yindi paki ya Python ikenewe. Ibisubizo bya XML bya Nmap bisomwa hakoreshejwe defusedxml, ari cyo gisabwa cy'ibanze, bityo kwagura entity (entity expansion) birangwa. hostcensus itangiza `nmap` iboneka muri `PATH` mu buryo butaziguye ikoresheje urutonde rw'ibipimo rudahinduka, igihe ntarengwa kiyongera uko ingano ya prefix yiyongera, n'umupaka w'ibisubizo wa 64 MiB. Nmap ntikenewe ku buryo bw'ibanze.

## Kwimuka uvuye kuri netprobe

hostcensus ni izina rishya rya netprobe, ryasohotse muri 3.0.0. Umushinga ntiwigeze utangazwa kuri PyPI ku izina na rimwe muri ayo, bityo gushyiramo byakorwaga uvanye mu kopi y'ububiko cyangwa mu isohora rya GitHub. Ububiko bwa GitHub bugumana izina ryabwo.

| Byahoze ari | Ubu ni | Guhuza |
| --- | --- | --- |
| Paki ya `netprobe` | `hostcensus` | Ongera ushyiremo uvanye mu kopi y'ububiko; nta paki ifite izina rya kera ibaho. |
| Ibwiriza `netprobe` | `hostcensus` | `netprobe` iracyakora kandi ikerekana umurongo umwe w'umuburo wo gucyura igihe kuri stderr. Kode zo gusohoka na stdout ntibyahindutse. Izakurwaho mu isohora rikuru rikurikiraho. |
| Impinduragaciro z'ibidukikije `NETPROBE_*` | `HOSTCENSUS_*` | Impinduragaciro ya `NETPROBE_*` ikoreshwa iyo impinduragaciro bihuje ya `HOSTCENSUS_*` itashyizweho, hamwe n'umuburo umwe kuri stderr uvuga amazina y'impinduragaciro ariko utigera werekana agaciro kazo. `HOSTCENSUS_*` iruta iyo byombi bishyizweho. Izakurwaho mu isohora rikuru rikurikiraho. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Impinduka ihagarika imikorere ya kera.** Nta buryo bwo guhuza import bushyirwamo; vugurura amabwiriza ya import. |
| Tagi y'ishusho ya Docker `network-discovery:test` (CI gusa) n'umukoresha wa container `netprobe` | `hostcensus:test`, umukoresha `hostcensus` | Nta shusho yigeze itangazwa muri registry. Ongera wubake ishusho kandi ukoreshe entrypoint ya `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Idosiye isanzwe ifite izina rya kera ry'ibanze iracyakoreshwa, hamwe n'umuburo, igihe izina rishya ritarabaho. Inzira zatanzwe ku mugaragaro na `--config` hamwe na `--history` ntizihinduka. |
| Raporo na snapshot bifite `"format": "netprobe-report"` cyangwa `"netprobe-snapshot"`, n'igice cya `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` na `export` biracyasoma amadosiye yanditswe ku izina rya kera, kandi JSON Schema zatangajwe zemera inyandiko zombi. Amadosiye mashya akoresha amazina mashya. Ububiko bw'amateka bwa SQLite ntibwahindutse kandi bukomeza gusomwa nka mbere. |
| Script za Kadupul zivuye kuri `netprobe export` | Script zivuye kuri `hostcensus export` | Script za kera zikomeza gukora kandi zigakomeza gusoma `NETPROBE_SNMP_*` iyo zikoreshejwe. Script nshya zisoma `HOSTCENSUS_SNMP_*`. |

## Urugero rwihuse

Byakorewe muri container y'igerageza ya laboratwari ihujwe isobanurwa mu gice cy'Iterambere; ibisubizo byagabanyijwe:

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

## Kode zo gusohoka

| Ibwiriza | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | ibyabonetse cyangwa raporo byabitswe | isuzuma rya mbere, backend, amateka, cyangwa kwandika raporo na snapshot byananiwe | intego, amahitamo, amagenamiterere, cyangwa imipaka bitari byo | - | `--deadline` yagezeho; raporo ituzuye yanditswe, amateka na snapshot byasimbukiwe |
| `preflight` | igenzura ryagenze neza | igenzura ryo aho ukorera ryananiwe | intego cyangwa amagenamiterere bitari byo, cyangwa inzira zo kwandikamo zigongana | - | - |
| `profiles` | imyirondoro yemejwe yagaragajwe | - | amagenamiterere cyangwa ihitamo bidasomeka cyangwa bitari byo | - | - |
| `history` | incamake zagaragajwe | amateka abura, atari yo, cyangwa adashyigikiwe | amahitamo ya CLI atari yo | - | - |
| `compare` | igereranya ryakozwe, harimo n'iyo hari impinduka | amateka adasomeka, igice cyangwa urutonde bidahura, cyangwa kwandika byananiwe | amahitamo ya CLI atari yo | - | - |
| `diff` | nta mpinduka | idosiye ya `-o` ntishoboye kwandikwa | idosiye ibura, idasomeka cyangwa idashyigikiwe, cyangwa igenzura rituzuye ridafite `--allow-partial` | impinduka zabonetse, ibyabonetse bitaremezwa, cyangwa igenzura rituzuye | - |
| `export` | script yanditswe | script ntishoboye kwandikwa | idosiye idasomeka, igenzura rituzuye ridafite `--allow-partial`, cyangwa amakuru adashobora koherezwa mu mutekano | - | - |

## Imiterere ya kode

| Igice (Module) | Inshingano |
| --- | --- |
| `cli.py` | Amahitamo y'amabwiriza, guhitamo umwirondoro, isuzuma rya mbere, igenzura no gukora raporo |
| `scanner.py`, `probes.py` | Kwagura intego, imirimo ikorera rimwe ifite umupaka, gushakisha imashini no kugenzura serivisi |
| `config.py`, `profiles.py` | Ibisobanuro bya serivisi n'imyirondoro y'ibarura yemejwe |
| `models.py`, `output.py` | Ubwoko bw'ibisubizo no kugaragaza mu buryo bwa terminal, JSON na CSV |
| `history.py`, `diff.py` | Amateka ya SQLite n'igereranya rya snapshot z'amadosiye zifite verisiyo |
| `preflight.py` | Igenzura ryo aho ukorera no kureba verisiyo ya Nmap bifite umupaka |
| `export.py` | Script zo kwinjiza amakuru muri Kadupul zemejwe kandi zishyizwe mu twuguruzo (quoted) |

Buri suzuma rya serivisi ribika imiterere yayo ukwabyo bitandukanye n'umwirondoro itangaza.
Gusoma n'igihe ntarengwa bifite imipaka; amakosa y'isuzuma aguma mu makosa y'imashini. Amateka ya SQLite
akoresha transaction, gufunga umuyoboro ku mugaragaro, n'uburyo bwo gusoma gusa mu kugaragaza urutonde no
kugereranya. Amakuru y'ibanga ya SNMP yinjira gusa binyuze mu mpinduragaciro z'ibidukikije cyangwa amadosiye
y'ibanga; amateka y'ibarura abika gusa amagenamiterere akoreshwa atari ay'ibanga. Reba
[Imiterere y'uburyo ikora](../../../docs/architecture.md) kugira ngo ubone inzira y'igenzura, imipaka yayo n'imipaka
y'icyizere, na [SECURITY.md](../../../SECURITY.md#authorized-use) ku mikoreshereze yemewe.


## Imikoreshereze

Genzura imiyoboro uyobora gusa.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Ihitamo | Ibisobanuro |
| --- | --- |
| `NETWORK` | CIDR, IP, cyangwa izina ry'imashini (hostname); bishobora kudasabwa iyo hakoreshejwe `--profile`. Ibirango bya IPv6 scope birangwa. |
| `-o, --output PATH` | Andika raporo. Imiterere ikurikiza umugereka (`.json`, `.csv`); indi migereka ikoresha JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Hatiriza imiterere ya raporo. Nta gaciro bigira nta `--output`. `.sh` ihitamo `kadupul`. |
| `-v, --verbose` | Inyandiko z'igenzura rya debug. |
| `-q, --quiet` | Hisha ibisubizo, aho igikorwa kigeze n'inyandiko z'amakuru; imiburo n'amakosa bikomeza kugaragara kuri stderr. |
| `--backend asyncio\|nmap` | Gushakisha imashini. `asyncio` (uburyo bw'ibanze) isuzuma port za serivisi mu buryo butaziguye; `nmap` ibanza gukora ping sweep ya nmap kandi isaba porogaramu ya `nmap` muri `PATH`. |
| `--timeout SECONDS` | Igihe cyo gutegereza amasuzuma atishyiriyeho igihe cyayo (uburyo bw'ibanze 1.0). Amasuzuma y'ibanze yo kwihuza (connect probes) akoresha 0.3s keretse imbonerahamwe ya serivisi ishyizeho `timeout`. |
| `--concurrency N` | Umubare w'amasuzuma akorera rimwe (uburyo bw'ibanze 256). |
| `--deadline SECONDS` | Hagarika igenzura ryose, harimo na ping sweep ya nmap, nyuma y'iki gihe (uburyo bw'ibanze 3600, ntarengwa 604800; impinduragaciro `HOSTCENSUS_DEADLINE`). Imashini zarangiye zandikwa muri raporo zifite `"complete": false`, nta mateka cyangwa snapshot byandikwa, kandi `scan` isohoka ifite kode 4. |
| `--config PATH` | Ibisobanuro bya serivisi bya TOML n'amagenamiterere ya `[profiles]` afite amazina atari itegeko. |
| `--profile NAME` | Koresha umwirondoro ufite izina; uburyo bw'ibanze bukoresha `hostcensus.toml` iyo `--config` itatanzwe. |
| `--exclude IP/CIDR` | Ongeraho ibikurwamo; subira uko bikenewe. Imashini ya IPv4 yakuwemo inakura mo aderesi za IPv6 ziyigeraho: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) na 6to4. Intego n'ibikurwamo bya IPv4-mapped bifatwa nk'aderesi za IPv4 zihagarariye. |
| `--max-hosts N` | Umupaka w'aderesi ugenzurwa mbere yo gukuramo izakuwemo (uburyo bw'ibanze kandi ntarengwa ni 65,536). |
| `--history PATH` | Bika igenzura ryarangiye mu bubiko bw'amateka bwa SQLite buhitamo gukoreshwa. |
| `--services NAMES` | Urutonde rw'amazina ya serivisi zitandukanyijwe n'akitso zigomba kugenzurwa, muri urwo rutonde (uburyo bw'ibanze: zose). |
| `--ports SPEC` | Urutonde rutandukanyijwe n'akitso rwa `NAME=PORT` (kwimura serivisi) cyangwa `PORT` (kongeraho igenzura risanzwe rya TCP ryitwa `tcp-PORT`). |
| `--snmp-community-file PATH` | Idosiye ibitse community ya SNMPv2c y'ikibazo cya system MIB. Impinduragaciro: `HOSTCENSUS_SNMP_COMMUNITY` (agaciro) cyangwa `HOSTCENSUS_SNMP_COMMUNITY_FILE` (inzira). |
| `--snmp-user` | Umukoresha wa SNMPv3. Impinduragaciro: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (uburyo bw'ibanze), `SHA224`, `SHA256`, `SHA384`, `SHA512` n'idosiye ibitse ijambobanga. Impinduragaciro: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` cyangwa `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (uburyo bw'ibanze), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` n'idosiye ibitse ijambobanga. Impinduragaciro: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` cyangwa `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Andika kandi snapshot ifite verisiyo ya `hostcensus diff`. |
| `--tls-ca-file PATH` | Emeza ibyemezo bya HTTPS ukoresheje iri tsinda rya PEM aho gukoresha ububiko bwa sisitemu. Impinduragaciro: `HOSTCENSUS_TLS_CA_FILE`. |

Mu buryo bw'ibanze, buri mashini igenzurwaho SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) na HTTPS (TCP 443). Port za TCP zisuzumwa hakoreshejwe ihuza ryuzuye (full connect). SNMP isuzumwa hakoreshejwe icyifuzo cyo gushakisha engine ya SNMPv3, buri agent ya SNMPv3 igomba gusubiza nta makuru yo kwinjira; agent zikoresha v1/v2c gusa ntizimenyekana muri iri suzuma. Hakoreshejwe backend ya asyncio, imashini ibarwa nk'izima iyo isuzuma iryo ari ryo ryose ribonye igisubizo, harimo n'ihuza ryanzwe, bityo imashini yanga buri suzuma ntigire icyo isubiza iba ifite `alive=false` n'ikosa "Host is down"; ibi ntibyemeza ko izimije mu by'ukuri. Hakoreshejwe `--backend nmap`, nmap ni yo yemeza imashini zizima (ICMP nk'umukoresha root, cyangwa TCP 80/443 ubundi).

### Ibimenyetso biranga serivisi

Buri serivisi ifunguye isuzumirwa ibimenyetso bihereye ku byo yohereza mbere yo kwinjira (login). Nta kintu gikora ubugenzuzi bwo kwinjira keretse ikibazo cya SNMP, kandi gusa iyo utanze amakuru yo kwinjira.

| Isuzuma | Ibyo risoma | `version` | Imfunguzo za `details` |
| --- | --- | --- | --- |
| `ssh` | Umurongo uranga wa RFC 4253 | porogaramu, urugero `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Indamutso y'ibanze ya MySQL/MariaDB | verisiyo ya seriveri | `server_version`, `flavor`, `auth_plugin`, cyangwa `error_code`/`error` |
| `http` | Igisubizo cya `HEAD /` | Umutwe wa `Server` | `status`, `server` |
| `https` | Ihuza rya TLS, icyemezo, `HEAD /` | Umutwe wa `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Gushakisha SNMPv3; hamwe n'amakuru yo kwinjira, GET ya sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; hamwe n'amakuru yo kwinjira `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, cyangwa `snmp_error` |

Intego y'izina ry'imashini (hostname) isobanurwa rimwe kuri buri mashini kandi buri suzuma ryihuza kuri iyo aderesi, ikabikwa nka `address` mu bisubizo; izina rikoreshwa gusa kuri TLS SNI, kwemeza icyemezo n'umutwe wa HTTP `Host`. Izina ritasobanutse ritanga imiterere ya `unknown` n'ikosa rya `Cannot resolve`. Amazina ya Reverse DNS abikwa gusa iyo arimo inyuguti zemewe z'izina ry'imashini, kandi ishakisha ritarenze 16 rikorera rimwe. HTTPS ikoresha iyemeza ry'icyemezo n'izina ry'imashini ugereranyije n'ububiko bwa sisitemu cyangwa `--tls-ca-file`. Ububiko bw'icyizere busomwa rimwe ku igenzura ryose bukongera gukoreshwa kuri buri suzuma rya HTTPS. Ihuza rya TCP n'ihuza rya TLS bibarirwa igihe ukwabyo, bityo port yemera ihuza ariko igahagarika ihuza rya TLS iba `open` ifite `tls_error`, aho kuba `filtered`. Iyo iyemeza rinaniwe, igisubizo kibika `cert_verified: false` na `cert_verify_error`; ntikigera gisubiramo gikoresheje amagenamiterere yoroshye cyangwa ngo cyohereze icyifuzo cya HTTP. Ibisobanuro by'icyemezo n'imitwe ya HTTP bikusanywa gusa nyuma y'uko iyemeza rigenze neza. Tanga itsinda rya CA rikwiye kuri serivisi zikoresha CA yihariye. Raporo za kera zishobora kuba zirimo `cert_read_unverified`, amasuzuma y'ubu atakibyara.

Amakuru y'ibanga ya SNMP asomwa gusa mu mpinduragaciro z'ibidukikije cyangwa mu madosiye (`--snmp-*-file`, cyangwa impinduragaciro bihuje ya `HOSTCENSUS_SNMP_*_FILE`), ntazigera asomwa mu bipimo byo ku murongo w'amabwiriza, ibyo abandi bakoresha ba sisitemu bashobora kubona ku rutonde rw'ibikorwa (process list). `--snmp-community`, `--snmp-auth-key` na `--snmp-priv-key` bifite agaciro bisohoka bifite kode 2 kandi bikerekana icyo bikwiriye gusimbuzwa. Idosiye y'ibanga igomba kuba ari UTF-8 itarimo ubusa kandi itarengeje bayite 4096; umurongo umwe musa w'impera urirengagizwa, kandi gushyiraho impinduragaciro n'idosiye ku ibanga rimwe ni ikosa. Amakosa avuga izina ry'idosiye ariko ntazigera yerekana ibiyirimo. Raporo z'igenzura n'amateka ntibishyiramo ku bushake agaciro k'amakuru yo kwinjira. Igikoresho cyo kohereza (exporter) gifite ihitamo ryihariye kandi risobanutse rya `--include-credentials` risobanurwa hasi. Community ihitamo SNMPv2c; umukoresha ahitamo SNMPv3, hamwe n'iyemeza (authentication) iyo urufunguzo rwa auth rutanzwe hamwe n'ibanga (privacy) iyo imfunguzo zombi zitanze (`snmp_security_level` ibika uburyo bwakoreshejwe). hostcensus yanga, isohoka ifite kode 2, guhuza community n'umukoresha wa v3, gukoresha urufunguzo rwa privacy nta rufunguzo rwa auth, cyangwa gukoresha imfunguzo nta mukoresha, kandi ntizigera isubiramo ikibazo cya v3 cyananiwe ikoresheje v2c cyangwa urwego rw'umutekano ruri hasi. Agent zikoresha v1/v2c gusa zirengagiza ishakisha rya v3 ridafite amakuru yo kwinjira, bityo zigaragara nk'izifunguye gusa iyo community itanzwe.

Inyandiko ya banner igabanywa ikagumana inyuguti zigaragara (printable characters) gusa kandi ikagira umupaka w'inyuguti 256 mbere yo kubikwa cyangwa kwerekanwa. Gusoma na ko gufite imipaka: 4 KiB kuri buri murongo, 4 KiB ku ndamutso ya MySQL, 16 KiB ku mitwe ya HTTP. SNMP engine ID irengeje octets 32 irakatwa mbere yo kubikwa. HTTP na HTTPS zohereza umutwe wa Host ufite aderesi ya IPv6 iri mu dukubo tw'imfuruka (brackets) kandi ufite port iyo atari 80 cyangwa 443. Utuzu twa CSV dutangira n'ikimenyetso gitangiza imibare ya spreadsheet twongerwaho inyuguti imbere kugira ngo akazu kagume ari inyandiko isanzwe.

### Imipaka

Igenzura rimwe ryemera aderesi zitarenze 65,536, serivisi 64, n'amasuzuma 524,288 (imashini gukuba serivisi); ibyifuzo binini kurushaho bisohoka bifite kode 2 mbere y'uko hagira ikintu cyoherezwa. `--concurrency` ifite umupaka wa socket 4096. Buri suzuma rifite igihe ntarengwa cya nyuma kingana n'inshuro enye z'igihe ryagenewe. Amasuzuma yo kwihuza (`tcp`, `ssh`, `mysql`, `http`) akoresha amasegonda 0.3 keretse iyo serivisi ishyizeho `timeout`. SNMP na HTTPS zikoresha `--timeout` (uburyo bw'ibanze 1.0) iyo zitashyizeho igihe cyazo. Isuzuma rigeze ku gihe ntarengwa ribikwa nka `unknown` hamwe na "probe timed out" muri `errors`. Amakosa ya socket yo ku mashini ukorera ho (urugero nko gushirirwa na file descriptors) na yo aba `unknown` ikosa rikabikwa; ntazigera abarwa nka port ifunze na firewall (`filtered`) cyangwa imashini izimije. Mbere yo gusuzuma, hostcensus izamura umupaka woroshye (soft limit) w'amadosiye afunguye iwugana ku mupaka ukomeye (hard limit) kugira ngo uhuze na `--concurrency` wongeyeho descriptors 64; iyo bitashobotse, igenzura rya preflight rya `open files` rirananirwa maze `scan` igasohoka ifite kode 1 mbere yo kohereza amakuru ku muyoboro. Gushakisha kwa Nmap gukoresha igihe ntarengwa cy'amasegonda 30 kuri buri mashini. Prefix ihabwa nmap mu buryo bwa CIDR, kandi ping sweep irananirwa igasohoka ifite kode 1 iyo nmap itanze aderesi nkeya ugereranyije n'izo yahawe (urugero izina itashoboye gusobanura) aho kubara izo mashini nk'izizimije. Intego y'izina ry'imashini isobanurwa rimwe maze nmap igahabwa iyo aderesi, kugira ngo gushakisha n'amasuzuma bigere ku mashini imwe. Prefix yuzuye ni igikorwa kimwe cya nmap gifite igihe ntarengwa cya subprocess cy'amasegonda 35 kuri buri aderesi 256, kizamurwa ku mubare wuzuye. Ping sweep zifite ibikurwamo zikoresha ibice by'imashini 256 n'igihe ntarengwa cy'amasegonda 35 kuri buri gice. Gushyiraho imirimo ikorera rimwe (workers) bifite umupaka utajyanye n'ubunini bw'urwego rw'aderesi. Reverse DNS no gusobanura amazina y'imashini bifite igihe ntarengwa cyihariye cy'amasegonda abiri; ishakisha ritagaruka rirarekwa ku murongo waryo (thread), kugira ngo ritagumisha hostcensus ikora hejuru y'iyo mipaka. Ishakisha ritarenze 16 rikorera rimwe, kandi ishakisha ryaretswe rigumana umwanya waryo kugeza rigarutse, kugira ngo umubare wa thread zahagaze ugume ufite umupaka; iyo zose 16 zahagaze, amashakisha akurikiraho ategereza umwanya hanze y'igihe ntarengwa cy'amasegonda abiri (gitangira iyo umwanya uboneka) kugeza `--deadline` ihagaritse igenzura. `NetworkScanner` ikoreshejwe nk'isomero (library) idafite `deadline` ishobora gutegereza uwo mwanya ubuziraherezo. `--deadline` (uburyo bw'ibanze isaha imwe) ishyira umupaka ku igenzura ryose hejuru y'ibi byose.

### Kugenamiterere ya serivisi

Serivisi zishobora guhindurwa hakoreshejwe idosiye ya TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` iba imwe muri `tcp`, `ssh`, `mysql`, `http`, `https` cyangwa `snmp` kandi mu buryo bw'ibanze ifata izina rya serivisi iyo ari isuzuma, ubundi igafata `tcp`. `snmp` yonyine ni yo ikoresha UDP. Amazina ya serivisi agizwe n'inyuguti ntoya, imibare, `-` na `_`. Serivisi ebyiri ntizishobora gusangira port na protocol; amateka abika imiterere imwe kuri iryo huriro. `timeout` si itegeko, ibarwa mu masegonda, kandi ntijya munsi ya 0.05. Amasuzuma y'uburyo bwo kwihuza (`tcp`, `ssh`, `mysql`, `http`) mu buryo bw'ibanze akoresha amasegonda 0.3. `snmp` na `https` zikoresha `--timeout` y'igenzura iyo serivisi itashyizeho `timeout`. `--timeout` ntisimbura igihe serivisi isanganywe.

Raporo za JSON ni inyandiko zifite verisiyo (`"format": "hostcensus-report"`, `"version": 1`) zibika intego, serivisi zasuzumwe n'amagenamiterere iruhande rwa `devices`; `--format json` idafite `-o` yandika raporo kuri stdout aho kwerekana imbonerahamwe. Buri gisubizo cya JSON gifite schema yatangajwe; reba [Ibisubizo bya JSON](../../../docs/json-output.md). Ibikoresho bigumana ibice by'ibanze bya `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` na `errors` bikongeraho urutonde rwa `services` rurimo `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, cyangwa `unknown` iyo isuzuma ryananiwe ku mashini ukorera ho cyangwa ryageze ku gihe ntarengwa), `version` na `details` za buri suzuma. Ibisubizo bya CSV byongerwaho inkingi z'impera za `services` na `versions` kuri serivisi zifunguye. Agaciro ka boolean ka `ssh`, `snmp` na `mysql` gakurikiza serivisi zifite ayo mazina neza.


## Imyirondoro y'ibarura, isuzuma rya mbere n'amateka yo ku mashini

Imyirondoro ifite amazina isangira idosiye ya TOML n'ibisobanuro bya `[services]` bisanzweho. Koporora
[hostcensus.example.toml](../../../hostcensus.example.toml) mu idosiye `hostcensus.toml` maze ushyiremo imiyoboro
uyobora:

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

`preflight` isobanura amahitamo n'imyirondoro neza nk'uko `scan` ibikora, harimo
`--concurrency` ku igenzura ry'amadosiye afunguye, bityo isuzuma rya preflight rigenze neza rivuga ko `scan` izatangira
ifite gahunda imwe.

Imyirondoro yemera `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, na `max_hosts`. `services` na `ports` zikoresha imyandikire isanzwe y'urutonde
rutandukanyijwe n'akitso. Amahitamo ya CLI atanzwe ku mugaragaro asimbura amagenamiterere y'umwirondoro;
`--exclude` isubiwemo yongera ku bikurwamo by'umwirondoro. Umuyoboro utanzwe ku mugaragaro hamwe na `--profile` ugomba
kuba uri mu gice cya IP/CIDR cy'uwo mwirondoro. Amazina y'imashini (hostnames) aracyashyigikiwe ku magenzura
ataziguye, ariko ntashobora guhuzwa n'ibikurwamo bya IP. Imipaka y'imashini ikurikizwa mbere
y'ibikurwamo; umupaka rusange w'amasuzuma uracyakurikizwa nyuma yaho. Imashini zakuwemo
ntizisuzumwa mu igenzura rya serivisi no mu ishakisha rya Nmap ryo guhitamo.

Buri genzura rikora isuzuma rya preflight aho ukorera mbere yo kohereza amakuru ku ntego: imipaka y'intego n'amasuzuma,
uburenganzira bwo kwandika aho amakuru ajya, kuba porogaramu cyangwa wrapper ya Nmap bihari iyo bihiswemo, schema y'amateka,
n'itsinda rya TLS CA ryashyizweho. `preflight` itanga ibisubizo muri JSON kandi ntigenzura
intego cyangwa ngo ikore ububiko bw'amateka. Yandika by'agateganyo idosiye iruhande rwaho kugira ngo isuzume
uburenganzira bwo kwandika itahinduye ibisanzwe bihari. Uburyo bw'ibanze bwa asyncio
ntibukenera Nmap cyangwa root. Inzira zo kwandikamo zigomba kuba zitandukanye hagati yazo
no ku idosiye y'amagenamiterere yinjira, harimo na hard links; symlinks z'aho kwandika
zirangwa. Igenzura ryananiwe risubiza kode 1; igice cyangwa amagenamiterere bitari byo bisubiza kode 2.

Kwandika raporo no kohereza (export) bisaba ubufasha bwa `O_NOFOLLOW`. Kuri sisitemu zitagifite,
harimo na Windows, uko kwandika kurananirwa kutafunguye cyangwa ngo gusibe ibiri mu idosiye y'intego.
Raporo nshya na script zo kohereza bihabwa uburenganzira bwa nyirabyo gusa (mode 0600); gusimbura idosiye isanzweho bigumana
uburenganzira bwayo. Kwandika muri named pipe idafite uyisoma bihita binanirwa aho gutegereza. Ububiko bushya bwa `--history` na bwo bukorwa buhabwa uburenganzira bwa nyirabwo gusa; ubwari busanzweho bugumana uburenganzira bwabwo. Ubutumwa bw'inyandiko (logs) bwose bujya kuri stderr, kugira ngo stdout itware ibisubizo gusa. Amadosiye yoherejwe arimo amakuru yo kwinjira buri gihe ahatirizwa mode 0600.

Amateka ni ayo guhitamo kandi yuzuza snapshot za JSON zisanzweho n'ibwiriza rya `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Koresha ID zivuye muri `history`; urugero rwibanda ku bubiko bushya. Snapshot zibikwa
mu buryo bwa transaction hamwe n'igihe cyo gutangira n'icyo kurangiza cya UTC, verisiyo ya paki, amagenamiterere akoreshwa atari
ay'ibanga, incamake, n'ibyabonetse byose ku mashini no kuri serivisi, harimo n'amakosa ya buri mashini.
Ibyabonetse bituzuye by'imashini birabikwa. Amagenzura yahagaritswe ntabikwa. Amasezerano asanzweho ya raporo,
snapshot, export, na kode zo gusohoka za scan aragumishwa.

`history` igaragaza incamake za JSON itarinze gusoma amakuru yose y'ibikoresho byo mu mateka.
`compare` isoma amagenzura abiri yabitswe, isaba intego zisa neza na port zahiswemo
zisa, maze ikagaragaza impinduka mu gusubiza, imiterere, n'imiterere ya port. ID y'igenzura rya mbere
igomba kubanziriza ID y'irya nyuma. Iyo amagenzura yombi yabitswe afite `timeout` cyangwa `backend`
kandi izo ndangagaciro zitandukanye, raporo itanga umuburo ariko igakomeza kugereranya
ibyabonetse. Igihe cyo gutegereza gitandukanye gishobora gutuma port ya `filtered` igaragara nk'ifunguye. Amakosa y'igenzura
n'amasuzuma ya port ya `unknown` bishyirwaho ikimenyetso cy'ibitaramenyekana neza aho gufatwa
nk'ibimaze kuzimira cyangwa gufungwa byemejwe: imashini zifite amakosa zigaragara muri `uncertain_hosts`, kandi
buri mpinduka ya port irimo `unknown` (harimo n'iyo ari `unknown` mu magenzura yombi) igaragara
muri `unconfirmed_ports` aho kuba muri `port_changes`, keretse port ifunguye mu
igenzura rya nyuma, yo iba impinduka ya port. `compare` na `diff` zishyira port mu byiciro zikoresheje itegeko rimwe.
`no_longer_responding` isobanura kubura igisubizo, si ikimenyetso ko igikoresho cyakuweho.
Kode yo gusohoka 0 ya scan ntigaragaza ko buri mashini yashubije: genzura amakosa ya buri mashini. Igereranya rigenze neza risubiza 0 haba hari impinduka cyangwa ntazo; `diff` y'amadosiye isanzweho
igumana amasezerano yayo ya kode 3 yo gusohoka. Amateka adashyigikiwe cyangwa yangiritse asubiza 1.

Amateka abika amakuru y'ibarura, bityo hitamo ububiko bwo ku mashini burinzwe bikwiye. Amadosiye y'imyirondoro n'amagenamiterere abitswe ntabamo amakuru yo kwinjira ya SNMP;
imicungire y'amakuru yo kwinjira ikomeza kunyura mu mahitamo n'impinduragaciro z'ibidukikije bya runtime bisanzweho.

## Itandukaniro ry'ibarura

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Snapshot ni JSON ifite `format: "hostcensus-snapshot"`, `version: 1`, verisiyo ya hostcensus, igihe yakorewe cya UTC, intego, `timeout` na `backend` by'igenzura iyo igenzura ryabibitse, serivisi zasuzumwe, n'imashini zizima mu miterere imwe na raporo ya `-o`. Imashini zizimije ntizishyirwamo. `diff` yemera kandi raporo zisanzwe za JSON za `scan -o`, harimo n'izakozwe mbere y'uko igice cya `services` kibaho.

`diff` igaragaza imashini nshya n'izazimiye, port zafungutse cyangwa zafunzwe ku mashini ziri mu mpande zombi, na serivisi zahinduye `version`. Port zasuzumwe mu igenzura rimwe gusa muri ayo abiri ntizigereranywa, kandi umuburo ubisobanura. Amasuzuma yananiwe ntazigera afatwa nka "nta mpinduka": port ya `unknown` mu igenzura iryo ari ryo ryose kandi itafunguye mu rya nyuma ishyirwa muri `unconfirmed`, atari muri `closed`, ifite `before` ya `open`, `unknown` cyangwa `not-open` (yasuzumwe igasanga ifunze cyangwa ari `filtered`) na `after` ya `unknown` cyangwa `not-open`; port ifunguye ubu igaragazwa muri `opened` n'iyo isuzuma rya mbere ryaba ryananiwe. Imashini amasuzuma yayo yose yananiwe nta gisubizo mu igenzura iryo ari ryo ryose ishyirwa muri `unsettled_hosts` (ifite `before`/`after` ya `up`, `uncertain` cyangwa `absent`, harimo n'iyo yananiwe mu magenzura yombi cyangwa ibura mu yindi dosiye) aho kuba muri `vanished_hosts`; iyo ishubije mu igenzura rya nyuma inagaragazwa nk'imashini nshya hamwe na port zayo zifunguye. Snapshot zigumana izo mashini zananiwe ku bw'iyo mpamvu. Umuburo kandi ugaragara iyo intego zitandukanye, n'iyo amadosiye yombi yabika `timeout` cyangwa `backend` zitandukanye. `-o PATH` yandika kandi imiterere ya JSON mu idosiye.

Raporo y'igenzura ryahagaritswe na `--deadline` (`"complete": false`) igaragaza gusa imashini yagezeho, bityo `diff` na `export` ziyanga zisohoka zifite kode 2. `--allow-partial` irayemera hamwe n'umuburo kuri stderr: `diff` ihita ishyira imashini igenzura rituzuye ritagaragaje na gato muri `unsettled_hosts` nka `unscanned` aho kuba izazimiye (imashini yagaragajwe nk'izimije ikomeza kubarwa nk'iyazimiye), ishyira `partial` kuri true kandi ntizigera itangaza ko nta mpinduka zabaye, naho `export` yandika umuburo mu mutwe wa script.

Kode zo gusohoka za `diff`: `0` nta mpinduka, `3` impinduka zabonetse, ibyabonetse bitashoboye kwemezwa, cyangwa idosiye ituzuye (`changed` iba true igihe cyose urutonde urwo ari rwo rwose, harimo `unsettled_hosts` na `unconfirmed`, rutari ubusa, cyangwa `partial` iri true), `2` idosiye irabura, ntishobora gusomwa, si snapshot ishyigikiwe, cyangwa ntiyuzuye kandi nta `--allow-partial`, `1` idosiye ya `-o` ntishoboye kwandikwa.

## Kohereza muri Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (ishami rya Cacti 1.2.31) nta buryo ifite bwo kwinjiza amadosiye y'ibikoresho byinshi icyarimwe. Uburyo bwayo bushyigikiwe bwo kongeramo ibikoresho uvanye muri script ni `cli/add_device.php`, igikoresho kimwe kuri buri guhamagara, hakoreshejwe ibipimo bya `--option=value`. `hostcensus export` yandika script ya POSIX `sh` irimo ayo mahamagara:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Buri mashini izima ihinduka `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Imashini ikibazo cya SNMP cy'igenzura cyagenze neza zihabwa `--version=2 --community=...` cyangwa `--version=3 --username=... --authproto=... --password=...` (wongeyeho `--privproto`/`--privpass` kuri authPriv), `--port` na `--avail=snmp`. Kohereza SNMPv3 bisaba `--snmp-user`, kandi noAuthNoPriv irangwa kuko `add_device.php` isaba ijambobanga rya v3.
- Izindi mashini zihabwa `--version=0 --avail=ping`, hamwe na `--ping_method=tcp --ping_port=` port ya mbere ya TCP ifunguye, cyangwa ICMP iyo ntayo.
- `--notes` igaragaza serivisi zifunguye na verisiyo zazo. `--description` iba izina rya reverse-DNS iyo risanzwe (inyuguti, imibare, `.`, `_`, `-`), ubundi ikaba IP, kandi igirwa yihariye, kuko `add_device.php` ifata ibisobanuro bisanzweho nko kuvugurura icyo gikoresho.

Buri gaciro karagenzurwa kandi kakajya mu twuguruzo twa shell hakoreshejwe `shlex.quote`. Mu buryo bw'ibanze nta banga rya SNMP ryandikwa: script ikoresha `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` cyangwa `HOSTCENSUS_SNMP_PRIV_KEY` mu gihe cyo gukora kandi igahagarara iyo hari itashyizweho. `--include-credentials` yo yandika agaciro kavuye muri izo mpinduragaciro z'ibidukikije muri script, ikayikora ifite mode 0600, kandi ikandika umuburo. `add_device.php` ubwayo yerekana community kandi yakira amabanga nk'ibipimo, bigaragara ku rutonde rw'ibikorwa (process list) rwa seriveri ya Kadupul mu gihe buri guhamagara kuri gukora.

`add_device.php` isohoka ifite kode 1 ku bikoresho bisubiyemo no ku makosa; script ikomeza gukora, ikabara ibyananiwe, kandi igasohoka ifite kode 1 iyo hari igikoresho kitongeweho. ID za template ziva muri `php cli/add_device.php --list-host-templates`. Kode zo gusohoka za `export`: `0` yanditswe, `2` idosiye yinjira idasomeka, igenzura rituzuye ridafite `--allow-partial`, cyangwa amakuru adashobora koherezwa mu mutekano, `1` script ntishoboye kwandikwa.

## Kugena verisiyo n'uburyo bwo gusohora

hostcensus ikurikiza [Semantic Versioning](https://semver.org/spec/v2.0.0.html): ibikosorwa
bihuza n'ibisanzwe byongera verisiyo ya patch, ibikorwa bishya cyangwa ibicyuye igihe bihuza n'ibisanzwe byongera
verisiyo ya minor, naho impinduka zihagarika guhuza zongera verisiyo ya major.
Amabwiriza n'amahitamo, kode zo gusohoka na JSON schema ni yo masezerano rusange;
imikorere yacyuye igihe ikomeza gukora kugeza ku isohora rikuru rikurikiraho, keretse igihe
igikosorwa cy'umutekano gisaba kuyihindura mbere (icyo gihe changelog isobanura impamvu).

release-please ifungura PR y'isohora ikuye ku mitwe ya Conventional Commit iri kuri `main`,
ikazamura `pyproject.toml`, `uv.lock` na `CHANGES.md`. Kuyihuza (merge) bihita bikora
tagi ya `vMAJOR.MINOR.PATCH` n'isohora ry'ibanze (draft) rya GitHub, aho CI yongeraho
wheel yageragejwe, source distribution na checksums; GitHub ibika build attestations
z'ayo madosiye binyuze muri API yayo ya attestations. Umuyobozi w'umushinga asuzuma akanatangaza
isohora ry'ibanze amadosiye amaze kongerwaho. Amasohora ntazigera asimbuzwa.

Gutangaza kwizewe kuri PyPI (trusted publishing) ni ugushaka kandi bisaba uburenganzira bwa nyir'umushinga, trusted
publisher n'ibidukikije bya `pypi`. Bitangaza amadosiye y'isohora amwe yagenzuwe
bitongeye kuyubaka cyangwa ngo bibike token ya API. Amasohora afite tagi muri ubu bubiko
rusange abyara GitHub artifact attestations; amashami yihariye (private forks) asaba gahunda
ishyigikiwe no kwemeza ku mugaragaro. Reba
[ubuyobozi bwuzuye bwo gusohora](../../../docs/releasing.md) ku myiteguro, amabwiriza nyayo no kongera kugerageza.

## Iterambere

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Ibikoresho by'iterambere biba mu matsinda y'ibisabwa ya [PEP 735](https://peps.python.org/pep-0735/)
muri `pyproject.toml` (`dev`, `fuzz`, `build`), bityo ntibizigera bigaragara muri
metadata ya paki yatangajwe. `uv.lock` ni yo lockfile imwe rukumbi; CI ishyiramo ikoresheje
`uv sync --locked` kandi ikanga iyo lockfile ishaje. Hitamo interpreter ukoresheje
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), cyangwa Python 3.12+ iyo ari yo yose.

CI yubahiriza igipimo cyo hasi cya 90% cy'ubwishingizi bw'ibizamini (coverage) bya paki. Ibizamini by'ibice (unit tests) birimo
seriveri za loopback zigenzurwa n'ingero zo hanze ya murandasi z'imyirondoro, amateka no kwemeza isohora; laboratwari ya Compose ikoresha
OpenSSH, MariaDB, nginx na net-snmp kuri bridge yihariye. Yikoreshe ukoresheje
`make test-integration`. Reba [CONTRIBUTING.md](../../../CONTRIBUTING.md) na
[ibikoresho byo gusohora](../../../scripts/README.md).

Container ya runtime ikora nka UID/GID 10001 idafite ububiko bwa home, idafite kwinjira muri shell
kandi idafite pip, kandi ishobora kwandika muri `/app/output`. Ha uwo mukoresha uburenganzira bwo kwandika
mu bubiko bwose bw'ibisubizo bwahujwe (mounted). Ntikenera ubushobozi bwihariye (capabilities) kandi ikorana na
root filesystem isomwa gusa, bityo ishobora gukora nka:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap ikoresha imikorere yayo yo gushakisha TCP itagira uburenganzira bwihariye muri iyi container. CI ihagarika
iyubakwa ry'ishusho ku ntege nke zose za HIGH cyangwa CRITICAL zishobora gukosorwa zitangajwe na Trivy.

## Igenzura ry'uruhererekane rw'ibikoresho

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
ikorera kuri main na buri cyumweru, igatangaza amanota yayo nyayo, kandi ikohereza ibyabonetse kuri GitHub
code scanning. Actions n'ishusho shingiro za container zifungwa hakoreshejwe immutable hashes; ibisabwa bya Python
bikemurwa muri `uv.lock`. Amakosa ya Bandit ahagarika CI, kandi fuzzing ifite umupaka ya Atheris
igerageza abasomyi ba SSH, MySQL, HTTP, ibyemezo na SNMPv3 BER nta murandasi ikoreshejwe.

Scorecard ipima kandi amateka y'isuzuma rya kode, ubudasa bw'abatanga umusanzu, n'inkomoko
y'isohora (release provenance). Ayo manota agaragaza ibimenyetso nyabyo; si ukwemeza
ko buri genzura ry'imiyoborere cyangwa ry'amasohora ya kera ryujujwe. Reba
[SECURITY.md](../../../SECURITY.md) na [inkomoko y'isohora](../../../docs/releasing.md).

## Gushyira mu ndimi

Ubutumwa bwa CLI n'imbonerahamwe z'incamake n'itandukaniro zo kuri terminal bishyigikira indimi 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) nta yindi paki ya runtime ikenewe. Guhitamo ururimi bikurikiza `--lang`, hanyuma `LC_ALL`, `LC_MESSAGES`, na `LANG`, bigasubira kuri `en` iyo ntayibonetse. JSON schemas, inkingi za CSV, na script zo kohereza ntibihinduka mu ndimi zose.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Gutanga umusanzu

Imisanzu igomba kuba irimo urugero rushobora gusubirwamo, ikubahiriza amasezerano yanditse ya CLI
n'imiterere y'amakuru, kandi igatsinda igenzura ry'ubuziranenge riri hejuru. Reba
[CONTRIBUTING.md](../../../CONTRIBUTING.md) ku buryo bw'imikorere y'iterambere na
[ubuyobozi bwo gusohora](../../../docs/releasing.md) ku byemezo byo guhuza no kugena verisiyo.

## Umutekano n'imiterere y'uruhushya

Reba [SECURITY.md](../../../SECURITY.md) ku buryo bwo gutanga raporo mu ibanga na verisiyo zishyigikiwe.
hostcensus ifite uruhushya rwa [MIT License](../../../LICENSE).

Imitwe y'amadosiye ya kode ikoresha ibirango bya SPDX kandi ikagumana izina ry'abatanze umusanzu riva mu mateka ya Git.
Reba [AUTHORS.md](../../../AUTHORS.md) ku birebana no gushimira ababigizemo uruhare. Amadosiye y'igerageza ya binary na
lockfile yakozwe bikoresha amadosiye ya `.license` ari iruhande rwabyo; inyandiko ya MIT iri muri `LICENSES/MIT.txt`.
