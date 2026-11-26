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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · **Hausa** · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus kayan aikin layin umarni (CLI) ne na Python don maimaita lissafin sabis a kan cibiyoyin sadarwar da kuke gudanarwa.
Yana rikodin abin da na'urori ke buɗewa, yana kwatanta sakamakon lura a tsawon lokaci, kuma yana ƙirƙirar
rubutun shigarwa na Kadupul. Tsarin baya na tsoho yana amfani da soket ɗin asyncio ba tare da izinin root ba;
binciken Nmap na zaɓi yana iya gano na'urori fiye da tashoshin sabis da aka saita.

## Me ya sa hostcensus

Rahoton tasha na lokaci ɗaya ba ya bayyana ko lura ta gaba ta canza ne ko
kawai ta gaza. hostcensus yana haɗa bayyanannun yanayin sabis, gwaje-gwaje masu iyaka, tsarin
bincike da za a iya sake amfani da su, da tarihi na gida. Masu gudanarwa na iya maimaita iyaka ɗaya, bincika
kurakurai, kuma su bambance lura marar tabbas daga canje-canjen da aka tabbatar.

- **Shaidar sabis:** tantancewar SSH, gaisuwar MySQL, kanun HTTP, lura da takardar shaidar
  TLS, da gano SNMP ko tambayoyin system-MIB masu shaidar shiga.
- **Iyaka mai maimaituwa:** tsarin bincike na TOML masu suna, keɓewa mai ƙaruwa, sabis masu
  saitawa, iyakokin na'urori/gwaje-gwaje, da ma'aikata masu iyaka.
- **Bincike kafin aika bayanai:** gwajin kafin farawa na gida yana tantance manufofi, kayan aiki, damar
  shiga wurin ajiya, tsarin tarihi, da kunshin TLS CA da aka saita.
- **Tarihin lissafi:** hotunan SQLite masu ma'amala suna adana duk abubuwan da aka lura;
  kwatance-kwatance suna ci gaba da nuna gazawar mai bincike da yanayin da ba a sani ba.
- **Fitowar bayanai masu dacewa da juna:** rahotannin tashar umarni, JSON da CSV, hotunan fayil masu siga,
  da rubutun shigarwa na Kadupul.

CI tana rufe Python 3.12, 3.13 da 3.14 a kan Linux da macOS, tare da ɗakin gwajin haɗin gwiwa na Compose
mai sarrafawa. Lambar tana amfani da laƙabin nau'i na zamani, sakamakon gwajin kafin farawa mai nau'i,
tsarin bincike masu rami na kalmar maɓalli kawai da tsaftacewar async mai tsari yayin da take riƙe waɗannan
sigogin aiki. Duba [Sigogi da fitarwa](../../../docs/releasing.md) don yarjejeniyar dacewar SemVer
da tsarin fitarwa na GitHub. Alamar fitarwa tana bayyana
kayan da aka buga ne, ba kwafin ajiya ba: alamar da aka buga ta ƙarshe a halin yanzu ita ce
`v0.3.0`, yayin da wannan kwafin ke amfani da sigar fakiti `3.0.0`. Shigar daga kwafin ajiyar
don amfani da fasalullukan lissafi da aka rubuta a nan.

