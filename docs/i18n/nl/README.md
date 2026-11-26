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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · **Nederlands** · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus is een Python-CLI voor herhaalbare service-inventarisatie op netwerken die u beheert.
Het legt vast wat apparaten aanbieden, vergelijkt waarnemingen in de loop van de tijd en genereert
Kadupul-importscripts. De standaardbackend gebruikt asyncio-sockets zonder rootrechten;
optionele Nmap-detectie kan hosts identificeren buiten de geconfigureerde servicepoorten.

## Waarom hostcensus

Een eenmalig poortrapport verklaart niet of een volgende waarneming is veranderd of
gewoon is mislukt. hostcensus combineert expliciete servicestatussen, begrensde probes, herbruikbare
scanprofielen en lokale geschiedenis. Beheerders kunnen dezelfde scope herhalen, fouten
inspecteren en onzekere waarnemingen onderscheiden van bevestigde wijzigingen.

- **Servicebewijs:** SSH-identificatie, MySQL-begroetingen, HTTP-headers, waarnemingen van TLS-certificaten
  en SNMP-detectie of geauthenticeerde system-MIB-query's.
- **Herhaalbare scope:** benoemde TOML-profielen, additieve uitsluitingen, configureerbare
  services, host- en probelimieten en begrensde workers.
- **Controles voorafgaand aan netwerkverkeer:** lokale preflight valideert doelen, tools,
  doeltoegang, het geschiedenisschema en geconfigureerde TLS CA-bundels.
- **Inventarisatiegeschiedenis:** transactionele SQLite-snapshots bewaren alle waarnemingen;
  vergelijkingen houden scannerfouten en onbekende statussen zichtbaar.
- **Interoperabele uitvoer:** terminal-, JSON- en CSV-rapporten, geversioneerde bestandssnapshots
  en Kadupul-importscripts.

CI dekt Python 3.12, 3.13 en 3.14 op Linux en macOS, plus een gecontroleerd Compose-integratielab.
De code gebruikt moderne type-aliassen, getypeerde preflight-resultaten,
keyword-only slotted profielen en gestructureerde async-opruiming met behoud van die
runtimeversies. Zie [Versiebeheer en releases](../../../docs/releasing.md) voor het SemVer-compatibiliteitscontract
en het GitHub-releaseproces. De releasebadge beschrijft gepubliceerde
artefacten, niet deze checkout: de laatst gepubliceerde tag is momenteel
`v0.3.0`, terwijl deze checkout pakketversie `3.0.0` gebruikt. Installeer vanuit deze checkout
om de hier gedocumenteerde inventarisatiefuncties te gebruiken.

