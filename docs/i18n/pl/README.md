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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · **Polski** · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus to narzędzie CLI w języku Python do powtarzalnej inwentaryzacji usług w administrowanych sieciach.
Rejestruje usługi udostępniane przez urządzenia, porównuje obserwacje w czasie i generuje
skrypty importu dla Kadupul. Domyślny backend korzysta z gniazd asyncio bez uprawnień root;
opcjonalne wykrywanie za pomocą Nmap pozwala identyfikować hosty wykraczające poza skonfigurowane porty usług.

## Dlaczego hostcensus

Jednorazowy raport portów nie wyjaśnia, czy kolejna obserwacja uległa zmianie, czy
po prostu zakończyła się błędem. hostcensus łączy jawne stany usług, sondy o ograniczonym czasie i rozmiarze, wielokrotnego użytku
profile skanowania oraz lokalną historię. Operatorzy mogą powtarzać ten sam zakres, analizować
błędy oraz odróżniać niepewne obserwacje od potwierdzonych zmian.

- **Dowody działania usług:** identyfikacja SSH, powitania MySQL, nagłówki HTTP, obserwacje
  certyfikatów TLS oraz wykrywanie SNMP lub uwierzytelnione zapytania system-MIB.
- **Powtarzalny zakres:** nazwane profile TOML, addytywne wykluczenia, konfigurowalne
  usługi, limity hostów/sond oraz ograniczona pula procesów roboczych.
- **Kontrole przed wysłaniem ruchu:** lokalny preflight weryfikuje cele, narzędzia, dostęp do
  lokalizacji docelowych, schemat historii oraz skonfigurowane pakiety CA dla TLS.
- **Historia inwentaryzacji:** transakcyjne migawki SQLite przechowują wszystkie obserwacje;
  porównania zachowują widoczność błędów skanera i nieznanych stanów.
- **Interoperacyjne dane wyjściowe:** raporty terminalowe, JSON i CSV, wersjonowane migawki plikowe
  oraz skrypty importu dla Kadupul.

CI obejmuje wersje Python 3.12, 3.13 i 3.14 na systemach Linux i macOS oraz kontrolowane środowisko
integracyjne Compose. Kod wykorzystuje nowoczesne aliasy typów, typowane wyniki kontroli preflight,
profile ze slotami i parametrami wyłącznie nazwanymi oraz ustrukturyzowane czyszczenie asynchroniczne, zachowując zgodność z tymi
wersjami środowiska uruchomieniowego. Zobacz [Wersjonowanie i wydania](../../../docs/releasing.md), aby zapoznać się z kontraktem zgodności SemVer
oraz procesem wydań w serwisie GitHub. Odznaka wydania opisuje
opublikowane artefakty, a nie bieżącą kopię roboczą repozytorium: najnowszy opublikowany tag to obecnie
`v0.3.0`, podczas gdy ta kopia robocza używa wersji pakietu `3.0.0`. Zainstaluj pakiet z tej kopii roboczej,
aby korzystać z opisanych tutaj funkcji inwentaryzacji.

