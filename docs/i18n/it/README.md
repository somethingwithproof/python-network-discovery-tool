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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · **Italiano** · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus è una CLI Python per l'inventario ripetibile dei servizi sulle reti che amministri.
Registra ciò che i dispositivi espongono, confronta le osservazioni nel tempo e genera
script di importazione per Kadupul. Il backend predefinito utilizza socket asyncio senza privilegi di root;
il rilevamento opzionale con Nmap può identificare host oltre le porte di servizio configurate.

## Perché hostcensus

Un report occasionale sulle porte non chiarisce se l'osservazione successiva sia cambiata o
semplicemente fallita. hostcensus combina stati espliciti dei servizi, probe limitati, profili di
scansione riutilizzabili e cronologia locale. Gli operatori possono ripetere lo stesso ambito, ispezionare
gli errori e distinguere le osservazioni incerte dalle modifiche confermate.

- **Evidenze dei servizi:** identificazione SSH, greeting MySQL, header HTTP, osservazioni sui
  certificati TLS e rilevamento SNMP o query system-MIB con credenziali.
- **Ambito ripetibile:** profili TOML con nome, esclusioni additive, servizi configurabili,
  limiti su host/probe e worker limitati.
- **Controlli prima del traffico:** il preflight locale convalida target, strumenti, accesso alle
  destinazioni, schema della cronologia e bundle CA TLS configurati.
- **Cronologia dell'inventario:** gli snapshot SQLite transazionali conservano tutte le osservazioni;
  i confronti mantengono visibili gli errori dello scanner e gli stati sconosciuti.
- **Output interoperabile:** report da terminale, JSON e CSV, snapshot su file versionati
  e script di importazione Kadupul.

La CI copre Python 3.12, 3.13 e 3.14 su Linux e macOS, oltre a un laboratorio di integrazione
Compose controllato. Il codice utilizza alias di tipo moderni, risultati di preflight tipizzati,
profili con slot solo keyword-only e pulizia asincrona strutturata mantenendo il supporto a tali
versioni di runtime. Consulta [Versioning e rilasci](../../../docs/releasing.md) per il contratto di
compatibilità SemVer e il processo di rilascio su GitHub. Il badge del rilascio descrive
gli artefatti pubblicati, non il checkout: il tag pubblicato più recente è attualmente
`v0.3.0`, mentre questo checkout usa la versione del pacchetto `3.0.0`. Installa dal checkout
per utilizzare le funzionalità di inventario documentate qui.

