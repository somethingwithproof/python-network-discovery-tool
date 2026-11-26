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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · **Kiswahili** · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus ni zana ya CLI ya Python ya ukaguzi wa huduma unaoweza kurudiwa kwenye mitandao unayosimamia.
Inarekodi kile ambacho vifaa vinaonyesha, inalinganisha uchunguzi baada ya muda, na inazalisha
hati za uingizaji za Kadupul. Sehemu ya nyuma ya chaguomsingi hutumia soketi za asyncio bila ruhusa ya root;
ugunduzi wa hiari wa Nmap unaweza kutambua hosti nje ya bandari za huduma zilizosanidiwa.

## Kwa nini hostcensus

Ripoti ya bandari ya mara moja haielezi ikiwa uchunguzi unaofuata ulibadilika au
ulishindwa tu. hostcensus inachanganya hali dhahiri za huduma, uchunguzi wenye mipaka, wasifu wa
uchanganuzi unaoweza kutumika tena, na historia ya ndani. Waendeshaji wanaweza kurudia wigo uleule, kukagua
hitilafu, na kutofautisha uchunguzi usio na uhakika na mabadiliko yaliyothibitishwa.

- **Ushahidi wa huduma:** Utambulisho wa SSH, salamu za MySQL, vichwa vya HTTP, uchunguzi wa
  vyeti vya TLS, na ugunduzi wa SNMP au maulizo yenye vitambulisho vya system-MIB.
- **Wigo unaoweza kurudiwa:** wasifu wa TOML wenye majina, vighairi vinavyoongezeka, huduma zinazoweza kusanidiwa,
  vikomo vya hosti/uchunguzi, na wafanyakazi wenye mipaka.
- **Ukaguzi kabla ya trafiki:** ukaguzi wa awali wa ndani huthibitisha shabaha, zana, ufikiaji wa
  lengwa, muundo wa historia, na vifurushi vya TLS CA vilivyosanidiwa.
- **Historia ya orodha:** picha za haraka za miamala za SQLite huhifadhi uchunguzi wote;
  ulinganisho huweka hitilafu za kichanganuzi na hali zisizojulikana zikionekana.
- **Toleo linaloshirikiana:** ripoti za terminal, JSON na CSV, picha za faili zenye matoleo,
  na hati za uingizaji za Kadupul.

CI inashughulikia Python 3.12, 3.13 na 3.14 kwenye Linux na macOS, pamoja na maabara ya ujumuishaji
ya Compose iliyodhibitiwa. Msimbo unatumia lakabu za aina za kisasa, matokeo ya ukaguzi wa awali yenye aina,
wasifu wa neno-msingi pekee wenye nafasi maalum na usafishaji wa async uliopangwa huku ukidumisha
matoleo hayo ya utekelezaji. Tazama [Upangaji wa matoleo na utoaji](../../../docs/releasing.md) kwa mkataba wa uoanifu
wa SemVer na mchakato wa toleo la GitHub. Beji ya toleo inaelezea
vizalia vilivyochapishwa, si nakala ya sasa ya msimbo: lebo ya hivi karibuni iliyochapishwa kwa sasa ni
`v0.3.0`, ilhali nakala hii ya msimbo inatumia toleo la kifurushi `3.0.0`. Sakinisha kutoka kwenye nakala hii ya msimbo
ili kutumia vipengele vya orodha vilivyoandikwa hapa.

