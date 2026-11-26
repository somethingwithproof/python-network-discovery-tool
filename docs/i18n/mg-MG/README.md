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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · **Malagasy** · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Ny hostcensus dia fitaovana CLI amin'ny Python natao hanaovana lisitry ny tolotra azo averina matetika amin'ny tambajotra tantananao.
Mirakitra izay asehon'ny fitaovana izy, mampitaha ny fandinihana rehefa mandeha ny fotoana, ary mamorona soratra baiko fanafarana ho an'ny Kadupul. Ny rafitra ao ambadika mahazatra dia mampiasa soketa asyncio tsy mila zon'ny root; ny fitadiavana mpampiantrano amin'ny alalan'ny Nmap tsy voatery dia afaka mamantatra mpampiantrano mihoatra ny seranan-tolotra voarindra.

## Nahoana no mampiasa hostcensus

Ny tatitra seranana indray mandeha dia tsy manazava raha niova ny fandinihana manaraka na tsy nahomby fotsiny. Ny hostcensus dia manambatra ny toetry ny tolotra mazava, fitsapana voafetra, mombamomba ny fitarafana azo ampiasaina indray, ary tantara eo an-toerana. Afaka mamerina ny sahan'asa mitovy ny mpandraharaha, mijery ny hadisoana, ary manavaka ny fandinihana tsy azo antoka amin'ny fiovana voamarina.

- **Porofon'ny tolotra:** famantarana SSH, fiarahabana MySQL, lohateny HTTP, fandinihana taratasy fanamarinana TLS, ary fitadiavana SNMP na fanontaniana system-MIB misy mari-pamantarana.
- **Sahan'asa azo averina:** mombamomba TOML misy anarana, fanilihana azo ampiana, tolotra azo arindra, fetran'ny mpampiantrano/fitsapana, ary mpiasa voafetra.
- **Fanamarinana mialoha ny fifamoivoizana:** ny fanamarinana mialoha eo an-toerana dia manamarina ny lasibatra, fitaovana, fidirana amin'ny toerana fitehirizana, rafitry ny tantara, ary fonosana TLS CA voarindra.
- **Tantaran'ny lisitra:** ny tahiry raikitra SQLite misy fifanakalozana voaaro dia mitahiry ny fandinihana rehetra; ny fampitahana dia mitazona ho hita maso ny tsy fahombiazan'ny mpitarika fitarafana sy ny toetra tsy fantatra.
- **Vokatra mifandrindra:** tatitra amin'ny terminal, JSON sy CSV, tahiry raikitra an-drakitra misy kinova, ary soratra baiko fanafarana Kadupul.

Ny CI dia mandrakotra ny Python 3.12, 3.13 ary 3.14 amin'ny Linux sy macOS, miampy laboratoara fampidirana Compose voafehy. Ny kaody dia mampiasa anarana solon'ny karazana maoderina, vokatry ny fanamarinana mialoha voasokajy karazana, mombamomba misy slot sy teny fanalahidy ihany ary fanadiovana async voarafitra sady mitazona ireo kinova fampandehanana ireo. Jereo ny [Fanomezana kinova sy famoahana](../../../docs/releasing.md) ho an'ny fifanarahana momba ny fifanentanana SemVer sy ny dingana famoahana ao amin'ny GitHub. Ny marika famoahana dia mamaritra ny vokatra navoaka fa tsy ity dika nalaina ity: ny marika navoaka farany ankehitriny dia `v0.3.0`, fa ity dika nalaina ity kosa mampiasa kinovan'ny fonosana `3.0.0`. Mametraha avy amin'ity dika nalaina ity raha te hampiasa ireo endri-javatra lisitry ny tolotra voarakitra ato.

