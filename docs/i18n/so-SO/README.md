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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · **Soomaali** · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus waa aalad khadka amarka (CLI) ee Python ah oo loogu talagalay tira-koobka adeegyada ee lagu celcelin karo shabakadaha aad maamusho. Waxay diwaangelisaa waxa qalabyadu muujiyaan, waxay isbarbardhigtaa natiijooyinka la helay muddo ka dib, waxayna soo saartaa qoraallada gelinta ee Kadupul. Habka dambe ee caadiga ah wuxuu adeegsadaa godadka asyncio isagoon u baahnayn awoodda root; baaritaanka Nmap ee ikhtiyaariga ah wuxuu aqoonsan karaa martigeliyeyaasha ka baxsan dekedaha adeegyada ee habaysan.

## Sababta loo doorto hostcensus

Warbixin hal mar ah oo dekedaha ku saabsan ma sharraxdo haddii baaritaanka xiga uu wax iska beddelay ama uu si fudud u fashilmay. hostcensus waxay isku darsataa xaalado adeeg oo cad, tijaabooyin xadidan, borofayllo baaris oo dib loo adeegsan karo, iyo taariikh maxalli ah. Hawlwadeennadu waxay ku celcelin karaan isla xadka baaritaanka, way baari karaan qaladaadka, waxayna kala saari karaan natiijooyinka aan la hubin iyo isbeddellada la xaqiijiyay.

- **Caddaynta adeegyada:** aqoonsiga SSH, salaanta bilowga ee MySQL, madaxyada HTTP, hubinta shahaadooyinka TLS, iyo baaritaanka SNMP ama weydiimaha system-MIB ee leh aqoonsi sir ah.
- **Xad baaris oo lagu celcelin karo:** borofayllo TOML oo magacaaban, ka-reebisyo lagu dari karo, adeegyo la habayn karo, xadadka martigeliyeyaasha iyo tijaabooyinka, iyo shaqaale hawleed oo xadidan.
- **Hubin ka hor inta aan xog shabakad la dirin:** hubinta hordhaca ah ee maxalliga ah waxay xaqiijisaa bartilmaameedyada, aaladaha, gelitaanka meesha lagu qorayo, qaab-dhismeedka taariikhda, iyo xirmooyinka TLS CA ee habaysan.
- **Taariikhda tira-koobka:** nuqul-xilliyeedyada SQLite ee habka transactional waxay kaydiyaan dhammaan natiijooyinka la helay; isbarbardhigyadu waxay si muuqata u ilaaliyaan guul-darrooyinka baaraha iyo xaaladaha aan la garanayn.
- **Natiijooyin la isku xiri karo:** warbixinnada terminal, JSON iyo CSV, nuqul-xilliyeedyada faylasha ee noocaysan, iyo qoraallada gelinta ee Kadupul.

CI wuxuu daboolaa Python 3.12, 3.13 iyo 3.14 ee Linux iyo macOS, iyadoo ay weheliso shaybaar isku-dhafan oo Compose ah oo la xakameeyo. Koodhku wuxuu adeegsadaa magacyada noocyada casriga ah, natiijooyinka hubinta hordhaca ah ee noocaysan, borofayllo keyword-only oo slotted ah, iyo nadiifin async ah oo habaysan iyadoo la ilaalinayo noocyadaas runtime-ka. Eeg [Noocaynta iyo sii-daynta](../../../docs/releasing.md) si aad u aragto heshiiska is-waafajinta SemVer iyo habka sii-daynta GitHub. Calaamaddu (release badge) waxay sharraxdaa agabka la daabacay, ma aha nuqulka kaydka: sumadda ugu dambeysay ee la daabacay hadda waa `v0.3.0`, halka nuqulkan kaydku uu adeegsado nooca xirmada `3.0.0`. Ka rakib nuqulka kaydka si aad u isticmaasho astaamaha tira-koobka ee halkan lagu sharraxay.

