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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · **اردو** · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus ایک Python CLI ہے جو آپ کے زیر انتظام نیٹ ورکس پر قابلِ تکرار سروس انوینٹری کے لیے بنایا گیا ہے۔ یہ ریکارڈ کرتا ہے کہ آلات کیا کچھ ظاہر کرتے ہیں، وقت کے ساتھ مشاہدات کا موازنہ کرتا ہے، اور Kadupul امپورٹ اسکرپٹس تیار کرتا ہے۔ ڈیفالٹ بیک اینڈ بغیر root کے asyncio ساکٹس استعمال کرتا ہے؛ اختیاری Nmap ڈسکوری ترتیب دیے گئے سروس پورٹس سے آگے کے ہوسٹس کی شناخت کر سکتی ہے۔

## hostcensus کیوں

ایک وقتی پورٹ رپورٹ یہ واضح نہیں کرتی کہ اگلا مشاہدہ تبدیل ہوا یا محض ناکام ہو گیا۔ hostcensus واضح سروس اسٹیٹس، محدود پروبز، قابلِ دوبارہ استعمال اسکین پروفائلز، اور مقامی ہسٹری کو یکجا کرتا ہے۔ آپریٹرز اسی دائرہ کار کو دہرا سکتے ہیں، خرابیوں کا معائنہ کر سکتے ہیں، اور غیر یقینی مشاہدات کو مصدقہ تبدیلیوں سے الگ کر سکتے ہیں۔

- **سروس کے شواہد:** SSH شناخت، MySQL گریٹنگز، HTTP ہیڈرز، TLS سرٹیفکیٹ مشاہدات، اور SNMP ڈسکوری یا اسناد کے ساتھ system-MIB استفسارات۔
- **قابلِ تکرار دائرہ کار:** نامزد TOML پروفائلز، اضافی اخراجات، قابلِ ترتیب سروسز، ہوسٹ/پروب کی حدود، اور محدود ورکرز۔
- **ٹریفک سے پہلے جانچ:** مقامی preflight اہداف، ٹولز، منزل تک رسائی، ہسٹری اسکیما، اور ترتیب دیے گئے TLS CA بنڈلز کی توثیق کرتا ہے۔
- **انوینٹری ہسٹری:** ٹرانزیکشنل SQLite اسنیپ شاٹس تمام مشاہدات کو محفوظ رکھتے ہیں؛ موازنے اسکینر کی ناکامیوں اور نامعلوم اسٹیٹس کو نمایاں رکھتے ہیں۔
- **باہم قابلِ عمل آؤٹ پٹ:** ٹرمینل، JSON اور CSV رپورٹس، ورژن شدہ فائل اسنیپ شاٹس، اور Kadupul امپورٹ اسکرپٹس۔

CI میں Linux اور macOS پر Python 3.12، 3.13 اور 3.14 کے ساتھ ایک کنٹرولڈ Compose انٹیگریشن لیب شامل ہے۔ کوڈ ان رن ٹائم ورژنز کو برقرار رکھتے ہوئے جدید type aliases، typed preflight نتائج، keyword-only slotted پروفائلز اور منظم async کلین اپ استعمال کرتا ہے۔ SemVer مطابقت کے معاہدے اور GitHub ریلیز کے عمل کے لیے [ورژننگ اور ریلیزز](../../../docs/releasing.md) دیکھیں۔ ریلیز بیج شائع شدہ آرٹیفیکٹس کو ظاہر کرتا ہے، اس چیک آؤٹ کو نہیں: فی الحال تازہ ترین شائع شدہ ٹیگ `v0.3.0` ہے، جبکہ یہ چیک آؤٹ پیکج ورژن `3.0.0` استعمال کرتا ہے۔ یہاں دستاویز کردہ انوینٹری فیچرز استعمال کرنے کے لیے چیک آؤٹ سے انسٹال کریں۔