Atombohy amin'ny [fametrahana](#install), avy eo ny [mombamomba sy tantara](#inventory-profiles-preflight-and-local-history).
Ho an'ny antsipirian'ny fampidirana, jereo ny [famantarana ny tolotra](#fingerprints),
[fampitahana rakitra](#inventory-diff), ary [fanondranana Kadupul](#kadupul-export).

## Fametrahana

Ilaina ny Python 3.12 na vaovao kokoa; Python 3.12 hatramin'ny 3.14 no andiam-kinova voasedra. Avy amin'ity dika nalaina ity, apetraho ireo fiankinana fampandehanana voahidy:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Ho an'ny fitadiavana mpampiantrano amin'ny Nmap tsy voatery, apetraho ny fitaovana Nmap azo alefa amin'ny alalan'ny mpitantana fonosana amin'ny rafitrao; tsy mila fonosana Python fanampiny. Ny vokatra XML an'ny Nmap dia vakiana amin'ny alalan'ny defusedxml, fiankinana fototra, ka lavina ny fanitarana singa XML. Ny hostcensus dia mampandeha mivantana ny `nmap` hita ao amin'ny `PATH` miaraka amin'ny lisitra tondro raikitra, fe-potoana mitombo arakaraka ny haben'ny prefix, ary fetran'ny vokatra 64 MiB. Tsy ilaina ny Nmap ho an'ny rafitra ao ambadika mahazatra.

## Fifindrana avy amin'ny netprobe

Ny hostcensus no anarana vaovaon'ny netprobe, navoaka tamin'ny kinova 3.0.0. Tsy mbola navoaka tao amin'ny PyPI na tamin'ny anarana iray na tamin'ny iray hafa ity tetikasa ity, ka avy amin'ny dika nalaina na famoahana GitHub no nanaovana fametrahana. Mitazona ny anarany ny tahiry GitHub.

| Taloha | Ankehitriny | Fifanentanana |
| --- | --- | --- |
| Fonosana `netprobe` | `hostcensus` | Avereno apetraka avy amin'ny dika nalaina; tsy misy fonosana amin'ny anarana taloha. |
| Baiko `netprobe` | `hostcensus` | Mbola mandeha ny `netprobe` ary mamoaka andalana fampitandremana iray momba ny fanesorana miandalana ao amin'ny stderr. Tsy miova ny kaody fivoahana sy ny stdout. Hesorina amin'ny famoahana lehibe manaraka. |
| Fari-tontolo iainana `NETPROBE_*` | `HOSTCENSUS_*` | Ampiasaina ny fari-tontolo iainana `NETPROBE_*` rehefa tsy voafaritra ny mitovy aminy `HOSTCENSUS_*`, miaraka amin'ny fampitandremana iray ao amin'ny stderr izay manonona ny anaran'ny fari-tontolo fa tsy ny sandany velively. Mandresy ny `HOSTCENSUS_*` rehefa samy voafaritra izy roa. Hesorina amin'ny famoahana lehibe manaraka. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Manapaka fifanentanana.** Tsy misy tetezana fanafarana napetraka; havaozy ny fanafarana. |
| Marika sary Docker `network-discovery:test` (CI ihany) sy mpampiasa kaontenera `netprobe` | `hostcensus:test`, mpampiasa `hostcensus` | Tsy mbola nisy sary navoaka tany amin'ny rejisitra. Amboary indray ny sary ary ampiasao ny fidirana `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Ny rakitra efa misy mitondra ny anarana mahazatra taloha dia mbola ampiasaina, miaraka amin'ny fampitandremana, raha mbola tsy misy ny anarana vaovao. Tsy mikasika ny lalan-drakitra `--config` sy `--history` voafaritra mazava izany. |
| Tatitra sy tahiry raikitra misy `"format": "netprobe-report"` na `"netprobe-snapshot"`, sy ny saha `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | Ny `diff` sy `export` dia mbola mamaky rakitra voasoratra tamin'ny anarana taloha, ary manaiky ireo tsipelina roa ireo ny rafitra JSON Schemas navoaka. Ny rakitra vaovao dia mampiasa ny anarana vaovao. Tsy miova ny tahiry tantara SQLite ary mbola azo vakiana toy ny teo aloha. |
| Soratra baiko Kadupul avy amin'ny `netprobe export` | Soratra baiko avy amin'ny `hostcensus export` | Mbola miasa ny soratra baiko taloha ary mbola mamaky `NETPROBE_SNMP_*` rehefa mandeha. Ny soratra baiko vaovao dia mamaky `HOSTCENSUS_SNMP_*`. |

## Ohatra haingana

Alefaso avy ao amin'ny kaontenera fitsapana ao amin'ny laboratoara fampidirana voalaza ao amin'ny Fampandrosoana; nofohezina ny vokatra:

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

## Kaody fivoahana

| Baiko | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | voarakitra ny fandinihana/tatitra | tsy nahomby ny fanamarinana mialoha/rafitra ao ambadika, tantara, na fanoratana tatitra/tahiry raikitra | lasibatra, safidy, fandrindrana, na fetra tsy manan-kery | - | tratra ny `--deadline`; voasoratra ny tatitra ampahany, tsy natao ny tantara sy ny tahiry raikitra |
| `preflight` | nandalo ny fanamarinana | tsy nahomby ny fanamarinana eo an-toerana | lasibatra/fandrindrana tsy manan-kery na toerana fitehirizana mifanohitra | - | - |
| `profiles` | voatanisa ny mombamomba voamarina | - | fandrindrana na safidy tsy azo vakiana/tsy manan-kery | - | - |
| `history` | voatanisa ny famintinana | tantara tsy hita, tsy manan-kery, na tsy tohanana | safidy CLI tsy manan-kery | - | - |
| `compare` | vita ny fampitahana, anisan'izany rehefa misy fiovana | tantara tsy azo vakiana, sahan'asa/filaharana tsy mifanaraka, na tsy fahombiazan'ny fanoratana | safidy CLI tsy manan-kery | - | - |
| `diff` | tsy misy fiovana | tsy azo nosoratana ny rakitra `-o` | fampidirana tsy hita, tsy azo vakiana na tsy tohanana, na fitarafana tsy feno tsy misy `--allow-partial` | hita ny fiovana, fandinihana tsy voamarina, na fitarafana tsy feno | - |
| `export` | voasoratra ny soratra baiko | tsy azo nosoratana ny soratra baiko | fampidirana tsy azo vakiana, fitarafana tsy feno tsy misy `--allow-partial`, na angona tsy azo aondrana am-pilaminana | - | - |

## Fandaminana

| Maody | Andraikitra |
| --- | --- |
| `cli.py` | Safidin'ny baiko, famahana mombamomba, fanamarinana mialoha, fitarafana ary fanaovana tatitra |
| `scanner.py`, `probes.py` | Fanitarana lasibatra, mpiasa voafetra, fitadiavana mpampiantrano ary fandinihana tolotra |
| `config.py`, `profiles.py` | Famaritana tolotra sy mombamomba lisitra voamarina |
| `models.py`, `output.py` | Karazana vokatra sy famoahana amin'ny terminal/JSON/CSV |
| `history.py`, `diff.py` | Tantara SQLite sy fampitahana tahiry raikitra an-drakitra misy kinova |
| `preflight.py` | Fanamarinana eo an-toerana sy fijerena kinovan'ny Nmap voafetra |
| `export.py` | Soratra baiko fanafarana Kadupul voamarina sy voaaro tamin'ny mari-tsoratra |

Ny fandinihana tolotra tsirairay dia mirakitra misaraka ny toetrany sy ny mombamomba asehony.
Voafetra ny famakiana sy ny fe-potoana; mijanona ao amin'ny hadisoan'ny mpampiantrano ny hadisoana amin'ny fitsapana. Ny tantara SQLite dia mampiasa fifanakalozana voaaro, fanadiovana fifandraisana mazava, ary lalana famakiana ihany ho an'ny fitanisana sy fampitahana. Ny tsiambaratelo SNMP dia miditra amin'ny alalan'ny fari-tontolo iainana na rakitra tsiambaratelo ihany; ny tantaran'ny lisitra dia mitahiry ny fandrindrana tsy miafina manan-kery. Jereo ny [Rafitra](../../../docs/architecture.md) ho an'ny fantsona fitarafana, ny fetrany sy ny sisin-tanin'ny fitokisana, ary ny [SECURITY.md](../../../SECURITY.md#authorized-use) ho an'ny fampiasana nahazoana alalana.


## Fampiasana

Aza mitarika fitarafana afa-tsy amin'ny tambajotra tantananao.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Safidy | Dikany |
| --- | --- |
| `NETWORK` | CIDR, IP, na anaran'ny mpampiantrano; tsy voatery miaraka amin'ny `--profile`. Lavina ny famantarana faritra IPv6. |
| `-o, --output PATH` | Manoratra tatitra. Ny endrika dia manaraka ny fanitarana anaran-drakitra (`.json`, `.csv`); miverina amin'ny JSON ny fanitarana hafa. |
| `-f, --format json\|csv\|kadupul\|auto` | Manery ny endriky ny tatitra. Tsy misy fiantraikany raha tsy misy `--output`. Ny `.sh` dia misafidy `kadupul`. |
| `-v, --verbose` | Fandraiketana antsipiriany fanamboarana (debug). |
| `-q, --quiet` | Manafina ny vokatra, ny fivoarana ary ny tatitra fampahafantarana; mbola miseho ao amin'ny stderr ny fampitandremana sy ny hadisoana. |
| `--backend asyncio\|nmap` | Fitadiavana mpampiantrano. Ny `asyncio` (mahazatra) dia mitsapa mivantana ny seranan-tolotra; ny `nmap` dia manao fitarafana ping nmap aloha ary mila ny fitaovana `nmap` ao amin'ny `PATH`. |
| `--timeout SECONDS` | Miandry ireo fitsapana tsy mametraka fe-potoana manokana (mahazatra 1.0). Ny fitsapana fifandraisana ao anatiny dia mampiasa 0.3s raha tsy mametraka `timeout` ny tabilao tolotra. |
| `--concurrency N` | Fitsapana mandeha miaraka indray mandeha (mahazatra 256). |
| `--deadline SECONDS` | Mampiato ny fitarafana manontolo, anisan'izany ny fitarafana nmap, aorian'io faharetany io (mahazatra 3600, farafahabetsany 604800; fari-tontolo `HOSTCENSUS_DEADLINE`). Ny mpampiantrano vita dia soratana ao amin'ny tatitra miaraka amin'ny `"complete": false`, tsy misy tantara na tahiry raikitra soratana, ary mivoaka amin'ny kaody 4 ny `scan`. |
| `--config PATH` | Famaritana tolotra TOML sy fandrindrana `[profiles]` misy anarana tsy voatery. |
| `--profile NAME` | Mampiasa mombamomba misy anarana; mampiasa `hostcensus.toml` ho mahazatra rehefa tavela ny `--config`. |
| `--exclude IP/CIDR` | Manampy fanilihana; avereno araka izay ilaina. Ny mpampiantrano IPv4 voahilika dia manilika koa ny adiresy IPv6 mahatratra azy: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) ary 6to4. Ny lasibatra sy fanilihana IPv4-mapped dia raisina toy ny adiresy IPv4 tondroiny. |
| `--max-hosts N` | Fetran'ny adiresy hamarinina mialoha ny fanilihana (mahazatra/fetra faratampony 65,536). |
| `--history PATH` | Mirakitra ny fitarafana vita ao anaty tahiry tantara SQLite safidy. |
| `--services NAMES` | Lisitra anaran-tolotra sarahan'ny faingo hohamarinina, araka izany filaharany izany (mahazatra: rehetra). |
| `--ports SPEC` | Lisitra sarahan'ny faingo misy `NAME=PORT` (mamindra tolotra) na `PORT` (manampy fitsapana TCP tsotra antsoina hoe `tcp-PORT`). |
| `--snmp-community-file PATH` | Rakitra mitahiry ny community SNMPv2c ho an'ny fanontaniana system MIB. Fari-tontolo: `HOSTCENSUS_SNMP_COMMUNITY` (ny sanda) na `HOSTCENSUS_SNMP_COMMUNITY_FILE` (ny lalana). |
| `--snmp-user` | Mpampiasa SNMPv3. Fari-tontolo: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (mahazatra), `SHA224`, `SHA256`, `SHA384`, `SHA512` sy rakitra mitahiry ny fehezanteny miafina. Fari-tontolo: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` na `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (mahazatra), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` sy rakitra mitahiry ny fehezanteny miafina. Fari-tontolo: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` na `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Manoratra tahiry raikitra misy kinova koa ho an'ny `hostcensus diff`. |
| `--tls-ca-file PATH` | Manamarina ny taratasy fanamarinana HTTPS amin'ity fonosana PEM ity fa tsy amin'ny tahirin'ny rafitra. Fari-tontolo: `HOSTCENSUS_TLS_CA_FILE`. |

Amin'ny fomba mahazatra, ny mpampiantrano tsirairay dia hamarinina amin'ny SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) ary HTTPS (TCP 443). Ny seranana TCP dia tsapaina amin'ny fifandraisana feno. Ny SNMP dia tsapaina amin'ny fangatahana fitadiavana motera SNMPv3, izay tsy maintsy valian'ny mpandraharaha SNMPv3 rehetra tsy mila mari-pamantarana; ny mpandraharaha tsy mampiasa afa-tsy v1/v2c dia tsy ho hitan'ity fitsapana ity. Amin'ny rafitra ao ambadika asyncio, ny mpampiantrano dia heverina ho velona rehefa mahazo valiny ny fitsapana iray, anisan'izany ny fifandraisana nolavina, ka ny mpampiantrano mandà mangina ny fitsapana rehetra dia manana `alive=false` sy ny hadisoana "Host is down"; tsy manaporofo izany fa maty ara-batana izy. Miaraka amin'ny `--backend nmap`, ny nmap no manapa-kevitra hoe iza amin'ny mpampiantrano no velona (ICMP raha root, TCP 80/443 raha tsy izany).

### Famantarana ny tolotra

Ny tolotra misokatra tsirairay dia fantarina avy amin'izay alefany mialoha ny fidirana. Tsy misy manao fanamarinana maha-izy azy afa-tsy ny fanontaniana SNMP, ary rehefa manome mari-pamantarana ianao ihany.

| Fitsapana | Mamaky | `version` | Fanalahidy `details` |
| --- | --- | --- | --- |
| `ssh` | Andalana famantarana RFC 4253 | rindrankajy, ohatra `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Fifandraisana voalohany MySQL/MariaDB | kinovan'ny lohamilina | `server_version`, `flavor`, `auth_plugin`, na `error_code`/`error` |
| `http` | Valin'ny `HEAD /` | lohateny `Server` | `status`, `server` |
| `https` | Fifandraisana TLS, taratasy fanamarinana, `HEAD /` | lohateny `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Fitadiavana SNMPv3; miaraka amin'ny mari-pamantarana, GET an'ny sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; miaraka amin'ny mari-pamantarana `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, na `snmp_error` |

Ny lasibatra anaran'ny mpampiantrano dia vahana indray mandeha isaky ny mpampiantrano ary ny fitsapana rehetra dia mifandray amin'io adiresy io, voarakitra ho `address` ao amin'ny vokatra; ny anarana dia ampiasaina ihany ho an'ny TLS SNI, fanamarinana taratasy fanamarinana ary ny lohateny HTTP `Host`. Ny anarana tsy voavaha dia manome toetra `unknown` sy hadisoana `Cannot resolve`. Ny anarana reverse DNS dia tazonina ihany rehefa tsy ahitana afa-tsy soratra azo ekena amin'ny anaran'ny mpampiantrano, ary farafahabetsany 16 ny fikarohana mandeha indray mandeha. Ny HTTPS dia mampiasa fanamarinana taratasy fanamarinana sy anaran'ny mpampiantrano mifanaraka amin'ny tahirin'ny rafitra na `--tls-ca-file`. Ny tahiry fitokisana dia ampidirina indray mandeha ho an'ny fitarafana manontolo ary ampiasaina indray amin'ny fitsapana HTTPS rehetra. Ny fifandraisana TCP sy ny fifandraisana TLS dia refesina misaraka ny fotoanany, ka ny seranana manaiky fifandraisana fa mampihantona ny fifandraisana TLS dia `open` miaraka amin'ny `tls_error`, fa tsy `filtered`. Raha tsy mahomby ny fanamarinana, ny vokatra dia mirakitra `cert_verified: false` sy `cert_verify_error`; tsy manandrana indray amin'ny fandrindrana malemy kokoa na mandefa fangatahana HTTP izy. Ny antsipirian'ny taratasy fanamarinana sy ny lohateny HTTP dia angonina rehefa mahomby ny fanamarinana ihany. Omeo ny fonosana CA mety ho an'ny tolotra mampiasa CA manokana. Ny tatitra taloha kokoa dia mety ahitana `cert_read_unverified`, izay tsy avoakan'ny fitsapana ankehitriny intsony.

Ny tsiambaratelo SNMP dia vakiana avy amin'ny fari-tontolo iainana na avy amin'ny rakitra ihany (`--snmp-*-file`, na ny fari-tontolo mifanandrify `HOSTCENSUS_SNMP_*_FILE`), tsy avy amin'ny sanda eo amin'ny andalana baiko velively, izay hitan'ny mpampiasa eo an-toerana hafa ao amin'ny lisitry ny fizotrana. Ny `--snmp-community`, `--snmp-auth-key` ary `--snmp-priv-key` misy sanda dia mivoaka amin'ny kaody 2 ary manonona ny fanoloana. Ny rakitra tsiambaratelo dia tsy maintsy UTF-8 tsy banga ary farafahabetsany 4096 bytes; odian-tsy hita ny fiverenana an-dalana iray any amin'ny farany, ary hadisoana ny fametrahana sady fari-tontolo no rakitra ho an'ny tsiambaratelo iray ihany. Ny hadisoana dia manonona ny rakitra fa tsy mamoaka ny ao anatiny velively. Ny tatitra fitarafana sy ny tantara dia tsy mampiditra niniana ny sandan'ny mari-pamantarana. Ny mpanondrana dia manana safidy mazava misaraka `--include-credentials` voalaza etsy ambany. Ny community iray dia misafidy SNMPv2c; ny mpampiasa iray dia misafidy SNMPv3, miaraka amin'ny fanamarinana rehefa omena fanalahidy auth ary fiarovana ny tsiambaratelo rehefa omena izy roa (`snmp_security_level` no mirakitra izany). Mandà ny hostcensus, miaraka amin'ny kaody fivoahana 2, ny hanambatra community sy mpampiasa v3, hampiasa fanalahidy privacy tsy misy fanalahidy auth, na hampiasa fanalahidy tsy misy mpampiasa, ary tsy manandrana indray mihitsy ny fanontaniana v3 tsy nahomby amin'ny v2c na ambaratonga fiarovana ambany kokoa. Ny mpandraharaha tsy mampiasa afa-tsy v1/v2c dia tsy miraharaha ny fitadiavana v3 tsy misy mari-pamantarana, ka miseho ho misokatra ihany izy ireo rehefa omena community.

Ny lahatsoratra faneva dia ahena ho soratra azo atonta ihany ary ferana ho soratra 256 alohan'ny itahirizana na anehoana azy. Voafetra koa ny famakiana: 4 KiB isaky ny andalana, 4 KiB ho an'ny fiarahabana MySQL, 16 KiB ho an'ny lohateny HTTP. Ny famantarana motera SNMP lava mihoatra ny 32 octets dia tapahina alohan'ny itahirizana azy. Ny HTTP sy HTTPS dia mandefa lohateny Host miaraka amin'ny adiresy IPv6 anaty fonon-teny efamira ary miaraka amin'ny seranana rehefa tsy 80 na 443 izany. Ny sela CSV manomboka amin'ny marika fampandehanana raikipohy tabilao dia asiana tovona mialoha mba hijanona ho lahatsoratra.

### Fetra

Ny fampandehanana iray dia manaiky adiresy 65,536, tolotra 64, ary fitsapana 524,288 (mpampiantrano ampitomboina amin'ny tolotra) farafahabetsany; ny fangatahana lehibe kokoa dia mivoaka amin'ny kaody 2 mialoha ny handefasana na inona na inona. Ny `--concurrency` dia ferana ho soketa 4096. Ny fitsapana tsirairay dia manana fe-potoana hentitra avo efatra heny noho ny teti-potoanany manokana. Ny fitsapana fifandraisana (`tcp`, `ssh`, `mysql`, `http`) dia mampiasa 0.3 segondra raha tsy mametraka `timeout` io tolotra io. Ny SNMP sy HTTPS dia mampiasa `--timeout` (mahazatra 1.0) rehefa tsy mametraka iray izy ireo. Ny fitsapana mahatratra ny fe-potoana dia tatitra ho `unknown` miaraka amin'ny "probe timed out" ao amin'ny `errors`. Ny tsy fahombiazan'ny soketa eo an-toerana (ohatra ny fahataperan'ny file descriptors) dia `unknown` koa miaraka amin'ny hadisoana voarakitra; tsy isaina velively ho seranana voasivana na mpampiantrano maty izy ireo. Mialoha ny fitsapana, ny hostcensus dia mampiakatra ny fetra malefaky ny rakitra misokatra mankany amin'ny fetra henjana mba hahafeno ny `--concurrency` miampy 64 descriptors; rehefa tsy vitany izany dia tsy mahomby ny fanamarinana mialoha `open files` ary mivoaka amin'ny kaody 1 ny `scan` mialoha ny handefasana fifamoivoizana. Ny fitadiavana Nmap dia mampiasa fe-potoana 30 segondra isaky ny mpampiantrano. Ny prefix iray dia ampitaina amin'ny nmap amin'ny endrika CIDR, ary tsy mahomby amin'ny kaody fivoahana 1 ny fitarafana rehefa mamoaka adiresy vitsy kokoa noho izay nomena azy ny nmap (ohatra anarana tsy voavahany) fa tsy manamarika ny mpampiantrano ho maty. Ny lasibatra anaran'ny mpampiantrano dia vahana indray mandeha ary omena ny nmap io adiresy io, ka tonga amin'ny milina iray ihany ny fitadiavana sy ny fitsapana. Ny prefix feno dia fizotrana nmap iray izay manana fe-potoanan'ny fizotrana zanak'asa 35 segondra isaky ny adiresy 256, boriboriana miakatra. Ny fitarafana misy fanilihana dia mampiasa andiany mpampiantrano 256 sy fe-potoana 35 segondra isaky ny andiany. Ny famoronana mpiasa dia voafetra tsy miankina amin'ny haben'ny faritra. Ny reverse DNS sy ny famahana anaran'ny mpampiantrano dia manana fe-potoana misaraka roa segondra; ny antso mpamaha tsy miverina mihitsy dia avela amin'ny kofehy fanatanterahany manokana, ka tsy afaka mitazona ny hostcensus handeha mihoatra ireo fetra ireo. Farafahabetsany 16 ny fikarohana mandeha indray mandeha, ary ny antso navela dia mitazona ny toerany mandra-piveriny, ka mijanona ho voafetra ny isan'ny kofehy voahidy; raha mihantona avokoa izy 16, ny fikarohana manaraka dia milahatra miandry toerana ivelan'ny fe-potoana roa segondra (izay manomboka rehefa misy toerana malalaka) mandra-piaton'ny `--deadline` ny fitarafana. Ny `NetworkScanner` ampiasaina ho tranomboky tsy misy `deadline` dia afaka miandry toerana toy izany tsy misy farany. Ny `--deadline` (mahazatra adiny iray) no mametra ny fampandehanana manontolo ambonin'ireo rehetra ireo.

### Fandrindrana ny tolotra

Azo ovaina amin'ny alalan'ny rakitra TOML ny tolotra:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

Ny `probe` dia iray amin'ny `tcp`, `ssh`, `mysql`, `http`, `https` na `snmp` ary mampiasa ny anaran'ny tolotra ho mahazatra rehefa fitsapana izany, na `tcp` raha tsy izany. Ny `snmp` ihany no mampiasa UDP. Ny anaran'ny tolotra dia litera madinika, isa, `-` ary `_`. Tsy afaka mizara seranana sy fifanarahana iray ny tolotra roa; mirakitra toetra iray ho an'io mpivady io ny tantara. Tsy voatery ny `timeout`, amin'ny segondra, ary farafahakeliny 0.05. Ny fitsapana karazana fifandraisana (`tcp`, `ssh`, `mysql`, `http`) dia mampiasa 0.3 segondra ho mahazatra. Ny `snmp` sy `https` dia mampiasa ny `--timeout` an'ny fitarafana rehefa tsy mametraka `timeout` ny tolotra. Tsy manolo ny teti-potoana efa ananan'ny tolotra ny `--timeout`.

Ny tatitra JSON dia antontan-taratasy misy kinova (`"format": "hostcensus-report"`, `"version": 1`) izay mirakitra ny lasibatra, ny tolotra notsapaina ary ny fandrindrana eo akaikin'ny `devices`; ny `--format json` tsy misy `-o` dia manoratra ny tatitra ao amin'ny stdout fa tsy ny tabilao. Ny vokatra JSON rehetra dia manana rafitra navoaka; jereo ny [Vokatra JSON](../../../docs/json-output.md). Ny fitaovana dia mitazona ny saha tany am-boalohany `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` ary `errors` ary manampy lisitra `services` miaraka amin'ny `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, na `unknown` rehefa tsy nahomby eo an-toerana na nahatratra ny fe-potoany ny fitsapana), `version` ary `details` an'ny fitsapana tsirairay. Ny vokatra CSV dia mahazo tsanganana farany `services` sy `versions` ho an'ireo misokatra. Ny sanda marina/diso `ssh`, `snmp` ary `mysql` dia manaraka ireo tolotra mitondra ireo anarana ireo indrindra.


## Mombamomba ny lisitra, fanamarinana mialoha, ary tantara eo an-toerana

Ny mombamomba misy anarana dia mizara rakitra TOML miaraka amin'ny famaritana `[services]` efa misy. Adikao ny [hostcensus.example.toml](../../../hostcensus.example.toml) ho `hostcensus.toml` ary apetraho ny tambajotra tantananao:

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

Ny `preflight` dia mamaha ny safidy sy mombamomba mitovy tanteraka amin'ny ataon'ny `scan`, anisan'izany ny `--concurrency` ho an'ny fanamarinana rakitra misokatra, ka ny fanamarinana mialoha mandalo dia midika fa hanomboka amin'ny drafitra mitovy ny `scan`.

Ny mombamomba dia manaiky `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency`, ary `max_hosts`. Ny `services` sy `ports` dia mampiasa ny fomba fanoratana lisitra sarahan'ny faingo efa misy. Ny safidy CLI voafaritra mazava dia manolo ny fandrindran'ny mombamomba; ny safidy `--exclude` miverimberina dia manampy amin'ny fanilihan'ny mombamomba. Ny tambajotra voafaritra mazava miaraka amin'ny `--profile` dia tsy maintsy ao anatin'ny faritra IP/CIDR an'io mombamomba io. Mbola tohanana ny anaran'ny mpampiantrano ho an'ny fitarafana mivantana, fa tsy azo atambatra amin'ny fanilihana IP. Ny fetran'ny mpampiantrano dia mihatra mialoha ny fanilihana; mbola mihatra aorian'izay ny fetra ankapobeny amin'ny fitsapana. Ny mpampiantrano voahilika dia esorina na amin'ny fanamarinana tolotra na amin'ny fitadiavana Nmap tsy voatery.

Ny fitarafana rehetra dia manao fanamarinana mialoha eo an-toerana alohan'ny fifamoivoizana mankany amin'ny lasibatra: fetran'ny lasibatra/fitsapana, fidirana amin'ny toerana fitehirizana, fisian'ny fitaovana/fonosana Nmap tsy voatery, rafitry ny tantara, ary fonosana TLS CA voarindra. Ny `preflight` dia mamoaka JSON ary tsy mitarika fitarafana lasibatra na mamorona tahiry tantara. Manoratra rakitra mpiray tam-po vonjimaika izy hanamarinana ny fidirana amin'ny toerana fitehirizana nefa tsy manova ny votoaty efa misy. Ny rafitra ao ambadika asyncio mahazatra dia mbola tsy mila na Nmap na zon'ny root. Ny lalan'ny toerana fitehirizana dia tsy maintsy samy hafa avokoa ary tsy mitovy amin'ny fandrindrana fampidirana, anisan'izany ny rohy mafy; lavina ny rohy an'ohatra amin'ny toerana fitehirizana. Ny fanamarinana tsy mahomby dia mamerina 1; ny sahan'asa/fandrindrana tsy manan-kery dia mamerina 2.

Ny fanoratana tatitra sy fanondranana dia mitaky fanohanana `O_NOFOLLOW`. Amin'ny rafitra tsy manana izany, anisan'izany ny Windows, tsy mahomby ireo fanoratana ireo nefa tsy manokatra na manapaka ny toerana fitehirizana. Ny tatitra sy soratra baiko fanondranana vaovao dia ho an'ny tompony ihany (maody 0600); ny fanoloana rakitra efa misy dia mitazona ny fahazoan-dalany. Ny fanoratana amin'ny fantsona misy anarana (named pipe) tsy misy mpamaky dia tsy mahomby avy hatrany fa tsy miandry. Ny tahiry `--history` vaovao dia foronina ho an'ny tompony ihany koa; ny efa misy dia mitazona ny maodiny. Ny hafatra fandraiketana dia mankany amin'ny stderr hatrany, ka vokatra ihany no entin'ny stdout. Ny fanondranana ahitana mari-pamantarana dia manery hatrany ny maody 0600.

Safidy ny tantara ary mameno ireo tahiry raikitra JSON efa misy sy ny baiko `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Ampiasao ny ID avy amin'ny `history`; ity ohatra ity dia mihevitra tahiry vaovao. Ny tahiry raikitra dia tehirizina amin'ny fifanakalozana voaaro miaraka amin'ny fotoana fanombohana/famaranana UTC, kinovan'ny fonosana, fandrindrana tsy miafina manan-kery, famintinana, ary ny fandinihana mpampiantrano/tolotra rehetra, anisan'izany ny hadisoana isaky ny mpampiantrano. Tazonina ny fandinihana mpampiantrano tsy feno. Tsy tehirizina ny fampandehanana nofoanana. Tazonina ireo fifanarahana efa misy momba ny tatitra, tahiry raikitra, fanondranana, ary kaody fivoahan'ny fitarafana.

Ny `history` dia mitanisa famintinana JSON nefa tsy mamaky ny angona fitaovana rehetra ao amin'ny tantara.
Ny `compare` dia mamaky fitarafana roa voatahiry, mitaky lasibatra sy seranana voafidy mitovy, ary mitatitra ny fiovan'ny famaliana, toetra, ary toetry ny seranana. Ny ID fitarafana taloha dia tsy maintsy mialoha ny ID taty aoriana. Rehefa samy nirakitra `timeout` na `backend` ny fitarafana roa ary samy hafa ireo sanda ireo, ny tatitra dia mitanisa fampitandremana fa mbola mampitaha ny fandinihana ihany. Ny fiandrasana hafa dia mety hahatonga ny seranana voasivana ho toa misokatra. Ny hadisoan'ny mpitarika fitarafana sy ny fandinihana seranana tsy fantatra dia marihina ho tsy azo antoka fa tsy raisina ho fanjavonana na fanakatonana voamarina: ny mpampiantrano misy hadisoana dia miseho ao amin'ny `uncertain_hosts`, ary ny fiovan'ny seranana rehetra ahitana `unknown` (anisan'izany ny tsy fantatra amin'ny fitarafana roa) dia voatanisa ao amin'ny `unconfirmed_ports` fa tsy ao amin'ny `port_changes`, afa-tsy ny seranana misokatra amin'ny fitarafana taty aoriana, izay fiovan'ny seranana. Ny `compare` sy `diff` dia manasokajy seranana amin'ny fitsipika mitovy. Ny `no_longer_responding` dia midika tsy fisian'ny valiny, fa tsy porofon'ny fanesorana fitaovana. Ny kaody fivoahana 0 an'ny fitarafana dia tsy miantoka fa namaly daholo ny mpampiantrano rehetra: jereo ny hadisoana isaky ny mpampiantrano. Ny fahombiazan'ny fampitahana dia mamerina 0 na misy fiovana na tsia; ny `diff` an-drakitra efa misy dia mitazona ny fifanarahany amin'ny kaody fivoahana 3. Ny tantara tsy tohanana na simba dia mamerina 1.

Ny tantara dia mitahiry fampahalalana momba ny lisitry ny tambajotra, ka misafidiana lahatahiry eo an-toerana voaaro araka ny tokony ho izy. Ny rakitra mombamomba sy ny fandrindrana voatahiry dia tsy ahitana mari-pamantarana SNMP; ny fitantanana mari-pamantarana dia mitohy amin'ny alalan'ny safidy fampandehanana/fari-tontolo iainana efa misy.

## Fampitahana lisitra

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Ny tahiry raikitra dia JSON misy `format: "hostcensus-snapshot"`, `version: 1`, ny kinovan'ny hostcensus, ny fotoana namoronana UTC, ny lasibatra, ny `timeout` sy `backend` an'ny fitarafana rehefa noraketin'ny fitarafana izany, ny tolotra notsapaina, ary ny mpampiantrano velona amin'ny endrika mitovy amin'ny tatitra `-o`. Avela tsy tafiditra ny mpampiantrano maty. Ny `diff` dia manaiky koa tatitra JSON `scan -o` tsotra, anisan'izany ireo tany alohan'ny nisian'ny saha `services`.

Ny `diff` dia mitatitra mpampiantrano vaovao sy nanjavona, seranana nisokatra na nihidy tamin'ny mpampiantrano hita tamin'izy roa, ary tolotra niova `version`. Ny seranana notsapaina tamin'ny iray amin'ireo fitarafana roa ihany dia tsy ampitahaina, ary milaza izany ny fampitandremana. Ny fandinihana tsy nahomby dia tsy vakiana velively ho "tsy misy fiovana": ny seranana izay `unknown` amin'ny iray amin'ny fitarafana roa ary tsy misokatra amin'ilay taty aoriana dia voatanisa eo ambanin'ny `unconfirmed`, fa tsy `closed`, miaraka amin'ny `before` ho `open`, `unknown` na `not-open` (notsapaina ka nihidy na voasivana) ary `after` ho `unknown` na `not-open`; ny seranana misokatra ankehitriny dia tatitra eo ambanin'ny `opened` na dia tsy nahomby aza ny fitsapana teo aloha. Ny mpampiantrano izay tsy nahomby daholo ny fitsapana taminy nefa tsy nahazo valiny tamin'ny iray amin'ny fitarafana roa dia voatanisa eo ambanin'ny `unsettled_hosts` (miaraka amin'ny `before`/`after` ho `up`, `uncertain` na `absent`, anisan'izany rehefa tsy nahomby tamin'izy roa na tsy hita tao amin'ny rakitra iray hafa) fa tsy `vanished_hosts`; raha mamaly izy tamin'ny fitarafana taty aoriana dia tatitra koa ho mpampiantrano vaovao miaraka amin'ny seranany misokatra. Mitazona ireo mpampiantrano tsy nahomby ireo ny tahiry raikitra noho izany antony izany. Miseho koa ny fampitandremana rehefa samy hafa ny lasibatra, ary rehefa samy nirakitra fe-potoana na rafitra ao ambadika ny rakitra roa ary samy hafa ireo sanda ireo. Ny `-o PATH` dia manoratra ny endrika JSON amin'ny rakitra koa.

Ny tatitra avy amin'ny fitarafana najanon'ny `--deadline` (`"complete": false`) dia tsy mitanisa afa-tsy ny mpampiantrano tratrany, ka mandà azy ny `diff` sy `export` miaraka amin'ny kaody fivoahana 2. Manaiky azy ny `--allow-partial` miaraka amin'ny fampitandremana ao amin'ny stderr: ny `diff` avy eo dia mitanisa ireo mpampiantrano tsy voatanisa mihitsy tamin'ny fitarafana tsy feno eo ambanin'ny `unsettled_hosts` ho `unscanned` fa tsy nanjavona (ny mpampiantrano notanisainy ho maty dia mbola nanjavona ihany), mametraka `partial` ho marina ary tsy mitatitra velively hoe tsy misy fiovana, ary ny `export` dia manoratra fampitandremana ao amin'ny lohatenin'ny soratra baiko.

Kaody fivoahan'ny `diff`: `0` tsy misy fiovana, `3` hita ny fiovana, fandinihana tsy voamarina, na fampidirana tsy feno (marina ny `changed` isaky ny misy lisitra tsy banga, anisan'izany ny `unsettled_hosts` sy `unconfirmed`, na marina ny `partial`), `2` misy rakitra tsy hita, tsy azo vakiana, tsy tahiry raikitra tohanana, na tsy feno tsy misy `--allow-partial`, `1` tsy azo nosoratana ny rakitra `-o`.

## Fanondranana Kadupul

Ny [Kadupul](https://github.com/kadupulhq/kadupul) (sampana avy amin'ny Cacti 1.2.31) dia tsy manana fanafarana fitaovana maro indray mandeha avy amin'ny rakitra. Ny fomba tohanany hanampiana fitaovana avy amin'ny soratra baiko dia `cli/add_device.php`, fitaovana iray isaky ny antso, miaraka amin'ny tondro `--option=value`. Ny `hostcensus export` dia manoratra soratra baiko POSIX `sh` ahitana ireo antso ireo:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Ny mpampiantrano velona tsirairay dia lasa `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Ny mpampiantrano izay nahomby ny fanontaniana SNMP tamin'ny fitarafana dia mahazo `--version=2 --community=...` na `--version=3 --username=... --authproto=... --password=...` (miampy `--privproto`/`--privpass` ho an'ny authPriv), `--port` ary `--avail=snmp`. Ny fanondranana SNMPv3 dia mila `--snmp-user`, ary lavina ny noAuthNoPriv satria mitaky tenimiafina v3 ny `add_device.php`.
- Ny mpampiantrano hafa dia mahazo `--version=0 --avail=ping`, miaraka amin'ny `--ping_method=tcp --ping_port=` ny seranana TCP misokatra voalohany, na ICMP raha tsy misy.
- Ny `--notes` dia mitanisa ny tolotra misokatra sy ny kinovany. Ny `--description` dia ny anarana reverse-DNS rehefa tsotra (litera, isa, `.`, `_`, `-`), na ny IP raha tsy izany, ary atao tokana tsy misy mitovy, satria ny `add_device.php` dia mandray ny famaritana efa misy ho fanavaozana an'io fitaovana io.