Ka bilow [rakibaadda](#install), ka dibna [borofayllada iyo taariikhda](#inventory-profiles-preflight-and-local-history). Faahfaahinta isku-xirka, eeg [aqoonsiga adeegyada](#fingerprints), [isbarbardhigga faylasha](#inventory-diff), iyo [dhoofinta Kadupul](#kadupul-export).

## Rakibaadda

Waxaa loo baahan yahay Python 3.12 ama ka cusub; Python 3.12-3.14 waa noocyada la tijaabiyay. Nuqulkan kaydka ka rakib xirmooyinka runtime-ka ee qufulan:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Baaritaanka martigeliyaha Nmap ee ikhtiyaariga ah, ku rakib barnaamijka Nmap adigoo adeegsanaya maareeyaha xirmooyinka ee nidaamkaaga; looma baahna xirmo Python oo dheeraad ah. Natiijada XML ee Nmap waxaa lagu farsameeyaa defusedxml, oo ah ku-tiirsanaan aasaasi ah, sidaas darteed ballaarinta entity waa la diidaa. hostcensus waxay si toos ah u socodsiisaa `nmap` ee laga helo `PATH` iyadoo adeegsanaysa liis doodo ah oo go'an, xad waqti oo la kora cabbirka horgalaha (prefix), iyo xad natiijo oo ah 64 MiB. Nmap looma baahna habka dambe ee caadiga ah.

## Ka-guurista netprobe

hostcensus waa magaca cusub ee netprobe, oo lagu soo saaray nooca 3.0.0. Mashruuca waligiis laguma daabicin PyPI midkoodna labada magac, markaa rakibaaduhu waxay ka yimaadeen nuqulka kaydka ama sii-daynta GitHub. Kaydka GitHub wuxuu haystaa magaciisa.

| Wuxuu ahaa | Hadda | Is-waafajinta |
| --- | --- | --- |
| Qaybinta `netprobe` | `hostcensus` | Dib uga rakib nuqulka kaydka; ma jirto xirmo magaca hore leh. |
| Amarka `netprobe` | `hostcensus` | `netprobe` weli wuu shaqeeyaa wuxuuna daabacaa hal sadar oo digniin ka-bixis ah oo ku qoran stderr. Koodhadhka bixitaanka iyo stdout isma beddelin. Waxaa laga saari doonaa sii-daynta weyn ee xigta. |
| Doorsoomayaasha deegaanka `NETPROBE_*` | `HOSTCENSUS_*` | Doorsoome `NETPROBE_*` ah ayaa la adeegsadaa marka mataankiisa `HOSTCENSUS_*` uusan dejisnayn, iyadoo la bixinayo hal digniin oo stderr ah oo sheegaysa magacyada doorsoomayaasha balse aan marnaba daabicin qiimahooda. `HOSTCENSUS_*` ayaa guulaysta marka labadaba la dejiyo. Waxaa laga saari doonaa sii-daynta weyn ee xigta. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Isbeddel jabinaya is-waafajinta.** Ma jiro shim soo-gelin ah oo la rakibay; cusbooneysii soo-gelinta (imports). |
| Sumadda sawirka Docker `network-discovery:test` (CI oo keliya) iyo isticmaalaha konteenarka `netprobe` | `hostcensus:test`, isticmaalaha `hostcensus` | Waligii laguma daabicin sawir diiwaanka (registry). Dib u dhis sawirka oo isticmaal barta laga galo ee `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Fayl hore u jiray oo wata magaca caadiga ah ee hore weli waa la adeegsadaa, iyadoo digniin la bixinayo, inta uusan magaca cusub jirin. Waddooyinka `--config` iyo `--history` ee si cad loo sheegay lama taaban. |
| Warbixinnada iyo nuqul-xilliyeedyada leh `"format": "netprobe-report"` ama `"netprobe-snapshot"`, iyo goobta `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` iyo `export` weli waxay akhriyaan faylasha lagu qoray magaca hore, qaab-dhismeedyada JSON Schemas ee la daabacayna waxay aqbalaan labada higgaad. Faylasha cusub waxay adeegsadaan magacyada cusub. Kaydadka taariikhda SQLite isma beddelin waxayna u furmaan sidii hore. |
| Qoraallada Kadupul ee ka yimid `netprobe export` | Qoraallada ka yimid `hostcensus export` | Qoraalladii hore way sii shaqeeyaan waxayna weli akhriyaan `NETPROBE_SNMP_*` marka la socodsiiyo. Qoraallada cusub waxay akhriyaan `HOSTCENSUS_SNMP_*`. |

## Tusaale degdeg ah

Waxaa laga socodsiiyay konteenarka tijaabada ee shaybaarka isku-dhafan ee lagu sharraxay qaybta Horumarinta; natiijada waa la soo koobay:

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

## Koodhadhka bixitaanka

| Amar | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | natiijooyinka/warbixinta waa la diwaangeliyay | hubinta hordhaca ah/habka dambe, taariikhda, ama qorista warbixinta/nuqul-xilliyeedka ayaa fashilantay | bartilmaameed, ikhtiyaarro, habayn, ama xadad aan sax ahayn | - | `--deadline` waa la gaaray; warbixin qayb ah ayaa la qoray, taariikhda iyo nuqul-xilliyeedka waa laga booday |
| `preflight` | hubinta waa lagu guulaystay | hubinta maxalliga ah way fashilantay | bartilmaameed/habayn aan sax ahayn ama meelo lagu qorayo oo iska hor imaanaya | - | - |
| `profiles` | borofayllada la xaqiijiyay waa la taxay | - | habayn ama xulasho aan la akhrin karin ama aan sax ahayn | - | - |
| `history` | soo-koobidda waa la taxay | taariikh maqan, aan sax ahayn, ama aan la taageerin | ikhtiyaarro CLI oo aan sax ahayn | - | - |
| `compare` | isbarbardhigga waa la soo saaray, xitaa marka isbeddello jiraan | taariikh aan la akhrin karin, xad/hab-kala-horreyn aan is-waafaqsanayn, ama qoris fashilantay | ikhtiyaarro CLI oo aan sax ahayn | - | - |
| `diff` | isbeddel ma jiro | faylka `-o` lama qori karin | gelin maqan, aan la akhrin karin ama aan la taageerin, ama baaris aan dhammaystirnayn iyada oo aan la isticmaalin `--allow-partial` | isbeddello ayaa la helay, natiijooyin aan la xaqiijin, ama baaris aan dhammaystirnayn | - |
| `export` | qoraalka waa la qoray | qoraalka lama qori karin | gelin aan la akhrin karin, baaris aan dhammaystirnayn iyada oo aan la isticmaalin `--allow-partial`, ama xog aan si ammaan ah loo dhoofin karin | - | - |

## Qaab-dhismeedka

| Qayb | Mas'uuliyadda |
| --- | --- |
| `cli.py` | Ikhtiyaarrada amarrada, xallinta borofayllada, hubinta hordhaca ah, baarista iyo warbixinta |
| `scanner.py`, `probes.py` | Ballaarinta bartilmaameedyada, shaqaalaha xadidan, ogaanshaha martigeliyeyaasha iyo baarista adeegyada |
| `config.py`, `profiles.py` | Qeexidda adeegyada iyo borofayllada tira-koobka ee la xaqiijiyay |
| `models.py`, `output.py` | Noocyada natiijooyinka iyo soo-bandhigidda terminal/JSON/CSV |
| `history.py`, `diff.py` | Taariikhda SQLite iyo isbarbardhigga nuqul-xilliyeedyada faylasha ee noocaysan |
| `preflight.py` | Hubinta maxalliga ah iyo eegista nooca Nmap ee xadidan |
| `export.py` | Qoraallada gelinta ee Kadupul oo la xaqiijiyay lana xigtay |

Mid kasta oo ka mid ah natiijooyinka adeeggu wuxuu si gaar ah u diwaangeliyaa xaaladdiisa iyadoo laga soocayo aqoonsiga uu sheegtay. Akhrinta iyo xadadka waqtigu waa kuwo xadidan; qaladaadka ka yimaada tijaabooyinka waxay ku haraan qaladaadka martigeliyaha. Taariikhda SQLite waxay adeegsataa habka transactional, nadiifinta isku-xirka oo cad, iyo waddooyin akhris-keliya ah oo loogu talagalay taxidda iyo isbarbardhigga. Siraha SNMP waxay soo galaan oo keliya iyadoo la marayo doorsoomayaasha deegaanka ama faylasha sirta ah; taariikhda tira-koobku waxay kaydisaa habaynta shaqaynaysa ee aan sirta ahayn. Eeg [Qaab-dhismeedka nidaamka](../../../docs/architecture.md) si aad u aragto tubta baarista, xadadkeeda iyo xuduudaha kalsoonida, iyo [SECURITY.md](../../../SECURITY.md#authorized-use) si aad u aragto adeegsiga la oggol yahay.


## Adeegsiga

Baar oo keliya shabakadaha aad adigu maamusho.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Ikhtiyaar | Macnaha |
| --- | --- |
| `NETWORK` | CIDR, IP, ama magaca martigeliyaha; waa ikhtiyaari marka la adeegsanayo `--profile`. Aqoonsiyada xadka IPv6 (scope identifiers) waa la diidaa. |
| `-o, --output PATH` | Qor warbixin. Qaabku wuxuu raacaa kordhinta faylka (`.json`, `.csv`); kordhinnada kale waxay dib ugu laabtaan JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Ku qasab qaabka warbixinta. Wax saamayn ah ma laha haddii aan la isticmaalin `--output`. `.sh` waxay doorataa `kadupul`. |
| `-v, --verbose` | Diiwaangelinta faahfaahsan ee cilad-baarista (debug logging). |
| `-q, --quiet` | Aamusi natiijooyinka, horumarka iyo diiwaannada macluumaadka; digniinaha iyo qaladaadku weli waxay ka muuqdaan stderr. |
| `--backend asyncio\|nmap` | Ogaanshaha martigeliyeyaasha. `asyncio` (caadiga ah) wuxuu si toos ah u tijaabiyaa dekedaha adeegyada; `nmap` wuxuu marka hore socodsiiyaa baaritaanka ping sweep ee nmap wuxuuna u baahan yahay in barnaamijka `nmap` laga helo `PATH`. |
| `--timeout SECONDS` | Sugitaanka tijaabooyinka aan dejin waqti u gaar ah (caadiga ah 1.0). Tijaabooyinka ku-xirnaanta ee gudaha ku jira waxay adeegsadaan 0.3s haddii uusan jadwalka adeeggu dejin `timeout`. |
| `--concurrency N` | Tirada tijaabooyinka isku mar socda (caadiga ah 256). |
| `--deadline SECONDS` | Jooji baarista oo dhan, oo ay ku jirto baaritaanka nmap, waqtigan ka dib (caadiga ah 3600, ugu badnaan 604800; doorsoomaha deegaanka `HOSTCENSUS_DEADLINE`). Martigeliyeyaasha dhammaaday waxaa lagu qoraa warbixinta iyadoo wadata `"complete": false`, taariikh iyo nuqul-xilliyeed lama qoro, `scan` wuxuuna ku baxaa koodhka 4. |
| `--config PATH` | Qeexidda adeegyada TOML iyo habaynta ikhtiyaariga ah ee `[profiles]` ee magacaaban. |
| `--profile NAME` | Adeegso borofayl magacaaban; wuxuu caadi ahaan adeegsadaa `hostcensus.toml` marka laga tago `--config`. |
| `--exclude IP/CIDR` | Ku dar ka-reebis; ku celi inta loo baahan yahay. Martigeliye IPv4 ah oo laga reebay wuxuu sidoo kale ka reebaa cinwaannada IPv6 ee gaara: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) iyo 6to4. Bartilmaameedyada iyo ka-reebisyada IPv4-mapped waxaa loola dhaqmaa sidii cinwaannada IPv4 ee ay matalaan. |
| `--max-hosts N` | Xadka cinwaannada ee la hubiyo ka hor ka-reebista (caadiga ah/ugu badnaan adag 65,536). |
| `--history PATH` | Ku diwaangeli baarista dhammaystiran kaydka taariikhda SQLite ee ikhtiyaariga ah. |
| `--services NAMES` | Liis kooma ku kala go'an oo ah magacyada adeegyada la hubinayo, sida ay u kala horreeyaan (caadiga ah: dhammaan). |
| `--ports SPEC` | Liis kooma ku kala go'an oo ah `NAME=PORT` (u wareeji adeeg) ama `PORT` (ku dar hubin TCP oo caadi ah oo loo bixiyay `tcp-PORT`). |
| `--snmp-community-file PATH` | Fayl haya community-ga SNMPv2c ee weydiinta system MIB. Doorsoomaha deegaanka: `HOSTCENSUS_SNMP_COMMUNITY` (qiimaha) ama `HOSTCENSUS_SNMP_COMMUNITY_FILE` (waddada). |
| `--snmp-user` | Isticmaalaha SNMPv3. Doorsoomaha deegaanka: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (caadiga ah), `SHA224`, `SHA256`, `SHA384`, `SHA512` iyo fayl haya furaha sirta ah. Doorsoomaha deegaanka: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ama `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (caadiga ah), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` iyo fayl haya furaha sirta ah. Doorsoomaha deegaanka: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ama `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Sidoo kale qor nuqul-xilliyeed noocaysan oo loogu talagalay `hostcensus diff`. |
| `--tls-ca-file PATH` | Ku xaqiiji shahaadooyinka HTTPS xirmadan PEM halkii aad ka adeegsan lahayd kaydka nidaamka. Doorsoomaha deegaanka: `HOSTCENSUS_TLS_CA_FILE`. |

Si caadi ah, martigeliye kasta waxaa laga hubiyaa SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) iyo HTTPS (TCP 443). Dekedaha TCP waxaa lagu tijaabiyaa isku-xir dhammaystiran. SNMP waxaa lagu tijaabiyaa codsiga ogaanshaha matoorka SNMPv3, kaas oo wakiil kasta oo SNMPv3 ah ay waajib ku tahay inuu ka jawaabo iyada oo aan loo baahnayn aqoonsi sir ah; wakiillada ku hadla oo keliya v1/v2c laguma ogaan doono tijaabadan. Marka la adeegsanayo habka dambe ee asyncio, martigeliyuhu wuxuu noqdaa mid nool marka tijaabo kasta ay hesho jawaab, oo ay ku jirto isku-xir la diiday, sidaas darteed martigeliye tuura tijaabo kasta wuxuu yeeshaa `alive=false` iyo qaladka "Host is down"; tani ma caddaynayso inuu jir ahaan u damisan yahay. Marka la adeegsanayo `--backend nmap`, nmap ayaa go'aamisa martigeliyeyaasha nool (ICMP marka la haysto awoodda root, ama TCP 80/443 xaaladaha kale).

