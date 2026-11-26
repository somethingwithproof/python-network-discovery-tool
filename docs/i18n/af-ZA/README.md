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

**Afrikaans** · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus is 'n Python-CLI vir herhaalbare diensinventaris op netwerke wat jy administreer.
Dit teken aan wat toestelle blootstel, vergelyk waarnemings oor tyd heen en genereer
Kadupul-invoerskripte. Die verstek-agterkant gebruik asyncio-sokke sonder root;
opsionele Nmap-ontdekking kan gashere buite die gekonfigureerde dienspoorte identifiseer.

## Waarom hostcensus

'n Eenmalige poortverslag verduidelik nie of die volgende waarneming verander het of
bloot misluk het nie. hostcensus kombineer eksplisiete dienstoestande, begrensde sondes, herbruikbare
skanderingsprofiele en plaaslike geskiedenis. Operateurs kan dieselfde omvang herhaal, foute
inspekteer en onseker waarnemings van bevestigde veranderinge onderskei.

- **Diensbewyse:** SSH-identifikasie, MySQL-begroetings, HTTP-kopstukke, TLS-
  sertifikaatwaarnemings en SNMP-ontdekking of system-MIB-navrae met aanmeldbesonderhede.
- **Herhaalbare omvang:** benoemde TOML-profiele, additiewe uitsluitings, konfigureerbare
  dienste, gasheer-/sondeperke en begrensde werkers.
- **Kontroles voor verkeer:** plaaslike voorvlugkontrole valideer teikens, nutsmiddels,
  bestemmingstoegang, geskiedenisskema en gekonfigureerde TLS-CA-bundels.
- **Inventarisgeskiedenis:** transaksionele SQLite-kiekies behou alle waarnemings;
  vergelykings hou skandeerderfoute en onbekende toestande sigbaar.
- **Interoperabele uitvoer:** terminaal-, JSON- en CSV-verslae, weergawebeheerde lêerkiekies
  en Kadupul-invoerskripte.

CI dek Python 3.12, 3.13 en 3.14 op Linux en macOS, plus 'n beheerde Compose-
integrasielaboratorium. Die kode gebruik moderne tipe-aliasse, getipeerde voorvlugresultate,
gegleufde profiele met slegs-sleutelwoord-parameters en gestruktureerde async-skoonmaak terwyl daardie
looptydweergawes behoue bly. Sien [Weergawebeheer en vrystellings](../../../docs/releasing.md) vir die SemVer-
versoenbaarheidskontrak en GitHub-vrystellingsproses. Die vrystellingskenteken beskryf
gepubliseerde artefakte, nie die werkskopie nie: die jongste gepubliseerde merker is tans
`v0.3.0`, terwyl hierdie werkskopie pakketweergawe `3.0.0` gebruik. Installeer vanaf die werkskopie
om die inventarisfunksies wat hier gedokumenteer word, te gebruik.