Begin met [installatie](#install) en daarna [profielen en geschiedenis](#inventory-profiles-preflight-and-local-history).
Zie voor integratiedetails [service-fingerprints](#fingerprints),
[bestandsvergelijkingen](#inventory-diff) en [Kadupul-export](#kadupul-export).

## Installatie

Python 3.12 of nieuwer is vereist; Python 3.12–3.14 is de geteste matrix. Installeer vanuit deze
checkout de vergrendelde runtime-afhankelijkheden:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Installeer voor optionele Nmap-hostdetectie het uitvoerbare bestand van Nmap via de pakketbeheerder
van uw platform; er is geen extra Python-pakket nodig. De XML-uitvoer van Nmap wordt geparseerd met
defusedxml, een kernafhankelijkheid, zodat entity-expansie wordt geweigerd. hostcensus voert
de `nmap` die op `PATH` wordt gevonden rechtstreeks uit met een vaste argumentenlijst, een deadline die meegroeit
met de prefixgrootte en een uitvoerlimiet van 64 MiB. Nmap is niet nodig voor de standaardbackend.

## Migreren vanaf netprobe

hostcensus is de nieuwe naam van netprobe, uitgebracht in 3.0.0. Het project is nooit
onder een van beide namen op PyPI gepubliceerd, dus installaties kwamen vanuit een checkout of een GitHub-release.
De GitHub-repository behoudt zijn naam.

| Was | Nu | Compatibiliteit |
| --- | --- | --- |
| Distributie `netprobe` | `hostcensus` | Herinstalleer vanuit de checkout; er is geen pakket onder de oude naam. |
| Opdracht `netprobe` | `hostcensus` | `netprobe` werkt nog steeds en schrijft één verouderingsmelding naar stderr. Exitcodes en stdout zijn ongewijzigd. Wordt in de volgende hoofdrelease verwijderd. |
| `NETPROBE_*`-omgevingsvariabelen | `HOSTCENSUS_*` | Een `NETPROBE_*`-variabele wordt gebruikt wanneer de bijbehorende `HOSTCENSUS_*`-variabele niet is ingesteld, met één waarschuwing op stderr die de variabelenamen noemt en nooit de waarden. `HOSTCENSUS_*` gaat voor als beide zijn ingesteld. Wordt in de volgende hoofdrelease verwijderd. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Brekende wijziging.** Er is geen import-shim geïnstalleerd; werk imports bij. |
| Docker-imagetag `network-discovery:test` (alleen CI) en containergebruiker `netprobe` | `hostcensus:test`, gebruiker `hostcensus` | Er is nooit een image in een registry gepubliceerd. Bouw de image opnieuw en gebruik het `hostcensus`-entrypoint. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Een bestaand bestand met de oude standaardnaam wordt nog steeds gebruikt, met een waarschuwing, zolang de nieuwe naam niet bestaat. Expliciete `--config`- en `--history`-paden blijven ongemoeid. |
| Rapporten en snapshots met `"format": "netprobe-report"` of `"netprobe-snapshot"`, en het veld `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` en `export` laden nog steeds bestanden die onder de oude naam zijn geschreven, en de gepubliceerde JSON-schema's accepteren beide schrijfwijzen. Nieuwe bestanden gebruiken de nieuwe namen. SQLite-geschiedenisdatabases zijn ongewijzigd en laden net als voorheen. |
| Kadupul-scripts van `netprobe export` | Scripts van `hostcensus export` | Oude scripts blijven werken en lezen bij uitvoering nog steeds `NETPROBE_SNMP_*`. Nieuwe scripts lezen `HOSTCENSUS_SNMP_*`. |

## Snel voorbeeld

Uitgevoerd vanuit de testercontainer van het integratielab dat onder Ontwikkeling wordt beschreven; uitvoer ingekort:

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

## Exitcodes

| Opdracht | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | waarnemingen/rapport vastgelegd | mislukte preflight/backend, geschiedenis of schrijven van rapport/snapshot | ongeldig doel, opties, configuratie of limieten | - | `--deadline` bereikt; gedeeltelijk rapport geschreven, geschiedenis en snapshot overgeslagen |
| `preflight` | controles geslaagd | lokale controle mislukt | ongeldig doel/configuratie of conflicterende bestemmingen | - | - |
| `profiles` | gevalideerde profielen weergegeven | - | onleesbare/ongeldige configuratie of selectie | - | - |
| `history` | samenvattingen weergegeven | ontbrekende, ongeldige of niet-ondersteunde geschiedenis | ongeldige CLI-opties | - | - |
| `compare` | vergelijking opgesteld, ook wanneer er wijzigingen zijn | onleesbare geschiedenis, incompatibele scope/volgorde of schrijffout | ongeldige CLI-opties | - | - |
| `diff` | geen wijzigingen | `-o`-bestand kon niet worden geschreven | ontbrekende, onleesbare of niet-ondersteunde invoer, of een onvolledige scan zonder `--allow-partial` | wijzigingen gevonden, onbevestigde waarnemingen of een onvolledige scan | - |
| `export` | script geschreven | script kon niet worden geschreven | onleesbare invoer, een onvolledige scan zonder `--allow-partial`, of gegevens die niet veilig kunnen worden geëxporteerd | - | - |

## Indeling

| Module | Verantwoordelijkheid |
| --- | --- |
| `cli.py` | Opdrachtopties, profielresolutie, preflight, scannen en rapporteren |
| `scanner.py`, `probes.py` | Doelexpansie, begrensde workers, hostdetectie en servicewaarnemingen |
| `config.py`, `profiles.py` | Servicedefinities en gevalideerde inventarisatieprofielen |
| `models.py`, `output.py` | Resultaattypen en weergave voor terminal/JSON/CSV |
| `history.py`, `diff.py` | SQLite-geschiedenis en vergelijkingen van geversioneerde bestandssnapshots |
| `preflight.py` | Lokale controles en begrensde Nmap-versieopvraging |
| `export.py` | Gevalideerde en ge-quote Kadupul-importscripts |

Elke servicewaarneming legt de status los van de geadverteerde identiteit vast.
Leesacties en deadlines zijn begrensd; probe-uitzonderingen blijven in hostfouten staan. De SQLite-geschiedenis
gebruikt transacties, expliciete verbindingsopruiming en alleen-lezen paden voor oplijsten en
vergelijken. SNMP-geheimen komen uitsluitend binnen via omgevingsvariabelen of bestanden met geheimen;
de inventarisatiegeschiedenis slaat alleen de effectieve niet-geheime instellingen op. Zie
[Architectuur](../../../docs/architecture.md) voor de scanpijplijn, de limieten en vertrouwensgrenzen,
en [SECURITY.md](../../../SECURITY.md#authorized-use) voor geautoriseerd gebruik.


## Gebruik

Scan alleen netwerken die u zelf beheert.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Optie | Betekenis |
| --- | --- |
| `NETWORK` | CIDR, IP of hostnaam; optioneel bij `--profile`. IPv6-scope-identifiers worden geweigerd. |
| `-o, --output PATH` | Schrijf een rapport. Het formaat volgt de extensie (`.json`, `.csv`); andere extensies vallen terug op JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Forceer het rapportformaat. Heeft geen effect zonder `--output`. `.sh` selecteert `kadupul`. |
| `-v, --verbose` | Debug-logging. |
| `-q, --quiet` | Onderdruk resultaten, voortgang en informatieve logs; waarschuwingen en fouten verschijnen nog steeds op stderr. |
| `--backend asyncio\|nmap` | Hostdetectie. `asyncio` (standaard) probet de servicepoorten rechtstreeks; `nmap` voert eerst een nmap-ping-sweep uit en vereist het uitvoerbare bestand `nmap` op `PATH`. |
| `--timeout SECONDS` | Wachttijd voor probes die geen eigen budget instellen (standaard 1.0). Ingebouwde connect-probes gebruiken 0,3 s tenzij de servicetabel `timeout` instelt. |
| `--concurrency N` | Gelijktijdig actieve probes (standaard 256). |
| `--deadline SECONDS` | Stop de volledige scan, inclusief nmap-sweep, na deze tijdsduur (standaard 3600, maximaal 604800; omgevingsvariabele `HOSTCENSUS_DEADLINE`). Afgeronde hosts worden naar het rapport geschreven met `"complete": false`, er wordt geen geschiedenis of snapshot geschreven en `scan` sluit af met code 4. |
| `--config PATH` | TOML-servicedefinities en optionele benoemde `[profiles]`-instellingen. |
| `--profile NAME` | Gebruik een benoemd profiel; valt terug op `hostcensus.toml` wanneer `--config` is weggelaten. |
| `--exclude IP/CIDR` | Voeg een uitsluiting toe; herhaal naar behoefte. Een uitgesloten IPv4-host sluit ook de IPv6-adressen uit die ernaar verwijzen: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) en 6to4. IPv4-mapped doelen en uitsluitingen worden behandeld als de IPv4-adressen die ze aanduiden. |
| `--max-hosts N` | Adreslimiet die vóór uitsluitingen wordt gecontroleerd (standaard en hard maximum 65.536). |
| `--history PATH` | Leg de voltooide scan vast in een opt-in SQLite-geschiedenisdatabase. |
| `--services NAMES` | Kommagescheiden lijst van servicenamen om te controleren, in die volgorde (standaard: alle). |
| `--ports SPEC` | Kommagescheiden lijst van `NAME=PORT` (verplaats een service) of `PORT` (voeg een gewone TCP-controle toe met de naam `tcp-PORT`). |
| `--snmp-community-file PATH` | Bestand met de SNMPv2c-community voor de system-MIB-query. Omgevingsvariabele: `HOSTCENSUS_SNMP_COMMUNITY` (de waarde) of `HOSTCENSUS_SNMP_COMMUNITY_FILE` (het pad). |
| `--snmp-user` | SNMPv3-gebruiker. Omgevingsvariabele: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (standaard), `SHA224`, `SHA256`, `SHA384`, `SHA512` en een bestand met de wachtwoordzin. Omgevingsvariabele: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` of `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (standaard), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` en een bestand met de wachtwoordzin. Omgevingsvariabele: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` of `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Schrijf ook een geversioneerd snapshot voor `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifieer HTTPS-certificaten tegen deze PEM-bundel in plaats van de systeemopslag. Omgevingsvariabele: `HOSTCENSUS_TLS_CA_FILE`. |

Standaard wordt elke host gecontroleerd op SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) en HTTPS (TCP 443). TCP-poorten worden getest met een volledige connect. SNMP wordt getest met een SNMPv3 engine-discovery-verzoek, dat elke SNMPv3-agent zonder inloggegevens moet beantwoorden; agents die alleen v1/v2c ondersteunen, worden door deze probe niet gedetectecteerd. Bij de asyncio-backend telt een host als bereikbaar zodra een probe antwoord krijgt, inclusief een geweigerde verbinding, dus een host die elke probe negeert krijgt `alive=false` en de fout "Host is down"; dit bewijst niet dat de host fysiek uitstaat. Met `--backend nmap` bepaalt nmap welke hosts actief zijn (ICMP als root, anders TCP 80/443).

### Fingerprints

Elke open service krijgt een fingerprint op basis van wat deze vóór enige aanmelding verstuurt. Niets authenticeert behalve de SNMP-query, en alleen wanneer u inloggegevens opgeeft.

| Probe | Leest | `version` | `details`-sleutels |
| --- | --- | --- | --- |
| `ssh` | RFC 4253-identificatieregel | software, bijv. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Initiële MySQL/MariaDB-handshake | serverversie | `server_version`, `flavor`, `auth_plugin`, of `error_code`/`error` |
| `http` | `HEAD /`-respons | `Server`-header | `status`, `server` |
| `https` | TLS-handshake, certificaat, `HEAD /` | `Server`-header | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3-detectie; met inloggegevens GET van sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; met inloggegevens `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, of `snmp_error` |

Een hostnaamdoel wordt één keer per host geresolved en elke probe maakt verbinding met dat adres, dat als `address` in de resultaten wordt vastgelegd; de naam wordt alleen gebruikt voor TLS SNI, certificaatverificatie en de HTTP `Host`-header. Een naam die niet kan worden geresolved levert `unknown`-statussen op en de fout `Cannot resolve`. Reverse-DNS-namen worden alleen bewaard wanneer ze geldige hostnaamtekens bevatten, en er draaien maximaal 16 lookups tegelijk. HTTPS gebruikt certificaat- en hostnaamverificatie tegen de systeemopslag of `--tls-ca-file`. De truststore wordt eenmaal voor de scan geladen en hergebruikt voor elke HTTPS-probe. De TCP-connect en de TLS-handshake krijgen elk een eigen timeout, dus een poort die verbindingen accepteert maar de handshake laat hangen is `open` met `tls_error`, niet `filtered`. Als verificatie mislukt, legt het resultaat `cert_verified: false` en `cert_verify_error` vast; er wordt niet opnieuw geprobeerd met zwakkere instellingen en er wordt geen HTTP-verzoek verzonden. Certificaatgegevens en HTTP-headers worden pas verzameld nadat verificatie is geslaagd. Geef de juiste CA-bundel op voor services met een eigen CA. Oudere rapporten kunnen `cert_read_unverified` bevatten, wat huidige probes niet langer produceren.

SNMP-geheimen worden alleen gelezen uit omgevingsvariabelen of uit bestanden (`--snmp-*-file` of de bijbehorende variabele `HOSTCENSUS_SNMP_*_FILE`), nooit uit opdrachtregelwaarden die andere lokale gebruikers in de proceslijst kunnen zien. `--snmp-community`, `--snmp-auth-key` en `--snmp-priv-key` met een waarde sluiten af met code 2 en noemen het vervangende alternatief. Een bestand met een geheim moet niet-lege UTF-8 zijn van maximaal 4096 bytes; één afsluitende regeleinde wordt genegeerd, en het instellen van zowel een variabele als een bestand voor hetzelfde geheim is een fout. Foutmeldingen noemen het bestand, maar tonen nooit de inhoud. Scanrapporten en geschiedenis bevatten opzettelijk geen inlogwaarden. De exporter heeft een aparte, expliciete optie `--include-credentials` die hieronder wordt beschreven. Een community kiest SNMPv2c; een gebruiker kiest SNMPv3, met authenticatie wanneer een auth-sleutel wordt opgegeven en privacy wanneer beide sleutels worden opgegeven (`snmp_security_level` legt vast welke). hostcensus weigert, met exitcode 2, om een community te combineren met een v3-gebruiker, om een privacysleutel te gebruiken zonder auth-sleutel of om sleutels te gebruiken zonder gebruiker, en probeert een mislukte v3-query nooit opnieuw met v2c of een lager beveiligingsniveau. Agents die alleen v1/v2c spreken negeren de v3-detectie zonder inloggegevens, zodat ze alleen als open worden weergegeven wanneer een community wordt opgegeven.

Bannertekst wordt teruggebracht tot afdrukbare tekens en afgekapt op 256 tekens voordat deze wordt opgeslagen of weergegeven. Leesacties zijn ook begrensd: 4 KiB per regel, 4 KiB voor een MySQL-begroeting, 16 KiB aan HTTP-headers. Een SNMP engine ID langer dan 32 octetten wordt ingekort voordat het wordt opgeslagen. HTTP en HTTPS sturen een Host-header met een IPv6-adres tussen vierkante haken en met de poort wanneer die niet 80 of 443 is. CSV-cellen die beginnen met een teken dat een spreadsheetformule activeert, krijgen een voorvoegsel zodat de cel tekst blijft.

### Limieten

Eén uitvoering accepteert maximaal 65.536 adressen, 64 services en 524.288 probes (hosts maal services); grotere verzoeken sluiten af met code 2 voordat er iets wordt verzonden. `--concurrency` is begrensd op 4096 sockets. Elke probe heeft een harde deadline van vier keer zijn eigen budget. Connect-probes (`tcp`, `ssh`, `mysql`, `http`) gebruiken 0,3 seconden tenzij die service `timeout` instelt. SNMP en HTTPS gebruiken `--timeout` (standaard 1.0) wanneer ze er zelf geen instellen. Een probe die de deadline bereikt, wordt gerapporteerd als `unknown` met "probe timed out" in `errors`. Lokale socketfouten (bijvoorbeeld een tekort aan bestandsdescriptors) zijn ook `unknown` met de fout vastgelegd; ze tellen nooit als een gefilterde poort of een uitgeschakelde host. Vóór het proben verhoogt hostcensus de soft-limiet voor open bestanden richting de hard-limiet om ruimte te bieden voor `--concurrency` plus 64 descriptors; als dat niet lukt, faalt de `open files`-preflightcontrole en sluit `scan` af met code 1 voordat verkeer wordt verzonden. Nmap-detectie gebruikt een host-timeout van 30 seconden. Een prefix wordt in CIDR-vorm aan nmap doorgegeven en een sweep faalt met exitcode 1 wanneer nmap minder adressen rapporteert dan het heeft gekregen (bijvoorbeeld een naam die niet kan worden geresolved), in plaats van hosts als down te markeren. Een hostnaamdoel wordt eenmaal geresolved en nmap krijgt dat adres, zodat detectie en probes dezelfde machine bereiken. Een volledige prefix is één nmap-proces waarvan de subprocess-deadline 35 seconden per 256 adressen bedraagt, naar boven afgerond. Sweeps met uitsluitingen gebruiken batches van 256 hosts en een deadline van 35 seconden per batch. Het aanmaken van workers is begrensd onafhankelijk van de bereikgrootte. Reverse-DNS en hostnaamresolutie hebben een afzonderlijke deadline van twee seconden; een resolver-aanroep die nooit terugkeert wordt op zijn eigen thread achtergelaten, zodat deze hostcensus niet voorbij deze limieten kan laten draaien. Er lopen maximaal 16 lookups tegelijk en een achtergelaten aanroep behoudt zijn slot totdat hij terugkeert, zodat het aantal vastgelopen threads begrensd blijft; als alle 16 blijven hangen, wachten latere lookups op een slot buiten de deadline van twee seconden (die pas ingaat zodra een slot vrij is) totdat `--deadline` de scan stopt. `NetworkScanner` gebruikt als bibliotheek zonder `deadline` kan onbeperkt op zo'n slot wachten. `--deadline` (standaard één uur) begrenst bovenop dit alles de volledige uitvoering.

### Services configureren

Services kunnen worden gewijzigd met een TOML-bestand:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` is een van `tcp`, `ssh`, `mysql`, `http`, `https` of `snmp` en gebruikt standaard de servicenaam wanneer dat een probe is, anders `tcp`. Alleen `snmp` gebruikt UDP. Servicenamen bestaan uit kleine letters, cijfers, `-` en `_`. Twee services kunnen geen poort en protocol delen; de geschiedenis legt één status voor dat paar vast. `timeout` is optioneel, in seconden, en minimaal 0,05. Connect-achtige probes (`tcp`, `ssh`, `mysql`, `http`) gebruiken standaard 0,3 seconden. `snmp` en `https` gebruiken de `--timeout` van de scan wanneer de service geen `timeout` instelt. `--timeout` vervangt geen budget dat de service al heeft.

JSON-rapporten zijn geversioneerde documenten (`"format": "hostcensus-report"`, `"version": 1`) die naast `devices` het doel, de geprobete services en de instellingen vastleggen; `--format json` zonder `-o` schrijft het rapport naar stdout in plaats van de tabel. Elke JSON-uitvoer heeft een gepubliceerd schema; zie [JSON-uitvoer](../../../docs/json-output.md). Apparaten behouden de oorspronkelijke velden `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` en `errors` en voegen een lijst `services` toe met van elke probe `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, of `unknown` wanneer de probe lokaal faalde of de deadline bereikte), `version` en `details`. CSV-uitvoer krijgt afsluitende kolommen `services` en `versions` voor de open services. De booleans `ssh`, `snmp` en `mysql` volgen de services met exact die namen.


## Inventarisatieprofielen, preflight en lokale geschiedenis

Benoemde profielen delen een TOML-bestand met de bestaande `[services]`-definities. Kopieer
[hostcensus.example.toml](../../../hostcensus.example.toml) naar `hostcensus.toml` en stel netwerken in
die u beheert:

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

`preflight` resolveert opties en profielen exact zoals `scan` dat doet, inclusief
`--concurrency` voor de controle op open bestanden, zodat een geslaagde preflight betekent dat `scan`
met hetzelfde plan start.

Profielen accepteren `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` en `max_hosts`. `services` en `ports` gebruiken de bestaande syntaxis met kommalijsten.
Expliciete CLI-opties overschrijven profielinstellingen; herhaalde `--exclude`-opties
worden toegevoegd aan de uitsluitingen van het profiel. Een expliciet netwerk bij `--profile` moet
binnen de IP/CIDR-scope van dat profiel vallen. Hostnamen blijven ondersteund voor directe
scans, maar kunnen niet worden gecombineerd met IP-uitsluitingen. Hostlimieten gelden vóór
uitsluitingen; de totale probelimiet geldt daarna nog steeds. Uitgesloten hosts worden
weggelaten uit zowel servicecontroles als optionele Nmap-detectie.

Elke scan voert lokale preflightcontroles uit vóór doelverkeer: doel- en probelimieten,
doeltoegang, beschikbaarheid van optionele Nmap-binaries/wrappers, geschiedenisschema
en een geconfigureerde TLS CA-bundel. `preflight` rapporteert in JSON en scant geen
doelen noch maakt het een geschiedenisdatabase aan. Het schrijft tijdelijk een bestand naast het doelbestand om
doeltoegang te testen zonder bestaande inhoud te wijzigen. De standaard asyncio-backend
vereist nog steeds noch Nmap noch root. Doelpaden moeten verschillend zijn van elkaar
en van de invoerconfiguratie, inclusief hardlinks; symlinks naar bestemmingen worden
geweigerd. Mislukte controles retourneren 1; ongeldige scope of configuratie retourneert 2.

Het schrijven van rapporten en exports vereist ondersteuning voor `O_NOFOLLOW`. Op platformen zonder deze ondersteuning,
waaronder Windows, mislukken deze schrijfacties zonder de bestemming te openen of af te kappen.
Nieuwe rapporten en exportscripts zijn alleen toegankelijk voor de eigenaar (modus 0600); het vervangen van een bestaand bestand behoudt de
rechten ervan. Schrijven naar een named pipe zonder lezer mislukt direct in plaats van te wachten. Een nieuwe `--history`-database wordt ook alleen voor de eigenaar aangemaakt; een bestaande behoudt zijn modus. Logberichten gaan altijd naar stderr, zodat stdout alleen resultaten bevat. Exports met inloggegevens forceren altijd modus 0600.

Geschiedenis is opt-in en vult de bestaande JSON-snapshots en de opdracht `diff` aan:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Gebruik ID's uit `history`; het voorbeeld gaat uit van een nieuwe database. Snapshots worden
transactioneel opgeslagen met UTC start- en eindtijden, pakketversie, effectieve niet-geheime
instellingen, samenvattingen en alle host- en servicewaarnemingen, inclusief fouten per host.
Onvolledige hostwaarnemingen worden bewaard. Geannuleerde uitvoeringen worden niet opgeslagen. Bestaande
contracten voor rapporten, snapshots, exports en scan-exitcodes blijven behouden.

`history` toont JSON-samenvattingen zonder alle historische apparaat-payloads te lezen.
`compare` leest twee opgeslagen scans, vereist identieke doelidentiteiten en geselecteerde
poorten, en rapporteert wijzigingen in bereikbaarheid, status en poortstatus. De eerdere
scan-ID moet voorafgaan aan de latere ID. Wanneer beide scans `timeout` of `backend` hebben vastgelegd
en die waarden verschillen, vermeldt het rapport een waarschuwing en vergelijkt het de
waarnemingen alsnog. Een andere wachttijd kan een gefilterde poort open doen lijken. Scannerfouten
en onbekende poortwaarnemingen worden als onzeker gemarkeerd in plaats van behandeld als
bevestigde verdwijning of sluiting: hosts met fouten verschijnen in `uncertain_hosts`, en
elke poortovergang waarbij `unknown` betrokken is (inclusief unknown in beide scans) wordt vermeld
in `unconfirmed_ports` in plaats van `port_changes`, behalve een poort die in de
latere scan open is, wat een poortwijziging is. `compare` en `diff` classificeren poorten volgens dezelfde regel.
`no_longer_responding` betekent het uitblijven van een reactie, geen bewijs dat een apparaat is verwijderd.
Scan-exitcode 0 garandeert niet dat elke host heeft gereageerd: inspecteer fouten per host. Een geslaagde vergelijking retourneert 0 ongeacht of er wijzigingen zijn; bestands-`diff`
behoudt zijn exitcode 3-contract. Niet-ondersteunde of beschadigde geschiedenis retourneert 1.

Geschiedenis slaat inventarisatiegegevens op, kies dus een passend beschermde lokale
map. Profielbestanden en opgeslagen instellingen bevatten geen SNMP-inloggegevens;
de afhandeling van inloggegevens blijft lopen via de bestaande runtime-opties en omgevingsvariabelen.

## Inventarisatie-diff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Een snapshot is JSON met `format: "hostcensus-snapshot"`, `version: 1`, de hostcensus-versie, het UTC-aanmaaktijdstip, het doel, de `timeout` en `backend` van de scan wanneer die door de scan zijn vastgelegd, de geprobete services en de bereikbare hosts in dezelfde vorm als het `-o`-rapport. Onbereikbare hosts worden weggelaten. `diff` accepteert ook gewone `scan -o` JSON-rapporten, inclusief rapporten van vóór het bestaan van het veld `services`.

`diff` rapporteert nieuwe en verdwenen hosts, poorten die zijn geopend of gesloten op hosts die in beide aanwezig zijn, en services waarvan `version` is gewijzigd. Poorten die in slechts één van beide scans zijn geprobet worden niet vergeleken, en een waarschuwing meldt dit. Mislukte waarnemingen tellen nooit als "geen wijziging": een poort die in een van beide scans `unknown` is en in de latere scan niet open is, wordt vermeld onder `unconfirmed`, niet onder `closed`, met `before` als `open`, `unknown` of `not-open` (geprobet en gesloten of gefilterd) en `after` als `unknown` of `not-open`; een poort die nu open is wordt gerapporteerd onder `opened`, zelfs als de eerdere probe faalde. Een host waarvan alle probes zonder antwoord faalden in een van beide scans wordt vermeld onder `unsettled_hosts` (met `before`/`after` als `up`, `uncertain` of `absent`, ook wanneer deze in beide scans faalde of in het andere bestand ontbreekt) in plaats van `vanished_hosts`; als de host in de latere scan antwoordt, wordt deze ook gerapporteerd als een nieuwe host met zijn open poorten. Snapshots bewaren die mislukte hosts om deze reden. Er verschijnt ook een waarschuwing wanneer de doelen verschillen en wanneer beide bestanden een timeout of backend hebben vastgelegd en die waarden verschillen. `-o PATH` schrijft de JSON-vorm ook naar een bestand.

Een rapport van een scan die door `--deadline` is gestopt (`"complete": false`) bevat alleen de bereikte hosts, zodat `diff` en `export` het weigeren met exitcode 2. `--allow-partial` accepteert het met een waarschuwing op stderr: `diff` vermeldt hosts die de onvolledige scan helemaal niet vermeldde dan onder `unsettled_hosts` als `unscanned` in plaats van verdwenen (een host die als down werd vermeld is nog steeds verdwenen), zet `partial` op true en rapporteert nooit dat er geen wijzigingen zijn, en `export` schrijft een waarschuwing in de scriptheader.

Exitcodes van `diff`: `0` geen wijzigingen, `3` wijzigingen gevonden, waarnemingen die niet konden worden bevestigd of onvolledige invoer (`changed` is true zodra een lijst, inclusief `unsettled_hosts` en `unconfirmed`, niet leeg is, of `partial` true is), `2` een bestand ontbreekt, is onleesbaar, is geen ondersteund snapshot of is onvolledig zonder `--allow-partial`, `1` het `-o`-bestand kon niet worden geschreven.

## Kadupul-export

[Kadupul](https://github.com/kadupulhq/kadupul) (een fork van Cacti 1.2.31) heeft geen bulkimport van apparaten uit een bestand. De ondersteunde manier om apparaten vanuit een script toe te voegen is `cli/add_device.php`, één apparaat per aanroep, met `--option=value`-argumenten. `hostcensus export` schrijft een POSIX `sh`-script met die aanroepen:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Elke bereikbare host wordt `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hosts waarbij de SNMP-query van de scan is geslaagd, krijgen `--version=2 --community=...` of `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` voor authPriv), `--port` en `--avail=snmp`. SNMPv3-export vereist `--snmp-user`, en noAuthNoPriv wordt geweigerd omdat `add_device.php` een v3-wachtwoord vereist.
- Andere hosts krijgen `--version=0 --avail=ping`, met `--ping_method=tcp --ping_port=` de eerste open TCP-poort, of ICMP als er geen open TCP-poort is.
- `--notes` vermeldt de open services en versies. `--description` is de reverse-DNS-naam wanneer die uit gewone tekens bestaat (letters, cijfers, `.`, `_`, `-`), anders het IP-adres, en wordt uniek gemaakt omdat `add_device.php` een bestaande beschrijving behandelt als een update van dat apparaat.

Elke waarde wordt gevalideerd en voor de shell ge-quote met `shlex.quote`. Standaard wordt er geen SNMP-geheim geschreven: het script expandeert tijdens uitvoering `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` of `HOSTCENSUS_SNMP_PRIV_KEY` en stopt als een ervan niet is ingesteld. `--include-credentials` schrijft in plaats daarvan de waarden uit die omgevingsvariabelen in het script, maakt het bestand aan met modus 0600 en logt een waarschuwing. `add_device.php` zelf drukt de community af en ontvangt geheimen als argumenten, die tijdens elke aanroep zichtbaar zijn in de proceslijst van de Kadupul-server.

`add_device.php` sluit af met code 1 bij duplicaten en fouten; het script gaat door, telt het aantal fouten en sluit af met code 1 als een apparaat niet kon worden toegevoegd. Template-ID's komen uit `php cli/add_device.php --list-host-templates`. Exitcodes van `export`: `0` geschreven, `2` onleesbare invoer, een onvolledige scan zonder `--allow-partial`, of gegevens die niet veilig kunnen worden geëxporteerd, `1` het script kon niet worden geschreven.

## Versiebeheer en releaseproces

hostcensus volgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html): compatibele fixes verhogen de patch-versie, compatibele functies en deprecations verhogen de minor-versie en brekende compatibiliteitswijzigingen verhogen de major-versie. Opdrachten en opties, exitcodes en de JSON-schema's vormen het publieke contract; verouderd gedrag blijft werken tot de volgende major-release, tenzij een beveiligingsfix een eerdere wijziging vereist (het changelog legt dan uit waarom).