[انسٹالیشن](#install) سے آغاز کریں، پھر [پروفائلز اور ہسٹری](#inventory-profiles-preflight-and-local-history) دیکھیں۔ انٹیگریشن کی تفصیلات کے لیے [سروس فنگر پرنٹس](#fingerprints)، [فائل موازنے](#inventory-diff)، اور [Kadupul ایکسپورٹ](#kadupul-export) دیکھیں۔

## انسٹالیشن

Python 3.12 یا اس سے جدید ورژن درکار ہے؛ Python 3.12 سے 3.14 ٹیسٹ شدہ میٹرکس ہے۔ اس چیک آؤٹ سے، لاک شدہ رن ٹائم انحصار انسٹال کریں:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

اختیاری Nmap ہوسٹ ڈسکوری کے لیے، اپنے پلیٹ فارم کے پیکج مینیجر کے ذریعے Nmap ایگزیکیوٹیبل انسٹال کریں؛ کسی اضافی Python پیکج کی ضرورت نہیں ہے۔ Nmap کے XML آؤٹ پٹ کو defusedxml (جو ایک بنیادی انحصار ہے) سے پارس کیا جاتا ہے، اس لیے entity expansion کو مسترد کر دیا جاتا ہے۔ hostcensus `PATH` پر موجود `nmap` کو براہ راست ایک مقررہ آرگیومنٹ لسٹ، پریفکس سائز کے ساتھ بڑھنے والی ڈیڈ لائن، اور 64 MiB آؤٹ پٹ کی حد کے ساتھ چلاتا ہے۔ ڈیفالٹ بیک اینڈ کے لیے Nmap کی ضرورت نہیں ہے۔

## netprobe سے منتقلی

hostcensus دراصل netprobe کا نیا نام ہے، جو 3.0.0 میں ریلیز ہوا۔ یہ پروجیکٹ کسی بھی نام سے PyPI پر کبھی شائع نہیں ہوا، لہٰذا انسٹالیشن چیک آؤٹ یا GitHub ریلیز سے کی جاتی رہی ہے۔ GitHub ریپوزٹری اپنا نام برقرار رکھتی ہے۔

| پہلے | اب | مطابقت |
| --- | --- | --- |
| ڈسٹری بیوشن `netprobe` | `hostcensus` | چیک آؤٹ سے دوبارہ انسٹال کریں؛ پرانے نام کا کوئی پیکج موجود نہیں ہے۔ |
| `netprobe` کمانڈ | `hostcensus` | `netprobe` اب بھی چلتا ہے اور stderr پر ایک deprecation لائن پرنٹ کرتا ہے۔ Exit codes اور stdout غیر تبدیل شدہ ہیں۔ اگلی بڑی ریلیز میں ہٹا دیا جائے گا۔ |
| `NETPROBE_*` ماحولیاتی متغیرات | `HOSTCENSUS_*` | جب اس کا ہم منصب `HOSTCENSUS_*` سیٹ نہ ہو تو `NETPROBE_*` متغیر استعمال ہوتا ہے، ساتھ ہی stderr پر ایک وارننگ آتی ہے جو متغیرات کے نام بتاتی ہے لیکن ان کی قدریں کبھی نہیں۔ دونوں سیٹ ہونے پر `HOSTCENSUS_*` کو ترجیح ملتی ہے۔ اگلی بڑی ریلیز میں ہٹا دیا جائے گا۔ |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **بریکنگ تبدیلی۔** کوئی import shim انسٹال نہیں ہے؛ امپورٹس کو اپ ڈیٹ کریں۔ |
| Docker امیج ٹیگ `network-discovery:test` (صرف CI) اور کنٹینر صارف `netprobe` | `hostcensus:test`، صارف `hostcensus` | کوئی رجسٹری امیج کبھی شائع نہیں ہوئی۔ امیج دوبارہ بلڈ کریں اور `hostcensus` انٹری پوائنٹ استعمال کریں۔ |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | جب نیا نام موجود نہ ہو تو پرانے ڈیفالٹ نام والی موجودہ فائل ایک وارننگ کے ساتھ اب بھی استعمال ہوتی ہے۔ واضح `--config` اور `--history` پاتھ متاثر نہیں ہوتے۔ |
| `"format": "netprobe-report"` یا `"netprobe-snapshot"` والی رپورٹس اور اسنیپ شاٹس، اور `netprobe_version` فیلڈ | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` اور `export` پرانے نام کے تحت لکھی گئی فائلوں کو اب بھی لوڈ کرتے ہیں، اور شائع شدہ JSON Schemas دونوں املا قبول کرتے ہیں۔ نئی فائلیں نئے نام استعمال کرتی ہیں۔ SQLite ہسٹری ڈیٹا بیسز غیر تبدیل شدہ ہیں اور پہلے کی طرح لوڈ ہوتے ہیں۔ |
| `netprobe export` سے بنی Kadupul اسکرپٹس | `hostcensus export` سے بنی اسکرپٹس | پرانی اسکرپٹس کام کرتی رہتی ہیں اور چلتے وقت اب بھی `NETPROBE_SNMP_*` پڑھتی ہیں۔ نئی اسکرپٹس `HOSTCENSUS_SNMP_*` پڑھتی ہیں۔ |

## مختصر مثال

ترقی کے تحت بیان کردہ انٹیگریشن لیب کے ٹیسٹر کنٹینر سے چلائیں؛ آؤٹ پٹ مختصر کیا گیا ہے:

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

## ایگزٹ کوڈز

| کمانڈ | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | مشاہدات/رپورٹ ریکارڈ ہو گئی | preflight/backend، ہسٹری، یا رپورٹ/اسنیپ شاٹ لکھنے میں ناکامی | غلط ہدف، اختیارات، کنفیگریشن، یا حدود | - | `--deadline` تک پہنچ گیا؛ جزوی رپورٹ لکھی گئی، ہسٹری اور اسنیپ شاٹ چھوڑ دیے گئے |
| `preflight` | چیکس کامیاب رہے | مقامی چیک ناکام رہا | غلط ہدف/کنفیگریشن یا متصادم منزلیں | - | - |
| `profiles` | توثیق شدہ پروفائلز درج ہو گئیں | - | ناقابلِ مطالعہ/غلط کنفیگریشن یا انتخاب | - | - |
| `history` | خلاصے درج ہو گئے | گمشدہ، غلط، یا غیر معاون ہسٹری | غلط CLI اختیارات | - | - |
| `compare` | موازنہ تیار ہو گیا، بشمول جب تبدیلیاں موجود ہوں | ناقابلِ مطالعہ ہسٹری، غیر مطابقت پذیر دائرہ کار/ترتیب، یا لکھنے میں ناکامی | غلط CLI اختیارات | - | - |
| `diff` | کوئی تبدیلی نہیں | `-o` فائل لکھی نہیں جا سکی | گمشدہ، ناقابلِ مطالعہ یا غیر معاون ان پٹ، یا `--allow-partial` کے بغیر نامکمل اسکین | تبدیلیاں ملیں، غیر مصدقہ مشاہدات، یا نامکمل اسکین | - |
| `export` | اسکرپٹ لکھی گئی | اسکرپٹ لکھی نہیں جا سکی | ناقابلِ مطالعہ ان پٹ، `--allow-partial` کے بغیر نامکمل اسکین، یا ایسا ڈیٹا جسے محفوظ طریقے سے ایکسپورٹ نہیں کیا جا سکتا | - | - |

## ساخت

| ماڈیول | ذمہ داری |
| --- | --- |
| `cli.py` | کمانڈ اختیارات، پروفائل کا حل، preflight، اسکیننگ اور رپورٹنگ |
| `scanner.py`, `probes.py` | ہدف کی توسیع، محدود ورکرز، ہوسٹ ڈسکوری اور سروس مشاہدات |
| `config.py`, `profiles.py` | سروس کی تعریفیں اور توثیق شدہ انوینٹری پروفائلز |
| `models.py`, `output.py` | نتائج کی اقسام اور ٹرمینل/JSON/CSV رینڈرنگ |
| `history.py`, `diff.py` | SQLite ہسٹری اور ورژن شدہ فائل اسنیپ شاٹ موازنے |
| `preflight.py` | مقامی چیکس اور محدود Nmap ورژن تلاش |
| `export.py` | توثیق شدہ اور کوٹ شدہ Kadupul امپورٹ اسکرپٹس |

ہر سروس مشاہدہ اپنی حالت کو اپنی مشتہر کردہ شناخت سے الگ ریکارڈ کرتا ہے۔ ریڈز اور ڈیڈ لائنز محدود ہیں؛ پروب کی مستثنیات ہوسٹ کی خرابیوں میں رہتی ہیں۔ SQLite ہسٹری ٹرانزیکشنز، واضح کنکشن کلین اپ، اور صرف پڑھنے کے قابل لسٹنگ اور موازنے کے راستے استعمال کرتی ہے۔ SNMP راز صرف ماحولیاتی متغیرات یا سیکرٹ فائلوں کے ذریعے داخل ہوتے ہیں؛ انوینٹری ہسٹری مؤثر غیر خفیہ ترتیبات کو محفوظ کرتی ہے۔ اسکین پائپ لائن، اس کی حدود اور ٹرسٹ باؤنڈریز کے لیے [آرکیٹیکچر](../../../docs/architecture.md)، اور مجاز استعمال کے لیے [SECURITY.md](../../../SECURITY.md#authorized-use) دیکھیں۔


## استعمال

صرف وہی نیٹ ورکس اسکین کریں جن کا انتظام آپ کے پاس ہے۔

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| اختیار | مطلب |
| --- | --- |
| `NETWORK` | CIDR، IP، یا ہوسٹ نیم؛ `--profile` کے ساتھ اختیاری۔ IPv6 اسکوپ آئیڈینٹیفائرز مسترد کر دیے جاتے ہیں۔ |
| `-o, --output PATH` | رپورٹ لکھیں۔ فارمیٹ ایکسٹینشن (`.json`, `.csv`) کی پیروی کرتا ہے؛ دیگر ایکسٹینشنز JSON پر واپس آ جاتی ہیں۔ |
| `-f, --format json\|csv\|kadupul\|auto` | رپورٹ فارمیٹ کو لازمی قرار دیں۔ `--output` کے بغیر کوئی اثر نہیں ہوتا۔ `.sh` سے `kadupul` منتخب ہوتا ہے۔ |
| `-v, --verbose` | ڈیبگ لاگنگ۔ |
| `-q, --quiet` | نتائج، پیش رفت اور معلوماتی لاگز کو روکیں؛ انتباہات اور خرابیاں پھر بھی stderr پر ظاہر ہوتی ہیں۔ |
| `--backend asyncio\|nmap` | ہوسٹ ڈسکوری۔ `asyncio` (ڈیفالٹ) براہ راست سروس پورٹس کو پروب کرتا ہے؛ `nmap` پہلے ایک nmap پنگ سویپ چلاتا ہے اور اسے `PATH` پر `nmap` ایگزیکیوٹیبل کی ضرورت ہوتی ہے۔ |
| `--timeout SECONDS` | ان پروبز کے لیے انتظار کریں جو اپنا بجٹ خود مقرر نہیں کرتے (ڈیفالٹ 1.0)۔ بلٹ ان کنیکٹ پروبز 0.3s استعمال کرتے ہیں جب تک کہ سروس ٹیبل `timeout` مقرر نہ کرے۔ |
| `--concurrency N` | ایک وقت میں چلنے والے پروبز (ڈیفالٹ 256)۔ |
| `--deadline SECONDS` | اتنے وقت کے بعد پورا اسکین، بشمول nmap سویپ، روک دیں (ڈیفالٹ 3600، زیادہ سے زیادہ 604800؛ ماحولیاتی متغیر `HOSTCENSUS_DEADLINE`)۔ جو ہوسٹس مکمل ہو چکے ہیں وہ `"complete": false` کے ساتھ رپورٹ میں لکھے جاتے ہیں، کوئی ہسٹری یا اسنیپ شاٹ نہیں لکھا جاتا، اور `scan` کوڈ 4 کے ساتھ باہر نکلتا ہے۔ |
| `--config PATH` | TOML سروس کی تعریفیں اور اختیاری نامزد `[profiles]` ترتیبات۔ |
| `--profile NAME` | ایک نامزد پروفائل استعمال کریں؛ `--config` نہ دینے پر ڈیفالٹ `hostcensus.toml` ہوتا ہے۔ |
| `--exclude IP/CIDR` | ایک اخراج شامل کریں؛ ضرورت کے مطابق دہرائیں۔ خارج کردہ IPv4 ہوسٹ ان IPv6 پتوں کو بھی خارج کر دیتا ہے جو اس تک پہنچتے ہیں: IPv4-mapped (`::ffff:a.b.c.d`)، NAT64 (`64:ff9b::/96`) اور 6to4۔ IPv4-mapped اہداف اور اخراجات کو انہی IPv4 پتوں کے طور پر سمجھا جاتا ہے جن کی وہ نمائندگی کرتے ہیں۔ |
| `--max-hosts N` | اخراجات سے پہلے چیک کی جانے والی پتوں کی حد (ڈیفالٹ/زیادہ سے زیادہ حد 65,536)۔ |
| `--history PATH` | مکمل شدہ اسکین کو ایک opt-in SQLite ہسٹری ڈیٹا بیس میں ریکارڈ کریں۔ |
| `--services NAMES` | چیک کرنے کے لیے سروس ناموں کی کوما سے الگ فہرست، اسی ترتیب میں (ڈیفالٹ: تمام)۔ |
| `--ports SPEC` | `NAME=PORT` (کسی سروس کو منتقل کریں) یا `PORT` (`tcp-PORT` نامی ایک سادہ TCP چیک شامل کریں) کی کوما سے الگ فہرست۔ |
| `--snmp-community-file PATH` | سسٹم MIB استفسار کے لیے SNMPv2c کمیونٹی رکھنے والی فائل۔ ماحولیاتی متغیر: `HOSTCENSUS_SNMP_COMMUNITY` (قدر) یا `HOSTCENSUS_SNMP_COMMUNITY_FILE` (پاتھ)۔ |
| `--snmp-user` | SNMPv3 صارف۔ ماحولیاتی متغیر: `HOSTCENSUS_SNMP_USER`۔ |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (ڈیفالٹ), `SHA224`, `SHA256`, `SHA384`, `SHA512` اور پاس فریز رکھنے والی فائل۔ ماحولیاتی متغیر: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` یا `HOSTCENSUS_SNMP_AUTH_KEY_FILE`۔ |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (ڈیفالٹ), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` اور پاس فریز رکھنے والی فائل۔ ماحولیاتی متغیر: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` یا `HOSTCENSUS_SNMP_PRIV_KEY_FILE`۔ |
| `--save-snapshot PATH` | `hostcensus diff` کے لیے ایک ورژن شدہ اسنیپ شاٹ بھی لکھیں۔ |
| `--tls-ca-file PATH` | سسٹم اسٹور کے بجائے اس PEM بنڈل کے خلاف HTTPS سرٹیفکیٹس کی تصدیق کریں۔ ماحولیاتی متغیر: `HOSTCENSUS_TLS_CA_FILE`۔ |

ڈیفالٹ طور پر ہر ہوسٹ کو SSH (TCP 22)، SNMP (UDP 161)، MySQL (TCP 3306)، HTTP (TCP 80) اور HTTPS (TCP 443) کے لیے چیک کیا جاتا ہے۔ TCP پورٹس کو مکمل کنیکٹ کے ساتھ ٹیسٹ کیا جاتا ہے۔ SNMP کو SNMPv3 انجن ڈسکوری درخواست کے ساتھ ٹیسٹ کیا جاتا ہے، جس کا جواب کسی بھی SNMPv3 ایجنٹ کو بغیر اسناد کے دینا لازمی ہے؛ جو ایجنٹس صرف v1/v2c بولتے ہیں وہ اس پروب سے دریافت نہیں ہوں گے۔ asyncio بیک اینڈ کے ساتھ کوئی ہوسٹ تب زندہ شمار ہوتا ہے جب کسی بھی پروب کو جواب ملے، بشمول مسترد کردہ کنکشن کے، اس لیے جو ہوسٹ ہر پروب کو ڈراپ کر دیتا ہے اس کا `alive=false` اور خرابی "Host is down" ہوتی ہے؛ یہ اس بات کا ثبوت نہیں ہے کہ وہ جسمانی طور پر بند ہے۔ `--backend nmap` کے ساتھ، nmap فیصلہ کرتا ہے کہ کون سے ہوسٹس زندہ ہیں (root کے طور پر ICMP، ورنہ TCP 80/443)۔

### فنگر پرنٹس

ہر کھلی سروس کا فنگر پرنٹ اس بنیاد پر لیا جاتا ہے جو وہ کسی بھی لاگ ان سے پہلے بھیجتی ہے۔ SNMP استفسار کے سوا کوئی چیز تصدیق نہیں کرتی، اور وہ بھی صرف تب جب آپ اسناد فراہم کریں۔

| پروب | پڑھتا ہے | `version` | `details` کیز |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 شناختی لائن | سافٹ ویئر، مثلاً `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | MySQL/MariaDB ابتدائی ہینڈ شیک | سرور ورژن | `server_version`, `flavor`, `auth_plugin`، یا `error_code`/`error` |
| `http` | `HEAD /` جواب | `Server` ہیڈر | `status`, `server` |
| `https` | TLS ہینڈ شیک، سرٹیفکیٹ، `HEAD /` | `Server` ہیڈر | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 ڈسکوری؛ اسناد کے ساتھ، sysDescr, sysObjectID, sysName کا GET | sysDescr | `engine_id`؛ اسناد کے ساتھ `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`، یا `snmp_error` |

ہوسٹ نیم ہدف کو فی ہوسٹ ایک بار حل کیا جاتا ہے اور ہر پروب اسی پتے سے جڑتا ہے، جو نتائج میں `address` کے طور پر ریکارڈ ہوتا ہے؛ نام صرف TLS SNI، سرٹیفکیٹ کی تصدیق اور HTTP `Host` ہیڈر کے لیے استعمال ہوتا ہے۔ جو نام حل نہیں ہوتا وہ `unknown` اسٹیٹس اور `Cannot resolve` خرابی دیتا ہے۔ ریورس DNS نام صرف تب رکھے جاتے ہیں جب ان میں ہوسٹ نیم کے حروف ہوں، اور ایک وقت میں زیادہ سے زیادہ 16 تلاشیاں چلتی ہیں۔ HTTPS سسٹم اسٹور یا `--tls-ca-file` کے خلاف سرٹیفکیٹ اور ہوسٹ نیم کی تصدیق استعمال کرتا ہے۔ ٹرسٹ اسٹور کو اسکین کے لیے ایک بار لوڈ کیا جاتا ہے اور ہر HTTPS پروب کے لیے دوبارہ استعمال کیا جاتا ہے۔ TCP کنیکٹ اور TLS ہینڈ شیک کا وقت الگ الگ ناپا جاتا ہے، اس لیے جو پورٹ کنکشن قبول کر لے لیکن ہینڈ شیک کو روک دے وہ `filtered` نہیں بلکہ `tls_error` کے ساتھ `open` ہوتا ہے۔ اگر تصدیق ناکام ہو جائے، تو نتیجہ `cert_verified: false` اور `cert_verify_error` ریکارڈ کرتا ہے؛ یہ کمزور ترتیبات کے ساتھ دوبارہ کوشش نہیں کرتا اور نہ ہی HTTP درخواست بھیجتا ہے۔ سرٹیفکیٹ کی تفصیلات اور HTTP ہیڈرز صرف تصدیق کامیاب ہونے کے بعد جمع کیے جاتے ہیں۔ پرائیویٹ CA سروسز کے لیے درست CA بنڈل فراہم کریں۔ پرانی رپورٹس میں `cert_read_unverified` ہو سکتا ہے، جو موجودہ پروبز اب تیار نہیں کرتے۔

SNMP راز صرف ماحولیاتی متغیرات یا فائلوں (`--snmp-*-file`، یا مماثل `HOSTCENSUS_SNMP_*_FILE` متغیر) سے پڑھے جاتے ہیں، کبھی کمانڈ لائن قدروں سے نہیں، جنہیں دیگر مقامی صارفین پروسیس لسٹ میں دیکھ سکتے ہیں۔ قدر کے ساتھ `--snmp-community`, `--snmp-auth-key` اور `--snmp-priv-key` کوڈ 2 کے ساتھ باہر نکل جاتے ہیں اور متبادل کا نام بتاتے ہیں۔ سیکرٹ فائل غیر خالی UTF-8 اور زیادہ سے زیادہ 4096 بائٹس کی ہونی چاہیے؛ ایک اختتامی نئی لائن کو نظر انداز کر دیا جاتا ہے، اور ایک ہی راز کے لیے متغیر اور فائل دونوں سیٹ کرنا ایک خرابی ہے۔ خرابیاں فائل کا نام بتاتی ہیں لیکن اس کے مواد کو کبھی پرنٹ نہیں کرتیں۔ اسکین رپورٹس اور ہسٹری میں جان بوجھ کر اسناد کی قدریں شامل نہیں کی جاتیں۔ ایکسپورٹر کے پاس ایک الگ، واضح `--include-credentials` اختیار ہے جس کی تفصیل نیچے دی گئی ہے۔ کمیونٹی SNMPv2c کو منتخب کرتی ہے؛ صارف SNMPv3 کو منتخب کرتا ہے، جب auth کی دی جائے تو تصدیق کے ساتھ اور جب دونوں کیز دی جائیں تو رازداری کے ساتھ (`snmp_security_level` ریکارڈ کرتا ہے کہ کون سا استعمال ہوا)۔ hostcensus ایگزٹ کوڈ 2 کے ساتھ کمیونٹی کو v3 صارف کے ساتھ ملانے، auth کی کے بغیر پرائیویسی کی استعمال کرنے، یا صارف کے بغیر کیز استعمال کرنے سے انکار کرتا ہے، اور یہ ناکام ہونے والے v3 استفسار کو کبھی v2c یا کم سیکیورٹی لیول کے ساتھ دوبارہ نہیں چلاتا۔ جو ایجنٹس صرف v1/v2c بولتے ہیں وہ اسناد کے بغیر v3 ڈسکوری کو نظر انداز کر دیتے ہیں، اس لیے وہ صرف تب open نظر آتے ہیں جب کمیونٹی فراہم کی جائے۔

بینر کے متن کو محفوظ کرنے یا دکھانے سے پہلے قابلِ طباعت حروف تک محدود کیا جاتا ہے اور 256 حروف پر روک دیا جاتا ہے۔ ریڈز بھی محدود ہیں: فی لائن 4 KiB، MySQL گریٹنگ کے لیے 4 KiB، HTTP ہیڈرز کے لیے 16 KiB۔ 32 اوکٹیٹس سے لمبے SNMP انجن ID کو محفوظ کرنے سے پہلے کاٹ دیا جاتا ہے۔ HTTP اور HTTPS ایک Host ہیڈر بھیجتے ہیں جس میں IPv6 پتہ بریکٹ میں ہوتا ہے اور جب پورٹ 80 یا 443 نہ ہو تو پورٹ بھی شامل ہوتا ہے۔ ایسے CSV سیلز جو اسپریڈشیٹ فارمولا ٹرگر سے شروع ہوتے ہیں ان کے آگے سابقہ لگا دیا جاتا ہے تاکہ سیل متن ہی رہے۔

### حدود

ایک رن زیادہ سے زیادہ 65,536 پتے، 64 سروسز، اور 524,288 پروبز (ہوسٹس ضرب سروسز) قبول کرتا ہے؛ اس سے بڑی درخواستیں کچھ بھی بھیجنے سے پہلے کوڈ 2 کے ساتھ باہر نکل جاتی ہیں۔ `--concurrency` کی حد 4096 ساکٹس ہے۔ ہر پروب کی سخت ڈیڈ لائن اس کے اپنے بجٹ سے چار گنا ہوتی ہے۔ کنیکٹ پروبز (`tcp`, `ssh`, `mysql`, `http`) 0.3 سیکنڈ استعمال کرتے ہیں جب تک کہ وہ سروس `timeout` مقرر نہ کرے۔ SNMP اور HTTPS جب اپنا ٹائم آؤٹ مقرر نہ کریں تو `--timeout` (ڈیفالٹ 1.0) استعمال کرتے ہیں۔ جو پروب ڈیڈ لائن تک پہنچ جائے اسے `errors` میں "probe timed out" کے ساتھ `unknown` رپورٹ کیا جاتا ہے۔ مقامی ساکٹ ناکامیاں (مثلاً فائل ڈسکرپٹرز ختم ہو جانا) بھی ریکارڈ شدہ خرابی کے ساتھ `unknown` ہوتی ہیں؛ وہ کبھی فلٹرڈ پورٹ یا ڈاؤن ہوسٹ شمار نہیں ہوتیں۔ پروبنگ سے پہلے، hostcensus اوپن فائل سافٹ لمٹ کو ہارڈ لمٹ کی طرف بڑھاتا ہے تاکہ `--concurrency` جمع 64 ڈسکرپٹرز سما سکیں؛ جب وہ ایسا نہ کر سکے، تو `open files` preflight چیک ناکام ہو جاتا ہے اور `scan` ٹریفک بھیجنے سے پہلے 1 کے ساتھ باہر نکل جاتا ہے۔ Nmap ڈسکوری 30 سیکنڈ کا ہوسٹ ٹائم آؤٹ استعمال کرتی ہے۔ nmap کو پریفکس CIDR شکل میں دیا جاتا ہے، اور جب nmap دیے گئے پتوں سے کم پتے رپورٹ کرے (مثلاً کوئی ایسا نام جسے وہ حل نہ کر سکے) تو سویپ ہوسٹس کو ڈاؤن قرار دینے کے بجائے ایگزٹ 1 کے ساتھ ناکام ہو جاتا ہے۔ ہوسٹ نیم ہدف کو ایک بار حل کیا جاتا ہے اور nmap کو وہی پتہ دیا جاتا ہے، تاکہ ڈسکوری اور پروبز ایک ہی مشین تک پہنچیں۔ ایک مکمل پریفکس ایک nmap پروسیس ہے جس کی سب پروسیس ڈیڈ لائن ہر 256 پتوں کے لیے 35 سیکنڈ ہے، جسے اوپر کی طرف راؤنڈ کیا جاتا ہے۔ اخراجات والے سویپس 256 ہوسٹس کے بیچز اور ہر بیچ کے لیے 35 سیکنڈ کی ڈیڈ لائن استعمال کرتے ہیں۔ ورکر کی تخلیق رینج کے سائز سے آزادانہ طور پر محدود ہے۔ ریورس DNS اور ہوسٹ نیم ریزولوشن کی دو سیکنڈ کی الگ ڈیڈ لائن ہے؛ ایک ریزولور کال جو کبھی واپس نہ آئے اسے اپنے تھریڈ پر چھوڑ دیا جاتا ہے، تاکہ وہ hostcensus کو ان حدود سے آگے چلتا نہ رکھ سکے۔ ایک وقت میں زیادہ سے زیادہ 16 تلاشیاں چلتی ہیں، اور ایک ترک کی گئی کال واپس آنے تک اپنا سلاٹ برقرار رکھتی ہے، اس لیے پھنسے ہوئے تھریڈز کی تعداد محدود رہتی ہے؛ اگر تمام 16 لٹک جائیں، تو بعد کی تلاشیاں دو سیکنڈ کی ڈیڈ لائن سے باہر ایک سلاٹ کے لیے قطار میں لگ جاتی ہیں (جو سلاٹ خالی ہونے پر شروع ہوتی ہے) جب تک کہ `--deadline` اسکین کو روک نہ دے۔ `NetworkScanner` کو `deadline` کے بغیر لائبریری کے طور پر استعمال کرنے پر ایسے سلاٹ کے لیے غیر معینہ مدت تک انتظار کرنا پڑ سکتا ہے۔ `--deadline` (ڈیفالٹ ایک گھنٹہ) ان سب کے اوپر پورے رن کو محدود کرتا ہے۔

### سروسز کی کنفیگریشن

سروسز کو ایک TOML فائل کے ذریعے تبدیل کیا جا سکتا ہے:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` دراصل `tcp`, `ssh`, `mysql`, `http`, `https` یا `snmp` میں سے ایک ہے اور جب سروس کا نام خود ایک پروب ہو تو ڈیفالٹ وہی ہوتا ہے، ورنہ `tcp` ہوتا ہے۔ صرف `snmp` UDP استعمال کرتا ہے۔ سروس کے نام چھوٹے حروف، ہندسے، `-` اور `_` پر مشتمل ہوتے ہیں۔ دو سروسز ایک ہی پورٹ اور پروٹوکول شیئر نہیں کر سکتیں؛ ہسٹری اس جوڑے کے لیے ایک اسٹیٹ ریکارڈ کرتی ہے۔ `timeout` اختیاری ہے، سیکنڈز میں، اور کم از کم 0.05 ہوتا ہے۔ کنیکٹ طرز کے پروبز (`tcp`, `ssh`, `mysql`, `http`) کا ڈیفالٹ 0.3 سیکنڈ ہے۔ `snmp` اور `https` جب سروس `timeout` مقرر نہ کرے تو اسکین کا `--timeout` استعمال کرتے ہیں۔ `--timeout` اس بجٹ کو تبدیل نہیں کرتا جو سروس کے پاس پہلے سے موجود ہو۔

JSON رپورٹس ورژن شدہ دستاویزات ہیں (`"format": "hostcensus-report"`, `"version": 1`) جو `devices` کے ساتھ ہدف، پروب کی گئی سروسز اور ترتیبات ریکارڈ کرتی ہیں؛ `-o` کے بغیر `--format json` ٹیبل کے بجائے رپورٹ کو stdout پر لکھتا ہے۔ ہر JSON آؤٹ پٹ کا ایک شائع شدہ اسکیما ہے؛ [JSON آؤٹ پٹ](../../../docs/json-output.md) دیکھیں۔ آلات اصل `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` اور `errors` فیلڈز برقرار رکھتے ہیں اور ہر پروب کے `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`، یا جب پروب مقامی طور پر ناکام ہوا یا اپنی ڈیڈ لائن تک پہنچ گیا تو `unknown`), `version` اور `details` کے ساتھ ایک `services` لسٹ شامل کرتے ہیں۔ CSV آؤٹ پٹ میں کھلی سروسز کے لیے آخر میں `services` اور `versions` کالم شامل ہوتے ہیں۔ `ssh`, `snmp` اور `mysql` بولینز بالکل انہی ناموں والی سروسز کی پیروی کرتے ہیں۔


