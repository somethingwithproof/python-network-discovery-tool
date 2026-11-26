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

[Afrikaans](../af-ZA/README.md) · **አማርኛ** · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus እርስዎ በሚያስተዳድሯቸው አውታረ መረቦች ላይ ተደጋጋሚ የአገልግሎት ቆጠራ ለማካሄድ የሚያገለግል የPython CLI መሣሪያ ነው።
መሣሪያዎች ምን እንደሚያቀርቡ ይመዘግባል፣ ምልከታዎችን በጊዜ ሂደት ያወዳድራል፣ እንዲሁም የKadupul ማስገቢያ ስክሪፕቶችን ያመነጫል። ነባሪው backend ያለ root ፈቃድ asyncio ሶኬቶችን ይጠቀማል፤ አማራጭ የNmap ፍለጋ ደግሞ ከተዋቀሩት የአገልግሎት ወደቦች ባሻገር ያሉ አስተናጋጆችን መለየት ይችላል።

## ለምን hostcensus

አንድ ጊዜ ብቻ የሚወጣ የወደብ ሪፖርት ቀጣዩ ምልከታ መለወጡን ወይም በቀላሉ አለመሳካቱን አያብራራም። hostcensus ግልጽ የአገልግሎት ሁኔታዎችን፣ የተገደቡ ፍተሻዎችን፣ እንደገና ጥቅም ላይ ሊውሉ የሚችሉ የፍተሻ መገለጫዎችን እና የአካባቢ ታሪክን ያጣምራል። ኦፕሬተሮች ተመሳሳይ ወሰንን መድገም፣ ስህተቶችን መመርመር፣ እንዲሁም እርግጠኛ ያልሆኑ ምልከታዎችን ከተረጋገጡ ለውጦች መለየት ይችላሉ።

- **የአገልግሎት ማስረጃ፦** የSSH መለያ፣ የMySQL ሰላምታዎች፣ የHTTP ራስጌዎች፣ የTLS ሰርተፊኬት ምልከታዎች፣ እና የSNMP ፍለጋ ወይም በማረጋገጫ የሚካሄዱ የsystem-MIB መጠይቆች።
- **ተደጋጋሚ ወሰን፦** የተሰየሙ የTOML መገለጫዎች፣ ተደማሪ ማግለያዎች፣ ሊዋቀሩ የሚችሉ አገልግሎቶች፣ የአስተናጋጅ/ፍተሻ ገደቦች፣ እና የተገደቡ ሰራተኞች።
- **ከትራፊክ በፊት የሚደረጉ ፍተሻዎች፦** የአካባቢ preflight ዒላማዎችን፣ መሣሪያዎችን፣ የመድረሻ መዳረሻን፣ የታሪክ schema እና የተዋቀሩ የTLS CA ጥቅሎችን ያረጋግጣል።
- **የቆጠራ ታሪክ፦** ግብይት-ተኮር የSQLite ቅጽበታዊ ገጽ እይታዎች ሁሉንም ምልከታዎች ይይዛሉ፤ ንጽጽሮች የስካነር ውድቀቶችን እና ያልታወቁ ሁኔታዎችን በግልጽ ያሳያሉ።
- **ተኳኋኝ ውጤት፦** የተርሚናል፣ JSON እና CSV ሪፖርቶች፣ ስሪት የተሰጣቸው የፋይል ቅጽበታዊ ገጽ እይታዎች፣ እና የKadupul ማስገቢያ ስክሪፕቶች።

CI በLinux እና macOS ላይ Python 3.12፣ 3.13 እና 3.14ን፣ እንዲሁም ቁጥጥር የሚደረግበት የCompose ውህደት ላብራቶሪን ይሸፍናል። ኮዱ እነዚያን የአሂድ ጊዜ ስሪቶች እየጠበቀ ዘመናዊ type aliases፣ ዓይነት የተሰጣቸው የpreflight ውጤቶችን፣ ቁልፍ-ቃል ብቻ የሚቀበሉ slotted መገለጫዎችን እና የተዋቀረ async ጽዳትን ይጠቀማል። ለSemVer ተኳኋኝነት ውል እና ለGitHub ልቀት ሂደት [ስሪት አሰጣጥ እና ልቀቶች](../../../docs/releasing.md)ን ይመልከቱ። የልቀት ባጁ የሚገልጸው የታተሙ ቅርሶችን እንጂ ይህን ቅጂ አይደለም፦ በአሁኑ ጊዜ የቅርብ ጊዜው የታተመ መለያ `v0.3.0` ሲሆን፣ ይህ ቅጂ ግን የጥቅል ስሪት `3.0.0`ን ይጠቀማል። እዚህ የተዘገቡትን የቆጠራ ባህሪያት ለመጠቀም ከዚህ ቅጂ ይጫኑ።

