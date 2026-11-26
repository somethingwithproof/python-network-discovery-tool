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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · **Svenska** · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus är ett Python-CLI för upprepningsbar tjänsteinventering i nätverk som du administrerar. Det registrerar vad enheter exponerar, jämför observationer över tid och genererar importskript för Kadupul. Standardbackend använder asyncio-sockets utan root-behörighet; valfri Nmap-upptäckt kan identifiera värdar utöver de konfigurerade tjänsteportarna.

## Varför hostcensus

En enstaka portrapport förklarar inte om nästa observation ändrades eller helt enkelt misslyckades. hostcensus kombinerar explicita tjänstetillstånd, begränsade prober, återanvändbara skanningsprofiler och lokal historik. Operatörer kan upprepa samma omfattning, granska fel och skilja osäkra observationer från bekräftade förändringar.

- **Tjänstebevis:** SSH-identifiering, MySQL-hälsningar, HTTP-headers, observationer av TLS-certifikat samt SNMP-upptäckt eller autentiserade system-MIB-frågor.
- **Upprepningsbar omfattning:** namngivna TOML-profiler, additiva undantag, konfigurerbara tjänster, gränser för värdar/prober och begränsat antal parallella arbetare.
- **Kontroller före trafik:** lokal förkontroll validerar mål, verktyg, åtkomst till målfiler, historikschema och konfigurerade TLS CA-paket.
- **Inventeringshistorik:** transaktionella SQLite-ögonblicksbilder behåller alla observationer; jämförelser håller skannerfel och okända tillstånd synliga.
- **Interoperabla utdata:** terminal-, JSON- och CSV-rapporter, versionshanterade filögonblicksbilder samt importskript för Kadupul.

CI täcker Python 3.12, 3.13 och 3.14 på Linux och macOS, samt ett kontrollerat Compose-integrationslabb. Koden använder moderna typalias, typade förkontrollsresultat, keyword-only slotted-profiler och strukturerad asynkron rensning samtidigt som dessa körtidsversioner stöds. Se [Versionshantering och utgåvor](../../../docs/releasing.md) för SemVer-kompatibilitetskontraktet och GitHub-utgivningsprocessen. Utgåveemblemet beskriver publicerade artefakter, inte utcheckningen: den senaste publicerade taggen är för närvarande `v0.3.0`, medan den här utcheckningen använder paketversion `3.0.0`. Installera från utcheckningen för att använda de inventeringsfunktioner som dokumenteras här.