## انوینٹری پروفائلز، preflight، اور مقامی ہسٹری

نامزد پروفائلز موجودہ `[services]` تعریفوں کے ساتھ ایک TOML فائل شیئر کرتی ہیں۔ [hostcensus.example.toml](../../../hostcensus.example.toml) کو `hostcensus.toml` پر کاپی کریں اور وہ نیٹ ورکس سیٹ کریں جن کا انتظام آپ کرتے ہیں:

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

`preflight` اختیارات اور پروفائلز کو بالکل `scan` کی طرح حل کرتا ہے، بشمول اوپن فائل چیک کے لیے `--concurrency`، اس لیے کامیاب preflight کا مطلب ہے کہ `scan` اسی پلان کے ساتھ شروع ہوگا۔

پروفائلز `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency`, اور `max_hosts` قبول کرتی ہیں۔ `services` اور `ports` موجودہ کوما لسٹ سنٹیکس استعمال کرتے ہیں۔ واضح CLI اختیارات پروفائل کی ترتیبات پر غالب آتے ہیں؛ بار بار دیے گئے `--exclude` اختیارات پروفائل کے اخراجات میں شامل ہو جاتے ہیں۔ `--profile` کے ساتھ ایک واضح نیٹ ورک اس پروفائل کے IP/CIDR دائرہ کار میں شامل ہونا ضروری ہے۔ براہ راست اسکینز کے لیے ہوسٹ نیمز اب بھی معاون ہیں، لیکن انہیں IP اخراجات کے ساتھ ملایا نہیں جا سکتا۔ ہوسٹ کی حدود اخراجات سے پہلے لاگو ہوتی ہیں؛ کل پروب کی حد بعد میں بھی لاگو رہتی ہے۔ خارج کردہ ہوسٹس کو سروس چیکس اور اختیاری Nmap ڈسکوری دونوں سے خارج کر دیا جاتا ہے۔

