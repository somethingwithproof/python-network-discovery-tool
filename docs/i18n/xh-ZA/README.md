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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · **isiXhosa** · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

I-hostcensus sisixhobo se-CLI sePython soluhlu lweenkonzo oluphindaphindekayo kwiinethiwekhi ozilawulayo.
Irekhoda oko kuvezwa zizixhobo, ithelekise iziphumo zokujonga ngokuhamba kwexesha, kwaye yenze izikripthi zokungenisa kwi-Kadupul. I-backend emiselweyo isebenzisa ii-sockets ze-asyncio ngaphandle kwe-root; ukufumanisa nge-Nmap okukhethekayo kunokuchonga ii-hosts ngaphaya kwee-ports zeenkonzo ezicwangcisiweyo.

## Kutheni usebenzisa i-hostcensus

Ingxelo ye-port yexesha elinye ayichazi ukuba uqwalaselo olulandelayo lutshintshile okanye lusilele nje. I-hostcensus idibanisa iimeko zeenkonzo ezicacileyo, ii-probes ezinemida, iiprofayile zokuskena eziphindaphindekayo, kunye nembali yasekhaya. Abasebenzisi bokulawula banokuphinda umda ofanayo, bahlole iimpazamo, kwaye bahlule iziphumo ezingaqinisekanga kutshintsho oluqinisekisiweyo.

- **Ubungqina benkonzo:** ukuchongwa kwe-SSH, imibuliso ye-MySQL, ii-headers ze-HTTP, uqwalaselo lwezatifikethi ze-TLS, kunye nokufumanisa nge-SNMP okanye imibuzo ye-system-MIB eneziqinisekiso.
- **Umda ophindaphindekayo:** iiprofayile ze-TOML ezinamagama, ukukhutshelwa ngaphandle okongezelelekayo, iinkonzo ezicwangcisekayo, imida ye-host/probe, kunye nabasebenzi (workers) abanemida.
- **Ukuhlolwa phambi kwetrafikhi:** uhlolo lwasekhaya lwangaphambili (preflight) luqinisekisa iithagethi, izixhobo, ufikelelo kwindawo ekuyiwa kuyo, iskima sembali, kunye neebhandile ze-TLS CA ezicwangcisiweyo.
- **Imbali yoluhlu:** ii-snapshots ze-SQLite ezinentengiselwano (transactional) zigcina lonke uqwalaselo; uthelekiso lugcina ukusilela kwesikena kunye neemeko ezingaziwayo zibonakala.
- **Iziphumo ezisebenzisana nezinye iinkqubo:** iingxelo zetheminali, i-JSON kunye ne-CSV, ii-snapshots zeefayile ezinenguqulelo, kunye nezikripthi zokungenisa kwi-Kadupul.

I-CI igubungela iPython 3.12, 3.13 kunye ne-3.14 kwiLinux nakwi-macOS, kunye nelebhu yodibaniso yeCompose elawulwayo. Ikhowudi isebenzisa ii-type aliases zanamhlanje, iziphumo ze-preflight ezineentlobo ezicacileyo (typed), iiprofayile ezine-slots ezingamagama angundoqo kuphela (keyword-only) kunye nokucocwa kwe-async okulungelelanisiweyo ngelixa igcina ezo nguqulelo ze-runtime. Jonga [Ukulandelelana kweenguqulelo nokukhutshwa](../../../docs/releasing.md) ngokumalunga nesivumelwano sokuhambelana kweSemVer nenkqubo yokukhupha yeGitHub. Ibheji yokukhutshwa ichaza iziphumo ezipapashiweyo, hayi le checkout: ithegi yamva nje epapashiweyo ngoku ngu-`v0.3.0`, ngelixa le checkout isebenzisa inguqulelo yephakeji ethi `3.0.0`. Faka ukusuka kule checkout ukuze usebenzise iimpawu zoluhlu ezichazwe apha.

