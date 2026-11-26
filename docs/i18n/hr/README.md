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

<details><summary>More languages (28 locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [Bosanski](../bs/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · **Hrvatski** · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Српски](../sr/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus je Python CLI alat za ponovljivu inventarizaciju usluga na mrežama kojima upravljate. Bilježi što uređaji izlažu, uspoređuje opažanja tijekom vremena i generira skripte za uvoz u Kadupul. Zadani pozadinski sustav koristi asyncio utičnice bez root ovlasti; neobvezno otkrivanje putem alata Nmap može identificirati domaćine i izvan konfiguriranih priključaka usluga.

## Zašto hostcensus

Jednokratno izvješće o priključcima ne objašnjava je li se sljedeće opažanje promijenilo ili je jednostavno završilo pogreškom. hostcensus objedinjuje izričita stanja usluga, vremenski ograničene provjere, višekratno upotrebljive profile skeniranja i lokalnu povijest. Operatori mogu ponoviti isti opseg, pregledati pogreške i razlučiti nesigurna opažanja od potvrđenih promjena.

- **Dokazi o uslugama:** SSH identifikacija, pozdravne poruke MySQL poslužitelja, HTTP zaglavlja, opažanja TLS certifikata te SNMP otkrivanje ili ovjereni upiti za system-MIB.
- **Ponovljiv opseg:** imenovani TOML profili, aditivna izuzeća, prilagodljive usluge, ograničenja broja domaćina i provjera te ograničen broj radnih zadataka.
- **Provjere prije mrežnog prometa:** lokalna prethodna provjera potvrđuje odredišta, alate, pristup izlaznim datotekama, shemu povijesti i konfigurirane skupove TLS CA certifikata.
- **Povijest inventara:** transakcijske SQLite snimke pohranjuju sva opažanja; usporedbe zadržavaju vidljivima pogreške skenera i nepoznata stanja.
- **Interoperabilan ispis:** prikaz u terminalu, JSON i CSV izvješća, inačicama označene datotečne snimke te skripte za uvoz u Kadupul.

CI obuhvaća Python 3.12, 3.13 i 3.14 na sustavima Linux i macOS, uz nadziranu Compose integracijsku okolinu. Kôd koristi suvremene zamjenske nazive tipova, tipizirane rezultate prethodne provjere, slotove za profile s parametrima samo po ključnoj riječi i strukturirano asinkrono čišćenje uz očuvanje podrške za te inačice izvođenja. Pogledajte [Upravljanje inačicama i izdanjima](../../../docs/releasing.md) za ugovor o SemVer kompatibilnosti i postupak objave na GitHubu. Značka izdanja opisuje objavljene artefakte, a ne radnu kopiju: najnovija objavljena oznaka trenutačno je `v0.3.0`, dok ova radna kopija koristi inačicu paketa `3.0.0`. Instalirajte iz radne kopije kako biste upotrebljavali ovdje dokumentirane mogućnosti inventarizacije.

Započnite s [instalacijom](#instalacija), a zatim prijeđite na [profile i povijest](#profili-inventara-prethodna-provjera-i-lokalna-povijest). Za pojedinosti o integraciji pogledajte [otiske usluga](#otisci-usluga), [usporedbu datoteka](#usporedba-inventara) i [izvoz za Kadupul](#izvoz-za-kadupul).

## Instalacija

Potreban je Python 3.12 ili noviji; testirana matrica pokriva Python 3.12-3.14. Iz ove radne kopije instalirajte zaključane ovisnosti za izvođenje:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Za neobvezno Nmap otkrivanje domaćina instalirajte izvršnu datoteku Nmap putem upravitelja paketa vaše platforme; dodatni Python paket nije potreban. XML izlaz alata Nmap raščlanjuje se bibliotekom defusedxml, koja je temeljna ovisnost, pa se proširivanje entiteta odbija. hostcensus pokreće `nmap` pronađen u putanji `PATH` izravno s nepromjenjivim popisom argumenata, krajnjim rokom koji raste s veličinom prefiksa i ograničenjem ispisa od 64 MiB. Nmap nije potreban za zadani pozadinski sustav.

## Prelazak s alata netprobe

hostcensus je novi naziv za netprobe, objavljen u inačici 3.0.0. Projekt nikada nije objavljen na servisu PyPI ni pod jednim nazivom, pa su instalacije dolazile iz radne kopije ili GitHub izdanja. GitHub repozitorij zadržava svoj izvorni naziv.

| Prije | Sada | Kompatibilnost |
| --- | --- | --- |
| Distribucija `netprobe` | `hostcensus` | Ponovno instalirajte iz radne kopije; paket pod starim nazivom ne postoji. |
| Naredba `netprobe` | `hostcensus` | `netprobe` i dalje radi i ispisuje jedan redak upozorenja o zastarjelosti na stderr. Izlazni kodovi i stdout ostaju nepromijenjeni. Bit će uklonjeno u sljedećem velikom izdanju. |
| Varijable okruženja `NETPROBE_*` | `HOSTCENSUS_*` | Varijabla `NETPROBE_*` rabi se kada njezin par `HOSTCENSUS_*` nije postavljen, uz jedno upozorenje na stderr koje navodi nazive varijabli, a nikada njihove vrijednosti. `HOSTCENSUS_*` ima prednost kad su obje postavljene. Bit će uklonjeno u sljedećem velikom izdanju. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Nepovratna promjena.** Nije instaliran zamjenski sloj za uvoz; ažurirajte uvoze. |
| Oznaka Docker slike `network-discovery:test` (samo CI) i korisnik spremnika `netprobe` | `hostcensus:test`, korisnik `hostcensus` | Nijedna slika nikada nije objavljena u registru. Ponovno izgradite sliku i rabite ulaznu točku `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Postojeća datoteka sa starim zadanim nazivom i dalje se rabi uz upozorenje dok novi naziv ne postoji. Izričite putanje `--config` i `--history` ostaju netaknute. |
| Izvješća i snimke s `"format": "netprobe-report"` ili `"netprobe-snapshot"` i poljem `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` i `export` i dalje učitavaju datoteke zapisane pod starim nazivom, a objavljene JSON sheme prihvaćaju oba oblika. Nove datoteke koriste nove nazive. SQLite baze povijesti ostaju nepromijenjene i učitavaju se kao prije. |
| Kadupul skripte iz `netprobe export` | Skripte iz `hostcensus export` | Stare skripte i dalje rade te pri pokretanju čitaju `NETPROBE_SNMP_*`. Nove skripte čitaju `HOSTCENSUS_SNMP_*`. |

## Brzi primjer

Pokrenuto iz testnog spremnika integracijske okoline opisane u odjeljku Razvoj; ispis je skraćen:

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

## Izlazni kodovi

| Naredba | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | opažanja ili izvješće pohranjeni | neuspjela prethodna provjera/pozadinski sustav, povijest ili pohrana izvješća/snimke | nevaljan cilj, opcije, konfiguracija ili ograničenja | - | istekao `--deadline`; zapisano nepotpuno izvješće, povijest i snimka preskočene |
| `preflight` | provjere uspješne | lokalna provjera nije uspjela | nevaljan cilj/konfiguracija ili sukobljena odredišta | - | - |
| `profiles` | ispisani potvrđeni profili | - | nečitljiva/nevaljana konfiguracija ili odabir | - | - |
| `history` | ispisani sažetci | nedostajuća, nevaljana ili nepodržana povijest | nevaljane CLI opcije | - | - |
| `compare` | usporedba izrađena, uključujući slučaj s promjenama | nečitljiva povijest, neusklađen opseg/redoslijed ili pogreška zapisa | nevaljane CLI opcije | - | - |
| `diff` | nema promjena | nije bilo moguće zapisati datoteku `-o` | nedostajući, nečitljiv ili nepodržan ulaz ili nepotpuno skeniranje bez `--allow-partial` | pronađene promjene, nepotvrđena opažanja ili nepotpuno skeniranje | - |
| `export` | skripta zapisana | nije bilo moguće zapisati skriptu | nečitljiv ulaz, nepotpuno skeniranje bez `--allow-partial` ili podatci koji se ne mogu sigurno izvesti | - | - |

## Raspored modula

| Modul | Zaduženje |
| --- | --- |
| `cli.py` | Opcije naredbi, razrješavanje profila, prethodna provjera, skeniranje i izvješćivanje |
| `scanner.py`, `probes.py` | Proširivanje ciljeva, ograničeni radni zadatci, otkrivanje domaćina i opažanja usluga |
| `config.py`, `profiles.py` | Definicije usluga i potvrđeni profili inventara |
| `models.py`, `output.py` | Tipovi rezultata te prikaz u terminalu, JSON i CSV obliku |
| `history.py`, `diff.py` | SQLite pohrana povijesti i usporedba datotečnih snimki s inačicama |
| `preflight.py` | Lokalne provjere i vremenski ograničeno očitanje inačice alata Nmap |
| `export.py` | Potvrđene i sigurno ograđene skripte za uvoz u Kadupul |

Svako opažanje usluge bilježi njezino stanje odvojeno od oglašenog identiteta. Čitanja i krajnji rokovi su ograničeni; iznimke provjera ostaju zabilježene u pogreškama domaćina. SQLite povijest rabi transakcije, izričito zatvaranje veza te putanje samo za čitanje pri ispisu i usporedbi. SNMP tajne ulaze isključivo putem varijabli okruženja ili datoteka s tajnama; povijest inventara pohranjuje stvarne postavke bez tajni. Pogledajte [Arhitekturu](../../../docs/architecture.md) za cjevovod skeniranja, njegova ograničenja i granice povjerenja, te [SECURITY.md](../../../SECURITY.md#authorized-use) za ovlaštenu uporabu.

## Uporaba

Skenirajte isključivo mreže kojima upravljate.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opcija | Značenje |
| --- | --- |
| `NETWORK` | CIDR, IP ili naziv domaćina; neobvezno uz `--profile`. Identifikatori IPv6 opsega se odbijaju. |
| `-o, --output PATH` | Zapisuje izvješće u datoteku. Oblik prati nastavak (`.json`, `.csv`); ostali nastavci koriste JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Prisilno određuje oblik izvješća. Nema učinka bez `--output`. `.sh` odabire `kadupul`. |
| `-v, --verbose` | Detaljno zapisivanje za ispravljanje pogrešaka. |
| `-q, --quiet` | Potiskuje rezultate, napredak i informativne zapise; upozorenja i pogreške i dalje idu na stderr. |
| `--backend asyncio\|nmap` | Otkrivanje domaćina. `asyncio` (zadano) izravno provjerava priključke usluga; `nmap` prvo pokreće nmap ping pretraživanje i zahtijeva izvršnu datoteku `nmap` u `PATH`. |
| `--timeout SECONDS` | Vrijeme čekanja za provjere bez vlastitog proračuna vremena (zadano 1.0). Ugrađene provjere povezivanja rabe 0,3 s ako tablica usluga ne postavi `timeout`. |
| `--concurrency N` | Broj istodobnih provjera u tijeku (zadano 256). |
| `--deadline SECONDS` | Zaustavlja cijelo skeniranje, uključujući nmap pretraživanje, nakon zadanog vremena (zadano 3600, najviše 604800; varijabla okruženja `HOSTCENSUS_DEADLINE`). Dovršeni domaćini zapisuju se u izvješće s `"complete": false`, povijest i snimka se ne pohranjuju, a `scan` izlazi s kodom 4. |
| `--config PATH` | TOML datoteka s definicijama usluga i neobveznim imenovanim `[profiles]` postavkama. |
| `--profile NAME` | Rabi imenovani profil; zadano se koristi `hostcensus.toml` kada je `--config` izostavljen. |
| `--exclude IP/CIDR` | Dodaje izuzeće; ponavljajte po potrebi. Izuzeti IPv4 domaćin također izuzima IPv6 adrese koje do njega vode: IPv4-preslikane (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) i 6to4. IPv4-preslikani ciljevi i izuzeća tretiraju se kao odgovarajuće IPv4 adrese. |
| `--max-hosts N` | Ograničenje broja adresa koje se provjerava prije izuzeća (zadani i tvrdi maksimum 65.536). |
| `--history PATH` | Pohranjuje dovršeno skeniranje u neobveznu SQLite bazu povijesti. |
| `--services NAMES` | Zarezom odvojen popis naziva usluga za provjeru tim redoslijedom (zadano: sve). |
| `--ports SPEC` | Zarezom odvojen popis oblika `NAME=PORT` (premješta uslugu) ili `PORT` (dodaje običnu TCP provjeru naziva `tcp-PORT`). |
| `--snmp-community-file PATH` | Datoteka koja sadrži SNMPv2c niz zajednice (community) za upit system MIB. Varijable okruženja: `HOSTCENSUS_SNMP_COMMUNITY` (vrijednost) ili `HOSTCENSUS_SNMP_COMMUNITY_FILE` (putanja). |
| `--snmp-user` | SNMPv3 korisnik. Varijabla okruženja: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (zadano), `SHA224`, `SHA256`, `SHA384`, `SHA512` i datoteka sa zaporkom. Varijable okruženja: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ili `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (zadano), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` i datoteka sa zaporkom. Varijable okruženja: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ili `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Dodatno pohranjuje inačicom označenu snimku za `hostcensus diff`. |
| `--tls-ca-file PATH` | Provjerava HTTPS certifikate prema ovom PEM skupu umjesto pohrane sustava. Varijabla okruženja: `HOSTCENSUS_TLS_CA_FILE`. |

Zadano se svaki domaćin provjerava na SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) i HTTPS (TCP 443). TCP priključci ispituju se potpunim povezivanjem. SNMP se ispituje zahtjevom za otkrivanje SNMPv3 pogona, na koji svaki SNMPv3 agent mora odgovoriti bez vjerodajnica; agenti koji podržavaju samo v1/v2c neće biti otkriveni ovom provjerom. Uz pozadinski sustav asyncio domaćin se smatra aktivnim kada bilo koja provjera primi odgovor, uključujući odbijenu vezu, pa domaćin koji odbacuje sve pakete ima `alive=false` i pogrešku "Host is down"; to ne dokazuje da je računalo fizički isključeno. Uz `--backend nmap`, nmap određuje aktivne domaćine (ICMP uz root ovlasti, inače TCP 80/443).

### Otisci usluga

Svaka otvorena usluga dobiva otisak na temelju podataka koje pošalje prije ikakve prijave. Ništa se ne provjerava autentifikacijom osim SNMP upita, i to tek kada dostavite vjerodajnice.

| Provjera | Čita | `version` | Ključevi u `details` |
| --- | --- | --- | --- |
| `ssh` | identifikacijski redak RFC 4253 | softver, npr. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | početno rukovanje za MySQL/MariaDB | inačica poslužitelja | `server_version`, `flavor`, `auth_plugin` ili `error_code`/`error` |
| `http` | odgovor na `HEAD /` | zaglavlje `Server` | `status`, `server` |
| `https` | TLS rukovanje, certifikat, `HEAD /` | zaglavlje `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 otkrivanje; uz vjerodajnice GET za sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; uz vjerodajnice `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` ili `snmp_error` |

Ciljni naziv domaćina razrješava se jednom po domaćinu i svaka se provjera povezuje na tu adresu, zabilježenu kao `address` u rezultatima; naziv se rabi samo za TLS SNI, provjeru certifikata i HTTP zaglavlje `Host`. Naziv koji se ne može razriješiti daje stanja `unknown` i pogrešku `Cannot resolve`. Obrnuti DNS nazivi čuvaju se samo kada sadrže dopuštene znakove naziva domaćina, a istodobno se izvodi najviše 16 upita. HTTPS provjerava certifikat i naziv domaćina prema pohrani povjerenja sustava ili `--tls-ca-file`. Pohrana povjerenja učitava se jednom po skeniranju i ponovno rabi za svaku HTTPS provjeru. TCP povezivanje i TLS rukovanje mjere se zasebno, pa je priključak koji prihvati vezu ali zastane tijekom rukovanja `open` s `tls_error`, a ne `filtered`. Ako provjera ne uspije, rezultat bilježi `cert_verified: false` i `cert_verify_error`; ne pokušava ponovno sa slabijim postavkama niti šalje HTTP zahtjev. Pojedinosti certifikata i HTTP zaglavlja prikupljaju se tek nakon uspješne provjere. Dostavite odgovarajući CA skup za usluge s privatnim izdavateljem certifikata. Starija izvješća mogu sadržavati `cert_read_unverified`, što trenutačne provjere više ne proizvode.

SNMP tajne čitaju se isključivo iz varijabli okruženja ili datoteka (`--snmp-*-file` ili odgovarajuća varijabla `HOSTCENSUS_SNMP_*_FILE`), nikada iz vrijednosti u naredbenom retku koje drugi lokalni korisnici mogu vidjeti u popisu procesa. `--snmp-community`, `--snmp-auth-key` i `--snmp-priv-key` s vrijednošću završavaju izlaznim kodom 2 i navode zamjenu. Datoteka s tajnom mora biti neprazan UTF-8 tekst veličine najviše 4096 bajtova; jedan završni znak novog retka se zanemaruje, a istodobno postavljanje varijable i datoteke za istu tajnu jest pogreška. Pogreške imenuju datoteku, ali nikada ne ispisuju njezin sadržaj. Izvješća skeniranja i povijest namjerno ne uključuju vrijednosti vjerodajnica. Izvoznik ima zasebnu, izričitu opciju `--include-credentials` opisanu u nastavku. Niz zajednice (community) odabire SNMPv2c; korisnik odabire SNMPv3, s provjerom autentičnosti kada je zadan ključ za autentifikaciju i šifriranjem kada su zadana oba ključa (`snmp_security_level` bilježi odabranu razinu). hostcensus odbija, s izlaznim kodom 2, kombiniranje niza zajednice s v3 korisnikom, uporabu ključa privatnosti bez ključa autentifikacije ili uporabu ključeva bez korisnika, te nikada ne ponavlja neuspjeli v3 upit putem v2c ili niže razine sigurnosti. Agenti koji podržavaju samo v1/v2c zanemaruju v3 otkrivanje bez vjerodajnica, pa se prikazuju kao otvoreni tek kada je zadan niz zajednice.

Tekst natpisa (banner) svodi se na ispisive znakove i skraćuje na najviše 256 znakova prije pohrane ili prikaza. Čitanja su također ograničena: 4 KiB po retku, 4 KiB za MySQL pozdrav, 16 KiB za HTTP zaglavlja. SNMP engine ID dulji od 32 okteta skraćuje se prije pohrane. HTTP i HTTPS šalju zaglavlje Host s IPv6 adresom u uglatim zagradama i s brojem priključka kad nije 80 ili 443. CSV ćelije koje počinju pokretačem formule proračunske tablice dobivaju prefiks kako bi ostale običan tekst.

### Ograničenja

Jedno pokretanje prihvaća najviše 65.536 adresa, 64 usluge i 524.288 provjera (broj domaćina pomnožen s brojem usluga); veći zahtjevi izlaze s kodom 2 prije slanja ikakvog prometa. `--concurrency` ograničen je na 4096 utičnica. Svaka provjera ima tvrdi krajnji rok jednak četverostrukom vlastitom vremenskom proračunu. Provjere povezivanja (`tcp`, `ssh`, `mysql`, `http`) rabe 0,3 sekunde ako za uslugu nije postavljen `timeout`. SNMP i HTTPS rabe `--timeout` (zadano 1.0) kada nemaju vlastiti. Provjera koja dosegne krajnji rok bilježi se kao `unknown` s porukom "probe timed out" u `errors`. Lokalne pogreške utičnica (primjerice iscrpljenost opisnika datoteka) također su `unknown` uz zabilježenu pogrešku; nikada se ne računaju kao filtriran priključak ili nedostupan domaćin. Prije provjera hostcensus podiže meko ograničenje otvorenih datoteka prema tvrdom ograničenju kako bi obuhvatio `--concurrency` plus 64 opisnika; kad to nije moguće, prethodna provjera `open files` ne uspijeva i `scan` izlazi s kodom 1 prije slanja prometa. Nmap otkrivanje rabi vremensko ograničenje od 30 sekundi po domaćinu. Prefiks se prosljeđuje alatu nmap u CIDR zapisu, a pretraživanje završava pogreškom i kodom 1 kada nmap vrati manje adresa nego što mu je predano (primjerice naziv koji ne može razriješiti), umjesto da domaćine označi nedostupnima. Ciljni naziv domaćina razrješava se jednom i nmap dobiva tu adresu, tako da otkrivanje i provjere dosežu isto računalo. Cjeloviti prefiks jest jedan nmap proces s rokom podprocesa od 35 sekundi za svakih 256 adresa, zaokruženo naviše. Pretraživanja s izuzećima rabe skupine od po 256 domaćina i rok od 35 sekundi po skupini. Stvaranje radnih zadataka ograničeno je neovisno o veličini raspona. Obrnuti DNS i razrješavanje naziva domaćina imaju zaseban dvosekundni rok; poziv razrješivača koji se nikada ne vrati napušta se na vlastitoj niti kako ne bi zadržao hostcensus dulje od ovih ograničenja. Istodobno radi najviše 16 upita, a napušteni poziv zadržava svoje mjesto dok se ne vrati, čime broj zaglavljenih niti ostaje ograničen; ako svih 16 zastane, kasniji upiti čekaju u redu izvan dvosekundnog roka (koji počinje tek po oslobađanju mjesta) dok `--deadline` ne zaustavi skeniranje. `NetworkScanner` upotrijebljen kao biblioteka bez parametra `deadline` može neograničeno čekati takvo mjesto. `--deadline` (zadano jedan sat) povrh svega ograničava cijelo izvođenje.

### Konfiguriranje usluga

Usluge se mogu prilagoditi putem TOML datoteke:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` je jedan od `tcp`, `ssh`, `mysql`, `http`, `https` ili `snmp` te zadano preuzima naziv usluge kada je to vrsta provjere, inače `tcp`. Samo `snmp` koristi UDP. Nazivi usluga sastoje se od malih slova, znamenki, `-` i `_`. Dvije usluge ne smiju dijeliti isti priključak i protokol; povijest bilježi jedno stanje za taj par. `timeout` je neobvezan, u sekundama, i iznosi najmanje 0,05. Provjere temeljene na povezivanju (`tcp`, `ssh`, `mysql`, `http`) zadano rabe 0,3 sekunde. `snmp` i `https` rabe `--timeout` skeniranja kada usluga nema postavljen `timeout`. `--timeout` ne zamjenjuje proračun koji usluga već ima.

JSON izvješća jesu dokumenti s oznakom inačice (`"format": "hostcensus-report"`, `"version": 1`) koji bilježe cilj, provjerene usluge i postavke uz polje `devices`; `--format json` bez `-o` ispisuje izvješće na stdout umjesto tablice. Svaki JSON izlaz ima objavljenu shemu; pogledajte [JSON izlaz](../../../docs/json-output.md). Uređaji zadržavaju izvorna polja `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` i `errors` te dodaju popis `services` s poljima svake provjere: `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` ili `unknown` kada je provjera lokalno zakazala ili dosegla krajnji rok), `version` i `details`. CSV ispis dobiva završne stupce `services` i `versions` za otvorene usluge. Logičke vrijednosti `ssh`, `snmp` i `mysql` prate usluge s točno tim nazivima.

## Profili inventara, prethodna provjera i lokalna povijest

Imenovani profili dijele TOML datoteku s postojećim definicijama `[services]`. Kopirajte [hostcensus.example.toml](../../../hostcensus.example.toml) u `hostcensus.toml` i postavite mreže kojima upravljate:

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

`preflight` razrješava opcije i profile jednako kao `scan`, uključujući `--concurrency` za provjeru otvorenih datoteka, pa uspješna prethodna provjera znači da će `scan` započeti s istim planom.

Profili prihvaćaju `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency` i `max_hosts`. `services` i `ports` rabe postojeću sintaksu popisa odvojenog zarezima. Izričite CLI opcije nadjačavaju postavke profila; ponovljene opcije `--exclude` dodaju se izuzećima profila. Izričito navedena mreža uz `--profile` mora biti obuhvaćena IP/CIDR opsegom tog profila. Nazivi domaćina i dalje su podržani za izravna skeniranja, ali se ne mogu kombinirati s IP izuzećima. Ograničenja domaćina primjenjuju se prije izuzeća; ukupno ograničenje provjera i dalje vrijedi nakon njih. Izuzeti domaćini izostavljaju se iz provjera usluga i iz neobveznog Nmap otkrivanja.

Svako skeniranje provodi lokalne prethodne provjere prije mrežnog prometa: ograničenja ciljeva/provjera, pristup odredištima, dostupnost neobvezne izvršne datoteke ili omotača za Nmap, shemu povijesti i konfigurirani TLS CA skup. `preflight` ispisuje JSON te ne skenira ciljeve niti stvara bazu povijesti. Privremeno zapisuje susjednu datoteku radi provjere pristupa odredištu bez izmjene postojećeg sadržaja. Zadani pozadinski sustav asyncio i dalje ne zahtijeva ni Nmap ni root. Odredišne putanje moraju biti međusobno različite i različite od ulazne konfiguracije, uključujući tvrde poveznice; simboličke poveznice na odredištu se odbijaju. Neuspjele provjere vraćaju 1; nevaljan opseg ili konfiguracija vraća 2.

Pohrana izvješća i izvoznih skripti zahtijeva podršku za `O_NOFOLLOW`. Na platformama bez te podrške, uključujući Windows, ovakvi zapisi ne uspijevaju bez otvaranja ili skraćivanja odredišne datoteke. Nova izvješća i skripte za izvoz stvaraju se s pristupom samo za vlasnika (način 0600); zamjena postojeće datoteke čuva njezine dozvole. Pisanje u imenovani cjevovod bez čitača odmah završava pogreškom umjesto čekanja. Nova baza `--history` također se stvara samo za vlasnika; postojeća zadržava svoje dozvole. Poruke dnevnika uvijek idu na stderr, tako da stdout nosi isključivo rezultate. Izvozi koji sadrže vjerodajnice uvijek prisilno postavljaju način 0600.

Povijest je neobvezna i nadopunjuje postojeće JSON snimke te naredbu `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Rabite identifikatore iz naredbe `history`; primjer pretpostavlja novu bazu podataka. Snimke se pohranjuju transakcijski s UTC vremenima početka/završetka, inačicom paketa, stvarnim postavkama bez tajni, sažetcima i svim opažanjima domaćina/usluga, uključujući pogreške po domaćinu. Nepotpuna opažanja domaćina se zadržavaju. Otkazana pokretanja se ne spremaju. Postojeći ugovori za izvješća, snimke, izvoz i izlazne kodove skeniranja ostaju očuvani.

`history` ispisuje JSON sažetke bez učitavanja svih povijesnih podataka o uređajima. `compare` čita dva spremljena skeniranja, zahtijeva istovjetne ciljeve i odabrane priključke te izvješćuje o promjenama odziva, stanja i stanja priključaka. Identifikator ranijeg skeniranja mora prethoditi kasnijem. Kad oba skeniranja imaju zabilježen `timeout` ili `backend` i te se vrijednosti razlikuju, izvješće bilježi upozorenje i ipak uspoređuje opažanja. Drugačije vrijeme čekanja može učiniti da filtrirani priključak izgleda otvoren. Pogreške skenera i nepoznata stanja priključaka označavaju se kao nesigurna umjesto da se tretiraju kao potvrđen nestanak ili zatvaranje: domaćini s pogreškama pojavljuju se u `uncertain_hosts`, a svaki prijelaz priključka koji uključuje `unknown` (uključujući unknown u oba skeniranja) navodi se u `unconfirmed_ports` umjesto u `port_changes`, osim priključka otvorenog u kasnijem skeniranju, što jest promjena priključka. `compare` i `diff` razvrstavaju priključke prema istom pravilu. `no_longer_responding` označava izostanak odgovora, a ne dokaz uklanjanja uređaja. Izlazni kod 0 pri skeniranju ne jamči da je svaki domaćin odgovorio: provjerite pogreške po domaćinu. Uspješna usporedba vraća 0 bez obzira ima li promjena; postojeća datotečna naredba `diff` zadržava ugovor izlaznog koda 3. Nepodržana ili oštećena povijest vraća 1.

Povijest pohranjuje podatke o inventaru, pa odaberite primjereno zaštićenu lokalnu mapu. Datoteke profila i pohranjene postavke ne sadrže SNMP vjerodajnice; upravljanje vjerodajnicama ostaje putem postojećih opcija pri izvođenju i okruženja.

## Usporedba inventara

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Snimka je JSON s poljima `format: "hostcensus-snapshot"`, `version: 1`, inačicom alata hostcensus, UTC vremenom nastanka, ciljem, postavkama `timeout` i `backend` kada ih je skeniranje zabilježilo, provjerenim uslugama i aktivnim domaćinima u istom obliku kao `-o` izvješće. Nedostupni domaćini se izostavljaju. `diff` također prihvaća obična JSON izvješća iz `scan -o`, uključujući ona nastala prije uvođenja polja `services`.

`diff` prijavljuje nove i nestale domaćine, priključke koji su se otvorili ili zatvorili na domaćinima prisutnim u obje snimke te usluge čija se `version` promijenila. Priključci provjereni samo u jednom od dva skeniranja ne uspoređuju se, uz pripadajuće upozorenje. Neuspjela opažanja nikada se ne tumače kao "nema promjena": priključak sa stanjem `unknown` u bilo kojem skeniranju koji nije otvoren u kasnijem navodi se pod `unconfirmed`, a ne pod `closed`, s `before` vrijednošću `open`, `unknown` ili `not-open` (provjeren i zatvoren ili filtriran) te `after` vrijednošću `unknown` ili `not-open`; priključak koji je sada otvoren prijavljuje se pod `opened` čak i ako je prijašnja provjera zakazala. Domaćin čije su sve provjere zakazale bez odgovora u bilo kojem skeniranju navodi se pod `unsettled_hosts` (s `before`/`after` vrijednošću `up`, `uncertain` ili `absent`, uključujući slučaj kada je zakazao u oba skeniranja ili nedostaje u drugoj datoteci) umjesto pod `vanished_hosts`; ako odgovori u kasnijem skeniranju, prijavljuje se i kao novi domaćin sa svojim otvorenim priključcima. Snimke čuvaju te neuspjele domaćine upravo zbog toga. Upozorenje se prikazuje i kada se ciljevi razlikuju te kada obje datoteke bilježe timeout ili backend i te se vrijednosti razlikuju. `-o PATH` također zapisuje JSON oblik u datoteku.

Izvješće iz skeniranja zaustavljenog opcijom `--deadline` (`"complete": false`) navodi samo domaćine do kojih je skeniranje doprlo, pa ga `diff` i `export` odbijaju s izlaznim kodom 2. `--allow-partial` ga prihvaća uz upozorenje na stderr: `diff` tada domaćine koje nepotpuno skeniranje uopće nije navelo svrstava u `unsettled_hosts` kao `unscanned` umjesto kao nestale (domaćin naveden kao nedostupan i dalje ostaje nestao), postavlja `partial` na true i nikada ne prijavljuje izostanak promjena, a `export` upisuje upozorenje u zaglavlje skripte.

Izlazni kodovi za `diff`: `0` nema promjena, `3` pronađene promjene, opažanja koja se nisu mogla potvrditi ili nepotpun ulaz (`changed` je true kad god je bilo koji popis, uključujući `unsettled_hosts` i `unconfirmed`, neprazan ili je `partial` true), `2` datoteka nedostaje, nečitljiva je, nije podržana snimka ili je nepotpuna bez `--allow-partial`, `1` datoteku `-o` nije bilo moguće zapisati.

## Izvoz za Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (odvojak sustava Cacti 1.2.31) nema skupni uvoz uređaja iz datoteke. Podržani način dodavanja uređaja iz skripte jest `cli/add_device.php`, jedan uređaj po pozivu, s argumentima `--option=value`. `hostcensus export` zapisuje POSIX `sh` skriptu tih poziva:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Svaki aktivni domaćin postaje `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Domaćini kod kojih je SNMP upit tijekom skeniranja uspio dobivaju `--version=2 --community=...` ili `--version=3 --username=... --authproto=... --password=...` (uz `--privproto`/`--privpass` za authPriv), `--port` i `--avail=snmp`. SNMPv3 izvoz zahtijeva `--snmp-user`, a noAuthNoPriv se odbija jer `add_device.php` zahtijeva v3 zaporku.
- Ostali domaćini dobivaju `--version=0 --avail=ping`, s `--ping_method=tcp --ping_port=` postavljenim na prvi otvoreni TCP priključak ili ICMP ako nema nijednog.
- `--notes` navodi otvorene usluge i inačice. `--description` je obrnuti DNS naziv kada je jednostavan (slova, znamenke, `.`, `_`, `-`), inače IP adresa, te se čini jedinstvenim jer `add_device.php` postojeći opis tumači kao ažuriranje tog uređaja.

Svaka vrijednost provjerava se i ograđuje za ljusku pomoću `shlex.quote`. Zadano se ne zapisuje nijedna SNMP tajna: skripta pri izvođenju proširuje `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ili `HOSTCENSUS_SNMP_PRIV_KEY` i zaustavlja se ako neka nije postavljena. `--include-credentials` umjesto toga upisuje vrijednosti tih varijabli okruženja u skriptu, stvara je s načinom 0600 i bilježi upozorenje. Sam `add_device.php` ispisuje niz zajednice i prima tajne kao argumente koji su vidljivi u popisu procesa Kadupul poslužitelja dok se svaki poziv izvodi.

`add_device.php` izlazi s kodom 1 za duplikate i pogreške; skripta nastavlja, broji neuspjehe i izlazi s kodom 1 ako bilo koji uređaj nije dodan. Identifikatori predložaka dobivaju se naredbom `php cli/add_device.php --list-host-templates`. Izlazni kodovi za `export`: `0` zapisano, `2` nečitljiv ulaz, nepotpuno skeniranje bez `--allow-partial` ili podatci koji se ne mogu sigurno izvesti, `1` skriptu nije bilo moguće zapisati.

## Upravljanje inačicama i postupak objave

hostcensus slijedi [Semantičko označavanje inačica](https://semver.org/spec/v2.0.0.html): kompatibilni ispravci povećavaju zakrpnu (patch) inačicu, kompatibilne značajke i oznake zastarjelosti povećavaju sporednu (minor) inačicu, a nekompatibilne promjene povećavaju glavnu (major) inačicu. Naredbe i opcije, izlazni kodovi i JSON sheme čine javni ugovor; zastarjelo ponašanje nastavlja raditi do sljedećeg velikog izdanja, osim ako sigurnosni ispravak ne zahtijeva raniju promjenu (tada zapisnik promjena objašnjava razlog).

release-please otvara PR za izdanje na temelju naslova Conventional Commit poruka na grani `main`, ažurirajući `pyproject.toml`, `uv.lock` i `CHANGES.md`. Spajanje tog PR-a stvara oznaku `vMAJOR.MINOR.PATCH` i nacrt GitHub izdanja na koji CI prilaže testirani wheel, izvornu distribuciju i kontrolne zbrojeve; GitHub pohranjuje atestacije izgradnje za te datoteke putem svog API-ja za atestacije. Održavatelj pregledava i objavljuje nacrt nakon prilaganja datoteka. Izdanja se nikada ne zamjenjuju.

Pouzdano objavljivanje na servisu PyPI neobvezno je i zahtijeva vlasništvo nad projektom, pouzdanog izdavača i okruženje `pypi`. Objavljuje iste provjerene artefakte izdanja bez ponovne izgradnje i bez pohrane API tokena. Označena izdanja u ovom javnom repozitoriju generiraju GitHub atestacije artefakata; privatni odvojci zahtijevaju podržan plan i izričito uključivanje. Pogledajte [potpuni vodič za izdanja](../../../docs/releasing.md) za postavljanje, točne naredbe i ponovne pokušaje.

## Razvoj

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Razvojni alati nalaze se u [PEP 735](https://peps.python.org/pep-0735/) skupinama ovisnosti u datoteci `pyproject.toml` (`dev`, `fuzz`, `build`), pa se nikada ne pojavljuju u objavljenim metapodatcima paketa. `uv.lock` jedina je zaključana datoteka ovisnosti; CI instalira naredbom `uv sync --locked` i pada kada je datoteka zastarjela. Odaberite tumač putem `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) ili bilo kojeg Pythona 3.12+.