### Aqoonsiga adeegyada

Adeeg kasta oo furan waxaa laga sameeyaa aqoonsi iyadoo lagu saleynayo waxa uu soo diro ka hor inta aan wax galitaan (login) ah la samayn. Waxba ma sameeyaan xaqiijin aqoonsi marka laga reebo weydiinta SNMP, taasna waa oo keliya marka aad bixiso aqoonsiyada sirta ah.

| Tijaabo | Waxa la akhriyo | `version` | Furayaasha `details` |
| --- | --- | --- | --- |
| `ssh` | Sadarka aqoonsiga RFC 4253 | barnaamijka, tusaale `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Is-afgaradka bilowga ah ee MySQL/MariaDB | nooca adeegaha | `server_version`, `flavor`, `auth_plugin`, ama `error_code`/`error` |
| `http` | Jawaabta `HEAD /` | madaxa `Server` | `status`, `server` |
| `https` | Is-afgaradka TLS, shahaadada, `HEAD /` | madaxa `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Ogaanshaha SNMPv3; iyadoo la haysto aqoonsi sir ah, GET ee sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; iyadoo la haysto aqoonsi sir ah `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ama `snmp_error` |

Bartilmaameedka magaca martigeliyaha waxaa la xalliyaa hal mar martigeliye kasta, tijaabo kastana waxay ku xirantaa cinwaankaas, kaas oo natiijooyinka loogu diwaangeliyo `address`; magaca waxaa loo adeegsadaa oo keliya TLS SNI, xaqiijinta shahaadada iyo madaxa HTTP `Host`. Magac aan la xallin karin wuxuu soo celiyaa xaalado `unknown` ah iyo qaladka `Cannot resolve`. Magacyada reverse DNS waxaa la ilaaliyaa oo keliya marka ay ka kooban yihiin xarfaha magaca martigeliyaha, waxaana isku mar shaqayn kara ugu badnaan 16 raadin. HTTPS waxay adeegsataa xaqiijinta shahaadada iyo magaca martigeliyaha iyadoo la barbardhigayo kaydka nidaamka ama `--tls-ca-file`. Kaydka kalsoonida waxaa la soo raraa hal mar baarista oo dhan waxaana dib loogu adeegsadaa tijaabo kasta oo HTTPS ah. Isku-xirka TCP iyo is-afgaradka TLS waxaa si kala gooni ah loogu xisaabiyaa waqtiga, markaa deked aqbasha isku-xirka balse hakisa is-afgaradka waxaa loo diwaangeliyaa `open` iyadoo wadata `tls_error`, ee ma aha `filtered`. Haddii xaqiijintu fashilanto, natiijadu waxay diwaangelisaa `cert_verified: false` iyo `cert_verify_error`; dib iskuma daydo habayn daciif ah mana dirto codsi HTTP ah. Faahfaahinta shahaadada iyo madaxyada HTTP waxaa la ururiyaa oo keliya marka xaqiijintu guulaysato. Bixi xirmada CA ee saxda ah adeegyada leh CA gaar ah. Warbixinnadii hore waxay yeelan karaan `cert_read_unverified`, taas oo tijaabooyinka hadda jira aysan mar dambe soo saarin.

Siraha SNMP waxaa laga akhriyaa oo keliya doorsoomayaasha deegaanka ama faylasha (`--snmp-*-file`, ama doorsoomaha la midka ah ee `HOSTCENSUS_SNMP_*_FILE`), waligoodna lagama akhriyo qiimayaasha khadka amarka, kuwaas oo isticmaaleyaasha kale ee maxalliga ah ay ka arki karaan liiska hababka socda (process list). `--snmp-community`, `--snmp-auth-key` iyo `--snmp-priv-key` oo leh qiimo waxay ku baxaan koodhka 2 waxayna sheegaan beddelkooda. Faylka sirta ah waa inuu ahaadaa UTF-8 aan marneyn oo ugu badnaan ah 4096 bytes; hal sadar cusub oo dhammaadka ah waa la iska indhatiraa, dejinta doorsoome iyo fayl isku mid ah oo hal sir ahna waa qalad. Qaladaadku waxay magacaabaan faylka balse waligood ma daabacaan waxa ku jira. Warbixinnada baarista iyo taariikhdu si ula kac ah uguma daraan qiimayaasha aqoonsiyada sirta ah. Dhoofiyuhu wuxuu leeyahay ikhtiyaar gaar ah oo cad oo ah `--include-credentials` oo hoos lagu sharraxay. Community waxay doorataa SNMPv2c; isticmaale wuxuu doortaa SNMPv3, iyadoo leh xaqiijin (authentication) marka la bixiyo furaha auth iyo asturnaanta (privacy) marka la bixiyo labada fureba (`snmp_security_level` ayaa diwaangeliya midka la adeegsaday). hostcensus way diiddaa, iyadoo ku baxaysa koodhka 2, in la isku daro community iyo isticmaale v3, in la adeegsado furaha privacy iyada oo aan la haysan furaha auth, ama in la adeegsado furayaal iyada oo aan la haysan isticmaale, waligeedna dib iskuma daydo weydiin v3 ah oo fashilantay iyadoo adeegsanaysa v2c ama heer amni oo ka hooseeya. Wakiillada ku hadla oo keliya v1/v2c way iska indhatiraan ogaanshaha v3 ee aan sirta lahayn, sidaas darteed waxay u muuqdaan kuwo furan oo keliya marka community la bixiyo.

Qoraalka soo-dhaweynta (banner) waxaa lagu soo koobaa xarfaha la daabici karo waxaana lagu xadeeyaa 256 xaraf ka hor inta aan la kaydin ama aan la muujin. Akhrintu sidoo kale waa mid xadidan: 4 KiB sadarkiiba, 4 KiB salaanta MySQL, 16 KiB madaxyada HTTP. Aqoonsiga matoorka SNMP (engine ID) ee ka dheer 32 octets waa la soo gaabiyaa ka hor inta aan la kaydin. HTTP iyo HTTPS waxay diraan madaxa Host iyadoo cinwaanka IPv6 ku jiro qaansooyin labajibbaaran iyo dekedda marka aysan ahayn 80 ama 443. Unugyada CSV ee ku bilowda astaamaha kiciya qaacidooyinka jadwalka (spreadsheet formula) waxaa lagu daraa horgale si unuggu ugu sii jiro qoraal caadi ah.

### Xadadka

Hal socodsiin waxay aqbashaa ugu badnaan 65,536 cinwaan, 64 adeeg, iyo 524,288 tijaabo (martigeliyeyaasha oo lagu dhuftay adeegyada); codsiyada ka weyn waxay ku baxaan koodhka 2 ka hor inta aan waxba la dirin. `--concurrency` waxaa lagu xadeeyay 4096 godad (sockets). Tijaabo kasta waxay leedahay xad waqti oo adag oo afar jibbaar ka badan miisaaniyaddeeda waqtiga. Tijaabooyinka ku-xirnaanta (`tcp`, `ssh`, `mysql`, `http`) waxay adeegsadaan 0.3 ilbiriqsi haddii uusan adeeggaasi dejin `timeout`. SNMP iyo HTTPS waxay adeegsadaan `--timeout` (caadiga ah 1.0) marka aysan dejin mid u gaar ah. Tijaabo gaarta xadka waqtiga waxaa loo soo sheegaa `unknown` iyadoo "probe timed out" lagu qorayo `errors`. Guul-darrooyinka godadka maxalliga ah (tusaale ahaan dhammaanshaha file descriptors) iyaguna waa `unknown` iyadoo qaladka la diwaangelinayo; waligood looma tiriyo deked la shaandheeyay (filtered) ama martigeliye damisan. Ka hor tijaabinta, hostcensus waxay kor u qaaddaa xadka jilicsan ee faylasha furan (open-file soft limit) iyadoo u dhaweynaysa xadka adag si ay u qaaddo `--concurrency` oo lagu daray 64 descriptors; marka aysan awoodin, hubinta hordhaca ah ee `open files` way fashilantaa `scan` wuxuuna ku baxaa koodhka 1 ka hor inta aan xog shabakad la dirin. Ogaanshaha Nmap wuxuu adeegsadaa 30 ilbiriqsi oo waqti-dhammaad martigeliye ah. Horgale (prefix) waxaa loo gudbiyaa nmap isagoo ku jira qaabka CIDR, baaritaankuna wuxuu ku fashilmaa koodhka 1 marka nmap ay soo sheegto cinwaanno ka yar kuwii la siiyay (tusaale ahaan magac aysan xallin karin) halkii ay martigeliyeyaasha ku calaamadin lahayd kuwo damisan. Bartilmaameedka magaca martigeliyaha waxaa la xalliyaa hal mar waxaana nmap la siiyaa cinwaankaas, si ogaanshaha iyo tijaabooyinku ay u gaaraan isla mishiinka. Horgale dhammaystiran waa hal habsocod (process) oo nmap ah kaas oo xadka waqtigiisu yahay 35 ilbiriqsi 256-kii cinwaanba, iyadoo kor loo wareejiyo. Baaritaannada leh ka-reebisyo waxay adeegsadaan kooxo ka kooban 256 martigeliye iyo xad waqti oo 35 ilbiriqsi ah koox kasta. Abuurista shaqaalaha waxay u xadidan tahay si ka madax-bannaan cabbirka xadka cinwaannada. Reverse DNS iyo xallinta magacyada martigeliyeyaasha waxay leeyihiin xad waqti oo gaar ah oo labo ilbiriqsi ah; wicitaan xalliye ah oo aan waligiis soo noqon waxaa looga tagaa xargigiisa (thread) gaarka ah, si uusan hostcensus ugu hayn inay dhaafto xadadkan. Ugu badnaan 16 raadin ayaa isku mar socon kara, wicitaan laga tagayna wuxuu haystaa booskiisa ilaa uu ka soo noqdo, si tirada xargaha xaniban ay u xadidnaato; haddii dhammaan 16-ka ay xayirmaan, raadinaha dambe waxay saf u galaan boos ka baxsan xadka labada ilbiriqsi (kaas oo bilowda marka boos bannaanaado) ilaa `--deadline` uu joojiyo baarista. `NetworkScanner` marka loo adeegsado sidii maktabad iyada oo aan la siin `deadline` wuxuu booskaas sugi karaa muddo aan xadidnayn. `--deadline` (caadiga ah hal saac) ayaa xadeeya socodsiinta oo dhan marka lagu daro xadadkan.

### Habaynta adeegyada

Adeegyada waxaa lagu beddeli karaa fayl TOML ah:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` waa mid ka mid ah `tcp`, `ssh`, `mysql`, `http`, `https` ama `snmp` wuxuuna si caadi ah u qaataa magaca adeegga marka uu yahay tijaabo, haddii kalena `tcp`. Keliya `snmp` ayaa adeegsada UDP. Magacyada adeegyadu waa xarfo yar-yar, tirooyin, `-` iyo `_`. Labo adeeg ma wadaagi karaan hal deked iyo hal borotokool; taariikhdu waxay u diwaangelisaa hal xaalad lammaanahaas. `timeout` waa ikhtiyaari, wuxuu ku cabbiran yahay ilbiriqsiyo, waana ugu yaraan 0.05. Tijaabooyinka nooca ku-xirnaanta (`tcp`, `ssh`, `mysql`, `http`) waxay si caadi ah u adeegsadaan 0.3 ilbiriqsi. `snmp` iyo `https` waxay adeegsadaan `--timeout` ee baarista marka uusan adeeggu dejin `timeout`. `--timeout` ma beddelo waqti uu adeeggu hore u lahaa.