Begin met [installasie](#install), dan [profiele en geskiedenis](#inventory-profiles-preflight-and-local-history).
Vir integrasiebesonderhede, sien [diensvingerafdrukke](#fingerprints),
[lêervergelykings](#inventory-diff) en [Kadupul-uitvoer](#kadupul-export).

## Installasie

Python 3.12 of nuwer word vereis; Python 3.12–3.14 is die getoetste matriks. Vanaf hierdie
werkskopie, installeer die geslote looptydafhanklikhede:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Vir opsionele Nmap-gasheerontdekking, installeer die Nmap-uitvoerbare lêer met jou platform se
pakketbestuurder; geen ekstra Python-pakket is nodig nie. Nmap se XML-uitvoer word met
defusedxml, 'n kernafhanklikheid, ontleed sodat entiteituitbreiding geweier word. hostcensus voer
die `nmap` wat op `PATH` gevind word direk uit met 'n vaste argumentlys, 'n sperdatum wat
saam met die voorvoeggrootte groei, en 'n uitvoerperk van 64 MiB. Nmap is nie nodig vir die verstek-agterkant nie.

## Migrasie vanaf netprobe

hostcensus is die nuwe naam van netprobe, vrygestel in 3.0.0. Die projek is nooit
op PyPI onder enige van die twee name gepubliseer nie, dus het installasies vanaf 'n werkskopie of 'n GitHub-
vrystelling gekom. Die GitHub-bewaarplek behou sy naam.

| Was | Nou | Versoenbaarheid |
| --- | --- | --- |
| Pakketverspreiding `netprobe` | `hostcensus` | Herinstalleer vanaf die werkskopie; daar is geen pakket onder die ou naam nie. |
| `netprobe`-opdrag | `hostcensus` | `netprobe` loop steeds en druk een verouderingsreël na stderr. Afsluitkodes en stdout bly onveranderd. Word in die volgende hoofvrystelling verwyder. |
| `NETPROBE_*`-omgewingsveranderlikes | `HOSTCENSUS_*` | 'n `NETPROBE_*`-veranderlike word gebruik wanneer sy `HOSTCENSUS_*`-eweknie nie gestel is nie, met een stderr-waarskuwing wat die veranderlikes benoem en nooit hul waardes nie. `HOSTCENSUS_*` wen wanneer albei gestel is. Word in die volgende hoofvrystelling verwyder. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Brekend.** Geen invoer-shim is geïnstalleer nie; werk invoere by. |
| Docker-beeldmerker `network-discovery:test` (slegs CI) en houergebruiker `netprobe` | `hostcensus:test`, gebruiker `hostcensus` | Geen registerbeeld is ooit gepubliseer nie. Bou die beeld weer en gebruik die `hostcensus`-toegangspunt. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | 'n Bestaande lêer met die ou versteknaam word steeds gebruik, met 'n waarskuwing, solank die nuwe naam nie bestaan nie. Eksplisiete `--config`- en `--history`-paaie bly onaangeraak. |
| Verslae en kiekies met `"format": "netprobe-report"` of `"netprobe-snapshot"`, en die `netprobe_version`-veld | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` en `export` laai steeds lêers wat onder die ou naam geskryf is, en die gepubliseerde JSON-skemas aanvaar albei spellings. Nuwe lêers gebruik die nuwe name. SQLite-geskiedenisdatabasisse is onveranderd en laai soos voorheen. |
| Kadupul-skripte vanaf `netprobe export` | Skripte vanaf `hostcensus export` | Ou skripte bly werk en lees steeds `NETPROBE_SNMP_*` wanneer hulle loop. Nuwe skripte lees `HOSTCENSUS_SNMP_*`. |

## Vinnige voorbeeld

Uitgevoer vanaf die toetshouer van die integrasielaboratorium wat onder Ontwikkeling beskryf word; uitvoer is verkort:

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

## Afsluitkodes

| Opdrag | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | waarnemings/verslag aangeteken | mislukte voorvlug/agterkant, geskiedenis, of skryf van verslag/kiekie | ongeldige teiken, opsies, konfigurasie, of perke | - | `--deadline` bereik; gedeeltelike verslag geskryf, geskiedenis en kiekie oorgeslaan |
| `preflight` | kontroles geslaag | plaaslike kontrole het misluk | ongeldige teiken/konfigurasie of botsende bestemmings | - | - |
| `profiles` | gevalideerde profiele gelys | - | onleesbare/ongeldige konfigurasie of keuse | - | - |
| `history` | opsommings gelys | ontbrekende, ongeldige, of nie-ondersteunde geskiedenis | ongeldige CLI-opsies | - | - |
| `compare` | vergelyking opgelewer, insluitend wanneer veranderinge bestaan | onleesbare geskiedenis, onversoenbare omvang/volgorde, of skryffout | ongeldige CLI-opsies | - | - |
| `diff` | geen veranderinge | `-o`-lêer kon nie geskryf word nie | ontbrekende, onleesbare of nie-ondersteunde toevoer, of 'n onvolledige skandering sonder `--allow-partial` | veranderinge gevind, onbevestigde waarnemings, of 'n onvolledige skandering | - |
| `export` | skrip geskryf | skrip kon nie geskryf word nie | onleesbare toevoer, 'n onvolledige skandering sonder `--allow-partial`, of data wat nie veilig uitgevoer kan word nie | - | - |

## Uitleg

| Module | Verantwoordelikheid |
| --- | --- |
| `cli.py` | Opdragopsies, profieloplossing, voorvlugkontrole, skandering en verslagdoening |
| `scanner.py`, `probes.py` | Teikenuitbreiding, begrensde werkers, gasheerontdekking en dienswaarnemings |
| `config.py`, `profiles.py` | Diensdefinisies en gevalideerde inventarisprofiele |
| `models.py`, `output.py` | Resultaattipes en terminaal-/JSON-/CSV-weergawe |
| `history.py`, `diff.py` | SQLite-geskiedenis en weergawebeheerde lêerkiekievergelykings |
| `preflight.py` | Plaaslike kontroles en begrensde Nmap-weergawe-opsoek |
| `export.py` | Gevalideerde en aangehaalde Kadupul-invoerskripte |

Elke dienswaarneming teken sy toestand afsonderlik van sy geadverteerde identiteit aan.
Leeswerk en sperdatums is begrens; sondefoute bly in gasheerfoute. SQLite-
geskiedenis gebruik transaksies, eksplisiete verbindingsskoonmaak en leesalleen-lys- en
vergelykingspaaie. SNMP-geheime kom slegs binne via omgewingsveranderlikes of geheim-
lêers; inventarisgeskiedenis stoor die effektiewe nie-geheime instellings. Sien
[Argitektuur](../../../docs/architecture.md) vir die skanderingspyplyn, sy perke en vertrouens-
grense, en [SECURITY.md](../../../SECURITY.md#authorized-use) vir gemagtigde gebruik.


## Gebruik

Skandeer slegs netwerke wat jy administreer.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opsie | Betekenis |
| --- | --- |
| `NETWORK` | CIDR, IP, of gasheernaam; opsioneel met `--profile`. IPv6-omvangidentifiseerders word verwerp. |
| `-o, --output PATH` | Skryf 'n verslag. Die formaat volg die uitbreiding (`.json`, `.csv`); ander uitbreidings val terug na JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Dwing die verslagformaat af. Het geen effek sonder `--output` nie. `.sh` kies `kadupul`. |
| `-v, --verbose` | Ontfoutingslogboeke. |
| `-q, --quiet` | Onderdruk resultate, vordering en inligtingslogboeke; waarskuwings en foute verskyn steeds op stderr. |
| `--backend asyncio\|nmap` | Gasheerontdekking. `asyncio` (verstek) toets die dienspoorte direk; `nmap` voer eers 'n nmap-pingveeg uit en benodig die `nmap`-uitvoerbare lêer op `PATH`. |
| `--timeout SECONDS` | Wag vir sondes wat nie hul eie begroting stel nie (verstek 1.0). Ingeboude verbindingsondes gebruik 0.3s tensy die dienstabel `timeout` stel. |
| `--concurrency N` | Sondes gelyktydig aan die gang (verstek 256). |
| `--deadline SECONDS` | Stop die hele skandering, nmap-veeg ingesluit, na hierdie tydsduur (verstek 3600, hoogstens 604800; omg. `HOSTCENSUS_DEADLINE`). Gashere wat voltooi het word na die verslag geskryf met `"complete": false`, geen geskiedenis of kiekie word geskryf nie, en `scan` sluit af met 4. |
| `--config PATH` | TOML-diensdefinisies en opsionele benoemde `[profiles]`-instellings. |
| `--profile NAME` | Gebruik 'n benoemde profiel; gebruik `hostcensus.toml` as verstek wanneer `--config` weggelaat word. |
| `--exclude IP/CIDR` | Voeg 'n uitsluiting by; herhaal soos nodig. 'n Uitgeslote IPv4-gasheer sluit ook die IPv6-adresse uit wat dit bereik: IPv4-gekarteerde (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) en 6to4. IPv4-gekarteerde teikens en uitsluitings word hanteer as die IPv4-adresse wat hulle aandui. |
| `--max-hosts N` | Adresperk wat voor uitsluitings nagegaan word (verstek/harde maksimum 65,536). |
| `--history PATH` | Teken die voltooide skandering aan in 'n opt-in SQLite-geskiedenisdatabasis. |
| `--services NAMES` | Kommageskeide lys van diensname om na te gaan, in daardie volgorde (verstek: alle). |
| `--ports SPEC` | Kommageskeide lys van `NAME=PORT` (skuif 'n diens) of `PORT` (voeg 'n gewone TCP-kontrole genaamd `tcp-PORT` by). |
| `--snmp-community-file PATH` | Lêer wat die SNMPv2c-gemeenskap vir die stelsel-MIB-navraag bevat. Omg.: `HOSTCENSUS_SNMP_COMMUNITY` (die waarde) of `HOSTCENSUS_SNMP_COMMUNITY_FILE` (die pad). |
| `--snmp-user` | SNMPv3-gebruiker. Omg.: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (verstek), `SHA224`, `SHA256`, `SHA384`, `SHA512` en 'n lêer wat die wagfrase bevat. Omg.: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` of `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (verstek), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` en 'n lêer wat die wagfrase bevat. Omg.: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` of `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Skryf ook 'n weergawebeheerde kiekie vir `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifieer HTTPS-sertifikate teen hierdie PEM-bundel in plaas van die stelselstoor. Omg.: `HOSTCENSUS_TLS_CA_FILE`. |

By verstek word elke gasheer getoets vir SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) en HTTPS (TCP 443). TCP-poorte word met 'n volle verbinding getoets. SNMP word getoets met 'n SNMPv3-enjinontdekkingsversoek, waarop enige SNMPv3-agent sonder aanmeldbesonderhede moet antwoord; agente wat slegs v1/v2c praat, sal nie deur hierdie sonde opgespoor word nie. Met die asyncio-agterkant tel 'n gasheer as lewendig wanneer enige sonde 'n antwoord kry, insluitend 'n geweierde verbinding, dus het 'n gasheer wat elke sonde laat val `alive=false` en die fout "Host is down"; dit bewys nie dat dit fisies af is nie. Met `--backend nmap` besluit nmap watter gashere lewendig is (ICMP as root, TCP 80/443 andersins).

### Vingerafdrukke

Elke oop diens word gevingerafdruk uit wat dit stuur voor enige aanmelding. Niks verifieer nie behalwe die SNMP-navraag, en slegs wanneer jy aanmeldbesonderhede verskaf.

| Sonde | Lees | `version` | `details`-sleutels |
| --- | --- | --- | --- |
| `ssh` | RFC 4253-identifikasiereël | sagteware, bv. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Aanvanklike MySQL/MariaDB-handdruk | bedienerweergawe | `server_version`, `flavor`, `auth_plugin`, of `error_code`/`error` |
| `http` | `HEAD /`-respons | `Server`-kopstuk | `status`, `server` |
| `https` | TLS-handdruk, sertifikaat, `HEAD /` | `Server`-kopstuk | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3-ontdekking; met aanmeldbesonderhede, GET van sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; met aanmeldbesonderhede `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, of `snmp_error` |

'n Gasheernaamteiken word een keer per gasheer opgelos en elke sonde verbind met daardie adres, wat as `address` in die resultate aangeteken word; die naam word slegs gebruik vir TLS SNI, sertifikaatverifikasie en die HTTP-`Host`-kopstuk. 'n Naam wat nie oplos nie, gee `unknown`-toestande en 'n `Cannot resolve`-fout. Omgekeerde DNS-name word slegs behou wanneer hulle gasheernaamkarakters bevat, en hoogstens 16 opsoeke loop gelyktydig. HTTPS gebruik sertifikaat- en gasheernaamverifikasie teen die stelselstoor of `--tls-ca-file`. Die vertrouenstoor word een keer vir die skandering gelaai en vir elke HTTPS-sonde hergebruik. Die TCP-verbinding en die TLS-handdruk word afsonderlik tydbereken, sodat 'n poort wat verbindings aanvaar maar die handdruk laat vashaak `open` met `tls_error` is, nie `filtered` nie. As verifikasie misluk, teken die resultaat `cert_verified: false` en `cert_verify_error` aan; dit probeer nie weer met swakker instellings of stuur 'n HTTP-versoek nie. Sertifikaatbesonderhede en HTTP-kopstukke word slegs versamel nadat verifikasie slaag. Verskaf die korrekte CA-bundel vir privaat-CA-dienste. Ouer verslae kan `cert_read_unverified` bevat, wat huidige sondes nie meer produseer nie.

SNMP-geheime word slegs uit omgewingsveranderlikes of uit lêers gelees (`--snmp-*-file`, of die ooreenstemmende `HOSTCENSUS_SNMP_*_FILE`-veranderlike), nooit uit opdragreëlwaardes wat ander plaaslike gebruikers in die proseslys kan sien nie. `--snmp-community`, `--snmp-auth-key` en `--snmp-priv-key` met 'n waarde sluit af met kode 2 en noem die plaasvervanger. 'n Geheimlêer moet nie-leë UTF-8 van hoogstens 4096 grepe wees; een agtervolgende nuwereël word geïgnoreer, en die stel van beide 'n veranderlike en 'n lêer vir dieselfde geheim is 'n fout. Foute benoem die lêer maar druk nooit sy inhoud nie. Skanderingsverslae en geskiedenis sluit nie opsetlik aanmeldbesonderhede in nie. Die uitvoerder het 'n afsonderlike, eksplisiete `--include-credentials`-opsie wat hieronder beskryf word. 'n Gemeenskap kies SNMPv2c; 'n gebruiker kies SNMPv3, met stawing wanneer 'n stawingsleutel gegee word en privaatheid wanneer albei sleutels gegee word (`snmp_security_level` teken aan watter een). hostcensus weier, met afsluitkode 2, om 'n gemeenskap met 'n v3-gebruiker te kombineer, om 'n privaatheidssleutel sonder 'n stawingsleutel te gebruik, of om sleutels sonder 'n gebruiker te gebruik, en dit probeer nooit weer 'n mislukte v3-navraag met v2c of 'n laer sekuriteitsvlak nie. Agente wat slegs v1/v2c praat, ignoreer die v3-ontdekking sonder aanmeldbesonderhede, dus wys hulle slegs as oop wanneer 'n gemeenskap verskaf word.

Banierteks word tot drukbare karakters gereduseer en tot 256 karakters beperk voordat dit gestoor of gewys word. Leeswerk is ook begrens: 4 KiB per reël, 4 KiB vir 'n MySQL-begroeting, 16 KiB se HTTP-kopstukke. 'n SNMP-enjin-ID langer as 32 oktette word afgekort voordat dit gestoor word. HTTP en HTTPS stuur 'n Host-kopstuk met 'n IPv6-adres tussen hakies en met die poort wanneer dit nie 80 of 443 is nie. CSV-selle wat met 'n sigbladformule-sneller begin, kry 'n voorvoegsel sodat die sel teks bly.

### Perke

Een lopie aanvaar hoogstens 65,536 adresse, 64 dienste en 524,288 sondes (gashere maal dienste); groter versoeke sluit af met kode 2 voordat enigiets gestuur word. `--concurrency` word tot 4096 sokke beperk. Elke sonde het 'n harde sperdatum van vier keer sy eie begroting. Verbindingsondes (`tcp`, `ssh`, `mysql`, `http`) gebruik 0.3 sekondes tensy daardie diens `timeout` stel. SNMP en HTTPS gebruik `--timeout` (verstek 1.0) wanneer hulle nie een stel nie. 'n Sonde wat die sperdatum tref, word aangemeld as `unknown` met "probe timed out" in `errors`. Plaaslike sokfoute (byvoorbeeld om sonder lêerbeskrywers te raak) is ook `unknown` met die fout aangeteken; hulle tel nooit as 'n gefiltreerde poort of 'n af-gasheer nie. Voordat daar gesondeer word, verhoog hostcensus die sagte perk vir oop lêers na die harde perk om `--concurrency` plus 64 beskrywers te pas; wanneer dit nie kan nie, misluk die `open files`-voorvlugkontrole en `scan` sluit af met 1 voordat verkeer gestuur word. Nmap-ontdekking gebruik 'n 30-sekonde-gasheertydperk. 'n Voorvoeg word in CIDR-vorm aan nmap deurgegee, en 'n veeg misluk met afsluitkode 1 wanneer nmap minder adresse rapporteer as wat aan hom gegee is (byvoorbeeld 'n naam wat dit nie kan oplos nie) eerder as om gashere as af te merk. 'n Gasheernaamteiken word een keer opgelos en nmap kry daardie adres, sodat ontdekking en die sondes dieselfde masjien bereik. 'n Volle voorvoeg is een nmap-proses wie se subproses-sperdatum 35 sekondes vir elke 256 adresse is, opgerond. Vee met uitsluitings gebruik groepe van 256 gashere en 'n 35-sekonde-sperdatum vir elke groep. Werkerskepping word onafhanklik van reeksgrootte begrens. Omgekeerde DNS en gasheernaamoplossing het 'n afsonderlike sperdatum van twee sekondes; 'n oplosser-oproep wat nooit terugkeer nie word op sy eie draad laat vaar, sodat dit nie hostcensus verby hierdie perke kan aan die gang hou nie. Hoogstens 16 opsoeke loop gelyktydig, en 'n laatvaarde oproep behou sy gleuf totdat dit terugkeer, sodat die aantal vasgesteekte drade begrens bly; as al 16 hang, wag latere opsoeke in 'n ry vir 'n gleuf buite die twee-sekonde-sperdatum (wat begin sodra 'n gleuf vry is) totdat `--deadline` die skandering stop. `NetworkScanner` wat as 'n biblioteek sonder 'n `deadline` gebruik word, kan onbepaald vir so 'n gleuf wag. `--deadline` (verstek een uur) begrens die hele lopie bo en behalwe hierdie perke.

### Konfigurasie van dienste

Dienste kan met 'n TOML-lêer verander word:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` is een van `tcp`, `ssh`, `mysql`, `http`, `https` of `snmp` en neem die diensnaam as verstek wanneer dit 'n sonde is, anders `tcp`. Slegs `snmp` gebruik UDP. Diensname is kleinletters, syfers, `-` en `_`. Twee dienste kan nie 'n poort en protokol deel nie; geskiedenis teken een toestand vir daardie paar aan. `timeout` is opsioneel, in sekondes, en ten minste 0.05. Verbindingstyl-sondes (`tcp`, `ssh`, `mysql`, `http`) het 'n verstek van 0.3 sekondes. `snmp` en `https` gebruik die skandering se `--timeout` wanneer die diens nie `timeout` stel nie. `--timeout` vervang nie 'n begroting wat die diens reeds het nie.

JSON-verslae is weergawebeheerde dokumente (`"format": "hostcensus-report"`, `"version": 1`) wat die teiken, gesondeerde dienste en instellings langs `devices` aanteken; `--format json` sonder `-o` skryf die verslag na stdout in plaas van die tabel. Elke JSON-uitvoer het 'n gepubliseerde skema; sien [JSON-uitvoer](../../../docs/json-output.md). Toestelle behou die oorspronklike `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` en `errors`-velde en voeg 'n `services`-lys by met elke sonde se `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, of `unknown` wanneer die sonde plaaslik misluk het of sy sperdatum getref het), `version` en `details`. CSV-uitvoer kry agtervolgende `services`- en `versions`-kolomme vir die oop dienste. Die `ssh`-, `snmp`- en `mysql`-booleans volg die dienste met presies daardie name.


## Inventarisprofiele, voorvlugkontrole en plaaslike geskiedenis

Benoemde profiele deel 'n TOML-lêer met die bestaande `[services]`-definisies. Kopieer
[hostcensus.example.toml](../../../hostcensus.example.toml) na `hostcensus.toml` en stel netwerke
wat jy administreer:

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

`preflight` los opsies en profiele presies op soos `scan` dit doen, insluitend
`--concurrency` vir die oop-lêer-kontrole, sodat 'n geslaagde voorvlugkontrole beteken `scan` sal
met dieselfde plan begin.

Profiele aanvaar `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` en `max_hosts`. `services` en `ports` gebruik die bestaande kommageskeide
sintaksis. Eksplisiete CLI-opsies oorheers profielinstellings; herhaalde `--exclude`-
opsies word by profieluitsluitings gevoeg. 'n Eksplisiete netwerk met `--profile` moet
vervat wees in daardie profiel se IP/CIDR-omvang. Gasheername bly ondersteun vir direkte
skanderings, maar kan nie met IP-uitsluitings gekombineer word nie. Gasheerperke geld voor
uitsluitings; die totale sondeperk geld steeds daarna. Uitgeslote gashere word
uitgelaat uit beide dienskontroles en opsionele Nmap-ontdekking.

Elke skandering voer plaaslike voorvlugkontroles uit voor teikenverkeer: teiken-/sonde-
perke, bestemmingstoegang, opsionele Nmap-uitvoerbare/omhulsel-beskikbaarheid, geskiedenis-
skema en 'n gekonfigureerde TLS-CA-bundel. `preflight` rapporteer JSON en skandeer nie
teikens of skep 'n geskiedenisdatabasis nie. Dit skryf tydelik 'n susterlêer om
bestemmingstoegang te toets sonder om bestaande inhoud te verander. Die verstek asyncio-agterkant
vereis steeds nóg Nmap nóg root. Bestemmingspaaie moet onderskeibaar van mekaar
en die toevoer-konfigurasie wees, insluitend harde skakels; bestemmingsimboliese skakels word
verwerp. Mislukte kontroles gee 1 terug; ongeldige omvang/konfigurasie gee 2 terug.

Verslag- en uitvoerskryfwerk vereis `O_NOFOLLOW`-ondersteuning. Op platforms daarsonder,
insluitend Windows, misluk hierdie skryfwerk sonder om die bestemming oop te maak of af te kort.
Nuwe verslae en uitvoerskripte is slegs-eienaar (modus 0600); die vervanging van 'n bestaande lêer behou sy
toestemmings. Skryf na 'n benoemde pyp met geen leser nie misluk dadelik in plaas van te wag. 'n Nuwe `--history`-databasis word ook slegs-eienaar geskep; 'n bestaande een behou sy modus. Logboodskappe gaan altyd na stderr, sodat stdout slegs resultate dra. Uitvoere wat aanmeldbesonderhede bevat, dwing altyd modus 0600 af.

Geskiedenis is opt-in en vul die bestaande JSON-kiekies en `diff`-opdrag aan:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Gebruik ID's vanaf `history`; die voorbeeld veronderstel 'n nuwe databasis. Kiekies word
transaksioneel gestoor met UTC begin-/eindtye, pakketweergawe, effektiewe nie-geheime
instellings, opsommings en alle gasheer-/dienswaarnemings, insluitend per-gasheer-foute.
Onvolledige gasheerwaarnemings word behou. Gekanselleerde lopies word nie gestoor nie. Bestaande
verslag-, kiekie-, uitvoer- en skanderings-afsluitkodekontrakte bly behoue.

`history` lys JSON-opsommings sonder om alle historiese toestelladings te lees.
`compare` lees twee gestoorde skanderings, vereis identiese teikenidentiteite en geselekteerde
poorte, en rapporteer reaksievermoë-, toestand- en poorttoestandveranderinge. Die vroeër
skanderings-ID moet die later ID voorafgaan. Wanneer albei skanderings `timeout` of `backend` aangeteken het
en daardie waardes verskil, lys die verslag 'n waarskuwing en vergelyk steeds die
waarnemings. 'n Ander wagtyd kan 'n gefiltreerde poort oop laat lyk. Skandeerderfoute
en onbekende poortwaarnemings word as onseker gemerk eerder as om as
bevestigde verdwyning of sluiting behandel te word: gashere met foute verskyn in `uncertain_hosts`, en
elke poortoorgang wat `unknown` betrek (insluitend unknown in albei skanderings) word gelys
in `unconfirmed_ports` in plaas van `port_changes`, behalwe 'n poort wat oop is in die
later skandering, wat 'n poortverandering is. `compare` en `diff` klassifiseer poorte volgens dieselfde reël.
`no_longer_responding` beteken gebrek aan 'n antwoord, nie bewys van toestelverwydering nie.
Skanderingsafsluitkode 0 waarborg nie dat elke gasheer geantwoord het nie: inspekteer per-gasheer-foute. Vergelykingsukses gee 0 terug ongeag of veranderinge bestaan; bestaande lêer-`diff`
behou sy afsluitkode 3-kontrak. Nie-ondersteunde of korrupte geskiedenis gee 1 terug.

Geskiedenis stoor inventarisinligting, so kies 'n toepaslik beskermde plaaslike
gids. Profiellêers en gestoorde instellings bevat nie SNMP-aanmeldbesonderhede nie;
aanmeldbesonderhede-hantering gaan voort deur die bestaande looptydopsies/omgewing.

## Inventaris-diff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

'n Kiekie is JSON met `format: "hostcensus-snapshot"`, `version: 1`, die hostcensus-weergawe, die UTC-skeppingstyd, die teiken, die skandering se `timeout` en `backend` wanneer die skandering dit aangeteken het, die dienste wat gesondeer is, en die lewendige gashere in dieselfde vorm as die `-o`-verslag. Af-gashere word uitgelaat. `diff` aanvaar ook gewone `scan -o`-JSON-verslae, insluitend dié van voordat die `services`-veld bestaan het.

`diff` rapporteer nuwe en verdwene gashere, poorte wat oopgemaak of toegemaak het op gashere wat in albei teenwoordig is, en dienste wie se `version` verander het. Poorte wat in slegs een van die twee skanderings gesondeer is, word nie vergelyk nie, en 'n waarskuwing sê so. Mislukte waarnemings lees nooit as "geen verandering" nie: 'n poort wat `unknown` in enige van die skanderings is en nie oop in die later een nie, word onder `unconfirmed` gelys, nie `closed` nie, met `before` van `open`, `unknown` of `not-open` (gesondeer en toe of gefiltreer) en `after` van `unknown` of `not-open`; 'n poort wat nou oop is, word onder `opened` gerapporteer selfs al het die vroeër sonde misluk. 'n Gasheer wie se sondes almal sonder 'n antwoord in enige van die skanderings misluk het, word onder `unsettled_hosts` gelys (met `before`/`after` van `up`, `uncertain` of `absent`, insluitend wanneer dit in albei skanderings misluk het of in die ander lêer ontbreek) in plaas van `vanished_hosts`; as dit in die later skandering antwoord, word dit ook as 'n nuwe gasheer met sy oop poorte gerapporteer. Kiekies behou daardie mislukte gashere om hierdie rede. 'n Waarskuwing verskyn ook wanneer die teikens verskil, en wanneer albei lêers 'n timeout of backend aangeteken het en daardie waardes verskil. `-o PATH` skryf die JSON-vorm ook na 'n lêer.

'n Verslag van 'n skandering wat deur `--deadline` gestop is (`"complete": false`) lys slegs die gashere wat dit bereik het, so `diff` en `export` weier dit met afsluitkode 2. `--allow-partial` aanvaar dit met 'n waarskuwing op stderr: `diff` lys dan gashere wat die onvolledige skandering glad nie gelys het nie onder `unsettled_hosts` as `unscanned` in plaas van verdwene ('n gasheer wat dit as af gelys het, is steeds verdwene), stel `partial` op true en rapporteer nooit geen verandering nie, en `export` skryf 'n waarskuwing in die skripkopskrif.

`diff`-afsluitkodes: `0` geen veranderinge, `3` veranderinge gevind, waarnemings wat nie bevestig kon word nie, of 'n onvolledige toevoer (`changed` is true wanneer enige lys, insluitend `unsettled_hosts` en `unconfirmed`, nie-leeg is, of `partial` true is), `2` 'n lêer ontbreek, is onleesbaar, nie 'n ondersteunde kiekie nie, of onvolledig sonder `--allow-partial`, `1` die `-o`-lêer kon nie geskryf word nie.

## Kadupul-uitvoer

[Kadupul](https://github.com/kadupulhq/kadupul) ('n vurk van Cacti 1.2.31) het geen grootmaat-toestellêer-invoer nie. Sy ondersteunde manier om toestelle vanaf 'n skrip by te voeg is `cli/add_device.php`, een toestel per oproep, met `--option=value`-argumente. `hostcensus export` skryf 'n POSIX `sh`-skrip van daardie oproepe:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Elke lewendige gasheer word `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Gashere waar die skandering se SNMP-navraag geslaag het, kry `--version=2 --community=...` of `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` vir authPriv), `--port` en `--avail=snmp`. SNMPv3-uitvoer benodig `--snmp-user`, en noAuthNoPriv word geweier omdat `add_device.php` 'n v3-wagwoord vereis.
- Ander gashere kry `--version=0 --avail=ping`, met `--ping_method=tcp --ping_port=` die eerste oop TCP-poort, of ICMP indien geen.
- `--notes` lys die oop dienste en weergawes. `--description` is die omgekeerde-DNS-naam wanneer dit eenvoudig is (letters, syfers, `.`, `_`, `-`), anders die IP, en word uniek gemaak, omdat `add_device.php` 'n bestaande beskrywing as 'n opdatering aan daardie toestel hanteer.

Elke waarde word gevalideer en dop-aangehaal met `shlex.quote`. By verstek word geen SNMP-geheim geskryf nie: die skrip brei `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` of `HOSTCENSUS_SNMP_PRIV_KEY` tydens looptyd uit en stop as een nie gestel is nie. `--include-credentials` skryf in plaas daarvan die waardes uit daardie omgewingsveranderlikes in die skrip, skep dit met modus 0600 en teken 'n waarskuwing aan. `add_device.php` self druk die gemeenskap en ontvang geheime as argumente, wat in die Kadupul-bediener se proseslys sigbaar is terwyl elke oproep loop.

`add_device.php` sluit af met 1 vir duplikate en foute; die skrip gaan voort, tel mislukkings en sluit af met 1 as enige toestel nie bygevoeg is nie. Sjabloon-ID's kom vanaf `php cli/add_device.php --list-host-templates`. `export`-afsluitkodes: `0` geskryf, `2` onleesbare toevoer, 'n onvolledige skandering sonder `--allow-partial`, of data wat nie veilig uitgevoer kan word nie, `1` die skrip kon nie geskryf word nie.

## Weergawebeheer en vrystellingsproses

hostcensus volg [Semantic Versioning](https://semver.org/spec/v2.0.0.html): versoenbare
regstellings verhoog die pleisterweergawe, versoenbare funksies/verouderings verhoog die
minderweergawe, en brekende versoenbaarheidsveranderinge verhoog die hoofweergawe.
Opdragte en opsies, afsluitkodes en die JSON-skemas is die openbare kontrak;
verouderde gedrag bly werk tot die volgende hoofvrystelling, tensy 'n
sekuriteitsregstelling vereis dat dit gouer verander word (die veranderingslog sê dan waarom).

release-please open 'n vrystellings-PR vanaf die Conventional Commit-titels op `main`,
wat `pyproject.toml`, `uv.lock` en `CHANGES.md` opdateer. Deur dit saam te smelt word die
`vMAJOR.MINOR.PATCH`-merker en 'n konsep-GitHub-vrystelling geskep, waaraan CI 'n getoetste
wheel, bronverspreiding en kontrolesomme heg; GitHub stoor bou-attesterings vir
daardie lêers deur sy attesterings-API. 'n Onderhouer hersien en publiseer die
konsep sodra die lêers aangeheg is. Vrystellings word nooit vervang nie.

PyPI-vertroude publisering is opt-in en vereis projekeienaarskap, 'n vertroude
publiseerder en die `pypi`-omgewing. Dit publiseer dieselfde nagegaande vrystellingsartefakte
sonder om 'n API-teken te herbou of te stoor. Gemerkte vrystellings in hierdie openbare
bewaarplek genereer GitHub-artefak-attesterings; privaat vurke vereis 'n ondersteunde
plan en eksplisiete opt-in. Sien die
[volledige vrystellingsgids](../../../docs/releasing.md) vir opstelling, presiese opdragte en herprobeerslae.

## Ontwikkeling

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Ontwikkelingsnutsmiddels woon in [PEP 735](https://peps.python.org/pep-0735/)-afhanklikheids-
groepe in `pyproject.toml` (`dev`, `fuzz`, `build`), sodat hulle nooit in die
gepubliseerde pakketmetadata verskyn nie. `uv.lock` is die enkele slotlêer; CI installeer met
`uv sync --locked` en misluk wanneer die slotlêer verouderd is. Kies die vertolker met
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), of enige Python 3.12+.

CI dwing 'n pakketdekkingsvloer van 90% af. Eenheidstoetse sluit beheerde teruglus-
bedieners en vanlyn profiel-/geskiedenis-/vrystellingsvalideerder-gevalle in; die Compose-laboratorium voer
OpenSSH, MariaDB, nginx en net-snmp op 'n geïsoleerde brug uit. Voer dit uit met
`make test-integration`. Sien [CONTRIBUTING.md](../../../CONTRIBUTING.md) en
[vrystellingsnutsmiddels](../../../scripts/README.md).

Die looptydhouer loop as UID/GID 10001 met geen tuisgids, geen dop-
aanmelding en geen pip nie, en kan na `/app/output` skryf. Gee daardie gebruiker skryftoegang tot
enige gekoppelde uitvoergids. Dit het geen vermoëns nodig nie en werk met 'n
leesalleen-wortellêerstelsel, dus kan dit uitgevoer word as:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap gebruik sy onbevoorregte TCP-ontdekkingsgedrag in hierdie houer. CI laat
die beeldbou misluk op enige regstelbare HIGH- of CRITICAL-kwesbaarheid wat Trivy rapporteer.

## Voorsieningskettingkontroles

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
loop op main en weekliks, publiseer sy werklike telling en laai bevindinge op na GitHub-
kodeskandering. Aksies en houerbasisse word deur onveranderlike hutsings vasgepen; Python-
afhanklikhede word in `uv.lock` opgelos. Bandit-mislukkings laat CI misluk, en begrensde Atheris-
fuzzing oefen die SSH-, MySQL-, HTTP-, sertifikaat- en SNMPv3-BER-ontleders
sonder netwerktoegang.

Scorecard meet ook historiese hersieningsaktiwiteit, bydraerdiversiteit en
vrystellingsherkoms. Daardie tellings weerspieël werklike bewyse; dit is nie bewerings
dat elke bestuurs- of historiese-vrystelling-kontrole bevredig word nie. Sien
[SECURITY.md](../../../SECURITY.md) en [vrystellingsherkoms](../../../docs/releasing.md).

## Lokalisering

CLI-boodskappe en terminaal-opsommings-/diff-tabelle ondersteun 45 lokale (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) met geen bykomende looptydafhanklikhede nie. Oplossing eerbiedig `--lang`, dan `LC_ALL`, `LC_MESSAGES` en `LANG`, en val terug na `en`. JSON-skemas, CSV-kolomme en uitvoerskripte bly onveranderd oor alle lokale heen.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Bydraes

Bydraes moet 'n reproduseerbare geval insluit, die gedokumenteerde CLI- en
dataformaatkontrakte behou, en die kwaliteitskontroles hierbo slaag. Sien
[CONTRIBUTING.md](../../../CONTRIBUTING.md) vir die ontwikkelingswerkvloei en
[die vrystellingsgids](../../../docs/releasing.md) vir versoenbaarheids- en weergawebeheerbesluite.

## Sekuriteit en lisensiestatus

Sien [SECURITY.md](../../../SECURITY.md) vir privaat aanmelding en ondersteunde weergawes.
hostcensus word gelisensieer onder die [MIT-lisensie](../../../LICENSE).

Bronkopstukke gebruik SPDX-identifiseerders en behou bydraerkrediete uit Git-
geskiedenis. Sien [AUTHORS.md](../../../AUTHORS.md) vir toeskrywing. Binêre toetsopnames en die
gegenereerde slotlêer gebruik aangrensende `.license`-lêers; MIT-teks is in `LICENSES/MIT.txt`.