ہر اسکین ہدف کی ٹریفک سے پہلے مقامی preflight چیکس انجام دیتا ہے: ہدف/پروب کی حدود، منزل تک رسائی، اختیاری Nmap ایگزیکیوٹیبل/ریپر کی دستیابی، ہسٹری اسکیما، اور ترتیب دیا گیا TLS CA بنڈل۔ `preflight` JSON رپورٹ کرتا ہے اور نہ تو اہداف کو اسکین کرتا ہے اور نہ ہی ہسٹری ڈیٹا بیس بناتا ہے۔ یہ موجودہ مواد کو تبدیل کیے بغیر منزل تک رسائی ٹیسٹ کرنے کے لیے عارضی طور پر ایک ہم مرتبہ فائل لکھتا ہے۔ ڈیفالٹ asyncio بیک اینڈ کو اب بھی نہ Nmap کی ضرورت ہے اور نہ root کی۔ منزل کے پاتھ ایک دوسرے سے اور ان پٹ کنفیگریشن سے مختلف ہونے چاہئیں، بشمول ہارڈ لنکس کے؛ منزل کے سم لنکس مسترد کر دیے جاتے ہیں۔ ناکام چیکس 1 واپس کرتے ہیں؛ غلط دائرہ کار/کنفیگریشن 2 واپس کرتا ہے۔

