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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · **Bosanski** · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Hrvatski](../hr/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Српски](../sr/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus je Python CLI alat za ponovljivu inventarizaciju servisa u mrežama kojima upravljate. Bilježi šta uređaji izlažu, poredi zapažanja kroz vrijeme i generiše skripte za uvoz u Kadupul. Podrazumijevani pozadinski mehanizam koristi asyncio sokete bez root ovlaštenja; opciono otkrivanje putem Nmap alata može identifikovati hostove i izvan konfigurisanih portova servisa.

## Zašto hostcensus

Jednokratni izvještaj o portovima ne objašnjava da li se naredno zapažanje promijenilo ili jednostavno nije uspjelo. hostcensus kombinuje eksplicitna stanja servisa, ograničene provjere, višekratno upotrebljive profile skeniranja i lokalnu historiju. Operatori mogu ponoviti isti opseg, ispitati greške i razlikovati nesigurna zapažanja od potvrđenih promjena.

- **Dokazi o servisima:** SSH identifikacija, MySQL pozdravne poruke, HTTP zaglavlja, opažanja TLS certifikata te SNMP otkrivanje ili autorizovani upiti za system-MIB.
- **Ponovljiv opseg:** imenovani TOML profili, aditivna izuzeća, podesivi servisi, ograničenja broja hostova i provjera te ograničen broj radnika.
- **Provjere prije saobraćaja:** lokalna predprovjera validira ciljeve, alate, pristup odredištima, šemu historije i konfigurisane TLS CA pakete.
- **Historija inventara:** transakcijski SQLite snimci zadržavaju sva zapažanja; poređenja zadržavaju vidljivim greške skenera i nepoznata stanja.
- **Interoperabilan izlaz:** prikaz u terminalu, JSON i CSV izvještaji, verzionisani snimci u datotekama i skripte za uvoz u Kadupul.

CI pokriva Python 3.12, 3.13 i 3.14 na sistemima Linux i macOS, uz kontrolisanu Compose integracijsku laboratoriju. Kod koristi moderne alijase tipova, tipizirane rezultate predprovjere, slotovane profile s parametrima samo po ključnoj riječi i strukturirano asinhrono čišćenje uz očuvanje podrške za te verzije okruženja. Pogledajte [Verzionisanje i izdanja](../../../docs/releasing.md) za ugovor o SemVer kompatibilnosti i proces objavljivanja na GitHubu. Oznaka izdanja opisuje objavljene artefakte, a ne radnu kopiju: najnovija objavljena oznaka trenutno je `v0.3.0`, dok ova radna kopija koristi verziju paketa `3.0.0`. Instalirajte iz radne kopije da biste koristili ovdje dokumentovane mogućnosti inventarizacije.

Počnite sa [instalacijom](#instalacija), zatim pređite na [profile i historiju](#profili-inventara-predprovjera-i-lokalna-historija). Za detalje integracije pogledajte [otiske servisa](#otisci-servisa), [poređenje datoteka](#poređenje-inventara) i [izvoz za Kadupul](#izvoz-za-kadupul).

## Instalacija

Potreban je Python 3.12 ili noviji; testirana matrica pokriva Python 3.12-3.14. Iz ove radne kopije instalirajte zaključane zavisnosti za izvršavanje:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Za opciono Nmap otkrivanje hostova instalirajte izvršnu datoteku Nmap putem upravitelja paketa vaše platforme; nije potreban dodatni Python paket. XML izlaz alata Nmap parsira se pomoću biblioteke defusedxml, koja je osnovna zavisnost, pa se proširivanje entiteta odbija. hostcensus pokreće `nmap` pronađen na putanji `PATH` direktno s fiksnom listom argumenata, krajnjim rokom koji raste s veličinom prefiksa i ograničenjem izlaza od 64 MiB. Nmap nije potreban za podrazumijevani pozadinski mehanizam.

## Migracija sa netprobe

hostcensus je novo ime za netprobe, objavljeno u verziji 3.0.0. Projekat nikada nije bio objavljen na PyPI ni pod jednim imenom, pa su instalacije dolazile iz radne kopije ili GitHub izdanja. GitHub repozitorij zadržava svoje postojeće ime.

| Ranije | Sada | Kompatibilnost |
| --- | --- | --- |
| Distribucija `netprobe` | `hostcensus` | Ponovo instalirajte iz radne kopije; paket pod starim imenom ne postoji. |
| Komanda `netprobe` | `hostcensus` | `netprobe` i dalje radi i ispisuje jednu liniju upozorenja o zastarjelosti na stderr. Izlazni kodovi i stdout ostaju nepromijenjeni. Bit će uklonjeno u narednom velikom izdanju. |
| Varijable okruženja `NETPROBE_*` | `HOSTCENSUS_*` | Varijabla `NETPROBE_*` koristi se kada njen parnjak `HOSTCENSUS_*` nije postavljen, uz jedno upozorenje na stderr koje navodi imena varijabli, a nikada njihove vrijednosti. `HOSTCENSUS_*` ima prednost kada su obje postavljene. Bit će uklonjeno u narednom velikom izdanju. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Nekompatibilna promjena.** Nije instaliran zamjenski modul za uvoz; ažurirajte uvoze. |
| Oznaka Docker slike `network-discovery:test` (samo CI) i korisnik kontejnera `netprobe` | `hostcensus:test`, korisnik `hostcensus` | Nijedna slika nikada nije objavljena u registru. Ponovo izgradite sliku i koristite ulaznu tačku `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Postojeća datoteka sa starim podrazumijevanim imenom i dalje se koristi uz upozorenje sve dok novo ime ne postoji. Eksplicitne putanje `--config` i `--history` ostaju netaknute. |
| Izvještaji i snimci s `"format": "netprobe-report"` ili `"netprobe-snapshot"` te poljem `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` i `export` i dalje učitavaju datoteke zapisane pod starim imenom, a objavljene JSON šeme prihvataju oba oblika. Nove datoteke koriste nova imena. SQLite baze historije ostaju nepromijenjene i učitavaju se kao ranije. |
| Kadupul skripte iz `netprobe export` | Skripte iz `hostcensus export` | Stare skripte nastavljaju raditi i prilikom pokretanja i dalje čitaju `NETPROBE_SNMP_*`. Nove skripte čitaju `HOSTCENSUS_SNMP_*`. |

## Brzi primjer

Pokrenuto iz testnog kontejnera integracijske laboratorije opisane u odjeljku Razvoj; izlaz je skraćen:

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

| Komanda | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | zapažanja ili izvještaj zapisani | neuspjela predprovjera/pozadinski mehanizam, historija ili zapisivanje izvještaja/snimka | neispravan cilj, opcije, konfiguracija ili ograničenja | - | dostignut `--deadline`; nepotpun izvještaj zapisan, historija i snimak preskočeni |
| `preflight` | provjere prošle | lokalna provjera nije uspjela | neispravan cilj/konfiguracija ili sukobljena odredišta | - | - |
| `profiles` | prikazani validirani profili | - | nečitljiva/neispravna konfiguracija ili izbor | - | - |
| `history` | prikazani sažeci | nedostajuća, neispravna ili nepodržana historija | neispravne CLI opcije | - | - |
| `compare` | poređenje proizvedeno, uključujući slučaj kada postoje promjene | nečitljiva historija, nekompatibilan opseg/redoslijed ili greška pri zapisivanju | neispravne CLI opcije | - | - |
| `diff` | nema promjena | datoteka `-o` se nije mogla zapisati | nedostajući, nečitljiv ili nepodržan ulaz, ili nepotpuno skeniranje bez `--allow-partial` | pronađene promjene, nepotvrđena zapažanja ili nepotpuno skeniranje | - |
| `export` | skripta zapisana | skripta se nije mogla zapisati | nečitljiv ulaz, nepotpuno skeniranje bez `--allow-partial`, ili podaci koji se ne mogu sigurno izvesti | - | - |

## Struktura

| Modul | Odgovornost |
| --- | --- |
| `cli.py` | Opcije komandi, razrješavanje profila, predprovjera, skeniranje i izvještavanje |
| `scanner.py`, `probes.py` | Proširivanje ciljeva, ograničeni radnici, otkrivanje hostova i opažanje servisa |
| `config.py`, `profiles.py` | Definicije servisa i validirani profili inventara |
| `models.py`, `output.py` | Tipovi rezultata i ispis za terminal, JSON i CSV |
| `history.py`, `diff.py` | SQLite historija i poređenje verzionisanih snimaka iz datoteka |
| `preflight.py` | Lokalne provjere i vremenski ograničeno očitanje Nmap verzije |
| `export.py` | Validirane i sigurno citirane skripte za uvoz u Kadupul |

Svako opažanje servisa bilježi njegovo stanje odvojeno od oglašenog identiteta. Čitanja i krajnji rokovi su ograničeni; izuzeci pri provjerama ostaju zabilježeni u greškama hosta. SQLite historija koristi transakcije, eksplicitno zatvaranje konekcija te putanje samo za čitanje prilikom listanja i poređenja. SNMP tajne ulaze isključivo putem varijabli okruženja ili datoteka s tajnama; historija inventara čuva efektivne postavke bez tajni. Pogledajte [Arhitekturu](../../../docs/architecture.md) za cjevovod skeniranja, njegova ograničenja i granice povjerenja, te [SECURITY.md](../../../SECURITY.md#authorized-use) za ovlaštenu upotrebu.

## Upotreba

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
| `NETWORK` | CIDR, IP ili naziv hosta; opciono uz `--profile`. Identifikatori IPv6 opsega se odbijaju. |
| `-o, --output PATH` | Zapisuje izvještaj u datoteku. Format prati ekstenziju (`.json`, `.csv`); ostale ekstenzije se vraćaju na JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Forsira format izvještaja. Bez `--output`, `json` ispisuje na stdout, `auto` prikazuje podrazumijevanu tabelu, a `csv` i `kadupul` se ignorišu uz upozorenje. `.sh` bira `kadupul`. |
| `-v, --verbose` | Detaljno zapisivanje za otklanjanje grešaka. |
| `-q, --quiet` | Potiskuje rezultate, napredak i informativne zapise; upozorenja i greške se i dalje prikazuju na stderr. |
| `--backend asyncio\|nmap` | Otkrivanje hostova. `asyncio` (podrazumijevano) direktno provjerava portove servisa; `nmap` najprije pokreće nmap ping pretragu i zahtijeva izvršnu datoteku `nmap` u `PATH`. |
| `--timeout SECONDS` | Vrijeme čekanja za provjere koje ne postavljaju sopstveni budžet (podrazumijevano 1.0). Ugrađene provjere povezivanja koriste 0.3 s osim ako tabela servisa ne definiše `timeout`. |
| `--concurrency N` | Broj istovremenih provjera u toku (podrazumijevano 256). |
| `--deadline SECONDS` | Zaustavlja cijelo skeniranje, uključujući nmap pretragu, nakon zadatog vremena (podrazumijevano 3600, najviše 604800; varijabla okruženja `HOSTCENSUS_DEADLINE`). Obrađeni hostovi se zapisuju u izvještaj sa `"complete": false`, historija i snimak se ne zapisuju, a `scan` izlazi s kodom 4. |
| `--config PATH` | TOML datoteka s definicijama servisa i opcionim imenovanim `[profiles]` postavkama. |
| `--profile NAME` | Koristi imenovani profil; podrazumijevano koristi `hostcensus.toml` kada je `--config` izostavljen. |
| `--exclude IP/CIDR` | Dodaje izuzeće; ponavljajte po potrebi. Izuzeti IPv4 host također izuzima IPv6 adrese koje vode do njega: IPv4-mapirane (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) i 6to4. IPv4-mapirani ciljevi i izuzeća tretiraju se kao IPv4 adrese koje predstavljaju. |
| `--max-hosts N` | Ograničenje broja adresa koje se provjerava prije izuzeća (podrazumijevani i tvrdi maksimum 65.536). |
| `--history PATH` | Bilježi završeno skeniranje u opcionu SQLite bazu historije. |
| `--services NAMES` | Lista naziva servisa odvojena zarezima za provjeru tim redoslijedom (podrazumijevano: svi). |
| `--ports SPEC` | Lista odvojena zarezima oblika `NAME=PORT` (premješta servis) ili `PORT` (dodaje običnu TCP provjeru pod nazivom `tcp-PORT`). |
| `--snmp-community-file PATH` | Datoteka koja sadrži SNMPv2c community string za upit system MIB. Varijable okruženja: `HOSTCENSUS_SNMP_COMMUNITY` (vrijednost) ili `HOSTCENSUS_SNMP_COMMUNITY_FILE` (putanja). |
| `--snmp-user` | SNMPv3 korisnik. Varijabla okruženja: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (podrazumijevano), `SHA224`, `SHA256`, `SHA384`, `SHA512` i datoteka sa lozinkom. Varijable okruženja: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ili `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (podrazumijevano), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` i datoteka sa lozinkom. Varijable okruženja: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ili `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Dodatno zapisuje verzionisani snimak za `hostcensus diff`. |
| `--tls-ca-file PATH` | Provjerava HTTPS certifikate prema ovom PEM paketu umjesto sistemskog skladišta. Varijabla okruženja: `HOSTCENSUS_TLS_CA_FILE`. |

Podrazumijevano se svaki host provjerava na SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) i HTTPS (TCP 443). TCP portovi se testiraju potpunim povezivanjem. SNMP se testira zahtjevom za otkrivanje SNMPv3 mehanizma, na koji svaki SNMPv3 agent mora odgovoriti bez akreditiva; agenti koji govore samo v1/v2c neće biti otkriveni ovom provjerom. S pozadinskim mehanizmom asyncio host se smatra aktivnim kada bilo koja provjera dobije odgovor, uključujući odbijenu konekciju, pa host koji odbacuje sve provjere ima `alive=false` i grešku "Host is down"; to ne dokazuje da je fizički isključen. S `--backend nmap`, nmap odlučuje koji su hostovi aktivni (ICMP kao root, inače TCP 80/443).

### Otisci servisa

Svaki otvoreni servis dobija otisak na osnovu onoga što pošalje prije bilo kakve prijave. Ništa se ne autentifikuje osim SNMP upita, i to samo kada dostavite akreditive.

| Provjera | Čita | `version` | Ključevi u `details` |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 identifikacijski red | softver, npr. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Početno rukovanje za MySQL/MariaDB | verzija servera | `server_version`, `flavor`, `auth_plugin` ili `error_code`/`error` |
| `http` | Odgovor na `HEAD /` | zaglavlje `Server` | `status`, `server` |
| `https` | TLS rukovanje, certifikat, `HEAD /` | zaglavlje `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 otkrivanje; uz akreditive GET za sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; uz akreditive `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` ili `snmp_error` |

Ciljni naziv hosta razrješava se jednom po hostu i svaka provjera se povezuje na tu adresu, zabilježenu kao `address` u rezultatima; naziv se koristi samo za TLS SNI, verifikaciju certifikata i HTTP zaglavlje `Host`. Naziv koji se ne može razriješiti daje stanja `unknown` i grešku `Cannot resolve`. Obrnuti DNS nazivi se zadržavaju samo kada sadrže znakove valjanog naziva hosta, a najviše 16 upita radi istovremeno. HTTPS koristi verifikaciju certifikata i naziva hosta prema sistemskom skladištu ili `--tls-ca-file`. Skladište povjerenja učitava se jednom za skeniranje i ponovo koristi za svaku HTTPS provjeru. TCP povezivanje i TLS rukovanje mjere se zasebno, pa je port koji prihvati konekciju ali zastane u rukovanju `open` sa `tls_error`, a ne `filtered`. Ako verifikacija ne uspije, rezultat bilježi `cert_verified: false` i `cert_verify_error`; ne pokušava ponovo sa slabijim postavkama niti šalje HTTP zahtjev. Detalji certifikata i HTTP zaglavlja prikupljaju se tek nakon uspješne verifikacije. Dostavite odgovarajući CA paket za servise sa privatnim CA. Stariji izvještaji mogu sadržavati `cert_read_unverified`, što trenutne provjere više ne proizvode.

SNMP tajne se čitaju isključivo iz varijabli okruženja ili datoteka (`--snmp-*-file` ili odgovarajuća varijabla `HOSTCENSUS_SNMP_*_FILE`), nikada iz vrijednosti na komandnoj liniji koje drugi lokalni korisnici mogu vidjeti u listi procesa. `--snmp-community`, `--snmp-auth-key` i `--snmp-priv-key` s vrijednošću završavaju izlaznim kodom 2 i navode zamjenu. Datoteka s tajnom mora biti neprazan UTF-8 tekst od najviše 4096 bajtova; jedan završni znak novog reda se zanemaruje, a postavljanje i varijable i datoteke za istu tajnu je greška. Greške navode naziv datoteke ali nikada ne ispisuju njen sadržaj. Izvještaji skeniranja i historija namjerno ne uključuju vrijednosti akreditiva. Izvoznik ima zasebnu, eksplicitnu opciju `--include-credentials` opisanu u nastavku. Community bira SNMPv2c; korisnik bira SNMPv3, uz autentifikaciju kada je dat ključ autentifikacije i privatnost kada su data oba ključa (`snmp_security_level` bilježi odabrani nivo). hostcensus odbija, uz izlazni kod 2, kombinovanje community stringa sa v3 korisnikom, korištenje ključa privatnosti bez ključa autentifikacije ili korištenje ključeva bez korisnika, i nikada ne ponavlja neuspjeli v3 upit sa v2c ili nižim nivoom sigurnosti. Agenti koji govore samo v1/v2c zanemaruju SNMPv3 otkrivanje bez akreditiva, pa se prikazuju kao otvoreni samo kada se navede community.

Tekst banera se svodi na ispisive znakove i ograničava na 256 znakova prije pohrane ili prikaza. Čitanja su također ograničena: 4 KiB po liniji, 4 KiB za MySQL pozdrav, 16 KiB za HTTP zaglavlja. SNMP engine ID duži od 32 okteta skraćuje se prije pohrane. HTTP i HTTPS šalju zaglavlje Host sa IPv6 adresom u uglastim zagradama i s portom kada nije 80 ili 443. CSV ćelije koje počinju okidačem formula za proračunske tabele dobijaju prefiks kako bi ćelija ostala tekst.

### Ograničenja

Jedno pokretanje prihvata najviše 65.536 adresa, 64 servisa i 524.288 provjera (hostovi pomnoženi sa servisima); veći zahtjevi izlaze s kodom 2 prije slanja bilo kakvog saobraćaja. `--concurrency` je ograničen na 4096 soketa. Svaka provjera ima tvrdi krajnji rok jednak četverostrukom sopstvenom budžetu. Provjere povezivanja (`tcp`, `ssh`, `mysql`, `http`) koriste 0,3 sekunde osim ako taj servis ne postavi `timeout`. SNMP i HTTPS koriste `--timeout` (podrazumijevano 1.0) kada nemaju sopstveni. Provjera koja dostigne krajnji rok prijavljuje se kao `unknown` s porukom "probe timed out" u `errors`. Lokalne greške soketa (na primjer nestanak opisnika datoteka) također su `unknown` uz zabilježenu grešku; nikada se ne računaju kao filtriran port ili nedostupan host. Prije provjera, hostcensus podiže meko ograničenje otvorenih datoteka prema tvrdom ograničenju kako bi stalo `--concurrency` plus 64 opisnika; kada to nije moguće, predprovjera `open files` ne uspijeva i `scan` izlazi s kodom 1 prije slanja saobraćaja. Nmap otkrivanje koristi vremensko ograničenje od 30 sekundi po hostu. Prefiks se prosljeđuje alatu nmap u CIDR obliku, a pretraga ne uspijeva s kodom 1 kada nmap vrati manje adresa nego što mu je dato (na primjer naziv koji ne može razriješiti), umjesto da hostove označi nedostupnim. Ciljni naziv hosta razrješava se jednom i nmap dobija tu adresu, tako da otkrivanje i provjere dolaze do istog računara. Pun prefiks je jedan nmap proces čiji je rok podprocesa 35 sekundi za svakih 256 adresa, zaokruženo naviše. Pretrage s izuzećima koriste pakete od po 256 hostova i rok od 35 sekundi po paketu. Kreiranje radnika je ograničeno nezavisno od veličine opsega. Obrnuti DNS i razrješavanje naziva hostova imaju zaseban rok od dvije sekunde; poziv razrješavača koji se nikada ne vrati napušta se na sopstvenoj niti, tako da ne može zadržati hostcensus preko ovih granica. Istovremeno radi najviše 16 upita, a napušteni poziv zadržava svoje mjesto dok se ne vrati, pa broj zaglavljenih niti ostaje ograničen; ako se svih 16 zaglavi, kasniji upiti čekaju u redu izvan dvosekundnog roka (koji počinje tek kada se mjesto oslobodi) dok `--deadline` ne zaustavi skeniranje. `NetworkScanner` korišten kao biblioteka bez parametra `deadline` može čekati takvo mjesto neograničeno dugo. `--deadline` (podrazumijevano jedan sat) ograničava cijelo pokretanje povrh svega navedenog.

### Konfigurisanje servisa

Servisi se mogu mijenjati putem TOML datoteke:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` je jedan od `tcp`, `ssh`, `mysql`, `http`, `https` ili `snmp` i podrazumijevano uzima naziv servisa kada je to vrsta provjere, inače `tcp`. Samo `snmp` koristi UDP. Nazivi servisa sastoje se od malih slova, cifara, `-` i `_`. Dva servisa ne mogu dijeliti isti port i protokol; historija bilježi jedno stanje za taj par. `timeout` je opcion, u sekundama, i iznosi najmanje 0,05. Provjere zasnovane na povezivanju (`tcp`, `ssh`, `mysql`, `http`) podrazumijevano koriste 0,3 sekunde. `snmp` i `https` koriste `--timeout` skeniranja kada servis ne postavi `timeout`. `--timeout` ne zamjenjuje budžet koji servis već ima.

JSON izvještaji su verzionisani dokumenti (`"format": "hostcensus-report"`, `"version": 1`) koji bilježe cilj, provjerene servise i postavke pored polja `devices`; `--format json` bez `-o` ispisuje izvještaj na stdout umjesto tabele. Svaki JSON izlaz ima objavljenu šemu; pogledajte [JSON izlaz](../../../docs/json-output.md). Uređaji zadržavaju izvorna polja `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` i `errors` te dodaju listu `services` sa poljima svake provjere: `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` ili `unknown` kada je provjera lokalno pala ili dostigla krajnji rok), `version` i `details`. CSV izlaz dobija završne kolone `services` i `versions` za otvorene servise. Logičke vrijednosti `ssh`, `snmp` i `mysql` prate servise s tačno tim nazivima.