Ny sanda tsirairay dia hamarinina ary arovan'ny mari-tsoratra shell amin'ny alalan'ny `shlex.quote`. Amin'ny fomba mahazatra dia tsy misy tsiambaratelo SNMP soratana: ny soratra baiko dia manitatra `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` na `HOSTCENSUS_SNMP_PRIV_KEY` mandritra ny fampandehanana ary mijanona raha misy iray tsy voafaritra. Ny `--include-credentials` dia manoratra ny sanda avy amin'ireo fari-tontolo iainana ireo ao anatin'ny soratra baiko, mamorona azy amin'ny maody 0600, ary mirakitra fampitandremana. Ny `add_device.php` tenany dia mamoaka ny community ary mandray tsiambaratelo ho tondro, izay hita maso ao amin'ny lisitry ny fizotrana ao amin'ny lohamilina Kadupul mandritra ny fandehan'ny antso tsirairay.

Mivoaka amin'ny kaody 1 ny `add_device.php` raha misy dika mitovy sy hadisoana; manohy ny soratra baiko, manisa ny tsy fahombiazana, ary mivoaka amin'ny kaody 1 raha nisy fitaovana tsy tafiditra. Ny ID modely dia avy amin'ny `php cli/add_device.php --list-host-templates`. Kaody fivoahan'ny `export`: `0` voasoratra, `2` fampidirana tsy azo vakiana, fitarafana tsy feno tsy misy `--allow-partial`, na angona tsy azo aondrana am-pilaminana, `1` tsy azo nosoratana ny soratra baiko.

