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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · **isiZulu**

</details>

I-hostcensus iyithuluzi le-Python CLI lokubhala uhlu lwamasevisi olungaphindwa kumanethiwekhi owalawulayo.
Ibhala phansi okudalulwa amadivayisi, iqhathanise okutholakele ngokuhamba kwesikhathi, futhi ikhiqize
izikripthi zokungenisa ku-Kadupul. I-backend emisiwe isebenzisa ama-socket e-asyncio ngaphandle kwemvume ye-root;
ukutholwa nge-Nmap okungakhethwa kungakhomba ama-host ngale kwamachweba amasevisi ahleliwe.

## Kungani i-hostcensus

Umbiko wechweba owenziwa kanye awuchazi ukuthi ukuhlola okulandelayo kushintshile noma
kumane kwehlulekile. I-hostcensus ihlanganisa izimo zamasevisi ezicacile, ama-probe anomkhawulo, amaphrofaili
okuskena angasetshenziswa kabusha, nomlando wendawo. Abaphathi bangaphinda ububanzi obufanayo, bahlole
amaphutha, futhi bahlukanise phakathi kokutholakele okungaqinisekile nezinguquko eziqinisekisiwe.

- **Ubufakazi besevisi:** ukuhlonza kwe-SSH, imikhonzo ye-MySQL, ama-header e-HTTP, ukuhlola
  kwezitifiketi ze-TLS, nokutholwa kwe-SNMP noma imibuzo ye-system-MIB enezifakazi zokungena.
- **Ububanzi obuphindekayo:** amaphrofaili e-TOML aqanjwe amagama, ukukhishwa okungezekayo, amasevisi
  ahlelekayo, imikhawulo yama-host/ama-probe, nezisebenzi ezinomkhawulo.
- **Ukuhlola ngaphambi kwethrafikhi:** ukuhlola kwangaphambili kwendawo kuqinisekisa izinhloso, amathuluzi,
  ukufinyelela endaweni okuyiwa kuyo, i-schema yomlando, namaqoqo e-TLS CA ahleliwe.
- **Umlando wohlu:** ama-snapshot e-SQLite anama-transaction agcina konke okutholakele;
  ukuqhathanisa kugcina ukwehluleka kwesikena nezimo ezingaziwa kubonakala.
- **Umphumela osebenzisana nezinye izinhlelo:** imibiko ye-terminal, ye-JSON neye-CSV, ama-snapshot amafayela anezinguqulo,
  nezikripthi zokungenisa ku-Kadupul.

I-CI ihlanganisa i-Python 3.12, 3.13 ne-3.14 ku-Linux naku-macOS, kanye nelabhoratri yokuhlanganiswa ye-Compose
elawulwayo. Ikhodi isebenzisa ama-type alias esimanje, imiphumela yokuhlola kwangaphambili enohlobo olucacile,
amaphrofaili ane-slot asebenzisa ama-keyword kuphela, nokuhlanza kwe-async okuhlelekile ngenkathi igcina lezo
zinguqulo zokusebenza. Bona [Ukuhlelwa kwezinguqulo nokukhishwa](../../../docs/releasing.md) ukuze uthole isivumelwano sokuhambisana kwe-SemVer
nenqubo yokukhishwa ku-GitHub. Ibheji yokukhishwa ichaza ama-artifact ashicilelwe, hhayi le khophi yekhodi (checkout): ithegi yakamuva eshicilelwe okwamanje ithi
`v0.3.0`, kanti le khophi isebenzisa inguqulo yephakheji ethi `3.0.0`. Faka usuka kule khophi
ukuze usebenzise izici zohlu ezibhalwe lapha.