## Profili inventara, predprovjera i lokalna historija

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

`preflight` razrješava opcije i profile potpuno isto kao `scan`, uključujući `--concurrency` za provjeru otvorenih datoteka, tako da uspješna predprovjera znači da će `scan` krenuti s istim planom.

Profili prihvataju `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency` i `max_hosts`. `services` i `ports` koriste postojeću sintaksu liste odvojene zarezima. Eksplicitne CLI opcije nadjačavaju postavke profila; ponovljene opcije `--exclude` dodaju se izuzećima profila. Eksplicitna mreža uz `--profile` mora biti sadržana u IP/CIDR opsegu tog profila. Nazivi hostova ostaju podržani za direktna skeniranja, ali se ne mogu kombinovati s IP izuzećima. Ograničenja hostova primjenjuju se prije izuzeća; ukupno ograničenje provjera i dalje važi nakon njih. Izuzeti hostovi se izostavljaju i iz provjera servisa i iz opcionog Nmap otkrivanja.

Svako skeniranje obavlja lokalne predprovjere prije ciljanog saobraćaja: ograničenja ciljeva/provjera, pristup odredištima, dostupnost opcionog Nmap izvršnog fajla ili omotača, šemu historije i konfigurisani TLS CA paket. `preflight` ispisuje JSON i ne skenira ciljeve niti kreira bazu historije. Privremeno zapisuje susjednu datoteku radi provjere pristupa odredištu bez izmjene postojećeg sadržaja. Podrazumijevani asyncio mehanizam i dalje ne zahtijeva ni Nmap ni root. Putanje odredišta moraju se razlikovati jedna od druge i od ulazne konfiguracije, uključujući tvrde veze; simboličke veze na odredištu se odbijaju. Neuspjele provjere vraćaju 1; neispravan opseg/konfiguracija vraća 2.