رپورٹ اور ایکسپورٹ لکھنے کے لیے `O_NOFOLLOW` کی معاونت درکار ہے۔ اس کے بغیر پلیٹ فارمز پر، بشمول Windows، یہ تحریریں منزل کو کھولے یا کاٹے بغیر ناکام ہو جاتی ہیں۔ نئی رپورٹس اور ایکسپورٹ اسکرپٹس صرف مالک کے لیے قابلِ رسائی (موڈ 0600) ہوتی ہیں؛ موجودہ فائل کو تبدیل کرنے سے اس کی اجازتیں برقرار رہتی ہیں۔ بغیر ریڈر والے نامزد پائپ پر لکھنا انتظار کرنے کے بجائے فوراً ناکام ہو جاتا ہے۔ نیا `--history` ڈیٹا بیس بھی صرف مالک کے لیے بنایا جاتا ہے؛ موجودہ ڈیٹا بیس اپنا موڈ برقرار رکھتا ہے۔ لاگ پیغامات ہمیشہ stderr پر جاتے ہیں، اس لیے stdout صرف نتائج لے کر آتا ہے۔ اسناد پر مشتمل ایکسپورٹس ہمیشہ موڈ 0600 نافذ کرتے ہیں۔

ہسٹری opt-in ہے اور موجودہ JSON اسنیپ شاٹس اور `diff` کمانڈ کی تکمیل کرتی ہے:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