Fara da [shigarwa](#install), sannan [tsarin bincike da tarihi](#inventory-profiles-preflight-and-local-history).
Don cikakkun bayanai na haɗin gwiwa, duba [alamun gane sabis](#fingerprints),
[kwatanta fayiloli](#inventory-diff), da [fitarwa zuwa Kadupul](#kadupul-export).

<a name="install"></a>

## Shigarwa

Ana buƙatar Python 3.12 ko sabuwa; Python 3.12-3.14 ita ce rukunin da aka gwada. Daga wannan
kwafin ajiyar, shigar da abubuwan dogaro na aiki da aka kulle:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Don gano na'urori da Nmap na zaɓi, shigar da fayil ɗin aiwatarwa na Nmap ta amfani da manajan fakitin
tsarin ku; ba a buƙatar ƙarin fakitin Python. Ana fassara fitowar XML ta Nmap da
defusedxml, wani muhimmin abin dogaro, don haka ana ƙin faɗaɗa mahallai. hostcensus yana gudanar da
`nmap` da aka samu a kan `PATH` kai tsaye tare da tsayayyen jerin hujjoji, wa'adi da ke ƙaruwa
tare da girman prefix, da iyakar fitowa ta 64 MiB. Ba a buƙatar Nmap don tsarin baya na tsoho.

## Ƙaura daga netprobe

hostcensus shine sabon sunan netprobe, wanda aka fitar a 3.0.0. Ba a taɓa
buga aikin zuwa PyPI a ƙarƙashin kowane suna ba, don haka shigarwa ta fito ne daga kwafin ajiya ko fitarwar
GitHub. Ma'ajiyar GitHub tana riƙe sunanta.

| Da | Yanzu | Dacewa |
| --- | --- | --- |
| Rarrabawar `netprobe` | `hostcensus` | Sake shigarwa daga kwafin ajiyar; babu fakitin tsohon suna. |
| Umarnin `netprobe` | `hostcensus` | `netprobe` har yanzu yana aiki kuma yana buga layin sanarwar daina tallafawa ɗaya a stderr. Lambobin fita da stdout ba su canza ba. Za a cire shi a babbar fitarwa ta gaba. |
| Masu canjin muhalli `NETPROBE_*` | `HOSTCENSUS_*` | Ana amfani da mai canjin `NETPROBE_*` idan ba a saita takwaransa `HOSTCENSUS_*` ba, tare da gargaɗin stderr guda ɗaya wanda ke ambaton sunayen masu canjin ba ƙimarsu ba. `HOSTCENSUS_*` yana rinjaye idan aka saita duka biyun. Za a cire shi a babbar fitarwa ta gaba. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Mai karya dacewa.** Ba a shigar da hanyar shigo da tsohon suna ba; sabunta shigo da fayiloli. |
| Alamar hoton Docker `network-discovery:test` (CI kawai) da mai amfani na kwantena `netprobe` | `hostcensus:test`, mai amfani `hostcensus` | Ba a taɓa buga hoton rajista ba. Sake gina hoton kuma yi amfani da wurin shiga na `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Har yanzu ana amfani da fayil ɗin da ke da tsohon sunan tsoho, tare da gargaɗi, muddin sabon sunan bai wanzu ba. Takamaiman hanyoyin `--config` da `--history` ba su taɓu ba. |
| Rahotanni da hotunan lokaci masu `"format": "netprobe-report"` ko `"netprobe-snapshot"`, da filin `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` da `export` har yanzu suna loda fayilolin da aka rubuta da tsohon sunan, kuma JSON Schemas da aka buga suna karɓar haruffan biyu. Sabbin fayiloli suna amfani da sabbin sunaye. Rumbun tarihin SQLite ba su canza ba kuma suna loda kamar da. |
| Rubutun Kadupul daga `netprobe export` | Rubutu daga `hostcensus export` | Tsoffin rubutun suna ci gaba da aiki kuma har yanzu suna karanta `NETPROBE_SNMP_*` lokacin da suke gudu. Sabbin rubutu suna karanta `HOSTCENSUS_SNMP_*`. |

## Misali mai sauri

Ana gudanarwa daga kwantenan gwaji na ɗakin gwajin haɗin gwiwa da aka bayyana a ƙarƙashin Haɓakawa; an rage fitowar:

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

## Lambobin fita

| Umarni | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | an yi rikodin lura/rahoto | gazawar gwajin kafin farawa/tsarin baya, tarihi, ko rubuta rahoto/hoton lokaci | manufa, zaɓuɓɓuka, saiti, ko iyakoki marasa inganci | - | an kai `--deadline`; an rubuta rahoton rabi, an tsallake tarihi da hoton lokaci |
| `preflight` | gwaje-gwaje sun wuce | gwajin gida ya gaza | manufa/saiti mara inganci ko wuraren ajiya masu cin karo | - | - |
| `profiles` | an jera tsarin bincike da aka tantance | - | saiti ko zaɓi mara karantuwa/mara inganci | - | - |
| `history` | an jera taƙaitawa | tarihi ya ɓace, mara inganci, ko ba a tallafa masa ba | zaɓuɓɓukan CLI marasa inganci | - | - |
| `compare` | an samar da kwatance, har da lokacin da canje-canje suka wanzu | tarihi mara karantuwa, iyaka/tsari mara dacewa, ko gazawar rubutu | zaɓuɓɓukan CLI marasa inganci | - | - |
| `diff` | babu canje-canje | ba za a iya rubuta fayil ɗin `-o` ba | shigarwa da ta ɓace, mara karantuwa ko ba a tallafa mata ba, ko binciken da bai cika ba ba tare da `--allow-partial` ba | an sami canje-canje, lura marasa tabbaci, ko binciken da bai cika ba | - |
| `export` | an rubuta rubutun | ba za a iya rubuta rubutun ba | shigarwa mara karantuwa, binciken da bai cika ba ba tare da `--allow-partial` ba, ko bayanan da ba za a iya fitar da su cikin aminci ba | - | - |

## Tsarin fayiloli

| Kundi | Nauyi |
| --- | --- |
| `cli.py` | Zaɓuɓɓukan umarni, warware tsarin bincike, gwajin kafin farawa, bincike da ba da rahoto |
| `scanner.py`, `probes.py` | Faɗaɗa manufa, ma'aikata masu iyaka, gano na'urori da lura da sabis |
| `config.py`, `profiles.py` | Bayanan sabis da tsarin binciken lissafi da aka tantance |
| `models.py`, `output.py` | Nau'o'in sakamako da fitar da tashar umarni/JSON/CSV |
| `history.py`, `diff.py` | Tarihin SQLite da kwatanta hotunan fayil masu siga |
| `preflight.py` | Gwaje-gwajen gida da neman sigar Nmap mai iyaka |
| `export.py` | Rubutun shigarwa na Kadupul da aka tantance kuma aka sanya alamar magana |

Kowace lura da sabis tana rikodin yanayinta daban da shaidar da yake nunawa.
Karatu da wa'adi suna da iyaka; kurakuran gwaji suna kasancewa a cikin kurakuran na'ura. Tarihin SQLite
yana amfani da ma'amaloli, tsaftacewar haɗi a bayyane, da hanyoyin jera bayanai da
kwatantawa na karatu kawai. Sirrikan SNMP suna shiga ne kawai ta hanyar masu canjin muhalli ko fayilolin
sirri; tarihin lissafi yana adana saitunan da ba na sirri ba masu aiki. Duba
[Tsarin gine-gine](../../../docs/architecture.md) don tsarin binciken, iyakokinsa da iyakokin
amincewa, da [SECURITY.md](../../../SECURITY.md#authorized-use) don amfani mai izini.


## Amfani

Bincika cibiyoyin sadarwar da kuke gudanarwa kawai.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Zaɓi | Ma'ana |
| --- | --- |
| `NETWORK` | CIDR, IP, ko sunan na'ura; na zaɓi tare da `--profile`. Ana ƙin masu gano iyaka na IPv6. |
| `-o, --output PATH` | Rubuta rahoto. Tsarin yana bin ƙarin sunan fayil (`.json`, `.csv`); sauran ƙarin sunaye suna komawa ga JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Tilasta tsarin rahoto. Ba shi da tasiri ba tare da `--output` ba. `.sh` yana zaɓar `kadupul`. |
| `-v, --verbose` | Rikodin gyara kuskure. |
| `-q, --quiet` | Ɓoye sakamako, ci gaba da rikodin bayanai; gargaɗi da kurakurai har yanzu suna bayyana a stderr. |
| `--backend asyncio\|nmap` | Gano na'urori. `asyncio` (tsoho) yana gwada tashoshin sabis kai tsaye; `nmap` yana gudanar da binciken ping na nmap da farko kuma yana buƙatar fayil ɗin aiwatarwa na `nmap` a kan `PATH`. |
| `--timeout SECONDS` | Jira gwaje-gwajen da ba su saita kasafin lokacinsu ba (tsoho 1.0). Gwaje-gwajen haɗi da aka gina suna amfani da 0.3s sai dai idan teburin sabis ya saita `timeout`. |
| `--concurrency N` | Gwaje-gwajen da ke gudana a lokaci guda (tsoho 256). |
| `--deadline SECONDS` | Dakatar da dukan binciken, har da binciken nmap, bayan wannan lokacin (tsoho 3600, mafi yawa 604800; muhalli `HOSTCENSUS_DEADLINE`). Ana rubuta na'urorin da suka kammala a cikin rahoton da `"complete": false`, ba a rubuta tarihi ko hoton lokaci ba, kuma `scan` yana fita da 4. |
| `--config PATH` | Bayanan sabis na TOML da saitunan `[profiles]` masu suna na zaɓi. |
| `--profile NAME` | Yi amfani da tsarin bincike mai suna; yana komawa ga `hostcensus.toml` idan aka bar `--config`. |
| `--exclude IP/CIDR` | Ƙara keɓewa; maimaita yadda ake buƙata. Keɓe na'urar IPv4 kuma yana keɓe adiresoshin IPv6 da ke kaiwa gare ta: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) da 6to4. Ana ɗaukar manufofi da keɓewa na IPv4-mapped kamar adiresoshin IPv4 da suke wakilta. |
| `--max-hosts N` | Iyakar adireshi da ake dubawa kafin keɓewa (tsoho/mafi girman iyaka 65,536). |
| `--history PATH` | Yi rikodin binciken da aka kammala a cikin rumbun tarihin SQLite na zaɓi. |
| `--services NAMES` | Jerin sunayen sabis da aka raba da waƙafi don dubawa, a cikin wannan tsarin (tsoho: duka). |
| `--ports SPEC` | Jerin `NAME=PORT` da aka raba da waƙafi (matsar da sabis) ko `PORT` (ƙara binciken TCP mai sauƙi mai suna `tcp-PORT`). |
| `--snmp-community-file PATH` | Fayil da ke ɗauke da SNMPv2c community don tambayar system MIB. Muhalli: `HOSTCENSUS_SNMP_COMMUNITY` (ƙimar) ko `HOSTCENSUS_SNMP_COMMUNITY_FILE` (hanyar). |
| `--snmp-user` | Mai amfani da SNMPv3. Muhalli: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (tsoho), `SHA224`, `SHA256`, `SHA384`, `SHA512` da fayil da ke ɗauke da kalmar sirri. Muhalli: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ko `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (tsoho), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` da fayil da ke ɗauke da kalmar sirri. Muhalli: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ko `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Kuma rubuta hoton lokaci mai siga don `hostcensus diff`. |
| `--tls-ca-file PATH` | Tantance takaddun shaidar HTTPS a kan wannan kunshin PEM maimakon ma'ajiyar tsari. Muhalli: `HOSTCENSUS_TLS_CA_FILE`. |

Ta tsoho ana bincika kowace na'ura don SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) da HTTPS (TCP 443). Ana gwada tashoshin TCP da cikakken haɗi. Ana gwada SNMP da buƙatar gano injin SNMPv3, wanda kowane wakilin SNMPv3 dole ne ya amsa ba tare da shaidar shiga ba; wannan gwajin ba zai gano wakilan da ke magana v1/v2c kawai ba. Tare da tsarin baya na asyncio ana ƙidaya na'ura a matsayin mai aiki idan kowane gwaji ya sami amsa, har da haɗin da aka ƙi, don haka na'urar da ta zubar da kowane gwaji tana da `alive=false` da kuskuren "Host is down"; wannan ba ya tabbatar da cewa tana kashe a zahiri ba. Tare da `--backend nmap`, nmap yana yanke shawarar waɗanne na'urori ne ke aiki (ICMP a matsayin root, TCP 80/443 in ba haka ba).

<a name="fingerprints"></a>

### Alamun gane sabis

Ana gane kowane buɗaɗɗen sabis daga abin da yake aikawa kafin kowane shiga. Babu abin da ke tantance shiga sai tambayar SNMP, kuma sai idan kun bayar da shaidar shiga.

| Gwaji | Abin da yake karantawa | `version` | Maɓallan `details` |
| --- | --- | --- | --- |
| `ssh` | Layin tantancewa na RFC 4253 | manhaja, misali `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Gaisuwar farko ta MySQL/MariaDB | sigar uwar garke | `server_version`, `flavor`, `auth_plugin`, ko `error_code`/`error` |
| `http` | Amsar `HEAD /` | Kanun `Server` | `status`, `server` |
| `https` | Musafahar TLS, takardar shaida, `HEAD /` | Kanun `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Gano SNMPv3; tare da shaidar shiga, GET na sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; tare da shaidar shiga `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ko `snmp_error` |

Ana warware manufar sunan na'ura sau ɗaya ga kowace na'ura kuma kowane gwaji yana haɗuwa da wannan adireshin, wanda aka rubuta a matsayin `address` a cikin sakamakon; ana amfani da sunan ne kawai don TLS SNI, tantance takardar shaida da kanun HTTP `Host`. Sunan da bai warware ba yana ba da yanayin `unknown` da kuskuren `Cannot resolve`. Ana riƙe sunayen Reverse DNS ne kawai lokacin da suke ɗauke da haruffan sunan na'ura, kuma mafi yawan bincike 16 ne ke gudana a lokaci guda. HTTPS yana amfani da tantance takardar shaida da sunan na'ura a kan ma'ajiyar tsari ko `--tls-ca-file`. Ana loda ma'ajiyar amincewa sau ɗaya don binciken kuma ana sake amfani da ita ga kowane gwajin HTTPS. Ana auna lokacin haɗin TCP da musafahar TLS daban, don haka tashar da ke karɓar haɗi amma ta tsayar da musafaha tana kasancewa `open` tare da `tls_error`, ba `filtered` ba. Idan tantancewa ta gaza, sakamakon yana rikodin `cert_verified: false` da `cert_verify_error`; ba ya sake gwadawa da saituna masu rauni ko aika buƙatar HTTP. Ana tattara bayanan takardar shaida da kanun HTTP ne kawai bayan tantancewa ta yi nasara. Bayar da kunshin CA da ya dace don sabis na private-CA. Tsoffin rahotanni na iya ƙunsar `cert_read_unverified`, wanda gwaje-gwajen yanzu ba sa ƙara samarwa.

Ana karanta sirrikan SNMP ne kawai daga masu canjin muhalli ko daga fayiloli (`--snmp-*-file`, ko mai canjin `HOSTCENSUS_SNMP_*_FILE` da ya dace), ba daga ƙimar layin umarni ba, waɗanda sauran masu amfani na gida za su iya gani a cikin jerin matakai. `--snmp-community`, `--snmp-auth-key` da `--snmp-priv-key` tare da ƙima suna fita da lamba 2 kuma suna ambaton madadinsu. Dole ne fayil ɗin sirri ya zama UTF-8 mara fanko na mafi yawan baiti 4096; ana yin watsi da sabon layi ɗaya a ƙarshe, kuma saita mai canji da fayil don sirri ɗaya kuskure ne. Kurakurai suna ambaton fayil ɗin amma ba sa buga abubuwan da ke cikinsa. Rahotannin bincike da tarihi ba sa haɗa ƙimar shaidar shiga da gangan. Mai fitarwa yana da zaɓin `--include-credentials` daban, a bayyane wanda aka bayyana a ƙasa. Community yana zaɓar SNMPv2c; mai amfani yana zaɓar SNMPv3, tare da tantancewa lokacin da aka ba da maɓallin auth da sirri lokacin da aka ba da maɓallan biyu (`snmp_security_level` yana rikodin wanne). hostcensus yana ƙi, tare da lambar fita 2, ya haɗa community da mai amfani na v3, ya yi amfani da maɓallin sirri ba tare da maɓallin auth ba, ko ya yi amfani da maɓallai ba tare da mai amfani ba, kuma ba ya taɓa sake gwada tambayar v3 da ta gaza tare da v2c ko ƙananan matakin tsaro. Wakilan da ke magana v1/v2c kawai suna yin watsi da gano v3 mara shaidar shiga, don haka suna bayyana a buɗe ne kawai lokacin da aka bayar da community.

Ana rage rubutun banner zuwa haruffa masu buguwa kuma ana iyakance shi zuwa haruffa 256 kafin a adana ko a nuna shi. Karatu ma yana da iyaka: 4 KiB ga kowane layi, 4 KiB don gaisuwar MySQL, 16 KiB na kanun HTTP. Ana yanke SNMP engine ID da ya fi octet 32 kafin a adana shi. HTTP da HTTPS suna aika kanun Host tare da adireshin IPv6 a cikin baka kuma tare da tashar idan ba 80 ko 443 ba ce. Ana ƙara gabatarwa ga sel ɗin CSV da suka fara da alamar dabarar jadawali don sel ɗin ya kasance rubutu.

### Iyakoki

Gudu ɗaya yana karɓar mafi yawan adiresoshi 65,536, sabis 64, da gwaje-gwaje 524,288 (na'urori sau sabis); manyan buƙatu suna fita da lamba 2 kafin a aika komai. An iyakance `--concurrency` zuwa soket 4096. Kowane gwaji yana da tsauraran wa'adi na sau huɗu na kasafin lokacinsa. Gwaje-gwajen haɗi (`tcp`, `ssh`, `mysql`, `http`) suna amfani da daƙiƙa 0.3 sai dai idan wannan sabis ɗin ya saita `timeout`. SNMP da HTTPS suna amfani da `--timeout` (tsoho 1.0) lokacin da ba su saita ɗaya ba. Ana ba da rahoton gwajin da ya kai wa'adin a matsayin `unknown` tare da "probe timed out" a cikin `errors`. Gazawar soket na gida (misali ƙarewar masu bayyana fayil) su ma `unknown` ne tare da rikodin kuskuren; ba sa taɓa ƙidayuwa a matsayin tashar da aka tace ko na'urar da ta mutu. Kafin gwaji, hostcensus yana ɗaga ƙaramin iyakar buɗe fayil zuwa babbar iyaka don dacewa da `--concurrency` da ƙarin masu bayyana 64; lokacin da ba zai iya ba, gwajin kafin farawa na `open files` yana gazawa kuma `scan` yana fita da 1 kafin aika bayanai. Gano Nmap yana amfani da ƙayyadadden lokacin na'ura na daƙiƙa 30. Ana miƙa prefix ga nmap a tsarin CIDR, kuma bincike yana gazawa da fita 1 lokacin da nmap ya ba da rahoton adiresoshi ƙasa da waɗanda aka ba shi (misali sunan da ba zai iya warwarewa ba) maimakon yi wa na'urori alamar sun mutu. Ana warware manufar sunan na'ura sau ɗaya kuma ana ba wa nmap wannan adireshin, don haka ganowa da gwaje-gwaje su kai ga injin ɗaya. Cikakken prefix tsari ne guda ɗaya na nmap wanda wa'adin ƙaramin tsarinsa shine daƙiƙa 35 ga kowane adiresoshi 256, an ƙara zuwa sama. Bincike mai keɓewa yana amfani da rukunoni na na'urori 256 da wa'adin daƙiƙa 35 ga kowane rukuni. Ƙirƙirar ma'aikata tana da iyaka ba tare da la'akari da girman kewayon ba. Reverse DNS da warware sunan na'ura suna da wa'adin daƙiƙa biyu daban; ana watsi da kiran mai warwarewa da ba ya taɓa dawowa a kan zaren sa, don haka ba zai iya riƙe hostcensus yana aiki fiye da waɗannan iyakokin ba. Mafi yawan bincike 16 ne ke gudana a lokaci guda, kuma kiran da aka watsar yana riƙe ramin sa har sai ya dawo, don haka adadin zaren da suka maƙale yana kasancewa da iyaka; idan duka 16 suka rataya, binciken da zai biyo baya yana yin layi don rami a wajen wa'adin daƙiƙa biyu (wanda ke farawa da zarar rami ya buɗe) har sai `--deadline` ya dakatar da binciken. `NetworkScanner` da ake amfani da shi a matsayin ɗakin karatu ba tare da `deadline` ba zai iya jiran irin wannan ramin har abada. `--deadline` (tsoho awa ɗaya) yana iyakance dukan gudun a saman waɗannan.

### Saita sabis

Ana iya canza sabis da fayil ɗin TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` ɗaya ne daga cikin `tcp`, `ssh`, `mysql`, `http`, `https` ko `snmp` kuma yana komawa ga sunan sabis lokacin da wannan gwaji ne, in ba haka ba `tcp`. `snmp` ne kawai ke amfani da UDP. Sunayen sabis ƙananan haruffa ne, lambobi, `-` da `_`. Sabis biyu ba za su iya raba tasha da ƙa'ida ba; tarihi yana rikodin yanayi ɗaya don wannan ma'auratan. `timeout` na zaɓi ne, a cikin daƙiƙa, kuma aƙalla 0.05. Gwaje-gwajen salon haɗi (`tcp`, `ssh`, `mysql`, `http`) suna komawa ga daƙiƙa 0.3. `snmp` da `https` suna amfani da `--timeout` na binciken lokacin da sabis ɗin bai saita `timeout` ba. `--timeout` ba ya maye gurbin kasafin lokacin da sabis ɗin ya riga ya mallaka.

Rahotannin JSON takardu ne masu siga (`"format": "hostcensus-report"`, `"version": 1`) waɗanda ke rikodin manufa, sabis ɗin da aka gwada da saituna kusa da `devices`; `--format json` ba tare da `-o` ba yana rubuta rahoton zuwa stdout maimakon tebur. Kowace fitowar JSON tana da tsarin da aka buga; duba [Fitowar JSON](../../../docs/json-output.md). Na'urori suna riƙe asalin filayen `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` da `errors` kuma suna ƙara jerin `services` tare da kowane gwajin `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, ko `unknown` lokacin da gwajin ya gaza a gida ko ya kai wa'adinsa), `version` da `details`. Fitowar CSV tana samun ginshiƙan ƙarshe na `services` da `versions` don buɗaɗɗun. Booleans na `ssh`, `snmp` da `mysql` suna bin sabis ɗin da ke da ainihin waɗannan sunayen.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Tsarin binciken lissafi, gwajin kafin farawa, da tarihi na gida

Tsarin bincike masu suna suna raba fayil ɗin TOML tare da bayanan `[services]` da ke akwai. Kwafi
[hostcensus.example.toml](../../../hostcensus.example.toml) zuwa `hostcensus.toml` kuma saita cibiyoyin sadarwar
da kuke gudanarwa:

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

`preflight` yana warware zaɓuɓɓuka da tsarin bincike daidai kamar yadda `scan` ke yi, har da
`--concurrency` don duba buɗaɗɗun fayiloli, don haka gwajin kafin farawa da ya wuce yana nufin `scan` zai
fara da shiri ɗaya.

Tsarin bincike suna karɓar `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, da `max_hosts`. `services` da `ports` suna amfani da tsarin jerin waƙafi da ke akwai.
Zaɓuɓɓukan CLI na bayyane suna rinjayar saitunan tsarin bincike; maimaita zaɓuɓɓukan `--exclude`
yana ƙara wa keɓewar tsarin bincike. Dole ne cibiyar sadarwa ta bayyane tare da `--profile` ta kasance
a cikin iyakar IP/CIDR na wannan tsarin binciken. Sunayen na'urori suna ci gaba da samun tallafi don bincike
kai tsaye, amma ba za a iya haɗa su da keɓewar IP ba. Iyakokin na'ura suna aiki kafin
keɓewa; jimillar iyakar gwaje-gwaje tana ci gaba da aiki bayan haka. Ana cire na'urorin da aka keɓe
daga duka binciken sabis da gano Nmap na zaɓi.

Kowane bincike yana yin gwaje-gwajen kafin farawa na gida kafin aika bayanai ga manufa: iyakokin
manufa/gwaji, damar shiga wurin ajiya, samuwar fayil ɗin aiwatarwa/wrapper na Nmap na zaɓi, tsarin
tarihi, da kunshin TLS CA da aka saita. `preflight` yana ba da rahoton JSON kuma ba ya bincika
manufofi ko ƙirƙirar rumbun tarihi. Yana rubuta fayil mai maƙwabtaka na ɗan lokaci don gwada
damar shiga wurin ajiya ba tare da canza abubuwan da ke akwai ba. Tsarin baya na asyncio na tsoho
har yanzu ba ya buƙatar Nmap ko root. Dole ne hanyoyin wurin ajiya su bambanta da
juna da saitin shigarwa, har da hard links; ana ƙin symlinks na wurin ajiya. Gwaje-gwajen da suka gaza
suna dawo da 1; iyaka/saiti mara inganci yana dawo da 2.

Rubuta rahoto da fitarwa suna buƙatar tallafin `O_NOFOLLOW`. A kan tsarin da ba su da shi,
har da Windows, waɗannan rubuce-rubucen suna gazawa ba tare da buɗewa ko yanke wurin ajiyar ba.
Sabbin rahotanni da rubutun fitarwa na mai shi ne kawai (yanayi 0600); maye gurbin fayil ɗin da ke akwai yana riƙe
izininsa. Rubutu zuwa named pipe ba tare da mai karatu ba yana gazawa nan take maimakon jira. Haka kuma ana ƙirƙirar sabon rumbun `--history` na mai shi kawai; wanda ke akwai yana riƙe yanayinsa. Saƙonnin rikodi koyaushe suna zuwa stderr, don haka stdout yana ɗaukar sakamako kawai. Fitarwa da ke ɗauke da shaidar shiga koyaushe tana tilasta yanayi 0600.

Tarihi na zaɓi ne kuma yana cika hotunan JSON da umarnin `diff` da ke akwai:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Yi amfani da IDs daga `history`; misalin yana ɗauka cewa sabon rumbun bayanai ne. Ana adana hotunan lokaci
cikin ma'amala tare da lokutan farawa/ƙarewa na UTC, sigar fakiti, saitunan da ba na sirri ba masu
aiki, taƙaitawa, da duk abubuwan da aka lura na na'ura/sabis, har da kurakuran kowace na'ura.
Ana riƙe lura da na'ura da bai cika ba. Ba a adana gudun da aka soke ba. Ana kiyaye yarjejeniyar
rahoto, hoton lokaci, fitarwa, da lambar fita ta bincike da ke akwai.

`history` yana jera taƙaitawar JSON ba tare da karanta duk bayanan na'urori na tarihi ba.
`compare` yana karanta bincike biyu da aka adana, yana buƙatar shaidar manufa iri ɗaya da tashoshin
da aka zaɓa, kuma yana ba da rahoton amsawa, matsayi, da canje-canjen yanayin tasha. Dole ne ID na binciken
farko ya riga ID na gaba. Lokacin da binciken biyu suka yi rikodin `timeout` ko `backend`
kuma waɗannan ƙimomin suka bambanta, rahoton yana jera gargaɗi kuma har yanzu yana kwatanta
abubuwan da aka lura. Bambancin jira na iya sa tashar da aka tace ta yi kama da a buɗe. Ana yi wa kurakuran
mai bincike da lura da tashar da ba a sani ba alama a matsayin marasa tabbas maimakon ɗaukar su a matsayin
tabbataccen ɓacewa ko rufewa: na'urori masu kurakurai suna bayyana a cikin `uncertain_hosts`, kuma
kowane sauyin tasha da ya ƙunshi `unknown` (har da unknown a binciken biyu) ana jera shi
a cikin `unconfirmed_ports` maimakon `port_changes`, banda tashar da ke buɗe a binciken
gaba, wanda canjin tasha ne. `compare` da `diff` suna rarraba tashoshi da ƙa'ida ɗaya.
`no_longer_responding` yana nufin rashin amsa, ba shaidar cire na'ura ba.
Lambar fita ta bincike 0 ba ta tabbatar da cewa kowace na'ura ta amsa ba: duba kurakuran kowace na'ura. Nasarar kwatantawa tana dawo da 0 ko akwai canje-canje ko babu; `diff` na fayil da ke akwai
yana riƙe yarjejeniyar lambar fita 3. Tarihi mara tallafi ko lalacewa yana dawo da 1.

Tarihi yana adana bayanan lissafi, don haka zaɓi kundin adireshi na gida mai kariya da ta dace.
Fayilolin tsarin bincike da saitunan da aka adana ba su ƙunshi shaidar shiga ta SNMP ba;
sarrafa shaidar shiga yana ci gaba ta hanyar zaɓuɓɓukan aiki/muhalli da ke akwai.

<a name="inventory-diff"></a>

## Kwatanta lissafi

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Hoton lokaci JSON ne mai `format: "hostcensus-snapshot"`, `version: 1`, sigar hostcensus, lokacin ƙirƙira na UTC, manufa, `timeout` da `backend` na binciken lokacin da binciken ya yi rikodinsu, sabis ɗin da aka gwada, da na'urorin da ke aiki a cikin siffa ɗaya kamar rahoton `-o`. Ana barin na'urorin da suka mutu. `diff` kuma yana karɓar rahotannin JSON na `scan -o` masu sauƙi, har da waɗanda suka gabaci samuwar filin `services`.

`diff` yana ba da rahoton sabbin na'urori da waɗanda suka ɓace, tashoshin da suka buɗe ko suka rufe a kan na'urorin da ke cikin duka biyun, da sabis ɗin da `version` ɗinsu ya canza. Ba a kwatanta tashoshin da aka gwada a ɗaya kawai daga cikin binciken biyu ba, kuma gargaɗi yana faɗin hakan. Lura da ta gaza ba ta taɓa karantawa a matsayin "babu canji" ba: tashar da ke `unknown` a ko wane bincike kuma ba a buɗe take a na gaba ba ana jera ta a ƙarƙashin `unconfirmed`, ba `closed` ba, tare da `before` na `open`, `unknown` ko `not-open` (an gwada kuma a rufe ko an tace) da `after` na `unknown` ko `not-open`; tashar da ke buɗe yanzu ana ba da rahotonta a ƙarƙashin `opened` ko da gwajin farko ya gaza. Na'urar da duk gwaje-gwajenta suka gaza ba tare da amsa a ko wane bincike ba ana jera ta a ƙarƙashin `unsettled_hosts` (tare da `before`/`after` na `up`, `uncertain` ko `absent`, har da lokacin da ta gaza a binciken biyu ko ta ɓace daga ɗayan fayil ɗin) maimakon `vanished_hosts`; idan ta amsa a binciken gaba kuma ana ba da rahotonta a matsayin sabuwar na'ura tare da buɗaɗɗun tashoshinta. Hotunan lokaci suna riƙe waɗannan na'urorin da suka gaza saboda wannan dalili. Gargaɗi kuma yana bayyana lokacin da manufofi suka bambanta, da kuma lokacin da fayilolin biyu suka yi rikodin timeout ko backend kuma waɗannan ƙimomin suka bambanta. `-o PATH` yana rubuta sigar JSON zuwa fayil ma.

Rahoto daga binciken da `--deadline` ya dakatar (`"complete": false`) yana jera na'urorin da ya kai gare su ne kawai, don haka `diff` da `export` suna ƙin shi da lambar fita 2. `--allow-partial` yana karɓar shi tare da gargaɗi a stderr: sannan `diff` yana jera na'urorin da binciken da bai cika ba bai jera su kwata-kwata ba a ƙarƙashin `unsettled_hosts` a matsayin `unscanned` maimakon vanished (na'urar da ya jera a matsayin ta mutu har yanzu vanished ce), yana saita `partial` zuwa true kuma ba ya taɓa ba da rahoton babu canji ba, kuma `export` yana rubuta gargaɗi a cikin kanun rubutun.

Lambobin fita na `diff`: `0` babu canje-canje, `3` an sami canje-canje, lura da ba za a iya tabbatarwa ba, ko shigarwa da bai cika ba (`changed` gaskiya ne duk lokacin da kowane jeri, har da `unsettled_hosts` da `unconfirmed`, ba fanko ba ne, ko `partial` gaskiya ne), `2` fayil ya ɓace, ba ya karantuwa, ba hoton lokaci da aka tallafa ba ne, ko bai cika ba ba tare da `--allow-partial` ba, `1` ba za a iya rubuta fayil ɗin `-o` ba.

<a name="kadupul-export"></a>

## Fitarwa zuwa Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (wani reshe na Cacti 1.2.31) ba shi da shigar da fayil ɗin na'urori da yawa a lokaci guda. Hanyarsa da aka tallafa don ƙara na'urori daga rubutu ita ce `cli/add_device.php`, na'ura ɗaya ga kowane kira, tare da hujjojin `--option=value`. `hostcensus export` yana rubuta rubutun POSIX `sh` na waɗannan kiraye-kirayen:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Kowace na'ura mai aiki tana zama `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Na'urorin da tambayar SNMP ta binciken ta yi nasara suna samun `--version=2 --community=...` ko `--version=3 --username=... --authproto=... --password=...` (tare da `--privproto`/`--privpass` don authPriv), `--port` da `--avail=snmp`. Fitarwar SNMPv3 tana buƙatar `--snmp-user`, kuma ana ƙin noAuthNoPriv saboda `add_device.php` yana buƙatar kalmar sirri ta v3.
- Sauran na'urori suna samun `--version=0 --avail=ping`, tare da `--ping_method=tcp --ping_port=` tashar TCP ta farko da ke buɗe, ko ICMP idan babu.
- `--notes` yana jera buɗaɗɗun sabis da sigogi. `--description` shine sunan reverse-DNS lokacin da yake mai sauƙi (haruffa, lambobi, `.`, `_`, `-`), in ba haka ba IP, kuma ana sanya shi na musamman, saboda `add_device.php` yana ɗaukar bayanin da ke akwai a matsayin sabuntawa ga wannan na'urar.

Ana tantance kowace ƙima kuma ana sanya mata alamar magana ta harsashi tare da `shlex.quote`. Ta tsoho ba a rubuta wani sirrin SNMP ba: rubutun yana faɗaɗa `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ko `HOSTCENSUS_SNMP_PRIV_KEY` a lokacin gudu kuma yana tsayawa idan ba a saita ɗaya ba. `--include-credentials` yana rubuta ƙimomin daga waɗannan masu canjin muhalli a cikin rubutun a maimakon haka, yana ƙirƙirar shi da yanayi 0600, kuma yana yin rikodin gargaɗi. `add_device.php` da kansa yana buga community kuma yana karɓar sirrika a matsayin hujjoji, waɗanda ake iya gani a cikin jerin matakai na uwar garken Kadupul yayin da kowane kira ke gudana.

`add_device.php` yana fita da 1 don kwafi da kurakurai; rubutun yana ci gaba, yana ƙidaya gazawa, kuma yana fita da 1 idan ba a ƙara wata na'ura ba. Template ids suna fitowa daga `php cli/add_device.php --list-host-templates`. Lambobin fita na `export`: `0` an rubuta, `2` shigarwa mara karantuwa, binciken da bai cika ba ba tare da `--allow-partial` ba, ko bayanan da ba za a iya fitar da su cikin aminci ba, `1` ba za a iya rubuta rubutun ba.

## Tsarin sigogi da fitarwa

hostcensus yana bin [Semantic Versioning](https://semver.org/spec/v2.0.0.html): gyare-gyare
masu dacewa suna ƙara sigar patch, fasalulluka/daina tallafawa masu dacewa suna ƙara
sigar minor, kuma canje-canjen da ke karya dacewa suna ƙara sigar major.
Umarnai da zaɓuɓɓuka, lambobin fita da tsarin JSON sune yarjejeniyar jama'a;
halin da aka daina tallafawa yana ci gaba da aiki har zuwa babbar fitarwa ta gaba, sai dai idan
gyaran tsaro ya buƙaci canza shi da wuri (sannan changelog yana bayyana dalilin).

release-please yana buɗe PR na fitarwa daga taken Conventional Commit a kan `main`,
yana ɗaga `pyproject.toml`, `uv.lock` da `CHANGES.md`. Haɗa shi yana ƙirƙirar
alamar `vMAJOR.MINOR.PATCH` da daftarin fitarwar GitHub, wanda CI ke haɗa masa
wheel da aka gwada, rarraba tushen lamba da lambobin tantancewa; GitHub yana adana shaidar gini don
waɗannan fayilolin ta hanyar API ɗin shaidarsa. Mai kula yana dubawa kuma ya buga
daftarin da zarar an haɗa fayilolin. Ba a taɓa maye gurbin fitarwa ba.

Amintaccen bugawa na PyPI na zaɓi ne kuma yana buƙatar mallakar aiki, amintaccen
mai bugawa da muhallin `pypi`. Yana buga ainihin kayan fitarwar da aka bincika
ba tare da sake ginawa ko adana alamar API ba. Fitarwa masu alama a cikin wannan ma'ajiyar
jama'a suna samar da shaidar kayan GitHub; reshe masu zaman kansu suna buƙatar tsarin da aka tallafa
da shiga a bayyane. Duba
[cikakken jagorar fitarwa](../../../docs/releasing.md) don saiti, ainihin umarnai da sake gwadawa.

## Haɓakawa

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Kayan aikin haɓakawa suna zama a cikin rukunonin abubuwan dogaro na [PEP 735](https://peps.python.org/pep-0735/)
a cikin `pyproject.toml` (`dev`, `fuzz`, `build`), don haka ba sa taɓa bayyana a cikin
bayanan fakitin da aka buga. `uv.lock` shine fayil ɗin kullewa guda ɗaya; CI tana shigarwa da
`uv sync --locked` kuma tana gazawa lokacin da fayil ɗin kullewar ya tsufa. Zaɓi mai fassarar Python da
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), ko kowane Python 3.12+.

CI tana tilasta ƙarancin rufe gwajin fakiti na 90%. Gwaje-gwajen sassa sun haɗa da uwar garken loopback
masu sarrafawa da shari'o'in tsarin bincike/tarihi/mai tantance fitarwa ba tare da intanet ba; ɗakin gwajin Compose yana gudanar da
OpenSSH, MariaDB, nginx da net-snmp a kan gadar cibiyar sadarwa keɓaɓɓiya. Gudanar da shi da
`make test-integration`. Duba [CONTRIBUTING.md](../../../CONTRIBUTING.md) da
[kayan aikin fitarwa](../../../scripts/README.md).

Kwantenan aiki yana gudana a matsayin UID/GID 10001 ba tare da kundin gida ba, ba tare da shigar
harsashi ba kuma ba tare da pip ba, kuma yana iya rubutawa zuwa `/app/output`. Ba wa wannan mai amfanin damar rubutu zuwa
kowane kundin fitowa da aka haɗa. Ba ya buƙatar ƙarin izinin tsari (capabilities) kuma yana aiki da
tsarin fayil na tushe na karatu kawai, don haka yana iya gudana kamar haka:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap yana amfani da halayensa na gano TCP ba tare da gata ba a cikin wannan kwantenan. CI tana sa
ginin hoton ya gaza a kan kowane rauni mai gyaruwa na HIGH ko CRITICAL da Trivy ya ba da rahoto.

## Binciken sarkar samarwa

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
yana gudana a kan main da kowane mako, yana buga ainihin makin sa, kuma yana loda sakamakon bincike zuwa
binciken lamba na GitHub. Ana kulle ayyuka da tushen kwantena ta hanyar hashes marasa canzawa; ana warware
abubuwan dogaro na Python a cikin `uv.lock`. Gazawar Bandit tana sa CI ta gaza, kuma gwajin fuzzing na Atheris
mai iyaka yana gwada masu nazarin tsari na SSH, MySQL, HTTP, takardar shaida da SNMPv3 BER
ba tare da samun hanyar sadarwa ba.

Scorecard kuma yana auna ayyukan bita na tarihi, bambancin masu ba da gudummawa, da
asalin fitarwa. Waɗannan maki suna nuna ainihin shaida; ba da'awa ba ne
cewa kowane binciken shugabanci ko fitarwar tarihi ya cika. Duba
[SECURITY.md](../../../SECURITY.md) da [asalin fitarwa](../../../docs/releasing.md).

## Fassara da daidaita harshe

Saƙonnin CLI da teburan taƙaitawa/diff na tashar umarni suna tallafawa harsuna 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ba tare da ƙarin abubuwan dogaro na aiki ba. Warwarewa yana girmama `--lang`, sannan `LC_ALL`, `LC_MESSAGES`, da `LANG`, yana komawa ga `en`. Tsarin JSON, ginshiƙan CSV, da rubutun fitarwa ba su canzawa a duk harsuna.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Ba da gudummawa

Gudummawa ya kamata su haɗa da shari'a mai maimaituwa, su kiyaye yarjejeniyar CLI da
tsarin bayanai da aka rubuta, kuma su wuce binciken inganci da ke sama. Duba
[CONTRIBUTING.md](../../../CONTRIBUTING.md) don tsarin aikin haɓakawa da
[jagorar fitarwa](../../../docs/releasing.md) don yanke shawara na dacewa da sigogi.

## Matsayin tsaro da lasisi

Duba [SECURITY.md](../../../SECURITY.md) don rahoton sirri da sigogin da aka tallafa.
An ba da lasisi ga hostcensus a ƙarƙashin [Lasisin MIT](../../../LICENSE).

Kanun tushe suna amfani da masu gano SPDX kuma suna kiyaye yabon masu ba da gudummawa daga tarihin
Git. Duba [AUTHORS.md](../../../AUTHORS.md) don yabo. Ɗaukar gwajin binary da
fayil ɗin kullewa da aka samar suna amfani da fayilolin `.license` masu maƙwabtaka; rubutun MIT yana cikin `LICENSES/MIT.txt`.