Anza na [usakinishaji](#install), kisha [wasifu na historia](#inventory-profiles-preflight-and-local-history).
Kwa maelezo ya ujumuishaji, tazama [alama za vidole za huduma](#fingerprints),
[ulinganisho wa faili](#inventory-diff), na [uhamishaji wa Kadupul](#kadupul-export).

<a name="install"></a>

## Usakinishaji

Python 3.12 au mpya zaidi inahitajika; Python 3.12 hadi 3.14 ndiyo orodha iliyokaguliwa. Kutoka kwenye
nakala hii ya msimbo, sakinisha vitegemezi vilivyofungwa vya utekelezaji:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Kwa ugunduzi wa hiari wa hosti wa Nmap, sakinisha faili tekelezi ya Nmap kwa kutumia kidhibiti cha vifurushi
cha mfumo wako; hakuna kifurushi cha ziada cha Python kinachohitajika. Toleo la XML la Nmap huchanganuliwa kwa
defusedxml, kitegemezi cha msingi, kwa hivyo upanuzi wa huluki hukataliwa. hostcensus huendesha
`nmap` inayopatikana kwenye `PATH` moja kwa moja na orodha ya hoja iliyowekwa, muda wa mwisho unaoongezeka
kulingana na ukubwa wa kiambishi awali, na kikomo cha toleo la 64 MiB. Nmap haihitajiki kwa sehemu ya nyuma ya chaguomsingi.

## Kuhama kutoka netprobe

hostcensus ni jina jipya la netprobe, lililotolewa katika 3.0.0. Mradi haujawahi
kuchapishwa kwenye PyPI chini ya jina lolote, kwa hivyo usakinishaji ulitoka kwenye nakala ya msimbo au toleo la GitHub.
Hazina ya GitHub inabaki na jina lake.

| Ilikuwa | Sasa | Uoanifu |
| --- | --- | --- |
| Usambazaji `netprobe` | `hostcensus` | Sakinisha tena kutoka kwenye nakala ya msimbo; hakuna kifurushi chenye jina la zamani. |
| Amri `netprobe` | `hostcensus` | `netprobe` bado inaendeshwa na huchapisha mstari mmoja wa onyo la kuachwa kutumika kwenye stderr. Misimbo ya kutoka na stdout hazijabadilika. Itaondolewa katika toleo kuu lijalo. |
| Vigezo vya mazingira `NETPROBE_*` | `HOSTCENSUS_*` | Kigezo cha `NETPROBE_*` hutumiwa wakati pacha wake `HOSTCENSUS_*` haujawekwa, kikiwa na onyo moja kwenye stderr linalotaja majina ya vigezo na kamwe si thamani zake. `HOSTCENSUS_*` huchukuliwa kwanza wakati vyote viwili vimewekwa. Itaondolewa katika toleo kuu lijalo. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Inavunja uoanifu.** Hakuna kiunganishi cha muda cha kuingiza kilichosakinishwa; sasisha uingizaji. |
| Lebo ya picha ya Docker `network-discovery:test` (CI pekee) na mtumiaji wa kontena `netprobe` | `hostcensus:test`, mtumiaji `hostcensus` | Hakuna picha ya sajili iliyowahi kuchapishwa. Jenga picha tena na utumie sehemu ya kuingilia ya `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Faili iliyopo yenye jina la chaguomsingi la zamani bado hutumiwa, kukiwa na onyo, wakati jina jipya halipo. Njia dhahiri za `--config` na `--history` haziguswi. |
| Ripoti na picha za haraka zenye `"format": "netprobe-report"` au `"netprobe-snapshot"`, na sehemu ya `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` na `export` bado hupakia faili zilizoandikwa chini ya jina la zamani, na Miundo ya JSON iliyochapishwa hukubali tahajia zote mbili. Faili mpya hutumia majina mapya. Hifadhidata za historia za SQLite hazijabadilika na hupakia kama awali. |
| Hati za Kadupul kutoka `netprobe export` | Hati kutoka `hostcensus export` | Hati za zamani huendelea kufanya kazi na bado husoma `NETPROBE_SNMP_*` zinapoendeshwa. Hati mpya husoma `HOSTCENSUS_SNMP_*`. |

## Mfano wa haraka

Endesha kutoka kwenye kontena la majaribio la maabara ya ujumuishaji iliyoelezwa chini ya Uendelezaji; matokeo yamefupishwa:

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

## Misimbo ya kutoka

| Amri | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | uchunguzi/ripoti imerekodiwa | ukaguzi wa awali/sehemu ya nyuma, historia, au uandishi wa ripoti/picha ya haraka umeshindwa | shabaha, chaguo, usanidi, au vikomo batili | - | `--deadline` imefikiwa; ripoti ya sehemu imeandikwa, historia na picha ya haraka zimerukwa |
| `preflight` | ukaguzi umefaulu | ukaguzi wa ndani umeshindwa | shabaha/usanidi batili au lengwa zinazokinzana | - | - |
| `profiles` | wasifu uliothibitishwa umeorodheshwa | - | usanidi au uteuzi usiosomeka/batili | - | - |
| `history` | muhtasari umeorodheshwa | historia haipo, ni batili, au haitumiki | chaguo za CLI batili | - | - |
| `compare` | ulinganisho umetolewa, ikiwa ni pamoja na wakati mabadiliko yapo | historia isiyosomeka, wigo/mpangilio usiooana, au kushindwa kuandika | chaguo za CLI batili | - | - |
| `diff` | hakuna mabadiliko | faili ya `-o` haikuweza kuandikwa | ingizo halipo, halisomeki au halitumiki, au uchanganuzi usio kamili bila `--allow-partial` | mabadiliko yamepatikana, uchunguzi usio na uhakika, au uchanganuzi usio kamili | - |
| `export` | hati imeandikwa | hati haikuweza kuandikwa | ingizo lisilosomeka, uchanganuzi usio kamili bila `--allow-partial`, au data isiyoweza kuhamishwa kwa usalama | - | - |

## Mpangilio

| Moduli | Jukumu |
| --- | --- |
| `cli.py` | Chaguo za amri, utatuzi wa wasifu, ukaguzi wa awali, uchanganuzi na kuripoti |
| `scanner.py`, `probes.py` | Upanuzi wa shabaha, wafanyakazi wenye mipaka, ugunduzi wa hosti na uchunguzi wa huduma |
| `config.py`, `profiles.py` | Ufafanuzi wa huduma na wasifu wa orodha uliothibitishwa |
| `models.py`, `output.py` | Aina za matokeo na uonyeshaji wa terminal/JSON/CSV |
| `history.py`, `diff.py` | Historia ya SQLite na ulinganisho wa picha za faili zenye matoleo |
| `preflight.py` | Ukaguzi wa ndani na utafutaji wa toleo la Nmap wenye mipaka |
| `export.py` | Hati za uingizaji za Kadupul zilizothibitishwa na kuwekewa alama za nukuu |

Kila uchunguzi wa huduma hurekodi hali yake kando na utambulisho wake uliotangazwa.
Usomaji na muda wa mwisho una mipaka; vighairi vya uchunguzi hubaki katika hitilafu za hosti. Historia ya
SQLite hutumia miamala, usafishaji dhahiri wa miunganisho, na njia za kuorodhesha na
kulinganisha za kusoma pekee. Siri za SNMP huingia tu kupitia vigezo vya mazingira au faili
za siri; historia ya orodha huhifadhi mipangilio inayofanya kazi isiyo ya siri. Tazama
[Usanifu](../../../docs/architecture.md) kwa mtiririko wa uchanganuzi, vikomo vyake na mipaka ya
uaminifu, na [SECURITY.md](../../../SECURITY.md#authorized-use) kwa matumizi yaliyoidhinishwa.


## Matumizi

Changanua mitandao unayosimamia pekee.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Chaguo | Maana |
| --- | --- |
| `NETWORK` | CIDR, IP, au jina la hosti; ya hiari na `--profile`. Vitambulisho vya wigo wa IPv6 hukataliwa. |
| `-o, --output PATH` | Andika ripoti. Umbizo hufuata kiendelezi (`.json`, `.csv`); viendelezi vingine hurudi kwenye JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Lazimisha umbizo la ripoti. Haina athari bila `--output`. `.sh` huchagua `kadupul`. |
| `-v, --verbose` | Kurekodi kumbukumbu za utatuzi. |
| `-q, --quiet` | Zima matokeo, maendeleo na kumbukumbu za taarifa; maonyo na hitilafu bado huonekana kwenye stderr. |
| `--backend asyncio\|nmap` | Ugunduzi wa hosti. `asyncio` (chaguomsingi) huchunguza bandari za huduma moja kwa moja; `nmap` huendesha uchanganuzi wa ping wa nmap kwanza na huhitaji faili tekelezi ya `nmap` kwenye `PATH`. |
| `--timeout SECONDS` | Subiri uchunguzi ambao haujaweka bajeti yake wenyewe (chaguomsingi 1.0). Uchunguzi wa muunganisho uliojengewa ndani hutumia 0.3s isipokuwa jedwali la huduma liweke `timeout`. |
| `--concurrency N` | Uchunguzi unaoendeshwa kwa wakati mmoja (chaguomsingi 256). |
| `--deadline SECONDS` | Simamisha uchanganuzi mzima, pamoja na uchanganuzi wa nmap, baada ya muda huu (chaguomsingi 3600, usizidi 604800; kigezo cha mazingira `HOSTCENSUS_DEADLINE`). Hosti zilizokamilika huandikwa kwenye ripoti zikiwa na `"complete": false`, hakuna historia au picha ya haraka inayoandikwa, na `scan` hutoka na msimbo 4. |
| `--config PATH` | Ufafanuzi wa huduma wa TOML na mipangilio ya hiari yenye majina ya `[profiles]`. |
| `--profile NAME` | Tumia wasifu wenye jina; chaguomsingi ni `hostcensus.toml` wakati `--config` imeachwa. |
| `--exclude IP/CIDR` | Ongeza kighairi; rudia inavyohitajika. Hosti ya IPv4 iliyotengwa pia hutenga anwani za IPv6 zinazoifikia: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) na 6to4. Shabaha na vighairi vya IPv4-mapped huchukuliwa kama anwani za IPv4 zinazoashiria. |
| `--max-hosts N` | Kikomo cha anwani kinachokaguliwa kabla ya vighairi (chaguomsingi/kiwango cha juu kabisa 65,536). |
| `--history PATH` | Rekodi uchanganuzi uliokamilika katika hifadhidata ya hiari ya historia ya SQLite. |
| `--services NAMES` | Orodha iliyotenganishwa kwa mkato ya majina ya huduma ya kukagua, kwa mpangilio huo (chaguomsingi: zote). |
| `--ports SPEC` | Orodha iliyotenganishwa kwa mkato ya `NAME=PORT` (hamisha huduma) au `PORT` (ongeza ukaguzi wa kawaida wa TCP uitwao `tcp-PORT`). |
| `--snmp-community-file PATH` | Faili yenye jumuiya ya SNMPv2c kwa ajili ya ulizo la MIB ya mfumo. Kigezo cha mazingira: `HOSTCENSUS_SNMP_COMMUNITY` (thamani) au `HOSTCENSUS_SNMP_COMMUNITY_FILE` (njia). |
| `--snmp-user` | Mtumiaji wa SNMPv3. Kigezo cha mazingira: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (chaguomsingi), `SHA224`, `SHA256`, `SHA384`, `SHA512` na faili yenye nenosiri. Kigezo cha mazingira: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` au `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (chaguomsingi), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` na faili yenye nenosiri. Kigezo cha mazingira: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` au `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Pia andika picha ya haraka yenye toleo kwa ajili ya `hostcensus diff`. |
| `--tls-ca-file PATH` | Thibitisha vyeti vya HTTPS dhidi ya kifurushi hiki cha PEM badala ya hifadhi ya mfumo. Kigezo cha mazingira: `HOSTCENSUS_TLS_CA_FILE`. |

Kwa chaguomsingi kila hosti hukaguliwa kwa SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) na HTTPS (TCP 443). Bandari za TCP hukaguliwa kwa muunganisho kamili. SNMP hukaguliwa kwa ombi la ugunduzi wa injini ya SNMPv3, ambalo wakala yeyote wa SNMPv3 lazima ajibu bila vitambulisho; mawakala wanaozungumza v1/v2c pekee hawatagunduliwa na uchunguzi huu. Kwa sehemu ya nyuma ya asyncio hosti huhesabiwa kuwa hai wakati uchunguzi wowote unapopata jibu, ikiwa ni pamoja na muunganisho uliokataliwa, kwa hivyo hosti inayotupa kila uchunguzi ina `alive=false` na hitilafu "Host is down"; hii haithibitishi kuwa imezimwa kimwili. Kwa `--backend nmap`, nmap huamua ni hosti zipi ziko hai (ICMP kama root, TCP 80/443 vinginevyo).

<a name="fingerprints"></a>

### Alama za vidole

Kila huduma iliyo wazi huchukuliwa alama ya kidole kutokana na kile inachotuma kabla ya kuingia. Hakuna kinachothibitisha utambulisho isipokuwa ulizo la SNMP, na tu unapotoa vitambulisho.

| Uchunguzi | Husoma | `version` | funguo za `details` |
| --- | --- | --- | --- |
| `ssh` | Mstari wa utambulisho wa RFC 4253 | programu, k.m. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Kupeana mikono kwa awali kwa MySQL/MariaDB | toleo la seva | `server_version`, `flavor`, `auth_plugin`, au `error_code`/`error` |
| `http` | Jibu la `HEAD /` | kichwa cha `Server` | `status`, `server` |
| `https` | Kupeana mikono kwa TLS, cheti, `HEAD /` | kichwa cha `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Ugunduzi wa SNMPv3; kwa vitambulisho, GET ya sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; kwa vitambulisho `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, au `snmp_error` |

Shabaha ya jina la hosti hutatuliwa mara moja kwa kila hosti na kila uchunguzi huunganisha kwenye anwani hiyo, iliyorekodiwa kama `address` katika matokeo; jina hutumiwa tu kwa TLS SNI, uthibitishaji wa cheti na kichwa cha HTTP `Host`. Jina lisilotatulika hutoa hali za `unknown` na hitilafu ya `Cannot resolve`. Majina ya Reverse DNS huhifadhiwa tu yanapokuwa na herufi za jina la hosti, na utafutaji usiozidi 16 huendeshwa kwa wakati mmoja. HTTPS hutumia uthibitishaji wa cheti na jina la hosti dhidi ya hifadhi ya mfumo au `--tls-ca-file`. Hifadhi ya uaminifu hupakiwa mara moja kwa uchanganuzi na kutumika tena kwa kila uchunguzi wa HTTPS. Muunganisho wa TCP na kupeana mikono kwa TLS huhesabiwa muda kando, kwa hivyo bandari inayokubali miunganisho lakini ikakwama wakati wa kupeana mikono ni `open` yenye `tls_error`, si `filtered`. Uthibitishaji ukishindwa, matokeo hurekodi `cert_verified: false` na `cert_verify_error`; haijaribu tena kwa mipangilio dhaifu au kutuma ombi la HTTP. Maelezo ya cheti na vichwa vya HTTP hukusanywa tu baada ya uthibitishaji kufaulu. Toa kifurushi sahihi cha CA kwa huduma za CA ya kibinafsi. Ripoti za zamani zinaweza kuwa na `cert_read_unverified`, ambayo uchunguzi wa sasa hautoi tena.

Siri za SNMP husomwa tu kutoka kwa vigezo vya mazingira au kutoka kwa faili (`--snmp-*-file`, au kigezo kinacholingana cha `HOSTCENSUS_SNMP_*_FILE`), kamwe si kutoka kwa thamani za mstari wa amri, ambazo watumiaji wengine wa ndani wanaweza kuziona kwenye orodha ya michakato. `--snmp-community`, `--snmp-auth-key` na `--snmp-priv-key` zenye thamani hutoka na msimbo 2 na kutaja mbadala. Faili ya siri lazima iwe UTF-8 isiyo tupu ya si zaidi ya baiti 4096; mstari mmoja mpya wa mwisho hupuuzwa, na kuweka kigezo na faili kwa siri hiyohiyo ni hitilafu. Hitilafu hutaja faili lakini kamwe hazichapishi maudhui yake. Ripoti za uchanganuzi na historia hazijumuishi thamani za vitambulisho kimakusudi. Zana ya uhamishaji ina chaguo tofauti na dhahiri la `--include-credentials` lililoelezwa hapa chini. Jumuiya huchagua SNMPv2c; mtumiaji huchagua SNMPv3, kukiwa na uthibitishaji wakati ufunguo wa auth unatolewa na faragha wakati funguo zote mbili zinatolewa (`snmp_security_level` hurekodi ni ipi). hostcensus hukataa, na msimbo wa kutoka 2, kuchanganya jumuiya na mtumiaji wa v3, kutumia ufunguo wa faragha bila ufunguo wa auth, au kutumia funguo bila mtumiaji, na haijaribu kamwe kurudia ulizo la v3 lililoshindwa kwa kutumia v2c au kiwango cha chini cha usalama. Mawakala wanaozungumza v1/v2c pekee hupuuza ugunduzi wa v3 usio na vitambulisho, kwa hivyo huonekana kuwa wazi tu wakati jumuiya inatolewa.

Maandishi ya bango hupunguzwa hadi herufi zinazochapishika na kuwekewa kikomo cha herufi 256 kabla ya kuhifadhiwa au kuonyeshwa. Usomaji pia una mipaka: 4 KiB kwa kila mstari, 4 KiB kwa salamu ya MySQL, 16 KiB ya vichwa vya HTTP. Kitambulisho cha injini ya SNMP kirefu kuliko okteti 32 hukatwa kabla ya kuhifadhiwa. HTTP na HTTPS hutuma kichwa cha Host chenye anwani ya IPv6 ndani ya mabano ya mraba na chenye bandari wakati si 80 au 443. Seli za CSV zinazoanza na kichocheo cha fomula ya lahajedwali huwekewa kiambishi awali ili seli ibaki kuwa maandishi.

### Vikomo

Uendeshaji mmoja hukubali anwani zisizozidi 65,536, huduma 64, na uchunguzi 524,288 (hosti zikizidishwa na huduma); maombi makubwa zaidi hutoka na msimbo 2 kabla ya chochote kutumwa. `--concurrency` ina kikomo cha soketi 4096. Kila uchunguzi una muda wa mwisho mkali wa mara nne ya bajeti yake mwenyewe. Uchunguzi wa muunganisho (`tcp`, `ssh`, `mysql`, `http`) hutumia sekunde 0.3 isipokuwa huduma hiyo iweke `timeout`. SNMP na HTTPS hutumia `--timeout` (chaguomsingi 1.0) wakati hazijaweka moja. Uchunguzi unaofikia muda wa mwisho huripotiwa kama `unknown` ukiwa na "probe timed out" katika `errors`. Kushindwa kwa soketi za ndani (kwa mfano kuishiwa na vifafanuzi vya faili) pia ni `unknown` kukiwa na hitilafu iliyorekodiwa; kamwe hakuhesabiwi kama bandari iliyochujwa au hosti iliyozimwa. Kabla ya kuchunguza, hostcensus huinua kikomo laini cha faili wazi kuelekea kikomo kigumu ili kutoshea `--concurrency` pamoja na vifafanuzi 64; isipoweza, ukaguzi wa awali wa `open files` hushindwa na `scan` hutoka 1 kabla ya kutuma trafiki. Ugunduzi wa Nmap hutumia muda wa mwisho wa hosti wa sekunde 30. Kiambishi awali hupitishwa kwa nmap katika umbo la CIDR, na uchanganuzi hushindwa na kutoka 1 wakati nmap inaripoti anwani chache kuliko ilizopewa (kwa mfano jina lisiloweza kutatuliwa) badala ya kuweka alama kuwa hosti zimezimwa. Shabaha ya jina la hosti hutatuliwa mara moja na nmap hupewa anwani hiyo, ili ugunduzi na uchunguzi ufikie mashine ileile. Kiambishi awali kamili ni mchakato mmoja wa nmap ambao muda wake wa mwisho wa mchakato mdogo ni sekunde 35 kwa kila anwani 256, zikikadiriwa juu. Uchanganuzi wenye vighairi hutumia mafungu ya hosti 256 na muda wa mwisho wa sekunde 35 kwa kila fungu. Uundaji wa wafanyakazi una mipaka bila kutegemea ukubwa wa masafa. Reverse DNS na utatuzi wa jina la hosti vina muda tofauti wa mwisho wa sekunde mbili; wito wa kitatuzi ambao haurudi kamwe huachwa kwenye uzi wake wenyewe, ili usiendelee kuiweka hostcensus ikifanya kazi kupita vikomo hivi. Utafutaji usiozidi 16 huendeshwa kwa wakati mmoja, na wito ulioachwa hushikilia nafasi yake hadi urudi, kwa hivyo idadi ya nyuzi zilizokwama hubaki na mipaka; ikiwa zote 16 zitakwama, utafutaji unaofuata husubiri foleni kwa nafasi nje ya muda wa mwisho wa sekunde mbili (ambao huanza mara tu nafasi inapopatikana) hadi `--deadline` isimamishe uchanganuzi. `NetworkScanner` ikitumika kama maktaba bila `deadline` inaweza kusubiri nafasi kama hiyo bila kikomo. `--deadline` (chaguomsingi saa moja) huweka kikomo kwa uendeshaji wote juu ya hivi.

### Kusanidi huduma

Huduma zinaweza kubadilishwa kwa kutumia faili ya TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` ni mojawapo ya `tcp`, `ssh`, `mysql`, `http`, `https` au `snmp` na chaguomsingi ni jina la huduma wakati hilo ni uchunguzi, vinginevyo `tcp`. `snmp` pekee ndiyo hutumia UDP. Majina ya huduma ni herufi ndogo, tarakimu, `-` na `_`. Huduma mbili haziwezi kushiriki bandari na itifaki; historia hurekodi hali moja kwa jozi hiyo. `timeout` ni ya hiari, katika sekunde, na angalau 0.05. Uchunguzi wa mtindo wa muunganisho (`tcp`, `ssh`, `mysql`, `http`) chaguomsingi ni sekunde 0.3. `snmp` na `https` hutumia `--timeout` ya uchanganuzi wakati huduma haijaweka `timeout`. `--timeout` haibadilishi bajeti ambayo huduma tayari inayo.

Ripoti za JSON ni nyaraka zenye matoleo (`"format": "hostcensus-report"`, `"version": 1`) zinazorekodi shabaha, huduma zilizochunguzwa na mipangilio karibu na `devices`; `--format json` bila `-o` huandika ripoti kwenye stdout badala ya jedwali. Kila toleo la JSON lina muundo uliochapishwa; tazama [Toleo la JSON](../../../docs/json-output.md). Vifaa huhifadhi sehemu za awali za `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` na `errors` na kuongeza orodha ya `services` yenye `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, au `unknown` wakati uchunguzi ulishindwa ndani au ulifikia muda wake wa mwisho), `version` na `details` za kila uchunguzi. Toleo la CSV hupata safuwima za mwisho za `services` na `versions` kwa zile zilizo wazi. Thamani za boolean za `ssh`, `snmp` na `mysql` hufuata huduma zenye majina hayo hasa.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Wasifu wa orodha, ukaguzi wa awali, na historia ya ndani

Wasifu wenye majina hushiriki faili ya TOML na ufafanuzi uliopo wa `[services]`. Nakili
[hostcensus.example.toml](../../../hostcensus.example.toml) kwenye `hostcensus.toml` na uweke mitandao
unayosimamia:

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

`preflight` hutatua chaguo na wasifu sawasawa kabisa na `scan`, ikijumuisha
`--concurrency` kwa ukaguzi wa faili wazi, kwa hivyo ukaguzi wa awali unaofaulu unamaanisha `scan`
itaanza na mpango uleule.

Wasifu hukubali `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, na `max_hosts`. `services` na `ports` hutumia sintaksia iliyopo ya orodha
iliyotenganishwa kwa mkato. Chaguo dhahiri za CLI hubatilisha mipangilio ya wasifu; chaguo za `--exclude`
zinazorudiwa huongeza kwenye vighairi vya wasifu. Mtandao dhahiri ulio na `--profile` lazima uwe
ndani ya wigo wa IP/CIDR wa wasifu huo. Majina ya hosti yanaendelea kutumika kwa uchanganuzi wa moja kwa moja,
lakini hayawezi kuunganishwa na vighairi vya IP. Vikomo vya hosti hutumika kabla ya
vighairi; kikomo cha jumla cha uchunguzi bado kinatumika baadaye. Hosti zilizotengwa
huachwa kutoka kwa ukaguzi wa huduma na ugunduzi wa hiari wa Nmap.

Kila uchanganuzi hufanya ukaguzi wa awali wa ndani kabla ya trafiki ya shabaha: vikomo vya shabaha/uchunguzi,
ufikiaji wa lengwa, upatikanaji wa faili tekelezi/kifungaji cha hiari cha Nmap, muundo wa historia,
na kifurushi cha TLS CA kilichosanidiwa. `preflight` huripoti JSON na haichanganui
shabaha wala kuunda hifadhidata ya historia. Huandika kwa muda faili jirani ili kujaribu
ufikiaji wa lengwa bila kubadilisha maudhui yaliyopo. Sehemu ya nyuma ya chaguomsingi ya asyncio
bado haihitaji Nmap wala root. Njia za lengwa lazima ziwe tofauti na kila
moja na kutoka kwa usanidi wa ingizo, ikiwa ni pamoja na viungo vigumu; viungo vya ishara vya lengwa
hukataliwa. Ukaguzi ulioshindwa hurudisha 1; wigo/usanidi batili hurudisha 2.

Uandishi wa ripoti na uhamishaji huhitaji usaidizi wa `O_NOFOLLOW`. Kwenye mifumo isiyo na usaidizi huo,
ikiwa ni pamoja na Windows, uandishi huu hushindwa bila kufungua au kukata lengwa.
Ripoti mpya na hati za uhamishaji ni za mmiliki pekee (hali 0600); kubadilisha faili iliyopo huhifadhi
ruhusa zake. Kuandika kwenye bomba lenye jina bila msomaji hushindwa mara moja badala ya kusubiri. Hifadhidata mpya ya `--history` pia huundwa kwa mmiliki pekee; iliyopo huhifadhi hali yake. Ujumbe wa kumbukumbu huenda kwenye stderr kila wakati, kwa hivyo stdout hubeba matokeo pekee. Uhamishaji ulio na vitambulisho hulazimisha hali 0600 kila wakati.

Historia ni ya hiari na inakamilisha picha za haraka za JSON zilizopo na amri ya `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Tumia vitambulisho kutoka `history`; mfano unachukulia hifadhidata mpya. Picha za haraka huhifadhiwa
kimuamala zikiwa na nyakati za kuanza/mwisho za UTC, toleo la kifurushi, mipangilio inayofanya kazi isiyo ya siri,
muhtasari, na uchunguzi wote wa hosti/huduma, ikijumuisha hitilafu za kila hosti.
Uchunguzi wa hosti usio kamili huhifadhiwa. Uendeshaji ulioghairiwa hauhifadhiwi. Mikataba iliyopo ya
ripoti, picha ya haraka, uhamishaji, na misimbo ya kutoka ya uchanganuzi huhifadhiwa.

`history` huorodhesha muhtasari wa JSON bila kusoma mizigo yote ya kihistoria ya vifaa.
`compare` husoma uchanganuzi mbili zilizohifadhiwa, huhitaji utambulisho sawa wa shabaha na bandari
zilizochaguliwa, na huripoti uitikiaji, hali, na mabadiliko ya hali ya bandari. Kitambulisho cha
uchanganuzi wa awali lazima kitangulie kitambulisho cha baadaye. Wakati uchanganuzi zote mbili zilirekodi `timeout` au `backend`
na thamani hizo zinatofautiana, ripoti huorodhesha onyo na bado inalinganisha
uchunguzi. Muda tofauti wa kusubiri unaweza kufanya bandari iliyochujwa ionekane wazi. Hitilafu za kichanganuzi
na uchunguzi wa bandari usiojulikana huwekewa alama kama usio na uhakika badala ya kuchukuliwa kama
kutoweka au kufungwa kulikothibitishwa: hosti zenye hitilafu huonekana katika `uncertain_hosts`, na
kila mpito wa bandari unaohusisha `unknown` (ikiwa ni pamoja na kutojulikana katika uchanganuzi zote mbili) huorodheshwa
katika `unconfirmed_ports` badala ya `port_changes`, isipokuwa bandari iliyo wazi katika uchanganuzi wa
baadaye, ambayo ni badiliko la bandari. `compare` na `diff` huainisha bandari kwa sheria hiyohiyo.
`no_longer_responding` inamaanisha ukosefu wa jibu, si uthibitisho wa kuondolewa kwa kifaa.
Msimbo wa kutoka wa uchanganuzi 0 hauhakikishi kila hosti ilijibu: kagua hitilafu za kila hosti. Kufaulu kwa ulinganisho hurudisha 0 iwe mabadiliko yapo au la; `diff` ya faili iliyopo
huhifadhi mkataba wake wa msimbo wa kutoka 3. Historia isiyotumika au iliyoharibika hurudisha 1.

Historia huhifadhi taarifa za orodha, kwa hivyo chagua saraka ya ndani iliyolindwa ipasavyo.
Faili za wasifu na mipangilio iliyohifadhiwa haina vitambulisho vya SNMP;
ushughulikiaji wa vitambulisho huendelea kupitia chaguo/mazingira yaliyopo ya wakati wa utekelezaji.

<a name="inventory-diff"></a>

## Tofauti ya orodha

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Picha ya haraka ni JSON yenye `format: "hostcensus-snapshot"`, `version: 1`, toleo la hostcensus, muda wa kuundwa wa UTC, shabaha, `timeout` na `backend` za uchanganuzi wakati uchanganuzi ulizirekodi, huduma zilizochunguzwa, na hosti zilizo hai katika umbo lilelile kama ripoti ya `-o`. Hosti zilizozimwa huachwa nje. `diff` pia hukubali ripoti za kawaida za JSON za `scan -o`, ikiwa ni pamoja na zile za kabla ya sehemu ya `services` kuwepo.

`diff` huripoti hosti mpya na zilizotoweka, bandari zilizofunguka au kufungwa kwenye hosti zilizopo katika zote mbili, na huduma ambazo `version` yazo ilibadilika. Bandari zilizochunguzwa katika mojawapo tu ya uchanganuzi mbili hazilinganishwi, na onyo husema hivyo. Uchunguzi ulioshindwa hausomwi kamwe kama "hakuna mabadiliko": bandari ambayo ni `unknown` katika uchanganuzi wowote na haiko wazi katika ule wa baadaye huorodheshwa chini ya `unconfirmed`, si `closed`, ikiwa na `before` ya `open`, `unknown` au `not-open` (ilichunguzwa na ikafungwa au kuchujwa) na `after` ya `unknown` au `not-open`; bandari iliyo wazi sasa huripotiwa chini ya `opened` hata kama uchunguzi wa awali ulishindwa. Hosti ambayo uchunguzi wake wote ulishindwa bila jibu katika uchanganuzi wowote huorodheshwa chini ya `unsettled_hosts` (ikiwa na `before`/`after` ya `up`, `uncertain` au `absent`, ikiwa ni pamoja na iliposhindwa katika uchanganuzi zote mbili au haipo kwenye faili nyingine) badala ya `vanished_hosts`; ikijibu katika uchanganuzi wa baadaye pia huripotiwa kama hosti mpya pamoja na bandari zake zilizo wazi. Picha za haraka huhifadhi hosti hizo zilizoshindwa kwa sababu hii. Onyo pia huonekana wakati shabaha zinatofautiana, na wakati faili zote mbili zilirekodi muda wa mwisho au sehemu ya nyuma na thamani hizo zinatofautiana. `-o PATH` huandika umbo la JSON kwenye faili pia.

Ripoti kutoka kwa uchanganuzi uliosimamishwa na `--deadline` (`"complete": false`) huorodhesha tu hosti ilizofikia, kwa hivyo `diff` na `export` huikataa kwa msimbo wa kutoka 2. `--allow-partial` huikubali ikiwa na onyo kwenye stderr: `diff` kisha huorodhesha hosti ambazo uchanganuzi usio kamili haukuorodhesha kabisa chini ya `unsettled_hosts` kama `unscanned` badala ya kutoweka (hosti iliyoorodheshwa kama iliyozimwa bado imetoweka), huweka `partial` kuwa true na kamwe hairipoti hakuna mabadiliko, na `export` huandika onyo kwenye kichwa cha hati.

Misimbo ya kutoka ya `diff`: `0` hakuna mabadiliko, `3` mabadiliko yamepatikana, uchunguzi ambao haukuweza kuthibitishwa, au ingizo lisilo kamili (`changed` ni true wakati wowote orodha yoyote, ikiwa ni pamoja na `unsettled_hosts` na `unconfirmed`, si tupu, au `partial` ni true), `2` faili haipo, haisomeki, si picha ya haraka inayotumika, au si kamili bila `--allow-partial`, `1` faili ya `-o` haikuweza kuandikwa.

<a name="kadupul-export"></a>

## Uhamishaji wa Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (tawi la Cacti 1.2.31) haina uingizaji wa faili za vifaa kwa wingi. Njia yake inayotumika kuongeza vifaa kutoka kwa hati ni `cli/add_device.php`, kifaa kimoja kwa kila wito, kikiwa na hoja za `--option=value`. `hostcensus export` huandika hati ya POSIX `sh` ya miito hiyo:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Kila hosti iliyo hai huwa `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hosti ambazo ulizo lao la SNMP la uchanganuzi lilifaulu hupata `--version=2 --community=...` au `--version=3 --username=... --authproto=... --password=...` (pamoja na `--privproto`/`--privpass` kwa authPriv), `--port` na `--avail=snmp`. Uhamishaji wa SNMPv3 huhitaji `--snmp-user`, na noAuthNoPriv hukataliwa kwa sababu `add_device.php` huhitaji nenosiri la v3.
- Hosti nyingine hupata `--version=0 --avail=ping`, kukiwa na `--ping_method=tcp --ping_port=` bandari ya kwanza ya TCP iliyo wazi, au ICMP ikiwa hakuna.
- `--notes` huorodhesha huduma zilizo wazi na matoleo. `--description` ni jina la reverse-DNS linapokuwa wazi (herufi, tarakimu, `.`, `_`, `-`), vinginevyo IP, na hufanywa la kipekee, kwa sababu `add_device.php` huchukulia maelezo yaliyopo kama sasisho kwa kifaa hicho.

Kila thamani huthibitishwa na kuwekewa alama za nukuu za shell kwa kutumia `shlex.quote`. Kwa chaguomsingi hakuna siri ya SNMP inayoandikwa: hati hupanua `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` au `HOSTCENSUS_SNMP_PRIV_KEY` wakati wa utekelezaji na kusimama ikiwa moja haijawekwa. `--include-credentials` huandika thamani kutoka kwa vigezo hivyo vya mazingira kwenye hati badala yake, huunda hati hiyo kwa hali 0600, na hurekodi onyo. `add_device.php` yenyewe huchapisha jumuiya na hupokea siri kama hoja, ambazo huonekana kwenye orodha ya michakato ya seva ya Kadupul wakati kila wito unaendeshwa.

`add_device.php` hutoka na msimbo 1 kwa nakala rudufu na hitilafu; hati huendelea, huhesabu kushindwa, na hutoka 1 ikiwa kifaa chochote hakikuongezwa. Vitambulisho vya kiolezo hutoka kwa `php cli/add_device.php --list-host-templates`. Misimbo ya kutoka ya `export`: `0` imeandikwa, `2` ingizo lisilosomeka, uchanganuzi usio kamili bila `--allow-partial`, au data isiyoweza kuhamishwa kwa usalama, `1` hati haikuweza kuandikwa.

## Upangaji wa matoleo na mchakato wa toleo

hostcensus hufuata [Semantic Versioning](https://semver.org/spec/v2.0.0.html): marekebisho yanayooana
huongeza toleo la viraka (patch), vipengele/maonyo ya kuacha kutumika yanayooana huongeza
toleo dogo (minor), na mabadiliko yanayovunja uoanifu huongeza toleo kuu (major).
Amri na chaguo, misimbo ya kutoka na miundo ya JSON ni mkataba wa umma;
tabia iliyoachwa kutumika huendelea kufanya kazi hadi toleo kuu lijalo, isipokuwa
marekebisho ya usalama yahitaji kuibadilisha mapema (kumbukumbu ya mabadiliko kisha hueleza kwa nini).

release-please hufungua PR ya toleo kutoka kwa vichwa vya Conventional Commit kwenye `main`,
ikipandisha `pyproject.toml`, `uv.lock` na `CHANGES.md`. Kuiunganisha huunda
lebo ya `vMAJOR.MINOR.PATCH` na rasimu ya toleo la GitHub, ambapo CI huambatanisha gurudumu
lililokaguliwa, usambazaji wa msimbo chanzo na jumla za ukaguzi; GitHub huhifadhi uthibitisho wa ujenzi kwa
faili hizo kupitia API yake ya uthibitisho. Msimamizi hukagua na kuchapisha
rasimu mara tu faili zinapoambatanishwa. Matoleo hayabadilishwi kamwe.

Uchapishaji unaoaminika wa PyPI ni wa hiari na huhitaji umiliki wa mradi, mchapishaji
anayeaminika na mazingira ya `pypi`. Huchapisha vizalia vilevile vya toleo vilivyokaguliwa
bila kujenga tena au kuhifadhi tokeni ya API. Matoleo yenye lebo katika hazina hii ya umma
huzalisha uthibitisho wa vizalia vya GitHub; matawi ya kibinafsi huhitaji mpango
unaotumika na kujiunga dhahiri. Tazama
[mwongozo kamili wa toleo](../../../docs/releasing.md) kwa usanidi, amri halisi na marudio.

## Uendelezaji

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Zana za uendelezaji ziko katika vikundi vya vitegemezi vya [PEP 735](https://peps.python.org/pep-0735/)
katika `pyproject.toml` (`dev`, `fuzz`, `build`), kwa hivyo hazionekani kamwe katika
metadata ya kifurushi kilichochapishwa. `uv.lock` ndiyo faili pekee ya kufunga; CI husakinisha kwa
`uv sync --locked` na hushindwa wakati faili ya kufunga imepitwa na wakati. Chagua mkalimani kwa
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), au Python 3.12+ yoyote.

CI hutekeleza kiwango cha chini cha 90% cha ufunikaji wa kifurushi. Majaribio ya vitengo yanajumuisha seva za loopback
zilizodhibitiwa na kesi za wasifu/historia/kithibitishaji-toleo za nje ya mtandao; maabara ya Compose huendesha
OpenSSH, MariaDB, nginx na net-snmp kwenye daraja lililotengwa. Iendeshe kwa
`make test-integration`. Tazama [CONTRIBUTING.md](../../../CONTRIBUTING.md) na
[zana za toleo](../../../scripts/README.md).

Kontena la utekelezaji huendeshwa kama UID/GID 10001 bila saraka ya nyumbani, bila kuingia kwa shell
na bila pip, na linaweza kuandika kwenye `/app/output`. Mpe mtumiaji huyo ruhusa ya kuandika kwenye
saraka yoyote ya toleo iliyopachikwa. Halihitaji uwezo wowote na hufanya kazi na
mfumo wa faili wa root wa kusoma pekee, kwa hivyo linaweza kuendeshwa kama:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap hutumia tabia yake ya ugunduzi wa TCP isiyo na upendeleo katika kontena hili. CI husababisha
ujenzi wa picha kushindwa kwa udhaifu wowote wa HIGH au CRITICAL unaoweza kurekebishwa ambao Trivy huripoti.

## Ukaguzi wa mnyororo wa ugavi

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
huendeshwa kwenye main na kila wiki, huchapisha alama yake halisi, na kupakia matokeo kwenye uchanganuzi
wa msimbo wa GitHub. Vitendo na misingi ya kontena imefungwa kwa hashi zisizobadilika; vitegemezi vya Python
hutatuliwa katika `uv.lock`. Hitilafu za Bandit husababisha CI kushindwa, na upimaji wa Atheris
wenye mipaka hujaribu vichanganuzi vya SSH, MySQL, HTTP, cheti na SNMPv3 BER
bila ufikiaji wa mtandao.

Scorecard pia hupima shughuli za ukaguzi wa kihistoria, utofauti wa wachangiaji, na
asili ya toleo. Alama hizo huakisi ushahidi halisi; si madai
kwamba kila ukaguzi wa utawala au toleo la kihistoria umetimizwa. Tazama
[SECURITY.md](../../../SECURITY.md) na [asili ya toleo](../../../docs/releasing.md).

## Ujanibishaji

Ujumbe wa CLI na majedwali ya muhtasari/tofauti ya terminal hutumia lugha 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) bila vitegemezi vyovyote vya ziada vya wakati wa utekelezaji. Utatuzi huheshimu `--lang`, kisha `LC_ALL`, `LC_MESSAGES`, na `LANG`, ukirudi kwenye `en`. Miundo ya JSON, safuwima za CSV, na hati za uhamishaji hubaki bila kubadilika katika lugha zote.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Kuchangia

Michango inapaswa kujumuisha kesi inayoweza kurudiwa, kuhifadhi mikataba iliyoandikwa ya CLI na
umbizo la data, na kufaulu ukaguzi wa ubora hapo juu. Tazama
[CONTRIBUTING.md](../../../CONTRIBUTING.md) kwa mtiririko wa kazi wa uendelezaji na
[mwongozo wa toleo](../../../docs/releasing.md) kwa maamuzi ya uoanifu na matoleo.

## Hali ya usalama na leseni

Tazama [SECURITY.md](../../../SECURITY.md) kwa kuripoti kwa faragha na matoleo yanayotumika.
hostcensus ina leseni chini ya [Leseni ya MIT](../../../LICENSE).

Vichwa vya chanzo hutumia vitambulisho vya SPDX na kuhifadhi sifa za wachangiaji kutoka kwa historia ya Git.
Tazama [AUTHORS.md](../../../AUTHORS.md) kwa utambuzi. Rekodi za majaribio ya jozi na
faili ya kufunga iliyozalishwa hutumia faili jirani za `.license`; maandishi ya MIT yako katika `LICENSES/MIT.txt`.
