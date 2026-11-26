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

**Languages:** [English](../../../README.md) · **Deutsch** · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus ist eine Python-CLI für eine wiederholbare Dienstinventarisierung in Netzwerken, die Sie selbst verwalten.
Sie erfasst, welche Dienste Geräte bereitstellen, vergleicht Beobachtungen über die Zeit und erzeugt
Kadupul-Importskripte. Das Standard-Backend nutzt asyncio-Sockets ohne Root-Rechte;
eine optionale Nmap-Erkennung kann Hosts auch jenseits der konfigurierten Dienstports identifizieren.

## Warum hostcensus

Ein einmaliger Portbericht erklärt nicht, ob sich bei der nächsten Beobachtung tatsächlich etwas geändert hat
oder die Abfrage lediglich fehlgeschlagen ist. hostcensus kombiniert explizite Dienstzustände, begrenzte Probes, wiederverwendbare
Scan-Profile und einen lokalen Verlauf. Betreiber können denselben Scope wiederholt prüfen, Fehler
inspizieren und unsichere Beobachtungen von bestätigten Änderungen unterscheiden.

- **Dienstnachweise:** SSH-Identifikation, MySQL-Greetings, HTTP-Header, Beobachtungen zu
  TLS-Zertifikaten sowie SNMP-Erkennung oder authentifizierte System-MIB-Abfragen.
- **Wiederholbarer Scope:** benannte TOML-Profile, additive Ausschlüsse, konfigurierbare
  Dienste, Host-/Probe-Obergrenzen und begrenzte Worker-Pools.
- **Prüfungen vor dem Netzwerkverkehr:** ein lokaler Preflight validiert Ziele, Werkzeuge,
  Zielzugriff, das Verlaufsschema und konfigurierte TLS-CA-Bundles.
- **Inventarverlauf:** transaktionale SQLite-Snapshots behalten alle Beobachtungen;
  Vergleiche halten Scannerfehler und unbekannte Zustände sichtbar.
- **Interoperable Ausgabe:** Terminal-, JSON- und CSV-Berichte, versionierte Datei-Snapshots
  und Kadupul-Importskripte.

Die CI deckt Python 3.12, 3.13 und 3.14 unter Linux und macOS sowie ein kontrolliertes Compose-Integrationslabor ab.
Der Code nutzt moderne Type Aliases, typisierte Preflight-Ergebnisse,
keyword-only Slotted-Profile und strukturiertes asynchrones Cleanup unter Beibehaltung dieser
Laufzeitversionen. Siehe [Versionierung und Releases](../../../docs/releasing.md) für den SemVer-Kompatibilitätsvertrag
und den GitHub-Release-Prozess. Das Release-Badge beschreibt
veröffentlichte Artefakte, nicht den aktuellen Checkout: Das neueste veröffentlichte Tag ist derzeit
`v0.3.0`, während dieser Checkout die Paketversion `3.0.0` verwendet. Installieren Sie aus dem Checkout,
um die hier dokumentierten Inventarisierungsfunktionen zu nutzen.