CI provodi minimalni prag pokrivenosti paketa testovima od 90%. Jedinični testovi uključuju nadzirane loopback poslužitelje te izvanmrežne slučajeve za profile, povijest i provjeru izdanja; Compose okolina pokreće OpenSSH, MariaDB, nginx i net-snmp na izoliranom mrežnom mostu. Pokrenite je naredbom `make test-integration`. Pogledajte [CONTRIBUTING.md](../../../CONTRIBUTING.md) i [alate za izdanja](../../../scripts/README.md).

Izvršni spremnik radi pod UID/GID 10001 bez matične mape, bez prijave u ljusku i bez alata pip te može pisati u `/app/output`. Omogućite tom korisniku pravo pisanja u svaku priključenu izlaznu mapu. Ne zahtijeva nikakve dodatne sposobnosti i radi s korijenskim datotečnim sustavom samo za čitanje, pa se može pokrenuti ovako:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap u ovom spremniku rabi svoje neprivilegirano TCP otkrivanje. CI prekida izgradnju slike pri svakoj popravljivoj ranjivosti razine HIGH ili CRITICAL koju prijavi Trivy.

## Provjere lanca opskrbe

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) pokreće se na grani main i tjedno, objavljuje svoj stvarni rezultat i učitava nalaze u GitHub skeniranje kôda. Radnje i osnovne slike spremnika pričvršćene su nepromjenjivim sažetcima; Python ovisnosti razriješene su u `uv.lock`. Pogreške alata Bandit ruše CI, a ograničeni Atheris fuzzing ispituje SSH, MySQL, HTTP, certifikat i SNMPv3 BER raščlanjivače bez mrežnog pristupa.