Zapisivanje izvještaja i izvoznih datoteka zahtijeva podršku za `O_NOFOLLOW`. Na platformama bez nje, uključujući Windows, ovakvi zapisi ne uspijevaju bez otvaranja ili skraćivanja odredišta. Novi izvještaji i skripte za izvoz kreiraju se samo za vlasnika (režim 0600); zamjena postojeće datoteke čuva njene dozvole. Zapisivanje u imenovanu cijev bez čitača odmah ne uspijeva umjesto da čeka. Nova baza `--history` također se kreira samo za vlasnika; postojeća zadržava svoj režim. Zapisnici uvijek idu na stderr, pa stdout nosi samo rezultate. Izvozi koji sadrže akreditive uvijek forsiraju režim 0600.

Historija je opciona i dopunjuje postojeće JSON snimke i komandu `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Koristite ID-ove iz komande `history`; primjer pretpostavlja novu bazu podataka. Snimci se pohranjuju transakcijski s UTC vremenima početka/završetka, verzijom paketa, efektivnim postavkama bez tajni, sažecima i svim opažanjima hostova/servisa, uključujući greške po hostu. Nepotpuna opažanja hostova se zadržavaju. Otkazana pokretanja se ne čuvaju. Postojeći ugovori za izvještaje, snimke, izvoz i izlazne kodove skeniranja ostaju očuvani.

`history` ispisuje JSON sažetke bez čitanja svih historijskih podataka o uređajima. `compare` čita dva sačuvana skeniranja, zahtijeva identične ciljeve i odabrane portove te izvještava o promjenama odziva, statusa i stanja portova. ID ranijeg skeniranja mora prethoditi kasnijem ID-u. Kada oba skeniranja imaju zabilježen `timeout` ili `backend` i te se vrijednosti razlikuju, izvještaj navodi upozorenje ali ipak poredi zapažanja. Drugačije vrijeme čekanja može učiniti da filtrirani port izgleda otvoren. Greške skenera i nepoznata stanja portova označavaju se kao nesigurna umjesto da se tretiraju kao potvrđen nestanak ili zatvaranje: hostovi s greškama pojavljuju se u `uncertain_hosts`, a svaki prijelaz porta koji uključuje `unknown` (uključujući unknown u oba skeniranja) navodi se u `unconfirmed_ports` umjesto u `port_changes`, osim porta koji je otvoren u kasnijem skeniranju, što predstavlja promjenu porta. `compare` i `diff` klasifikuju portove po istom pravilu. `no_longer_responding` znači izostanak odgovora, a ne dokaz uklanjanja uređaja. Izlazni kod 0 pri skeniranju ne garantuje da je svaki host odgovorio: provjerite greške po hostu. Uspješno poređenje vraća 0 bez obzira ima li promjena; postojeća datotečna komanda `diff` zadržava svoj ugovor izlaznog koda 3. Nepodržana ili oštećena historija vraća 1.

Historija čuva podatke o inventaru, pa odaberite odgovarajuće zaštićen lokalni direktorij. Datoteke profila i pohranjene postavke ne sadrže SNMP akreditive; rukovanje akreditivima ostaje putem postojećih opcija pri pokretanju i okruženja.

## Poređenje inventara

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Snimak je JSON sa `format: "hostcensus-snapshot"`, `version: 1`, verzijom hostcensuse, UTC vremenom nastanka, ciljem, `timeout` i `backend` postavkama skeniranja kada ih je skeniranje zabilježilo, provjerenim servisima i aktivnim hostovima u istom obliku kao `-o` izvještaj. Nedostupni hostovi se izostavljaju. `diff` također prihvata obične JSON izvještaje iz `scan -o`, uključujući one nastale prije postojanja polja `services`.

`diff` prijavljuje nove i nestale hostove, portove koji su se otvorili ili zatvorili na hostovima prisutnim u oba snimka te servise čija se `version` promijenila. Portovi provjereni samo u jednom od dva skeniranja se ne porede, uz odgovarajuće upozorenje. Neuspjela opažanja nikada se ne tumače kao "bez promjena": port sa stanjem `unknown` u bilo kojem skeniranju koji nije otvoren u kasnijem navodi se pod `unconfirmed`, a ne pod `closed`, sa `before` vrijednošću `open`, `unknown` ili `not-open` (provjeren i zatvoren ili filtriran) te `after` vrijednošću `unknown` ili `not-open`; port koji je sada otvoren prijavljuje se pod `opened` čak i ako je ranija provjera pala. Host čije su sve provjere pale bez odgovora u bilo kojem skeniranju navodi se pod `unsettled_hosts` (sa `before`/`after` vrijednošću `up`, `uncertain` ili `absent`, uključujući slučaj kada je pao u oba skeniranja ili nedostaje u drugoj datoteci) umjesto pod `vanished_hosts`; ako odgovori u kasnijem skeniranju, prijavljuje se i kao novi host sa svojim otvorenim portovima. Snimci zadržavaju takve neuspjele hostove upravo iz tog razloga. Upozorenje se također prikazuje kada se ciljevi razlikuju te kada obje datoteke bilježe timeout ili backend i te se vrijednosti razlikuju. `-o PATH` također zapisuje JSON oblik u datoteku.

Izvještaj iz skeniranja zaustavljenog putem `--deadline` (`"complete": false`) navodi samo hostove do kojih je skeniranje stiglo, pa ga `diff` i `export` odbijaju s izlaznim kodom 2. `--allow-partial` ga prihvata uz upozorenje na stderr: `diff` tada hostove koje nepotpuno skeniranje uopće nije navelo stavlja u `unsettled_hosts` kao `unscanned` umjesto kao nestale (host naveden kao nedostupan i dalje je nestali), postavlja `partial` na true i nikada ne prijavljuje odsustvo promjena, dok `export` upisuje upozorenje u zaglavlje skripte.

Izlazni kodovi za `diff`: `0` nema promjena, `3` pronađene promjene, zapažanja koja se nisu mogla potvrditi ili nepotpun ulaz (`changed` je true kad god je bilo koja lista, uključujući `unsettled_hosts` i `unconfirmed`, neprazna ili je `partial` true), `2` datoteka nedostaje, nečitljiva je, nije podržan snimak ili je nepotpuna bez `--allow-partial`, `1` datoteka `-o` se nije mogla zapisati.

## Izvoz za Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (fork sistema Cacti 1.2.31) nema masovni uvoz uređaja iz datoteke. Njegov podržani način dodavanja uređaja iz skripte jeste `cli/add_device.php`, jedan uređaj po pozivu, s argumentima `--option=value`. `hostcensus export` zapisuje POSIX `sh` skriptu takvih poziva:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Svaki aktivni host postaje `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hostovi kod kojih je SNMP upit tokom skeniranja uspio dobijaju `--version=2 --community=...` ili `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` za authPriv), `--port` i `--avail=snmp`. SNMPv3 izvoz zahtijeva `--snmp-user`, a noAuthNoPriv se odbija jer `add_device.php` zahtijeva v3 lozinku.
- Ostali hostovi dobijaju `--version=0 --avail=ping`, sa `--ping_method=tcp --ping_port=` postavljenim na prvi otvoreni TCP port, ili ICMP ako nema nijednog.
- `--notes` navodi otvorene servise i verzije. `--description` je obrnuti DNS naziv kada je jednostavan (slova, cifre, `.`, `_`, `-`), inače IP adresa, i čini se jedinstvenim jer `add_device.php` postojeći opis tretira kao ažuriranje tog uređaja.