Warbixinnada JSON waa dukumentiyo noocaysan (`"format": "hostcensus-report"`, `"version": 1`) oo diwaangeliya bartilmaameedka, adeegyada la tijaabiyay iyo habaynta iyagoo garab yaalla `devices`; `--format json` iyada oo aan la isticmaalin `-o` waxay warbixinta ku qortaa stdout halkii ay ka soo bandhigi lahayd jadwalka. Natiijo kasta oo JSON ah waxay leedahay qaab-dhismeed (schema) la daabacay; eeg [Natiijada JSON](../../../docs/json-output.md). Qalabyadu waxay ilaashadaan goobaha asalka ah ee `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` iyo `errors` waxayna ku daraan liiska `services` oo leh tijaabo kasta `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, ama `unknown` marka tijaabadu si maxalli ah u fashilanto ama gaarto xadka waqtiga), `version` iyo `details`. Natiijada CSV waxaa dhammaadka loogu daraa tiirarka `services` iyo `versions` ee kuwa furan. Qiimayaasha run/been (booleans) ee `ssh`, `snmp` iyo `mysql` waxay raacaan adeegyada leh isla magacyadaas.


## Borofayllada tira-koobka, hubinta hordhaca ah, iyo taariikhda maxalliga ah

Borofayllada magacaaban waxay faylka TOML la wadaagaan qeexidda `[services]` ee hore u jirtay. Nuqul ka samee [hostcensus.example.toml](../../../hostcensus.example.toml) una bixi `hostcensus.toml` oo deji shabakadaha aad maamusho:

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

`preflight` wuxuu u xalliyaa ikhtiyaarrada iyo borofayllada si la mid ah `scan`, oo ay ku jirto `--concurrency` ee hubinta faylasha furan, sidaas darteed hubin hordhac ah oo guulaysata waxay ka dhigan tahay in `scan` uu ku bilaaban doono isla qorshahaas.

Borofaylladu waxay aqbalaan `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency`, iyo `max_hosts`. `services` iyo `ports` waxay adeegsadaan qaab-qoraalka liiska koomada ee hore u jiray. Ikhtiyaarrada CLI ee si cad loo qoro waxay ka awood bataan habaynta borofaylka; ikhtiyaarrada `--exclude` ee lagu celceliyo waxaa lagu daraa ka-reebisyada borofaylka. Shabakad si cad loo sheegay iyadoo la adeegsanayo `--profile` waa inay ku jirtaa xadka IP/CIDR ee borofaylkaas. Magacyada martigeliyeyaasha weli waa la taageeraa baaritaannada tooska ah, laakiin laguma dari karo ka-reebisyada IP. Xadadka martigeliyeyaasha waxay dhaqan galaan ka hor ka-reebista; xadka guud ee tijaabooyinka weli wuxuu dhaqan galaa ka dib. Martigeliyeyaasha laga reebay waxaa laga saaraa labadaba hubinta adeegyada iyo ogaanshaha Nmap ee ikhtiyaariga ah.

Baaris kasta waxay samaysaa hubin hordhac ah oo maxalli ah ka hor inta aan xog loo dirin bartilmaameedka: xadadka bartilmaameedka/tijaabada, gelitaanka meesha lagu qorayo, helitaanka barnaamijka/wrapper-ka Nmap ee ikhtiyaariga ah, qaab-dhismeedka taariikhda, iyo xirmada TLS CA ee habaysan. `preflight` wuxuu soo celiyaa warbixin JSON ah mana baaro bartilmaameedyada mana abuuro kayd taariikheed. Wuxuu si ku-meel-gaar ah u qoraa fayl la deris ah si uu u tijaabiyo gelitaanka meesha lagu qorayo isagoon beddelin waxa hore ugu jiray. Habka dambe ee caadiga ah ee asyncio weli uma baahna Nmap mana u baahna root. Waddooyinka meelaha lagu qorayo waa inay kala duwanaadaan kana duwanaadaan faylka habaynta ee gelinta, oo ay ku jiraan isku-xirka adag (hard links); isku-xirka calaamadeed (symlinks) ee meesha lagu qorayo waa la diidaa. Hubinta fashilanta waxay soo celisaa 1; xad ama habayn aan sax ahayn waxay soo celisaa 2.

Qorista warbixinnada iyo dhoofinta waxay u baahan yihiin taageerada `O_NOFOLLOW`. Nidaamyada aan lahayn, oo uu ku jiro Windows, qorisyadani way fashilmaan iyagoon furin ama jarin faylka loo socdo. Warbixinnada cusub iyo qoraallada dhoofinta waxaa iska leh oo keliya mulkiilaha (qaabka 0600); beddelidda fayl hore u jiray waxay ilaalisaa rukhsadihiisa. Ku qorista tuubbo magacaaban (named pipe) oo aan lahayn akhriye isla markiiba way fashilantaa halkii ay sugi lahayd. Kaydka cusub ee `--history` isagana waxaa loo abuuraa mulkiilaha oo keliya; mid hore u jirayna wuxuu ilaashadaa qaabkiisa rukhsadda. Fariimaha diiwaanku (logs) mar walba waxay aadaan stderr, si stdout ay u qaaddo oo keliya natiijooyinka. Dhoofinnada ay ku jiraan aqoonsiyo sir ah mar walba waxay ku qasbaan qaabka 0600.

Taariikhdu waa ikhtiyaari waxayna kaabtaa nuqul-xilliyeedyada JSON ee hore u jiray iyo amarka `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Adeegso aqoonsiyada (IDs) ka yimid `history`; tusaaluhu wuxuu u qaadanayaa kayd cusub. Nuqul-xilliyeedyada waxaa loo kaydiyaa habka transactional iyagoo wata waqtiyada bilowga iyo dhammaadka ee UTC, nooca xirmada, habaynta shaqaynaysa ee aan sirta ahayn, soo-koobidda, iyo dhammaan natiijooyinka martigeliyaha iyo adeegyada, oo ay ku jiraan qaladaadka martigeliye kasta. Natiijooyinka martigeliyeyaasha ee aan dhammaystirnayn waa la ilaaliyaa. Socodsiinnada la joojiyay (cancelled) lama kaydiyo. Heshiisyada koodhadhka bixitaanka ee warbixinta, nuqul-xilliyeedka, dhoofinta, iyo baarista ee hore u jiray waa la ilaaliyay.