Zacznij od [instalacji](#install), a następnie przejdź do [profili i historii](#inventory-profiles-preflight-and-local-history).
Szczegóły integracji opisano w sekcjach [odciski usług](#fingerprints),
[porównywanie plików](#inventory-diff) oraz [eksport do Kadupul](#kadupul-export).

## Instalacja

Wymagany jest Python 3.12 lub nowszy; przetestowana matryca obejmuje wersje Python 3.12–3.14. Z poziomu tej
kopii roboczej zainstaluj zablokowane zależności uruchomieniowe:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Aby korzystać z opcjonalnego wykrywania hostów za pomocą Nmap, zainstaluj plik wykonywalny Nmap przy użyciu menedżera pakietów swojej platformy;
nie jest wymagany żaden dodatkowy pakiet Pythona. Dane wyjściowe XML z Nmap są parsowane za pomocą
defusedxml (zależności podstawowej), dzięki czemu rozwijanie encji jest odrzucane. hostcensus uruchamia
program `nmap` znaleziony w `PATH` bezpośrednio ze stałą listą argumentów, limitem czasu rosnącym
wraz z rozmiarem prefiksu oraz ograniczeniem wyjścia do 64 MiB. Nmap nie jest potrzebny dla domyślnego backendu.

## Migracja z netprobe

hostcensus to nowa nazwa projektu netprobe, wydana w wersji 3.0.0. Projekt nigdy nie był
publikowany w PyPI pod żadną z tych nazw, więc instalacje pochodziły z kopii roboczej repozytorium lub wydania GitHub.
Repozytorium GitHub zachowuje swoją nazwę.

| Poprzednio | Obecnie | Zgodność |
| --- | --- | --- |
| Dystrybucja `netprobe` | `hostcensus` | Zainstaluj ponownie z kopii roboczej; nie istnieje pakiet pod starą nazwą. |
| Polecenie `netprobe` | `hostcensus` | `netprobe` nadal działa i wypisuje jeden wiersz ostrzeżenia o wycofaniu na stderr. Kody wyjścia i stdout pozostają bez zmian. Zostanie usunięte w kolejnym wydaniu głównym. |
| Zmienne środowiskowe `NETPROBE_*` | `HOSTCENSUS_*` | Zmienna `NETPROBE_*` jest używana, gdy jej odpowiednik `HOSTCENSUS_*` nie jest ustawiony, czemu towarzyszy jedno ostrzeżenie na stderr podające nazwy zmiennych, nigdy ich wartości. `HOSTCENSUS_*` ma pierwszeństwo, gdy ustawione są obie. Zostanie usunięte w kolejnym wydaniu głównym. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Zmiana niezgodna wstecz.** Nie zainstalowano warstwy zgodności importów; należy zaktualizować importy. |
| Tag obrazu Docker `network-discovery:test` (tylko CI) oraz użytkownik kontenera `netprobe` | `hostcensus:test`, użytkownik `hostcensus` | Żaden obraz nie został opublikowany w rejestrze. Zbuduj obraz ponownie i użyj punktu wejścia `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Istniejący plik o starej nazwie domyślnej jest nadal używany z ostrzeżeniem, dopóki nie istnieje plik o nowej nazwie. Jawne ścieżki `--config` oraz `--history` pozostają bez zmian. |
| Raporty i migawki z `"format": "netprobe-report"` lub `"netprobe-snapshot"` oraz polem `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` i `export` nadal wczytują pliki zapisane pod starą nazwą, a opublikowane schematy JSON Schema akceptują oba warianty zapisu. Nowe pliki używają nowych nazw. Bazy historii SQLite są bez zmian i wczytują się jak dotychczas. |
| Skrypty dla Kadupul z `netprobe export` | Skrypty z `hostcensus export` | Stare skrypty nadal działają i podczas uruchamiania wciąż czytają `NETPROBE_SNMP_*`. Nowe skrypty czytają `HOSTCENSUS_SNMP_*`. |

## Szybki przykład

Uruchomione z kontenera testowego środowiska integracyjnego opisanego w sekcji Rozwój; wynik skrócony:

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

## Kody wyjścia

| Polecenie | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | obserwacje/raport zapisane | niepowodzenie preflight/backendu, zapisu historii albo raportu/migawki | nieprawidłowy cel, opcje, konfiguracja lub limity | - | osiągnięto `--deadline`; zapisano raport częściowy, pominięto historię i migawkę |
| `preflight` | kontrole zakończone pomyślnie | niepowodzenie lokalnej kontroli | nieprawidłowy cel/konfiguracja lub sprzeczne lokalizacje docelowe | - | - |
| `profiles` | wyświetlono zwalidowane profile | - | nieczytelna/nieprawidłowa konfiguracja lub wybór | - | - |
| `history` | wyświetlono podsumowania | brakująca, nieprawidłowa lub nieobsługiwana historia | nieprawidłowe opcje CLI | - | - |
| `compare` | utworzono porównanie, również gdy występują zmiany | nieczytelna historia, niezgodny zakres/kolejność lub błąd zapisu | nieprawidłowe opcje CLI | - | - |
| `diff` | brak zmian | nie udało się zapisać pliku `-o` | brakujące, nieczytelne lub nieobsługiwane dane wejściowe albo niekompletne skanowanie bez `--allow-partial` | wykryto zmiany, niepotwierdzone obserwacje lub niekompletne skanowanie | - |
| `export` | skrypt zapisany | nie udało się zapisać skryptu | nieczytelne dane wejściowe, niekompletne skanowanie bez `--allow-partial` lub dane nienadające się do bezpiecznego eksportu | - | - |

## Struktura projektu

| Moduł | Odpowiedzialność |
| --- | --- |
| `cli.py` | Opcje poleceń, rozwiązywanie profili, preflight, skanowanie i raportowanie |
| `scanner.py`, `probes.py` | Rozwijanie celów, ograniczona pula procesów roboczych, wykrywanie hostów i obserwacje usług |
| `config.py`, `profiles.py` | Definicje usług i zwalidowane profile inwentaryzacji |
| `models.py`, `output.py` | Typy wyników oraz renderowanie w terminalu/JSON/CSV |
| `history.py`, `diff.py` | Historia SQLite i porównania wersjonowanych migawek plikowych |
| `preflight.py` | Lokalne kontrole oraz ograniczone czasowo sprawdzanie wersji Nmap |
| `export.py` | Zwalidowane i odpowiednio cytowane skrypty importu dla Kadupul |

Każda obserwacja usługi rejestruje jej stan oddzielnie od deklarowanej tożsamości.
Odczyty i limity czasu są ograniczone; wyjątki sond pozostają w błędach hosta. Historia SQLite
korzysta z transakcji, jawnego zamykania połączeń oraz ścieżek wyłącznie do odczytu do listowania i
porównywania. Sekrety SNMP trafiają do programu wyłącznie przez zmienne środowiskowe lub pliki z sekretami;
historia inwentaryzacji przechowuje efektywne ustawienia niebędące sekretami. Zobacz
[Architektura](../../../docs/architecture.md), aby poznać potok skanowania, jego limity i granice
zaufania, oraz [SECURITY.md](../../../SECURITY.md#authorized-use) w sprawie dozwolonego użycia.


## Użycie

Skanuj wyłącznie sieci, którymi administrujesz.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opcja | Znaczenie |
| --- | --- |
| `NETWORK` | CIDR, adres IP lub nazwa hosta; opcjonalne z `--profile`. Identyfikatory zakresu IPv6 są odrzucane. |
| `-o, --output PATH` | Zapisz raport. Format wynika z rozszerzenia (`.json`, `.csv`); pozostałe rozszerzenia domyślnie używają JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Wymuś format raportu. Nie ma zastosowania bez `--output`. `.sh` wybiera `kadupul`. |
| `-v, --verbose` | Logowanie debugowania. |
| `-q, --quiet` | Pomiń wyniki, postęp i logi informacyjne; ostrzeżenia i błędy nadal pojawiają się na stderr. |
| `--backend asyncio\|nmap` | Wykrywanie hostów. `asyncio` (domyślnie) sonduje bezpośrednio porty usług; `nmap` najpierw wykonuje ping sweep za pomocą nmap i wymaga pliku wykonywalnego `nmap` w `PATH`. |
| `--timeout SECONDS` | Czas oczekiwania dla sond, które nie definiują własnego limitu (domyślnie 1.0). Wbudowane sondy połączeniowe używają 0.3s, chyba że tabela usług ustawia `timeout`. |
| `--concurrency N` | Liczba jednocześnie wykonywanych sond (domyślnie 256). |
| `--deadline SECONDS` | Zatrzymaj całe skanowanie, wliczając sweep nmap, po tym czasie (domyślnie 3600, maksymalnie 604800; zmienna `HOSTCENSUS_DEADLINE`). Ukończone hosty są zapisywane do raportu z `"complete": false`, historia ani migawka nie są zapisywane, a `scan` kończy się kodem 4. |
| `--config PATH` | Definicje usług w formacie TOML oraz opcjonalne nazwane ustawienia `[profiles]`. |
| `--profile NAME` | Użyj nazwanego profilu; domyślnie `hostcensus.toml`, gdy pominięto `--config`. |
| `--exclude IP/CIDR` | Dodaj wykluczenie; powtarzaj w razie potrzeby. Wykluczony host IPv4 wyklucza także prowadzące do niego adresy IPv6: odwzorowane na IPv4 (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) oraz 6to4. Cele i wykluczenia odwzorowane na IPv4 są traktowane jako oznaczane przez nie adresy IPv4. |
| `--max-hosts N` | Limit adresów sprawdzany przed wykluczeniami (domyślne/twarde maksimum 65 536). |
| `--history PATH` | Zapisz ukończone skanowanie w opcjonalnej bazie historii SQLite. |
| `--services NAMES` | Rozdzielona przecinkami lista nazw usług do sprawdzenia w tej kolejności (domyślnie: wszystkie). |
| `--ports SPEC` | Rozdzielona przecinkami lista wpisów `NAME=PORT` (przeniesienie usługi) lub `PORT` (dodanie zwykłej kontroli TCP o nazwie `tcp-PORT`). |
| `--snmp-community-file PATH` | Plik zawierający ciąg community SNMPv2c dla zapytania system MIB. Zmienna: `HOSTCENSUS_SNMP_COMMUNITY` (wartość) lub `HOSTCENSUS_SNMP_COMMUNITY_FILE` (ścieżka). |
| `--snmp-user` | Użytkownik SNMPv3. Zmienna: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (domyślnie), `SHA224`, `SHA256`, `SHA384`, `SHA512` oraz plik zawierający hasło. Zmienne: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` lub `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (domyślnie), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` oraz plik zawierający hasło. Zmienne: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` lub `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Zapisz dodatkowo wersjonowaną migawkę dla polecenia `hostcensus diff`. |
| `--tls-ca-file PATH` | Weryfikuj certyfikaty HTTPS względem tego pakietu PEM zamiast magazynu systemowego. Zmienna: `HOSTCENSUS_TLS_CA_FILE`. |

Domyślnie każdy host jest sprawdzany pod kątem usług SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) i HTTPS (TCP 443). Porty TCP są testowane pełnym połączeniem (connect). SNMP jest testowane żądaniem wykrywania silnika SNMPv3 (engine-discovery), na które każdy agent SNMPv3 musi odpowiedzieć bez poświadczeń; agenty obsługujące wyłącznie v1/v2c nie zostaną wykryte przez tę sondę. W przypadku backendu asyncio host jest uznawany za aktywny (alive), gdy jakakolwiek sonda otrzyma odpowiedź, w tym odrzucenie połączenia, więc host ignorujący każdą sondę otrzymuje `alive=false` oraz błąd "Host is down"; nie dowodzi to, że jest fizycznie wyłączony. Przy `--backend nmap` to nmap decyduje, które hosty są aktywne (ICMP z uprawnieniami root, w przeciwnym razie TCP 80/443).

### Odciski usług

Każda otwarta usługa jest identyfikowana na podstawie tego, co wysyła przed jakimkolwiek logowaniem. Żadna sonda nie uwierzytelnia się poza zapytaniem SNMP i tylko wtedy, gdy dostarczysz poświadczenia.

| Sonda | Odczytuje | `version` | Klucze `details` |
| --- | --- | --- | --- |
| `ssh` | wiersz identyfikacyjny RFC 4253 | oprogramowanie, np. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | początkowy handshake MySQL/MariaDB | wersja serwera | `server_version`, `flavor`, `auth_plugin` lub `error_code`/`error` |
| `http` | odpowiedź `HEAD /` | nagłówek `Server` | `status`, `server` |
| `https` | handshake TLS, certyfikat, `HEAD /` | nagłówek `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | wykrywanie SNMPv3; z poświadczeniami GET dla sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; z poświadczeniami `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` lub `snmp_error` |

Docelowa nazwa hosta jest rozwiązywana raz na host i każda sonda łączy się z tym adresem, zapisanym w wynikach jako `address`; nazwa jest używana wyłącznie do TLS SNI, weryfikacji certyfikatu oraz nagłówka HTTP `Host`. Nazwa, której nie można rozwiązać, daje stany `unknown` oraz błąd `Cannot resolve`. Nazwy z odwrotnego DNS są zachowywane tylko wtedy, gdy zawierają znaki nazwy hosta, a jednocześnie działa najwyżej 16 zapytań. HTTPS stosuje weryfikację certyfikatu i nazwy hosta względem magazynu systemowego lub `--tls-ca-file`. Magazyn zaufania jest wczytywany raz dla całego skanowania i używany ponownie w każdej sondzie HTTPS. Połączenie TCP i handshake TLS mają osobne limity czasu, dzięki czemu port akceptujący połączenia, lecz zawieszający handshake, ma stan `open` z `tls_error`, a nie `filtered`. Jeśli weryfikacja zawiedzie, wynik zapisuje `cert_verified: false` oraz `cert_verify_error`; sonda nie ponawia próby ze słabszymi ustawieniami ani nie wysyła żądania HTTP. Szczegóły certyfikatu i nagłówki HTTP są zbierane dopiero po pomyślnej weryfikacji. Dla usług z prywatnym urzędem CA podaj właściwy pakiet CA. Starsze raporty mogą zawierać `cert_read_unverified`, czego obecne sondy już nie generują.

Sekrety SNMP są odczytywane wyłącznie ze zmiennych środowiskowych lub z plików (`--snmp-*-file` albo odpowiadająca zmienna `HOSTCENSUS_SNMP_*_FILE`), nigdy z wartości podanych bezpośrednio w wierszu poleceń, które inni lokalni użytkownicy mogą zobaczyć na liście procesów. Opcje `--snmp-community`, `--snmp-auth-key` i `--snmp-priv-key` z wartością kończą działanie z kodem 2 i wskazują zamiennik. Plik z sekretem musi być niepustym tekstem UTF-8 o rozmiarze co najwyżej 4096 bajtów; jeden końcowy znak nowego wiersza jest ignorowany, a jednoczesne ustawienie zmiennej i pliku dla tego samego sekretu jest błędem. Komunikaty błędów podają nazwę pliku, ale nigdy nie wypisują jego zawartości. Raporty skanowania i historia nie zawierają celowo wartości poświadczeń. Eksporter ma osobną, jawną opcję `--include-credentials` opisaną poniżej. Podanie ciągu community wybiera SNMPv2c; podanie użytkownika wybiera SNMPv3, z uwierzytelnianiem po podaniu klucza uwierzytelniania oraz szyfrowaniem po podaniu obu kluczy (`snmp_security_level` rejestruje wybrany poziom). hostcensus odmawia z kodem wyjścia 2 łączenia community z użytkownikiem v3, użycia klucza szyfrowania bez klucza uwierzytelniania albo użycia kluczy bez użytkownika i nigdy nie ponawia nieudanego zapytania v3 za pomocą v2c ani niższego poziomu bezpieczeństwa. Agenty obsługujące wyłącznie v1/v2c ignorują bezpoświadczeniowe wykrywanie v3, więc są wykazywane jako otwarte tylko po podaniu community.

Tekst banera jest redukowany do znaków drukowalnych i ograniczany do 256 znaków przed zapisaniem lub wyświetleniem. Odczyty również są ograniczone: 4 KiB na wiersz, 4 KiB dla powitania MySQL oraz 16 KiB dla nagłówków HTTP. Identyfikator silnika SNMP (engine ID) dłuższy niż 32 oktety jest obcinany przed zapisaniem. HTTP i HTTPS wysyłają nagłówek Host z adresem IPv6 w nawiasach kwadratowych oraz z numerem portu, gdy jest inny niż 80 lub 443. Komórki CSV zaczynające się od znaku wyzwalającego formułę arkusza kalkulacyjnego otrzymują prefiks, aby pozostały tekstem.

### Limity

Pojedyncze uruchomienie przyjmuje maksymalnie 65 536 adresów, 64 usługi i 524 288 sond (liczba hostów pomnożona przez liczbę usług); większe żądania kończą działanie z kodem 2 przed wysłaniem czegokolwiek. `--concurrency` jest ograniczone do 4096 gniazd. Każda sonda ma twardy limit czasu równy czterokrotności własnego budżetu. Sondy połączeniowe (`tcp`, `ssh`, `mysql`, `http`) używają 0.3 sekundy, chyba że dana usługa ustawia `timeout`. SNMP i HTTPS używają `--timeout` (domyślnie 1.0), gdy nie mają własnego limitu. Sonda, która przekroczy limit czasu, jest raportowana jako `unknown` z komunikatem "probe timed out" w `errors`. Lokalne błędy gniazd (na przykład wyczerpanie deskryptorów plików) również otrzymują stan `unknown` z zapisanym błędem; nigdy nie liczą się jako port filtrowany ani wyłączony host. Przed sondowaniem hostcensus podnosi miękki limit otwartych plików w kierunku limitu twardego, aby zmieścić `--concurrency` plus 64 deskryptory; gdy nie może tego zrobić, kontrola preflight `open files` kończy się niepowodzeniem, a `scan` wychodzi z kodem 1 przed wysłaniem ruchu. Wykrywanie Nmap używa 30-sekundowego limitu czasu na host. Prefiks jest przekazywany do nmap w postaci CIDR, a sweep kończy się niepowodzeniem z kodem 1, gdy nmap zwróci mniej adresów niż mu przekazano (na przykład nazwę, której nie potrafi rozwiązać), zamiast oznaczać hosty jako wyłączone. Docelowa nazwa hosta jest rozwiązywana raz i ten adres jest przekazywany do nmap, dzięki czemu wykrywanie i sondy trafiają do tej samej maszyny. Pełny prefiks to jeden proces nmap z limitem czasu procesu podrzędnego wynoszącym 35 sekund na każde 256 adresów, zaokrąglone w górę. Sweepy z wykluczeniami używają partii po 256 hostów oraz 35-sekundowego limitu czasu na każdą partię. Tworzenie procesów roboczych jest ograniczone niezależnie od rozmiaru zakresu. Odwrotny DNS i rozwiązywanie nazw hostów mają osobny dwusekundowy limit czasu; wywołanie resolvera, które nigdy nie wraca, jest porzucane we własnym wątku, dzięki czemu nie może utrzymywać hostcensus przy życiu poza tymi limitami. Jednocześnie działa najwyżej 16 zapytań, a porzucone wywołanie zachowuje swoje miejsce aż do powrotu, dzięki czemu liczba zablokowanych wątków pozostaje ograniczona; jeśli wszystkie 16 zawisną, kolejne zapytania czekają w kolejce na wolne miejsce poza dwusekundowym limitem czasu (który zaczyna biec po zwolnieniu miejsca), dopóki `--deadline` nie zatrzyma skanowania. `NetworkScanner` używany jako biblioteka bez `deadline` może czekać na takie miejsce w nieskończoność. `--deadline` (domyślnie jedna godzina) ogranicza dodatkowo czas całego uruchomienia ponad tymi limitami.

### Konfigurowanie usług

Usługi można zmieniać za pomocą pliku TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` to jedna z wartości `tcp`, `ssh`, `mysql`, `http`, `https` lub `snmp` i domyślnie przyjmuje nazwę usługi, jeśli jest ona nazwą sondy, a w przeciwnym razie `tcp`. Tylko `snmp` używa protokołu UDP. Nazwy usług składają się z małych liter, cyfr, `-` oraz `_`. Dwie usługi nie mogą współdzielić tego samego portu i protokołu; historia rejestruje jeden stan dla tej pary. `timeout` jest opcjonalny, podawany w sekundach i musi wynosić co najmniej 0.05. Sondy połączeniowe (`tcp`, `ssh`, `mysql`, `http`) domyślnie używają 0.3 sekundy. `snmp` i `https` używają opcji `--timeout` skanowania, gdy usługa nie ustawia `timeout`. `--timeout` nie zastępuje limitu, który usługa już posiada.

Raporty JSON są wersjonowanymi dokumentami (`"format": "hostcensus-report"`, `"version": 1`), które zapisują cel, sondowane usługi i ustawienia obok `devices`; `--format json` bez `-o` wypisuje raport na stdout zamiast tabeli. Każdy format wyjściowy JSON ma opublikowany schemat; zobacz [Wyjście JSON](../../../docs/json-output.md). Obiekty urządzeń zachowują oryginalne pola `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` oraz `errors` i dodają listę `services` zawierającą `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` albo `unknown`, gdy sonda zawiodła lokalnie lub przekroczyła limit czasu), `version` i `details` każdej sondy. Wyjście CSV zyskuje końcowe kolumny `services` i `versions` dla otwartych usług. Wartości logiczne `ssh`, `snmp` i `mysql` odpowiadają usługom o dokładnie tych nazwach.


## Profile inwentaryzacji, preflight i lokalna historia

Nazwane profile współdzielą plik TOML z istniejącymi definicjami `[services]`. Skopiuj
[hostcensus.example.toml](../../../hostcensus.example.toml) do `hostcensus.toml` i ustaw sieci,
którymi administrujesz:

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

`preflight` rozwiązuje opcje i profile dokładnie tak samo jak `scan`, łącznie z
`--concurrency` na potrzeby kontroli otwartych plików, więc pomyślny preflight oznacza, że `scan`
wystartuje z tym samym planem.

Profile akceptują pola `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` oraz `max_hosts`. `services` i `ports` używają dotychczasowej składni list rozdzielonych przecinkami.
Jawne opcje CLI nadpisują ustawienia profilu; powtarzane opcje `--exclude`
dopisują się do wykluczeń profilu. Jawna sieć podana z `--profile` musi zawierać się
w zakresie IP/CIDR tego profilu. Nazwy hostów są nadal obsługiwane w bezpośrednich
skanowaniach, ale nie można ich łączyć z wykluczeniami IP. Limity hostów obowiązują przed
wykluczeniami; łączny limit sond nadal obowiązuje po ich zastosowaniu. Wykluczone hosty są
pomijane zarówno w kontrolach usług, jak i w opcjonalnym wykrywaniu Nmap.

Każde skanowanie wykonuje lokalne kontrole preflight przed wysłaniem ruchu do celów: limity celów/sond,
dostęp do lokalizacji docelowych, dostępność opcjonalnego pliku wykonywalnego/wrappera Nmap, schemat
historii oraz skonfigurowany pakiet TLS CA. `preflight` raportuje JSON i nie skanuje
celów ani nie tworzy bazy historii. Zapisuje tymczasowo plik sąsiedni, aby przetestować
dostęp do zapisu bez zmieniania istniejącej zawartości. Domyślny backend asyncio
nadal nie wymaga ani Nmap, ani uprawnień root. Ścieżki docelowe muszą być rozłączne względem siebie
oraz względem konfiguracji wejściowej, włączając twarde dowiązania; dowiązania symboliczne w miejscu docelowym są
odrzucane. Nieudane kontrole zwracają 1; nieprawidłowy zakres/konfiguracja zwraca 2.

Zapis raportów i eksportów wymaga obsługi `O_NOFOLLOW`. Na platformach bez tej obsługi,
w tym w systemie Windows, zapisy te kończą się niepowodzeniem bez otwierania ani obcinania pliku docelowego.
Nowe raporty i skrypty eksportu są dostępne wyłącznie dla właściciela (tryb 0600); nadpisanie istniejącego pliku zachowuje jego
uprawnienia. Zapis do potoku nazwanego bez czytelnika kończy się niepowodzeniem natychmiast zamiast czekać. Nowa baza `--history` jest również tworzona z dostępem wyłącznie dla właściciela; istniejąca zachowuje swój tryb. Komunikaty logów zawsze trafiają na stderr, dzięki czemu stdout przenosi wyłącznie wyniki. Eksporty zawierające poświadczenia zawsze wymuszają tryb 0600.

Historia jest opcjonalna (opt-in) i uzupełnia istniejące migawki JSON oraz polecenie `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Użyj identyfikatorów z `history`; przykład zakłada nową bazę danych. Migawki są zapisywane
transakcyjnie z czasami rozpoczęcia/zakończenia w UTC, wersją pakietu, efektywnymi ustawieniami
niebędącymi sekretami, podsumowaniami oraz wszystkimi obserwacjami hostów/usług, w tym błędami dla poszczególnych hostów.
Niekompletne obserwacje hostów są zachowywane. Anulowane uruchomienia nie są zapisywane. Istniejące
kontrakty raportów, migawek, eksportu oraz kodów wyjścia skanowania pozostają zachowane.

`history` wyświetla podsumowania JSON bez wczytywania całych historycznych danych urządzeń.
`compare` odczytuje dwa zapisane skanowania, wymaga identycznych tożsamości celów oraz wybranych
portów i raportuje zmiany dostępności, statusu oraz stanów portów. Wcześniejsze
ID skanowania musi poprzedzać późniejsze ID. Gdy oba skanowania zapisały `timeout` lub `backend`
i te wartości się różnią, raport zawiera ostrzeżenie i mimo to porównuje
obserwacje. Inny czas oczekiwania może sprawić, że filtrowany port będzie wyglądał na otwarty. Błędy skanera
oraz obserwacje portów o stanie unknown są oznaczane jako niepewne zamiast traktowania ich jako
potwierdzone zniknięcie lub zamknięcie: hosty z błędami trafiają do `uncertain_hosts`, a
każde przejście portu obejmujące `unknown` (w tym unknown w obu skanowaniach) jest umieszczane
w `unconfirmed_ports` zamiast `port_changes`, z wyjątkiem portu otwartego w
późniejszym skanowaniu, który stanowi zmianę portu. `compare` i `diff` klasyfikują porty według tej samej reguły.
`no_longer_responding` oznacza brak odpowiedzi, a nie dowód usunięcia urządzenia.
Kod wyjścia 0 dla `scan` nie gwarantuje, że każdy host odpowiedział: sprawdzaj błędy poszczególnych hostów. Pomyślne porównanie zwraca 0 niezależnie od tego, czy wystąpiły zmiany; istniejące polecenie `diff` na plikach
zachowuje kontrakt kodu wyjścia 3. Nieobsługiwana lub uszkodzona historia zwraca 1.

Historia przechowuje informacje inwentaryzacyjne, więc wybierz odpowiednio zabezpieczony lokalny
katalog. Pliki profili i zapisane ustawienia nie zawierają poświadczeń SNMP;
obsługa poświadczeń nadal odbywa się za pomocą dotychczasowych opcji uruchomieniowych i zmiennych środowiskowych.

## Porównanie inwentaryzacji (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Migawka to plik JSON z polami `format: "hostcensus-snapshot"`, `version: 1`, wersją hostcensus, czasem utworzenia w UTC, celem, wartościami `timeout` i `backend` skanowania (jeśli skanowanie je zapisało), sondowanymi usługami oraz aktywnymi hostami w takim samym kształcie jak raport `-o`. Wyłączone hosty są pomijane. `diff` akceptuje również zwykłe raporty JSON z `scan -o`, w tym pochodzące sprzed wprowadzenia pola `services`.

`diff` raportuje nowe i utracone hosty, porty otwarte lub zamknięte na hostach obecnych w obu plikach oraz usługi, których `version` uległa zmianie. Porty sondowane tylko w jednym z dwóch skanowań nie są porównywane, o czym informuje ostrzeżenie. Nieudane obserwacje nigdy nie są interpretowane jako "brak zmian": port o stanie `unknown` w dowolnym ze skanowań, który nie jest otwarty w późniejszym, trafia do `unconfirmed`, a nie `closed`, z `before` o wartości `open`, `unknown` lub `not-open` (sondowany i zamknięty lub filtrowany) oraz `after` o wartości `unknown` lub `not-open`; port otwarty obecnie jest raportowany w `opened`, nawet jeśli wcześniejsza sonda zawiodła. Host, którego wszystkie sondy zawiodły bez odpowiedzi w którymkolwiek skanowaniu, trafia do `unsettled_hosts` (z `before`/`after` o wartości `up`, `uncertain` lub `absent`, w tym gdy zawiódł w obu skanowaniach lub nie ma go w drugim pliku) zamiast `vanished_hosts`; jeśli odpowie w późniejszym skanowaniu, jest dodatkowo raportowany jako nowy host wraz z otwartymi portami. Z tego powodu migawki zachowują takie hosty z błędami. Ostrzeżenie pojawia się także wtedy, gdy różnią się cele oraz gdy oba pliki zapisały timeout lub backend o różnych wartościach. `-o PATH` zapisuje postać JSON również do pliku.

Raport ze skanowania zatrzymanego przez `--deadline` (`"complete": false`) zawiera tylko hosty, do których dotarto, dlatego `diff` i `export` odrzucają go z kodem wyjścia 2. `--allow-partial` akceptuje taki raport z ostrzeżeniem na stderr: `diff` wymienia wówczas hosty całkowicie pominięte przez niekompletne skanowanie w `unsettled_hosts` jako `unscanned` zamiast utraconych (host wymieniony jako wyłączony nadal jest uznawany za utracony), ustawia `partial` na true i nigdy nie raportuje braku zmian, a `export` zapisuje ostrzeżenie w nagłówku skryptu.

Kody wyjścia `diff`: `0` brak zmian, `3` wykryto zmiany, obserwacje niemożliwe do potwierdzenia albo niekompletne dane wejściowe (`changed` ma wartość true zawsze, gdy jakakolwiek lista, w tym `unsettled_hosts` i `unconfirmed`, jest niepusta lub `partial` ma wartość true), `2` brakujący plik, nieczytelny plik, nieobsługiwana migawka albo niekompletny plik bez `--allow-partial`, `1` nie udało się zapisać pliku `-o`.

## Eksport do Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (fork Cacti 1.2.31) nie ma masowego importu urządzeń z pliku. Obsługiwanym sposobem dodawania urządzeń ze skryptu jest `cli/add_device.php`, po jednym urządzeniu na wywołanie, z argumentami `--option=value`. `hostcensus export` zapisuje skrypt POSIX `sh` złożony z takich wywołań:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Każdy aktywny host staje się poleceniem `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hosty, na których zapytanie SNMP skanowania zakończyło się sukcesem, otrzymują `--version=2 --community=...` lub `--version=3 --username=... --authproto=... --password=...` (oraz `--privproto`/`--privpass` dla authPriv), `--port` i `--avail=snmp`. Eksport SNMPv3 wymaga `--snmp-user`, a tryb noAuthNoPriv jest odrzucany, ponieważ `add_device.php` wymaga hasła v3.
- Pozostałe hosty otrzymują `--version=0 --avail=ping`, z `--ping_method=tcp --ping_port=` ustawionym na pierwszy otwarty port TCP lub ICMP w przypadku jego braku.
- `--notes` wymienia otwarte usługi i wersje. `--description` to nazwa z odwrotnego DNS, gdy jest prosta (litery, cyfry, `.`, `_`, `-`), w przeciwnym razie adres IP, oraz jest unikalna, ponieważ `add_device.php` traktuje istniejący opis jako aktualizację tego urządzenia.

Każda wartość jest walidowana i cytowana powłokowo za pomocą `shlex.quote`. Domyślnie nie jest zapisywany żaden sekret SNMP: skrypt rozwija w czasie wykonania zmienne `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` lub `HOSTCENSUS_SNMP_PRIV_KEY` i zatrzymuje się, jeśli któraś nie jest ustawiona. `--include-credentials` zamiast tego wpisuje wartości z tych zmiennych środowiskowych do skryptu, tworzy go z uprawnieniami 0600 i loguje ostrzeżenie. Samo narzędzie `add_device.php` wypisuje ciąg community i przyjmuje sekrety jako argumenty, które są widoczne na liście procesów serwera Kadupul podczas wykonywania każdego wywołania.

`add_device.php` kończy działanie z kodem 1 w przypadku duplikatów i błędów; skrypt kontynuuje, zlicza niepowodzenia i kończy z kodem 1, jeśli nie udało się dodać któregokolwiek urządzenia. Identyfikatory szablonów pochodzą z `php cli/add_device.php --list-host-templates`. Kody wyjścia `export`: `0` zapisano, `2` nieczytelne dane wejściowe, niekompletne skanowanie bez `--allow-partial` lub dane nienadające się do bezpiecznego eksportu, `1` nie udało się zapisać skryptu.

## Wersjonowanie i proces wydań

hostcensus stosuje [Semantic Versioning](https://semver.org/spec/v2.0.0.html): zgodne
poprawki zwiększają wersję poprawkową (patch), zgodne funkcje/wycofania zwiększają wersję
pomocniczą (minor), a zmiany łamiące zgodność zwiększają wersję główną (major).
Polecenia i opcje, kody wyjścia oraz schematy JSON stanowią publiczny kontrakt;
wycofywane zachowanie działa aż do kolejnego wydania głównego, chyba że poprawka
bezpieczeństwa wymaga wcześniejszej zmiany (wówczas changelog wyjaśnia przyczynę).

release-please otwiera PR wydania na podstawie tytułów Conventional Commit na gałęzi `main`,
podbijając `pyproject.toml`, `uv.lock` i `CHANGES.md`. Jego scalenie tworzy tag
`vMAJOR.MINOR.PATCH` oraz szkic wydania GitHub, do którego CI dołącza przetestowany
pakiet wheel, dystrybucję źródłową oraz sumy kontrolne; GitHub zapisuje atestacje budowania dla
tych plików poprzez swoje API atestacji. Opiekun przegląda i publikuje
szkic po dołączeniu plików. Wydania nigdy nie są zastępowane.

Zaufane publikowanie w PyPI (PyPI trusted publishing) jest opcjonalne i wymaga własności projektu, zaufanego
wydawcy (trusted publisher) oraz środowiska `pypi`. Publikuje te same sprawdzone artefakty wydania
bez ponownego budowania ani przechowywania tokenu API. Otagowane wydania w tym publicznym
repozytorium generują atestacje artefaktów GitHub; prywatne forki wymagają obsługiwanego
planu oraz jawnego włączenia (opt-in). Zobacz
[pełny przewodnik po wydaniach](../../../docs/releasing.md), aby poznać konfigurację, dokładne polecenia i ponowne próby.

## Rozwój

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Narzędzia deweloperskie znajdują się w grupach zależności [PEP 735](https://peps.python.org/pep-0735/)
w `pyproject.toml` (`dev`, `fuzz`, `build`), dzięki czemu nigdy nie trafiają do
metadanych opublikowanego pakietu. `uv.lock` jest pojedynczym plikiem blokady; CI instaluje zależności przez
`uv sync --locked` i kończy się niepowodzeniem, gdy plik blokady jest nieaktualny. Wybierz interpreter za pomocą
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) lub dowolnego Pythona 3.12+.

CI wymusza próg 90% pokrycia kodu pakietu testami. Testy jednostkowe obejmują kontrolowane serwery
loopback oraz przypadki offline dla profili, historii i walidatora wydań; środowisko Compose uruchamia
OpenSSH, MariaDB, nginx i net-snmp w odizolowanej sieci bridge. Uruchamiaj je przez
`make test-integration`. Zobacz [CONTRIBUTING.md](../../../CONTRIBUTING.md) oraz
[narzędzia wydawnicze](../../../scripts/README.md).

Kontener uruchomieniowy działa jako UID/GID 10001 bez katalogu domowego, bez powłoki
logowania i bez pip oraz może zapisywać w `/app/output`. Nadaj temu użytkownikowi prawa zapisu do
dowolnego montowanego katalogu wyjściowego. Nie wymaga żadnych uprawnień Linux capabilities i działa z
głównym systemem plików tylko do odczytu, więc można go uruchamiać następująco:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

W tym kontenerze Nmap korzysta z nieuprzywilejowanego trybu wykrywania TCP. CI przerywa
budowanie obrazu w przypadku każdej możliwej do naprawienia podatności HIGH lub CRITICAL zgłoszonej przez Trivy.

## Kontrole łańcucha dostaw

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
działa na gałęzi main i co tydzień, publikuje rzeczywisty wynik oraz przesyła znaleziska do skanowania kodu
GitHub. Akcje i bazowe obrazy kontenerów są przypięte niezmiennymi skrótami; zależności Pythona
są rozwiązywane w `uv.lock`. Błędy Bandit powodują niepowodzenie CI, a ograniczony czasowo fuzzing Atheris
testuje parsery SSH, MySQL, HTTP, certyfikatów i SNMPv3 BER
bez dostępu do sieci.

Scorecard mierzy także historyczną aktywność przeglądów kodu, różnorodność współtwórców oraz
pochodzenie wydań (provenance). Wyniki te odzwierciedlają rzeczywiste dowody; nie są deklaracją,
że każda kontrola zarządzania projektem lub wydań historycznych została spełniona. Zobacz
[SECURITY.md](../../../SECURITY.md) oraz [pochodzenie wydań](../../../docs/releasing.md).

## Lokalizacja

Komunikaty CLI oraz terminalowe tabele podsumowań i różnic obsługują 45 ustawień regionalnych (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) bez żadnych dodatkowych zależności uruchomieniowych. Rozwiązywanie języka uwzględnia `--lang`, następnie `LC_ALL`, `LC_MESSAGES` i `LANG`, wracając domyślnie do `en`. Schematy JSON, kolumny CSV oraz skrypty eksportu pozostają niezmienione we wszystkich ustawieniach regionalnych.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Współtworzenie

Zgłaszane zmiany powinny zawierać powtarzalny przypadek testowy, zachowywać udokumentowane kontrakty CLI oraz
formatów danych i przechodzić powyższe kontrole jakości. Zobacz
[CONTRIBUTING.md](../../../CONTRIBUTING.md), aby poznać przepływ pracy deweloperskiej, oraz
[przewodnik po wydaniach](../../../docs/releasing.md) w sprawie decyzji dotyczących zgodności i wersjonowania.

## Bezpieczeństwo i status licencji

Zobacz [SECURITY.md](../../../SECURITY.md), aby dowiedzieć się o prywatnym zgłaszaniu podatności oraz wspieranych wersjach.
hostcensus jest udostępniany na licencji [MIT License](../../../LICENSE).

Nagłówki plików źródłowych używają identyfikatorów SPDX i zachowują uznanie autorstwa współtwórców z historii
Git. Zobacz [AUTHORS.md](../../../AUTHORS.md) dla informacji o autorstwie. Binarne przechwyty testowe oraz
wygenerowany plik blokady używają sąsiednich plików `.license`; tekst licencji MIT znajduje się w `LICENSES/MIT.txt`.