Beginnen Sie mit der [Installation](#install) und anschließend mit [Profilen und Verlauf](#inventory-profiles-preflight-and-local-history).
Details zur Integration finden Sie unter [Dienst-Fingerprints](#fingerprints),
[Dateivergleiche](#inventory-diff) und [Kadupul-Export](#kadupul-export).

<a name="install"></a>

## Installation

Python 3.12 oder neuer ist erforderlich; Python 3.12–3.14 bildet die getestete Matrix. Installieren Sie
aus diesem Checkout heraus die gesperrten Laufzeitabhängigkeiten:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Für die optionale Nmap-Host-Erkennung installieren Sie das Nmap-Programm über den Paketmanager Ihrer
Plattform; ein zusätzliches Python-Paket ist nicht erforderlich. Die XML-Ausgabe von Nmap wird mit
defusedxml, einer Kernabhängigkeit, geparst, sodass Entity Expansion abgelehnt wird. hostcensus startet
das im `PATH` gefundene `nmap` direkt mit einer festen Argumentliste, einem Deadline-Limit, das mit
der Präfixgröße wächst, und einer Ausgabeobergrenze von 64 MiB. Für das Standard-Backend wird Nmap nicht benötigt.

## Migration von netprobe

hostcensus ist der neue Name von netprobe, veröffentlicht mit Version 3.0.0. Das Projekt wurde unter
keinem der beiden Namen auf PyPI veröffentlicht, sodass Installationen über einen Checkout oder ein
GitHub-Release erfolgten. Das GitHub-Repository behält seinen Namen.

| Vorher | Jetzt | Kompatibilität |
| --- | --- | --- |
| Distribution `netprobe` | `hostcensus` | Neuinstallation aus dem Checkout erforderlich; es gibt kein Paket mit dem alten Namen. |
| Befehl `netprobe` | `hostcensus` | `netprobe` läuft weiterhin und gibt eine Abkündigungsmeldung auf stderr aus. Exit-Codes und stdout bleiben unverändert. Wird im nächsten Major-Release entfernt. |
| Umgebungsvariablen `NETPROBE_*` | `HOSTCENSUS_*` | Eine `NETPROBE_*`-Variable wird verwendet, wenn ihr `HOSTCENSUS_*`-Gegenstück nicht gesetzt ist, begleitet von einer stderr-Warnung, die nur die Variablennamen und niemals deren Werte nennt. `HOSTCENSUS_*` hat Vorrang, wenn beide gesetzt sind. Wird im nächsten Major-Release entfernt. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Breaking Change.** Es ist kein Import-Shim installiert; passen Sie die Imports an. |
| Docker-Image-Tag `network-discovery:test` (nur CI) und Container-Benutzer `netprobe` | `hostcensus:test`, Benutzer `hostcensus` | Es wurde nie ein Registry-Image veröffentlicht. Bauen Sie das Image neu und nutzen Sie den Entrypoint `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Eine vorhandene Datei mit dem alten Standardnamen wird mit einer Warnung weiterhin verwendet, solange der neue Name nicht existiert. Explizite `--config`- und `--history`-Pfade bleiben unberührt. |
| Berichte und Snapshots mit `"format": "netprobe-report"` oder `"netprobe-snapshot"` sowie dem Feld `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` und `export` laden weiterhin Dateien, die unter dem alten Namen geschrieben wurden, und die veröffentlichten JSON-Schemas akzeptieren beide Schreibweisen. Neue Dateien verwenden die neuen Namen. SQLite-Verlaufsdatenbanken sind unverändert und lassen sich wie bisher laden. |
| Kadupul-Skripte aus `netprobe export` | Skripte aus `hostcensus export` | Alte Skripte funktionieren weiterhin und lesen beim Ausführen noch `NETPROBE_SNMP_*`. Neue Skripte lesen `HOSTCENSUS_SNMP_*`. |

## Kurzes Beispiel

Ausgeführt aus dem Tester-Container des unter Entwicklung beschriebenen Integrationslabors; Ausgabe gekürzt:

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

## Exit-Codes

| Befehl | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | Beobachtungen/Bericht erfasst | Preflight/Backend fehlgeschlagen oder Fehler beim Schreiben von Verlauf bzw. Bericht/Snapshot | ungültiges Ziel, ungültige Optionen, Konfiguration oder Limits | - | `--deadline` erreicht; Teilbericht geschrieben, Verlauf und Snapshot übersprungen |
| `preflight` | Prüfungen bestanden | lokale Prüfung fehlgeschlagen | ungültiges Ziel/Konfiguration oder widersprüchliche Zielpfade | - | - |
| `profiles` | validierte Profile aufgelistet | - | nicht lesbare/ungültige Konfiguration oder Auswahl | - | - |
| `history` | Zusammenfassungen aufgelistet | fehlender, ungültiger oder nicht unterstützter Verlauf | ungültige CLI-Optionen | - | - |
| `compare` | Vergleich erstellt, auch wenn Änderungen vorliegen | nicht lesbarer Verlauf, inkompatibler Scope/Reihenfolge oder Schreibfehler | ungültige CLI-Optionen | - | - |
| `diff` | keine Änderungen | `-o`-Datei konnte nicht geschrieben werden | fehlende, nicht lesbare oder nicht unterstützte Eingabe oder ein unvollständiger Scan ohne `--allow-partial` | Änderungen gefunden, unbestätigte Beobachtungen oder unvollständiger Scan | - |
| `export` | Skript geschrieben | Skript konnte nicht geschrieben werden | nicht lesbare Eingabe, unvollständiger Scan ohne `--allow-partial` oder Daten, die nicht sicher exportiert werden können | - | - |

## Aufbau

| Modul | Zuständigkeit |
| --- | --- |
| `cli.py` | Befehlsoptionen, Profilauflösung, Preflight, Scannen und Berichterstellung |
| `scanner.py`, `probes.py` | Zielerweiterung, begrenzte Worker, Host-Erkennung und Dienstbeobachtungen |
| `config.py`, `profiles.py` | Dienstdefinitionen und validierte Inventarprofile |
| `models.py`, `output.py` | Ergebnistypen und Terminal-/JSON-/CSV-Ausgabe |
| `history.py`, `diff.py` | SQLite-Verlauf und Vergleiche versionierter Datei-Snapshots |
| `preflight.py` | Lokale Prüfungen und begrenzte Nmap-Versionsabfrage |
| `export.py` | Validierte und korrekt gequotete Kadupul-Importskripte |

Jede Dienstbeobachtung erfasst ihren Zustand getrennt von der angekündigten Identität.
Lesevorgänge und Deadlines sind begrenzt; Probe-Ausnahmen verbleiben in den Host-Fehlern. Der SQLite-Verlauf
nutzt Transaktionen, explizites Schließen von Verbindungen sowie schreibgeschützte Listen- und
Vergleichspfade. SNMP-Secrets gelangen ausschließlich über Umgebungsvariablen oder Secret-Dateien in das System;
der Inventarverlauf speichert nur die effektiven, nicht geheimen Einstellungen. Siehe
[Architektur](../../../docs/architecture.md) für die Scan-Pipeline, ihre Limits und Vertrauensgrenzen
sowie [SECURITY.md](../../../SECURITY.md#authorized-use) zur autorisierten Nutzung.


## Verwendung

Scannen Sie nur Netzwerke, die Sie selbst verwalten.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Option | Bedeutung |
| --- | --- |
| `NETWORK` | CIDR, IP oder Hostname; bei `--profile` optional. IPv6-Scope-Identifier werden abgelehnt. |
| `-o, --output PATH` | Schreibt einen Bericht. Das Format richtet sich nach der Dateiendung (`.json`, `.csv`); andere Endungen fallen auf JSON zurück. |
| `-f, --format json\|csv\|kadupul\|auto` | Erzwingt das Berichtsformat. Hat ohne `--output` keine Wirkung. `.sh` wählt `kadupul`. |
| `-v, --verbose` | Debug-Protokollierung. |
| `-q, --quiet` | Unterdrückt Ergebnisse, Fortschritt und Informationsmeldungen; Warnungen und Fehler erscheinen weiterhin auf stderr. |
| `--backend asyncio\|nmap` | Host-Erkennung. `asyncio` (Standard) prüft die Dienstports direkt; `nmap` führt zuerst einen Nmap-Ping-Sweep aus und benötigt die ausführbare Datei `nmap` im `PATH`. |
| `--timeout SECONDS` | Wartezeit für Probes ohne eigenes Budget (Standard 1.0). Eingebaute Connect-Probes verwenden 0.3s, sofern die Diensttabelle kein `timeout` festlegt. |
| `--concurrency N` | Gleichzeitig laufende Probes (Standard 256). |
| `--deadline SECONDS` | Beendet den gesamten Scan inklusive Nmap-Sweep nach dieser Zeitspanne (Standard 3600, maximal 604800; Umgebungsvariable `HOSTCENSUS_DEADLINE`). Abgeschlossene Hosts werden mit `"complete": false` in den Bericht geschrieben, Verlauf und Snapshot werden nicht geschrieben, und `scan` endet mit Exit-Code 4. |
| `--config PATH` | TOML-Dienstdefinitionen und optionale benannte `[profiles]`-Einstellungen. |
| `--profile NAME` | Verwendet ein benanntes Profil; verwendet standardmäßig `hostcensus.toml`, wenn `--config` weggelassen wird. |
| `--exclude IP/CIDR` | Fügt einen Ausschluss hinzu; bei Bedarf wiederholen. Ein ausgeschlossener IPv4-Host schließt auch die IPv6-Adressen aus, die ihn erreichen: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) und 6to4. IPv4-mapped-Ziele und -Ausschlüsse werden wie die IPv4-Adressen behandelt, für die sie stehen. |
| `--max-hosts N` | Adresslimit, geprüft vor Ausschlüssen (Standard-/Hartlimit 65.536). |
| `--history PATH` | Speichert den abgeschlossenen Scan in einer opt-in SQLite-Verlaufsdatenbank. |
| `--services NAMES` | Kommagetrennte Liste der zu prüfenden Dienstnamen in dieser Reihenfolge (Standard: alle). |
| `--ports SPEC` | Kommagetrennte Liste von `NAME=PORT` (Dienst verschieben) oder `PORT` (einfachen TCP-Check namens `tcp-PORT` hinzufügen). |
| `--snmp-community-file PATH` | Datei mit der SNMPv2c-Community für die System-MIB-Abfrage. Umgebungsvariable: `HOSTCENSUS_SNMP_COMMUNITY` (der Wert) oder `HOSTCENSUS_SNMP_COMMUNITY_FILE` (der Pfad). |
| `--snmp-user` | SNMPv3-Benutzer. Umgebungsvariable: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (Standard), `SHA224`, `SHA256`, `SHA384`, `SHA512` und eine Datei mit der Passphrase. Umgebungsvariablen: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` oder `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (Standard), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` und eine Datei mit der Passphrase. Umgebungsvariablen: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` oder `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Schreibt zusätzlich einen versionierten Snapshot für `hostcensus diff`. |
| `--tls-ca-file PATH` | Prüft HTTPS-Zertifikate gegen dieses PEM-Bundle statt gegen den Systemspeicher. Umgebungsvariable: `HOSTCENSUS_TLS_CA_FILE`. |

Standardmäßig wird jeder Host auf SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) und HTTPS (TCP 443) geprüft. TCP-Ports werden mit einem vollständigen Connect getestet. SNMP wird mit einer SNMPv3-Engine-Discovery-Anfrage getestet, die jeder SNMPv3-Agent ohne Zugangsdaten beantworten muss; Agenten, die nur v1/v2c sprechen, werden durch diesen Probe nicht erkannt. Beim asyncio-Backend gilt ein Host als erreichbar, sobald ein Probe eine Antwort erhält, einschließlich einer abgelehnten Verbindung. Ein Host, der jeden Probe verwirft, erhält daher `alive=false` und den Fehler "Host is down"; dies beweist jedoch nicht, dass er physisch ausgeschaltet ist. Mit `--backend nmap` entscheidet nmap, welche Hosts erreichbar sind (ICMP als Root, sonst TCP 80/443).

### Fingerprints

Jeder offene Dienst wird anhand dessen identifiziert, was er vor einer Anmeldung sendet. Nichts authentifiziert sich, außer der SNMP-Abfrage, und das nur, wenn Sie Zugangsdaten angeben.

| Probe | Liest | `version` | `details`-Schlüssel |
| --- | --- | --- | --- |
| `ssh` | RFC-4253-Identifikationszeile | Software, z. B. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Initialer MySQL-/MariaDB-Handshake | Serverversion | `server_version`, `flavor`, `auth_plugin`, oder `error_code`/`error` |
| `http` | `HEAD /`-Antwort | `Server`-Header | `status`, `server` |
| `https` | TLS-Handshake, Zertifikat, `HEAD /` | `Server`-Header | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3-Discovery; mit Zugangsdaten GET von sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; mit Zugangsdaten `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` oder `snmp_error` |

Ein Hostname-Ziel wird einmal pro Host aufgelöst, und jeder Probe verbindet sich mit dieser Adresse, die in den Ergebnissen als `address` gespeichert wird; der Name wird nur für TLS SNI, die Zertifikatsprüfung und den HTTP-Header `Host` verwendet. Ein Name, der nicht aufgelöst werden kann, liefert den Zustand `unknown` und den Fehler `Cannot resolve`. Reverse-DNS-Namen werden nur übernommen, wenn sie gültige Hostname-Zeichen enthalten, und es laufen maximal 16 Abfragen gleichzeitig. HTTPS nutzt eine Zertifikats- und Hostname-Prüfung gegen den Systemspeicher oder `--tls-ca-file`. Der Trust-Store wird einmal pro Scan geladen und für jeden HTTPS-Probe wiederverwendet. TCP-Connect und TLS-Handshake werden getrennt zeitlich begrenzt, sodass ein Port, der Verbindungen annimmt, aber beim Handshake hängt, als `open` mit `tls_error` gemeldet wird und nicht als `filtered`. Schlägt die Prüfung fehl, erfasst das Ergebnis `cert_verified: false` und `cert_verify_error`; es erfolgt kein erneuter Versuch mit schwächeren Einstellungen und keine HTTP-Anfrage. Zertifikatsdetails und HTTP-Header werden erst nach erfolgreicher Prüfung erfasst. Geben Sie für Dienste mit privater CA das passende CA-Bundle an. Ältere Berichte können `cert_read_unverified` enthalten, was aktuelle Probes nicht mehr erzeugen.

SNMP-Secrets werden ausschließlich aus Umgebungsvariablen oder Dateien (`--snmp-*-file` oder der entsprechenden Variable `HOSTCENSUS_SNMP_*_FILE`) gelesen, niemals aus Kommandozeilenwerten, die andere lokale Benutzer in der Prozessliste sehen können. `--snmp-community`, `--snmp-auth-key` und `--snmp-priv-key` mit einem Wert beenden das Programm mit Exit-Code 2 und nennen den Ersatz. Eine Secret-Datei muss aus nicht leerem UTF-8 mit höchstens 4096 Bytes bestehen; ein einzelner abschließender Zeilenumbruch wird ignoriert, und das gleichzeitige Setzen einer Variable und einer Datei für dasselbe Secret ist ein Fehler. Fehlermeldungen nennen den Dateinamen, geben aber niemals den Dateiinhalt aus. Scan-Berichte und Verlauf enthalten absichtlich keine Zugangsdaten. Der Exporter verfügt über eine eigene, explizite Option `--include-credentials`, die unten beschrieben wird. Eine Community wählt SNMPv2c aus; ein Benutzer wählt SNMPv3, mit Authentifizierung bei Angabe eines Auth-Keys und mit Verschlüsselung, wenn beide Schlüssel angegeben sind (`snmp_security_level` dokumentiert die verwendete Stufe). hostcensus lehnt es mit Exit-Code 2 ab, eine Community mit einem v3-Benutzer zu kombinieren, einen Privacy-Key ohne Auth-Key zu verwenden oder Schlüssel ohne Benutzer anzugeben, und wiederholt eine fehlgeschlagene v3-Abfrage niemals mit v2c oder einer niedrigeren Sicherheitsstufe. Agenten, die nur v1/v2c sprechen, ignorieren die zugangsdatenfreie v3-Discovery und erscheinen daher nur als offen, wenn eine Community angegeben wird.

Banner-Text wird auf druckbare Zeichen reduziert und vor dem Speichern oder Anzeigen auf 256 Zeichen gekürzt. Lesevorgänge sind ebenfalls begrenzt: 4 KiB pro Zeile, 4 KiB für ein MySQL-Greeting und 16 KiB für HTTP-Header. Eine SNMP-Engine-ID mit mehr als 32 Oktetten wird vor dem Speichern gekürzt. HTTP und HTTPS senden einen Host-Header mit einer IPv6-Adresse in eckigen Klammern sowie mit Portangabe, wenn dieser nicht 80 oder 443 ist. CSV-Zellen, die mit einem Auslöser für Tabellenkalkulationsformeln beginnen, erhalten ein Präfix, damit die Zelle Text bleibt.

### Limits

Ein Lauf akzeptiert maximal 65.536 Adressen, 64 Dienste und 524.288 Probes (Hosts mal Dienste); größere Anfragen enden mit Exit-Code 2, bevor etwas gesendet wird. `--concurrency` ist auf 4096 Sockets begrenzt. Jeder Probe hat ein hartes Deadline-Limit vom Vierfachen seines eigenen Budgets. Connect-Probes (`tcp`, `ssh`, `mysql`, `http`) verwenden 0,3 Sekunden, sofern der Dienst kein `timeout` festlegt. SNMP und HTTPS nutzen `--timeout` (Standard 1.0), wenn sie keinen eigenen Wert setzen. Ein Probe, der seine Deadline erreicht, wird als `unknown` mit "probe timed out" in `errors` gemeldet. Lokale Socket-Fehler (etwa erschöpfte Dateideskriptoren) werden ebenfalls als `unknown` mit protokolliertem Fehler erfasst; sie zählen niemals als gefilterter Port oder als ausgefallener Host. Vor dem Prüfen hebt hostcensus das Soft-Limit für offene Dateien in Richtung des Hard-Limits an, damit `--concurrency` plus 64 Deskriptoren Platz haben; ist das nicht möglich, schlägt die Preflight-Prüfung `open files` fehl und `scan` beendet mit 1, bevor Traffic gesendet wird. Die Nmap-Erkennung verwendet ein Host-Timeout von 30 Sekunden. Ein Präfix wird an nmap in CIDR-Form übergeben, und ein Sweep schlägt mit Exit-Code 1 fehl, wenn nmap weniger Adressen meldet als übergeben wurden (z. B. bei einem nicht auflösbaren Namen), anstatt Hosts als down zu markieren. Ein Hostname-Ziel wird einmal aufgelöst und nmap erhält diese Adresse, sodass Erkennung und Probes denselben Rechner erreichen. Ein vollständiges Präfix ist ein einzelner nmap-Prozess, dessen Subprozess-Deadline pro 256 Adressen (aufgerundet) 35 Sekunden beträgt. Sweeps mit Ausschlüssen verwenden Batches zu je 256 Hosts und eine Deadline von 35 Sekunden pro Batch. Die Worker-Erstellung ist unabhängig von der Bereichsgröße begrenzt. Reverse-DNS und Hostname-Auflösung haben ein separates Zwei-Sekunden-Limit; ein Resolver-Aufruf, der nicht zurückkehrt, wird in seinem eigenen Thread aufgegeben, sodass er hostcensus nicht über diese Limits hinaus blockieren kann. Maximal 16 Abfragen laufen gleichzeitig, und ein aufgegebener Aufruf behält seinen Slot bis zur Rückkehr, sodass die Anzahl hängender Threads begrenzt bleibt; hängen alle 16, warten spätere Abfragen außerhalb der Zwei-Sekunden-Deadline (die erst beginnt, sobald ein Slot frei ist) auf einen freien Slot, bis `--deadline` den Scan beendet. Wird `NetworkScanner` als Bibliothek ohne `deadline` verwendet, kann er unbegrenzt auf einen solchen Slot warten. `--deadline` (Standard eine Stunde) begrenzt darüber hinaus den gesamten Lauf.

### Dienste konfigurieren

Dienste lassen sich über eine TOML-Datei anpassen:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` ist einer der Werte `tcp`, `ssh`, `mysql`, `http`, `https` oder `snmp` und entspricht standardmäßig dem Dienstnamen, sofern dieser ein Probe ist, sonst `tcp`. Nur `snmp` nutzt UDP. Dienstnamen bestehen aus Kleinbuchstaben, Ziffern, `-` und `_`. Zwei Dienste dürfen sich Port und Protokoll nicht teilen; der Verlauf speichert einen Zustand pro Paar. `timeout` ist optional, wird in Sekunden angegeben und beträgt mindestens 0.05. Connect-artige Probes (`tcp`, `ssh`, `mysql`, `http`) nutzen standardmäßig 0,3 Sekunden. `snmp` und `https` verwenden `--timeout` des Scans, wenn der Dienst kein `timeout` setzt. `--timeout` überschreibt kein Budget, das der Dienst bereits mitbringt.

JSON-Berichte sind versionierte Dokumente (`"format": "hostcensus-report"`, `"version": 1`), die neben `devices` das Ziel, die geprüften Dienste und die Einstellungen festhalten; `--format json` ohne `-o` schreibt den Bericht statt der Tabelle auf stdout. Jede JSON-Ausgabe besitzt ein veröffentlichtes Schema; siehe [JSON-Ausgabe](../../../docs/json-output.md). Geräte behalten die ursprünglichen Felder `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` und `errors` und ergänzen eine `services`-Liste mit `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` oder `unknown`, wenn der Probe lokal fehlgeschlagen ist oder seine Deadline erreicht hat), `version` und `details` für jeden Probe. Die CSV-Ausgabe erhält am Ende die Spalten `services` und `versions` für die offenen Dienste. Die Booleschen Felder `ssh`, `snmp` und `mysql` folgen den Diensten mit exakt diesen Namen.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Inventarprofile, Preflight und lokaler Verlauf

Benannte Profile teilen sich eine TOML-Datei mit den vorhandenen `[services]`-Definitionen. Kopieren Sie
[hostcensus.example.toml](../../../hostcensus.example.toml) nach `hostcensus.toml` und tragen Sie Netzwerke ein,
die Sie selbst verwalten:

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

`preflight` löst Optionen und Profile exakt so auf wie `scan`, einschließlich
`--concurrency` für die Prüfung offener Dateien, sodass ein bestandener Preflight bedeutet, dass `scan` mit
demselben Plan startet.

Profile akzeptieren `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` und `max_hosts`. `services` und `ports` verwenden die vorhandene kommagetrennte
Syntax. Explizite CLI-Optionen überschreiben Profileinstellungen; wiederholte `--exclude`-Optionen
ergänzen die Profil-Ausschlüsse. Ein explizites Netzwerk zusammen mit `--profile` muss innerhalb
des IP-/CIDR-Scopes dieses Profils liegen. Hostnamen bleiben für direkte Scans unterstützt,
können aber nicht mit IP-Ausschlüssen kombiniert werden. Host-Limits greifen vor den Ausschlüssen;
die gesamte Probe-Obergrenze gilt auch danach noch. Ausgeschlossene Hosts werden sowohl von
Dienstprüfungen als auch von der optionalen Nmap-Erkennung ausgenommen.

Jeder Scan führt vor dem Ziel-Traffic lokale Preflight-Prüfungen durch: Ziel-/Probe-Limits,
Zielzugriff, Verfügbarkeit des optionalen Nmap-Programms bzw. -Wrappers, Verlaufsschema
und ein konfiguriertes TLS-CA-Bundle. `preflight` gibt JSON aus, scannt keine Ziele
und legt keine Verlaufsdatenbank an. Zur Prüfung des Zielzugriffs legt es vorübergehend eine
Nachbardatei an, ohne vorhandene Inhalte zu verändern. Das Standard-Backend asyncio
benötigt weiterhin weder Nmap noch Root. Zielpfade müssen sich voneinander und von der
Eingabekonfiguration unterscheiden, einschließlich Hardlinks; Symlinks als Ziel werden
abgelehnt. Fehlgeschlagene Prüfungen liefern Exit-Code 1; ungültiger Scope oder ungültige Konfiguration liefert 2.

Das Schreiben von Berichten und Exporten erfordert `O_NOFOLLOW`-Unterstützung. Auf Plattformen ohne diese
Unterstützung, einschließlich Windows, schlagen diese Schreibvorgänge fehl, ohne das Ziel zu öffnen oder abzuschneiden.
Neue Berichte und Exportskripte sind nur für den Eigentümer lesbar (Modus 0600); beim Ersetzen einer
vorhandenen Datei bleiben deren Berechtigungen erhalten. Das Schreiben in eine Named Pipe ohne Leser
schlägt sofort fehl, statt zu blockieren. Eine neue `--history`-Datenbank wird ebenfalls nur für den
Eigentümer erstellt; eine bestehende behält ihren Modus. Log-Meldungen gehen immer auf stderr, sodass
stdout ausschließlich Ergebnisse trägt. Exporte, die Zugangsdaten enthalten, erzwingen immer Modus 0600.

Der Verlauf ist opt-in und ergänzt die vorhandenen JSON-Snapshots und den Befehl `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Verwenden Sie IDs aus `history`; das Beispiel geht von einer neuen Datenbank aus. Snapshots werden
transaktional mit UTC-Start-/Endzeiten, Paketversion, effektiven nicht geheimen Einstellungen,
Zusammenfassungen und allen Host-/Dienstbeobachtungen einschließlich Pro-Host-Fehlern gespeichert.
Unvollständige Host-Beobachtungen bleiben erhalten. Abgebrochene Läufe werden nicht gespeichert. Bestehende
Verträge für Berichte, Snapshots, Exporte und Scan-Exit-Codes bleiben gewahrt.

`history` listet JSON-Zusammenfassungen auf, ohne sämtliche historischen Geräte-Payloads einzulesen.
`compare` liest zwei gespeicherte Scans, verlangt identische Zielidentitäten sowie ausgewählte Ports
und meldet Änderungen bei Erreichbarkeit, Status und Port-Zuständen. Die frühere Scan-ID muss vor
der späteren ID liegen. Wenn beide Scans `timeout` oder `backend` erfasst haben und sich diese Werte
unterscheiden, gibt der Bericht eine Warnung aus und vergleicht die Beobachtungen dennoch. Eine andere
Wartezeit kann einen gefilterten Port offen erscheinen lassen. Scannerfehler und unbekannte
Port-Beobachtungen werden als unsicher markiert statt als bestätigtes Verschwinden oder Schließen behandelt:
Hosts mit Fehlern erscheinen in `uncertain_hosts`, und jeder Port-Übergang mit Beteiligung von `unknown`
(einschließlich `unknown` in beiden Scans) wird in `unconfirmed_ports` statt in `port_changes` aufgeführt,
mit Ausnahme eines Ports, der im späteren Scan offen ist und damit als Port-Änderung gilt. `compare` und
`diff` klassifizieren Ports nach derselben Regel. `no_longer_responding` bedeutet das Ausbleiben einer
Antwort, keinen Nachweis für die Entfernung des Geräts. Scan-Exit-Code 0 garantiert nicht, dass jeder
Host geantwortet hat: Prüfen Sie die Pro-Host-Fehler. Ein erfolgreicher Vergleich liefert 0, unabhängig
davon, ob Änderungen vorliegen; das bestehende Datei-`diff` behält seinen Exit-Code-3-Vertrag. Ein nicht
unterstützter oder beschädigter Verlauf liefert 1.

Der Verlauf speichert Inventarinformationen; wählen Sie daher ein entsprechend geschütztes lokales
Verzeichnis. Profildateien und gespeicherte Einstellungen enthalten keine SNMP-Zugangsdaten;
die Handhabung von Zugangsdaten erfolgt weiterhin über die bestehenden Laufzeitoptionen bzw. Umgebungsvariablen.

<a name="inventory-diff"></a>

## Inventar-Diff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Ein Snapshot ist JSON mit `format: "hostcensus-snapshot"`, `version: 1`, der hostcensus-Version, der UTC-Erstellungszeit, dem Ziel, dem `timeout` und `backend` des Scans (sofern erfasst), den geprüften Diensten und den erreichbaren Hosts in derselben Struktur wie der `-o`-Bericht. Nicht erreichbare Hosts werden weggelassen. `diff` akzeptiert auch normale `scan -o`-JSON-Berichte, einschließlich solcher aus der Zeit vor Einführung des Feldes `services`.

`diff` meldet neue und verschwundene Hosts, Ports, die auf in beiden Scans vorhandenen Hosts geöffnet oder geschlossen wurden, sowie Dienste, deren `version` sich geändert hat. Ports, die nur in einem der beiden Scans geprüft wurden, werden nicht verglichen, und eine Warnung weist darauf hin. Fehlgeschlagene Beobachtungen erscheinen niemals als "keine Änderung": Ein Port, der in einem der beiden Scans `unknown` und im späteren nicht offen ist, wird unter `unconfirmed` statt `closed` aufgeführt, mit `before` gleich `open`, `unknown` oder `not-open` (geprüft und geschlossen oder gefiltert) und `after` gleich `unknown` oder `not-open`; ein Port, der jetzt offen ist, wird unter `opened` gemeldet, selbst wenn der frühere Probe fehlgeschlagen ist. Ein Host, dessen Probes in einem der Scans alle ohne Antwort fehlgeschlagen sind, wird unter `unsettled_hosts` aufgeführt (mit `before`/`after` gleich `up`, `uncertain` oder `absent`, auch wenn er in beiden Scans fehlgeschlagen ist oder in der anderen Datei fehlt) statt unter `vanished_hosts`; antwortet er im späteren Scan, wird er zusätzlich als neuer Host mit seinen offenen Ports gemeldet. Snapshots behalten solche fehlgeschlagenen Hosts aus genau diesem Grund. Eine Warnung erscheint auch, wenn die Ziele abweichen oder wenn beide Dateien ein Timeout oder Backend erfasst haben und sich diese Werte unterscheiden. `-o PATH` schreibt die JSON-Form ebenfalls in eine Datei.

Ein Bericht aus einem durch `--deadline` gestoppten Scan (`"complete": false`) enthält nur die bis dahin erreichten Hosts, weshalb `diff` und `export` ihn mit Exit-Code 2 ablehnen. `--allow-partial` akzeptiert ihn mit einer Warnung auf stderr: `diff` führt Hosts, die der unvollständige Scan gar nicht aufführt, unter `unsettled_hosts` als `unscanned` statt als verschwunden auf (ein als down gelisteter Host gilt weiterhin als verschwunden), setzt `partial` auf true und meldet niemals keine Änderung, und `export` schreibt eine Warnung in den Skriptkopf.

Exit-Codes von `diff`: `0` keine Änderungen, `3` Änderungen gefunden, nicht bestätigbare Beobachtungen oder unvollständige Eingabe (`changed` ist true, sobald eine beliebige Liste einschließlich `unsettled_hosts` und `unconfirmed` nicht leer ist oder `partial` true ist), `2` eine Datei fehlt, ist nicht lesbar, kein unterstützter Snapshot oder ohne `--allow-partial` unvollständig, `1` die `-o`-Datei konnte nicht geschrieben werden.

## Kadupul-Export

[Kadupul](https://github.com/kadupulhq/kadupul) (ein Fork von Cacti 1.2.31) bietet keinen Massenimport aus einer Gerätedatei. Der unterstützte Weg zum Hinzufügen von Geräten per Skript ist `cli/add_device.php`, ein Gerät pro Aufruf, mit `--option=value`-Argumenten. `hostcensus export` schreibt ein POSIX-`sh`-Skript mit diesen Aufrufen:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Jeder erreichbare Host wird zu `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hosts, bei denen die SNMP-Abfrage des Scans erfolgreich war, erhalten `--version=2 --community=...` oder `--version=3 --username=... --authproto=... --password=...` (sowie `--privproto`/`--privpass` bei authPriv), `--port` und `--avail=snmp`. Der SNMPv3-Export erfordert `--snmp-user`, und noAuthNoPriv wird abgelehnt, da `add_device.php` ein v3-Passwort verlangt.
- Andere Hosts erhalten `--version=0 --avail=ping`, mit `--ping_method=tcp --ping_port=` für den ersten offenen TCP-Port oder ICMP, falls keiner offen ist.
- `--notes` listet die offenen Dienste und Versionen auf. `--description` ist der Reverse-DNS-Name, wenn er einfach ist (Buchstaben, Ziffern, `.`, `_`, `-`), sonst die IP, und wird eindeutig gemacht, weil `add_device.php` eine bereits vorhandene Beschreibung als Aktualisierung dieses Geräts behandelt.

Jeder Wert wird validiert und mit `shlex.quote` für die Shell gequotet. Standardmäßig wird kein SNMP-Secret in die Datei geschrieben: Das Skript expandiert zur Laufzeit `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` oder `HOSTCENSUS_SNMP_PRIV_KEY` und bricht ab, falls eine davon nicht gesetzt ist. `--include-credentials` schreibt stattdessen die Werte dieser Umgebungsvariablen in das Skript, legt es mit Modus 0600 an und protokolliert eine Warnung. `add_device.php` selbst gibt die Community aus und erhält Secrets als Argumente, die in der Prozessliste des Kadupul-Servers sichtbar sind, während der jeweilige Aufruf läuft.

`add_device.php` endet bei Duplikaten und Fehlern mit 1; das Skript läuft weiter, zählt Fehler und endet mit 1, falls ein Gerät nicht hinzugefügt wurde. Template-IDs stammen aus `php cli/add_device.php --list-host-templates`. Exit-Codes von `export`: `0` geschrieben, `2` nicht lesbare Eingabe, unvollständiger Scan ohne `--allow-partial` oder Daten, die nicht sicher exportiert werden können, `1` das Skript konnte nicht geschrieben werden.

## Versionierung und Release-Prozess

hostcensus folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html): kompatible
Fehlerbehebungen erhöhen die Patch-Version, kompatible Funktionen/Abkündigungen erhöhen die
Minor-Version und inkompatible Änderungen erhöhen die Major-Version.
Befehle und Optionen, Exit-Codes sowie die JSON-Schemas bilden den öffentlichen Vertrag;
abgekündigtes Verhalten funktioniert bis zum nächsten Major-Release weiter, sofern nicht eine
Sicherheitskorrektur eine frühere Änderung erfordert (das Changelog nennt dann den Grund).

release-please öffnet anhand der Conventional-Commit-Titel auf `main` einen Release-PR
und erhöht dabei `pyproject.toml`, `uv.lock` und `CHANGES.md`. Das Mergen erzeugt das
Tag `vMAJOR.MINOR.PATCH` sowie einen GitHub-Release-Entwurf, an den die CI ein getestetes
Wheel, ein Source-Distribution-Paket und Prüfsummen anhängt; GitHub speichert Build-Attestierungen für
diese Dateien über seine Attestations-API. Ein Maintainer prüft und veröffentlicht den
Entwurf, sobald die Dateien angehängt sind. Releases werden niemals ersetzt.

PyPI Trusted Publishing ist opt-in und erfordert Projekt-Ownership, einen Trusted
Publisher sowie das Environment `pypi`. Es veröffentlicht dieselben geprüften Release-Artefakte
ohne Neubau oder gespeichertes API-Token. Getaggte Releases in diesem öffentlichen
Repository erzeugen GitHub-Artifact-Attestierungen; private Forks erfordern einen unterstützten
Tarif und ein explizites Opt-in. Siehe den
[vollständigen Release-Leitfaden](../../../docs/releasing.md) für Einrichtung, genaue Befehle und Wiederholungsversuche.

## Entwicklung

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Entwicklungswerkzeuge liegen in [PEP-735](https://peps.python.org/pep-0735/)-Abhängigkeitsgruppen
in `pyproject.toml` (`dev`, `fuzz`, `build`), sodass sie niemals in den veröffentlichten
Paket-Metadaten erscheinen. `uv.lock` ist das einzige Lockfile; die CI installiert mit
`uv sync --locked` und schlägt fehl, wenn das Lockfile veraltet ist. Wählen Sie den Interpreter mit
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) oder einem beliebigen Python 3.12+.

Die CI erzwingt eine Paket-Testabdeckung von mindestens 90 %. Unit-Tests umfassen kontrollierte Loopback-Server
sowie Offline-Fälle für Profile, Verlauf und Release-Validierung; das Compose-Labor startet
OpenSSH, MariaDB, nginx und net-snmp auf einer isolierten Bridge. Starten Sie es mit
`make test-integration`. Siehe [CONTRIBUTING.md](../../../CONTRIBUTING.md) und
[Release-Tooling](../../../scripts/README.md).

Der Laufzeit-Container läuft unter UID/GID 10001 ohne Home-Verzeichnis, ohne Shell-Login
und ohne pip und darf nach `/app/output` schreiben. Geben Sie diesem Benutzer Schreibzugriff auf
jedes eingebundene Ausgabeverzeichnis. Er benötigt keine Capabilities und funktioniert mit einem
schreibgeschützten Root-Dateisystem, sodass er wie folgt gestartet werden kann:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap nutzt in diesem Container sein unprivilegiertes TCP-Discovery-Verhalten. Die CI lässt
den Image-Build bei jeder behebbaren HIGH- oder CRITICAL-Schwachstelle fehlschlagen, die Trivy meldet.

## Supply-Chain-Prüfungen

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
läuft auf main sowie wöchentlich, veröffentlicht den tatsächlichen Score und lädt Funde in das
GitHub-Code-Scanning hoch. Actions und Container-Basisimages sind über unveränderliche Hashes gepinnt; Python-Abhängigkeiten
sind in `uv.lock` aufgelöst. Bandit-Fehler lassen die CI fehlschlagen, und begrenztes Atheris-Fuzzing
testet die Parser für SSH, MySQL, HTTP, Zertifikate und SNMPv3-BER
ohne Netzwerkzugriff.

Scorecard misst außerdem historische Review-Aktivität, Beitragendenvielfalt und
Release-Provenienz. Diese Werte spiegeln tatsächliche Nachweise wider; sie sind keine Aussage darüber,
dass jede Governance- oder historische Release-Prüfung erfüllt ist. Siehe
[SECURITY.md](../../../SECURITY.md) und [Release-Provenienz](../../../docs/releasing.md).

## Lokalisierung

CLI-Meldungen sowie Terminal-Zusammenfassungs- und Diff-Tabellen unterstützen 45 Locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ohne zusätzliche Laufzeitabhängigkeiten. Die Auflösung berücksichtigt `--lang`, dann `LC_ALL`, `LC_MESSAGES` und `LANG`, mit Fallback auf `en`. JSON-Schemas, CSV-Spalten und Exportskripte bleiben über alle Locales hinweg unverändert.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Mitwirken

Beiträge sollten einen reproduzierbaren Fall enthalten, die dokumentierten CLI- und
Datenformat-Verträge wahren und die oben genannten Qualitätsprüfungen bestehen. Siehe
[CONTRIBUTING.md](../../../CONTRIBUTING.md) für den Entwicklungsablauf und
[den Release-Leitfaden](../../../docs/releasing.md) für Kompatibilitäts- und Versionierungsentscheidungen.

## Sicherheits- und Lizenzstatus

Siehe [SECURITY.md](../../../SECURITY.md) für private Sicherheitsmeldungen und unterstützte Versionen.
hostcensus steht unter der [MIT-Lizenz](../../../LICENSE).

Quelltext-Header verwenden SPDX-Identifier und bewahren die Urheberrechtsangaben der Beitragenden aus der
Git-Historie. Siehe [AUTHORS.md](../../../AUTHORS.md) zur Nennung der Mitwirkenden. Binäre Testmitschnitte und das
generierte Lockfile nutzen begleitende `.license`-Dateien; der MIT-Text befindet sich in `LICENSES/MIT.txt`.