`history` wuxuu taxaa soo-koobidda JSON isagoon akhrin dhammaan xogta qalabyada taariikhiga ah. `compare` wuxuu akhriyaa labo baaris oo la kaydiyay, wuxuu u baahan yahay aqoonsiyo bartilmaameed oo isku mid ah iyo dekeddo la doortay oo isku mid ah, wuxuuna soo sheegaa isbeddellada jawaab-celinta, xaaladda, iyo xaaladda dekedaha. Aqoonsiga baarista hore waa inuu ka horreeyaa aqoonsiga baarista dambe. Marka labada baarisba ay diwaangeliyeen `timeout` ama `backend` qiimayaashaasna ay kala duwan yihiin, warbixintu waxay taxdaa digniin waxayna weli isbarbardhigtaa natiijooyinka. Sugitaan ka duwan wuxuu ka dhigi karaa deked la shaandheeyay (filtered) inay u muuqato mid furan. Qaladaadka baaraha iyo natiijooyinka dekedaha aan la garanayn waxaa lagu calaamadiyaa kuwo aan la hubin halkii loola dhaqmi lahaa sidii lumid ama xiritaan la xaqiijiyay: martigeliyeyaasha leh qaladaad waxay ka muuqdaan `uncertain_hosts`, isbeddel kasta oo deked ah oo ay ku jirto `unknown` (oo ay ku jirto unknown labada baarisba) waxaa lagu qoraa `unconfirmed_ports` halkii laga qori lahaa `port_changes`, marka laga reebo deked furan baarista dambe, taas oo ah isbeddel deked. `compare` iyo `diff` waxay dekedaha u kala saaraan isla xeerkaas. `no_longer_responding` waxay ka dhigan tahay jawaab la'aan, ee ma aha caddayn in qalabka la saaray. Koodhka bixitaanka baarista ee 0 ma dammaanad qaadayo in martigeliye kasta uu ka jawaabay: hubi qaladaadka martigeliye kasta. Guusha isbarbardhiggu waxay soo celisaa 0 haddii ay isbeddello jiraan iyo haddii kaleba; `diff` ee faylasha hore u jiray wuxuu ilaashadaa heshiiskiisa koodhka bixitaanka 3. Taariikh aan la taageerin ama kharriban waxay soo celisaa 1.