release-please opent een release-PR op basis van de Conventional Commit-titels op `main` en verhoogt de versies in `pyproject.toml`, `uv.lock` en `CHANGES.md`. Door deze te mergen worden de tag `vMAJOR.MINOR.PATCH` en een concept-release op GitHub aangemaakt, waaraan CI een geteste wheel, brondistributie en checksums toevoegt; GitHub slaat build-attestaties voor die bestanden op via zijn attestations-API. Een beheerder beoordeelt en publiceert het concept zodra de bestanden zijn toegevoegd. Releases worden nooit vervangen.

PyPI trusted publishing is opt-in en vereist projecteigendom, een trusted publisher en de `pypi`-omgeving. Het publiceert dezelfde gecontroleerde release-artefacten zonder opnieuw te bouwen of een API-token op te slaan. Getagde releases in deze openbare repository genereren GitHub-artefactattestaties; privéforks vereisen een ondersteund abonnement en expliciete opt-in. Zie de [volledige releasehandleiding](../../../docs/releasing.md) voor configuratie, exacte opdrachten en herpogingen.

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

Ontwikkeltools staan in [PEP 735](https://peps.python.org/pep-0735/)-afhankelijkheidsgroepen in `pyproject.toml` (`dev`, `fuzz`, `build`), zodat ze nooit in de gepubliceerde pakketmetadata verschijnen. `uv.lock` is het enige lockbestand; CI installeert met `uv sync --locked` en faalt wanneer het lockbestand verouderd is. Selecteer de interpreter met `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) of een willekeurige Python 3.12+.

CI handhaaft een ondergrens van 90% pakketdekking. Unit-tests omvatten gecontroleerde loopback-servers en offline gevallen voor profielen, geschiedenis en releasevalidators; het Compose-lab draait OpenSSH, MariaDB, nginx en net-snmp op een geïsoleerde bridge. Voer het uit met `make test-integration`. Zie [CONTRIBUTING.md](../../../CONTRIBUTING.md) en [releasetooling](../../../scripts/README.md).

De runtime-container draait als UID/GID 10001 zonder home-directory, zonder shell-login en zonder pip, en kan schrijven naar `/app/output`. Geef die gebruiker schrijftoegang tot elke gekoppelde uitvoermap. De container heeft geen capabilities nodig en werkt met een alleen-lezen root-bestandssysteem, en kan dus worden uitgevoerd als:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap gebruikt in deze container zijn niet-geprivilegieerde TCP-detectiemodus. CI laat de image-build falen bij elke oplosbare HIGH- of CRITICAL-kwetsbaarheid die Trivy rapporteert.

## Supply-chain-controles

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) draait op main en wekelijks, publiceert de daadwerkelijke score en uploadt bevindingen naar GitHub code scanning. Actions en container-basisimages zijn vastgezet met onveranderlijke hashes; Python-afhankelijkheden zijn vastgelegd in `uv.lock`. Bandit-fouten laten CI falen, en begrensde Atheris-fuzzing test de parsers voor SSH, MySQL, HTTP, certificaten en SNMPv3 BER zonder netwerktoegang.