Svaka vrijednost se validira i citira za ljusku pomoću `shlex.quote`. Podrazumijevano se ne zapisuje nijedna SNMP tajna: skripta pri izvršavanju proširuje `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ili `HOSTCENSUS_SNMP_PRIV_KEY` i staje ako neka nije postavljena. `--include-credentials` umjesto toga upisuje vrijednosti tih varijabli okruženja u skriptu, kreira je s režimom 0600 i bilježi upozorenje. Sam `add_device.php` ispisuje community i prima tajne kao argumente, koji su vidljivi u listi procesa Kadupul servera dok se svaki poziv izvršava.

`add_device.php` izlazi s kodom 1 za duplikate i greške; skripta nastavlja, broji neuspjehe i izlazi s kodom 1 ako bilo koji uređaj nije dodat. ID-ovi šablona dobijaju se putem `php cli/add_device.php --list-host-templates`. Izlazni kodovi za `export`: `0` zapisano, `2` nečitljiv ulaz, nepotpuno skeniranje bez `--allow-partial` ili podaci koji se ne mogu sigurno izvesti, `1` skripta se nije mogla zapisati.

## Verzionisanje i proces objavljivanja

hostcensus prati [Semantičko verzionisanje](https://semver.org/spec/v2.0.0.html): kompatibilne ispravke povećavaju patch verziju, kompatibilne mogućnosti i oznake zastarjelosti povećavaju minor verziju, a nekompatibilne promjene povećavaju major verziju. Komande i opcije, izlazni kodovi i JSON šeme predstavljaju javni ugovor; zastarjelo ponašanje nastavlja raditi do narednog velikog izdanja, osim ako sigurnosna ispravka ne zahtijeva raniju izmjenu (tada dnevnik promjena objašnjava razlog).

release-please otvara PR za izdanje iz naslova Conventional Commit poruka na grani `main`, ažurirajući `pyproject.toml`, `uv.lock` i `CHANGES.md`. Spajanje tog PR-a kreira oznaku `vMAJOR.MINOR.PATCH` i nacrt GitHub izdanja na koji CI prilaže testirani wheel, izvornu distribuciju i kontrolne sume; GitHub pohranjuje atestacije izgradnje za te datoteke putem svog API-ja za atestacije. Održavatelj pregleda i objavljuje nacrt nakon prilaganja datoteka. Izdanja se nikada ne zamjenjuju.

Pouzdano objavljivanje na PyPI je opciono i zahtijeva vlasništvo nad projektom, pouzdanog izdavača i okruženje `pypi`. Objavljuje iste provjerene artefakte izdanja bez ponovne izgradnje i bez čuvanja API tokena. Označena izdanja u ovom javnom repozitoriju generišu GitHub atestacije artefakata; privatni forkovi zahtijevaju podržan plan i eksplicitno uključivanje. Pogledajte [potpuni vodič za izdanja](../../../docs/releasing.md) za podešavanje, tačne komande i ponovne pokušaje.

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

Razvojni alati nalaze se u [PEP 735](https://peps.python.org/pep-0735/) grupama zavisnosti u datoteci `pyproject.toml` (`dev`, `fuzz`, `build`), pa se nikada ne pojavljuju u objavljenim metapodacima paketa. `uv.lock` je jedina lock datoteka; CI instalira komandom `uv sync --locked` i pada kada je lock datoteka zastarjela. Odaberite interpreter putem `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) ili bilo kojeg Pythona 3.12+.