Taariikhdu waxay kaydisaa macluumaadka tira-koobka, markaa dooro gal maxalli ah oo si habboon u ilaalsan. Faylasha borofaylka iyo habaynta la kaydiyay kuma jiraan aqoonsiyada sirta ah ee SNMP; maaraynta aqoonsiyada sirta ah waxay ku sii socotaa ikhtiyaarrada/deegaanka runtime-ka ee hore u jiray.

## Isbarbardhigga tira-koobka

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Nuqul-xilliyeedku waa JSON leh `format: "hostcensus-snapshot"`, `version: 1`, nooca hostcensus, waqtiga abuurista UTC, bartilmaameedka, `timeout` iyo `backend` ee baarista marka baaristu diwaangelisay, adeegyada la tijaabiyay, iyo martigeliyeyaasha nool oo ku jira isla qaabka warbixinta `-o`. Martigeliyeyaasha damisan waa laga tagaa. `diff` wuxuu sidoo kale aqbalaa warbixinnada JSON ee caadiga ah ee `scan -o`, oo ay ku jiraan kuwii ka horreeyay inta aysan goobta `services` jirin.

`diff` wuxuu soo sheegaa martigeliyeyaasha cusub iyo kuwa lumay, dekedaha furmay ama xirmay ee martigeliyeyaasha ku jira labadaba, iyo adeegyada ay iska beddeshay `version`. Dekedaha lagu tijaabiyay hal baaris oo keliya lama isbarbardhigo, waxaana la bixiyaa digniin arrintaas sheegaysa. Natiijooyinka fashilmay waligood looma akhriyo "isbeddel ma jiro": deked ah `unknown` mid ka mid ah labada baaris oo aan furnayn baarista dambe waxaa lagu taxaa `unconfirmed`, ee ma aha `closed`, iyadoo `before` yahay `open`, `unknown` ama `not-open` (la tijaabiyay oo xiran ama la shaandheeyay) iyo `after` yahay `unknown` ama `not-open`; deked hadda furan waxaa lagu soo sheegaa `opened` xitaa haddii tijaabadii hore fashilantay. Martigeliye tijaabooyinkiisu oo dhan ay fashilmeen jawaab la'aan mid ka mid ah labada baaris waxaa lagu taxaa `unsettled_hosts` (iyadoo `before`/`after` yahay `up`, `uncertain` ama `absent`, oo ay ku jirto marka uu ku fashilmay labada baarisba ama uu ka maqan yahay faylka kale) halkii laga qori lahaa `vanished_hosts`; haddii uu ka jawaabo baarista dambe waxaa sidoo kale loo soo sheegaa sidii martigeliye cusub iyo dekedihiisa furan. Nuqul-xilliyeedyadu waxay sababtan awgeed u hayaan martigeliyeyaashaas fashilmay. Digniin ayaa sidoo kale soo baxda marka bartilmaameedyadu kala duwan yihiin, iyo marka labada faylba ay diwaangeliyeen timeout ama backend qiimayaashaasna ay kala duwan yihiin. `-o PATH` wuxuu qaabka JSON sidoo kale ku qoraa fayl.