Scorecard meet ook historische reviewactiviteit, diversiteit van bijdragers en release-herkomst. Die scores weerspiegelen feitelijk bewijs; het zijn geen beweringen dat aan elke governance- of historische releasecontrole is voldaan. Zie [SECURITY.md](../../../SECURITY.md) en [release-herkomst](../../../docs/releasing.md).

## Lokalisatie

CLI-berichten en samenvattings- en diff-tabellen in de terminal ondersteunen 45 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) zonder extra runtime-afhankelijkheden. De resolutie volgt `--lang`, daarna `LC_ALL`, `LC_MESSAGES` en `LANG`, met `en` als terugvaloptie. JSON-schema's, CSV-kolommen en exportscripts blijven in alle locales ongewijzigd.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Bijdragen

Bijdragen moeten een reproduceerbaar voorbeeld bevatten, de gedocumenteerde CLI- en gegevensformaatcontracten behouden en slagen voor de bovenstaande kwaliteitscontroles. Zie [CONTRIBUTING.md](../../../CONTRIBUTING.md) voor de ontwikkelworkflow en [de releasehandleiding](../../../docs/releasing.md) voor beslissingen rond compatibiliteit en versiebeheer.

## Beveiliging en licentiestatus

Zie [SECURITY.md](../../../SECURITY.md) voor privémeldingen en ondersteunde versies.
hostcensus is gelicentieerd onder de [MIT-licentie](../../../LICENSE).

Bronbestandskoppen gebruiken SPDX-identifiers en behouden de vermelding van bijdragers uit de Git-geschiedenis.
Zie [AUTHORS.md](../../../AUTHORS.md) voor naamsvermelding. Binaire testcaptures en het
gegenereerde lockbestand gebruiken naastgelegen `.license`-bestanden; de MIT-tekst staat in `LICENSES/MIT.txt`.