CI nameće prag pokrivenosti paketa testovima od 90%. Jedinični testovi uključuju kontrolisane loopback servere te vanmrežne slučajeve za profile, historiju i validaciju izdanja; Compose laboratorija pokreće OpenSSH, MariaDB, nginx i net-snmp na izolovanom mostu. Pokrenite je komandom `make test-integration`. Pogledajte [CONTRIBUTING.md](../../../CONTRIBUTING.md) i [alate za izdanja](../../../scripts/README.md).

Kontejner za izvršavanje radi pod UID/GID 10001 bez kućnog direktorija, bez prijave u ljusku i bez pip alata, a može pisati u `/app/output`. Dajte tom korisniku pravo pisanja u svaki montirani izlazni direktorij. Ne zahtijeva nikakve dodatne sposobnosti i radi s korijenskim datotečnim sistemom samo za čitanje, pa se može pokrenuti ovako:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap u ovom kontejneru koristi svoje neprivilegovano TCP otkrivanje. CI ruši izgradnju slike ako Trivy prijavi bilo koju popravljivu ranjivost nivoa HIGH ili CRITICAL.

## Provjere lanca snabdijevanja

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) izvršava se na grani main i sedmično, objavljuje svoj stvarni rezultat i učitava nalaze u GitHub skeniranje koda. Akcije i osnovne slike kontejnera fiksirane su nepromjenjivim heševima; Python zavisnosti razriješene su u `uv.lock`. Greške alata Bandit ruše CI, a ograničeni Atheris fuzzing ispituje SSH, MySQL, HTTP, certifikat i SNMPv3 BER parsere bez mrežnog pristupa.