Warbixin ka timid baaris uu joojiyay `--deadline` (`"complete": false`) waxay taxdaa oo keliya martigeliyeyaashii ay gaartay, sidaas darteed `diff` iyo `export` way diidaan iyagoo ku baxaya koodhka 2. `--allow-partial` wuu aqbalaa iyadoo digniin lagu qorayo stderr: `diff` wuxuu markaa martigeliyeyaasha aysan baarista aan dhammaystirnayn haba yaraatee taxin ku qoraa `unsettled_hosts` iyagoo ah `unscanned` halkii ay ka noqon lahaayeen kuwo lumay (martigeliye ay u taxday mid damisan weli wuxuu yahay mid lumay), wuxuu `partial` ka dhigaa run (true) waligiisna ma soo sheego in uusan jirin isbeddel, `export` wuxuuna qoraa digniin madaxa qoraalka (script header).

Koodhadhka bixitaanka ee `diff`: `0` isbeddel ma jiro, `3` isbeddello ayaa la helay, natiijooyin aan la xaqiijin karin, ama gelin aan dhammaystirnayn (`changed` waa run mar kasta oo liis kasta, oo ay ku jiraan `unsettled_hosts` iyo `unconfirmed`, uusan marneyn, ama `partial` uu run yahay), `2` fayl ayaa maqan, aan la akhrin karin, aan ahayn nuqul-xilliyeed la taageero, ama aan dhammaystirnayn iyada oo aan la isticmaalin `--allow-partial`, `1` faylka `-o` lama qori karin.

## Dhoofinta Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (oo ah farac ka yimid Cacti 1.2.31) ma laha soo-gelin fayl oo qalabyo badan isku mar lagu daro. Habka la taageero ee qalabyada looga daro qoraal (script) waa `cli/add_device.php`, hal qalab wicitaankiiba, iyadoo la adeegsanayo doodaha `--option=value`. `hostcensus export` wuxuu qoraa qoraal POSIX `sh` ah oo wicitaannadaas ka kooban:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Martigeliye kasta oo nool wuxuu noqdaa `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Martigeliyeyaasha weydiinta SNMP ee baaristu ku guulaysatay waxay helaan `--version=2 --community=...` ama `--version=3 --username=... --authproto=... --password=...` (oo lagu daray `--privproto`/`--privpass` ee authPriv), `--port` iyo `--avail=snmp`. Dhoofinta SNMPv3 waxay u baahan tahay `--snmp-user`, noAuthNoPriv-na waa la diidaa sababtoo ah `add_device.php` wuxuu u baahan yahay furaha sirta ah ee v3.
- Martigeliyeyaasha kale waxay helaan `--version=0 --avail=ping`, iyadoo `--ping_method=tcp --ping_port=` ay tahay dekedda TCP ee ugu horreysa ee furan, ama ICMP haddii aysan midna furnayn.
- `--notes` waxay taxdaa adeegyada furan iyo noocyadooda. `--description` waa magaca reverse-DNS marka uu fudud yahay (xarfo, tirooyin, `.`, `_`, `-`), haddii kalena IP-ga, waxaana laga dhigaa mid gaar ah, sababtoo ah `add_device.php` wuxuu sharraxaad hore u jirtay u qaataa cusboonaysiin qalabkaas.

Qiimo kasta waa la xaqiijiyaa waxaana shell-ka loogu xigtaa `shlex.quote`. Si caadi ah wax sir SNMP ah lama qoro: qoraalku wuxuu ballaariyaa `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ama `HOSTCENSUS_SNMP_PRIV_KEY` waqtiga socodsiinta wuxuuna istaagaa haddii mid uusan dejisnayn. `--include-credentials` wuxuu beddelkeeda qiimayaasha doorsoomayaashaas deegaanka ku qoraa qoraalka gudihiisa, wuxuu ku abuuraa qaabka 0600, wuxuuna diwaangeliyaa digniin. `add_device.php` laftiisu wuxuu daabacaa community-ga wuxuuna siraha u helaa sidii doodo, kuwaas oo ka muuqda liiska hababka socda ee adeegaha Kadupul inta wicitaan kasta socdo.

`add_device.php` wuxuu ku baxaa 1 nuqullada soo noqnoqda iyo qaladaadka; qoraalku wuu sii socdaa, wuxuu tiriyaa guul-darrooyinka, wuxuuna ku baxaa 1 haddii qalab kasta aan lagu darin. Aqoonsiyada qaab-dhismeedka (template ids) waxay ka yimaadaan `php cli/add_device.php --list-host-templates`. Koodhadhka bixitaanka ee `export`: `0` waa la qoray, `2` gelin aan la akhrin karin, baaris aan dhammaystirnayn iyada oo aan la isticmaalin `--allow-partial`, ama xog aan si ammaan ah loo dhoofin karin, `1` qoraalka lama qori karin.

## Noocaynta iyo habka sii-daynta

hostcensus waxay raacdaa [Semantic Versioning](https://semver.org/spec/v2.0.0.html): hagaajinta is-waafaqsan waxay kordhisaa nooca patch, astaamaha is-waafaqsan iyo digniinnada ka-bixista waxay kordhiyaan nooca minor, isbeddellada jabinaya is-waafajintuna waxay kordhiyaan nooca major. Amarrada iyo ikhtiyaarrada, koodhadhka bixitaanka iyo qaab-dhismeedyada JSON waa heshiiska guud; hab-dhaqanka la joojin doono wuxuu sii shaqeeyaa ilaa sii-daynta weyn ee xigta, haddii uusan hagaajin amni u baahan in goor hore la beddelo (diiwaanka isbeddelka ayaana sharraxa sababta).

release-please waxay furtaa PR sii-dayn ah iyadoo ka duulaysa cinwaannada Conventional Commit ee ku jira `main`, iyadoo kordhinaysa `pyproject.toml`, `uv.lock` iyo `CHANGES.md`. Isku-darkeedu wuxuu abuuraa sumadda `vMAJOR.MINOR.PATCH` iyo sii-dayn GitHub oo qabyo ah, taas oo CI uu ku lifaaqo wheel la tijaabiyay, qaybinta koodhka isha (source distribution) iyo checksums; GitHub wuxuu u kaydiyaa caddeymaha dhismaha (build attestations) faylashaas isagoo adeegsanaya attestations API. Maamulaha mashruuca ayaa dib u eega oo daabaca qabyada marka faylasha lagu lifaaqo. Sii-daynnada waligood lama beddelo.

Daabacaadda la aamini karo ee PyPI (trusted publishing) waa ikhtiyaari waxayna u baahan tahay lahaanshaha mashruuca, daabace la aamini karo iyo deegaanka `pypi`. Waxay daabacdaa isla agabka sii-daynta ee la hubiyay iyada oo aan dib loo dhisin ama aan la kaydin calaamad API (API token). Sii-daynnada sumadaysan ee kaydkan guud waxay soo saaraan caddeymaha agabka GitHub; faracyada gaarka ah (private forks) waxay u baahan yihiin qorshe la taageero iyo oggolaansho cad. Eeg [hagaha dhammaystiran ee sii-daynta](../../../docs/releasing.md) si aad u aragto habaynta, amarrada saxda ah iyo isku-dayga dib-u-socodsiinta.

## Horumarinta

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Aaladaha horumarintu waxay ku jiraan kooxaha ku-tiirsanaanta [PEP 735](https://peps.python.org/pep-0735/) ee gudaha `pyproject.toml` (`dev`, `fuzz`, `build`), sidaas darteed waligood kama muuqdaan xogta guud (metadata) ee xirmada la daabacay. `uv.lock` waa faylka qufulka ee keliya; CI wuxuu ku rakibaa `uv sync --locked` wuxuuna fashilmaa marka faylka qufulku duugoobo. Ku dooro tarjubaanka `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), ama Python 3.12+ kasta.