በ[መጫን](#install) ይጀምሩ፣ ከዚያ ወደ [መገለጫዎች እና ታሪክ](#inventory-profiles-preflight-and-local-history) ይቀጥሉ። ለውህደት ዝርዝሮች [የአገልግሎት አሻራዎች](#fingerprints)፣ [የፋይል ንጽጽሮች](#inventory-diff) እና [የKadupul ወደ ውጭ መላክ](#kadupul-export)ን ይመልከቱ።

## መጫን

Python 3.12 ወይም ከዚያ በላይ ያስፈልጋል፤ Python 3.12-3.14 የተፈተነው ማትሪክስ ነው። ከዚህ ቅጂ፣ የተቆለፉትን የአሂድ ጊዜ ጥገኞች ይጫኑ፦

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

ለአማራጭ የNmap አስተናጋጅ ፍለጋ፣ የመድረክዎን ጥቅል አስተዳዳሪ በመጠቀም የNmap ፈጻሚ ፋይልን ይጫኑ፤ ምንም ተጨማሪ የPython ጥቅል አያስፈልግም። የNmap XML ውጤት ዋና ጥገኛ በሆነው defusedxml ስለሚተነተን፣ የentity expansion ውድቅ ይደረጋል። hostcensus በ`PATH` ላይ የሚገኘውን `nmap` በቀጥታ በተወሰነ የargument ዝርዝር፣ ከprefix መጠን ጋር በሚያድግ የጊዜ ገደብ እና በ64 MiB የውጤት ገደብ ያስኬዳል። ለነባሪው backend Nmap አያስፈልግም።

## ከnetprobe መሸጋገር

hostcensus በ3.0.0 የተለቀቀው የnetprobe አዲስ ስም ነው። ፕሮጀክቱ በሁለቱም ስሞች ወደ PyPI ታትሞ አያውቅም፣ ስለዚህ መጫኖች ከቅጂ ወይም ከGitHub ልቀት የመጡ ነበሩ። የGitHub ማከማቻው ስሙን እንደያዘ ይቆያል።

| ቀድሞ የነበረ | አሁን | ተኳኋኝነት |
| --- | --- | --- |
| የ`netprobe` ስርጭት | `hostcensus` | ከቅጂው እንደገና ይጫኑ፤ በአሮጌው ስም የተዘጋጀ ጥቅል የለም። |
| የ`netprobe` ትዕዛዝ | `hostcensus` | `netprobe` አሁንም ይሰራል እና በstderr ላይ አንድ የጊዜ ያለፈበት ማስጠንቀቂያ መስመር ያትማል። የመውጫ ኮዶች እና stdout አልተለወጡም። በቀጣዩ ዋና ልቀት ይወገዳል። |
| የ`NETPROBE_*` አካባቢ ተለዋዋጮች | `HOSTCENSUS_*` | ተጓዳኙ `HOSTCENSUS_*` ሳይዋቀር ሲቀር የ`NETPROBE_*` ተለዋዋጭ ጥቅም ላይ ይውላል፣ የተለዋዋጮቹን ስም እንጂ እሴቶቻቸውን በፍጹም የማይጠቅስ አንድ የstderr ማስጠንቀቂያ ይሰጣል። ሁለቱም ሲዋቀሩ `HOSTCENSUS_*` ቅድሚያ ያገኛል። በቀጣዩ ዋና ልቀት ይወገዳል። |
| `import netprobe`፣ `python -m netprobe` | `import hostcensus`፣ `python -m hostcensus` | **ተኳኋኝነትን የሚሰብር።** ምንም የimport መሸጋገሪያ አልተጫነም፤ importsን ያዘምኑ። |
| የDocker ምስል መለያ `network-discovery:test` (CI ብቻ) እና የኮንቴይነር ተጠቃሚ `netprobe` | `hostcensus:test`፣ ተጠቃሚ `hostcensus` | ምንም የregistry ምስል ታትሞ አያውቅም። ምስሉን እንደገና ይገንቡ እና የ`hostcensus` entrypoint ይጠቀሙ። |
| `netprobe.toml`፣ `netprobe-history.sqlite3` | `hostcensus.toml`፣ `hostcensus-history.sqlite3` | አዲሱ ስም እስካልተፈጠረ ድረስ በአሮጌው ነባሪ ስም ያለ ፋይል ከማስጠንቀቂያ ጋር አሁንም ጥቅም ላይ ይውላል። በግልጽ የተሰጡ `--config` እና `--history` መንገዶች አይነኩም። |
| `"format": "netprobe-report"` ወይም `"netprobe-snapshot"` ያላቸው ሪፖርቶች እና ቅጽበታዊ ገጽ እይታዎች፣ እንዲሁም `netprobe_version` መስክ | `hostcensus-report`፣ `hostcensus-snapshot`፣ `hostcensus_version` | `diff` እና `export` በአሮጌው ስም የተጻፉ ፋይሎችን አሁንም ይጭናሉ፣ የታተሙት JSON Schemas ደግሞ ሁለቱንም አጻጻፎች ይቀበላሉ። አዲስ ፋይሎች አዲሶቹን ስሞች ይጠቀማሉ። የSQLite ታሪክ ዳታቤዞች አልተለወጡም እና እንደ ቀድሞው ይጫናሉ። |
| ከ`netprobe export` የመነጩ የKadupul ስክሪፕቶች | ከ`hostcensus export` የሚመነጩ ስክሪፕቶች | አሮጌ ስክሪፕቶች መሥራታቸውን ይቀጥላሉ እና ሲሄዱ አሁንም `NETPROBE_SNMP_*`ን ያነባሉ። አዲስ ስክሪፕቶች `HOSTCENSUS_SNMP_*`ን ያነባሉ። |

## ፈጣን ምሳሌ

በልማት ክፍል ስር ከተገለጸው የውህደት ላብራቶሪ ሞካሪ ኮንቴይነር የታዘዘ፤ ውጤቱ ተቆርጦ ቀርቧል፦

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

## የመውጫ ኮዶች

| ትዕዛዝ | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | ምልከታዎች/ሪፖርት ተመዝግበዋል | የpreflight/backend፣ የታሪክ ወይም የሪፖርት/ቅጽበታዊ ገጽ እይታ መጻፍ አልተሳካም | ልክ ያልሆነ ዒላማ፣ አማራጮች፣ ውቅረት ወይም ገደቦች | - | `--deadline` ደርሷል፤ ከፊል ሪፖርት ተጽፏል፣ ታሪክ እና ቅጽበታዊ ገጽ እይታ ታልፈዋል |
| `preflight` | ፍተሻዎች አልፈዋል | የአካባቢ ፍተሻ አልተሳካም | ልክ ያልሆነ ዒላማ/ውቅረት ወይም የሚጋጩ መድረሻዎች | - | - |
| `profiles` | የተረጋገጡ መገለጫዎች ተዘርዝረዋል | - | የማይነበብ/ልክ ያልሆነ ውቅረት ወይም ምርጫ | - | - |
| `history` | ማጠቃለያዎች ተዘርዝረዋል | የጠፋ፣ ልክ ያልሆነ ወይም የማይደገፍ ታሪክ | ልክ ያልሆኑ የCLI አማራጮች | - | - |
| `compare` | ለውጦች ሲኖሩም ጭምር ንጽጽር ተዘጋጅቷል | የማይነበብ ታሪክ፣ የማይጣጣም ወሰን/ቅደም ተከተል ወይም የመጻፍ ውድቀት | ልክ ያልሆኑ የCLI አማራጮች | - | - |
| `diff` | ምንም ለውጥ የለም | የ`-o` ፋይል ሊጻፍ አልቻለም | የጠፋ፣ የማይነበብ ወይም የማይደገፍ ግብዓት፣ ወይም ያለ `--allow-partial` ያልተጠናቀቀ ፍተሻ | ለውጦች ተገኝተዋል፣ ያልተረጋገጡ ምልከታዎች ወይም ያልተጠናቀቀ ፍተሻ | - |
| `export` | ስክሪፕት ተጽፏል | ስክሪፕት ሊጻፍ አልቻለም | የማይነበብ ግብዓት፣ ያለ `--allow-partial` ያልተጠናቀቀ ፍተሻ፣ ወይም በደህና ወደ ውጭ ሊላክ የማይችል ውሂብ | - | - |

## አወቃቀር

| ሞጁል | ኃላፊነት |
| --- | --- |
| `cli.py` | የትዕዛዝ አማራጮች፣ የመገለጫ መፍታት፣ preflight፣ ፍተሻ እና ሪፖርት ማድረግ |
| `scanner.py`፣ `probes.py` | የዒላማ ማስፋፊያ፣ የተገደቡ ሰራተኞች፣ የአስተናጋጅ ፍለጋ እና የአገልግሎት ምልከታዎች |
| `config.py`፣ `profiles.py` | የአገልግሎት ትርጓሜዎች እና የተረጋገጡ የቆጠራ መገለጫዎች |
| `models.py`፣ `output.py` | የውጤት ዓይነቶች እና የተርሚናል/JSON/CSV አቀራረብ |
| `history.py`፣ `diff.py` | የSQLite ታሪክ እና ስሪት የተሰጣቸው የፋይል ቅጽበታዊ ገጽ እይታ ንጽጽሮች |
| `preflight.py` | የአካባቢ ፍተሻዎች እና የተገደበ የNmap ስሪት ፍለጋ |
| `export.py` | የተረጋገጡ እና በshell ጥቅስ የተጠበቁ የKadupul ማስገቢያ ስክሪፕቶች |

እያንዳንዱ የአገልግሎት ምልከታ ሁኔታውን ከሚያስተዋውቀው መለያ ተነጥሎ ይመዘግባል።
ንባቦች እና የጊዜ ገደቦች የተገደቡ ናቸው፤ የፍተሻ ልዩ ስህተቶች በአስተናጋጅ ስህተቶች ውስጥ ይቀራሉ። የSQLite ታሪክ ግብይቶችን፣ ግልጽ የግንኙነት ጽዳትን እና ለንባብ ብቻ የሆኑ የዝርዝር እና የንጽጽር መንገዶችን ይጠቀማል። የSNMP ምስጢሮች የሚገቡት በአካባቢ ተለዋዋጮች ወይም በምስጢር ፋይሎች በኩል ብቻ ነው፤ የቆጠራ ታሪክ ምስጢር ያልሆኑ ውጤታማ ቅንብሮችን ያከማቻል። ስለ ፍተሻ ሂደት መስመር፣ ገደቦቹ እና የእምነት ወሰኖቹ [አርክቴክቸር](../../../docs/architecture.md)ን፣ ስለ ተፈቀደ አጠቃቀም ደግሞ [SECURITY.md](../../../SECURITY.md#authorized-use)ን ይመልከቱ።


## አጠቃቀም

የሚያስተዳድሯቸውን አውታረ መረቦች ብቻ ይፈትሹ።

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| አማራጭ | ትርጉም |
| --- | --- |
| `NETWORK` | CIDR፣ IP ወይም hostname፤ ከ`--profile` ጋር አማራጭ ነው። የIPv6 scope መለያዎች ውድቅ ይደረጋሉ። |
| `-o, --output PATH` | ሪፖርት ይጽፋል። ቅርጸቱ ቅጥያውን (`.json`፣ `.csv`) ይከተላል፤ ሌሎች ቅጥያዎች ወደ JSON ይመለሳሉ። |
| `-f, --format json\|csv\|kadupul\|auto` | የሪፖርት ቅርጸቱን ያስገድዳል። ያለ `--output` ምንም ውጤት የለውም። `.sh` `kadupul`ን ይመርጣል። |
| `-v, --verbose` | የdebug ምዝገባ። |
| `-q, --quiet` | ውጤቶችን፣ ሂደትን እና መረጃ ሰጪ ምዝግቦችን ይደብቃል፤ ማስጠንቀቂያዎች እና ስህተቶች አሁንም በstderr ላይ ይታያሉ። |
| `--backend asyncio\|nmap` | የአስተናጋጅ ፍለጋ። `asyncio` (ነባሪ) የአገልግሎት ወደቦችን በቀጥታ ይፈትሻል፤ `nmap` በመጀመሪያ የnmap ping sweep ያካሂዳል እና በ`PATH` ላይ የ`nmap` ፈጻሚ ፋይል ያስፈልገዋል። |
| `--timeout SECONDS` | የራሳቸውን የጊዜ በጀት ላልወሰኑ ፍተሻዎች የሚቆይበት ጊዜ (ነባሪ 1.0)። የአገልግሎት ሰንጠረዡ `timeout` እስካልወሰነ ድረስ አብሮ የተሰሩ የconnect ፍተሻዎች 0.3 ሰከንድ ይጠቀማሉ። |
| `--concurrency N` | በአንድ ጊዜ የሚካሄዱ ፍተሻዎች ብዛት (ነባሪ 256)። |
| `--deadline SECONDS` | የnmap ፍለጋን ጨምሮ ሙሉውን ፍተሻ ከዚህ ጊዜ በኋላ ያቆማል (ነባሪ 3600፣ ቢበዛ 604800፤ የአካባቢ ተለዋዋጭ `HOSTCENSUS_DEADLINE`)። የተጠናቀቁ አስተናጋጆች በ`"complete": false` ወደ ሪፖርቱ ይጻፋሉ፣ ታሪክ ወይም ቅጽበታዊ ገጽ እይታ አይጻፍም፣ እና `scan` በ4 ይወጣል። |
| `--config PATH` | የTOML አገልግሎት ትርጓሜዎች እና አማራጭ የተሰየሙ `[profiles]` ቅንብሮች። |
| `--profile NAME` | የተሰየመ መገለጫ ይጠቀማል፤ `--config` ሲቀር ነባሪው `hostcensus.toml` ነው። |
| `--exclude IP/CIDR` | ማግለያ ያክላል፤ እንደ አስፈላጊነቱ ይደግሙት። የተገለለ የIPv4 አስተናጋጅ ወደ እሱ የሚያደርሱትን የIPv6 አድራሻዎችንም ያገላል፦ IPv4-mapped (`::ffff:a.b.c.d`)፣ NAT64 (`64:ff9b::/96`) እና 6to4። IPv4-mapped ዒላማዎች እና ማግለያዎች እንደሚወክሉት የIPv4 አድራሻ ይቆጠራሉ። |
| `--max-hosts N` | ከማግለያዎች በፊት የሚረጋገጥ የአድራሻ ገደብ (ነባሪ/ከፍተኛ ገደብ 65,536)። |
| `--history PATH` | የተጠናቀቀውን ፍተሻ በፈቃደኝነት በሚመረጥ የSQLite ታሪክ ዳታቤዝ ውስጥ ይመዘግባል። |
| `--services NAMES` | በዚያ ቅደም ተከተል የሚፈተሹ የአገልግሎት ስሞች በነጠላ ሰረዝ የተለዩ ዝርዝር (ነባሪ፦ ሁሉም)። |
| `--ports SPEC` | በነጠላ ሰረዝ የተለዩ `NAME=PORT` (አገልግሎትን ለማዛወር) ወይም `PORT` (`tcp-PORT` የተሰየመ ተራ TCP ፍተሻ ለማከል) ዝርዝር። |
| `--snmp-community-file PATH` | ለsystem MIB መጠይቅ የSNMPv2c community የያዘ ፋይል። የአካባቢ ተለዋዋጭ፦ `HOSTCENSUS_SNMP_COMMUNITY` (እሴቱ) ወይም `HOSTCENSUS_SNMP_COMMUNITY_FILE` (መንገዱ)። |
| `--snmp-user` | የSNMPv3 ተጠቃሚ። የአካባቢ ተለዋዋጭ፦ `HOSTCENSUS_SNMP_USER`። |
| `--snmp-auth-protocol`፣ `--snmp-auth-key-file PATH` | `MD5`፣ `SHA` (ነባሪ)፣ `SHA224`፣ `SHA256`፣ `SHA384`፣ `SHA512` እና የይለፍ ሐረጉን የያዘ ፋይል። የአካባቢ ተለዋዋጭ፦ `HOSTCENSUS_SNMP_AUTH_PROTOCOL`፣ `HOSTCENSUS_SNMP_AUTH_KEY` ወይም `HOSTCENSUS_SNMP_AUTH_KEY_FILE`። |
| `--snmp-priv-protocol`፣ `--snmp-priv-key-file PATH` | `DES`፣ `AES` (ነባሪ)፣ `AES128`፣ `AES192`፣ `AES192C`፣ `AES256`፣ `AES256C` እና የይለፍ ሐረጉን የያዘ ፋይል። የአካባቢ ተለዋዋጭ፦ `HOSTCENSUS_SNMP_PRIV_PROTOCOL`፣ `HOSTCENSUS_SNMP_PRIV_KEY` ወይም `HOSTCENSUS_SNMP_PRIV_KEY_FILE`። |
| `--save-snapshot PATH` | ለ`hostcensus diff` ስሪት የተሰጠው ቅጽበታዊ ገጽ እይታም ይጽፋል። |
| `--tls-ca-file PATH` | ከስርዓቱ ማከማቻ ይልቅ የHTTPS ሰርተፊኬቶችን በዚህ የPEM ጥቅል ላይ ያረጋግጣል። የአካባቢ ተለዋዋጭ፦ `HOSTCENSUS_TLS_CA_FILE`። |

በነባሪ እያንዳንዱ አስተናጋጅ ለSSH (TCP 22)፣ SNMP (UDP 161)፣ MySQL (TCP 3306)፣ HTTP (TCP 80) እና HTTPS (TCP 443) ይፈተሻል። የTCP ወደቦች በሙሉ ግንኙነት ይፈተሻሉ። SNMP የሚፈተሸው ማንኛውም የSNMPv3 ወኪል ያለ ማረጋገጫ መመለስ ባለበት የSNMPv3 engine-discovery ጥያቄ ነው፤ v1/v2c ብቻ የሚናገሩ ወኪሎች በዚህ ፍተሻ አይታወቁም። በasyncio backend ማንኛውም ፍተሻ ምላሽ ሲያገኝ (የተከለከለ ግንኙነትን ጨምሮ) አስተናጋጁ ሕያው እንደሆነ ይቆጠራል፣ ስለዚህ እያንዳንዱን ፍተሻ የሚጥል አስተናጋጅ `alive=false` እና "Host is down" የሚል ስህተት ይኖረዋል፤ ይህ በአካል መጥፋቱን አያረጋግጥም። በ`--backend nmap` የትኞቹ አስተናጋጆች ሕያው እንደሆኑ nmap ይወስናል (እንደ root ICMP፣ ካልሆነ TCP 80/443)።

### የአገልግሎት አሻራዎች

እያንዳንዱ ክፍት አገልግሎት ከማንኛውም መግቢያ በፊት ከሚልከው መረጃ አሻራው ይወሰዳል። ከSNMP መጠይቅ በስተቀር ምንም ነገር ማረጋገጫ አያደርግም፣ እሱም ማረጋገጫዎችን ሲያቀርቡ ብቻ ነው።

| ፍተሻ | የሚያነበው | `version` | የ`details` ቁልፎች |
| --- | --- | --- | --- |
| `ssh` | የRFC 4253 መለያ መስመር | ሶፍትዌር፣ ለምሳሌ `OpenSSH_10.0` | `protocol`፣ `software`፣ `comments` |
| `mysql` | የMySQL/MariaDB መጀመሪያ handshake | የሰርቨር ስሪት | `server_version`፣ `flavor`፣ `auth_plugin` ወይም `error_code`/`error` |
| `http` | የ`HEAD /` ምላሽ | `Server` ራስጌ | `status`፣ `server` |
| `https` | የTLS handshake፣ ሰርተፊኬት፣ `HEAD /` | `Server` ራስጌ | `tls_version`፣ `cert_verified`፣ `cert_verify_error`፣ `cert_subject`፣ `cert_issuer`፣ `cert_sans`፣ `cert_not_before`፣ `cert_not_after` (UTC ISO 8601)፣ `cert_self_signed`፣ `status`፣ `server` |
| `snmp` | የSNMPv3 ፍለጋ፤ ከማረጋገጫዎች ጋር የsysDescr፣ sysObjectID፣ sysName GET | sysDescr | `engine_id`፤ ከማረጋገጫዎች ጋር `snmp_version`፣ `sys_descr`፣ `sys_object_id`፣ `sys_name` ወይም `snmp_error` |

የhostname ዒላማ በአንድ አስተናጋጅ አንድ ጊዜ ይፈታል እና እያንዳንዱ ፍተሻ በውጤቶቹ ውስጥ `address` ተብሎ ወደ ተመዘገበው አድራሻ ይገናኛል፤ ስሙ ጥቅም ላይ የሚውለው ለTLS SNI፣ ለሰርተፊኬት ማረጋገጫ እና ለHTTP `Host` ራስጌ ብቻ ነው። የማይፈታ ስም `unknown` ሁኔታዎችን እና `Cannot resolve` ስህተትን ይሰጣል። የተገላቢጦሽ DNS ስሞች የሚቀመጡት የhostname ቁምፊዎችን ሲይዙ ብቻ ሲሆን፣ በአንድ ጊዜ ቢበዛ 16 ፍለጋዎች ይካሄዳሉ። HTTPS በስርዓቱ ማከማቻ ወይም `--tls-ca-file` ላይ የሰርተፊኬት እና የhostname ማረጋገጫን ይጠቀማል። የእምነት ማከማቻው ለፍተሻው አንድ ጊዜ ይጫናል እና ለእያንዳንዱ የHTTPS ፍተሻ እንደገና ጥቅም ላይ ይውላል። የTCP ግንኙነት እና የTLS handshake ጊዜያቸው ለየብቻ ይሰላል፣ ስለዚህ ግንኙነቶችን የሚቀበል ነገር ግን handshakeን የሚያዘገይ ወደብ `filtered` ሳይሆን `open` ከ`tls_error` ጋር ይሆናል። ማረጋገጫው ካልተሳካ ውጤቱ `cert_verified: false` እና `cert_verify_error`ን ይመዘግባል፤ በደካማ ቅንብሮች እንደገና አይሞክርም ወይም የHTTP ጥያቄ አይልክም። የሰርተፊኬት ዝርዝሮች እና የHTTP ራስጌዎች የሚሰበሰቡት ማረጋገጫው ከተሳካ በኋላ ብቻ ነው። ለግል-CA አገልግሎቶች ትክክለኛውን የCA ጥቅል ያቅርቡ። የድሮ ሪፖርቶች የአሁኑ ፍተሻዎች የማያመርቱትን `cert_read_unverified` ሊይዙ ይችላሉ።

የSNMP ምስጢሮች የሚነበቡት ከአካባቢ ተለዋዋጮች ወይም ከፋይሎች (`--snmp-*-file` ወይም ተዛማጁ `HOSTCENSUS_SNMP_*_FILE` ተለዋዋጭ) ብቻ ነው፤ ሌሎች የአካባቢ ተጠቃሚዎች በሂደት ዝርዝር ውስጥ ሊያዩዋቸው ከሚችሉ የትዕዛዝ-መስመር እሴቶች በፍጹም አይነበቡም። `--snmp-community`፣ `--snmp-auth-key` እና `--snmp-priv-key` ከእሴት ጋር ሲሰጡ በመውጫ ኮድ 2 ይወጣሉ እና ምትኩን ይጠቅሳሉ። የምስጢር ፋይል ባዶ ያልሆነ እና ቢበዛ 4096 ባይት የሆነ UTF-8 መሆን አለበት፤ አንድ የመጨረሻ አዲስ መስመር ችላ ይባላል፣ እና ለተመሳሳይ ምስጢር ሁለቱንም ተለዋዋጭ እና ፋይል ማዋቀር ስህተት ነው። ስህተቶች የፋይሉን ስም ይጠቅሳሉ ነገር ግን ይዘቱን በፍጹም አያትሙም። የፍተሻ ሪፖርቶች እና ታሪክ ሆን ብለው የማረጋገጫ እሴቶችን አያካትቱም። ወደ ውጭ ላኪው ከዚህ በታች የተገለጸ የተለየ እና ግልጽ የሆነ `--include-credentials` አማራጭ አለው። community SNMPv2cን ይመርጣል፤ ተጠቃሚ SNMPv3ን ይመርጣል፣ የauth ቁልፍ ሲሰጥ ማረጋገጫ፣ ሁለቱም ቁልፎች ሲሰጡ ደግሞ ግላዊነት ይኖረዋል (`snmp_security_level` የትኛው እንደሆነ ይመዘግባል)። hostcensus communityን ከv3 ተጠቃሚ ጋር ማጣመርን፣ ያለ auth ቁልፍ የprivacy ቁልፍ መጠቀምን፣ ወይም ያለ ተጠቃሚ ቁልፎችን መጠቀምን በመውጫ ኮድ 2 ውድቅ ያደርጋል፣ እንዲሁም ያልተሳካ የv3 መጠይቅን በv2c ወይም በዝቅተኛ የደህንነት ደረጃ በፍጹም እንደገና አይሞክርም። v1/v2c ብቻ የሚናገሩ ወኪሎች ማረጋገጫ-አልባውን የv3 ፍለጋ ችላ ስለሚሉ፣ ክፍት ሆነው የሚታዩት community ሲቀርብ ብቻ ነው።

የባነር ጽሑፍ ከመቀመጡ ወይም ከመታየቱ በፊት ወደ ሊታተሙ የሚችሉ ቁምፊዎች ይቀነሳል እና በ256 ቁምፊዎች ይገደባል። ንባቦችም የተገደቡ ናቸው፦ በአንድ መስመር 4 KiB፣ ለMySQL ሰላምታ 4 KiB፣ ለHTTP ራስጌዎች 16 KiB። ከ32 octets በላይ የሆነ የSNMP engine ID ከመቀመጡ በፊት ይቆረጣል። HTTP እና HTTPS የIPv6 አድራሻን በቅንፍ ውስጥ በማስገባት እና ወደቡ 80 ወይም 443 ካልሆነ ከወደቡ ጋር የHost ራስጌ ይልካሉ። በስፕሬድሺት ፎርሙላ ቀስቃሽ የሚጀምሩ የCSV ሕዋሶች ጽሑፍ ሆነው እንዲቆዩ ቅድመ ቅጥያ ይደረግባቸዋል።

### ገደቦች

አንድ አሂድ ቢበዛ 65,536 አድራሻዎችን፣ 64 አገልግሎቶችን እና 524,288 ፍተሻዎችን (አስተናጋጆች ሲባዛ በአገልግሎቶች) ይቀበላል፤ ከዚህ የበለጡ ጥያቄዎች ምንም ነገር ከመላኩ በፊት በመውጫ ኮድ 2 ይወጣሉ። `--concurrency` በ4096 ሶኬቶች የተገደበ ነው። እያንዳንዱ ፍተሻ የራሱ በጀት አራት እጥፍ የሆነ ጥብቅ የጊዜ ገደብ አለው። የconnect ፍተሻዎች (`tcp`፣ `ssh`፣ `mysql`፣ `http`) ያ አገልግሎት `timeout` ካላስቀመጠ በስተቀር 0.3 ሰከንድ ይጠቀማሉ። SNMP እና HTTPS ራሳቸው ሳያስቀምጡ ሲቀሩ `--timeout` (ነባሪ 1.0) ይጠቀማሉ። የጊዜ ገደቡን የደረሰ ፍተሻ በ`errors` ውስጥ "probe timed out" ተብሎ `unknown` ሆኖ ሪፖርት ይደረጋል። የአካባቢ ሶኬት ውድቀቶች (ለምሳሌ የፋይል ገላጮች ማለቅ) ስህተቱ ተመዝግቦ `unknown` ይሆናሉ፤ እንደ ተጣራ ወደብ ወይም እንደ ጠፋ አስተናጋጅ በፍጹም አይቆጠሩም። ፍተሻ ከመጀመሩ በፊት hostcensus `--concurrency` ሲደመር 64 ገላጮችን ለመያዝ የክፍት-ፋይል ለስላሳ ገደብን ወደ ጥብቅ ገደቡ ከፍ ያደርጋል፤ ይህን ማድረግ ሳይችል ሲቀር የ`open files` preflight ፍተሻ አይሳካም እና `scan` ትራፊክ ከመላኩ በፊት በ1 ይወጣል። የNmap ፍለጋ የ30 ሰከንድ የአስተናጋጅ ጊዜ ማለቂያ ይጠቀማል። prefix ወደ nmap የሚተላለፈው በCIDR መልክ ነው፣ እና nmap ከተሰጠው ያነሰ አድራሻ ሲያሳውቅ (ለምሳሌ መፍታት የማይችለው ስም ሲኖር) አስተናጋጆችን እንደ ጠፉ ከመቁጠር ይልቅ ፍለጋው በመውጫ ኮድ 1 ይወድቃል። የhostname ዒላማ አንድ ጊዜ ተፈትቶ ያ አድራሻ ለnmap ይሰጣል፣ ስለዚህ ፍለጋው እና ፍተሻዎቹ ተመሳሳይ ማሽን ላይ ይደርሳሉ። ሙሉ prefix አንድ የnmap ሂደት ሲሆን የንዑስ ሂደቱ የጊዜ ገደብ ለእያንዳንዱ 256 አድራሻዎች 35 ሰከንድ ወደ ላይ ተጠጋግቶ ይሰላል። ማግለያዎች ያሏቸው ፍለጋዎች የ256 አስተናጋጆች ስብስቦችን እና ለእያንዳንዱ ስብስብ የ35 ሰከንድ የጊዜ ገደብ ይጠቀማሉ። የሰራተኞች መፈጠር ከክልሉ መጠን ተነጥሎ የተገደበ ነው። የተገላቢጦሽ DNS እና የhostname መፍታት የተለየ የሁለት ሰከንድ የጊዜ ገደብ አላቸው፤ በፍጹም የማይመለስ የresolver ጥሪ በራሱ ክር ላይ ይተዋል፣ ስለዚህ hostcensus ከእነዚህ ገደቦች በላይ እንዲቆይ ሊያደርገው አይችልም። በአንድ ጊዜ ቢበዛ 16 ፍለጋዎች ይካሄዳሉ፣ እና የተተወ ጥሪ እስኪመለስ ድረስ ቦታውን ይይዛል፣ ስለዚህ የተጣበቁ ክሮች ቁጥር የተገደበ ሆኖ ይቆያል፤ ሁሉም 16 ከተሰቀሉ፣ ቀጣይ ፍለጋዎች `--deadline` ፍተሻውን እስኪያቆም ድረስ ከሁለት ሰከንድ ገደቡ ውጭ (ቦታ ሲለቀቅ የሚጀምር) ቦታ ለማግኘት ወረፋ ይይዛሉ። ያለ `deadline` እንደ ቤተ-መጽሐፍት የሚያገለግል `NetworkScanner` ለእንዲህ ዓይነቱ ቦታ ላልተወሰነ ጊዜ ሊጠብቅ ይችላል። `--deadline` (ነባሪ አንድ ሰዓት) ከእነዚህ ሁሉ በላይ ሙሉውን አሂድ ይገድባል።

### አገልግሎቶችን ማዋቀር

አገልግሎቶች በTOML ፋይል ሊቀየሩ ይችላሉ፦

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` ከ`tcp`፣ `ssh`፣ `mysql`፣ `http`፣ `https` ወይም `snmp` አንዱ ሲሆን፣ የአገልግሎቱ ስም probe ከሆነ በነባሪ እሱን ይወስዳል፣ ካልሆነ `tcp` ይሆናል። UDP የሚጠቀመው `snmp` ብቻ ነው። የአገልግሎት ስሞች ትናንሽ የላቲን ፊደላት፣ አሃዞች፣ `-` እና `_` ናቸው። ሁለት አገልግሎቶች አንድ ወደብ እና ፕሮቶኮል ሊጋሩ አይችሉም፤ ታሪክ ለዚያ ጥንድ አንድ ሁኔታ ይመዘግባል። `timeout` አማራጭ፣ በሰከንዶች የሚገለጽ እና ቢያንስ 0.05 ነው። የconnect ዓይነት ፍተሻዎች (`tcp`፣ `ssh`፣ `mysql`፣ `http`) በነባሪ 0.3 ሰከንድ ናቸው። `snmp` እና `https` አገልግሎቱ `timeout` ሳያስቀምጥ ሲቀር የፍተሻውን `--timeout` ይጠቀማሉ። `--timeout` አገልግሎቱ ቀድሞ ያለውን በጀት አይተካም።

የJSON ሪፖርቶች ከ`devices` ጎን ለጎን ዒላማውን፣ የተፈተሹ አገልግሎቶችን እና ቅንብሮችን የሚመዘግቡ ስሪት የተሰጣቸው ሰነዶች (`"format": "hostcensus-report"`፣ `"version": 1`) ናቸው፤ ያለ `-o` የሚሰጥ `--format json` ከሰንጠረዡ ይልቅ ሪፖርቱን ወደ stdout ይጽፋል። እያንዳንዱ የJSON ውጤት የታተመ schema አለው፤ [የJSON ውጤት](../../../docs/json-output.md)ን ይመልከቱ። መሣሪያዎች ዋናዎቹን `ip`፣ `alive`፣ `ssh`፣ `snmp`፣ `mysql`፣ `hostname` እና `errors` መስኮች ይይዛሉ እና የእያንዳንዱን ፍተሻ `name`፣ `port`፣ `protocol`፣ `state` (`open`፣ `closed`፣ `filtered` ወይም ፍተሻው በአካባቢ ሲወድቅ ወይም የጊዜ ገደቡ ሲደርስ `unknown`)፣ `version` እና `details` የያዘ `services` ዝርዝር ያክላሉ። የCSV ውጤት ለክፍት አገልግሎቶች የመጨረሻ `services` እና `versions` አምዶችን ያገኛል። የ`ssh`፣ `snmp` እና `mysql` ቡሊያኖች በትክክል እነዚያን ስሞች የያዙ አገልግሎቶችን ይከተላሉ።


## የቆጠራ መገለጫዎች፣ preflight እና የአካባቢ ታሪክ

የተሰየሙ መገለጫዎች ከነባር `[services]` ትርጓሜዎች ጋር አንድ የTOML ፋይል ይጋራሉ። [hostcensus.example.toml](../../../hostcensus.example.toml)ን ወደ `hostcensus.toml` ይቅዱ እና እርስዎ የሚያስተዳድሯቸውን አውታረ መረቦች ያዋቅሩ፦

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

`preflight` ለክፍት-ፋይል ፍተሻ `--concurrency`ን ጨምሮ አማራጮችን እና መገለጫዎችን ልክ እንደ `scan` ይፈታል፣ ስለዚህ ያለፈ preflight `scan` በተመሳሳይ ዕቅድ እንደሚጀምር ያሳያል።

መገለጫዎች `network`፣ `exclusions`፣ `services`፣ `ports`፣ `backend`፣ `timeout`፣ `concurrency` እና `max_hosts`ን ይቀበላሉ። `services` እና `ports` ነባሩን በነጠላ ሰረዝ የተለየ ዝርዝር አገባብ ይጠቀማሉ። በግልጽ የተሰጡ የCLI አማራጮች የመገለጫ ቅንብሮችን ይሽራሉ፤ የተደጋገሙ `--exclude` አማራጮች በመገለጫ ማግለያዎች ላይ ይደመራሉ። ከ`--profile` ጋር በግልጽ የሚሰጥ አውታረ መረብ በዚያ መገለጫ የIP/CIDR ወሰን ውስጥ መካተት አለበት። Hostnames ለቀጥታ ፍተሻዎች አሁንም ይደገፋሉ፣ ነገር ግን ከIP ማግለያዎች ጋር ሊጣመሩ አይችሉም። የአስተናጋጅ ገደቦች ከማግለያዎች በፊት ይተገበራሉ፤ አጠቃላይ የፍተሻ ገደቡ ግን ከዚያ በኋላም ይተገበራል። የተገለሉ አስተናጋጆች ከአገልግሎት ፍተሻዎችም ሆነ ከአማራጭ የNmap ፍለጋ ይቀነሳሉ።

እያንዳንዱ ፍተሻ ወደ ዒላማው ትራፊክ ከመላኩ በፊት የአካባቢ preflight ፍተሻዎችን ያካሂዳል፦ የዒላማ/ፍተሻ ገደቦች፣ የመድረሻ መዳረሻ፣ አማራጭ የNmap ፈጻሚ/wrapper መገኘት፣ የታሪክ schema እና የተዋቀረ የTLS CA ጥቅል። `preflight` JSON ሪፖርት ያደርጋል እና ዒላማዎችን አይፈትሽም ወይም የታሪክ ዳታቤዝ አይፈጥርም። ነባር ይዘቶችን ሳይለውጥ የመድረሻ መዳረሻን ለመፈተሽ በጊዜያዊነት አንድ ጎረቤት ፋይል ይጽፋል። ነባሪው asyncio backend አሁንም Nmapንም ሆነ rootን አይፈልግም። የመድረሻ መንገዶች hard linksን ጨምሮ እርስ በርሳቸው እና ከግብዓት ውቅረቱ የተለዩ መሆን አለባቸው፤ የመድረሻ symlinks ውድቅ ይደረጋሉ። ያልተሳኩ ፍተሻዎች 1 ይመልሳሉ፤ ልክ ያልሆነ ወሰን/ውቅረት 2 ይመልሳል።

የሪፖርት እና የወደ ውጭ መላክ ጽሑፎች የ`O_NOFOLLOW` ድጋፍን ይፈልጋሉ። ይህ በሌለባቸው መድረኮች ላይ (Windowsን ጨምሮ) እነዚህ ጽሑፎች መድረሻውን ሳይከፍቱ ወይም ሳይቆርጡ ይወድቃሉ። አዲስ ሪፖርቶች እና የወደ ውጭ መላክ ስክሪፕቶች ለባለቤቱ ብቻ የተፈቀዱ (mode 0600) ናቸው፤ ነባር ፋይልን መተካት ፈቃዶቹን ይጠብቃል። አንባቢ ወደ ሌለው named pipe መጻፍ ከመጠበቅ ይልቅ ወዲያውኑ ይወድቃል። አዲስ `--history` ዳታቤዝም ለባለቤቱ ብቻ ሆኖ ይፈጠራል፤ ነባሩ ግን modeውን ይጠብቃል። የምዝገባ መልዕክቶች ሁልጊዜ ወደ stderr ስለሚሄዱ stdout ውጤቶችን ብቻ ይይዛል። ማረጋገጫዎችን የያዙ ወደ ውጭ መላኮች ሁልጊዜ mode 0600ን ያስገድዳሉ።

ታሪክ በፈቃደኝነት የሚመረጥ ሲሆን ነባሮቹን የJSON ቅጽበታዊ ገጽ እይታዎች እና `diff` ትዕዛዝን ያሟላል፦

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

ከ`history` የተገኙ መለያዎችን ይጠቀሙ፤ ምሳሌው አዲስ ዳታቤዝ እንዳለ ያስባል። ቅጽበታዊ ገጽ እይታዎች በUTC መጀመሪያ/መጨረሻ ጊዜያት፣ በጥቅል ስሪት፣ ምስጢር ባልሆኑ ውጤታማ ቅንብሮች፣ ማጠቃለያዎች እና በእያንዳንዱ አስተናጋጅ ስህተቶችን ጨምሮ በሁሉም የአስተናጋጅ/አገልግሎት ምልከታዎች በግብይት መልክ ይቀመጣሉ። ያልተጠናቀቁ የአስተናጋጅ ምልከታዎች ይቀመጣሉ። የተሰረዙ አሂዶች አይቀመጡም። ነባር የሪፖርት፣ ቅጽበታዊ ገጽ እይታ፣ ወደ ውጭ መላክ እና የፍተሻ መውጫ-ኮድ ውሎች ይጠበቃሉ።

`history` ሁሉንም ታሪካዊ የመሣሪያ ጭነቶች ሳያነብ የJSON ማጠቃለያዎችን ይዘረዝራል።
`compare` ሁለት የተቀመጡ ፍተሻዎችን ያነባል፣ ተመሳሳይ የዒላማ መለያዎችን እና የተመረጡ ወደቦችን ይጠይቃል፣ እንዲሁም የምላሽ ሰጪነት፣ የሁኔታ እና የወደብ-ሁኔታ ለውጦችን ሪፖርት ያደርጋል። የቀደመው የፍተሻ መለያ ከኋለኛው መለያ መቅደም አለበት። ሁለቱም ፍተሻዎች `timeout` ወይም `backend` ሲመዘግቡ እና እነዚያ እሴቶች ሲለያዩ፣ ሪፖርቱ ማስጠንቀቂያ ይዘረዝራል እና ምልከታዎቹን ማወዳደሩን ይቀጥላል። የተለየ የመቆያ ጊዜ የተጣራ ወደብ ክፍት እንዲመስል ሊያደርግ ይችላል። የስካነር ስህተቶች እና ያልታወቁ የወደብ ምልከታዎች እንደ ተረጋገጠ መጥፋት ወይም መዘጋት ከመቆጠር ይልቅ እርግጠኛ ያልሆኑ ተብለው ምልክት ይደረግባቸዋል፦ ስህተት ያለባቸው አስተናጋጆች በ`uncertain_hosts` ውስጥ ይታያሉ፣ እና `unknown`ን የሚያካትት እያንዳንዱ የወደብ ሽግግር (በሁለቱም ፍተሻዎች unknown መሆንን ጨምሮ) ከኋለኛው ፍተሻ ላይ ክፍት ከሆነ ወደብ በስተቀር (እሱ የወደብ ለውጥ ነው) ከ`port_changes` ይልቅ በ`unconfirmed_ports` ውስጥ ይዘረዘራል። `compare` እና `diff` ወደቦችን በተመሳሳይ ሕግ ይመድባሉ።
`no_longer_responding` ማለት ምላሽ አለመኖር እንጂ የመሣሪያው መወገድ ማረጋገጫ አይደለም።
የፍተሻ መውጫ ኮድ 0 እያንዳንዱ አስተናጋጅ ምላሽ መስጠቱን አያረጋግጥም፦ በአስተናጋጅ ደረጃ ያሉ ስህተቶችን ይመርምሩ። የንጽጽር ስኬት ለውጦች ቢኖሩም ባይኖሩም 0 ይመልሳል፤ ነባሩ የፋይል `diff` የመውጫ ኮድ 3 ውሉን ይጠብቃል። የማይደገፍ ወይም የተበላሸ ታሪክ 1 ይመልሳል።

ታሪክ የቆጠራ መረጃን ስለሚያከማች፣ በተገቢው መንገድ የተጠበቀ የአካባቢ ማውጫ ይምረጡ። የመገለጫ ፋይሎች እና የተቀመጡ ቅንብሮች የSNMP ማረጋገጫዎችን አይይዙም፤ የማረጋገጫ አያያዝ በነባሩ የአሂድ ጊዜ አማራጮች/አካባቢ በኩል ይቀጥላል።

## የቆጠራ diff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

ቅጽበታዊ ገጽ እይታ `format: "hostcensus-snapshot"`፣ `version: 1`፣ የhostcensus ስሪት፣ የUTC የተፈጠረበት ጊዜ፣ ዒላማው፣ ፍተሻው ከመዘገባቸው የፍተሻ `timeout` እና `backend`፣ የተፈተሹ አገልግሎቶች፣ እና ልክ እንደ `-o` ሪፖርት ቅርጽ ሕያው አስተናጋጆችን የያዘ JSON ነው። የጠፉ አስተናጋጆች ይተዋሉ። `diff` የ`services` መስክ ከመኖሩ በፊት የነበሩትን ጨምሮ ተራ የ`scan -o` JSON ሪፖርቶችንም ይቀበላል።

`diff` አዲስ እና የጠፉ አስተናጋጆችን፣ በሁለቱም ውስጥ በሚገኙ አስተናጋጆች ላይ የተከፈቱ ወይም የተዘጉ ወደቦችን፣ እና `version` የተለወጠባቸውን አገልግሎቶች ሪፖርት ያደርጋል። ከሁለቱ ፍተሻዎች በአንዱ ብቻ የተፈተሹ ወደቦች አይወዳደሩም፣ ማስጠንቀቂያም ይህን ይገልጻል። ያልተሳኩ ምልከታዎች በፍጹም እንደ "ምንም ለውጥ የለም" አይነበቡም፦ በየትኛውም ፍተሻ `unknown` የሆነ እና በኋለኛው ክፍት ያልሆነ ወደብ ከ`closed` ይልቅ በ`unconfirmed` ስር ይዘረዘራል፣ `before` `open`፣ `unknown` ወይም `not-open` (ተፈትሾ የተዘጋ ወይም የተጣራ) እና `after` `unknown` ወይም `not-open` ይሆናል፤ አሁን ክፍት የሆነ ወደብ የቀደመው ፍተሻ ባይሳካም እንኳ በ`opened` ስር ሪፖርት ይደረጋል። በየትኛውም ፍተሻ ሁሉም ፍተሻዎቹ ያለ ምላሽ የወደቁበት አስተናጋጅ ከ`vanished_hosts` ይልቅ በ`unsettled_hosts` ስር ይዘረዘራል (በሁለቱም ፍተሻዎች ሲወድቅ ወይም ከሌላው ፋይል ሲጎድል ጨምሮ `before`/`after` `up`፣ `uncertain` ወይም `absent` ይሆናል)፤ በኋለኛው ፍተሻ ምላሽ ከሰጠ ከክፍት ወደቦቹ ጋር እንደ አዲስ አስተናጋጅም ሪፖርት ይደረጋል። ቅጽበታዊ ገጽ እይታዎች በዚህ ምክንያት እነዚያን ያልተሳኩ አስተናጋጆች ያስቀምጣሉ። ዒላማዎቹ ሲለያዩ፣ እንዲሁም ሁለቱም ፋይሎች timeout ወይም backend ሲመዘግቡ እና እነዚያ እሴቶች ሲለያዩ ማስጠንቀቂያ ይታያል። `-o PATH` የJSON ቅርጹን ወደ ፋይልም ይጽፋል።

በ`--deadline` ከቆመ ፍተሻ የወጣ ሪፖርት (`"complete": false`) የደረሰባቸውን አስተናጋጆች ብቻ ስለሚዘረዝር፣ `diff` እና `export` በመውጫ ኮድ 2 ውድቅ ያደርጉታል። `--allow-partial` በstderr ላይ ማስጠንቀቂያ በመስጠት ይቀበለዋል፦ ከዚያ `diff` ያልተጠናቀቀው ፍተሻ ጨርሶ ያልዘረዘራቸውን አስተናጋጆች ከጠፉ ይልቅ በ`unsettled_hosts` ስር እንደ `unscanned` ይዘረዝራል (እንደ ጠፋ የዘረዘረው አስተናጋጅ አሁንም የጠፋ ነው)፣ `partial`ን true ያደርጋል እና በፍጹም ምንም ለውጥ የለም ብሎ ሪፖርት አያደርግም፣ `export` ደግሞ በስክሪፕቱ ራስጌ ላይ ማስጠንቀቂያ ይጽፋል።

የ`diff` መውጫ ኮዶች፦ `0` ምንም ለውጥ የለም፣ `3` ለውጦች ተገኝተዋል፣ ሊረጋገጡ ያልቻሉ ምልከታዎች ወይም ያልተጠናቀቀ ግብዓት (`unsettled_hosts` እና `unconfirmed`ን ጨምሮ ማንኛውም ዝርዝር ባዶ ካልሆነ ወይም `partial` true ከሆነ `changed` true ይሆናል)፣ `2` ፋይል ጠፍቷል፣ አይነበብም፣ የሚደገፍ ቅጽበታዊ ገጽ እይታ አይደለም ወይም ያለ `--allow-partial` ያልተጠናቀቀ ነው፣ `1` የ`-o` ፋይል ሊጻፍ አልቻለም።

## የKadupul export

[Kadupul](https://github.com/kadupulhq/kadupul) (የCacti 1.2.31 ቅርንጫፍ) በጅምላ የመሣሪያ ፋይል ማስገቢያ የለውም። ከስክሪፕት መሣሪያዎችን ለማከል የሚደግፈው መንገድ በአንድ ጥሪ አንድ መሣሪያ በ`--option=value` arguments የሚቀበለው `cli/add_device.php` ነው። `hostcensus export` የእነዚያን ጥሪዎች የPOSIX `sh` ስክሪፕት ይጽፋል፦

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

እያንዳንዱ ሕያው አስተናጋጅ `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` ይሆናል፦

- የፍተሻው SNMP መጠይቅ የተሳካባቸው አስተናጋጆች `--version=2 --community=...` ወይም `--version=3 --username=... --authproto=... --password=...` (እንዲሁም ለauthPriv `--privproto`/`--privpass`)፣ `--port` እና `--avail=snmp` ያገኛሉ። የSNMPv3 ወደ ውጭ መላክ `--snmp-user`ን ይፈልጋል፣ እና `add_device.php` የv3 ይለፍ ቃል ስለሚጠይቅ noAuthNoPriv ውድቅ ይደረጋል።
- ሌሎች አስተናጋጆች `--version=0 --avail=ping`፣ ከመጀመሪያው ክፍት የTCP ወደብ ጋር `--ping_method=tcp --ping_port=` ወይም ምንም ከሌለ ICMP ያገኛሉ።
- `--notes` ክፍት አገልግሎቶችን እና ስሪቶችን ይዘረዝራል። `--description` የተገላቢጦሽ-DNS ስሙ ተራ ከሆነ (ፊደላት፣ አሃዞች፣ `.`፣ `_`፣ `-`) እሱን ይጠቀማል፣ ካልሆነ IPውን ይወስዳል እና ልዩ እንዲሆን ይደረጋል፤ ምክንያቱም `add_device.php` ነባር መግለጫን ለዚያ መሣሪያ እንደ ማሻሻያ ይቆጥረዋል።

እያንዳንዱ እሴት ይረጋገጣል እና በ`shlex.quote` በshell ጥቅስ ይጠበቃል። በነባሪ ምንም የSNMP ምስጢር አይጻፍም፦ ስክሪፕቱ በአሂድ ጊዜ `HOSTCENSUS_SNMP_COMMUNITY`፣ `HOSTCENSUS_SNMP_AUTH_KEY` ወይም `HOSTCENSUS_SNMP_PRIV_KEY`ን ያስፋፋል እና አንዱ ካልተዋቀረ ይቆማል። `--include-credentials` በምትኩ ከእነዚያ አካባቢ ተለዋዋጮች የተወሰዱ እሴቶችን ወደ ስክሪፕቱ ይጽፋል፣ በmode 0600 ይፈጥረዋል እና ማስጠንቀቂያ ይመዘግባል። `add_device.php` ራሱ communityውን ያትማል እና ምስጢሮችን እንደ arguments ይቀበላል፣ እነዚህም እያንዳንዱ ጥሪ በሚካሄድበት ጊዜ በKadupul ሰርቨር የሂደት ዝርዝር ውስጥ ይታያሉ።

`add_device.php` ለድግግሞሾች እና ስህተቶች በ1 ይወጣል፤ ስክሪፕቱ ይቀጥላል፣ ውድቀቶችን ይቆጥራል እና ማንኛውም መሣሪያ ካልታከለ በ1 ይወጣል። የአብነት መለያዎች ከ`php cli/add_device.php --list-host-templates` ይገኛሉ። የ`export` መውጫ ኮዶች፦ `0` ተጽፏል፣ `2` የማይነበብ ግብዓት፣ ያለ `--allow-partial` ያልተጠናቀቀ ፍተሻ ወይም በደህና ወደ ውጭ ሊላክ የማይችል ውሂብ፣ `1` ስክሪፕቱ ሊጻፍ አልቻለም።

## ስሪት አሰጣጥ እና የልቀት ሂደት

hostcensus [Semantic Versioning](https://semver.org/spec/v2.0.0.html)ን ይከተላል፦ ተኳኋኝ ጥገናዎች የpatch ስሪቱን ይጨምራሉ፣ ተኳኋኝ ባህሪያት/ጊዜ ያለፈባቸው ማስጠንቀቂያዎች የminor ስሪቱን ይጨምራሉ፣ እና ተኳኋኝነትን የሚሰብሩ ለውጦች የmajor ስሪቱን ይጨምራሉ። ትዕዛዞች እና አማራጮች፣ የመውጫ ኮዶች እና የJSON schemas የሕዝብ ውል ናቸው፤ የደህንነት ጥገና ቀደም ብሎ መለወጥን ካልጠየቀ በስተቀር (ያኔ changelog ምክንያቱን ይገልጻል) ጊዜ ያለፈበት ባህሪ እስከ ቀጣዩ ዋና ልቀት ድረስ መሥራቱን ይቀጥላል።

release-please በ`main` ላይ ካሉ የConventional Commit ርዕሶች የልቀት PR ይከፍታል፣ `pyproject.toml`፣ `uv.lock` እና `CHANGES.md`ን ያሳድጋል። እሱን ማዋሃድ የ`vMAJOR.MINOR.PATCH` መለያ እና ረቂቅ የGitHub ልቀት ይፈጥራል፣ CI ደግሞ የተፈተነ wheel፣ የምንጭ ስርጭት እና checksums ያያይዝበታል፤ GitHub በattestations APIው በኩል ለእነዚያ ፋይሎች የግንባታ ማረጋገጫዎችን ያከማቻል። ፋይሎቹ ከተያያዙ በኋላ ተቆጣጣሪው ረቂቁን ገምግሞ ያትማል። ልቀቶች በፍጹም አይተኩም።

የPyPI የታመነ ህትመት በፈቃደኝነት የሚመረጥ ሲሆን የፕሮጀክት ባለቤትነትን፣ የታመነ አታሚን እና የ`pypi` አካባቢን ይጠይቃል። እንደገና ሳይገነባ ወይም የAPI ቶከን ሳያከማች እነዚያኑ የተረጋገጡ የልቀት ቅርሶች ያትማል። በዚህ የሕዝብ ማከማቻ ውስጥ መለያ የተሰጣቸው ልቀቶች የGitHub ቅርስ ማረጋገጫዎችን ያመነጫሉ፤ የግል ቅርንጫፎች የሚደገፍ ዕቅድ እና ግልጽ ፈቃድ ይፈልጋሉ። ለማዋቀር፣ ለትክክለኛ ትዕዛዞች እና ዳግም ሙከራዎች [ሙሉውን የልቀት መመሪያ](../../../docs/releasing.md) ይመልከቱ።

## ልማት

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

የልማት መሣሪያዎች በ`pyproject.toml` ውስጥ ባሉ የ[PEP 735](https://peps.python.org/pep-0735/) ጥገኛ ቡድኖች (`dev`፣ `fuzz`፣ `build`) ውስጥ ስለሚቀመጡ፣ በታተመው የጥቅል ሜታዳታ ውስጥ በፍጹም አይታዩም። `uv.lock` ብቸኛው lockfile ነው፤ CI በ`uv sync --locked` ይጫናል እና lockfileው ሲያረጅ ይወድቃል። አስተርጓሚውን በ`uv python`፣ በmise (`mise exec python@3.14 -- uv sync --locked`) ወይም በማንኛውም Python 3.12+ ይምረጡ።

CI የ90% የጥቅል ሽፋን ዝቅተኛ ገደብ ያስፈጽማል። የአሃድ ፈተናዎች ቁጥጥር የሚደረግባቸው loopback ሰርቨሮችን እና ከመስመር ውጭ የመገለጫ/ታሪክ/ልቀት-አረጋጋጭ ጉዳዮችን ያካትታሉ፤ የCompose ላብራቶሪ በተነጠለ bridge ላይ OpenSSH፣ MariaDB፣ nginx እና net-snmpን ያስኬዳል። በ`make test-integration` ያስኪዱት። [CONTRIBUTING.md](../../../CONTRIBUTING.md) እና [የልቀት መሣሪያዎች](../../../scripts/README.md)ን ይመልከቱ።

የአሂድ ጊዜ ኮንቴይነሩ ያለ መነሻ ማውጫ፣ ያለ shell መግቢያ እና ያለ pip እንደ UID/GID 10001 ይሰራል፣ እና ወደ `/app/output` መጻፍ ይችላል። ለዚያ ተጠቃሚ ወደ ማንኛውም የተሰቀለ የውጤት ማውጫ የመጻፍ መዳረሻ ይስጡት። ምንም capabilities አያስፈልገውም እና ለንባብ ብቻ በሆነ የroot ፋይል ሲስተም ይሰራል፣ ስለዚህ እንደሚከተለው ሊሄድ ይችላል፦

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap በዚህ ኮንቴይነር ውስጥ ልዩ መብት የማይጠይቅ የTCP ፍለጋ ባህሪውን ይጠቀማል። Trivy ሪፖርት በሚያደርገው ማንኛውም ሊስተካከል የሚችል HIGH ወይም CRITICAL ተጋላጭነት ላይ CI የምስል ግንባታውን ያቆማል።

## የአቅርቦት ሰንሰለት ፍተሻዎች

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) በmain ላይ እና በየሳምንቱ ይሰራል፣ ትክክለኛ ውጤቱን ያትማል፣ እና ግኝቶችን ወደ GitHub ኮድ ፍተሻ ይሰቅላል። Actions እና የኮንቴይነር መሠረቶች በማይለወጡ hashes ተሰክተዋል፤ የPython ጥገኞች በ`uv.lock` ውስጥ ይፈታሉ። የBandit ውድቀቶች CIን ያቆማሉ፣ እና የተገደበ የAtheris fuzzing ያለ አውታረ መረብ መዳረሻ የSSH፣ MySQL፣ HTTP፣ ሰርተፊኬት እና SNMPv3 BER ተንታኞችን ይፈትሻል።

Scorecard ታሪካዊ የግምገማ እንቅስቃሴን፣ የአስተዋጽዖ አበርካቾችን ብዝሃነት እና የልቀት ምንጭነትንም ይለካል። እነዚያ ነጥቦች ተጨባጭ ማስረጃን ያንጸባርቃሉ፤ እያንዳንዱ የአስተዳደር ወይም ታሪካዊ-ልቀት ፍተሻ መሟላቱን የሚገልጹ አይደሉም። [SECURITY.md](../../../SECURITY.md) እና [የልቀት ምንጭነት](../../../docs/releasing.md)ን ይመልከቱ።

## አካባቢያዊ ማድረግ

የCLI መልዕክቶች እና የተርሚናል ማጠቃለያ/diff ሰንጠረዦች ያለ ምንም ተጨማሪ የአሂድ ጊዜ ጥገኛ 45 አካባቢያዊ ቋንቋዎችን (`en`፣ `de`፣ `es`፣ `fr`፣ `it`፣ `pt-BR`፣ `nl`፣ `ru`፣ `uk`፣ `ja`፣ `ko`፣ `zh-CN`፣ `zh-TW`፣ `ar`፣ `hi`፣ `pl`፣ `tr`፣ `sv`፣ `vi`፣ `id`፣ `af-ZA`፣ `am-ET`፣ `ar-EG`፣ `ar-MA`፣ `fr-MA`፣ `fr-SN`፣ `ha-NG`፣ `ig-NG`፣ `mg-MG`፣ `rw-RW`፣ `so-SO`፣ `sw-KE`፣ `xh-ZA`፣ `yo-NG`፣ `zu-ZA`፣ `bn`፣ `fa`፣ `he`፣ `mr`፣ `ta`፣ `te`፣ `th`፣ `ur`፣ `ms`፣ `fil`) ይደግፋሉ። ምርጫው `--lang`ን፣ ከዚያ `LC_ALL`፣ `LC_MESSAGES` እና `LANG`ን ያከብራል፣ ካልተገኘ ወደ `en` ይመለሳል። የJSON schemas፣ የCSV አምዶች እና የወደ ውጭ መላክ ስክሪፕቶች በሁሉም አካባቢያዊ ቋንቋዎች አይለወጡም።

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## አስተዋጽዖ ማበርከት

አስተዋጽዖዎች ሊደገም የሚችል ምሳሌ ማካተት፣ የተዘገቡትን የCLI እና የውሂብ-ቅርጸት ውሎች መጠበቅ፣ እንዲሁም ከላይ ያሉትን የጥራት ፍተሻዎች ማለፍ አለባቸው። ለልማት የሥራ ፍሰት [CONTRIBUTING.md](../../../CONTRIBUTING.md)ን እና ለተኳኋኝነት እና ስሪት ውሳኔዎች [የልቀት መመሪያውን](../../../docs/releasing.md) ይመልከቱ።

## የደህንነት እና የፈቃድ ሁኔታ

ለግል ሪፖርት አቀራረብ እና ለሚደገፉ ስሪቶች [SECURITY.md](../../../SECURITY.md)ን ይመልከቱ።
hostcensus በ[MIT ፈቃድ](../../../LICENSE) ስር ፈቃድ ተሰጥቶታል።

የምንጭ ራስጌዎች የSPDX መለያዎችን ይጠቀማሉ እና ከGit ታሪክ የአስተዋጽዖ አበርካቾችን ምስጋና ይጠብቃሉ። ለባለቤትነት መግለጫ [AUTHORS.md](../../../AUTHORS.md)ን ይመልከቱ። የሁለትዮሽ ፈተና ቅጂዎች እና የመነጨው lockfile አጎራባች `.license` ፋይሎችን ይጠቀማሉ፤ የMIT ጽሑፍ በ`LICENSES/MIT.txt` ውስጥ ይገኛል።