`history` سے IDs استعمال کریں؛ مثال ایک نیا ڈیٹا بیس فرض کرتی ہے۔ اسنیپ شاٹس UTC آغاز/اختتام کے اوقات، پیکج ورژن، مؤثر غیر خفیہ ترتیبات، خلاصوں، اور تمام ہوسٹ/سروس مشاہدات بشمول فی ہوسٹ خرابیوں کے ساتھ ٹرانزیکشنل طور پر محفوظ کیے جاتے ہیں۔ نامکمل ہوسٹ مشاہدات برقرار رکھے جاتے ہیں۔ منسوخ شدہ رنز محفوظ نہیں کیے جاتے۔ موجودہ رپورٹ، اسنیپ شاٹ، ایکسپورٹ، اور اسکین ایگزٹ کوڈ معاہدے برقرار رکھے گئے ہیں۔

`history` تمام تاریخی ڈیوائس پے لوڈز کو پڑھے بغیر JSON خلاصے درج کرتا ہے۔ `compare` دو محفوظ شدہ اسکینز پڑھتا ہے، یکساں ہدف کی شناخت اور منتخب پورٹس کا تقاضا کرتا ہے، اور جوابی صلاحیت، حیثیت، اور پورٹ اسٹیٹ کی تبدیلیاں رپورٹ کرتا ہے۔ پہلے والے اسکین کی ID بعد والی ID سے پہلے ہونی چاہیے۔ جب دونوں اسکینز نے `timeout` یا `backend` ریکارڈ کیا ہو اور وہ قدریں مختلف ہوں، تو رپورٹ ایک وارننگ درج کرتی ہے اور پھر بھی مشاہدات کا موازنہ کرتی ہے۔ مختلف انتظار کا وقت کسی فلٹرڈ پورٹ کو کھلا دکھا سکتا ہے۔ اسکینر کی خرابیاں اور نامعلوم پورٹ مشاہدات مصدقہ گمشدگی یا بندش کے بجائے غیر یقینی کے طور پر نشان زد کیے جاتے ہیں: خرابیوں والے ہوسٹس `uncertain_hosts` میں ظاہر ہوتے ہیں، اور `unknown` پر مشتمل ہر پورٹ تبدیلی (بشمول دونوں اسکینز میں unknown) `port_changes` کے بجائے `unconfirmed_ports` میں درج ہوتی ہے، سوائے اس پورٹ کے جو بعد والے اسکین میں open ہو، جو کہ ایک پورٹ تبدیلی ہے۔ `compare` اور `diff` پورٹس کی درجہ بندی اسی اصول سے کرتے ہیں۔ `no_longer_responding` کا مطلب جواب کا نہ ملنا ہے، ڈیوائس ہٹائے جانے کا ثبوت نہیں۔ اسکین ایگزٹ کوڈ 0 اس بات کی ضمانت نہیں دیتا کہ ہر ہوسٹ نے جواب دیا: فی ہوسٹ خرابیاں چیک کریں۔ موازنے کی کامیابی 0 واپس کرتی ہے خواہ تبدیلیاں موجود ہوں یا نہ ہوں؛ موجودہ فائل `diff` اپنا ایگزٹ کوڈ 3 کا معاہدہ برقرار رکھتی ہے۔ غیر معاون یا خراب ہسٹری 1 واپس کرتی ہے۔

ہسٹری انوینٹری کی معلومات محفوظ کرتی ہے، اس لیے مناسب طور پر محفوظ مقامی ڈائریکٹری منتخب کریں۔ پروفائل فائلیں اور محفوظ شدہ ترتیبات SNMP اسناد نہیں رکھتیں؛ اسناد کی ہینڈلنگ موجودہ رن ٹائم اختیارات/ماحولیاتی متغیرات کے ذریعے جاری رہتی ہے۔

## انوینٹری diff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

اسنیپ شاٹ ایک JSON ہے جس میں `format: "hostcensus-snapshot"`, `version: 1`، hostcensus ورژن، UTC تخلیق کا وقت، ہدف، اسکین `timeout` اور `backend` (جب اسکین نے انہیں ریکارڈ کیا ہو)، پروب کی گئی سروسز، اور زندہ ہوسٹس `-o` رپورٹ کی اسی شکل میں ہوتے ہیں۔ ڈاؤن ہوسٹس کو چھوڑ دیا جاتا ہے۔ `diff` سادہ `scan -o` JSON رپورٹس بھی قبول کرتا ہے، بشمول وہ رپورٹس جو `services` فیلڈ کے وجود میں آنے سے پہلے کی ہوں۔

`diff` نئے اور غائب ہونے والے ہوسٹس، دونوں میں موجود ہوسٹس پر کھلنے یا بند ہونے والے پورٹس، اور ان سروسز کو رپورٹ کرتا ہے جن کا `version` تبدیل ہوا۔ جن پورٹس کو دونوں اسکینز میں سے صرف ایک میں پروب کیا گیا تھا ان کا موازنہ نہیں کیا جاتا، اور ایک وارننگ ایسا بتاتی ہے۔ ناکام مشاہدات کو کبھی "کوئی تبدیلی نہیں" نہیں سمجھا جاتا: جو پورٹ کسی بھی اسکین میں `unknown` ہو اور بعد والے میں open نہ ہو اسے `closed` کے بجائے `unconfirmed` کے تحت درج کیا جاتا ہے، جس میں `before` کی قدر `open`, `unknown` یا `not-open` (پروب کیا گیا اور closed یا filtered) اور `after` کی قدر `unknown` یا `not-open` ہوتی ہے؛ جو پورٹ اب کھلا ہے اسے `opened` کے تحت رپورٹ کیا جاتا ہے بھلے ہی پہلے والا پروب ناکام رہا ہو۔ جس ہوسٹ کے تمام پروبز کسی بھی اسکین میں جواب کے بغیر ناکام رہے ہوں اسے `vanished_hosts` کے بجائے `unsettled_hosts` کے تحت درج کیا جاتا ہے (`before`/`after` کی قدر `up`, `uncertain` یا `absent` کے ساتھ، بشمول جب وہ دونوں اسکینز میں ناکام رہا یا دوسری فائل سے غائب ہو)؛ اگر وہ بعد والے اسکین میں جواب دے تو اسے اس کے کھلے پورٹس کے ساتھ ایک نئے ہوسٹ کے طور پر بھی رپورٹ کیا جاتا ہے۔ اسنیپ شاٹس اسی وجہ سے ان ناکام ہوسٹس کو برقرار رکھتے ہیں۔ جب اہداف مختلف ہوں، اور جب دونوں فائلوں نے timeout یا backend ریکارڈ کیا ہو اور وہ قدریں مختلف ہوں تب بھی ایک وارننگ ظاہر ہوتی ہے۔ `-o PATH` JSON شکل کو ایک فائل میں بھی لکھتا ہے۔

