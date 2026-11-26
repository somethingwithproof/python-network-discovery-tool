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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · **Filipino** · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Ang hostcensus ay isang Python CLI para sa mauulit na service inventory sa mga network na iyong pinamamahalaan.
Itinatala nito kung ano ang mga serbisyong nakabukas sa mga device, ikinukumpara ang mga obserbasyon sa paglipas ng panahon, at bumubuo ng
mga Kadupul import script. Ang default na backend ay gumagamit ng asyncio sockets nang walang root;
ang opsyonal na Nmap discovery ay makakakilala ng mga host lampas sa mga naka-configure na service port.

## Bakit hostcensus

Ang isang minsanan lang na port report ay hindi nagpapaliwanag kung ang susunod na obserbasyon ay nagbago o
sadyang nabigo lamang. Pinagsasama ng hostcensus ang malinaw na mga service state, mga bounded probe, mga magagamit muli na
scan profile, at lokal na history. Maaaring ulitin ng mga operator ang parehong saklaw, suriin ang
mga error, at ibukod ang mga hindi tiyak na obserbasyon mula sa mga kumpirmadong pagbabago.

- **Katibayan ng serbisyo:** Pagkakakilanlan ng SSH, mga MySQL greeting, mga HTTP header, mga obserbasyon ng TLS
  certificate, at SNMP discovery o mga credentialed system-MIB query.
- **Mauulit na saklaw:** Mga pinangalanang TOML profile, mga additive exclusion, mga nako-configure na
  serbisyo, mga host/probe cap, at mga bounded worker.
- **Pagsusuri bago ang trapiko:** Bine-validate ng lokal na preflight ang mga target, tool, destination
  access, history schema, at mga naka-configure na TLS CA bundle.
- **History ng imbentaryo:** Pinapanatili ng mga transactional SQLite snapshot ang lahat ng obserbasyon;
  pinananatiling kita ng mga paghahambing ang mga pagkabigo ng scanner at mga unknown state.
- **Interoperable na output:** Mga terminal, JSON at CSV report, mga naka-bersyong file snapshot,
  at mga Kadupul import script.

Sinasaklaw ng CI ang Python 3.12, 3.13 at 3.14 sa Linux at macOS, kasama ang isang kontroladong Compose
integration lab. Gumagamit ang code ng mga modernong type alias, mga typed preflight result,
mga keyword-only slotted profile at structured async cleanup habang pinapanatili ang mga naturang
bersyon ng runtime. Tingnan ang [Pagbe-bersyon at mga release](../../../docs/releasing.md) para sa SemVer
compatibility contract at proseso ng pag-release sa GitHub. Inilalarawan ng release badge ang
mga nai-publish na artifact, hindi ang checkout: ang pinakabagong nai-publish na tag ay kasalukuyang
`v0.3.0`, habang ang checkout na ito ay gumagamit ng bersyon ng package na `3.0.0`. Mag-install mula sa checkout
upang magamit ang mga feature ng imbentaryo na nakadokumento rito.