Scorecard također mjeri povijesnu aktivnost pregleda, raznolikost suradnika i podrijetlo izdanja. Ti rezultati odražavaju stvarne dokaze; oni nisu tvrdnja da je svaka provjera upravljanja ili povijesnih izdanja ispunjena. Pogledajte [SECURITY.md](../../../SECURITY.md) i [podrijetlo izdanja](../../../docs/releasing.md).

## Lokalizacija

CLI poruke te terminalske tablice sažetka i usporedbe podržavaju 48 lokaliteta (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`, `bs`, `hr`, `sr`) bez ikakvih dodatnih ovisnosti pri izvođenju. Određivanje poštuje `--lang`, zatim `LC_ALL`, `LC_MESSAGES` i `LANG`, uz povratak na `en`. JSON sheme, CSV stupci i izvozne skripte ostaju nepromijenjeni u svim lokalitetima.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Doprinosi

Doprinosi trebaju uključivati ponovljiv primjer, očuvati dokumentirane ugovore za CLI i oblike podataka te proći gore navedene provjere kakvoće. Pogledajte [CONTRIBUTING.md](../../../CONTRIBUTING.md) za razvojni tijek rada i [vodič za izdanja](../../../docs/releasing.md) za odluke o kompatibilnosti i označavanju inačica.

## Sigurnost i status licencije

Pogledajte [SECURITY.md](../../../SECURITY.md) za povjerljivo prijavljivanje ranjivosti i podržane inačice. hostcensus je licenciran pod [MIT licencijom](../../../LICENSE).

Zaglavlja izvornih datoteka rabe SPDX identifikatore i čuvaju zasluge suradnika iz Git povijesti. Pogledajte [AUTHORS.md](../../../AUTHORS.md) za pripisivanje zasluga. Binarni testni zapisi i generirana zaključana datoteka rabe susjedne `.license` datoteke; tekst MIT licencije nalazi se u `LICENSES/MIT.txt`.