`--deadline` کے ذریعے روکے گئے اسکین (`"complete": false`) کی رپورٹ صرف ان ہوسٹس کو درج کرتی ہے جن تک وہ پہنچ سکا، اس لیے `diff` اور `export` اسے ایگزٹ کوڈ 2 کے ساتھ مسترد کر دیتے ہیں۔ `--allow-partial` اسے stderr پر ایک وارننگ کے ساتھ قبول کرتا ہے: `diff` پھر ان ہوسٹس کو جنہیں نامکمل اسکین نے بالکل درج نہیں کیا vanished کے بجائے `unsettled_hosts` کے تحت `unscanned` کے طور پر درج کرتا ہے (جو ہوسٹ اس نے down کے طور پر درج کیا وہ اب بھی vanished رہتا ہے)، `partial` کو true سیٹ کرتا ہے اور کبھی no change رپورٹ نہیں کرتا، اور `export` اسکرپٹ ہیڈر میں ایک وارننگ لکھتا ہے۔

`diff` ایگزٹ کوڈز: `0` کوئی تبدیلی نہیں، `3` تبدیلیاں ملیں، ایسے مشاہدات جن کی تصدیق نہیں ہو سکی، یا نامکمل ان پٹ (`changed` تب true ہوتا ہے جب کوئی بھی لسٹ، بشمول `unsettled_hosts` اور `unconfirmed`، غیر خالی ہو، یا `partial` true ہو)، `2` کوئی فائل غائب، ناقابلِ مطالعہ، معاون اسنیپ شاٹ نہیں، یا `--allow-partial` کے بغیر نامکمل ہے، `1` `-o` فائل لکھی نہیں جا سکی۔

## Kadupul ایکسپورٹ