## Fanomezana kinova sy dingana famoahana

Manaraka ny [Semantic Versioning](https://semver.org/spec/v2.0.0.html) ny hostcensus: ny fanamboarana mifanentana dia mampitombo ny kinova patch, ny endri-javatra/fanesorana miandalana mifanentana dia mampitombo ny kinova minor, ary ny fiovana manapaka ny fifanentanana dia mampitombo ny kinova major. Ny baiko sy safidy, ny kaody fivoahana ary ny rafitra JSON no fifanarahana ho an'ny besinimaro; ny fihetsika efa hoesorina miandalana dia mitohy miasa hatramin'ny famoahana lehibe manaraka, raha tsy misy fanamboarana fiarovana mitaky fanovana aloha kokoa (ny tantaran'ny fiovana no manazava ny antony).

Ny release-please dia manokatra PR famoahana avy amin'ny lohateny Conventional Commit ao amin'ny `main`, mampiakatra ny `pyproject.toml`, `uv.lock` ary `CHANGES.md`. Ny fampitambarana azy dia mamorona ny marika `vMAJOR.MINOR.PATCH` sy volavola famoahana GitHub, izay ampian'ny CI fonosana wheel voasedra, fizarana loharano ary checksums; ny GitHub dia mitahiry fanamarinana fanamboarana ho an'ireo rakitra ireo amin'ny alalan'ny API fanamarinana azy. Mpanara-maso iray no mijery sy mamoaka ny volavola rehefa tafiditra ny rakitra. Tsy soloina velively ny famoahana.

Safidy ny famoahana azo itokisana PyPI ary mitaky fananana tetikasa, mpamoaka azo itokisana ary ny tontolo `pypi`. Mamoaka ireo vokatra famoahana voamarina ireo ihany izy nefa tsy manamboatra indray na mitahiry marika API. Ny famoahana misy marika ato amin'ity tahiry ho an'ny besinimaro ity dia mamorona fanamarinana vokatra GitHub; ny sampana manokana dia mitaky drafitra tohanana sy safidy mazava. Jereo ny [torolalana feno momba ny famoahana](../../../docs/releasing.md) ho an'ny fanamboarana, baiko mazava ary fanandramana indray.

## Fampandrosoana

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Mipetraka ao amin'ny vondrona fiankinana [PEP 735](https://peps.python.org/pep-0735/) ao amin'ny `pyproject.toml` (`dev`, `fuzz`, `build`) ny fitaovana fampandrosoana, ka tsy miseho velively ao amin'ny angona fonosana navoaka. Ny `uv.lock` no rakitra fanidiana tokana; mametraka amin'ny `uv sync --locked` ny CI ary tsy mahomby rehefa lany andro ny rakitra fanidiana. Safidio ny mpandika teny miaraka amin'ny `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), na izay Python 3.12+.

Mampihatra fetra ambany 90% amin'ny fandrakofana fitsapana fonosana ny CI. Ny fitsapana singa dia ahitana lohamilina loopback voafehy sy tranga fanamarinana mombamomba/tantara/famoahana tsy mila tambajotra; ny laboratoara Compose dia mampandeha OpenSSH, MariaDB, nginx ary net-snmp amin'ny tetezana mitokana. Alefaso amin'ny `make test-integration` izany. Jereo ny [CONTRIBUTING.md](../../../CONTRIBUTING.md) sy ny [fitaovana famoahana](../../../scripts/README.md).

Ny kaontenera fampandehanana dia mandeha amin'ny UID/GID 10001 tsy misy lahatahiry fandraisana, tsy misy fidirana shell ary tsy misy pip, ary afaka manoratra ao amin'ny `/app/output`. Omeo alalana hanoratra ao amin'ny lahatahiry vokatra ampidirina io mpampiasa io. Tsy mila fahafaha-manao manokana izy ary miasa amin'ny rafitra rakitra fototra vakiana ihany, ka azo alefa toy izao:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Mampiasa ny fihetsika fitadiavana TCP tsy mila tombontsoa manokana ny Nmap ao anatin'ity kaontenera ity. Mampiato ny fanamboarana sary ny CI raha misy fahalemena ara-piarovana HIGH na CRITICAL azo ahitsy taterin'ny Trivy.

## Fanamarinana ny rojo famatsiana

Mandeha ao amin'ny main sy isan-kerinandro ny [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool), mamoaka ny naotiny tena izy, ary mampakatra ny vokatra ao amin'ny fitarafana kaody GitHub. Ny actions sy fototry ny kaontenera dia raikitra amin'ny alalan'ny hash tsy miova; vahana ao amin'ny `uv.lock` ny fiankinana Python. Mampiato ny CI ny tsy fahombiazan'ny Bandit, ary ny fitsapana kisendrasendra Atheris voafetra dia mitsapa ny mpamaky SSH, MySQL, HTTP, taratasy fanamarinana ary SNMPv3 BER tsy mila fidirana tambajotra.

Mandrefy ihany koa ny tantaran'ny famerenana kaody, ny fahasamihafan'ny mpandray anjara, ary ny fiavian'ny famoahana ny Scorecard. Maneho porofo tena izy ireo naoty ireo; tsy filazana izany fa feno avokoa ny fanamarinana fitantanana na famoahana taloha rehetra. Jereo ny [SECURITY.md](../../../SECURITY.md) sy ny [fiavian'ny famoahana](../../../docs/releasing.md).