Magsimula sa [pag-install](#install), pagkatapos ay [mga profile at history](#inventory-profiles-preflight-and-local-history).
Para sa mga detalye ng integrasyon, tingnan ang [mga service fingerprint](#fingerprints),
[mga paghahambing ng file](#inventory-diff), at [pag-export sa Kadupul](#kadupul-export).

<a name="install"></a>

## Pag-install

Kinakailangan ang Python 3.12 o mas bago; Python 3.12–3.14 ang nasubukang matrix. Mula sa
checkout na ito, i-install ang mga naka-lock na runtime dependency:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Para sa opsyonal na Nmap host discovery, i-install ang Nmap executable gamit ang package manager
ng iyong platform; walang dagdag na Python package na kailangan. Ang XML output ng Nmap ay pina-parse gamit ang
defusedxml, isang pangunahing dependency, kaya tinatanggihan ang entity expansion. Direktang pinapatakbo ng hostcensus
ang `nmap` na matatagpuan sa `PATH` na may nakapirming listahan ng argumento, isang deadline na lumalaki
kasabay ng laki ng prefix, at 64 MiB na output cap. Hindi kailangan ang Nmap para sa default na backend.

## Pag-migrate mula sa netprobe

Ang hostcensus ay ang bagong pangalan ng netprobe, na inilabas sa 3.0.0. Hindi kailanman nai-publish ang proyekto
sa PyPI sa ilalim ng alinmang pangalan, kaya ang mga pag-install ay nagmula sa isang checkout o isang GitHub
release. Pinapanatili ng GitHub repository ang pangalan nito.

| Dati | Ngayon | Pagkatugma |
| --- | --- | --- |
| Distribution `netprobe` | `hostcensus` | Muling mag-install mula sa checkout; walang package para sa lumang pangalan. |
| Command na `netprobe` | `hostcensus` | Tumatakbo pa rin ang `netprobe` at nagpi-print ng isang deprecation line sa stderr. Walang pagbabago sa mga exit code at stdout. Aalisin sa susunod na major release. |
| Mga environment variable na `NETPROBE_*` | `HOSTCENSUS_*` | Ginagamit ang isang `NETPROBE_*` variable kapag hindi naka-set ang katumbas nitong `HOSTCENSUS_*`, na may isang babala sa stderr na nagbabanggit sa mga variable ngunit hindi sa mga value nito. Panalo ang `HOSTCENSUS_*` kapag parehong naka-set. Aalisin sa susunod na major release. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Nakakasira ng pagkatugma (Breaking).** Walang naka-install na import shim; i-update ang mga import. |
| Docker image tag `network-discovery:test` (CI lamang) at container user na `netprobe` | `hostcensus:test`, user na `hostcensus` | Walang registry image na nai-publish kailanman. I-build muli ang image at gamitin ang `hostcensus` entrypoint. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Ginagamit pa rin ang isang umiiral na file na may lumang default na pangalan, kasama ang isang babala, habang wala pa ang bagong pangalan. Hindi ginagalaw ang mga tahasang `--config` at `--history` path. |
| Mga report at snapshot na may `"format": "netprobe-report"` o `"netprobe-snapshot"`, at ang field na `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | Nilo-load pa rin ng `diff` at `export` ang mga file na isinulat sa ilalim ng lumang pangalan, at tinatanggap ng mga nai-publish na JSON Schema ang parehong baybay. Gumagamit ang mga bagong file ng mga bagong pangalan. Walang pagbabago sa mga SQLite history database at naglo-load ang mga ito tulad ng dati. |
| Mga Kadupul script mula sa `netprobe export` | Mga script mula sa `hostcensus export` | Patuloy na gumagana ang mga lumang script at binabasa pa rin ang `NETPROBE_SNMP_*` kapag pinatakbo. Binabasa ng mga bagong script ang `HOSTCENSUS_SNMP_*`. |

## Mabilisang halimbawa

Patakbuhin mula sa tester container ng integration lab na inilarawan sa ilalim ng Pag-develop; pinutol ang output:

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

## Mga exit code

| Command | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | naitala ang mga obserbasyon/report | nabigo ang preflight/backend, history, o pagsusulat ng report/snapshot | hindi wastong target, mga opsyon, configuration, o mga limitasyon | - | naabot ang `--deadline`; naisulat ang bahagyang report, nilaktawan ang history at snapshot |
| `preflight` | pumasa ang mga pagsusuri | nabigo ang lokal na pagsusuri | hindi wastong target/configuration o magkasalungat na mga destinasyon | - | - |
| `profiles` | nailista ang mga na-validate na profile | - | hindi mabasa/hindi wastong configuration o pagpili | - | - |
| `history` | nailista ang mga buod | nawawala, hindi wasto, o hindi suportadong history | hindi wastong mga CLI option | - | - |
| `compare` | nakagawa ng paghahambing, kabilang kapag may mga pagbabago | hindi mabasang history, hindi tugmang saklaw/pagkakasunod-sunod, o pagkabigo sa pagsusulat | hindi wastong mga CLI option | - | - |
| `diff` | walang pagbabago | hindi maisulat ang `-o` file | nawawala, hindi mabasa o hindi suportadong input, o isang hindi kumpletong scan nang walang `--allow-partial` | may nakitang mga pagbabago, mga hindi kumpirmadong obserbasyon, o isang hindi kumpletong scan | - |
| `export` | naisulat ang script | hindi maisulat ang script | hindi mabasang input, isang hindi kumpletong scan nang walang `--allow-partial`, o data na hindi ligtas ma-export | - | - |

## Istruktura

| Module | Pananagutan |
| --- | --- |
| `cli.py` | Mga opsyon sa command, paglutas ng profile, preflight, pag-scan at pag-uulat |
| `scanner.py`, `probes.py` | Pagpapalawak ng target, mga bounded worker, host discovery at mga obserbasyon sa serbisyo |
| `config.py`, `profiles.py` | Mga kahulugan ng serbisyo at mga na-validate na inventory profile |
| `models.py`, `output.py` | Mga uri ng resulta at pag-render ng terminal/JSON/CSV |
| `history.py`, `diff.py` | SQLite history at mga paghahambing ng naka-bersyong file snapshot |
| `preflight.py` | Mga lokal na pagsusuri at bounded na paghahanap ng bersyon ng Nmap |
| `export.py` | Mga na-validate at naka-quote na Kadupul import script |

Ang bawat obserbasyon sa serbisyo ay nagtatala ng estado nito nang hiwalay sa ina-advertise na pagkakakilanlan nito.
Ang mga pagbasa at deadline ay may hangganan; ang mga probe exception ay nananatili sa mga error ng host. Ang SQLite
history ay gumagamit ng mga transaksyon, tahasang paglilinis ng koneksyon, at mga read-only na paglilista at
mga path ng paghahambing. Ang mga sikreto ng SNMP ay pumapasok lamang sa pamamagitan ng mga environment variable o mga secret
file; itinatala ng history ng imbentaryo ang mga epektibong setting na walang sikreto. Tingnan ang
[Arkitektura](../../../docs/architecture.md) para sa pipeline ng scan, mga limitasyon nito at mga trust
boundary, at ang [SECURITY.md](../../../SECURITY.md#authorized-use) para sa awtorisadong paggamit.


## Paggamit

Mag-scan lamang ng mga network na iyong pinamamahalaan.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opsyon | Kahulugan |
| --- | --- |
| `NETWORK` | CIDR, IP, o hostname; opsyonal kasama ang `--profile`. Tinatanggihan ang mga IPv6 scope identifier. |
| `-o, --output PATH` | Sumulat ng report. Sinusundan ng format ang extension (`.json`, `.csv`); ang ibang mga extension ay bumabalik sa JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Pilitin ang format ng report. Walang epekto nang walang `--output`. Pinipili ng `.sh` ang `kadupul`. |
| `-v, --verbose` | Debug logging. |
| `-q, --quiet` | Itago ang mga resulta, progreso at mga informational log; lumalabas pa rin ang mga babala at error sa stderr. |
| `--backend asyncio\|nmap` | Host discovery. Direktang sino-probe ng `asyncio` (default) ang mga service port; nagpapatakbo muna ang `nmap` ng nmap ping sweep at nangangailangan ng `nmap` executable sa `PATH`. |
| `--timeout SECONDS` | Maghintay para sa mga probe na hindi nagtatakda ng sarili nilang budget (default 1.0). Gumagamit ang mga built-in connect probe ng 0.3s maliban kung magtatakda ng `timeout` ang service table. |
| `--concurrency N` | Mga probe na sabay-sabay na tumatakbo (default 256). |
| `--deadline SECONDS` | Ihinto ang buong scan, kasama ang nmap sweep, pagkatapos ng ganitong katagal (default 3600, pinakamataas na 604800; env `HOSTCENSUS_DEADLINE`). Ang mga host na natapos ay isinusulat sa report na may `"complete": false`, walang history o snapshot na isinusulat, at nag-e-exit ang `scan` nang 4. |
| `--config PATH` | Mga TOML na kahulugan ng serbisyo at opsyonal na mga pinangalanang `[profiles]` setting. |
| `--profile NAME` | Gumamit ng pinangalanang profile; nagde-default sa `hostcensus.toml` kapag inalis ang `--config`. |
| `--exclude IP/CIDR` | Magdagdag ng exclusion; ulitin kung kinakailangan. Ang isang excluded na IPv4 host ay nag-e-exclude din sa mga IPv6 address na nakakaabot dito: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) at 6to4. Ang mga IPv4-mapped target at exclusion ay itinuturing bilang mga IPv4 address na tinutukoy nila. |
| `--max-hosts N` | Limitasyon sa address na sinusuri bago ang mga exclusion (default/hard maximum 65,536). |
| `--history PATH` | Itala ang nakumpletong scan sa isang opt-in na SQLite history database. |
| `--services NAMES` | Listahan ng mga pangalan ng serbisyo na pinaghihiwalay ng kuwit upang suriin, sa ganoong pagkakasunod-sunod (default: lahat). |
| `--ports SPEC` | Listahan na pinaghihiwalay ng kuwit ng `NAME=PORT` (ilipat ang isang serbisyo) o `PORT` (magdagdag ng simpleng TCP check na pinangalanang `tcp-PORT`). |
| `--snmp-community-file PATH` | File na naglalaman ng SNMPv2c community para sa system MIB query. Env: `HOSTCENSUS_SNMP_COMMUNITY` (ang value) o `HOSTCENSUS_SNMP_COMMUNITY_FILE` (ang path). |
| `--snmp-user` | User ng SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (default), `SHA224`, `SHA256`, `SHA384`, `SHA512` at isang file na naglalaman ng passphrase. Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` o `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (default), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` at isang file na naglalaman ng passphrase. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` o `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Sumulat din ng naka-bersyong snapshot para sa `hostcensus diff`. |
| `--tls-ca-file PATH` | I-verify ang mga HTTPS certificate laban sa PEM bundle na ito sa halip na sa system store. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Bilang default, sinusuri ang bawat host para sa SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) at HTTPS (TCP 443). Sinusubok ang mga TCP port sa pamamagitan ng ganap na koneksyon. Sinusubok ang SNMP sa pamamagitan ng isang SNMPv3 engine-discovery request, na dapat sagutin ng sinumang SNMPv3 agent nang walang kredensyal; hindi matutukoy ng probe na ito ang mga agent na v1/v2c lamang ang sinasalita. Gamit ang asyncio backend, itinuturing na buhay ang isang host kapag nakatanggap ng sagot ang anumang probe, kabilang ang isang tinanggihang koneksyon, kaya ang isang host na nagda-drop ng lahat ng probe ay may `alive=false` at ang error na "Host is down"; hindi nito pinapatunayan na pisikal itong nakapatay. Gamit ang `--backend nmap`, ang nmap ang nagpapasya kung aling mga host ang buhay (ICMP bilang root, TCP 80/443 kung hindi).

<a name="fingerprints"></a>

### Mga fingerprint

Ang bawat bukas na serbisyo ay kinukuhanan ng fingerprint mula sa ipinapadala nito bago ang anumang pag-login. Walang nag-a-authenticate maliban sa SNMP query, at kapag nagbigay ka lamang ng mga kredensyal.

| Probe | Binabasa | `version` | Mga key ng `details` |
| --- | --- | --- | --- |
| `ssh` | Linya ng pagkakakilanlan ng RFC 4253 | software, hal. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Paunang handshake ng MySQL/MariaDB | bersyon ng server | `server_version`, `flavor`, `auth_plugin`, o `error_code`/`error` |
| `http` | Tugon sa `HEAD /` | `Server` header | `status`, `server` |
| `https` | TLS handshake, certificate, `HEAD /` | `Server` header | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 discovery; kapag may mga kredensyal, GET ng sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; kapag may mga kredensyal `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, o `snmp_error` |

Ang isang hostname target ay nire-resolve nang isang beses bawat host at kumokonekta ang bawat probe sa address na iyon, na nakatala bilang `address` sa mga resulta; ang pangalan ay ginagamit lamang para sa TLS SNI, pag-verify ng certificate at sa HTTP `Host` header. Ang isang pangalan na hindi nare-resolve ay nagbibigay ng mga `unknown` state at isang `Cannot resolve` error. Ang mga reverse DNS name ay pinapanatili lamang kapag naglalaman ang mga ito ng mga character ng hostname, at hanggang 16 na paghahanap lamang ang sabay-sabay na tumatakbo. Gumagamit ang HTTPS ng pag-verify ng certificate at hostname laban sa system store o `--tls-ca-file`. Nilo-load ang trust store nang isang beses para sa scan at muling ginagamit para sa bawat HTTPS probe. Magkahiwalay na binibigyan ng oras ang TCP connect at ang TLS handshake, kaya ang isang port na tumatanggap ng mga koneksyon ngunit nabibitin sa handshake ay `open` na may `tls_error`, hindi `filtered`. Kung mabigo ang pag-verify, itinatala ng resulta ang `cert_verified: false` at `cert_verify_error`; hindi ito umuulit gamit ang mas mahinang setting o nagpapadala ng HTTP request. Kinokolekta lamang ang mga detalye ng certificate at HTTP header pagkatapos magtagumpay ang pag-verify. Magbigay ng tamang CA bundle para sa mga serbisyong may private-CA. Maaaring maglaman ang mga mas lumang report ng `cert_read_unverified`, na hindi na ginagawa ng mga kasalukuyang probe.

Ang mga sikreto ng SNMP ay binabasa lamang mula sa mga environment variable o mula sa mga file (`--snmp-*-file`, o ang katugmang `HOSTCENSUS_SNMP_*_FILE` variable), hindi kailanman mula sa mga value sa command-line, na makikita ng ibang lokal na user sa listahan ng proseso. Ang `--snmp-community`, `--snmp-auth-key` at `--snmp-priv-key` na may value ay nag-e-exit nang may code 2 at pinapangalanan ang pamalit. Ang isang secret file ay dapat na non-empty UTF-8 na hindi hihigit sa 4096 bytes; binabalewala ang isang trailing newline, at isang error ang pagtatakda ng parehong variable at file para sa iisang sikreto. Pinapangalanan ng mga error ang file ngunit hindi kailanman ini-print ang nilalaman nito. Hindi sinasadyang isinasama ng mga scan report at history ang mga value ng kredensyal. Ang exporter ay may hiwalay at tahasang `--include-credentials` option na inilalarawan sa ibaba. Pinipili ng isang community ang SNMPv2c; pinipili ng isang user ang SNMPv3, na may authentication kapag may ibinigay na auth key at may privacy kapag ibinigay ang parehong key (itinatala ng `snmp_security_level` kung alin). Tinatanggihan ng hostcensus, nang may exit code 2, na pagsamahin ang isang community at isang v3 user, gumamit ng privacy key nang walang auth key, o gumamit ng mga key nang walang user, at hindi nito kailanman inuulit ang isang nabigong v3 query gamit ang v2c o mas mababang security level. Binabalewala ng mga agent na v1/v2c lamang ang sinasalita ang credential-free v3 discovery, kaya lumilitaw lamang ang mga ito bilang open kapag may ibinigay na community.

Ang teksto ng banner ay binabawasan sa mga printable character at nililimitahan sa 256 character bago ito i-store o ipakita. May hangganan din ang mga pagbasa: 4 KiB bawat linya, 4 KiB para sa isang MySQL greeting, 16 KiB ng mga HTTP header. Ang isang SNMP engine ID na mas mahaba sa 32 octets ay pinuputol bago i-store. Nagpapadala ang HTTP at HTTPS ng Host header na may IPv6 address sa loob ng mga bracket at kasama ang port kapag hindi ito 80 o 443. Ang mga CSV cell na nagsisimula sa isang spreadsheet formula trigger ay nilalagyan ng prefix upang manatiling teksto ang cell.

### Mga limitasyon

Ang isang pagpapatakbo ay tumatanggap ng hanggang 65,536 na address, 64 na serbisyo, at 524,288 na probe (mga host times mga serbisyo); ang mas malalaking request ay nag-e-exit nang may code 2 bago pa may maipadala. Ang `--concurrency` ay nililimitahan sa 4096 na socket. Ang bawat probe ay may hard deadline na apat na beses ng sarili nitong budget. Gumagamit ang mga connect probe (`tcp`, `ssh`, `mysql`, `http`) ng 0.3 segundo maliban kung magtatakda ng `timeout` ang serbisyong iyon. Ginagamit ng SNMP at HTTPS ang `--timeout` (default 1.0) kapag wala silang itinakda. Ang isang probe na umabot sa deadline ay iniuulat bilang `unknown` na may "probe timed out" sa `errors`. Ang mga lokal na pagkabigo ng socket (halimbawa, pagkaubos ng mga file descriptor) ay `unknown` din kasama ang nakatalang error; hindi kailanman ito binibilang bilang isang filtered port o isang down host. Bago mag-probe, itinataas ng hostcensus ang open-file soft limit patungo sa hard limit upang magkasya ang `--concurrency` dagdag ang 64 na descriptor; kapag hindi nito magawa, nabibigo ang `open files` preflight check at nag-e-exit ang `scan` nang 1 bago magpadala ng trapiko. Gumagamit ang Nmap discovery ng 30-segundong host timeout. Ang isang prefix ay ipinapasa sa nmap sa anyong CIDR, at nabibigo ang isang sweep nang may exit 1 kapag nag-ulat ang nmap ng mas kaunting address kaysa sa ibinigay rito (halimbawa isang pangalan na hindi nito ma-resolve) sa halip na markahang down ang mga host. Ang isang hostname target ay nire-resolve nang isang beses at ibinibigay sa nmap ang address na iyon, kaya ang discovery at ang mga probe ay nakakaabot sa parehong machine. Ang isang buong prefix ay isang proseso ng nmap na ang subprocess deadline ay 35 segundo para sa bawat 256 na address, naka-round up. Gumagamit ang mga sweep na may mga exclusion ng mga batch ng 256 na host at 35-segundong deadline para sa bawat batch. Ang paggawa ng worker ay may hangganan nang nakapag-iisa sa laki ng saklaw. Ang reverse DNS at pag-resolve ng hostname ay may hiwalay na dalawang-segundong deadline; ang isang resolver call na hindi kailanman bumabalik ay iniiwan sa sarili nitong thread, kaya hindi nito mapapanatiling tumatakbo ang hostcensus lampas sa mga limitasyong ito. Hanggang 16 na paghahanap lamang ang sabay-sabay na tumatakbo, at ang isang iniwang call ay pinapanatili ang slot nito hanggang sa bumalik ito, kaya nananatiling limitado ang bilang ng mga na-stuck na thread; kung mag-hang ang lahat ng 16, pumipila ang mga susunod na paghahanap para sa isang slot sa labas ng dalawang-segundong deadline (na nagsisimula kapag may bakanteng slot na) hanggang sa ihinto ng `--deadline` ang scan. Ang `NetworkScanner` na ginamit bilang isang library nang walang `deadline` ay maaaring maghintay para sa ganoong slot nang walang katiyakan. Nililimitahan ng `--deadline` (default isang oras) ang buong pagpapatakbo sa ibabaw ng mga ito.

### Pag-configure ng mga serbisyo

Maaaring baguhin ang mga serbisyo gamit ang isang TOML file:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

Ang `probe` ay isa sa `tcp`, `ssh`, `mysql`, `http`, `https` o `snmp` at nagde-default sa pangalan ng serbisyo kapag iyon ay isang probe, kung hindi ay `tcp`. Tanging `snmp` lamang ang gumagamit ng UDP. Ang mga pangalan ng serbisyo ay maliliit na titik, numero, `-` at `_`. Hindi maaaring magbahagi ng port at protocol ang dalawang serbisyo; itinatala ng history ang isang estado para sa pares na iyon. Opsyonal ang `timeout`, sa segundo, at hindi bababa sa 0.05. Ang mga connect-style probe (`tcp`, `ssh`, `mysql`, `http`) ay nagde-default sa 0.3 segundo. Ginagamit ng `snmp` at `https` ang scan `--timeout` kapag hindi nagtatakda ng `timeout` ang serbisyo. Hindi pinapalitan ng `--timeout` ang budget na mayroon na ang serbisyo.

Ang mga JSON report ay mga naka-bersyong dokumento (`"format": "hostcensus-report"`, `"version": 1`) na nagtatala ng target, mga na-probe na serbisyo at mga setting sa tabi ng `devices`; ang `--format json` nang walang `-o` ay nagsusulat ng report sa stdout sa halip na sa talahanayan. Ang bawat JSON output ay may nai-publish na schema; tingnan ang [JSON output](../../../docs/json-output.md). Pinapanatili ng mga device ang orihinal na mga field na `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` at `errors` at nagdaragdag ng listahan ng `services` na may `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, o `unknown` kapag lokal na nabigo ang probe o naabot ang deadline nito), `version` at `details` ng bawat probe. Nagkakaroon ang CSV output ng mga trailing column na `services` at `versions` para sa mga bukas. Sinusundan ng mga boolean na `ssh`, `snmp` at `mysql` ang mga serbisyong may eksaktong ganoong mga pangalan.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Mga inventory profile, preflight, at lokal na history

Ang mga pinangalanang profile ay nagbabahagi ng isang TOML file sa mga umiiral na `[services]` definition. Kopyahin ang
[hostcensus.example.toml](../../../hostcensus.example.toml) sa `hostcensus.toml` at itakda ang mga network
na iyong pinamamahalaan:

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

Nire-resolve ng `preflight` ang mga opsyon at profile nang eksakto tulad ng ginagawa ng `scan`, kabilang ang
`--concurrency` para sa open-file check, kaya ang isang pumapasang preflight ay nangangahulugang magsisimula ang `scan`
nang may parehong plano.

Tumatanggap ang mga profile ng `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, at `max_hosts`. Gumagamit ang `services` at `ports` ng umiiral na comma-list
syntax. Ino-override ng mga tahasang CLI option ang mga setting ng profile; ang mga inulit na `--exclude`
option ay idinaragdag sa mga exclusion ng profile. Ang isang tahasang network na may `--profile` ay dapat
nakapaloob sa IP/CIDR scope ng profile na iyon. Nananatiling suportado ang mga hostname para sa mga direktang
scan, ngunit hindi maaaring isama sa mga IP exclusion. Nalalapat ang mga host limit bago ang
mga exclusion; nalalapat pa rin pagkatapos ang kabuuang probe cap. Ang mga excluded na host ay
tinatanggal mula sa parehong mga pagsusuri ng serbisyo at opsyonal na Nmap discovery.

Nagsasagawa ang bawat scan ng mga lokal na preflight check bago ang target na trapiko: mga limitasyon sa target/probe,
destination access, opsyonal na pagkakaroon ng Nmap executable/wrapper, history
schema, at isang naka-configure na TLS CA bundle. Nag-uulat ang `preflight` ng JSON at hindi nag-i-scan
ng mga target o gumagawa ng history database. Pansamantala itong nagsusulat ng isang sibling file upang subukan ang
destination access nang hindi binabago ang umiiral na nilalaman. Ang default na asyncio backend
ay hindi pa rin nangangailangan ng Nmap o root. Dapat magkaiba ang mga destination path sa isa't
isa at sa input configuration, kabilang ang mga hard link; tinatanggihan ang mga destination
symlink. Nagbabalik ng 1 ang mga nabigong pagsusuri; nagbabalik ng 2 ang hindi wastong saklaw/configuration.

Kinakailangan ng mga pagsusulat ng report at export ang suporta sa `O_NOFOLLOW`. Sa mga platform na wala nito,
kabilang ang Windows, nabibigo ang mga pagsusulat na ito nang hindi binubuksan o pinuputol ang destinasyon.
Ang mga bagong report at export script ay para sa may-ari lamang (mode 0600); pinapanatili ng pagpapalit ng isang umiiral na file ang mga
pahintulot nito. Ang pagsusulat sa isang named pipe na walang bumabasa ay agad na nabibigo sa halip na maghintay. Ang isang bagong `--history` database ay ginagawa ring para sa may-ari lamang; pinapanatili ng isang umiiral ang mode nito. Palaging napupunta sa stderr ang mga log message, kaya mga resulta lamang ang dinadala ng stdout. Palaging pinipilit ng mga export na naglalaman ng mga kredensyal ang mode 0600.

Ang history ay opt-in at pinupunan nito ang mga umiiral na JSON snapshot at ang `diff` command:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Gamitin ang mga ID mula sa `history`; ipinagpapalagay ng halimbawa ang isang bagong database. Ang mga snapshot ay ini-store
nang transactional kasama ang mga oras ng pagsisimula/pagtatapos sa UTC, bersyon ng package, mga epektibong setting na walang sikreto,
mga buod, at lahat ng obserbasyon sa host/serbisyo, kabilang ang mga error sa bawat host.
Pinapanatili ang mga hindi kumpletong obserbasyon sa host. Hindi sine-save ang mga kinanselang pagpapatakbo. Pinapanatili ang umiiral na
mga kontrata sa report, snapshot, export, at exit-code ng scan.

Inililista ng `history` ang mga JSON summary nang hindi binabasa ang lahat ng makasaysayang payload ng device.
Binabasa ng `compare` ang dalawang naka-save na scan, nangangailangan ng magkatulad na mga target identity at mga napiling
port, at nag-uulat ng mga pagbabago sa pagtugon, katayuan, at port-state. Dapat mauna ang mas maagang
scan ID sa mas huling ID. Kapag parehong nagtala ang dalawang scan ng `timeout` o `backend`
at magkaiba ang mga value na iyon, naglilista ang report ng isang babala at ikinukumpara pa rin ang
mga obserbasyon. Ang ibang tagal ng paghihintay ay maaaring magmukhang open ang isang filtered port. Ang mga error sa scanner
at mga unknown port observation ay minamarkahan bilang hindi tiyak sa halip na ituring bilang
kumpirmadong pagkawala o pagsasara: lumilitaw ang mga host na may error sa `uncertain_hosts`, at
bawat paglipat ng port na kinasasangkutan ng `unknown` (kabilang ang unknown sa parehong scan) ay inililista
sa `unconfirmed_ports` sa halip na sa `port_changes`, maliban sa isang port na open sa
mas huling scan, na isang port change. Inuuri ng `compare` at `diff` ang mga port gamit ang parehong panuntunan.
Nangangahulugan ang `no_longer_responding` ng kawalan ng tugon, hindi patunay ng pag-alis ng device.
Hindi ginagarantiya ng scan exit code 0 na tumugon ang bawat host: suriin ang mga error sa bawat host. Nagbabalik ng 0 ang tagumpay ng paghahambing may pagbabago man o wala; pinapanatili ng umiiral na file `diff`
ang kontrata nitong exit code 3. Nagbabalik ng 1 ang hindi suportado o sirang history.

Nag-iimbak ang history ng impormasyon sa imbentaryo, kaya pumili ng lokal na direktoryo na may angkop na proteksyon.
Hindi naglalaman ng mga kredensyal ng SNMP ang mga profile file at mga naka-store na setting;
patuloy na pinapangasiwaan ang mga kredensyal sa pamamagitan ng mga umiiral na runtime option/environment.

<a name="inventory-diff"></a>

## Diff ng imbentaryo

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Ang isang snapshot ay JSON na may `format: "hostcensus-snapshot"`, `version: 1`, ang bersyon ng hostcensus, ang oras ng paggawa sa UTC, ang target, ang scan `timeout` at `backend` kapag itinala ito ng scan, ang mga serbisyong na-probe, at ang mga buhay na host sa parehong hugis tulad ng `-o` report. Iniiwan ang mga down host. Tumatanggap din ang `diff` ng mga simpleng `scan -o` JSON report, kabilang ang mga mula pa bago umiral ang field na `services`.

Nag-uulat ang `diff` ng mga bago at nawalang host, mga port na nagbukas o nagsara sa mga host na naroroon sa pareho, at mga serbisyong nagbago ng `version`. Ang mga port na na-probe lamang sa isa sa dalawang scan ay hindi ikinukumpara, at sinasabi ito ng isang babala. Hindi kailanman binabasa ang mga nabigong obserbasyon bilang "walang pagbabago": ang isang port na `unknown` sa alinmang scan at hindi open sa mas huli ay inililista sa ilalim ng `unconfirmed`, hindi `closed`, na may `before` na `open`, `unknown` o `not-open` (na-probe at closed o filtered) at `after` na `unknown` o `not-open`; ang isang port na open na ngayon ay iniuulat sa ilalim ng `opened` kahit na nabigo ang naunang probe. Ang isang host na ang lahat ng probe ay nabigo nang walang sagot sa alinmang scan ay inililista sa ilalim ng `unsettled_hosts` (na may `before`/`after` na `up`, `uncertain` o `absent`, kabilang kapag nabigo ito sa parehong scan o nawawala sa kabilang file) sa halip na sa `vanished_hosts`; kung sumagot ito sa mas huling scan ay iniuulat din ito bilang isang bagong host kasama ang mga open port nito. Pinapanatili ng mga snapshot ang mga nabigong host na ito para sa dahilang ito. Lumilitaw din ang isang babala kapag magkaiba ang mga target, at kapag parehong nagtala ng timeout o backend ang dalawang file at magkaiba ang mga value na iyon. Isinusulat din ng `-o PATH` ang anyong JSON sa isang file.

Ang isang report mula sa isang scan na inihinto ng `--deadline` (`"complete": false`) ay naglilista lamang ng mga host na naabot nito, kaya tinatanggihan ito ng `diff` at `export` nang may exit code 2. Tinatanggap ito ng `--allow-partial` kasama ang isang babala sa stderr: pagkatapos ay inililista ng `diff` ang mga host na hindi talaga inilista ng hindi kumpletong scan sa ilalim ng `unsettled_hosts` bilang `unscanned` sa halip na vanished (ang isang host na inilista nito bilang down ay vanished pa rin), itinatakda ang `partial` sa true at hindi kailanman nag-uulat ng walang pagbabago, at nagsusulat ang `export` ng isang babala sa script header.

Mga exit code ng `diff`: `0` walang pagbabago, `3` may nakitang mga pagbabago, mga obserbasyong hindi nakumpirma, o isang hindi kumpletong input (ang `changed` ay true tuwing may anumang listahan, kabilang ang `unsettled_hosts` at `unconfirmed`, na hindi walang laman, o true ang `partial`), `2` nawawala ang isang file, hindi mabasa, hindi suportadong snapshot, o hindi kumpleto nang walang `--allow-partial`, `1` hindi maisulat ang `-o` file.

<a name="kadupul-export"></a>

## Pag-export sa Kadupul

Ang [Kadupul](https://github.com/kadupulhq/kadupul) (isang fork ng Cacti 1.2.31) ay walang bulk device file import. Ang suportadong paraan nito upang magdagdag ng mga device mula sa isang script ay ang `cli/add_device.php`, isang device bawat tawag, na may mga `--option=value` argument. Nagsusulat ang `hostcensus export` ng isang POSIX `sh` script ng mga tawag na iyon:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Ang bawat buhay na host ay nagiging `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Ang mga host kung saan nagtagumpay ang SNMP query ng scan ay nakakakuha ng `--version=2 --community=...` o `--version=3 --username=... --authproto=... --password=...` (kasama ang `--privproto`/`--privpass` para sa authPriv), `--port` at `--avail=snmp`. Nangangailangan ang SNMPv3 export ng `--snmp-user`, at tinatanggihan ang noAuthNoPriv dahil nangangailangan ang `add_device.php` ng v3 password.
- Ang ibang mga host ay nakakakuha ng `--version=0 --avail=ping`, na may `--ping_method=tcp --ping_port=` ang unang open TCP port, o ICMP kung wala.
- Inililista ng `--notes` ang mga bukas na serbisyo at bersyon. Ang `--description` ay ang reverse-DNS name kapag ito ay payak (mga titik, numero, `.`, `_`, `-`), kung hindi ay ang IP, at ginagawang natatangi, dahil itinuturing ng `add_device.php` ang isang umiiral na paglalarawan bilang isang update sa device na iyon.

Ang bawat value ay bina-validate at naka-shell-quote gamit ang `shlex.quote`. Bilang default, walang sikreto ng SNMP na isinusulat: pinapalawak ng script ang `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` o `HOSTCENSUS_SNMP_PRIV_KEY` sa run time at humihinto kung hindi naka-set ang isa. Sa halip, isinusulat ng `--include-credentials` ang mga value mula sa mga environment variable na iyon sa script, ginagawa ito nang may mode 0600, at naglo-log ng isang babala. Ini-print mismo ng `add_device.php` ang community at tumatanggap ng mga sikreto bilang mga argumento, na makikita sa process list ng Kadupul server habang tumatakbo ang bawat tawag.

Nag-e-exit ang `add_device.php` nang 1 para sa mga duplicate at error; nagpapatuloy ang script, binibilang ang mga pagkabigo, at nag-e-exit nang 1 kung may anumang device na hindi naidagdag. Nagmumula ang mga template id sa `php cli/add_device.php --list-host-templates`. Mga exit code ng `export`: `0` naisulat, `2` hindi mabasang input, isang hindi kumpletong scan nang walang `--allow-partial`, o data na hindi ligtas ma-export, `1` hindi maisulat ang script.

## Pagbe-bersyon at proseso ng pag-release

Sinusunod ng hostcensus ang [Semantic Versioning](https://semver.org/spec/v2.0.0.html): ang mga compatible
na pag-aayos ay nagpapataas ng patch version, ang mga compatible na feature/deprecation ay nagpapataas ng
minor version, at ang mga breaking compatibility change ay nagpapataas ng major version.
Ang mga command at opsyon, mga exit code at ang mga JSON schema ay ang pampublikong kontrata;
patuloy na gumagana ang deprecated na gawi hanggang sa susunod na major release, maliban kung
kailangang baguhin ito nang mas maaga dahil sa isang security fix (sasabihin ng changelog kung bakit).

Nagbubukas ang release-please ng isang release PR mula sa mga pamagat ng Conventional Commit sa `main`,
na nagba-bump ng `pyproject.toml`, `uv.lock` at `CHANGES.md`. Ang pag-merge nito ay lumilikha ng
`vMAJOR.MINOR.PATCH` tag at isang draft GitHub release, kung saan ikinakabit ng CI ang isang nasubukang
wheel, source distribution at mga checksum; nag-iimbak ang GitHub ng mga build attestation para sa
mga file na iyon sa pamamagitan ng attestations API nito. Sinusuri at ini-publish ng isang maintainer ang
draft kapag nakakabit na ang mga file. Hindi kailanman pinapalitan ang mga release.

Ang PyPI trusted publishing ay opt-in at nangangailangan ng pagmamay-ari ng proyekto, isang trusted
publisher at ang `pypi` environment. Ini-publish nito ang parehong nasuring mga release artifact
nang hindi muling nagbi-build o nag-iimbak ng API token. Ang mga naka-tag na release sa pampublikong
repository na ito ay bumubuo ng mga GitHub artifact attestation; nangangailangan ang mga pribadong fork ng suportadong
plano at tahasang opt-in. Tingnan ang
[kumpletong gabay sa pag-release](../../../docs/releasing.md) para sa pag-setup, mga eksaktong command at mga pag-ulit.

## Pag-develop

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Ang mga development tool ay nasa mga [PEP 735](https://peps.python.org/pep-0735/) dependency
group sa `pyproject.toml` (`dev`, `fuzz`, `build`), kaya hindi kailanman lumilitaw ang mga ito sa
nai-publish na package metadata. Ang `uv.lock` ay ang nag-iisang lockfile; nag-i-install ang CI gamit ang
`uv sync --locked` at nabibigo kapag luma na ang lockfile. Piliin ang interpreter gamit ang
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), o anumang Python 3.12+.

Nagpapatupad ang CI ng 90% package coverage floor. Kabilang sa mga unit test ang mga kontroladong loopback
server at mga offline na profile/history/release-validator case; pinapatakbo ng Compose lab ang
OpenSSH, MariaDB, nginx at net-snmp sa isang nakahiwalay na bridge. Patakbuhin ito gamit ang
`make test-integration`. Tingnan ang [CONTRIBUTING.md](../../../CONTRIBUTING.md) at
[mga tool sa pag-release](../../../scripts/README.md).

Ang runtime container ay tumatakbo bilang UID/GID 10001 nang walang home directory, walang shell
login at walang pip, at maaaring sumulat sa `/app/output`. Bigyan ang user na iyon ng write access sa
anumang naka-mount na output directory. Hindi ito nangangailangan ng mga capability at gumagana gamit ang isang
read-only root filesystem, kaya maaari itong patakbuhin bilang:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Ginagamit ng Nmap ang unprivileged TCP discovery behavior nito sa container na ito. Binibigo ng CI
ang image build sa anumang maaayos na HIGH o CRITICAL vulnerability na iniuulat ng Trivy.

## Mga pagsusuri sa supply-chain

Tumatakbo ang [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
sa main at lingguhan, ini-publish ang tunay nitong score, at ina-upload ang mga natuklasan sa GitHub
code scanning. Ang mga action at container base ay naka-pin sa pamamagitan ng mga hindi nagbabagong hash; ang mga Python
dependency ay nire-resolve sa `uv.lock`. Binibigo ng mga pagkabigo sa Bandit ang CI, at sinusubok ng bounded na Atheris
fuzzing ang mga SSH, MySQL, HTTP, certificate at SNMPv3 BER parser
nang walang access sa network.

Sinusukat din ng Scorecard ang makasaysayang aktibidad ng pag-review, pagkakaiba-iba ng kontribyutor, at
release provenance. Ang mga score na iyon ay sumasalamin sa aktwal na ebidensya; hindi ito mga pag-aangkin
na natutugunan ang bawat pagsusuri sa pamamahala o makasaysayang release. Tingnan ang
[SECURITY.md](../../../SECURITY.md) at [release provenance](../../../docs/releasing.md).

## Lokalisasyon

Sinusuportahan ng mga mensahe ng CLI at mga terminal summary/diff table ang 45 locale (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) nang walang dagdag na runtime dependency. Pinaparangalan ng paglutas ang `--lang`, pagkatapos ay `LC_ALL`, `LC_MESSAGES`, at `LANG`, at bumabalik sa `en`. Nananatiling hindi nagbabago ang mga JSON schema, CSV column, at export script sa lahat ng locale.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Pag-ambag

Dapat magsama ang mga kontribusyon ng isang mauulit na case, panatilihin ang mga nakadokumentong CLI at
data-format contract, at pumasa sa mga quality check sa itaas. Tingnan ang
[CONTRIBUTING.md](../../../CONTRIBUTING.md) para sa workflow ng pag-develop at
[ang gabay sa pag-release](../../../docs/releasing.md) para sa mga desisyon sa pagkatugma at pagbe-bersyon.

## Katayuan ng seguridad at lisensya

Tingnan ang [SECURITY.md](../../../SECURITY.md) para sa pribadong pag-uulat at mga suportadong bersyon.
Ang hostcensus ay lisensyado sa ilalim ng [MIT License](../../../LICENSE).

Gumagamit ang mga source header ng mga SPDX identifier at pinapanatili ang kredito ng mga kontribyutor mula sa Git
history. Tingnan ang [AUTHORS.md](../../../AUTHORS.md) para sa pagkilala. Ang mga binary test capture at ang
nabuong lockfile ay gumagamit ng mga katabing `.license` file; ang teksto ng MIT ay nasa `LICENSES/MIT.txt`.