Qala [ngokufaka](#install), uze uye [kwiiprofayile nembali](#inventory-profiles-preflight-and-local-history).
Ngeenkcukacha zodibaniso, jonga [iminwe yenkonzo](#fingerprints),
[uthelekiso lweefayile](#inventory-diff), kunye [nokuthumela ngaphandle kwi-Kadupul](#kadupul-export).

## Ukufaka

IPython 3.12 okanye entsha iyafuneka; iPython 3.12 ukuya ku-3.14 yimethrikhi evavanyiweyo. Ukusuka kule checkout, faka izinto ezixhomekeke kuzo ze-runtime ezitshixiweyo:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Ukufumanisa ii-hosts nge-Nmap okukhethekayo, faka inkqubo ye-Nmap esebenzisayo usebenzisa umphathi weephakeji weqonga lakho; akukho phakeji yePython eyongezelelweyo efunekayo. Iziphumo ze-XML ze-Nmap zihlalutywa nge-defusedxml, eyinto engundoqo exhomekeke kuyo, ngoko ukwandiswa kwe-entity kuyaliwa. I-hostcensus iqhuba i-`nmap` efunyenwe kwi-`PATH` ngokuthe ngqo ngoluhlu lwee-arguments olungatshintshiyo, umhla wokugqiba okhula nobungakanani be-prefix, kunye nomda weziphumo oyi-64 MiB. I-Nmap ayifuneki kwi-backend emiselweyo.

## Ukufuduka ukusuka kwi-netprobe

I-hostcensus ligama elitsha le-netprobe, elikhutshwe ku-3.0.0. Le projekthi ayizange ipapashwe kwi-PyPI phantsi kwalo naliphi na kula magama mabini, ngoko ukufakwa kwakuvela kwi-checkout okanye ekukhutshweni kweGitHub. Indawo yokugcina yekhowudi (repository) yeGitHub igcina igama layo.

| Yayingu | Ngoku | Ukuhambelana |
| --- | --- | --- |
| Unikezelo `netprobe` | `hostcensus` | Faka kwakhona ukusuka kwi-checkout; akukho phakeji yegama elidala. |
| Umyalelo `netprobe` | `hostcensus` | I-`netprobe` isasebenza kwaye ishicilela umgca omnye wesilumkiso sokuphelelwa lixesha kwi-stderr. Iikhowudi zokuphuma kunye ne-stdout azitshintshanga. Iya kususwa kukhupho olukhulu olulandelayo. |
| Ii-variables zemo engqongileyo `NETPROBE_*` | `HOSTCENSUS_*` | I-variable ye-`NETPROBE_*` isetyenziswa xa iwele layo le-`HOSTCENSUS_*` lingasetwanga, ngesilumkiso esinye kwi-stderr esikhankanya amagama ee-variables kwaye singaze sikhankanye amaxabiso azo. I-`HOSTCENSUS_*` iyaphumelela xa zombini zisetiwe. Iya kususwa kukhupho olukhulu olulandelayo. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Utshintsho olwaphula ukuhambelana.** Akukho shim yokungenisa efakiweyo; hlaziya ii-imports. |
| Ithegi yomfanekiso weDocker `network-discovery:test` (CI kuphela) kunye nomsebenzisi wekhonteyina `netprobe` | `hostcensus:test`, umsebenzisi `hostcensus` | Akukho mfanekiso we-registry owakhe wapapashwa. Yakha umfanekiso kwakhona kwaye usebenzise indawo yokuqala (entrypoint) ethi `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Ifayile esele ikho enegama elidala elimiselweyo isasetyenziswa, ngesilumkiso, ngelixa igama elitsha lingekabikho. Iindlela ezicacisiweyo ze-`--config` kunye ne-`--history` azichukunyiswa. |
| Iingxelo nee-snapshots ezine-`"format": "netprobe-report"` okanye `"netprobe-snapshot"`, kunye nomhlaba `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | I-`diff` kunye ne-`export` zisakwazi ukulayisha iifayile ezibhalwe phantsi kwegama elidala, kwaye ii-JSON Schemas ezipapashiweyo zamkela zombini iindlela zokubhala. Iifayile ezintsha zisebenzisa amagama amatsha. Iziseko zedatha zembali ze-SQLite azitshintshanga kwaye zilayisha njengakuqala. |
| Izikripthi ze-Kadupul ezivela kwi-`netprobe export` | Izikripthi ezivela kwi-`hostcensus export` | Izikripthi ezindala ziqhubeka zisebenza kwaye zisafunda i-`NETPROBE_SNMP_*` xa zisebenza. Izikripthi ezintsha zifunda i-`HOSTCENSUS_SNMP_*`. |

## Umzekelo okhawulezayo

Qhuba ukusuka kwikhonteyina yovavanyo yelebhu yodibaniso echazwe phantsi koPhuhliso; iziphumo zicuthiwe:

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

## Iikhowudi zokuphuma

| Umyalelo | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | uqwalaselo/ingxelo irekhodiwe | ukusilela kwe-preflight/backend, imbali, okanye ukubhalwa kwengxelo/snapshot | ithagethi, iinketho, uqwalaselo, okanye imida engasebenziyo | - | kufikelelwe ku-`--deadline`; ingxelo eyinxenye ibhaliwe, imbali kunye ne-snapshot zitsityiwe |
| `preflight` | uhlolo luphumelele | uhlolo lwasekhaya lusilele | ithagethi/uqwalaselo olungasebenziyo okanye iindawo ekuyiwa kuzo ezingqubanayo | - | - |
| `profiles` | iiprofayile eziqinisekisiweyo zidwelisiwe | - | uqwalaselo okanye ukhetho olungafundekiyo/olungasebenziyo | - | - |
| `history` | izishwankathelo zidwelisiwe | imbali elahlekileyo, engasebenziyo, okanye engaxhaswayo | iinketho ze-CLI ezingasebenziyo | - | - |
| `compare` | uthelekiso luvelisiwe, kubandakanya naxa kukho utshintsho | imbali engafundekiyo, umda/ulandelelwano olungahambelaniyo, okanye ukusilela kokubhala | iinketho ze-CLI ezingasebenziyo | - | - |
| `diff` | akukho tshintsho | ifayile ye-`-o` ayikwazanga ukubhalwa | igalelo elilahlekileyo, elingafundekiyo okanye elingaxhaswayo, okanye uskeno olungagqitywanga ngaphandle kwe-`--allow-partial` | utshintsho lufunyenwe, uqwalaselo olungaqinisekiswanga, okanye uskeno olungagqitywanga | - |
| `export` | isikripthi sibhaliwe | isikripthi asikwazanga ukubhalwa | igalelo elingafundekiyo, uskeno olungagqitywanga ngaphandle kwe-`--allow-partial`, okanye idatha engenakuthunyelwa ngaphandle ngokukhuselekileyo | - | - |

## Ulwakhiwo lweefayile

| Imoduli | Uxanduva |
| --- | --- |
| `cli.py` | Iinketho zomyalelo, ukusombululwa kweeprofayile, i-preflight, ukuskena kunye nokunika ingxelo |
| `scanner.py`, `probes.py` | Ukwandiswa kwethagethi, abasebenzi abanemida, ukufumanisa ii-hosts kunye noqwalaselo lweenkonzo |
| `config.py`, `profiles.py` | Iinkcazo zeenkonzo kunye neeprofayile zoluhlu eziqinisekisiweyo |
| `models.py`, `output.py` | Iintlobo zeziphumo kunye noboniso lwetheminali/JSON/CSV |
| `history.py`, `diff.py` | Imbali ye-SQLite kunye nothelekiso lwee-snapshots zeefayile ezinenguqulelo |
| `preflight.py` | Uhlolo lwasekhaya kunye nokukhangela inguqulelo ye-Nmap okunomda |
| `export.py` | Izikripthi zokungenisa kwi-Kadupul eziqinisekisiweyo nezibekwe kwizicatshulwa (quoted) |

Uqwalaselo ngalunye lwenkonzo lurekhoda imeko yalo ngokwahlukileyo kwisazisi salo esibhengeziweyo.
Ukufunda nemihla yokugqiba inemida; iimpazamo (exceptions) zee-probes zihlala kwiimpazamo ze-host. Imbali ye-SQLite isebenzisa ii-transactions, ukucocwa okucacileyo konxibelelwano, kunye neendlela zokudwelisa nokuthelekisa ezifundwayo kuphela (read-only). Iimfihlo ze-SNMP zingena kuphela ngee-variables zemo engqongileyo okanye ngeefayile zeemfihlo; imbali yoluhlu igcina iisetingi ezisebenzayo ezingezomfihlo. Jonga [Ulwakhiwo](../../../docs/architecture.md) ngombhobho wokuskena, imida yawo nemida yokuthembeka, kunye ne-[SECURITY.md](../../../SECURITY.md#authorized-use) ngokusetyenziswa okugunyazisiweyo.


## Ukusetyenziswa

Skena kuphela iinethiwekhi ozilawulayo.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Ukhetho | Intsingiselo |
| --- | --- |
| `NETWORK` | I-CIDR, i-IP, okanye igama le-host; iyazikhethelwa xa kukho `--profile`. Izazisi zomda we-IPv6 (scope identifiers) ziyaliwa. |
| `-o, --output PATH` | Bhala ingxelo. Ifomathi ilandela isongezo sefayile (`.json`, `.csv`); ezinye izongezo zibuyela kwi-JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Nyanzela ifomathi yengxelo. Ayinamphumo ngaphandle kwe-`--output`. I-`.sh` ikhetha i-`kadupul`. |
| `-v, --verbose` | Ukurekhoda iilog zokususa iimpazamo (debug logging). |
| `-q, --quiet` | Cinezela iziphumo, inkqubela kunye neelog zolwazi; izilumkiso neempazamo zisaqhubeka zivela kwi-stderr. |
| `--backend asyncio\|nmap` | Ukufumanisa ii-hosts. I-`asyncio` (emiselweyo) ihlola ii-ports zeenkonzo ngokuthe ngqo; i-`nmap` iqhuba uhlolo lwe-ping lwe-nmap kuqala kwaye ifuna inkqubo ye-`nmap` kwi-`PATH`. |
| `--timeout SECONDS` | Linda ii-probes ezingazisetelanga ixesha lazo (okumiselweyo yi-1.0). Ii-probes zoqhagamshelo ezakhelwe ngaphakathi zisebenzisa i-0.3s ngaphandle kokuba itheyibhile yenkonzo isete `timeout`. |
| `--concurrency N` | Ii-probes ezisebenza ngexesha elinye (okumiselweyo yi-256). |
| `--deadline SECONDS` | Misa lonke uskeno, kuquka uhlolo lwe-nmap, emva kweli xesha (okumiselweyo yi-3600, ubuninzi yi-604800; env `HOSTCENSUS_DEADLINE`). Ii-hosts ezigqibileyo zibhalwa kwingxelo zine-`"complete": false`, akukho mbali okanye snapshot ebhalwayo, kwaye i-`scan` iphuma ngekhowudi 4. |
| `--config PATH` | Iinkcazo zeenkonzo ze-TOML kunye neesetingi ezinamagama zokuzikhethela ze-`[profiles]`. |
| `--profile NAME` | Sebenzisa iprofayile enegama; isebenzisa i-`hostcensus.toml` ngokumiselweyo xa i-`--config` ishiyiwe. |
| `--exclude IP/CIDR` | Yongeza okukhutshelwa ngaphandle; phinda njengoko kufuneka. I-host ye-IPv4 ekhutshelwe ngaphandle ikhuphela ngaphandle needilesi ze-IPv6 ezifikelela kuyo: ezi-IPv4-mapped (`::ffff:a.b.c.d`), i-NAT64 (`64:ff9b::/96`) kunye ne-6to4. Iithagethi kunye nokukhutshelwa ngaphandle okuzi-IPv4-mapped ziphathwa njengeedilesi ze-IPv4 ezizimeleyo. |
| `--max-hosts N` | Umda weedilesi ohlolwa phambi kokukhutshelwa ngaphandle (okumiselweyo/ubuninzi obungenakugqithwa yi-65,536). |
| `--history PATH` | Rekhoda uskeno olugqityiweyo kwisiseko sedatha sembali se-SQLite esikhethwayo (opt-in). |
| `--services NAMES` | Uluhlu lwamagama eenkonzo olwahlulwe ngokhoma eziza kuhlolwa, ngolo landelelwano (okumiselweyo: zonke). |
| `--ports SPEC` | Uluhlu olwahlulwe ngokhoma lwe-`NAME=PORT` (hambisa inkonzo) okanye i-`PORT` (yongeza uhlolo oluqhelekileyo lwe-TCP olubizwa ngokuba yi-`tcp-PORT`). |
| `--snmp-community-file PATH` | Ifayile egcine i-SNMPv2c community yombuzo we-system MIB. Env: `HOSTCENSUS_SNMP_COMMUNITY` (ixabiso) okanye `HOSTCENSUS_SNMP_COMMUNITY_FILE` (indlela yefayile). |
| `--snmp-user` | Umsebenzisi we-SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (okumiselweyo), `SHA224`, `SHA256`, `SHA384`, `SHA512` kunye nefayile egcine i-passphrase. Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` okanye `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (okumiselweyo), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` kunye nefayile egcine i-passphrase. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` okanye `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Bhala kwakhona i-snapshot enenguqulelo ye-`hostcensus diff`. |
| `--tls-ca-file PATH` | Qinisekisa izatifikethi ze-HTTPS ngokuchasene nale bhandile ye-PEM endaweni yovimba wesixokelelwano. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Ngokumiselweyo i-host nganye ihlolwa i-SSH (TCP 22), i-SNMP (UDP 161), i-MySQL (TCP 3306), i-HTTP (TCP 80) kunye ne-HTTPS (TCP 443). Ii-ports ze-TCP zivavanywa ngoqhagamshelo olupheleleyo. I-SNMP ivavanywa ngesicelo sokufumanisa i-engine ye-SNMPv3, apho naliphi na i-agent le-SNMPv3 kufuneka liphendule ngaphandle kweziqinisekiso; ii-agents ezithetha i-v1/v2c kuphela aziyi kufunyanwa yile probe. Nge-backend ye-asyncio i-host ibalwa njengephilayo xa nayiphi na i-probe ifumana impendulo, kuquka uqhagamshelo olwaliweyo, ngoko ke i-host elahla zonke ii-probes ine-`alive=false` kunye nempazamo ethi "Host is down"; oku akubonisi ukuba icinyiwe ngokwenyama. Nge-`--backend nmap`, i-nmap igqiba ukuba zeziphi ii-hosts eziphilayo (i-ICMP njenge-root, i-TCP 80/443 ngenye indlela).

### Iminwe yenkonzo (Fingerprints)

Inkonzo nganye evulekileyo ifunyanwa uphawu lwayo (fingerprint) kwinto eyithumelayo phambi kwalo naluphi na ungeno. Akukho nto iqinisekisayo ngaphandle kombuzo we-SNMP, kwaye kuphela xa unikezela ngeziqinisekiso.

| I-probe | Ifunda | `version` | Izitshixo ze-`details` |
| --- | --- | --- | --- |
| `ssh` | Umgca wokuchonga we-RFC 4253 | isoftwe, umz. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Uxhulumaniso lokuqala lwe-MySQL/MariaDB (handshake) | inguqulelo yeseva | `server_version`, `flavor`, `auth_plugin`, okanye `error_code`/`error` |
| `http` | Impendulo ye-`HEAD /` | I-header ye-`Server` | `status`, `server` |
| `https` | I-TLS handshake, isatifikethi, `HEAD /` | I-header ye-`Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Ukufumanisa kwe-SNMPv3; ngeziqinisekiso, i-GET ye-sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; ngeziqinisekiso `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, okanye `snmp_error` |

Ithagethi yegama le-host isombululwa kube kanye kwi-host nganye kwaye yonke i-probe iqhagamshela kulo dilesi, erekhodwe njenge-`address` kwiziphumo; igama lisetyenziselwa kuphela i-TLS SNI, ukuqinisekiswa kwesatifikethi kunye ne-header ye-HTTP ethi `Host`. Igama elingasombululekiyo linika iimeko ezingaziwayo (`unknown`) kunye nempazamo ethi `Cannot resolve`. Amagama e-Reverse DNS agcinwa kuphela xa equlethe iimpawu zegama le-host, kwaye ukhangelo olungaphezulu kwe-16 alusebenzi ngexesha elinye. I-HTTPS isebenzisa ukuqinisekiswa kwesatifikethi negama le-host ngokuchasene novimba wesixokelelwano okanye i-`--tls-ca-file`. Uvimba wokuthembeka ulayishwa kube kanye kuskeno kwaye uphinde usetyenziswe kuyo yonke i-probe ye-HTTPS. Uqhagamshelo lwe-TCP kunye ne-TLS handshake zimiselwa ixesha ngokwahlukileyo, ngoko i-port eyamkela uqhagamshelo kodwa imise i-handshake iba yi-`open` ene-`tls_error`, hayi `filtered`. Ukuba uqinisekiso luyasilela, isiphumo sirekhoda `cert_verified: false` kunye ne-`cert_verify_error`; ayiphindi izame ngeesetingi ezibuthathaka okanye ithumele isicelo se-HTTP. Iinkcukacha zesatifikethi kunye nee-headers ze-HTTP ziqokelelwa kuphela emva kokuba uqinisekiso luphumelele. Nikezela ngebhandile ye-CA echanekileyo kwiinkonzo ze-CA yabucala. Iingxelo ezindala zinokuqulatha `cert_read_unverified`, ezingasaveliswa zii-probes zangoku.

Iimfihlo ze-SNMP zifundwa kuphela kwii-variables zemo engqongileyo okanye kwiifayile (`--snmp-*-file`, okanye i-variable ehambelanayo ethi `HOSTCENSUS_SNMP_*_FILE`), hayi kwamaxabiso omgca womyalelo (command-line), anokubonwa ngabanye abasebenzisi basekhaya kuluhlu lweenkqubo. I-`--snmp-community`, `--snmp-auth-key` kunye ne-`--snmp-priv-key` ezinexabiso ziphuma ngekhowudi 2 kwaye zichaze okutshintshwa ngako. Ifayile yemfihlo kufuneka ibe yi-UTF-8 enento ngaphakathi engadlulanga kwi-4096 bytes; umgca omnye omtsha wokugqibela uyashiywa, kwaye ukuseta zombini i-variable kunye nefayile yemfihlo enye yimpazamo. Iimpazamo zikhankanya igama lefayile kodwa azize zishicilele okuqulethwe kuyo. Iingxelo zokuskena nembali azibandakanyi ngabom amaxabiso eziqinisekiso. Isixhobo sokuthumela ngaphandle sinokhetho olwahlukileyo, olucacileyo oluthi `--include-credentials` oluchazwe ngezantsi. I-community ikhetha i-SNMPv2c; umsebenzisi ukhetha i-SNMPv3, enoqinisekiso xa isitshixo soqinisekiso (auth key) sinikeziwe kunye nobumfihlo xa zombini izitshixo zinikeziwe (`snmp_security_level` irekhoda ukuba yeyiphi). I-hostcensus iyala, ngekhowudi yokuphuma 2, ukudibanisa i-community nomsebenzisi we-v3, ukusebenzisa isitshixo sobumfihlo ngaphandle kwesitshixo soqinisekiso, okanye ukusebenzisa izitshixo ngaphandle komsebenzisi, kwaye ayize iphinde izame umbuzo we-v3 osileleyo nge-v2c okanye inqanaba lokhuseleko elisezantsi. Ii-agents ezithetha i-v1/v2c kuphela azikuhoyi ukufumanisa kwe-v3 okungenaziqinisekiso, ngoko zibonakala zivulekile kuphela xa kunikezelwe nge-community.

Isicatshulwa se-banner sicuthiwe saba ziimpawu ezinokushicilelwa kwaye sinomda weempawu ezingama-256 phambi kokuba sigcinwe okanye siboniswe. Ukufunda kunemida kwakhona: i-4 KiB ngomgca, i-4 KiB yombuliso we-MySQL, i-16 KiB yee-headers ze-HTTP. I-SNMP engine ID ende ngaphezu kwee-octets ezingama-32 iyanqunyulwa phambi kokuba igcinwe. I-HTTP kunye ne-HTTPS zithumela i-header ye-Host enedilesi ye-IPv6 kwizibiyeli kunye ne-port xa ingeyiyo 80 okanye 443. Iiseli ze-CSV eziqala ngophawu oluqalisa ifomyula ye-spreadsheet zongezwa isimaphambili ukuze iseli ihlale ilisicatshulwa.

### Imida

Uqhubo olunye lwamkela ubuninzi beedilesi ezingama-65,536, iinkonzo ezingama-64, kunye nee-probes ezingama-524,288 (ii-hosts ziphindaphindwe ngeenkonzo); izicelo ezinkulu ziphuma ngekhowudi 2 phambi kokuba kuthunyelwe nantoni na. I-`--concurrency` inomda wee-sockets ezingama-4096. I-probe nganye inomda ongqongqo wexesha ophindwe kane kwixabiso layo lexesha. Ii-probes zoqhagamshelo (`tcp`, `ssh`, `mysql`, `http`) zisebenzisa i-0.3 seconds ngaphandle kokuba loo nkonzo isete `timeout`. I-SNMP kunye ne-HTTPS zisebenzisa i-`--timeout` (okumiselweyo yi-1.0) xa zingazisetelanga eyazo. I-probe efikelela kumda wexesha ixelwa njenge-`unknown` ine-"probe timed out" kwi-`errors`. Ukusilela kwee-sockets zasekhaya (umzekelo ukuphelelwa zii-file descriptors) kukwayi-`unknown` kunye nempazamo erekhodiweyo; azize zibalwe njenge-port ehluziweyo (filtered) okanye i-host ecimileyo. Phambi kokuhlola, i-hostcensus inyusa umda othambileyo weefayile ezivuliweyo ukuya kumda ongqongqo ukuze ilingane ne-`--concurrency` kunye nee-descriptors ezingama-64; xa ingakwazi, uhlolo lwe-preflight lwe-`open files` luyasilela kwaye i-`scan` iphuma ngekhowudi 1 phambi kokuthumela itrafikhi. Ukufumanisa nge-Nmap kusebenzisa ixesha lokuphela kwe-host le-30 seconds. I-prefix igqithiselwa kwi-nmap ngendlela ye-CIDR, kwaye uhlolo luyasilela luphume ngekhowudi 1 xa i-nmap ixela iidilesi ezimbalwa kunoko inikwe zona (umzekelo igama engakwaziyo ukulisombulula) endaweni yokuphawula ii-hosts njengezicimileyo. Ithagethi yegama le-host isombululwa kube kanye kwaye i-nmap inikwa loo dilesi, ukuze ukufumanisa kunye nee-probes zifikelele kumatshini ofanayo. I-prefix epheleleyo yinkqubo enye ye-nmap enomda wexesha we-subprocess we-35 seconds kwiidilesi ezingama-256 nganye, zisondelwe phezulu. Uhlolo olukhuphela ngaphandle ezinye lusebenzisa amaqela ee-hosts ezingama-256 kunye nomda wexesha we-35 seconds kwiqela ngalinye. Ukudalwa kwabasebenzi kunomda ngokuzimeleyo kubungakanani boluhlu. I-Reverse DNS kunye nokusombululwa kwegama le-host zinomda wexesha owahlukileyo we-2 seconds; umnxeba we-resolver ongaze ubuye ushiywa kwi-thread yawo, ukuze ungagcini i-hostcensus isebenza ngaphaya kwale mida. Ukhangelo olungaphezulu kwe-16 alusebenzi ngexesha elinye, kwaye umnxeba oshiyiweyo ugcina indawo yawo de ubuye, ngoko inani lee-threads ezibambekileyo lihlala linomda; ukuba zonke ezili-16 ziyabambeka, ukhangelo lwamva lulinda emgceni indawo ngaphandle komda wemizuzwana emibini (oqala xa indawo ikhululekile) de i-`--deadline` imise uskeno. I-`NetworkScanner` esetyenziswa njengelayibrari ngaphandle kwe-`deadline` ingalinda indawo enjalo ngonaphakade. I-`--deadline` (okumiselweyo yiyure enye) imisela umda kuqhubo lonke ngaphezulu kwezi.

### Ukuqwalasela iinkonzo

Iinkonzo zinokutshintshwa ngefayile ye-TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

I-`probe` yenye yezi: `tcp`, `ssh`, `mysql`, `http`, `https` okanye `snmp` kwaye isebenzisa igama lenkonzo ngokumiselweyo xa elo gama liyi-probe, ngenye indlela `tcp`. Yi-`snmp` kuphela esebenzisa i-UDP. Amagama eenkonzo ngamagama amancinci, amanani, `-` kunye no-`_`. Iinkonzo ezimbini azinakwabelana nge-port kunye neprotocol; imbali irekhoda imeko enye kuloo mbini. I-`timeout` iyazikhethelwa, ngemizuzwana, kwaye ubuncinci ngu-0.05. Ii-probes zohlobo loqhagamshelo (`tcp`, `ssh`, `mysql`, `http`) zimiselwe ku-0.3 seconds. I-`snmp` kunye ne-`https` zisebenzisa i-`--timeout` yoskeno xa inkonzo ingasetanga `timeout`. I-`--timeout` ayitshintshi ixabiso lexesha elisele linayo inkonzo.

Iingxelo ze-JSON ngamaxwebhu anenguqulelo (`"format": "hostcensus-report"`, `"version": 1`) arekhoda ithagethi, iinkonzo ezihloliweyo kunye neesetingi ecaleni kwe-`devices`; i-`--format json` ngaphandle kwe-`-o` ibhala ingxelo kwi-stdout endaweni yetheyibhile. Zonke iziphumo ze-JSON zineskima esipapashiweyo; jonga [Iziphumo ze-JSON](../../../docs/json-output.md). Izixhobo zigcina imihlaba yasekuqaleni ye-`ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` kunye ne-`errors` kwaye zongeza uluhlu lwe-`services` olune-`name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, okanye `unknown` xa i-probe isilele ekhaya okanye ifikelele kumda wayo wexesha), `version` kunye ne-`details` ye-probe nganye. Iziphumo ze-CSV zifumana iikholamu zokugqibela ze-`services` kunye ne-`versions` zezivulekileyo. Ii-booleans ze-`ssh`, `snmp` kunye ne-`mysql` zilandela iinkonzo ezinamagama afanayo ncam.


## Iiprofayile zoluhlu, i-preflight, kunye nembali yasekhaya

Iiprofayile ezinamagama zabelana ngefayile ye-TOML kunye neenkcazo ezikhoyo ze-`[services]`. Kopisha i-[hostcensus.example.toml](../../../hostcensus.example.toml) kwi-`hostcensus.toml` kwaye usete iinethiwekhi ozilawulayo:

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

I-`preflight` isombulula iinketho kunye neeprofayile ngokufanayo ncam ne-`scan`, kuquka i-`--concurrency` yohlolo lweefayile ezivuliweyo, ngoko ke i-preflight ephumeleleyo ithetha ukuba i-`scan` iya kuqala ngesicwangciso esifanayo.

Iiprofayile zamkela i-`network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency`, kunye ne-`max_hosts`. I-`services` kunye ne-`ports` zisebenzisa indlela ekhoyo yoluhlu olwahlulwe ngokhoma. Iinketho ezicacileyo ze-CLI zigqitha iisetingi zeprofayile; iinketho eziphindaphindiweyo ze-`--exclude` zongeza kukukhutshelwa ngaphandle kweprofayile. Inethiwekhi ecacisiweyo kunye ne-`--profile` kufuneka iqulathwe ngaphakathi komda we-IP/CIDR waloo profayile. Amagama ee-hosts asaxhaswa kuskeno oluthe ngqo, kodwa akanakudityaniswa nokukhutshelwa ngaphandle kwe-IP. Imida yee-hosts isebenza phambi kokukhutshelwa ngaphandle; umda we-probe iyonke usasebenza emva koko. Ii-hosts ezikhutshelwe ngaphandle ziyashiywa zombini ekuhlolweni kweenkonzo nakukufumanisa nge-Nmap okukhethekayo.

Lonke uskeno lwenza uhlolo lwasekhaya lwe-preflight phambi kwetrafikhi yethagethi: imida yethagethi/probe, ufikelelo kwindawo ekuyiwa kuyo, ukufumaneka okukhethekayo kwenkqubo/wrapper ye-Nmap, iskima sembali, kunye nebhandile ye-TLS CA ecwangcisiweyo. I-`preflight` inika ingxelo ye-JSON kwaye ayiskeni iithagethi okanye idale isiseko sedatha sembali. Ibhala okwethutyana ifayile engumakhelwane ukuvavanya ufikelelo kwindawo ekuyiwa kuyo ngaphandle kokutshintsha okuqulethweyo okusele kukho. I-backend emiselweyo ye-asyncio ayifuni i-Nmap okanye i-root. Iindlela zendawo ekuyiwa kuyo kufuneka zahluke enye kwenye nakwisicwangciso segalelo, kuquka ii-hard links; ii-symlinks zendawo ekuyiwa kuyo ziyaliwa. Uhlolo olusileleyo lubuyisela u-1; umda/uqwalaselo olungasebenziyo lubuyisela u-2.

Ukubhalwa kweengxelo nokuthunyelwa ngaphandle kufuna inkxaso ye-`O_NOFOLLOW`. Kumaqonga angenayo, kuquka iWindows, oku kubhala kuyasilela ngaphandle kokuvula okanye ukunqumla indawo ekuyiwa kuyo. Iingxelo ezintsha nezikripthi zokuthumela ngaphandle zezomnini kuphela (mode 0600); ukutshintsha ifayile esele ikho kugcina iimvume zayo. Ukubhala kwi-named pipe engenamfundi kuyasilela kwangoko endaweni yokulinda. Isiseko sedatha esitsha se-`--history` naso sidalwa sesomnini kuphela; esele sikho sigcina i-mode yaso. Imiyalezo yeelog isoloko isiya kwi-stderr, ukuze i-stdout iphathe iziphumo kuphela. Ukuthunyelwa ngaphandle okuqulathe iziqinisekiso kusoloko kunyanzela i-mode 0600.

Imbali iyazikhethelwa (opt-in) kwaye ihambelana nee-snapshots ze-JSON ezikhoyo nomyalelo we-`diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Sebenzisa ii-ID ezivela kwi-`history`; umzekelo ucinga isiseko sedatha esitsha. Ii-snapshots zigcinwa ngokwe-transaction ngamaxesha okuqala/okuphela e-UTC, inguqulelo yephakeji, iisetingi ezisebenzayo ezingezomfihlo, izishwankathelo, kunye nalo lonke uqwalaselo lwee-hosts/iinkonzo, kuquka iimpazamo ze-host nganye. Uqwalaselo lwe-host olungagqitywanga luyagcinwa. Uqhubo olurhoxisiweyo alugcinwa. Izivumelwano ezikhoyo zengxelo, i-snapshot, ukuthumela ngaphandle, kunye neekhowudi zokuphuma zoskeno ziyagcinwa.

I-`history` idwelisa izishwankathelo ze-JSON ngaphandle kokufunda zonke ii-payloads zezixhobo zembali. I-`compare` ifunda izikeno ezimbini ezigciniweyo, ifuna izazisi zeethagethi ezifanayo kunye nee-ports ezikhethiweyo, kwaye ixela ukuphendula, imeko, kunye notshintsho lwemeko ye-port. I-ID yoskeno yangaphambili kufuneka yandulele i-ID yamva. Xa zombini izikeno zirekhode i-`timeout` okanye i-`backend` kwaye loo maxabiso ahlukile, ingxelo idwelisa isilumkiso kwaye isathelekisa uqwalaselo. Ixesha lokulinda elahlukileyo linokwenza i-port ehluziweyo (filtered) ibonakale ivulekile. Iimpazamo zesikena kunye noqwalaselo lwe-port olungaziwayo ziphawulwa njengezingaqinisekanga endaweni yokuphathwa njengokunyamalala okanye ukuvalwa okuqinisekisiweyo: ii-hosts ezineempazamo zivela kwi-`uncertain_hosts`, kwaye lonke utshintsho lwe-port olubandakanya `unknown` (kuquka ukungaziwa kuzo zombini izikeno) ludweliswa kwi-`unconfirmed_ports` endaweni ye-`port_changes`, ngaphandle kwe-port evulekileyo kuskeno lwamva, olulutshintsho lwe-port. I-`compare` kunye ne-`diff` zihlela ii-ports ngomgaqo ofanayo. I-`no_longer_responding` ithetha ukunqongophala kwempendulo, hayi ubungqina bokususwa kwesixhobo. Ikhowudi yokuphuma yoskeno ethi 0 ayiqinisekisi ukuba yonke i-host iphendule: hlola iimpazamo ze-host nganye. Impumelelo yothelekiso ibuyisela u-0 nokuba kukho utshintsho okanye akukho; ifayile ekhoyo ye-`diff` igcina isivumelwano sayo sekhowudi yokuphuma ethi 3. Imbali engaxhaswayo okanye eyonakeleyo ibuyisela u-1.

Imbali igcina ulwazi loluhlu, ngoko khetha uvimba weefayile wasekhaya okhuseleke ngokufanelekileyo. Iifayile zeeprofayile kunye neesetingi ezigciniweyo aziqulethe ziqinisekiso ze-SNMP; ukuphathwa kweziqinisekiso kuqhubeka ngeenketho ze-runtime/imo engqongileyo ezikhoyo.

## Uthelekiso loluhlu (Inventory diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

I-snapshot yi-JSON ene-`format: "hostcensus-snapshot"`, `version: 1`, inguqulelo ye-hostcensus, ixesha lokudalwa le-UTC, ithagethi, i-`timeout` kunye ne-`backend` yoskeno xa uskeno luzirekhodile, iinkonzo ezihloliweyo, kunye nee-hosts eziphilayo zikwimo efanayo nengxelo ye-`-o`. Ii-hosts ezicimileyo ziyashiywa. I-`diff` yamkela kwakhona iingxelo eziqhelekileyo ze-JSON ze-`scan -o`, kuquka ezo zaphambi kokuba kubekho umhlaba we-`services`.

I-`diff` ixela ii-hosts ezintsha nezinyamaleleyo, ii-ports ezivulekileyo okanye ezivalileyo kwii-hosts ezikhoyo kuzo zombini, kunye neenkonzo ezitshintshe i-`version`. Ii-ports ezihloliweyo kuskeno olunye kuphela kwezi zimbini azithelekiswa, kwaye isilumkiso siyachaza. Uqwalaselo olusileleyo aluze lufundwe njenge-"akukho tshintsho": i-port eyi-`unknown` nakuluphi na uskeno kwaye ingavulekanga kolwamva idweliswa phantsi kwe-`unconfirmed`, hayi i-`closed`, ine-`before` eyi-`open`, `unknown` okanye `not-open` (ihloliwe yaza yavalwa okanye yahluzwa) kunye ne-`after` eyi-`unknown` okanye `not-open`; i-port evulekileyo ngoku ixelwa phantsi kwe-`opened` nokuba i-probe yangaphambili isilele. I-host ezithi zonke ii-probes zayo zisilele ngaphandle kwempendulo nakuluphi na uskeno idweliswa phantsi kwe-`unsettled_hosts` (ine-`before`/`after` eyi-`up`, `uncertain` okanye `absent`, kuquka xa isilele kuzo zombini izikeno okanye ilahlekile kwenye ifayile) endaweni ye-`vanished_hosts`; ukuba iphendula kuskeno lwamva ixelwa kwakhona njenge-host entsha kunye nee-ports zayo ezivulekileyo. Ii-snapshots zigcina ezo hosts zisileleyo ngenxa yesi sizathu. Isilumkiso siyavela kwakhona xa iithagethi zahlukile, naxa zombini iifayile zirekhode i-timeout okanye i-backend kwaye loo maxabiso ahlukile. I-`-o PATH` ibhala ifom ye-JSON kwifayile nayo.

Ingxelo evela kuskeno olumisiweyo yi-`--deadline` (`"complete": false`) idwelisa kuphela ii-hosts olufikelele kuzo, ngoko i-`diff` kunye ne-`export` ziyayala ngekhowudi yokuphuma 2. I-`--allow-partial` iyayamkela ngesilumkiso kwi-stderr: i-`diff` ke idwelisa ii-hosts ezingadweliswanga kwaphela luskeno olungagqitywanga phantsi kwe-`unsettled_hosts` njenge-`unscanned` endaweni yokunyamalala (i-host eyidwelise njengecimileyo isanyamalele), isete `partial` ibe yinyani (true) kwaye ingaze ixele ukuba akukho tshintsho, kwaye i-`export` ibhala isilumkiso kwintloko yesikripthi.

Iikhowudi zokuphuma ze-`diff`: `0` akukho tshintsho, `3` utshintsho lufunyenwe, uqwalaselo olungaqinisekiswanga, okanye igalelo elingagqitywanga (`changed` iyinyani nanini na naluphi na uluhlu, kuquka `unsettled_hosts` kunye ne-`unconfirmed`, lunento ngaphakathi, okanye i-`partial` iyinyani), `2` ifayile ilahlekile, ayifundeki, ayiyiyo i-snapshot exhaswayo, okanye ayigqitywanga ngaphandle kwe-`--allow-partial`, `1` ifayile ye-`-o` ayikwazanga ukubhalwa.

## Ukuthumela ngaphandle kwi-Kadupul

I-[Kadupul](https://github.com/kadupulhq/kadupul) (i-fork ye-Cacti 1.2.31) ayinayo indlela yokungenisa izixhobo ezininzi ngefayile. Indlela yayo exhaswayo yokongeza izixhobo ukusuka kwisikripthi yi-`cli/add_device.php`, isixhobo esinye ngomnxeba, ngee-arguments eziyi-`--option=value`. I-`hostcensus export` ibhala isikripthi se-POSIX `sh` saloo minxeba:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

I-host nganye ephilayo iba ngu-`php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Ii-hosts apho umbuzo we-SNMP woskeno uphumeleleyo zifumana `--version=2 --community=...` okanye `--version=3 --username=... --authproto=... --password=...` (kunye ne-`--privproto`/`--privpass` kwi-authPriv), `--port` kunye ne-`--avail=snmp`. Ukuthumela ngaphandle kwe-SNMPv3 kufuna `--snmp-user`, kwaye i-noAuthNoPriv iyaliwa kuba i-`add_device.php` ifuna igama lokugqitha le-v3.
- Ezinye ii-hosts zifumana `--version=0 --avail=ping`, zine-`--ping_method=tcp --ping_port=` eyi-port yokuqala ye-TCP evulekileyo, okanye i-ICMP ukuba akukho nanye.
- I-`--notes` idwelisa iinkonzo ezivulekileyo kunye neenguqulelo. I-`--description` ligama le-reverse-DNS xa liqhelekile (oonobumba, amanani, `.`, `_`, `-`), ngenye indlela yi-IP, kwaye yenziwa yahluke, kuba i-`add_device.php` iphatha inkcazo esele ikho njengohlaziyo kweso sixhobo.

Lonke ixabiso liyaqinisekiswa kwaye libekwe kwizicatshulwa ze-shell nge-`shlex.quote`. Ngokumiselweyo akukho mfihlo ye-SNMP ebhalwayo: isikripthi sandisa i-`HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` okanye `HOSTCENSUS_SNMP_PRIV_KEY` ngexesha lokusebenza kwaye sima ukuba enye ayisetwanga. I-`--include-credentials` ibhala amaxabiso asuka kwezo variables zemo engqongileyo kwisikripthi endaweni yoko, iyidale ine-mode 0600, kwaye irekhode isilumkiso. I-`add_device.php` ngokwayo ishicilela i-community kwaye ifumana iimfihlo njengee-arguments, ezibonakala kuluhlu lweenkqubo zeseva ye-Kadupul ngelixa umnxeba ngamnye usebenza.

I-`add_device.php` iphuma ngekhowudi 1 kwiikopi eziphindiweyo nakwiimpazamo; isikripthi siyaqhubeka, sibale ukusilela, kwaye siphume ngekhowudi 1 ukuba kukho isixhobo esingongezwanga. Ii-ID zeethempleyithi zivela kwi-`php cli/add_device.php --list-host-templates`. Iikhowudi zokuphuma ze-`export`: `0` ibhaliwe, `2` igalelo elingafundekiyo, uskeno olungagqitywanga ngaphandle kwe-`--allow-partial`, okanye idatha engenakuthunyelwa ngaphandle ngokukhuselekileyo, `1` isikripthi asikwazanga ukubhalwa.

## Ukulandelelana kweenguqulelo nenkqubo yokukhupha

I-hostcensus ilandela i-[Semantic Versioning](https://semver.org/spec/v2.0.0.html): izilungiso ezihambelanayo zinyusa inguqulelo ye-patch, iimpawu/ukuyekiswa okuhambelanayo kunyusa inguqulelo encinci (minor), kwaye utshintsho olwaphula ukuhambelana lunyusa inguqulelo enkulu (major). Imiyalelo neenketho, iikhowudi zokuphuma kunye nee-JSON schemas sisivumelwano sikawonke-wonke; indlela yokusebenza ephelelwe lixesha iyaqhubeka isebenza de kube lukhupho olukhulu olulandelayo, ngaphandle kokuba isilungiso sokhuseleko sifuna ukuyitshintsha ngokukhawuleza (i-changelog ke ichaza isizathu).

I-release-please ivula i-PR yokukhupha kwizihloko ze-Conventional Commit kwi-`main`, inyusa i-`pyproject.toml`, `uv.lock` kunye ne-`CHANGES.md`. Ukuyidibanisa kudala ithegi ethi `vMAJOR.MINOR.PATCH` kunye noyilo lokukhupha lweGitHub, apho i-CI incamathelisa i-wheel evavanyiweyo, unikezelo lwekhowudi yomthombo (source distribution) kunye nee-checksums; iGitHub igcina iziqinisekiso zokwakha (build attestations) zezo fayile nge-API yayo yeziqinisekiso. Umgcini uyahlola aze apapashe uyilo zakuba iifayile zincamathelisiwe. Ukukhutshwa akuze kutshintshwe.

Ukupapasha okuthembekileyo kwe-PyPI kuyazikhethelwa kwaye kufuna ubunini beprojekthi, umpapashi othembekileyo kunye nemo engqongileyo ye-`pypi`. Ipapasha kwakuzo iziphumo zokukhupha ezihloliweyo ngaphandle kokwakha kwakhona okanye ukugcina ithokheni ye-API. Ukukhutshwa okunethegi kule ndawo yokugcina kawonke-wonke kuvelisa iziqinisekiso zeziphumo zeGitHub; ii-forks zabucala zifuna isicwangciso esixhaswayo kunye nokukhetha okucacileyo. Jonga [isikhokelo esipheleleyo sokukhupha](../../../docs/releasing.md) ngokuseta, imiyalelo echanekileyo kunye nokuzama kwakhona.

## Uphuhliso

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Izixhobo zophuhliso zihlala kumaqela ezinto ezixhomekeke kuzo ze-[PEP 735](https://peps.python.org/pep-0735/) kwi-`pyproject.toml` (`dev`, `fuzz`, `build`), ngoko azize zivele kwimetadatha yephakeji epapashiweyo. I-`uv.lock` yeyona fayile yotshixo (lockfile) yodwa; i-CI ifaka nge-`uv sync --locked` kwaye iyasilela xa ifayile yotshixo iphelelwe lixesha. Khetha itoliki (interpreter) nge-`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), okanye nayiphi na iPython 3.12+.

I-CI inyanzelisa ubuncinci bokugutyungelwa kwephakeji (coverage) obungama-90%. Iimvavanyo zeyunithi zibandakanya iiseva ze-loopback ezilawulwayo kunye neemeko zeprofayile/imbali/umqinisekisi wokukhupha ezingekho kwi-intanethi; ilebhu yeCompose iqhuba i-OpenSSH, i-MariaDB, i-nginx kunye ne-net-snmp kwibhulorho eyodwa (isolated bridge). Yiqhube nge-`make test-integration`. Jonga [CONTRIBUTING.md](../../../CONTRIBUTING.md) kunye [nezixhobo zokukhupha](../../../scripts/README.md).

Ikhonteyina ye-runtime isebenza njenge-UID/GID 10001 ngaphandle kovimba weefayile wasekhaya (home directory), ngaphandle kokungena kwi-shell nangaphandle kwe-pip, kwaye inokubhala ku-`/app/output`. Nika loo msebenzisi imvume yokubhala kuyo nayiphi na indawo yokuphuma eqhotyoshelweyo (mounted). Ayifuni malungelo (capabilities) kwaye isebenza ngesixokelelwano seefayile se-root esifundwayo kuphela (read-only), ngoko inokuqhubeka ngolu hlobo:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

I-Nmap isebenzisa indlela yayo yokufumanisa ye-TCP engenamalungelo awodwa kule khonteyina. I-CI yenza ukwakhiwa komfanekiso kusilele kulo naluphi na ubuthathaka be-HIGH okanye be-CRITICAL obulungisekayo obuxelwa yi-Trivy.

## Uhlolo lwetyathanga lonikezelo (Supply-chain checks)

I-[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) isebenza kwi-main nakwiveki nganye, ipapashe amanqaku ayo okwenene, kwaye ilayishe iziphumo kukuskenwa kwekhowudi yeGitHub. Ii-Actions kunye neziseko zeekhonteyina zibotshelelwe ngee-hashes ezingatshintshiyo; izinto ezixhomekeke kuzo zePython zisombululwe kwi-`uv.lock`. Ukusilela kwe-Bandit kwenza i-CI isilele, kwaye i-fuzzing ye-Atheris enomda ivavanya ii-parsers ze-SSH, i-MySQL, i-HTTP, isatifikethi kunye ne-SNMPv3 BER ngaphandle kofikelelo lwenethiwekhi.

I-Scorecard ikwalinganisa umsebenzi wophando wembali, iyantlukwano yabaxhasi, kunye nemvelaphi yokukhupha. Loo manqaku abonisa ubungqina bokwenene; awabangi ukuba lonke uhlolo lolawulo okanye lokukhupha lwembali lwanelisiwe. Jonga [SECURITY.md](../../../SECURITY.md) kunye [nemvelaphi yokukhupha](../../../docs/releasing.md).

## Ukulungiselela iilwimi (Localization)

Imiyalezo ye-CLI kunye neetheyibhile zezishwankathelo/diff zetheminali zixhasa iilwimi ezingama-45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ngaphandle kwezinto ezongezelelweyo ze-runtime ezixhomekeke kuzo. Ukusombulula kuhlonipha i-`--lang`, kulandele i-`LC_ALL`, `LC_MESSAGES`, kunye ne-`LANG`, kubuyele ku-`en`. Ii-JSON schemas, iikholamu ze-CSV, kunye nezikripthi zokuthumela ngaphandle zihlala zingatshintshanga kuzo zonke iilwimi.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Ukuba negalelo

Igalelo kufuneka libandakanye imeko ephindaphindekayo, ligcine izivumelwano ze-CLI nezefomathi yedatha ezibhaliweyo, kwaye liphumelele uhlolo lomgangatho olungentla. Jonga [CONTRIBUTING.md](../../../CONTRIBUTING.md) ngendlela yokusebenza yophuhliso kunye [nesikhokelo sokukhupha](../../../docs/releasing.md) ngezigqibo zokuhambelana nokulandelelana kweenguqulelo.

## Imeko yokhuseleko nelayisensi

Jonga [SECURITY.md](../../../SECURITY.md) ngokunika ingxelo yabucala kunye neenguqulelo ezixhaswayo.
I-hostcensus inelayisensi phantsi kwe-[MIT License](../../../LICENSE).

Ii-headers zekhowudi yomthombo zisebenzisa izazisi ze-SPDX kwaye zigcina imbeko yabaxhasi ukusuka kwimbali ye-Git. Jonga [AUTHORS.md](../../../AUTHORS.md) ngochazo lwabanegalelo. Uqokelelo lovavanyo lwe-binary kunye nefayile yotshixo evelisiweyo zisebenzisa iifayile ze-`.license` ezikufutshane; isicatshulwa se-MIT siku-`LICENSES/MIT.txt`.