Börja med [installation](#install), därefter [profiler och historik](#inventory-profiles-preflight-and-local-history). För integrationsdetaljer, se [tjänstefingeravtryck](#fingerprints), [filjämförelser](#inventory-diff) och [Kadupul-export](#kadupul-export).

<a name="install"></a>

## Installation

Python 3.12 eller nyare krävs; Python 3.12–3.14 är den testade matrisen. Installera de låsta körtidsberoendena från den här utcheckningen:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

För valfri Nmap-värdupptäckt installerar du den körbara filen för Nmap via din plattforms pakethanterare; inget extra Python-paket behövs. Nmaps XML-utdata tolkas med defusedxml, ett kärnberoende, så entitetsexpansion nekas. hostcensus kör den `nmap` som hittas i `PATH` direkt med en fast argumentlista, en tidsgräns som växer med prefixstorleken och en utdatagräns på 64 MiB. Nmap behövs inte för standardbackend.

## Migrera från netprobe

hostcensus är det nya namnet på netprobe, släppt i 3.0.0. Projektet publicerades aldrig på PyPI under något av namnen, så installationer gjordes från en utcheckning eller en GitHub-utgåva. GitHub-arkivet behåller sitt namn.

| Var | Nu | Kompatibilitet |
| --- | --- | --- |
| Distributionen `netprobe` | `hostcensus` | Installera om från utcheckningen; det finns inget paket med det gamla namnet. |
| Kommandot `netprobe` | `hostcensus` | `netprobe` körs fortfarande och skriver ut en utfasningsrad till stderr. Avslutningskoder och stdout är oförändrade. Tas bort i nästa huvudversion. |
| Miljövariablerna `NETPROBE_*` | `HOSTCENSUS_*` | En `NETPROBE_*`-variabel används när dess `HOSTCENSUS_*`-motsvarighet inte är satt, med en varning på stderr som namnger variablerna men aldrig deras värden. `HOSTCENSUS_*` vinner när båda är satta. Tas bort i nästa huvudversion. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Brytande ändring.** Ingen importbrygga installeras; uppdatera importer. |
| Docker-avbildningstagg `network-discovery:test` (endast CI) och containeranvändare `netprobe` | `hostcensus:test`, användare `hostcensus` | Ingen registeravbildning publicerades någonsin. Bygg avbildningen igen och använd startpunkten `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | En befintlig fil med det gamla standardnamnet används fortfarande, med en varning, så länge det nya namnet inte finns. Explicita sökvägar via `--config` och `--history` påverkas inte. |
| Rapporter och ögonblicksbilder med `"format": "netprobe-report"` eller `"netprobe-snapshot"`, samt fältet `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` och `export` läser fortfarande in filer som skrivits under det gamla namnet, och de publicerade JSON Schema-specifikationerna accepterar båda stavningarna. Nya filer använder de nya namnen. SQLite-historikdatabaser är oförändrade och läses in som tidigare. |
| Kadupul-skript från `netprobe export` | Skript från `hostcensus export` | Gamla skript fortsätter att fungera och läser fortfarande `NETPROBE_SNMP_*` när de körs. Nya skript läser `HOSTCENSUS_SNMP_*`. |

## Snabbexempel

Kör från testcontainern i integrationslabbet som beskrivs under Utveckling; utdata har kortats ned:

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

## Avslutningskoder

| Kommando | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | observationer/rapport registrerade | misslyckad förkontroll/backend, historik eller skrivning av rapport/ögonblicksbild | ogiltigt mål, flaggor, konfiguration eller gränser | - | `--deadline` nådd; partiell rapport skriven, historik och ögonblicksbild hoppades över |
| `preflight` | kontroller godkända | lokal kontroll misslyckades | ogiltigt mål/konfiguration eller motstridiga målfiler | - | - |
| `profiles` | validerade profiler listade | - | oläsbar/ogiltig konfiguration eller val | - | - |
| `history` | sammanfattningar listade | saknad, ogiltig eller ej stödd historik | ogiltiga CLI-flaggor | - | - |
| `compare` | jämförelse skapad, inklusive när förändringar finns | oläsbar historik, inkompatibel omfattning/ordning eller skrivfel | ogiltiga CLI-flaggor | - | - |
| `diff` | inga förändringar | `-o`-filen kunde inte skrivas | saknad, oläsbar eller ej stödd indata, eller en ofullständig skanning utan `--allow-partial` | förändringar hittade, obekräftade observationer eller en ofullständig skanning | - |
| `export` | skript skrivet | skriptet kunde inte skrivas | oläsbar indata, en ofullständig skanning utan `--allow-partial` eller data som inte kan exporteras säkert | - | - |

## Struktur

| Modul | Ansvar |
| --- | --- |
| `cli.py` | Kommandoflaggor, profilupplösning, förkontroll, skanning och rapportering |
| `scanner.py`, `probes.py` | Målexpansion, begränsade arbetare, värdupptäckt och tjänsteobservationer |
| `config.py`, `profiles.py` | Tjänstedefinitioner och validerade inventeringsprofiler |
| `models.py`, `output.py` | Resultattyper samt terminal-/JSON-/CSV-rendering |
| `history.py`, `diff.py` | SQLite-historik och versionshanterade jämförelser av filögonblicksbilder |
| `preflight.py` | Lokala kontroller och begränsad uppslagning av Nmap-version |
| `export.py` | Validerade och citerade importskript för Kadupul |

Varje tjänsteobservation registrerar sitt tillstånd separat från sin annonserade identitet. Läsningar och tidsgränser är begränsade; probundantag behålls i värdfel. SQLite-historik använder transaktioner, explicit anslutningsrensning och skrivskyddade listnings- och jämförelsevägar. SNMP-hemligheter matas endast in via miljövariabler eller hemlighetsfiler; inventeringshistoriken lagrar de effektiva icke-hemliga inställningarna. Se [Arkitektur](../../../docs/architecture.md) för skanningspipelinen, dess gränser och förtroendegränser, samt [SECURITY.md](../../../SECURITY.md#authorized-use) för auktoriserad användning.


## Användning

Skanna endast nätverk som du administrerar.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Flagga | Betydelse |
| --- | --- |
| `NETWORK` | CIDR, IP eller värdnamn; valfritt med `--profile`. IPv6-scope-identifierare avvisas. |
| `-o, --output PATH` | Skriv en rapport. Formatet följer filändelsen (`.json`, `.csv`); övriga filändelser faller tillbaka till JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Tvinga rapportformatet. Har ingen verkan utan `--output`. `.sh` väljer `kadupul`. |
| `-v, --verbose` | Felsökningsloggning. |
| `-q, --quiet` | Dölj resultat, förlopp och informationsloggar; varningar och fel visas fortfarande på stderr. |
| `--backend asyncio\|nmap` | Värdupptäckt. `asyncio` (standard) probar tjänsteportarna direkt; `nmap` kör en nmap-ping-svepning först och kräver den körbara filen `nmap` i `PATH`. |
| `--timeout SECONDS` | Väntetid för prober som inte anger en egen budget (standard 1.0). Inbyggda anslutningsprober använder 0.3s om inte tjänstetabellen anger `timeout`. |
| `--concurrency N` | Antal samtidiga pågående prober (standard 256). |
| `--deadline SECONDS` | Stoppa hela skanningen, inklusive nmap-svepningen, efter denna tid (standard 3600, högst 604800; miljövariabel `HOSTCENSUS_DEADLINE`). Värdar som hann slutföras skrivs till rapporten med `"complete": false`, ingen historik eller ögonblicksbild skrivs, och `scan` avslutas med kod 4. |
| `--config PATH` | TOML-tjänstedefinitioner och valfria namngivna `[profiles]`-inställningar. |
| `--profile NAME` | Använd en namngiven profil; använder `hostcensus.toml` som standard när `--config` utelämnas. |
| `--exclude IP/CIDR` | Lägg till ett undantag; upprepa vid behov. En exkluderad IPv4-värd exkluderar även de IPv6-adresser som når den: IPv4-mappade (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) och 6to4. IPv4-mappade mål och undantag behandlas som de IPv4-adresser de betecknar. |
| `--max-hosts N` | Adressgräns som kontrolleras före undantag (standard/hård maxgräns 65 536). |
| `--history PATH` | Registrera den slutförda skanningen i en opt-in SQLite-historikdatabas. |
| `--services NAMES` | Kommaseparerad lista över tjänstenamn att kontrollera, i den ordningen (standard: alla). |
| `--ports SPEC` | Kommaseparerad lista av `NAME=PORT` (flytta en tjänst) eller `PORT` (lägg till en enkel TCP-kontroll med namnet `tcp-PORT`). |
| `--snmp-community-file PATH` | Fil som innehåller SNMPv2c-community för system-MIB-frågan. Miljövariabel: `HOSTCENSUS_SNMP_COMMUNITY` (värdet) eller `HOSTCENSUS_SNMP_COMMUNITY_FILE` (sökvägen). |
| `--snmp-user` | SNMPv3-användare. Miljövariabel: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (standard), `SHA224`, `SHA256`, `SHA384`, `SHA512` och en fil med lösenfrasen. Miljövariabel: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` eller `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (standard), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` och en fil med lösenfrasen. Miljövariabel: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` eller `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Skriv även en versionshanterad ögonblicksbild för `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifiera HTTPS-certifikat mot detta PEM-paket i stället för systemets certifikatarkiv. Miljövariabel: `HOSTCENSUS_TLS_CA_FILE`. |

Som standard kontrolleras varje värd för SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) och HTTPS (TCP 443). TCP-portar testas med en fullständig anslutning. SNMP testas med en SNMPv3-begäran för motorupptäckt, som varje SNMPv3-agent måste besvara utan autentiseringsuppgifter; agenter som bara talar v1/v2c upptäcks inte av denna prob. Med asyncio-backend räknas en värd som aktiv när någon prob får ett svar, inklusive en nekad anslutning, så en värd som tyst släpper varje prob får `alive=false` och felet "Host is down"; detta bevisar inte att den är fysiskt nere. Med `--backend nmap` avgör nmap vilka värdar som är aktiva (ICMP som root, annars TCP 80/443).

<a name="fingerprints"></a>

### Tjänstefingeravtryck

Varje öppen tjänst fingeravtrycksbestäms utifrån vad den skickar före eventuell inloggning. Ingenting autentiserar utom SNMP-frågan, och endast när du anger autentiseringsuppgifter.

| Prob | Läser | `version` | Nycklar i `details` |
| --- | --- | --- | --- |
| `ssh` | Identifieringsrad enligt RFC 4253 | programvara, t.ex. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Initial handskakning för MySQL/MariaDB | serverversion | `server_version`, `flavor`, `auth_plugin`, eller `error_code`/`error` |
| `http` | `HEAD /`-svar | `Server`-header | `status`, `server` |
| `https` | TLS-handskakning, certifikat, `HEAD /` | `Server`-header | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3-upptäckt; med autentiseringsuppgifter, GET av sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; med autentiseringsuppgifter `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, eller `snmp_error` |

Ett värdnamnsmål slås upp en gång per värd och varje prob ansluter till den adressen, som registreras som `address` i resultaten; namnet används bara för TLS SNI, certifikatverifiering och HTTP-headern `Host`. Ett namn som inte går att slå upp ger tillståndet `unknown` och felet `Cannot resolve`. Omvända DNS-namn behålls bara när de innehåller giltiga värdnamnstecken, och högst 16 uppslagningar körs samtidigt. HTTPS använder certifikat- och värdnamnsverifiering mot systemets arkiv eller `--tls-ca-file`. Förtroendearkivet läses in en gång per skanning och återanvänds för varje HTTPS-prob. TCP-anslutningen och TLS-handskakningen tidsmäts separat, så en port som accepterar anslutningar men hänger sig i handskakningen rapporteras som `open` med `tls_error`, inte `filtered`. Om verifieringen misslyckas registrerar resultatet `cert_verified: false` och `cert_verify_error`; den försöker inte igen med svagare inställningar och skickar ingen HTTP-begäran. Certifikatdetaljer och HTTP-headers samlas endast in efter att verifieringen har lyckats. Ange rätt CA-paket för tjänster med privat CA. Äldre rapporter kan innehålla `cert_read_unverified`, vilket aktuella prober inte längre producerar.

SNMP-hemligheter läses bara från miljövariabler eller från filer (`--snmp-*-file`, eller motsvarande `HOSTCENSUS_SNMP_*_FILE`-variabel), aldrig från kommandoradsvärden som andra lokala användare kan se i processlistan. `--snmp-community`, `--snmp-auth-key` och `--snmp-priv-key` med ett värde avslutas med kod 2 och namnger ersättaren. En hemlighetsfil måste vara icke-tom UTF-8 på högst 4096 byte; en avslutande nyrad ignoreras, och att ange både en variabel och en fil för samma hemlighet är ett fel. Felmeddelanden namnger filen men skriver aldrig ut dess innehåll. Skanningsrapporter och historik inkluderar inte avsiktligen värden för autentiseringsuppgifter. Exportören har en separat, explicit flagga `--include-credentials` som beskrivs nedan. En community väljer SNMPv2c; en användare väljer SNMPv3, med autentisering när en auth-nyckel anges och integritet/kryptering (privacy) när båda nycklarna anges (`snmp_security_level` registrerar vilket). hostcensus vägrar, med avslutningskod 2, att kombinera en community med en v3-användare, att använda en priv-nyckel utan auth-nyckel, eller att använda nycklar utan användare, och försöker aldrig göra om en misslyckad v3-fråga med v2c eller en lägre säkerhetsnivå. Agenter som bara talar v1/v2c ignorerar den lösenordslösa v3-upptäckten, så de visas endast som öppna när en community anges.

Bannertext reduceras till utskrivbara tecken och begränsas till 256 tecken innan den lagras eller visas. Läsningar är också begränsade: 4 KiB per rad, 4 KiB för en MySQL-hälsning, 16 KiB HTTP-headers. Ett SNMP-motor-ID längre än 32 oktetter trunkeras innan det lagras. HTTP och HTTPS skickar en Host-header med en IPv6-adress inom hakparenteser och med porten när den inte är 80 eller 443. CSV-celler som börjar med en teckenföljd som utlöser en kalkylbladsformel får ett prefix så att cellen förblir text.

### Gränser

En körning accepterar högst 65 536 adresser, 64 tjänster och 524 288 prober (värdar multiplicerat med tjänster); större förfrågningar avslutas med kod 2 innan något skickas. `--concurrency` är begränsat till 4096 sockets. Varje prob har en hård tidsgräns på fyra gånger sin egen budget. Anslutningsprober (`tcp`, `ssh`, `mysql`, `http`) använder 0.3 sekunder om inte den tjänsten anger `timeout`. SNMP och HTTPS använder `--timeout` (standard 1.0) när de inte anger någon egen. En prob som når tidsgränsen rapporteras som `unknown` med "probe timed out" i `errors`. Lokala socket-fel (till exempel slut på filbeskrivare) rapporteras också som `unknown` med felet registrerat; de räknas aldrig som en filtrerad port eller en nergången värd. Före probning höjer hostcensus den mjuka gränsen för öppna filer mot den hårda gränsen för att rymma `--concurrency` plus 64 filbeskrivare; när det inte går misslyckas förkontrollen `open files` och `scan` avslutas med kod 1 innan trafik skickas. Nmap-upptäckt använder 30 sekunders värdtidsgräns. Ett prefix skickas till nmap i CIDR-form, och en svepning misslyckas med avslutningskod 1 när nmap rapporterar färre adresser än det fick (till exempel ett namn det inte kan slå upp) i stället för att markera värdar som nere. Ett värdnamnsmål slås upp en gång och nmap får den adressen, så att upptäckt och prober når samma maskin. Ett helt prefix är en enda nmap-process vars underprocesstidsgräns är 35 sekunder för varje 256 adresser, avrundat uppåt. Svepningar med undantag använder batchar om 256 värdar och en tidsgräns på 35 sekunder per batch. Skapande av arbetare begränsas oberoende av intervallstorleken. Omvänd DNS och värdnamnsuppslagning har en separat tidsgräns på två sekunder; ett uppslagningsanrop som aldrig returnerar överges på sin egen tråd så att det inte kan hålla hostcensus igång förbi dessa gränser. Högst 16 uppslagningar körs samtidigt, och ett övergivet anrop behåller sin plats tills det returnerar, så att antalet fastnade trådar förblir begränsat; om alla 16 hänger sig köar senare uppslagningar för en plats utanför tvåsekundersgränsen (som börjar när en plats blir ledig) tills `--deadline` stoppar skanningen. `NetworkScanner` använt som bibliotek utan en `deadline` kan vänta på en sådan plats på obestämd tid. `--deadline` (standard en timme) begränsar hela körningen utöver dessa gränser.

### Konfigurera tjänster

Tjänster kan ändras med en TOML-fil:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` är en av `tcp`, `ssh`, `mysql`, `http`, `https` eller `snmp` och har tjänstenamnet som standard när det är en prob, annars `tcp`. Endast `snmp` använder UDP. Tjänstenamn består av gemener, siffror, `-` och `_`. Två tjänster kan inte dela port och protokoll; historiken registrerar ett tillstånd för det paret. `timeout` är valfritt, anges i sekunder och är minst 0.05. Anslutningsbaserade prober (`tcp`, `ssh`, `mysql`, `http`) har 0.3 sekunder som standard. `snmp` och `https` använder skanningens `--timeout` när tjänsten inte anger `timeout`. `--timeout` ersätter inte en budget som tjänsten redan har.

JSON-rapporter är versionshanterade dokument (`"format": "hostcensus-report"`, `"version": 1`) som registrerar målet, probade tjänster och inställningar bredvid `devices`; `--format json` utan `-o` skriver rapporten till stdout i stället för tabellen. Varje JSON-utdata har ett publicerat schema; se [JSON-utdata](../../../docs/json-output.md). Enheter behåller de ursprungliga fälten `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` och `errors` och lägger till en `services`-lista med varje probs `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` eller `unknown` när proben misslyckades lokalt eller nådde sin tidsgräns), `version` och `details`. CSV-utdata får avslutande kolumner `services` och `versions` för de öppna tjänsterna. De booleska värdena `ssh`, `snmp` och `mysql` följer tjänsterna med exakt de namnen.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Inventeringsprofiler, förkontroll och lokal historik

Namngivna profiler delar en TOML-fil med de befintliga `[services]`-definitionerna. Kopiera [hostcensus.example.toml](../../../hostcensus.example.toml) till `hostcensus.toml` och ange nätverk som du administrerar:

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

`preflight` löser upp flaggor och profiler exakt som `scan` gör, inklusive `--concurrency` för kontrollen av öppna filer, så en godkänd förkontroll innebär att `scan` kommer att starta med samma plan.

Profiler accepterar `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency` och `max_hosts`. `services` och `ports` använder den befintliga kommaseparerade syntaxen. Explicita CLI-flaggor åsidosätter profilinställningar; upprepade `--exclude`-flaggor läggs till profilens undantag. Ett explicit nätverk tillsammans med `--profile` måste rymmas inom den profilens IP/CIDR-omfattning. Värdnamn stöds fortfarande för direkta skanningar, men kan inte kombineras med IP-undantag. Värdgränser gäller före undantag; den totala probgränsen gäller fortfarande efteråt. Exkluderade värdar utelämnas från både tjänstekontroller och valfri Nmap-upptäckt.

Varje skanning utför lokala förkontroller före måltrafik: mål-/probgränser, åtkomst till målfiler, tillgänglighet för valfri Nmap-fil/wrapper, historikschema och ett konfigurerat TLS CA-paket. `preflight` rapporterar JSON och skannar inga mål och skapar ingen historikdatabas. Den skriver tillfälligt en syskonfil för att testa skrivåtkomst till målplatsen utan att ändra befintligt innehåll. Standardbackend med asyncio kräver fortfarande varken Nmap eller root. Målsökvägar måste vara skilda från varandra och från indatakonfigurationen, inklusive hårda länkar; symlänkar som mål avvisas. Misslyckade kontroller returnerar 1; ogiltig omfattning/konfiguration returnerar 2.

Skrivningar av rapporter och exporter kräver stöd för `O_NOFOLLOW`. På plattformar utan detta stöd, inklusive Windows, misslyckas dessa skrivningar utan att öppna eller trunkera målfilen. Nya rapporter och exportskript skapas endast läs- och skrivbara för ägaren (läge 0600); att ersätta en befintlig fil bevarar dess rättigheter. Att skriva till en namngiven pipe utan läsare misslyckas omedelbart i stället för att vänta. En ny `--history`-databas skapas också endast för ägaren; en befintlig behåller sitt läge. Loggmeddelanden går alltid till stderr, så stdout bär endast resultat. Exporter som innehåller autentiseringsuppgifter tvingar alltid fram läge 0600.

Historik är opt-in och kompletterar de befintliga JSON-ögonblicksbilderna och kommandot `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Använd ID:n från `history`; exemplet förutsätter en ny databas. Ögonblicksbilder lagras transaktionellt med UTC-start-/sluttider, paketversion, effektiva icke-hemliga inställningar, sammanfattningar och alla värd-/tjänsteobservationer, inklusive fel per värd. Ofullständiga värdobservationer behålls. Avbrutna körningar sparas inte. Befintliga kontrakt för rapporter, ögonblicksbilder, exporter och avslutningskoder vid skanning bevaras.

`history` listar JSON-sammanfattningar utan att läsa in alla historiska enhetsdata. `compare` läser två sparade skanningar, kräver identiska målidentiteter och valda portar, och rapporterar förändringar i svarsbenägenhet, status och porttillstånd. Det tidigare skannings-ID:t måste föregå det senare ID:t. När båda skanningarna registrerade `timeout` eller `backend` och dessa värden skiljer sig åt, listar rapporten en varning och jämför ändå observationerna. En annan väntetid kan få en filtrerad port att se öppen ut. Skannerfel och okända portobservationer flaggas som osäkra i stället för att behandlas som bekräftat försvinnande eller stängning: värdar med fel visas i `uncertain_hosts`, och varje portövergång som involverar `unknown` (inklusive okänd i båda skanningarna) listas i `unconfirmed_ports` i stället för `port_changes`, utom en port som är öppen i den senare skanningen, vilket är en portförändring. `compare` och `diff` klassificerar portar med samma regel. `no_longer_responding` betyder uteblivet svar, inte bevis på att enheten tagits bort. Avslutningskod 0 för skanning garanterar inte att varje värd svarade: granska felen per värd. En lyckad jämförelse returnerar 0 oavsett om förändringar finns eller inte; befintlig fil-`diff` behåller sitt kontrakt med avslutningskod 3. Ej stödd eller skadad historik returnerar 1.

Historiken lagrar inventeringsinformation, så välj en lämpligt skyddad lokal katalog. Profilfiler och lagrade inställningar innehåller inte SNMP-autentiseringsuppgifter; hanteringen av autentiseringsuppgifter fortsätter via de befintliga körtidsflaggorna/miljövariablerna.

<a name="inventory-diff"></a>

## Inventeringsdiff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

En ögonblicksbild är JSON med `format: "hostcensus-snapshot"`, `version: 1`, hostcensus-versionen, UTC-tidpunkt för skapandet, målet, skanningens `timeout` och `backend` när skanningen registrerade dem, de tjänster som probades samt de aktiva värdarna i samma format som `-o`-rapporten. Nergångna värdar utelämnas. `diff` accepterar också vanliga `scan -o` JSON-rapporter, inklusive sådana från innan fältet `services` existerade.

`diff` rapporterar nya och försvunna värdar, portar som öppnats eller stängts på värdar som finns i båda, samt tjänster vars `version` har ändrats. Portar som bara probades i en av de två skanningarna jämförs inte, och en varning anger detta. Misslyckade observationer tolkas aldrig som "ingen ändring": en port som är `unknown` i endera skanningen och inte öppen i den senare listas under `unconfirmed`, inte `closed`, med `before` satt till `open`, `unknown` eller `not-open` (probad och stängd eller filtrerad) och `after` satt till `unknown` eller `not-open`; en port som är öppen nu rapporteras under `opened` även om den tidigare proben misslyckades. En värd vars samtliga prober misslyckades utan svar i endera skanningen listas under `unsettled_hosts` (med `before`/`after` satt till `up`, `uncertain` eller `absent`, inklusive när den misslyckades i båda skanningarna eller saknas i den andra filen) i stället för `vanished_hosts`; om den svarar i den senare skanningen rapporteras den också som en ny värd med sina öppna portar. Ögonblicksbilder behåller dessa misslyckade värdar av detta skäl. En varning visas också när målen skiljer sig åt, och när båda filerna registrerade en timeout eller backend och dessa värden skiljer sig åt. `-o PATH` skriver även JSON-formen till en fil.

En rapport från en skanning som stoppats av `--deadline` (`"complete": false`) listar bara de värdar den hann nå, så `diff` och `export` avvisar den med avslutningskod 2. `--allow-partial` accepterar den med en varning på stderr: `diff` listar då värdar som den ofullständiga skanningen inte listade alls under `unsettled_hosts` som `unscanned` i stället för försvunna (en värd som den listade som nere är fortfarande försvunnen), sätter `partial` till true och rapporterar aldrig ingen ändring, och `export` skriver en varning i skripthuvudet.

Avslutningskoder för `diff`: `0` inga ändringar, `3` ändringar hittade, observationer som inte kunde bekräftas eller en ofullständig indata (`changed` är true när någon lista, inklusive `unsettled_hosts` och `unconfirmed`, är icke-tom, eller när `partial` är true), `2` en fil saknas, är oläsbar, inte är en stödd ögonblicksbild eller är ofullständig utan `--allow-partial`, `1` `-o`-filen kunde inte skrivas.

## Kadupul-export

[Kadupul](https://github.com/kadupulhq/kadupul) (en förgrening av Cacti 1.2.31) har ingen massimport av enhetsfiler. Dess stödda sätt att lägga till enheter från ett skript är `cli/add_device.php`, en enhet per anrop, med `--option=value`-argument. `hostcensus export` skriver ett POSIX `sh`-skript med dessa anrop:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Varje aktiv värd blir `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Värdar där skanningens SNMP-fråga lyckades får `--version=2 --community=...` eller `--version=3 --username=... --authproto=... --password=...` (samt `--privproto`/`--privpass` för authPriv), `--port` och `--avail=snmp`. SNMPv3-export kräver `--snmp-user`, och noAuthNoPriv nekas eftersom `add_device.php` kräver ett v3-lösenord.
- Övriga värdar får `--version=0 --avail=ping`, med `--ping_method=tcp --ping_port=` satt till den första öppna TCP-porten, eller ICMP om ingen finns.
- `--notes` listar de öppna tjänsterna och versionerna. `--description` är det omvända DNS-namnet när det är enkelt (bokstäver, siffror, `.`, `_`, `-`), annars IP-adressen, och görs unikt eftersom `add_device.php` behandlar en befintlig beskrivning som en uppdatering av den enheten.

Varje värde valideras och skalciteras med `shlex.quote`. Som standard skrivs ingen SNMP-hemlighet ut: skriptet expanderar `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` eller `HOSTCENSUS_SNMP_PRIV_KEY` vid körning och stannar om någon inte är satt. `--include-credentials` skriver i stället värdena från dessa miljövariabler in i skriptet, skapar det med läge 0600 och loggar en varning. `add_device.php` självt skriver ut communityn och tar emot hemligheter som argument, vilket är synligt i Kadupul-serverns processlista medan varje anrop körs.

`add_device.php` avslutas med 1 vid dubbletter och fel; skriptet fortsätter, räknar misslyckanden och avslutas med 1 om någon enhet inte lades till. Mall-ID:n hämtas från `php cli/add_device.php --list-host-templates`. Avslutningskoder för `export`: `0` skrivet, `2` oläsbar indata, en ofullständig skanning utan `--allow-partial` eller data som inte kan exporteras säkert, `1` skriptet kunde inte skrivas.

## Versionshantering och utgivningsprocess

hostcensus följer [Semantic Versioning](https://semver.org/spec/v2.0.0.html): kompatibla rättningar ökar patchversionen, kompatibla funktioner/utfasningar ökar minorversionen och brytande kompatibilitetsändringar ökar majorversionen. Kommandon och flaggor, avslutningskoder och JSON-scheman utgör det publika kontraktet; utfasat beteende fortsätter att fungera till nästa huvudversion, om inte en säkerhetsrättning kräver att det ändras tidigare (ändringsloggen anger då varför).

release-please öppnar en release-PR utifrån Conventional Commit-titlarna på `main` och räknar upp `pyproject.toml`, `uv.lock` och `CHANGES.md`. När den slås samman skapas taggen `vMAJOR.MINOR.PATCH` och ett utkast till en GitHub-utgåva, till vilken CI bifogar en testad wheel, källkodsdistribution och kontrollsummor; GitHub lagrar byggattesteringar för dessa filer via sitt attestations-API. En underhållare granskar och publicerar utkastet när filerna har bifogats. Utgåvor ersätts aldrig.

Trusted publishing på PyPI är opt-in och kräver projektägarskap, en betrodd utgivare och miljön `pypi`. Den publicerar samma kontrollerade utgåveartefakter utan att bygga om eller lagra en API-token. Taggade utgåvor i detta publika arkiv genererar GitHub-artefaktattesteringar; privata förgreningar kräver en plan som stöder det och explicit opt-in. Se den [kompletta utgivningsguiden](../../../docs/releasing.md) för konfiguration, exakta kommandon och omförsök.

## Utveckling

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Utvecklingsverktyg ligger i [PEP 735](https://peps.python.org/pep-0735/)-beroendegrupper i `pyproject.toml` (`dev`, `fuzz`, `build`), så de förekommer aldrig i den publicerade paketmetadatan. `uv.lock` är den enda låsfilen; CI installerar med `uv sync --locked` och misslyckas när låsfilen är inaktuell. Välj tolk med `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) eller valfri Python 3.12+.

CI upprätthåller ett golv på 90 % pakettäckning. Enhetstester inkluderar kontrollerade loopback-servrar och offlinefall för profiler/historik/utgåvevalidering; Compose-labbet kör OpenSSH, MariaDB, nginx och net-snmp på en isolerad brygga. Kör det med `make test-integration`. Se [CONTRIBUTING.md](../../../CONTRIBUTING.md) och [utgivningsverktyg](../../../scripts/README.md).

Körtidscontainern körs som UID/GID 10001 utan hemkatalog, utan skalinloggning och utan pip, och kan skriva till `/app/output`. Ge den användaren skrivåtkomst till eventuella monterade utdatakataloger. Den behöver inga capabilities och fungerar med ett skrivskyddat rotfilsystem, så den kan köras som:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap använder sitt opriviligierade TCP-upptäcktsbeteende i den här containern. CI underkänner avbildningsbygget vid alla åtgärdbara HIGH- eller CRITICAL-sårbarheter som Trivy rapporterar.

## Kontroller av leveranskedjan

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) körs på main och veckovis, publicerar sitt verkliga resultat och laddar upp fynd till GitHub code scanning. Actions och containerbaser är fästa med oföränderliga hashar; Python-beroenden löses i `uv.lock`. Bandit-fel underkänner CI, och begränsad Atheris-fuzzing testar SSH-, MySQL-, HTTP-, certifikat- och SNMPv3 BER-tolkarna utan nätverksåtkomst.

Scorecard mäter också historisk granskningsaktivitet, bidragardiversitet och utgåveproveniens. Dessa poäng återspeglar faktiska belägg; de är inga påståenden om att varje styrnings- eller historisk utgåvekontroll är uppfylld. Se [SECURITY.md](../../../SECURITY.md) och [utgåveproveniens](../../../docs/releasing.md).

## Lokalisering

CLI-meddelanden och terminaltabeller för sammanfattning/diff stöder 45 språkvarianter (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) utan några extra körtidsberoenden. Valet följer `--lang`, därefter `LC_ALL`, `LC_MESSAGES` och `LANG`, med återgång till `en`. JSON-scheman, CSV-kolumner och exportskript förblir oförändrade över alla språkvarianter.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Bidra

Bidrag bör innehålla ett reproducerbart fall, bevara de dokumenterade CLI- och dataformatskontrakten samt klara kvalitetskontrollerna ovan. Se [CONTRIBUTING.md](../../../CONTRIBUTING.md) för utvecklingsarbetsflödet och [utgivningsguiden](../../../docs/releasing.md) för kompatibilitets- och versionsbeslut.

## Säkerhet och licensstatus

Se [SECURITY.md](../../../SECURITY.md) för privat rapportering och versioner som stöds. hostcensus är licensierat under [MIT-licensen](../../../LICENSE).

Källkodshuvuden använder SPDX-identifierare och bevarar bidragsgivares erkännande från Git-historiken. Se [AUTHORS.md](../../../AUTHORS.md) för tillskrivning. Binära testinfångningar och den genererade låsfilen använder intilliggande `.license`-filer; MIT-texten finns i `LICENSES/MIT.txt`.