Qala ngokuthi [ukufaka](#install), bese ulandela ngokuthi [amaphrofaili nomlando](#inventory-profiles-preflight-and-local-history).
Ukuze uthole imininingwane yokuhlanganiswa, bona [izigxivizo zamasevisi](#fingerprints),
[ukuqhathanisa amafayela](#inventory-diff), kanye [nokuthumela ku-Kadupul](#kadupul-export).

<a name="install"></a>

## Ukufaka

Kudingeka i-Python 3.12 noma entsha; i-Python 3.12-3.14 iyinhlanganisela ehloliwe. Usuka kule
khophi yekhodi, faka izincike zokusebenza ezikhiyiwe:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Ukuze uthole ama-host nge-Nmap ongayikhetha, faka uhlelo lwe-Nmap usebenzisa umphathi wamaphakheji
wohlelo lwakho; alikho iphakheji elengeziwe le-Python elidingekayo. Umphumela we-XML we-Nmap uhlaziywa nge-defusedxml,
okuyincike eyisisekelo, ngakho ukwandiswa kwezinto (entity expansion) kuyaliwa. I-hostcensus igijima
i-`nmap` etholakala ku-`PATH` ngqo ngohlu olungaguquki lwezimpikiswano, umnqamulajuqu okhula
ngosayizi we-prefix, nomkhawulo womphumela ongu-64 MiB. I-Nmap ayidingeki ku-backend emisiwe.

## Ukuthutha usuka ku-netprobe

I-hostcensus igama elisha le-netprobe, elikhishwe ku-3.0.0. Iphrojekthi ayikaze
ishicilelwe ku-PyPI ngaphansi kwelinye lala magama, ngakho ukufakwa kwakuvela kukhophi yekhodi noma ekukhishweni
ku-GitHub. Indawo yokugcina yekhodi ku-GitHub igcina igama layo.

| Kwakuyi- | Manje | Ukuhambisana |
| --- | --- | --- |
| Ukusabalalisa `netprobe` | `hostcensus` | Faka kabusha usuka kukhophi yekhodi; alikho iphakheji legama elidala. |
| Umyalo we-`netprobe` | `hostcensus` | I-`netprobe` isasebenza futhi iphrinta umugqa owodwa wesixwayiso sokuyekwa ku-stderr. Amakhodi okuphuma ne-stdout akushintshile. Izosuswa ekukhishweni okukhulu okulandelayo. |
| Iziguquguquki zendawo ze-`NETPROBE_*` | `HOSTCENSUS_*` | Isiguquguquki se-`NETPROBE_*` sisetshenziswa uma esihambisana naso se-`HOSTCENSUS_*` singasethiwe, ngesixwayiso esisodwa ku-stderr esiqamba amagama eziguquguquki hhayi amanani azo. I-`HOSTCENSUS_*` iyaphumelela uma zombili zisethiwe. Izosuswa ekukhishweni okukhulu okulandelayo. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Kuyaphula ukuhambisana.** Ayikho i-shim yokungenisa efakiwe; buyekeza ama-import. |
| Ithegi yesithombe se-Docker ethi `network-discovery:test` (i-CI kuphela) nomsebenzisi we-container ongu-`netprobe` | `hostcensus:test`, umsebenzisi ongu-`hostcensus` | Akukho sithombe se-registry esake sashicilelwa. Yakha isithombe futhi bese usebenzisa i-entrypoint ye-`hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Ifayela elikhona elinegama elidala elimisiwe lisasetshenziswa, ngesixwayiso, uma igama elisha lingakabi khona. Izindlela ezicacisiwe ze-`--config` ne-`--history` azithintwa. |
| Imibiko nama-snapshot ane-`"format": "netprobe-report"` noma `"netprobe-snapshot"`, kanye nensimu ye-`netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | I-`diff` ne-`export` zisalayisha amafayela abhalwe ngaphansi kwegama elidala, futhi ama-JSON Schema ashicilelwe amukela zombili izipelingi. Amafayela amasha asebenzisa amagama amasha. Izizindalwazi zomlando ze-SQLite azishintshile futhi zilayisha njengakuqala. |
| Izikripthi ze-Kadupul ezivela ku-`netprobe export` | Izikripthi ezivela ku-`hostcensus export` | Izikripthi ezindala ziqhubeka zisebenza futhi zisafunda i-`NETPROBE_SNMP_*` uma zigijima. Izikripthi ezintsha zifunda i-`HOSTCENSUS_SNMP_*`. |

## Isibonelo esisheshayo

Kugijinyiswe kusuka ku-container yokuhlola yelabhoratri yokuhlanganiswa echazwe ngaphansi kokuthi Ukuthuthukiswa; umphumela ufinyeziwe:

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

## Amakhodi okuphuma

| Umyalo | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | okutholakele/umbiko kubhaliwe | ukuhlola kwangaphambili/i-backend, umlando, noma ukubhalwa kombiko/kwe-snapshot kwehlulekile | inhloso, izinketho, ukuhlelwa, noma imikhawulo engavumelekile | - | i-`--deadline` ifinyelelwe; umbiko ongaphelele ubhaliwe, umlando ne-snapshot kweqiwe |
| `preflight` | ukuhlola kuphumelele | ukuhlola kwendawo kwehlulekile | inhloso/ukuhlelwa okungavumelekile noma izindawo okuyiwa kuzo eziphikisanayo | - | - |
| `profiles` | amaphrofaili aqinisekisiwe abaliwe | - | ukuhlelwa noma ukukhetha okungafundeki/okungavumelekile | - | - |
| `history` | izifinyezo zibaliwe | umlando ongekho, ongavumelekile, noma ongasekelwa | izinketho ze-CLI ezingavumelekile | - | - |
| `compare` | ukuqhathanisa kukhiqiziwe, okuhlanganisa nalapho kunezinguquko | umlando ongafundeki, ububanzi/ukuhleleka okungahambisani, noma ukwehluleka ukubhala | izinketho ze-CLI ezingavumelekile | - | - |
| `diff` | azikho izinguquko | ifayela le-`-o` alikwazanga ukubhalwa | okufakiwe okungekho, okungafundeki noma okungasekelwa, noma ukuskena okungaphelele ngaphandle kwe-`--allow-partial` | izinguquko ezitholakele, okutholakele okungaqinisekisiwe, noma ukuskena okungaphelele | - |
| `export` | iskripthi sibhaliwe | iskripthi asikwazanga ukubhalwa | okufakiwe okungafundeki, ukuskena okungaphelele ngaphandle kwe-`--allow-partial`, noma idatha engakwazi ukuthunyelwa ngokuphepha | - | - |

## Ukwakheka

| Imojuli | Umthwalo wemfanelo |
| --- | --- |
| `cli.py` | Izinketho zemiyalo, ukuxazulula amaphrofaili, ukuhlola kwangaphambili, ukuskena nokubika |
| `scanner.py`, `probes.py` | Ukwandisa izinhloso, izisebenzi ezinomkhawulo, ukutholwa kwama-host nokuhlola amasevisi |
| `config.py`, `profiles.py` | Izincazelo zamasevisi namaphrofaili ohlu aqinisekisiwe |
| `models.py`, `output.py` | Izinhlobo zemiphumela nokukhiqizwa kwe-terminal/JSON/CSV |
| `history.py`, `diff.py` | Umlando we-SQLite nokuqhathaniswa kwama-snapshot amafayela anezinguqulo |
| `preflight.py` | Ukuhlola kwendawo nokubheka inguqulo ye-Nmap okunomkhawulo |
| `export.py` | Izikripthi zokungenisa ku-Kadupul eziqinisekisiwe futhi ezifakwe izingcaphuno |

Ukuhlola kwesevisi ngayinye kubhala isimo sayo ngokwehlukana nobunikazi bayo obumenyezelwayo.
Ukufunda neminqamulajuqu kunomkhawulo; amaphutha ama-probe ahlala emaphutheni e-host. Umlando
we-SQLite usebenzisa ama-transaction, ukuhlanza kokuxhumana okucacile, nezindlela zokubala nezokuqhathanisa zokufunda kuphela.
Izimfihlo ze-SNMP zingena kuphela ngeziguquguquki zendawo noma ngamafayela emfihlo; umlando wohlu
ugcina izilungiselelo ezisebenzayo ezingeyona imfihlo. Bona
[Ukwakhiwa kwesistimu](../../../docs/architecture.md) ukuze uthole umugqa wokuskena, imikhawulo yawo nemingcele yokwethenjwa,
kanye ne-[SECURITY.md](../../../SECURITY.md#authorized-use) ukuze uthole ukusetshenziswa okugunyaziwe.


## Ukusetshenziswa

Skena kuphela amanethiwekhi owalawulayo.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Inketho | Incazelo |
| --- | --- |
| `NETWORK` | I-CIDR, i-IP, noma igama le-host; iyazikhethela uma usebenzisa i-`--profile`. Izihlonzi zobubanzi ze-IPv6 ziyaliwa. |
| `-o, --output PATH` | Bhala umbiko. Ifomethi ilandela isandiso (`.json`, `.csv`); ezinye izandiso zibuyela ku-JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Phoqa ifomethi yombiko. Akunamthelela ngaphandle kwe-`--output`. I-`.sh` ikhetha i-`kadupul`. |
| `-v, --verbose` | Ukubhala amalogi okususa amaphutha. |
| `-q, --quiet` | Fihla imiphumela, inqubekela phambili namalogi olwazi; izixwayiso namaphutha kusavela ku-stderr. |
| `--backend asyncio\|nmap` | Ukutholwa kwama-host. I-`asyncio` (emisiwe) ihlola amachweba amasevisi ngqo; i-`nmap` igijima i-nmap ping sweep kuqala futhi idinga uhlelo lwe-`nmap` ku-`PATH`. |
| `--timeout SECONDS` | Linda ama-probe angazibekeli isikhathi sawo (okumisiwe ngu-1.0). Ama-probe okuxhuma akhelwe ngaphakathi asebenzisa u-0.3s ngaphandle uma ithebula lesevisi libeka i-`timeout`. |
| `--concurrency N` | Inani lama-probe asebenza ngesikhathi esisodwa (okumisiwe ngu-256). |
| `--deadline SECONDS` | Misa ukuskena konke, kuhlanganise ne-nmap sweep, ngemva kwalesi sikhathi (okumisiwe ngu-3600, umkhawulo ongu-604800; env `HOSTCENSUS_DEADLINE`). Ama-host aqedile abhalwa embikweni ane-`"complete": false`, akukho mlando noma i-snapshot ebhalwayo, futhi i-`scan` iphuma ngekhodi 4. |
| `--config PATH` | Izincazelo zamasevisi ze-TOML nezilungiselelo ezingakhethwa ze-`[profiles]` eziqanjwe amagama. |
| `--profile NAME` | Sebenzisa iphrofaili eqanjwe igama; ibuyela ku-`hostcensus.toml` uma i-`--config` ingafakiwe. |
| `--exclude IP/CIDR` | Engeza okukhishiwe; phinda njengoba kudingeka. I-host ye-IPv4 ekhishiwe nayo ikhipha amakheli e-IPv6 afinyelela kuyo: e-IPv4-mapped (`::ffff:a.b.c.d`), i-NAT64 (`64:ff9b::/96`) ne-6to4. Izinhloso ezihlotshaniswe ne-IPv4 nokukhishiwe kuphathwa njengamakheli e-IPv4 ezimele wona. |
| `--max-hosts N` | Umkhawulo wamakheli ohlolwa ngaphambi kokukhishwa (okumisiwe/umkhawulo oqinile ngu-65,536). |
| `--history PATH` | Bhala ukuskena okuqediwe kusizindalwazi somlando se-SQLite esikhethelwayo. |
| `--services NAMES` | Uhlu oluhlukaniswe ngokhefana lwamagama amasevisi azohlolwa, ngalolo hlelo (okumisiwe: wonke). |
| `--ports SPEC` | Uhlu oluhlukaniswe ngokhefana lwe-`NAME=PORT` (yisa isevisi kwelinye ichweba) noma i-`PORT` (engeza ukuhlola kwe-TCP okujwayelekile okubizwa ngokuthi `tcp-PORT`). |
| `--snmp-community-file PATH` | Ifayela eline-SNMPv2c community yombuzo we-system MIB. Env: `HOSTCENSUS_SNMP_COMMUNITY` (inani) noma `HOSTCENSUS_SNMP_COMMUNITY_FILE` (indlela yefayela). |
| `--snmp-user` | Umsebenzisi we-SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | I-`MD5`, `SHA` (emisiwe), `SHA224`, `SHA256`, `SHA384`, `SHA512` kanye nefayela elinomusho wokungena (passphrase). Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` noma `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | I-`DES`, `AES` (emisiwe), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` kanye nefayela elinomusho wokungena (passphrase). Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` noma `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Bhala futhi ne-snapshot enenguqulo ye-`hostcensus diff`. |
| `--tls-ca-file PATH` | Qinisekisa izitifiketi ze-HTTPS ngokuqhathanisa naleli qoqo le-PEM esikhundleni sesitolo sesistimu. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Ngokumisiwe, i-host ngayinye ihlolelwa i-SSH (TCP 22), i-SNMP (UDP 161), i-MySQL (TCP 3306), i-HTTP (TCP 80) ne-HTTPS (TCP 443). Amachweba e-TCP ahlolwa ngokuxhumana okugcwele. I-SNMP ihlolwa ngesicelo sokutholwa kwe-injini ye-SNMPv3, noma iyiphi i-ejenti ye-SNMPv3 okufanele isiphendule ngaphandle kweziqinisekiso; ama-ejenti akhuluma i-v1/v2c kuphela ngeke atholwe yile probe. Nge-backend ye-asyncio i-host ibalwa njengephilayo uma noma iyiphi i-probe ithola impendulo, okuhlanganisa nokuxhumana okunqatshiwe, ngakho i-host eyehlisa yonke i-probe iba ne-`alive=false` nephutha elithi "Host is down"; lokhu akufakazeli ukuthi icishiwe ngempela. Nge-`--backend nmap`, i-nmap inquma ukuthi yimaphi ama-host aphilayo (i-ICMP njenge-root, i-TCP 80/443 ngenye indlela).

<a name="fingerprints"></a>

### Izigxivizo zamasevisi

Isevisi ngayinye evuliwe ithola isigxivizo ngalokho ekuthumelayo ngaphambi kwanoma yikuphi ukungena ngemvume. Akukho okuqinisekisa ukungena ngaphandle kombuzo we-SNMP, futhi kuphela uma unikeza iziqinisekiso.

| I-probe | Ifunda | `version` | Okhiye be-`details` |
| --- | --- | --- | --- |
| `ssh` | Umugqa wokuhlonza we-RFC 4253 | isofthiwe, isib. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Ukuxhawulana kokuqala kwe-MySQL/MariaDB | inguqulo yeseva | `server_version`, `flavor`, `auth_plugin`, noma `error_code`/`error` |
| `http` | Impendulo ye-`HEAD /` | I-header ye-`Server` | `status`, `server` |
| `https` | Ukuxhawulana kwe-TLS, isitifiketi, i-`HEAD /` | I-header ye-`Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Ukutholwa kwe-SNMPv3; ngeziqinisekiso, i-GET ye-sysDescr, sysObjectID, sysName | i-sysDescr | `engine_id`; ngeziqinisekiso `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, noma `snmp_error` |

Inhloso eyigama le-host ixazululwa kanye ku-host ngayinye futhi yonke i-probe ixhuma kulelo kheli, elibhalwa njenge-`address` emiphumeleni; igama lisetshenziselwa kuphela i-TLS SNI, ukuqinisekiswa kwesitifiketi ne-header ye-HTTP ethi `Host`. Igama elingaxazululeki linikeza izimo ezithi `unknown` nephutha elithi `Cannot resolve`. Amagama e-reverse DNS agcinwa kuphela uma equkethe izinhlamvu zegama le-host, futhi okungenakweqa ukusesha okungu-16 okugijima ngesikhathi esisodwa. I-HTTPS isebenzisa ukuqinisekiswa kwesitifiketi negama le-host kuqhathaniswa nesitolo sesistimu noma i-`--tls-ca-file`. Isitolo sokwethenjwa silayishwa kanye ekuskeneni bese sisetshenziswa kabusha kuyo yonke i-probe ye-HTTPS. Ukuxhumana kwe-TCP nokuxhawulana kwe-TLS kulinganiswa isikhathi ngokwehlukana, ngakho ichweba elamukela ukuxhumana kodwa elibambezela ukuxhawulana liba yi-`open` ne-`tls_error`, hhayi `filtered`. Uma ukuqinisekiswa kwehluleka, umphumela ubhala i-`cert_verified: false` ne-`cert_verify_error`; awuzami futhi ngezilungiselelo ezibuthaka noma uthumele isicelo se-HTTP. Imininingwane yesitifiketi nama-header e-HTTP kuqoqwa kuphela ngemva kokuba ukuqinisekiswa kuphumelele. Nikeza iqoqo le-CA elifanele lamasevisi e-CA yangasese. Imibiko emidala ingaqukatha i-`cert_read_unverified`, ama-probe amanje angasayikhiqizi.

Izimfihlo ze-SNMP zifundwa kuphela eziguquguqukini zendawo noma emafayeleni (`--snmp-*-file`, noma isiguquguquki esihambisanayo se-`HOSTCENSUS_SNMP_*_FILE`), hhayi emananini emugqa wemiyalo, abanye abasebenzisi bendawo abangawabona ohlwini lwezinqubo. I-`--snmp-community`, i-`--snmp-auth-key` ne-`--snmp-priv-key` ezinamanani ziphuma ngekhodi 2 futhi ziqambe okuzithathayo indawo. Ifayela lemfihlo kufanele kube i-UTF-8 equkethe okuthile enobukhulu obungeke buweqe ama-byte angu-4096; umugqa omusha owodwa ekugcineni awunakwa, futhi ukusetha kokubili isiguquguquki nefayela lemfihlo efanayo kuyiphutha. Amaphutha aqamba igama lefayela kodwa awaphrinti okuqukethwe kwalo. Imibiko yokuskena nomlando akufaki ngamabomu amanani eziqinisekiso. Isithumeli (exporter) sinenketho ehlukile, ecacile ethi `--include-credentials` echazwe ngezansi. I-community ikhetha i-SNMPv2c; umsebenzisi ukhetha i-SNMPv3, enokuqinisekisa uma kunikezwe ukhiye wokuqinisekisa (auth key) nobumfihlo uma kunikezwe bobabili okhiye (i-`snmp_security_level` ibhala ukuthi yikuphi). I-hostcensus iyala, ngekhodi yokuphuma engu-2, ukuhlanganisa i-community nomsebenzisi we-v3, ukusebenzisa ukhiye wobumfihlo ngaphandle kokhiye wokuqinisekisa, noma ukusebenzisa okhiye ngaphandle komsebenzisi, futhi ayikaze izame kabusha umbuzo we-v3 ohlulekile nge-v2c noma ngezinga eliphansi lokuphepha. Ama-ejenti akhuluma i-v1/v2c kuphela awanaki ukutholwa kwe-v3 okungenaziqinisekiso, ngakho avela njengavuliwe kuphela uma kunikezwe i-community.

Umbhalo we-banner uncishiselwa ezinhlamvwini eziphrintekayo futhi unikwe umkhawulo wezinhlamvu ezingu-256 ngaphambi kokuba ugcinwe noma uboniswe. Ukufunda nakho kunomkhawulo: ama-4 KiB ngomugqa, ama-4 KiB omkhonzo we-MySQL, ama-16 KiB ama-header e-HTTP. I-SNMP engine ID ende kunezingxenye ezingu-32 (octets) iyancishiswa ngaphambi kokuba igcinwe. I-HTTP ne-HTTPS zithumela i-header ye-Host enekheli le-IPv6 phakathi kwabakaki kanye nechweba uma kungewona u-80 noma u-443. Amaseli e-CSV aqala ngophawu oluvusa ifomula yesipredishithi afakelwa isiqalo ukuze iseli lihlale liwumbhalo.

### Imikhawulo

Ukugijima okukodwa kwamukela amakheli angangeqi ku-65,536, amasevisi angu-64, nama-probe angu-524,288 (ama-host aphindaphindwe ngamasevisi); izicelo ezinkulu kunalokhu ziphuma ngekhodi 2 ngaphambi kokuba kuthunyelwe lutho. I-`--concurrency` inomkhawulo wama-socket angu-4096. I-probe ngayinye inomnqamulajuqu oqinile ophindwe kane esikhathini sayo esibekiwe. Ama-probe okuxhuma (`tcp`, `ssh`, `mysql`, `http`) asebenzisa imizuzwana engu-0.3 ngaphandle uma leyo sevisi ibeka i-`timeout`. I-SNMP ne-HTTPS zisebenzisa i-`--timeout` (okumisiwe ngu-1.0) uma zingayibekile eyazo. I-probe efinyelela kumnqamulajuqu ibikwa njenge-`unknown` enombhalo othi "probe timed out" ku-`errors`. Ukwehluleka kwama-socket endawo (isibonelo ukuphelelwa ama-file descriptor) nakho kuba yi-`unknown` nephutha elibhaliwe; akukaze kubalwe njengechweba elihlungiwe noma i-host ecishiwe. Ngaphambi kokuhlola, i-hostcensus ikhuphula umkhawulo othambile wamafayela avuliwe iwusondeze kumkhawulo oqinile ukuze kulingane i-`--concurrency` kanye nama-descriptor angu-64; uma ingakwazi, ukuhlola kwangaphambili kwe-`open files` kuyehluleka futhi i-`scan` iphuma ngekhodi 1 ngaphambi kokuthumela ithrafikhi. Ukutholwa nge-Nmap kusebenzisa isikhathi sokuphela se-host esiyimizuzwana engu-30. I-prefix idluliselwa ku-nmap ngendlela ye-CIDR, futhi i-sweep iyehluleka iphume ngekhodi 1 uma i-nmap ibika amakheli ambalwa kunalawo eyawanikezwa (isibonelo igama engakwazi ukulixazulula) kunokuba iphawule ama-host njengacishiwe. Inhloso eyigama le-host ixazululwa kanye bese i-nmap inikezwa lelo kheli, ukuze ukutholwa nama-probe kufinyelele emshinini ofanayo. I-prefix ephelele iyinqubo eyodwa ye-nmap enomnqamulajuqu we-subprocess oyimizuzwana engu-35 kuwo wonke amakheli angu-256, kusongelelwe phezulu. Ama-sweep anokukhishiwe asebenzisa amaqoqo ama-host angu-256 nomnqamulajuqu oyimizuzwana engu-35 eqoqweni ngalinye. Ukwakhiwa kwezisebenzi kunomkhawulo ongancikile kusayizi webanga. I-reverse DNS nokuxazululwa kwegama le-host kunomnqamulajuqu ohlukile oyimizuzwana emibili; ukubizwa kwe-resolver okungabuyi kuyashiywa ku-thread yako, ukuze kungagcini i-hostcensus igijima ngale kwale mikhawulo. Ukusesha okungeke kweqe ku-16 kugijima ngesikhathi esisodwa, futhi ukubizwa okushiywe phansi kugcina isikhala sako kuze kubuye, ngakho inani lama-thread abambekile lihlala linomkhawulo; uma wonke angu-16 ebambeka, ukusesha okulandelayo kulinda kulayini wesikhala ngaphandle komnqamulajuqu wemizuzwana emibili (oqala lapho isikhala sesivulekile) kuze kube yilapho i-`--deadline` imisa ukuskena. I-`NetworkScanner` esetshenziswa njengelabhulali ngaphandle kwe-`deadline` ingalinda isikhala esinjalo unomphela. I-`--deadline` (okumisiwe yihora elilodwa) ibeka umkhawulo kukho konke ukugijima ngaphezu kwalezi.

### Ukuhlela amasevisi

Amasevisi angashintshwa ngefayela le-TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

I-`probe` ingesinye salezi: `tcp`, `ssh`, `mysql`, `http`, `https` noma `snmp` futhi ibuyela egameni lesevisi uma lokho kuyi-probe, ngaphandle kwalokho iba yi-`tcp`. I-`snmp` kuphela esebenzisa i-UDP. Amagama amasevisi ayizinhlamvu ezincane, izinombolo, i-`-` ne-`_`. Amasevisi amabili awakwazi ukwabelana ngechweba nephrothokholi; umlando ubhala isimo esisodwa salokho kubhangqa. I-`timeout` iyazikhethela, ingemizuzwana, futhi okungenani ingu-0.05. Ama-probe okuxhuma (`tcp`, `ssh`, `mysql`, `http`) abuyela emizuzwaneni engu-0.3. I-`snmp` ne-`https` zisebenzisa i-`--timeout` yokuskena uma isevisi ingabekile i-`timeout`. I-`--timeout` ayisithathi indawo isikhathi isevisi esivele inaso.

Imibiko ye-JSON ingamadokhumenti anezinguqulo (`"format": "hostcensus-report"`, `"version": 1`) abhala inhloso, amasevisi ahloliwe nezilungiselelo eduze kwe-`devices`; i-`--format json` ngaphandle kwe-`-o` ibhala umbiko ku-stdout esikhundleni sethebula. Wonke umphumela we-JSON une-schema eshicilelwe; bona [Umphumela we-JSON](../../../docs/json-output.md). Amadivayisi agcina izinkambu zokuqala ze-`ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` ne-`errors` bese engeza uhlu lwe-`services` nge-`name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, noma `unknown` lapho i-probe yehluleke endaweni noma ifinyelele kumnqamulajuqu wayo), `version` ne-`details` ze-probe ngayinye. Umphumela we-CSV uthola amakholomu okugcina e-`services` ne-`versions` alawo avuliwe. Amanani e-boolean e-`ssh`, `snmp` ne-`mysql` alandela amasevisi analawo magama ngqo.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Amaphrofaili ohlu, ukuhlola kwangaphambili, nomlando wendawo

Amaphrofaili aqanjwe amagama abelana ngefayela le-TOML nezincazelo ezikhona ze-`[services]`. Kopisha
i-[hostcensus.example.toml](../../../hostcensus.example.toml) uyise ku-`hostcensus.toml` bese usetha amanethiwekhi
owalawulayo:

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

I-`preflight` ixazulula izinketho namaphrofaili ngokufana ncamashi ne-`scan`, okuhlanganisa
ne-`--concurrency` yokuhlola amafayela avuliwe, ngakho ukuhlola kwangaphambili okuphumelelayo kusho ukuthi i-`scan`
izoqala ngohlelo olufanayo.

Amaphrofaili amukela i-`network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, ne-`max_hosts`. I-`services` ne-`ports` zisebenzisa indlela ekhona yohlu oluhlukaniswe ngokhefana.
Izinketho ze-CLI ezicacisiwe zidlula izilungiselelo zephrofaili; izinketho ze-`--exclude` eziphindiwe
zingeza kokukhishiwe kwephrofaili. Inethiwekhi ecacisiwe ene-`--profile` kufanele
iqukathwe ngaphakathi kobubanzi be-IP/CIDR baleyo phrofaili. Amagama ama-host asasekelwa ekuskeneni
okuqondile, kodwa awakwazi ukuhlanganiswa nokukhishwa kwe-IP. Imikhawulo yama-host isebenza ngaphambi
kokukhishwa; umkhawulo ophelele wama-probe usasebenza ngemva kwalokho. Ama-host akhishiwe
ayashiywa kokubili ekuhloleni amasevisi nasekutholeni nge-Nmap okungakhethwa.

Konke ukuskena kwenza ukuhlola kwangaphambili kwendawo ngaphambi kwethrafikhi yenhloso: imikhawulo yenhloso/ye-probe,
ukufinyelela endaweni okuyiwa kuyo, ukutholakala kohlelo/kwe-wrapper ye-Nmap okungakhethwa, i-schema yomlando,
neqoqo le-TLS CA elihleliwe. I-`preflight` ibika i-JSON futhi ayiskeni izinhloso noma yakhe isizindalwazi somlando.
Ibhala okwesikhashana ifayela eliseduze ukuze ihlole ukufinyelela endaweni okuyiwa kuyo ngaphandle kokushintsha okuqukethwe okukhona.
I-backend emisiwe ye-asyncio ayidingi i-Nmap noma i-root. Izindlela zezindawo okuyiwa kuzo kufanele zehluke kwezinye
nakukuhlelwa okufakiwe, okuhlanganisa nama-hard link; ama-symlink endawo okuyiwa kuyo ayaliwa.
Ukuhlola okuhlulekile kubuyisa u-1; ububanzi/ukuhlelwa okungavumelekile kubuyisa u-2.

Ukubhalwa kwemibiko nokuthunyelwa kudinga ukusekelwa kwe-`O_NOFOLLOW`. Kuzinhlelo ezinganakho,
okuhlanganisa ne-Windows, lokhu kubhala kuyehluleka ngaphandle kokuvula noma ukunciphisa indawo okuyiwa kuyo.
Imibiko emisha nezikripthi zokuthumela zakhelwa umnikazi kuphela (imodi 0600); ukushintsha ifayela elikhona kugcina
izimvume zalo. Ukubhala ku-named pipe engenamfundi kuyehluleka ngaso leso sikhathi kunokulinda. Isizindalwazi esisha se-`--history`
naso sakhiwa singesomnikazi kuphela; esikhona sigcina imodi yaso. Imilayezo yamalogi ihlezi iya ku-stderr, ukuze i-stdout ithwale imiphumela kuphela. Ukuthunyelwa okuqukethe iziqinisekiso kuhlezi kuphoqa imodi 0600.

Umlando uyazikhethela futhi uhambisana nama-snapshot e-JSON akhona nomyalo we-`diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Sebenzisa ama-ID avela ku-`history`; isibonelo sicabanga ngesizindalwazi esisha. Ama-snapshot agcinwa
ngama-transaction nezikhathi zokuqala/zokuphela ze-UTC, inguqulo yephakheji, izilungiselelo ezisebenzayo ezingeyona imfihlo,
izifinyezo, nakho konke okutholakele kwama-host/amasevisi, okuhlanganisa namaphutha e-host ngayinye.
Okutholakele kwama-host okungaphelele kuyagcinwa. Ukugijima okukhanseliwe akugcinwa. Izivumelwano ezikhona
zombiko, ze-snapshot, zokuthumela, namakhodi okuphuma okuskena ziyagcinwa.

I-`history` ibala izifinyezo ze-JSON ngaphandle kokufunda wonke ama-payload amadivayisi omlando.
I-`compare` ifunda izikeni ezimbili ezigciniwe, idinga ubunikazi benhloso obufanayo namachweba akhethiwe,
bese ibika ukusabela, isimo, nezinguquko zesimo samachweba. I-ID yokuskena kwangaphambili
kufanele yandulele i-ID yakamuva. Uma zombili izikeni zibhale i-`timeout` noma i-`backend`
futhi lawo manani ehluka, umbiko ubhala isixwayiso bese uqhubeka uqhathanisa okutholakele.
Ukulinda okuhlukile kungenza ichweba elihlungiwe libonakale livuliwe. Amaphutha esikena
nokutholakele kwamachweba angaziwa kuphawulwa njengokungaqinisekile kunokuba kuphathwe njengokunyamalala
noma ukuvalwa okuqinisekisiwe: ama-host anamaphutha avela ku-`uncertain_hosts`, futhi
lonke ushintsho lwechweba oluhilela i-`unknown` (okuhlanganisa okungaziwa kuzo zombili izikeni) lubalwa
ku-`unconfirmed_ports` esikhundleni se-`port_changes`, ngaphandle kwechweba elivuliwe ekuskeneni
kwakamuva, okuwushintsho lwechweba. I-`compare` ne-`diff` zihlukanisa amachweba ngomthetho ofanayo.
I-`no_longer_responding` isho ukungabi nampendulo, hhayi ubufakazi bokususwa kwedivayisi.
Ikhodi yokuphuma yokuskena engu-0 ayiqinisekisi ukuthi wonke ama-host aphendulile: hlola amaphutha e-host ngayinye. Impumelelo yokuqhathanisa ibuyisa u-0 kungakhathaliseki ukuthi kunezinguquko noma cha; i-`diff` yefayela ekhona
igcina isivumelwano sayo sekhodi yokuphuma engu-3. Umlando ongasekelwa noma owonakele ubuyisa u-1.

Umlando ugcina ulwazi lohlu, ngakho khetha uhla lwemibhalo lwendawo oluvikelwe ngokufanele.
Amafayela amaphrofaili nezilungiselelo ezigciniwe aziqukethe iziqinisekiso ze-SNMP;
ukuphathwa kweziqinisekiso kuqhubeka ngezinketho/ngendawo yokusebenza ekhona.

<a name="inventory-diff"></a>

## Ukuqhathanisa uhlu (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

I-snapshot iyi-JSON ene-`format: "hostcensus-snapshot"`, `version: 1`, inguqulo ye-hostcensus, isikhathi sokwakhiwa kwe-UTC, inhloso, i-`timeout` ne-`backend` yokuskena uma ukuskena kuzibhalile, amasevisi ahloliwe, nama-host aphilayo ngendlela efanayo nombiko we-`-o`. Ama-host acishiwe ayashiywa. I-`diff` iphinde yamukele imibiko ye-JSON ejwayelekile ye-`scan -o`, okuhlanganisa neyaphambi kokuba insimu ye-`services` ibe khona.

I-`diff` ibika ama-host amasha nanyamalele, amachweba avulekile noma avalekile kuma-host akhona kuzo zombili, namasevisi ane-`version` eshintshile. Amachweba ahlolwe kwesinye kuphela salezi zikeni ezimbili awaqhathaniswa, futhi isixwayiso siyasho lokho. Ukuhlola okuhlulekile akukaze kufundwe njengokuthi "azikho izinguquko": ichweba eliyi-`unknown` kunoma yisiphi isikeni futhi elingavuliwe kwesakamuva libalwa ngaphansi kwe-`unconfirmed`, hhayi i-`closed`, line-`before` eyi-`open`, `unknown` noma `not-open` (lihloliwe futhi livaliwe noma lihlungiwe) kanye ne-`after` eyi-`unknown` noma `not-open`; ichweba elivuliwe manje libikwa ngaphansi kwe-`opened` ngisho noma i-probe yangaphambili yehlulekile. I-host enama-probe wonke ehlulekile ngaphandle kwempendulo kunoma yisiphi isikeni ibalwa ngaphansi kwe-`unsettled_hosts` (ine-`before`/`after` eyi-`up`, `uncertain` noma `absent`, okuhlanganisa nalapho yehluleke kuzo zombili izikeni noma ingekho kwelinye ifayela) esikhundleni se-`vanished_hosts`; uma iphendula ekuskeneni kwakamuva iphinde ibikwe njenge-host entsha namachweba ayo avuliwe. Ama-snapshot agcina lawo ma-host ahlulekile ngenxa yalesi sizathu. Isixwayiso siphinde sivele uma izinhloso zehluka, nalapho womabili amafayela ebhale i-timeout noma i-backend futhi lawo manani ehluka. I-`-o PATH` ibhala ifomu le-JSON efayeleni nayo.

Umbiko ovela ekuskeneni okumisiwe yi-`--deadline` (`"complete": false`) ubala kuphela ama-host okufinyelelwe kuwo, ngakho i-`diff` ne-`export` ziyawala ngekhodi yokuphuma engu-2. I-`--allow-partial` iyawamukela ngesixwayiso ku-stderr: i-`diff` ibe isibala ama-host isikeni esingaphelele esingawabhalanga nhlobo ngaphansi kwe-`unsettled_hosts` njenge-`unscanned` esikhundleni sokunyamalala (i-host esiyibhale njengecishiwe isabalwa njengenyamalele), isetha i-`partial` ibe ngu-true futhi ayikaze ibike ukuthi azikho izinguquko, kanti i-`export` ibhala isixwayiso esihlokweni sesikripthi.

Amakhodi okuphuma e-`diff`: `0` azikho izinguquko, `3` izinguquko ezitholakele, okutholakele okungakwazanga ukuqinisekiswa, noma okufakiwe okungaphelele (i-`changed` iba ngu-true noma nini lapho noma yiluphi uhlu, okuhlanganisa i-`unsettled_hosts` ne-`unconfirmed`, luqukethe okuthile, noma i-`partial` ingu-true), `2` ifayela alikho, alifundeki, aliyona i-snapshot esekelwayo, noma aliphelele ngaphandle kwe-`--allow-partial`, `1` ifayela le-`-o` alikwazanga ukubhalwa.

<a name="kadupul-export"></a>

## Ukuthumela ku-Kadupul

I-[Kadupul](https://github.com/kadupulhq/kadupul) (i-fork ye-Cacti 1.2.31) ayinakho ukungeniswa kwefayela lamadivayisi ngobuningi. Indlela yayo esekelwayo yokwengeza amadivayisi ngokusebenzisa iskripthi iyi-`cli/add_device.php`, idivayisi eyodwa ngokubizwa ngakunye, ngezimpikiswano ze-`--option=value`. I-`hostcensus export` ibhala iskripthi se-POSIX `sh` salezo zibizo:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

I-host ngayinye ephilayo iba yi-`php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Ama-host lapho umbuzo we-SNMP wokuskena uphumelele khona athola i-`--version=2 --community=...` noma i-`--version=3 --username=... --authproto=... --password=...` (kanye ne-`--privproto`/`--privpass` ye-authPriv), i-`--port` ne-`--avail=snmp`. Ukuthunyelwa kwe-SNMPv3 kudinga i-`--snmp-user`, futhi i-noAuthNoPriv iyaliwa ngoba i-`add_device.php` idinga iphasiwedi ye-v3.
- Amanye ama-host athola i-`--version=0 --avail=ping`, ne-`--ping_method=tcp --ping_port=` okuba ichweba lokuqala le-TCP elivuliwe, noma i-ICMP uma lingekho.
- I-`--notes` ibala amasevisi avuliwe nezinguqulo zawo. I-`--description` iba igama le-reverse-DNS uma lilula (izinhlamvu, izinombolo, `.`, `_`, `-`), ngaphandle kwalokho iba yi-IP, futhi yenziwa ihluke, ngoba i-`add_device.php` iphatha incazelo ekhona njengokubuyekezwa kwaleyo divayisi.

Lonke inani liyaqinisekiswa futhi lifakwe izingcaphuno ze-shell nge-`shlex.quote`. Ngokumisiwe akukho mfihlo ye-SNMP ebhalwayo: iskripthi sinweba i-`HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` noma `HOSTCENSUS_SNMP_PRIV_KEY` ngesikhathi sokugijima bese siyama uma esisodwa singasethiwe. I-`--include-credentials` ibhala amanani asuka kulezo ziguquguquki zendawo eskripthini esikhundleni salokho, isakhe ngemodi 0600, futhi ibhale isixwayiso. I-`add_device.php` ngokwayo iphrinta i-community futhi ithola izimfihlo njengezimpikiswano, ezibonakala ohlwini lwezinqubo lweseva ye-Kadupul ngenkathi ukubizwa ngakunye kugijima.

I-`add_device.php` iphuma ngekhodi 1 kokuphindiwe namaphutha; iskripthi siyaqhubeka, sibale okuhlulekile, bese siphuma ngekhodi 1 uma noma iyiphi idivayisi ingengezwanga. Ama-ID ezifanekiso (template) avela ku-`php cli/add_device.php --list-host-templates`. Amakhodi okuphuma e-`export`: `0` ibhaliwe, `2` okufakiwe okungafundeki, ukuskena okungaphelele ngaphandle kwe-`--allow-partial`, noma idatha engakwazi ukuthunyelwa ngokuphepha, `1` iskripthi asikwazanga ukubhalwa.

## Ukuhlelwa kwezinguqulo nenqubo yokukhishwa

I-hostcensus ilandela i-[Semantic Versioning](https://semver.org/spec/v2.0.0.html): ukulungiswa okuhambisanayo
kukhuphula inguqulo ye-patch, izici ezihambisanayo/ukuyekwa kukhuphula inguqulo
encane (minor), kanti izinguquko eziphula ukuhambisana zikhuphula inguqulo enkulu (major).
Imiyalo nezinketho, amakhodi okuphuma nama-JSON schema yisivumelwano somphakathi;
ukuziphatha okuyekiwe kuqhubeka kusebenza kuze kube sekukhishweni okukhulu okulandelayo, ngaphandle uma
ukulungiswa kokuphepha kudinga ukukushintsha ngokushesha (uhlu lwezinguquko lube seluchaza ukuthi kungani).

I-release-please ivula i-PR yokukhishwa kusuka ezihlokweni ze-Conventional Commit ku-`main`,
ikhuphule i-`pyproject.toml`, i-`uv.lock` ne-`CHANGES.md`. Ukuyihlanganisa kwakha
ithegi ye-`vMAJOR.MINOR.PATCH` kanye nohlaka lokukhishwa ku-GitHub, lapho i-CI inamathisela khona
i-wheel ehloliwe, ukusabalalisa kwekhodi yomthombo nama-checksum; i-GitHub igcina iziqinisekiso zokwakha
zalawo mafayela nge-API yayo yeziqinisekiso. Umphathi uyabuyekeza bese eshicilela
uhlaka uma amafayela esenamathiselwe. Ukukhishwa akukaze kushintshwe ngokunye.

Ukushicilela okuthenjwayo ku-PyPI kuyazikhethela futhi kudinga ubunikazi bephrojekthi, umshicileli
othenjwayo nendawo ye-`pypi`. Kushicilela ama-artifact okukhishwa ahloliwe afanayo
ngaphandle kokwakha kabusha noma ukugcina i-token ye-API. Ukukhishwa okunamathegi kule ndawo yokugcina
yomphakathi kukhiqiza iziqinisekiso zama-artifact ze-GitHub; ama-fork angasese adinga uhlelo olusekelwayo
nokukhetha okucacile. Bona
[umhlahlandlela ophelele wokukhishwa](../../../docs/releasing.md) ukuze uthole ukusethwa, imiyalo eqondile nokuzama kabusha.

## Ukuthuthukiswa

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Amathuluzi okuthuthukisa ahlala emaqoqweni ezincike e-[PEP 735](https://peps.python.org/pep-0735/)
ku-`pyproject.toml` (`dev`, `fuzz`, `build`), ngakho awaveli kumethadatha yephakheji
eshicilelwe. I-`uv.lock` iyifayela lokukhiya elilodwa; i-CI ifaka nge-`uv sync --locked`
futhi iyehluleka uma ifayela lokukhiya selidala. Khetha umhumushi nge-`uv python`,
i-mise (`mise exec python@3.14 -- uv sync --locked`), noma iyiphi i-Python 3.12+.

I-CI iphoqelela ubuncane bokumbozwa kwephakheji obungu-90%. Ukuhlolwa kweyunithi kuhlanganisa amaseva
e-loopback alawulwayo nezimo ezingaxhunyiwe ku-inthanethi zamaphrofaili/zomlando/zokuqinisekisa ukukhishwa; ilabhoratri ye-Compose igijima
i-OpenSSH, i-MariaDB, i-nginx ne-net-snmp kubhuloho elihlukanisiwe. Yigijimise nge-`make test-integration`.
Bona i-[CONTRIBUTING.md](../../../CONTRIBUTING.md) kanye [namathuluzi okukhishwa](../../../scripts/README.md).

I-container yokusebenza igijima njenge-UID/GID 10001 engenalo uhla lwemibhalo lwasekhaya, engenakho ukungena
kwe-shell futhi engenayo i-pip, futhi ingabhala ku-`/app/output`. Nikeza lowo msebenzisi imvume yokubhala
kunoma yiluphi uhla lwemibhalo lomphumela olufakiwe (mounted). Ayidingi ama-capability futhi isebenza
ngesistimu yamafayela yezimpande yokufunda kuphela, ngakho ingagijima njengokuthi:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

I-Nmap isebenzisa indlela yayo yokutholwa kwe-TCP engenamalungelo akhethekile kule container. I-CI yehluleka
ukwakha isithombe kunoma yibuphi ubuthakathaka be-HIGH noma be-CRITICAL obulungisekayo obubikwa yi-Trivy.

## Ukuhlolwa kwe-supply-chain

I-[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
igijima ku-main nakuviki ngalinye, ishicilele amaphuzu ayo angempela, futhi ilayishe okutholakele ekuskeneni
kwekhodi ku-GitHub. Ama-Action nezisekelo ze-container ziboshwe ngama-hash angaguquki; izincike ze-Python
zixazululwa ku-`uv.lock`. Ukwehluleka kwe-Bandit kwenza i-CI yehluleke, futhi i-fuzzing ye-Atheris enomkhawulo
ihlola abahlaziyi be-SSH, i-MySQL, i-HTTP, izitifiketi ne-SNMPv3 BER ngaphandle kokufinyelela kunethiwekhi.

I-Scorecard iphinde ilinganise umsebenzi wokubuyekeza womlando, ukuhlukahluka kwabanikeli, kanye
nomsuka wokukhishwa. Lawo maphuzu abonisa ubufakazi bangempela; akuzona izimangalo zokuthi
konke ukuhlolwa kokubusa noma kokukhishwa komlando kwanelisiwe. Bona
i-[SECURITY.md](../../../SECURITY.md) kanye [nomsuka wokukhishwa](../../../docs/releasing.md).

## Ukwenza ngokwasendaweni (izilimi)

Imilayezo ye-CLI namathebula ezifinyezo/okuqhathanisa e-terminal asekela izilimi zezindawo ezingu-45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ngaphandle kwezincike zokusebenza ezengeziwe. Ukuxazulula kuhlonipha i-`--lang`, bese kuba yi-`LC_ALL`, `LC_MESSAGES`, ne-`LANG`, kubuyele ku-`en`. Ama-JSON schema, amakholomu e-CSV, nezikripthi zokuthumela kuhlala kungashintshile kuzo zonke izilimi.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Ukunikela

Iminikelo kufanele ifake isimo esiphindekayo, igcine izivumelwano ezibhaliwe ze-CLI nezefomethi yedatha,
futhi iphumelele ekuhloleni kwekhwalithi okungenhla. Bona
i-[CONTRIBUTING.md](../../../CONTRIBUTING.md) ukuze uthole inqubo yokuthuthukisa kanye
[nomhlahlandlela wokukhishwa](../../../docs/releasing.md) ngezinqumo zokuhambisana nezinguqulo.

## Isimo sokuphepha nelayisensi

Bona i-[SECURITY.md](../../../SECURITY.md) ukuze uthole ukubika okuyimfihlo nezinguqulo ezisekelwayo.
I-hostcensus inelayisensi ngaphansi kwe-[MIT License](../../../LICENSE).

Ama-header ekhodi yomthombo asebenzisa izihlonzi ze-SPDX futhi agcina ukwaziswa kwabanikeli okuvela emlandweni
we-Git. Bona i-[AUTHORS.md](../../../AUTHORS.md) ukuze uthole ukwaziswa kwabanikeli. Ukuthwetshulwa kokuhlolwa okuyi-binary
nefayela lokukhiya elikhiqiziwe kusebenzisa amafayela e-`.license` aseduze; umbhalo we-MIT uku-`LICENSES/MIT.txt`.