CI wuxuu dhaqan-geliyaa heerka ugu hooseeya ee daboolista tijaabada xirmada oo ah 90%. Tijaabooyinka unugga (unit tests) waxaa ku jira adeegayaal loopback ah oo la xakameeyo iyo kiisas offline ah oo borofaylka/taariikhda/xaqiijiyaha sii-daynta ah; shaybaarka Compose wuxuu ku socodsiiyaa OpenSSH, MariaDB, nginx iyo net-snmp buundo go'doonsan. Ku socodsii `make test-integration`. Eeg [CONTRIBUTING.md](../../../CONTRIBUTING.md) iyo [aaladaha sii-daynta](../../../scripts/README.md).

Konteenarka runtime-ku wuxuu ku shaqeeyaa UID/GID 10001 isagoon lahayn galka hoyga (home directory), galitaan shell iyo pip, wuxuuna wax ku qori karaa `/app/output`. Sii isticmaalahaas rukhsadda qorista gal kasta oo natiijo ah oo la rakibay (mounted). Uma baahna awoodo dheeraad ah (capabilities) wuxuuna la shaqeeyaa nidaam fayl root ah oo akhris-keliya ah, markaa waxaa lagu socodsiin karaa sidan:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap wuxuu konteenarkan gudihiisa ku adeegsadaa hab-dhaqankiisa ogaanshaha TCP ee aan awoodda sare lahayn. CI wuxuu fashiliyaa dhismaha sawirka haddii Trivy ay soo sheegto dayac amni oo la hagaajin karo oo heerkiisu yahay HIGH ama CRITICAL.

## Hubinta silsiladda saadka

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) waxay ku shaqaysaa main iyo toddobaadkiiba mar, waxay daabacdaa dhibcaheeda dhabta ah, waxayna natiijooyinka u gelisaa baarista koodhka ee GitHub. Actions iyo aasaaska konteenarrada waxaa lagu xiraa hashes aan isbeddelin; ku-tiirsanaannada Python waxaa lagu xalliyaa `uv.lock`. Guul-darrooyinka Bandit waxay fashiliyaan CI, tijaabinta fuzzing ee Atheris ee xadidanna waxay tijaabisaa farsameeyayaasha SSH, MySQL, HTTP, shahaadada iyo SNMPv3 BER iyada oo aan la adeegsan gelitaan shabakad.

Scorecard wuxuu sidoo kale cabbiraa dhaqdhaqaaqa dib-u-eegista taariikhiga ah, kala duwanaanshaha wax-ku-biiriyeyaasha, iyo asalka sii-daynta (release provenance). Dhibcahaasi waxay ka tarjumayaan caddayn dhab ah; ma aha sheegasho in hubin kasta oo maamul ama sii-dayn taariikhi ah la buuxiyay. Eeg [SECURITY.md](../../../SECURITY.md) iyo [asalka sii-daynta](../../../docs/releasing.md).

## Deegaameynta

Fariimaha CLI iyo jadwallada soo-koobidda iyo isbarbardhigga ee terminal-ka waxay taageeraan 45 deegaan-luqadeed (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) iyada oo aan loo baahnayn wax ku-tiirsanaan runtime oo dheeraad ah. Xallinta luqaddu waxay u kala horreysiisaa `--lang`, ka dib `LC_ALL`, `LC_MESSAGES`, iyo `LANG`, iyadoo ugu dambeyn ku noqonaysa `en`. Qaab-dhismeedyada JSON, tiirarka CSV, iyo qoraallada dhoofinta isma beddelaan dhammaan deegaan-luqadeedyada.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Wax-ku-biirinta

Wax-ku-biirintu waa inay ku jiraan kiis dib loo soo saari karo, waa inay ilaaliyaan heshiisyada CLI iyo qaababka xogta ee la diwaangeliyay, waana inay ka gudbaan hubinta tayada ee kor ku xusan. Eeg [CONTRIBUTING.md](../../../CONTRIBUTING.md) si aad u aragto hab-socodka horumarinta iyo [hagaha sii-daynta](../../../docs/releasing.md) ee go'aannada is-waafajinta iyo noocaynta.

## Xaaladda amniga iyo shatiga

Eeg [SECURITY.md](../../../SECURITY.md) si aad u aragto warbixinta gaarka ah ee amniga iyo noocyada la taageero. hostcensus waxaa lagu siiyay shatiga [MIT License](../../../LICENSE).

Madaxyada koodhka isha waxay adeegsadaan aqoonsiyada SPDX waxayna ilaaliyaan aqoonsiga wax-ku-biiriyeyaasha ee taariikhda Git. Eeg [AUTHORS.md](../../../AUTHORS.md) si aad u aragto aqoonsiga qorayaasha. Duubista tijaabooyinka binary-ga iyo faylka qufulka ee la soo saaray waxay adeegsadaan faylal `.license` ah oo garab yaalla; qoraalka MIT wuxuu ku jiraa `LICENSES/MIT.txt`.