Inizia con [l'installazione](#install), poi passa a [profili e cronologia](#inventory-profiles-preflight-and-local-history).
Per i dettagli di integrazione, consulta [fingerprint dei servizi](#fingerprints),
[confronti tra file](#inventory-diff) ed [esportazione Kadupul](#kadupul-export).

## Installazione

È richiesto Python 3.12 o successivo; Python 3.12-3.14 è la matrice testata. Da questo
checkout, installa le dipendenze runtime bloccate:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Per il rilevamento opzionale degli host con Nmap, installa l'eseguibile Nmap tramite il gestore di
pacchetti della tua piattaforma; non è necessario alcun pacchetto Python aggiuntivo. L'output XML di Nmap viene analizzato con
defusedxml, una dipendenza principale, quindi l'espansione delle entità viene rifiutata. hostcensus esegue
direttamente il comando `nmap` trovato in `PATH` con un elenco fisso di argomenti, una scadenza che cresce
con la dimensione del prefisso e un limite di output di 64 MiB. Nmap non è necessario per il backend predefinito.

## Migrazione da netprobe

hostcensus è il nuovo nome di netprobe, rilasciato nella versione 3.0.0. Il progetto non è mai stato
pubblicato su PyPI con nessuno dei due nomi, quindi le installazioni provenivano da un checkout o da una release
GitHub. Il repository GitHub mantiene il proprio nome.

| Prima | Ora | Compatibilità |
| --- | --- | --- |
| Distribuzione `netprobe` | `hostcensus` | Reinstalla dal checkout; non esiste un pacchetto con il vecchio nome. |
| Comando `netprobe` | `hostcensus` | `netprobe` viene comunque eseguito e stampa una riga di deprecazione su stderr. Codici di uscita e stdout restano invariati. Verrà rimosso nella prossima major release. |
| Variabili d'ambiente `NETPROBE_*` | `HOSTCENSUS_*` | Una variabile `NETPROBE_*` viene utilizzata quando la corrispondente `HOSTCENSUS_*` non è impostata, con un avviso su stderr che indica i nomi delle variabili e mai i loro valori. `HOSTCENSUS_*` prevale quando sono entrambe impostate. Verrà rimosso nella prossima major release. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Modifica incompatibile.** Non viene installato alcuno shim di importazione; aggiorna gli import. |
| Tag dell'immagine Docker `network-discovery:test` (solo CI) e utente del container `netprobe` | `hostcensus:test`, utente `hostcensus` | Nessuna immagine è mai stata pubblicata su un registry. Ricompila l'immagine e usa l'entrypoint `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Un file esistente con il vecchio nome predefinito viene ancora usato, con un avviso, finché il nuovo nome non esiste. I percorsi espliciti `--config` e `--history` non vengono modificati. |
| Report e snapshot con `"format": "netprobe-report"` o `"netprobe-snapshot"` e il campo `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` ed `export` caricano comunque i file scritti con il vecchio nome e gli schemi JSON pubblicati accettano entrambe le forme. I nuovi file usano i nuovi nomi. I database di cronologia SQLite restano invariati e si caricano come prima. |
| Script Kadupul da `netprobe export` | Script da `hostcensus export` | I vecchi script continuano a funzionare e leggono ancora `NETPROBE_SNMP_*` durante l'esecuzione. I nuovi script leggono `HOSTCENSUS_SNMP_*`. |

## Esempio rapido

Eseguito dal container tester del laboratorio di integrazione descritto in Sviluppo; output ridotto:

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

## Codici di uscita

| Comando | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | osservazioni/report registrati | preflight/backend, cronologia o scrittura di report/snapshot non riusciti | target, opzioni, configurazione o limiti non validi | - | `--deadline` raggiunta; report parziale scritto, cronologia e snapshot saltati |
| `preflight` | controlli superati | controllo locale non riuscito | target/configurazione non validi o destinazioni in conflitto | - | - |
| `profiles` | profili convalidati elencati | - | configurazione o selezione illeggibile/non valida | - | - |
| `history` | riepiloghi elencati | cronologia mancante, non valida o non supportata | opzioni CLI non valide | - | - |
| `compare` | confronto prodotto, anche in presenza di modifiche | cronologia illeggibile, ambito/ordine incompatibile o errore di scrittura | opzioni CLI non valide | - | - |
| `diff` | nessuna modifica | impossibile scrivere il file `-o` | input mancante, illeggibile o non supportato, oppure scansione incompleta senza `--allow-partial` | modifiche rilevate, osservazioni non confermate o scansione incompleta | - |
| `export` | script scritto | impossibile scrivere lo script | input illeggibile, scansione incompleta senza `--allow-partial` o dati non esportabili in sicurezza | - | - |

## Struttura

| Modulo | Responsabilità |
| --- | --- |
| `cli.py` | Opzioni dei comandi, risoluzione dei profili, preflight, scansione e reportistica |
| `scanner.py`, `probes.py` | Espansione dei target, worker limitati, rilevamento host e osservazioni dei servizi |
| `config.py`, `profiles.py` | Definizioni dei servizi e profili di inventario convalidati |
| `models.py`, `output.py` | Tipi di risultato e rendering su terminale/JSON/CSV |
| `history.py`, `diff.py` | Cronologia SQLite e confronti tra snapshot su file versionati |
| `preflight.py` | Controlli locali e ricerca limitata della versione di Nmap |
| `export.py` | Script di importazione Kadupul convalidati e con quoting sicuro |

Ogni osservazione di servizio registra il proprio stato separatamente dall'identità annunciata.
Letture e scadenze sono limitate; le eccezioni dei probe rimangono negli errori dell'host. La cronologia SQLite
utilizza transazioni, pulizia esplicita delle connessioni e percorsi di lettura e confronto in sola lettura.
I segreti SNMP entrano solo tramite variabili d'ambiente o file di segreti;
la cronologia dell'inventario memorizza le impostazioni effettive non segrete. Consulta
[Architettura](../../../docs/architecture.md) per la pipeline di scansione, i suoi limiti e i confini di
fiducia, e [SECURITY.md](../../../SECURITY.md#authorized-use) per l'uso autorizzato.


## Utilizzo

Scansiona solo le reti che amministri.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opzione | Significato |
| --- | --- |
| `NETWORK` | CIDR, IP o hostname; opzionale con `--profile`. Gli identificatori di ambito IPv6 vengono rifiutati. |
| `-o, --output PATH` | Scrive un report. Il formato segue l'estensione (`.json`, `.csv`); altre estensioni ricadono su JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Forza il formato del report. Non ha effetto senza `--output`. `.sh` seleziona `kadupul`. |
| `-v, --verbose` | Logging di debug. |
| `-q, --quiet` | Sopprime risultati, avanzamento e log informativi; avvisi ed errori continuano a comparire su stderr. |
| `--backend asyncio\|nmap` | Rilevamento host. `asyncio` (predefinito) sonda direttamente le porte di servizio; `nmap` esegue prima un ping sweep nmap e richiede l'eseguibile `nmap` in `PATH`. |
| `--timeout SECONDS` | Attesa per i probe che non impostano un proprio budget (predefinito 1.0). I probe di connessione integrati usano 0.3s a meno che la tabella dei servizi non imposti `timeout`. |
| `--concurrency N` | Probe contemporanei in corso (predefinito 256). |
| `--deadline SECONDS` | Interrompe l'intera scansione, incluso lo sweep nmap, dopo questo intervallo (predefinito 3600, massimo 604800; env `HOSTCENSUS_DEADLINE`). Gli host completati vengono scritti nel report con `"complete": false`, non vengono scritti cronologia né snapshot e `scan` esce con 4. |
| `--config PATH` | Definizioni TOML dei servizi e impostazioni opzionali `[profiles]` con nome. |
| `--profile NAME` | Usa un profilo con nome; usa `hostcensus.toml` per impostazione predefinita quando `--config` è omesso. |
| `--exclude IP/CIDR` | Aggiunge un'esclusione; ripetere secondo necessità. Un host IPv4 escluso esclude anche gli indirizzi IPv6 che lo raggiungono: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) e 6to4. Target ed esclusioni IPv4-mapped sono trattati come gli indirizzi IPv4 che rappresentano. |
| `--max-hosts N` | Limite di indirizzi verificato prima delle esclusioni (predefinito/massimo rigido 65.536). |
| `--history PATH` | Registra la scansione completata in un database di cronologia SQLite opt-in. |
| `--services NAMES` | Elenco separato da virgole di nomi di servizi da verificare, in quell'ordine (predefinito: tutti). |
| `--ports SPEC` | Elenco separato da virgole di `NAME=PORT` (sposta un servizio) o `PORT` (aggiunge un controllo TCP semplice chiamato `tcp-PORT`). |
| `--snmp-community-file PATH` | File contenente la community SNMPv2c per la query system MIB. Env: `HOSTCENSUS_SNMP_COMMUNITY` (il valore) o `HOSTCENSUS_SNMP_COMMUNITY_FILE` (il percorso). |
| `--snmp-user` | Utente SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (predefinito), `SHA224`, `SHA256`, `SHA384`, `SHA512` e un file contenente la passphrase. Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` o `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (predefinito), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` e un file contenente la passphrase. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` o `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Scrive anche uno snapshot versionato per `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifica i certificati HTTPS rispetto a questo bundle PEM anziché allo store di sistema. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Per impostazione predefinita ogni host viene verificato per SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) e HTTPS (TCP 443). Le porte TCP vengono testate con una connessione completa. SNMP viene testato con una richiesta di engine discovery SNMPv3, a cui qualsiasi agente SNMPv3 deve rispondere senza credenziali; gli agenti che parlano solo v1/v2c non vengono rilevati da questo probe. Con il backend asyncio un host è considerato attivo quando qualsiasi probe ottiene una risposta, inclusa una connessione rifiutata, quindi un host che scarta ogni probe ha `alive=false` e l'errore "Host is down"; ciò non dimostra che sia fisicamente spento. Con `--backend nmap`, è nmap a decidere quali host sono attivi (ICMP da root, altrimenti TCP 80/443).

### Fingerprint

Ogni servizio aperto viene identificato tramite fingerprint da ciò che invia prima di qualsiasi login. Nulla esegue l'autenticazione tranne la query SNMP, e solo quando fornisci le credenziali.

| Probe | Cosa legge | `version` | Chiavi di `details` |
| --- | --- | --- | --- |
| `ssh` | Riga di identificazione RFC 4253 | software, ad es. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Handshake iniziale MySQL/MariaDB | versione server | `server_version`, `flavor`, `auth_plugin`, oppure `error_code`/`error` |
| `http` | Risposta `HEAD /` | header `Server` | `status`, `server` |
| `https` | Handshake TLS, certificato, `HEAD /` | header `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Rilevamento SNMPv3; con credenziali, GET di sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; con credenziali `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, oppure `snmp_error` |

Un target hostname viene risolto una sola volta per host e ogni probe si connette a quell'indirizzo, registrato come `address` nei risultati; il nome viene usato solo per TLS SNI, la verifica del certificato e l'header HTTP `Host`. Un nome che non si risolve produce stati `unknown` e un errore `Cannot resolve`. I nomi DNS inversi vengono conservati solo quando contengono caratteri validi per hostname e vengono eseguite al massimo 16 ricerche contemporaneamente. HTTPS utilizza la verifica del certificato e dell'hostname rispetto allo store di sistema o a `--tls-ca-file`. Il trust store viene caricato una volta per la scansione e riutilizzato per ogni probe HTTPS. La connessione TCP e l'handshake TLS sono temporizzati separatamente, quindi una porta che accetta connessioni ma blocca l'handshake risulta `open` con `tls_error`, non `filtered`. Se la verifica fallisce, il risultato registra `cert_verified: false` e `cert_verify_error`; non riprova con impostazioni più deboli né invia una richiesta HTTP. I dettagli del certificato e gli header HTTP vengono raccolti solo dopo il successo della verifica. Fornisci il bundle CA corretto per i servizi con CA privata. I report più vecchi possono contenere `cert_read_unverified`, che i probe attuali non producono più.

I segreti SNMP vengono letti solo da variabili d'ambiente o da file (`--snmp-*-file`, o la corrispondente variabile `HOSTCENSUS_SNMP_*_FILE`), mai da valori sulla riga di comando, che altri utenti locali possono vedere nell'elenco dei processi. `--snmp-community`, `--snmp-auth-key` e `--snmp-priv-key` con un valore escono con codice 2 e indicano il parametro sostitutivo. Un file di segreti deve contenere testo UTF-8 non vuoto di al massimo 4096 byte; un eventuale newline finale viene ignorato e impostare sia una variabile sia un file per lo stesso segreto genera un errore. Gli errori indicano il file ma non ne stampano mai il contenuto. I report di scansione e la cronologia non includono intenzionalmente valori di credenziali. L'esportatore dispone di un'opzione separata ed esplicita `--include-credentials` descritta di seguito. Una community seleziona SNMPv2c; un utente seleziona SNMPv3, con autenticazione quando è fornita una chiave di autenticazione e privacy quando sono fornite entrambe le chiavi (`snmp_security_level` registra quale livello è usato). hostcensus rifiuta, con codice di uscita 2, di combinare una community con un utente v3, di usare una chiave di privacy senza una chiave di autenticazione o di usare chiavi senza un utente, e non riprova mai una query v3 fallita con v2c o con un livello di sicurezza inferiore. Gli agenti che parlano solo v1/v2c ignorano il rilevamento v3 senza credenziali, quindi risultano aperti solo quando viene fornita una community.

Il testo del banner viene ridotto ai caratteri stampabili e limitato a 256 caratteri prima di essere memorizzato o mostrato. Anche le letture sono limitate: 4 KiB per riga, 4 KiB per un greeting MySQL, 16 KiB di header HTTP. Un engine ID SNMP più lungo di 32 ottetti viene troncato prima della memorizzazione. HTTP e HTTPS inviano un header Host con l'indirizzo IPv6 tra parentesi quadre e con la porta quando è diversa da 80 o 443. Le celle CSV che iniziano con un carattere di attivazione di formule per fogli di calcolo ricevono un prefisso in modo che la cella resti testo.

### Limiti

Una singola esecuzione accetta al massimo 65.536 indirizzi, 64 servizi e 524.288 probe (host per servizi); richieste più grandi escono con codice 2 prima di inviare qualsiasi dato. `--concurrency` è limitato a 4096 socket. Ogni probe ha una scadenza rigida pari a quattro volte il proprio budget. I probe di connessione (`tcp`, `ssh`, `mysql`, `http`) usano 0.3 secondi a meno che quel servizio non imposti `timeout`. SNMP e HTTPS usano `--timeout` (predefinito 1.0) quando non ne impostano uno proprio. Un probe che raggiunge la scadenza viene segnalato come `unknown` con "probe timed out" in `errors`. Anche gli errori locali dei socket (ad esempio l'esaurimento dei descrittori di file) risultano `unknown` con l'errore registrato; non contano mai come porta filtrata o host irraggiungibile. Prima del probing, hostcensus alza il limite soft dei file aperti verso il limite hard per contenere `--concurrency` più 64 descrittori; quando non ci riesce, il controllo di preflight `open files` fallisce e `scan` esce con 1 prima di inviare traffico. Il rilevamento Nmap usa un timeout per host di 30 secondi. Un prefisso viene passato a nmap in forma CIDR e uno sweep fallisce con uscita 1 quando nmap riporta meno indirizzi di quanti ne ha ricevuti (ad esempio un nome che non riesce a risolvere) anziché contrassegnare gli host come inattivi. Un target hostname viene risolto una volta sola e a nmap viene passato quell'indirizzo, così rilevamento e probe raggiungono la stessa macchina. Un prefisso completo è un singolo processo nmap la cui scadenza di sottoprocesso è di 35 secondi ogni 256 indirizzi, arrotondata per eccesso. Gli sweep con esclusioni usano batch da 256 host e una scadenza di 35 secondi per ogni batch. La creazione dei worker è limitata indipendentemente dalla dimensione dell'intervallo. DNS inverso e risoluzione hostname hanno una scadenza separata di due secondi; una chiamata al resolver che non ritorna mai viene abbandonata sul proprio thread, così non può tenere hostcensus in esecuzione oltre questi limiti. Al massimo 16 ricerche girano contemporaneamente e una chiamata abbandonata mantiene il proprio slot finché non termina, mantenendo limitato il numero di thread bloccati; se tutte e 16 si bloccano, le ricerche successive restano in coda per uno slot al di fuori della scadenza di due secondi (che parte una volta liberato uno slot) finché `--deadline` non arresta la scansione. `NetworkScanner` usato come libreria senza una `deadline` può attendere tale slot indefinitamente. `--deadline` (predefinito un'ora) limita l'intera esecuzione oltre a questi limiti.

### Configurazione dei servizi

I servizi possono essere modificati con un file TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` è uno tra `tcp`, `ssh`, `mysql`, `http`, `https` o `snmp` e assume come valore predefinito il nome del servizio quando corrisponde a un probe, altrimenti `tcp`. Solo `snmp` usa UDP. I nomi dei servizi sono composti da lettere minuscole, cifre, `-` e `_`. Due servizi non possono condividere porta e protocollo; la cronologia registra un solo stato per quella coppia. `timeout` è opzionale, in secondi, e pari ad almeno 0.05. I probe di tipo connessione (`tcp`, `ssh`, `mysql`, `http`) usano 0.3 secondi per impostazione predefinita. `snmp` e `https` usano il `--timeout` della scansione quando il servizio non imposta `timeout`. `--timeout` non sostituisce un budget che il servizio possiede già.

I report JSON sono documenti versionati (`"format": "hostcensus-report"`, `"version": 1`) che registrano il target, i servizi sondati e le impostazioni accanto a `devices`; `--format json` senza `-o` scrive il report su stdout invece della tabella. Ogni output JSON ha uno schema pubblicato; consulta [Output JSON](../../../docs/json-output.md). I dispositivi mantengono i campi originali `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` ed `errors` e aggiungono un elenco `services` con `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` oppure `unknown` quando il probe è fallito localmente o ha raggiunto la scadenza), `version` e `details` di ciascun probe. L'output CSV aggiunge le colonne finali `services` e `versions` per quelli aperti. I booleani `ssh`, `snmp` e `mysql` seguono i servizi con esattamente quei nomi.


## Profili di inventario, preflight e cronologia locale

I profili con nome condividono un file TOML con le definizioni `[services]` esistenti. Copia
[hostcensus.example.toml](../../../hostcensus.example.toml) in `hostcensus.toml` e imposta le reti
che amministri:

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

`preflight` risolve opzioni e profili esattamente come fa `scan`, incluso
`--concurrency` per il controllo dei file aperti, quindi un preflight superato significa che `scan`
partirà con lo stesso piano.

I profili accettano `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` e `max_hosts`. `services` e `ports` usano la sintassi esistente con elenco
separato da virgole. Le opzioni CLI esplicite sovrascrivono le impostazioni del profilo; opzioni `--exclude`
ripetute si aggiungono alle esclusioni del profilo. Una rete esplicita con `--profile` deve essere
contenuta nell'ambito IP/CIDR di quel profilo. Gli hostname restano supportati per le scansioni
dirette, ma non possono essere combinati con esclusioni IP. I limiti sugli host si applicano prima delle
esclusioni; il limite totale dei probe continua ad applicarsi in seguito. Gli host esclusi vengono
omessi sia dai controlli dei servizi sia dal rilevamento opzionale con Nmap.

Ogni scansione esegue controlli locali di preflight prima del traffico verso i target:
limiti su target/probe, accesso alla destinazione, disponibilità dell'eseguibile/wrapper Nmap opzionale,
schema della cronologia e un bundle CA TLS configurato. `preflight` produce un report JSON e non scansiona
target né crea un database di cronologia. Scrive temporaneamente un file adiacente per verificare
l'accesso alla destinazione senza modificare i contenuti esistenti. Il backend asyncio predefinito
continua a non richiedere né Nmap né privilegi di root. I percorsi di destinazione devono essere distinti tra
loro e dalla configurazione di input, inclusi gli hard link; i symlink di destinazione vengono
rifiutati. I controlli non riusciti restituiscono 1; ambito o configurazione non validi restituiscono 2.

Le scritture di report ed esportazioni richiedono il supporto `O_NOFOLLOW`. Sulle piattaforme che ne sono prive,
incluso Windows, queste scritture falliscono senza aprire né troncare la destinazione.
I nuovi report e script di esportazione sono accessibili solo al proprietario (modalità 0600); la sostituzione di un file esistente ne preserva i
permessi. La scrittura su una named pipe senza lettori fallisce immediatamente invece di restare in attesa. Anche un nuovo database `--history` viene creato accessibile solo al proprietario; uno esistente mantiene la propria modalità. I messaggi di log vanno sempre su stderr, così stdout trasporta solo i risultati. Le esportazioni che contengono credenziali forzano sempre la modalità 0600.

La cronologia è opt-in e integra gli snapshot JSON esistenti e il comando `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Usa gli ID ricavati da `history`; l'esempio presuppone un nuovo database. Gli snapshot vengono memorizzati
in modo transazionale con orari UTC di inizio/fine, versione del pacchetto, impostazioni effettive non
segrete, riepiloghi e tutte le osservazioni di host/servizi, inclusi gli errori per host.
Le osservazioni incomplete degli host vengono conservate. Le esecuzioni annullate non vengono salvate. I contratti esistenti sui
codici di uscita di report, snapshot, export e scan vengono preservati.

`history` elenca i riepiloghi JSON senza leggere tutti i payload storici dei dispositivi.
`compare` legge due scansioni salvate, richiede identità dei target e porte selezionate
identiche e segnala le modifiche di reattività, stato e stato delle porte. L'ID di scansione precedente
deve precedere l'ID successivo. Quando entrambe le scansioni hanno registrato `timeout` o `backend`
e tali valori differiscono, il report include un avviso ed esegue comunque il confronto delle
osservazioni. Un'attesa diversa può far sembrare aperta una porta filtrata. Gli errori dello scanner
e le osservazioni di porte sconosciute vengono segnalati come incerti anziché essere trattati come
sparizione o chiusura confermata: gli host con errori compaiono in `uncertain_hosts` e
ogni transizione di porta che coinvolge `unknown` (incluso unknown in entrambe le scansioni) è elencata
in `unconfirmed_ports` invece che in `port_changes`, tranne una porta che risulta aperta nella
scansione successiva, che costituisce una modifica di porta. `compare` e `diff` classificano le porte con la stessa regola.
`no_longer_responding` indica mancanza di risposta, non la prova della rimozione del dispositivo.
Il codice di uscita 0 di `scan` non garantisce che ogni host abbia risposto: ispeziona gli errori per host. Un confronto riuscito restituisce 0 indipendentemente dalla presenza di modifiche; il comando `diff` esistente su file
mantiene il proprio contratto con codice di uscita 3. Una cronologia non supportata o danneggiata restituisce 1.

La cronologia memorizza informazioni di inventario, quindi scegli una directory locale adeguatamente
protetta. I file di profilo e le impostazioni memorizzate non contengono credenziali SNMP;
la gestione delle credenziali prosegue tramite le opzioni runtime e le variabili d'ambiente esistenti.

## Diff dell'inventario

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Uno snapshot è un documento JSON con `format: "hostcensus-snapshot"`, `version: 1`, la versione di hostcensus, l'ora di creazione UTC, il target, `timeout` e `backend` della scansione quando questa li ha registrati, i servizi sondati e gli host attivi nella stessa forma del report `-o`. Gli host inattivi vengono omessi. `diff` accetta anche normali report JSON di `scan -o`, inclusi quelli precedenti all'introduzione del campo `services`.

`diff` segnala i nuovi host e quelli scomparsi, le porte aperte o chiuse sugli host presenti in entrambi e i servizi la cui `version` è cambiata. Le porte sondate in una sola delle due scansioni non vengono confrontate e un avviso lo segnala. Le osservazioni fallite non vengono mai interpretate come "nessuna modifica": una porta che risulta `unknown` in una delle due scansioni e non è aperta nella successiva viene elencata sotto `unconfirmed`, non `closed`, con `before` pari a `open`, `unknown` o `not-open` (sondata e chiusa o filtrata) e `after` pari a `unknown` o `not-open`; una porta che è attualmente aperta viene segnalata sotto `opened` anche se il probe precedente è fallito. Un host i cui probe sono falliti tutti senza risposta in una delle due scansioni è elencato sotto `unsettled_hosts` (con `before`/`after` pari a `up`, `uncertain` o `absent`, incluso quando è fallito in entrambe le scansioni o manca dall'altro file) anziché in `vanished_hosts`; se risponde nella scansione successiva viene anche segnalato come nuovo host con le relative porte aperte. Gli snapshot conservano tali host falliti per questo motivo. Compare un avviso anche quando i target differiscono e quando entrambi i file hanno registrato un timeout o un backend diversi tra loro. `-o PATH` scrive la forma JSON anche in un file.

Un report di una scansione interrotta da `--deadline` (`"complete": false`) elenca solo gli host raggiunti, quindi `diff` ed `export` lo rifiutano con codice di uscita 2. `--allow-partial` lo accetta con un avviso su stderr: `diff` elenca quindi gli host che la scansione incompleta non ha proprio elencato sotto `unsettled_hosts` come `unscanned` anziché scomparsi (un host elencato come inattivo resta comunque scomparso), imposta `partial` su true e non segnala mai nessuna modifica, mentre `export` scrive un avviso nell'intestazione dello script.

Codici di uscita di `diff`: `0` nessuna modifica, `3` modifiche rilevate, osservazioni che non è stato possibile confermare o input incompleto (`changed` è true ogni volta che un qualsiasi elenco, inclusi `unsettled_hosts` e `unconfirmed`, non è vuoto, oppure `partial` è true), `2` file mancante, illeggibile, non uno snapshot supportato o incompleto senza `--allow-partial`, `1` impossibile scrivere il file `-o`.

## Esportazione Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (un fork di Cacti 1.2.31) non ha un'importazione massiva di dispositivi da file. Il suo modo supportato per aggiungere dispositivi da uno script è `cli/add_device.php`, un dispositivo per chiamata, con argomenti `--option=value`. `hostcensus export` scrive uno script POSIX `sh` con queste chiamate:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Ogni host attivo diventa `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Gli host in cui la query SNMP della scansione è riuscita ottengono `--version=2 --community=...` oppure `--version=3 --username=... --authproto=... --password=...` (più `--privproto`/`--privpass` per authPriv), `--port` e `--avail=snmp`. L'esportazione SNMPv3 richiede `--snmp-user`, e noAuthNoPriv viene rifiutato perché `add_device.php` richiede una password v3.
- Gli altri host ottengono `--version=0 --avail=ping`, con `--ping_method=tcp --ping_port=` la prima porta TCP aperta, oppure ICMP se non ve ne sono.
- `--notes` elenca i servizi aperti e le relative versioni. `--description` è il nome DNS inverso quando è semplice (lettere, cifre, `.`, `_`, `-`), altrimenti l'IP, e viene reso univoco, perché `add_device.php` tratta una descrizione esistente come un aggiornamento a quel dispositivo.

Ogni valore viene convalidato e quotato per la shell con `shlex.quote`. Per impostazione predefinita non viene scritto alcun segreto SNMP: lo script espande `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` o `HOSTCENSUS_SNMP_PRIV_KEY` a runtime e si ferma se una di queste variabili non è impostata. `--include-credentials` scrive invece i valori da tali variabili d'ambiente nello script, lo crea con modalità 0600 e registra un avviso. `add_device.php` stesso stampa la community e riceve i segreti come argomenti, che sono visibili nell'elenco dei processi del server Kadupul mentre ciascuna chiamata è in esecuzione.

`add_device.php` esce con 1 per duplicati ed errori; lo script continua, conta i fallimenti ed esce con 1 se un qualsiasi dispositivo non è stato aggiunto. Gli ID dei template provengono da `php cli/add_device.php --list-host-templates`. Codici di uscita di `export`: `0` scritto, `2` input illeggibile, scansione incompleta senza `--allow-partial` o dati che non possono essere esportati in sicurezza, `1` impossibile scrivere lo script.

## Controllo versioni e processo di rilascio

hostcensus segue il [Semantic Versioning](https://semver.org/spec/v2.0.0.html): le correzioni compatibili
incrementano la versione patch, le funzionalità compatibili e le deprecazioni incrementano la
versione minor, mentre le modifiche che rompono la compatibilità incrementano la versione major.
Comandi e opzioni, codici di uscita e gli schemi JSON costituiscono il contratto pubblico;
il comportamento deprecato continua a funzionare fino alla prossima major release, a meno che una
correzione di sicurezza non richieda di modificarlo prima (nel qual caso il changelog ne spiega il motivo).

release-please apre una PR di rilascio dai titoli Conventional Commit su `main`,
aggiornando `pyproject.toml`, `uv.lock` e `CHANGES.md`. Il merge crea il tag
`vMAJOR.MINOR.PATCH` e una bozza di release GitHub, a cui la CI allega un wheel testato,
la distribuzione sorgente e i checksum; GitHub archivia le attestazioni di build per
tali file tramite la propria API delle attestazioni. Un manutentore esamina e pubblica la
bozza una volta allegati i file. I rilasci non vengono mai sostituiti.

Il trusted publishing su PyPI è opt-in e richiede la proprietà del progetto, un publisher
attendibile e l'ambiente `pypi`. Pubblica gli stessi artefatti di rilascio verificati
senza ricompilare né memorizzare un token API. I rilasci taggati in questo repository pubblico
generano attestazioni degli artefatti GitHub; i fork privati richiedono un piano supportato
e un opt-in esplicito. Consulta la
[guida completa ai rilasci](../../../docs/releasing.md) per configurazione, comandi esatti e tentativi.

## Sviluppo

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Gli strumenti di sviluppo risiedono nei gruppi di dipendenze [PEP 735](https://peps.python.org/pep-0735/)
in `pyproject.toml` (`dev`, `fuzz`, `build`), quindi non compaiono mai nei
metadati del pacchetto pubblicato. `uv.lock` è l'unico lockfile; la CI installa con
`uv sync --locked` e fallisce quando il lockfile non è aggiornato. Seleziona l'interprete con
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) o qualsiasi Python 3.12+.

La CI applica una soglia minima di copertura del pacchetto del 90%. I test unitari includono server di loopback
controllati e casi offline per profili, cronologia e validatore di rilascio; il laboratorio Compose esegue
OpenSSH, MariaDB, nginx e net-snmp su un bridge isolato. Eseguilo con
`make test-integration`. Consulta [CONTRIBUTING.md](../../../CONTRIBUTING.md) e gli
[strumenti di rilascio](../../../scripts/README.md).

Il container runtime gira come UID/GID 10001 senza directory home, senza login di
shell e senza pip, e può scrivere in `/app/output`. Concedi a quell'utente l'accesso in scrittura a
qualsiasi directory di output montata. Non necessita di capability e funziona con un
filesystem root in sola lettura, quindi può essere eseguito come:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap usa il proprio comportamento di rilevamento TCP senza privilegi in questo container. La CI fa fallire
la compilazione dell'immagine per qualsiasi vulnerabilità HIGH o CRITICAL correggibile segnalata da Trivy.

## Controlli sulla supply chain

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
viene eseguito su main e settimanalmente, pubblica il proprio punteggio reale e carica i risultati nel code
scanning di GitHub. Le Action e le immagini base dei container sono bloccate tramite hash immutabili; le dipendenze
Python sono risolte in `uv.lock`. I fallimenti di Bandit fanno fallire la CI e il fuzzing limitato con Atheris
esercita i parser SSH, MySQL, HTTP, dei certificati e BER SNMPv3
senza accesso alla rete.

Scorecard misura anche l'attività storica di revisione, la diversità dei contributori e la
provenienza dei rilasci. Tali punteggi riflows/riflettono evidenze reali; non sono dichiarazioni
che ogni controllo di governance o di rilascio storico sia soddisfatto. Consulta
[SECURITY.md](../../../SECURITY.md) e la [provenienza dei rilasci](../../../docs/releasing.md).

## Localizzazione

I messaggi della CLI e le tabelle di riepilogo/diff su terminale supportano 45 impostazioni locali (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) senza dipendenze runtime aggiuntive. La risoluzione rispetta `--lang`, poi `LC_ALL`, `LC_MESSAGES` e `LANG`, ricadendo su `en`. Gli schemi JSON, le colonne CSV e gli script di esportazione rimangono invariati in tutte le lingue.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Contributi

I contributi devono includere un caso riproducibile, preservare i contratti documentati della CLI e dei
formati di dati e superare i controlli di qualità sopra indicati. Consulta
[CONTRIBUTING.md](../../../CONTRIBUTING.md) per il flusso di lavoro di sviluppo e
[la guida ai rilasci](../../../docs/releasing.md) per le decisioni su compatibilità e controllo delle versioni.

## Stato di sicurezza e licenza

Consulta [SECURITY.md](../../../SECURITY.md) per la segnalazione privata e le versioni supportate.
hostcensus è distribuito sotto la [Licenza MIT](../../../LICENSE).

Le intestazioni dei sorgenti utilizzano identificatori SPDX e preservano i crediti dei contributori dalla cronologia Git.
Consulta [AUTHORS.md](../../../AUTHORS.md) per l'attribuzione. Le catture binarie di test e il
lockfile generato usano file `.license` adiacenti; il testo MIT è in `LICENSES/MIT.txt`.