Scorecard također mjeri historijsku aktivnost pregleda, raznolikost saradnika i porijeklo izdanja. Ti rezultati odražavaju stvarne dokaze; oni nisu tvrdnja da je svaka provjera upravljanja ili historijskih izdanja ispunjena. Pogledajte [SECURITY.md](../../../SECURITY.md) i [porijeklo izdanja](../../../docs/releasing.md).

## Lokalizacija

CLI poruke i terminalske tabele sažetka i poređenja podržavaju 48 lokaliteta (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`, `bs`, `hr`, `sr`) bez ikakvih dodatnih zavisnosti pri izvršavanju. Određivanje poštuje `--lang`, zatim `LC_ALL`, `LC_MESSAGES` i `LANG`, uz povratak na `en`. JSON šeme, CSV kolone i izvozne skripte ostaju nepromijenjene u svim lokalitetima.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Doprinos

Doprinosi trebaju uključivati ponovljiv primjer, čuvati dokumentovane ugovore za CLI i formate podataka te proći gore navedene provjere kvaliteta. Pogledajte [CONTRIBUTING.md](../../../CONTRIBUTING.md) za razvojni tok rada i [vodič za izdanja](../../../docs/releasing.md) za odluke o kompatibilnosti i verzionisanju.

## Sigurnost i status licence

Pogledajte [SECURITY.md](../../../SECURITY.md) za privatno prijavljivanje ranjivosti i podržane verzije. hostcensus je licenciran pod [MIT licencom](../../../LICENSE).

Zaglavlja izvornih datoteka koriste SPDX identifikatore i čuvaju zasluge saradnika iz Git historije. Pogledajte [AUTHORS.md](../../../AUTHORS.md) za pripisivanje zasluga. Binarni testni snimci i generisana lock datoteka koriste susjedne `.license` datoteke; tekst MIT licence nalazi se u `LICENSES/MIT.txt`.