## Fampifanarahana amin'ny fiteny

Ny hafatra CLI sy ny tabilao famintinana/fampitahana amin'ny terminal dia manohana fiteny 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) nefa tsy mila fiankinana fampandehanana fanampiny. Ny famahana fiteny dia manaja ny `--lang`, avy eo `LC_ALL`, `LC_MESSAGES`, ary `LANG`, ary miverina amin'ny `en` raha tsy hita. Tsy miova ny rafitra JSON, ny tsanganana CSV, ary ny soratra baiko fanondranana amin'ny fiteny rehetra.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Fandraisana anjara

Ny fandraisana anjara dia tokony ahitana tranga azo averina, mitazona ny fifanarahana CLI sy endrika angona voarakitra, ary mandalo ireo fanamarinana kalitao etsy ambony. Jereo ny [CONTRIBUTING.md](../../../CONTRIBUTING.md) ho an'ny fizotran'ny fampandrosoana ary [ny torolalana momba ny famoahana](../../../docs/releasing.md) ho an'ny fanapahan-kevitra momba ny fifanentanana sy ny fanomezana kinova.

## Fiarovana sy toetry ny fahazoan-dalana

Jereo ny [SECURITY.md](../../../SECURITY.md) ho an'ny tatitra manokana sy ny kinova tohanana.
Ny hostcensus dia eo ambanin'ny [Fahazoan-dalana MIT](../../../LICENSE).

Mampiasa famantarana SPDX ny lohatenin'ny loharano ary mitazona ny fankasitrahana mpandray anjara avy amin'ny tantaran'ny Git. Jereo ny [AUTHORS.md](../../../AUTHORS.md) ho an'ny fankasitrahana. Ny rakitra fitsapana binary sy ny rakitra fanidiana vokarina dia mampiasa rakitra `.license` eo akaikiny; ao amin'ny `LICENSES/MIT.txt` ny lahatsoratry ny MIT.