[Kadupul](https://github.com/kadupulhq/kadupul) (Cacti 1.2.31 کا ایک فورک) میں بلک ڈیوائس فائل امپورٹ موجود نہیں ہے۔ اسکرپٹ سے آلات شامل کرنے کا اس کا معاون طریقہ `cli/add_device.php` ہے، فی کال ایک ڈیوائس، `--option=value` آرگیومنٹس کے ساتھ۔ `hostcensus export` ان کالز کی ایک POSIX `sh` اسکرپٹ لکھتا ہے:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

ہر زندہ ہوسٹ `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` بن جاتا ہے:

- جن ہوسٹس پر اسکین کا SNMP استفسار کامیاب رہا انہیں `--version=2 --community=...` یا `--version=3 --username=... --authproto=... --password=...` (authPriv کے لیے مزید `--privproto`/`--privpass`)، `--port` اور `--avail=snmp` ملتے ہیں۔ SNMPv3 ایکسپورٹ کے لیے `--snmp-user` درکار ہے، اور noAuthNoPriv مسترد کر دیا جاتا ہے کیونکہ `add_device.php` کو v3 پاس ورڈ درکار ہوتا ہے۔
- دیگر ہوسٹس کو `--version=0 --avail=ping` ملتا ہے، ساتھ ہی `--ping_method=tcp --ping_port=` میں پہلا کھلا TCP پورٹ، یا اگر کوئی نہ ہو تو ICMP۔
- `--notes` کھلی سروسز اور ورژنز کو درج کرتا ہے۔ `--description` ریورس-DNS نام ہوتا ہے جب وہ سادہ ہو (حروف، ہندسے، `.`, `_`, `-`)، ورنہ IP، اور اسے منفرد بنایا جاتا ہے، کیونکہ `add_device.php` موجودہ تفصیل کو اس ڈیوائس کی اپ ڈیٹ کے طور پر لیتا ہے۔

ہر قدر کی توثیق کی جاتی ہے اور اسے `shlex.quote` کے ساتھ شیل کوٹ کیا جاتا ہے۔ ڈیفالٹ طور پر کوئی SNMP راز نہیں لکھا جاتا: اسکرپٹ رن ٹائم پر `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` یا `HOSTCENSUS_SNMP_PRIV_KEY` کو پھیلاتی ہے اور اگر کوئی سیٹ نہ ہو تو رک جاتی ہے۔ `--include-credentials` اس کے بجائے ان ماحولیاتی متغیرات کی قدریں اسکرپٹ میں لکھ دیتا ہے، اسے موڈ 0600 کے ساتھ بناتا ہے، اور ایک وارننگ لاگ کرتا ہے۔ `add_device.php` خود کمیونٹی کو پرنٹ کرتا ہے اور رازوں کو آرگیومنٹس کے طور پر وصول کرتا ہے، جو ہر کال چلتے وقت Kadupul سرور کی پروسیس لسٹ میں نظر آتے ہیں۔

`add_device.php` ڈپلیکیٹس اور خرابیوں کے لیے 1 کے ساتھ باہر نکلتا ہے؛ اسکرپٹ جاری رہتی ہے، ناکامیوں کو گنتی ہے، اور اگر کوئی ڈیوائس شامل نہ ہو سکی تو 1 کے ساتھ باہر نکلتی ہے۔ ٹیمپلیٹ آئی ڈیز `php cli/add_device.php --list-host-templates` سے آتی ہیں۔ `export` ایگزٹ کوڈز: `0` لکھا گیا، `2` ناقابلِ مطالعہ ان پٹ، `--allow-partial` کے بغیر نامکمل اسکین، یا ایسا ڈیٹا جسے محفوظ طریقے سے ایکسپورٹ نہیں کیا جا سکتا، `1` اسکرپٹ لکھی نہیں جا سکی۔

## ورژننگ اور ریلیز کا عمل

hostcensus [Semantic Versioning](https://semver.org/spec/v2.0.0.html) کی پیروی کرتا ہے: مطابقت پذیر اصلاحات پیچ ورژن میں اضافہ کرتی ہیں، مطابقت پذیر فیچرز/ڈپریکیشنز مائنر ورژن میں اضافہ کرتے ہیں، اور بریکنگ مطابقت کی تبدیلیاں میجر ورژن میں اضافہ کرتی ہیں۔ کمانڈز اور اختیارات، ایگزٹ کوڈز اور JSON اسکیماز عوامی معاہدہ ہیں؛ ڈپریکیٹڈ رویہ اگلی بڑی ریلیز تک کام کرتا رہتا ہے، جب تک کہ کوئی سیکیورٹی فکس اسے جلد تبدیل کرنے کا تقاضا نہ کرے (تب changelog وجہ بیان کرتا ہے)۔

release-please `main` پر Conventional Commit عنوانات سے ایک ریلیز PR کھولتا ہے، جو `pyproject.toml`, `uv.lock` اور `CHANGES.md` کو اپ ڈیٹ کرتا ہے۔ اسے ضم کرنے سے `vMAJOR.MINOR.PATCH` ٹیگ اور ایک ڈرافٹ GitHub ریلیز بنتی ہے، جس کے ساتھ CI ایک ٹیسٹ شدہ wheel، سورس ڈسٹری بیوشن اور checksums منسلک کرتا ہے؛ GitHub اپنی attestations API کے ذریعے ان فائلوں کے لیے بلڈ اٹیسٹیشنز محفوظ کرتا ہے۔ ایک مینٹینر فائلیں منسلک ہونے کے بعد ڈرافٹ کا جائزہ لیتا ہے اور اسے شائع کرتا ہے۔ ریلیزز کو کبھی تبدیل نہیں کیا جاتا۔

PyPI ٹرسٹڈ پبلشنگ opt-in ہے اور اس کے لیے پروجیکٹ کی ملکیت، ایک ٹرسٹڈ پبلشر اور `pypi` ماحول درکار ہے۔ یہ بغیر دوبارہ بلڈ کیے یا API ٹوکن محفوظ کیے وہی چیک شدہ ریلیز آرٹیفیکٹس شائع کرتی ہے۔ اس عوامی ریپوزٹری میں ٹیگ شدہ ریلیزز GitHub آرٹیفیکٹ اٹیسٹیشنز تیار کرتی ہیں؛ پرائیویٹ فورکس کے لیے ایک معاون پلان اور واضح opt-in درکار ہے۔ سیٹ اپ، درست کمانڈز اور ریٹرائز کے لیے [مکمل ریلیز گائیڈ](../../../docs/releasing.md) دیکھیں۔

## ترقی

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

ڈیولپمنٹ ٹولز `pyproject.toml` میں [PEP 735](https://peps.python.org/pep-0735/) ڈیپینڈنسی گروپس (`dev`, `fuzz`, `build`) میں رہتے ہیں، اس لیے وہ کبھی شائع شدہ پیکج میٹا ڈیٹا میں ظاہر نہیں ہوتے۔ `uv.lock` واحد لاک فائل ہے؛ CI `uv sync --locked` کے ساتھ انسٹال کرتا ہے اور جب لاک فائل پرانی ہو تو ناکام ہو جاتا ہے۔ `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), یا کسی بھی Python 3.12+ کے ساتھ انٹرپریٹر منتخب کریں۔

CI 90% پیکج کوریج کی کم از کم حد نافذ کرتا ہے۔ یونٹ ٹیسٹس میں کنٹرولڈ لوپ بیک سرورز اور آف لائن پروفائل/ہسٹری/ریلیز-ویلیڈیٹر کیسز شامل ہیں؛ Compose لیب ایک الگ تھلگ برج پر OpenSSH, MariaDB, nginx اور net-snmp چلاتی ہے۔ اسے `make test-integration` کے ساتھ چلائیں۔ ڈیولپمنٹ ورک فلو اور تفصیلات کے لیے [CONTRIBUTING.md](../../../CONTRIBUTING.md) اور [ریلیز ٹولنگ](../../../scripts/README.md) دیکھیں۔

رن ٹائم کنٹینر UID/GID 10001 کے طور پر چلتا ہے جس میں کوئی ہوم ڈائریکٹری، شیل لاگ ان اور pip نہیں ہوتا، اور `/app/output` پر لکھ سکتا ہے۔ اس صارف کو کسی بھی ماؤنٹ کردہ آؤٹ پٹ ڈائریکٹری تک لکھنے کی رسائی دیں۔ اسے کسی capabilities کی ضرورت نہیں ہے اور یہ صرف پڑھنے کے قابل روٹ فائل سسٹم کے ساتھ کام کرتا ہے، لہٰذا اسے اس طرح چلایا جا سکتا ہے:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap اس کنٹینر میں اپنا غیر مراعات یافتہ TCP ڈسکوری رویہ استعمال کرتا ہے۔ CI امیج بلڈ کو کسی بھی قابلِ اصلاح HIGH یا CRITICAL کمزوری پر ناکام کر دیتا ہے جو Trivy رپورٹ کرے۔

## سپلائی چین چیکس

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) main پر اور ہفتہ وار چلتا ہے، اپنا حقیقی اسکور شائع کرتا ہے، اور نتائج کو GitHub کوڈ اسکیننگ پر اپ لوڈ کرتا ہے۔ ایکشنز اور کنٹینر بیسز غیر متغیر ہیشز سے پن کیے گئے ہیں؛ Python انحصار `uv.lock` میں حل کیے گئے ہیں۔ Bandit کی ناکامیاں CI کو ناکام کر دیتی ہیں، اور محدود Atheris فزنگ نیٹ ورک رسائی کے بغیر SSH, MySQL, HTTP, سرٹیفکیٹ اور SNMPv3 BER پارسرز کی جانچ کرتی ہے۔

Scorecard تاریخی ریویو سرگرمی، کنٹری بیوٹر کے تنوع، اور ریلیز پروویننس کی پیمائش بھی کرتا ہے۔ وہ اسکور حقیقی شواہد کی عکاسی کرتے ہیں؛ وہ اس بات کے دعوے نہیں ہیں کہ ہر گورننس یا تاریخی ریلیز چیک پورا ہو گیا ہے۔ مزید کے لیے [SECURITY.md](../../../SECURITY.md) اور [ریلیز پروویننس](../../../docs/releasing.md) دیکھیں۔

## لوکلائزیشن

CLI پیغامات اور ٹرمینل خلاصہ/diff ٹیبلز بغیر کسی اضافی رن ٹائم انحصار کے 45 لوکیلز (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) کی معاونت کرتے ہیں۔ ریزولوشن `--lang`، پھر `LC_ALL`, `LC_MESSAGES`, اور `LANG` کا احترام کرتا ہے، اور آخر میں `en` پر واپس آتا ہے۔ JSON اسکیماز، CSV کالمز، اور ایکسپورٹ اسکرپٹس تمام لوکیلز میں غیر تبدیل شدہ رہتے ہیں۔

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## تعاون

تعاون میں ایک قابلِ تکرار کیس شامل ہونا چاہیے، دستاویز کردہ CLI اور ڈیٹا فارمیٹ معاہدوں کو برقرار رکھنا چاہیے، اور اوپر دیے گئے معیار کے چیکس پاس کرنے چاہئیں۔ ڈیولپمنٹ ورک فلو کے لیے [CONTRIBUTING.md](../../../CONTRIBUTING.md) اور مطابقت و ورژننگ کے فیصلوں کے لیے [ریلیز گائیڈ](../../../docs/releasing.md) دیکھیں۔

## سیکیورٹی اور لائسنس کی حیثیت

پرائیویٹ رپورٹنگ اور معاون ورژنز کے لیے [SECURITY.md](../../../SECURITY.md) دیکھیں۔
hostcensus [MIT لائسنس](../../../LICENSE) کے تحت لائسنس یافتہ ہے۔

سورس ہیڈرز SPDX آئیڈینٹیفائرز استعمال کرتے ہیں اور Git ہسٹری سے شراکت داروں کا کریڈٹ محفوظ رکھتے ہیں۔ انتساب کے لیے [AUTHORS.md](../../../AUTHORS.md) دیکھیں۔ بائنری ٹیسٹ کیپچرز اور تیار کردہ لاک فائل ملحقہ `.license` فائلیں استعمال کرتے ہیں؛ MIT کا متن `LICENSES/MIT.txt` میں موجود ہے۔
