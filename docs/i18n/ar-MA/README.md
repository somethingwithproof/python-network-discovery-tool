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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · **العربية (المغرب)** · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus هو أداة سطر أوامر (CLI) مكتوبة بـ Python باش دير جرد متكرر ديال الخدمات ف الشبكات اللي كتسيّرها.
كيسجّل شنو كتبيّن الأجهزة، كيقارن الملاحظات مع الوقت، وكيولّد سكريبتات ديال الاستيراد لـ Kadupul. الباكاند الافتراضي كيستعمل asyncio sockets بلا صلاحيات root؛ وتقدر تستعمل الاكتشاف الاختياري بـ Nmap باش تتعرف على الأجهزة اللي خارج بورتات الخدمات المكونفيغورية.

## علاش hostcensus

تقرير ديال البورتات دار مرة وحدة ما كيشرحش واش الملاحظة الجاية تبدلات ولا غير فشلات. hostcensus كيجمع بين حالات خدمات واضحة، فحوصات محدودة ف الوقت والحجم، بروفايلات سكان تقدر تعاود تستعملها، وتاريخ محلي. المسيرين يقدرو يعاودو نفس النطاق، يشوفو الأخطاء بالتفصيل، ويفرّقو بين الملاحظات اللي ما مأكدّاش وبين التغييرات المؤكدة.

- **أدلة الخدمات:** التعريف ديال SSH، رسائل الترحيب ديال MySQL، هيدرات HTTP، ملاحظات شهادات TLS، واكتشاف SNMP ولا استعلامات system-MIB بالاعتمادات.
- **نطاق قابل للتكرار:** بروفايلات TOML مسمية، استثناءات إضافية، خدمات قابلة للتعديل، حدود قصوى للأجهزة والفحوصات، وعمال (workers) محدودين ف العدد.
- **فحوصات قبل الترافيك:** الفحص المسبق المحلي (preflight) كيتأكد من الأهداف، الأدوات، صلاحية الوصول لمسارات الإخراج، بنية قاعدة بيانات التاريخ، وحزم شهادات TLS CA المكونفيغورية.
- **تاريخ الجرد:** لقطات SQLite بمعاملات (transactional) كتحافظ على جميع الملاحظات؛ والمقارنات كتخلي أعطال السكان والحالات المجهولة باينة وواضحة.
- **مخرجات متوافقة:** تقارير ف التيرمينال و JSON و CSV، لقطات ملفات مرقّمة بالإصدار، وسكريبتات استيراد لـ Kadupul.

الـ CI كيغطي Python 3.12 و 3.13 و 3.14 على Linux و macOS، زائد مختبر تكامل مضبوط بـ Compose. الكود كيستعمل type aliases حديثة، نتائج preflight محددة النوع، بروفايلات بـ slots ومعاملات keyword-only، وتنظيف async منظم مع الحفاظ على دعم هاد إصدارات التشغيل. شوف [الإصدارات والإطلاقات](../../../docs/releasing.md) على ود عقد التوافق ديال SemVer وطريقة الإطلاق على GitHub. الشارة ديال الإصدار كتوصف الحزم المنشورة، ماشي هاد النسخة المحلية (checkout): آخر tag منشور دابا هو `v0.3.0`، بينما هاد النسخة المحلية كتستعمل إصدار الحزمة `3.0.0`. ثبت من النسخة المحلية باش تستعمل ميزات الجرد المشروحة هنا.

بدا بـ [التثبيت](#install)، ومن بعد شوف [البروفايلات والتاريخ](#inventory-profiles-preflight-and-local-history).
على ود تفاصيل التكامل، شوف [بصمات الخدمات](#fingerprints)،
[مقارنة الملفات](#inventory-diff)، و[التصدير لـ Kadupul](#kadupul-export).

## التثبيت

خاصك Python 3.12 ولا أحدث؛ الإصدارات المختبرة هي من Python 3.12 حتى 3.14. من هاد النسخة المحلية، ثبت الاعتماديات المقفولة ديال التشغيل:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

على ود اكتشاف الأجهزة الاختياري بـ Nmap، ثبت البرنامج التنفيذي ديال Nmap بمدير الحزم ديال النظام ديالك؛ ما كتحتاجش حتى شي حزمة Python زايدة. مخرجات XML ديال Nmap كتتحلل بـ defusedxml، اللي هي اعتمادية أساسية، باش يتمنع توسيع الكيانات (entity expansion). hostcensus كيشغّل `nmap` اللي كاين ف `PATH` مباشرة بلائحة معاملات ثابتة، ومهلة زمنية كتكبر على حساب الحجم ديال البريفيكس، وسقف إخراج ديال 64 MiB. ما كتحتاجش Nmap مع الباكاند الافتراضي.

## الانتقال من netprobe

hostcensus هو السمية الجديدة ديال netprobe، اللي خرجات ف الإصدار 3.0.0. المشروع ما عمره تنشر ف PyPI بحتى سمية منهم، يعني التثبيت كان ديما كيدّار من نسخة محلية ولا من إصدار على GitHub. الريبو على GitHub كيبقى بنفس السمية.

| كان قبل | دابا | التوافق |
| --- | --- | --- |
| التوزيعة `netprobe` | `hostcensus` | عاود التثبيت من النسخة المحلية؛ ما بقاتش حزمة بالسمية القديمة. |
| الأمر `netprobe` | `hostcensus` | `netprobe` باقي خدام وكيطبع سطر تحذير واحد على stderr باللي راه قديم. أكواد الخروج و stdout ما تبدلوش. غادي يتحيّد ف الإصدار الرئيسي الجاي. |
| متغيرات البيئة `NETPROBE_*` | `HOSTCENSUS_*` | كيتستعمل متغير `NETPROBE_*` إلا كان المقابل ديالو `HOSTCENSUS_*` ما مضبوطش، مع تحذير واحد ف stderr كيذكر أسماء المتغيرات وعمره ما كيطبع القيم ديالهم. `HOSTCENSUS_*` كيربح إلا كانو بجوج مضبوطين. غادي يتحيّد ف الإصدار الرئيسي الجاي. |
| `import netprobe`، `python -m netprobe` | `import hostcensus`، `python -m hostcensus` | **تغيير كاسر للتوافق.** ما كاين حتى shim للاستيراد؛ خاصك تحدث سطور الاستيراد. |
| تاغ صورة Docker `network-discovery:test` (غير ف CI) ومستخدم الحاوية `netprobe` | `hostcensus:test`، المستخدم `hostcensus` | ما عمر شي صورة تنشرات ف registry. عاود بني الصورة واستعمل نقطة الدخول `hostcensus`. |
| `netprobe.toml`، `netprobe-history.sqlite3` | `hostcensus.toml`، `hostcensus-history.sqlite3` | إلا كان كاين ملف بالسمية الافتراضية القديمة، راه كيبقى يتستعمل مع تحذير، مادام الملف بالسمية الجديدة ما كاينش. المسارات الصريحة `--config` و `--history` ما كيتقاسوش. |
| التقارير واللقطات اللي فيهم `"format": "netprobe-report"` ولا `"netprobe-snapshot"`، وحقل `netprobe_version` | `hostcensus-report`، `hostcensus-snapshot`، `hostcensus_version` | `diff` و `export` باقيين كيقراو الملفات اللي تكتبو بالسمية القديمة، ومخططات JSON Schemas المنشورة كتقبل الصيغتين بجوج. الملفات الجديدة كتستعمل السميات الجديدة. قواعد بيانات التاريخ ديال SQLite ما تبدلاتش وكتتحمل بحال قبل. |
| سكريبتات Kadupul من `netprobe export` | سكريبتات من `hostcensus export` | السكريبتات القديمة كتبقى خدامة وكتقرا `NETPROBE_SNMP_*` ملي كتشتاغل. السكريبتات الجديدة كتقرا `HOSTCENSUS_SNMP_*`. |

## مثال سريع

تشغيل من حاوية الاختبار (tester) ف مختبر التكامل المشروح تحت قسم التطوير؛ المخرجات مختصرة:

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

## أكواد الخروج

| الأمر | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | الملاحظات والتقرير تسجّلو | فشل preflight ولا الباكاند، ولا كتابة التاريخ ولا التقرير ولا اللقطة | هدف ولا خيارات ولا إعدادات ولا حدود ما صالحاش | - | وصل `--deadline`؛ تكتب تقرير جزئي وتجاوز كتابة التاريخ واللقطة |
| `preflight` | الفحوصات دازو بنجاح | فشل فحص محلي | هدف ولا إعدادات ما صالحاش ولا مسارات إخراج متعارضة | - | - |
| `profiles` | تعرْضو البروفايلات المتحقّق منها | - | إعدادات ولا اختيار ما كيتقراش ولا ما صالحش | - | - |
| `history` | تعرْضو الملخصات | تاريخ ناقص ولا ما صالحش ولا ما مدعومش | خيارات CLI ما صالحاش | - | - |
| `compare` | تخرّجات المقارنة، بما فيها إلا كانو تغييرات | تاريخ ما كيتقراش، نطاق ولا ترتيب غير متوافق، ولا فشل ف الكتابة | خيارات CLI ما صالحاش | - | - |
| `diff` | ما كاين حتى تغيير | ما قدرش يكتب ملف `-o` | مدخلات ناقصة ولا ما كتتقراش ولا ما مدعوماش، ولا سكان ناقص بلا `--allow-partial` | تلقاو تغييرات، ملاحظات ما مأكدّاش، ولا سكان ناقص | - |
| `export` | السكريبت تكتب | ما قدرش يكتب السكريبت | مدخلات ما كتتقراش، سكان ناقص بلا `--allow-partial`، ولا بيانات ما يمكنش تتصدّر بأمان | - | - |

## بنية المشروع

| الموديول | المسؤولية |
| --- | --- |
| `cli.py` | خيارات الأوامر، تحديد البروفايلات، preflight، السكان وإصدار التقارير |
| `scanner.py`، `probes.py` | توسيع الأهداف، العمال المحدودين، اكتشاف الأجهزة وملاحظات الخدمات |
| `config.py`، `profiles.py` | تعريفات الخدمات وبروفايلات الجرد المتحقّق منها |
| `models.py`، `output.py` | أنواع النتائج والعرض ف التيرمينال و JSON و CSV |
| `history.py`، `diff.py` | تاريخ SQLite ومقارنات لقطات الملفات المرقّمة بالإصدار |
| `preflight.py` | الفحوصات المحلية والتحقق المحدود من إصدار Nmap |
| `export.py` | سكريبتات استيراد Kadupul متحقّق منها ومحمية بالاقتباس |

كل ملاحظة خدمة كتسجّل الحالة ديالها بوحدها ومفصولة على الهوية اللي كتعرضها.
القراءات والمهل الزمنية محدودة؛ وأخطاء الفحص كتبقى مسجّلة ف أخطاء الجهاز. تاريخ SQLite كيستعمل المعاملات (transactions)، وتنظيف صريح للاتصالات، ومسارات للقراءة فقط على ود العرض والمقارنة. الأسرار ديال SNMP كتدخل غير عبر متغيرات البيئة ولا ملفات الأسرار؛ وتاريخ الجرد كيخزن غير الإعدادات الفعلية اللي ماشي سرية. شوف [البنية المعمارية](../../../docs/architecture.md) على ود مسار السكان والحدود ديالو وحدود الثقة، و[SECURITY.md](../../../SECURITY.md#authorized-use) على ود الاستخدام المرخّص.


## الاستعمال

دير السكان غير للشبكات اللي كتسيّرها.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| الخيار | المعنى |
| --- | --- |
| `NETWORK` | CIDR ولا IP ولا اسم مضيف (hostname)؛ اختياري مع `--profile`. معرفات نطاق IPv6 كترفض. |
| `-o, --output PATH` | كتابة تقرير ف ملف. الصيغة كتتبع الامتداد (`.json`، `.csv`)؛ الامتدادات الأخرى كترجع تلقائياً لـ JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | فرض صيغة التقرير. ما عندو حتى تأثير بلا `--output`. الامتداد `.sh` كيختار `kadupul`. |
| `-v, --verbose` | تفعيل سجلات التصحيح (debug). |
| `-q, --quiet` | إخفاء النتائج والتقدم والسجلات الإخبارية؛ التحذيرات والأخطاء كتبقى تبان ف stderr. |
| `--backend asyncio\|nmap` | طريقة اكتشاف الأجهزة. `asyncio` (افتراضي) كيفحص بورتات الخدمات مباشرة؛ `nmap` كيدير مسح ping بـ nmap الأول وكيحتاج البرنامج التنفيذي `nmap` يكون ف `PATH`. |
| `--timeout SECONDS` | مدة الانتظار للفحوصات اللي ما حدداتش مهلتها الخاصة (الافتراضي 1.0). فحوصات الاتصال المدمجة كتستعمل 0.3s إلا ما حددش جدول الخدمات قيمة `timeout`. |
| `--concurrency N` | عدد الفحوصات اللي كتخدم ف نفس الوقت (الافتراضي 256). |
| `--deadline SECONDS` | كيوقف السكان كامل، بما فيه مسح nmap، من بعد هاد المدة (الافتراضي 3600، والحد الأقصى 604800؛ متغير البيئة `HOSTCENSUS_DEADLINE`). الأجهزة اللي سالات كتتكتب ف التقرير مع `"complete": false`، وما كيتكتب لا تاريخ لا لقطة، والأمر `scan` كيخرج بالكود 4. |
| `--config PATH` | ملف TOML فيه تعريفات الخدمات وإعدادات `[profiles]` مسمية اختيارية. |
| `--profile NAME` | استعمال بروفايل مسمّى؛ كيرجع افتراضياً لـ `hostcensus.toml` ملي ما كيتعطاش `--config`. |
| `--exclude IP/CIDR` | إضافة استثناء؛ تقدر تعاودو على قد الحاجة. استثناء جهاز IPv4 كيستثني حتى عناوين IPv6 اللي كتوصل ليه: IPv4-mapped (`::ffff:a.b.c.d`) و NAT64 (`64:ff9b::/96`) و 6to4. الأهداف والاستثناءات ديال IPv4-mapped كيتعاملو بحال عناوين IPv4 اللي كيمثلوها. |
| `--max-hosts N` | سقف عدد العناوين اللي كيتحقق منو قبل الاستثناءات (الافتراضي والحد الأقصى الصارم هو 65,536). |
| `--history PATH` | تسجيل السكان المكتمل ف قاعدة بيانات تاريخ SQLite اختيارية. |
| `--services NAMES` | لائحة مفصولة بفواصل ديال أسماء الخدمات اللي بغيتي تفحص، بنفس الترتيب (الافتراضي: كلشي). |
| `--ports SPEC` | لائحة مفصولة بفواصل ديال `NAME=PORT` (تبديل بورت خدمة) ولا `PORT` (إضافة فحص TCP عادي سميتو `tcp-PORT`). |
| `--snmp-community-file PATH` | ملف فيه community ديال SNMPv2c لاستعلام system MIB. متغير البيئة: `HOSTCENSUS_SNMP_COMMUNITY` (القيمة) ولا `HOSTCENSUS_SNMP_COMMUNITY_FILE` (المسار). |
| `--snmp-user` | مستخدم SNMPv3. متغير البيئة: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`، `SHA` (افتراضي)، `SHA224`، `SHA256`، `SHA384`، `SHA512` وملف فيه عبارة المرور. متغير البيئة: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`، `HOSTCENSUS_SNMP_AUTH_KEY` ولا `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`، `AES` (افتراضي)، `AES128`، `AES192`، `AES192C`، `AES256`، `AES256C` وملف فيه عبارة المرور. متغير البيئة: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`، `HOSTCENSUS_SNMP_PRIV_KEY` ولا `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | كتابة لقطة مرقّمة بالإصدار حتى هي على ود `hostcensus diff`. |
| `--tls-ca-file PATH` | التحقق من شهادات HTTPS مقابل حزمة PEM هادي ف بلاصة مخزن النظام. متغير البيئة: `HOSTCENSUS_TLS_CA_FILE`. |

بشكل افتراضي كل جهاز كيتفحص فيه SSH (TCP 22)، و SNMP (UDP 161)، و MySQL (TCP 3306)، و HTTP (TCP 80)، و HTTPS (TCP 443). بورتات TCP كتتختبر باتصال كامل (full connect). أما SNMP فكيتختبر بطلب اكتشاف محرك SNMPv3، واللي أي وكيل SNMPv3 خاصو يجاوب عليه بلا اعتمادات؛ الوكلاء اللي كيهضرو غير بـ v1/v2c ما غاديش يتكتاشفو بهاد الفحص. مع باكاند asyncio، الجهاز كيتحسب حي ملي أي فحص كياخد جواب، حتى إلا كان اتصال مرفوض، يعني الجهاز اللي كيرمي جميع الفحوصات كيكون عندو `alive=false` والخطأ "Host is down"؛ هادا ما كيثبتش باللي راه طافي فعلياً. ومع `--backend nmap`، nmap هو اللي كيقرر شكون الأجهزة اللي حية (بـ ICMP بصلاحيات root، ولا TCP 80/443 ف الحالات الأخرى).

### بصمات الخدمات

كل خدمة محلولة كتتاخد البصمة ديالها من داكشي اللي كتبعثو قبل أي تسجيل دخول. حتى حاجة ما كدير المصادقة من غير استعلام SNMP، وغير ملي كتعطيه الاعتمادات.

| الفحص | شنو كيقرا | `version` | مفاتيح `details` |
| --- | --- | --- | --- |
| `ssh` | سطر التعريف ديال RFC 4253 | البرنامج، مثلاً `OpenSSH_10.0` | `protocol`، `software`، `comments` |
| `mysql` | المصافحة الأولية ديال MySQL/MariaDB | إصدار السيرفر | `server_version`، `flavor`، `auth_plugin`، ولا `error_code`/`error` |
| `http` | جواب `HEAD /` | هيدر `Server` | `status`، `server` |
| `https` | مصافحة TLS، الشهادة، `HEAD /` | هيدر `Server` | `tls_version`، `cert_verified`، `cert_verify_error`، `cert_subject`، `cert_issuer`، `cert_sans`، `cert_not_before`، `cert_not_after` (UTC ISO 8601)، `cert_self_signed`، `status`، `server` |
| `snmp` | اكتشاف SNMPv3؛ ومع الاعتمادات، طلب GET ديال sysDescr و sysObjectID و sysName | sysDescr | `engine_id`؛ ومع الاعتمادات `snmp_version`، `sys_descr`، `sys_object_id`، `sys_name`، ولا `snmp_error` |

الهدف اللي كيكون اسم مضيف (hostname) كيتحل مرة وحدة لكل جهاز وكل فحص كيتصل بهاد العنوان اللي كيتسجّل ف النتائج باسم `address`؛ والسمية كتستعمل غير لـ TLS SNI والتحقق من الشهادة وهيدر HTTP `Host`. الاسم اللي ما كيتحلش كيعطي حالات `unknown` وخطأ `Cannot resolve`. أسماء Reverse DNS كيتحافظ عليها غير إلا كانت فيها غير حروف صالحة لأسماء المضيفين، وبحد أقصى 16 استعلام ف نفس الوقت. HTTPS كيستعمل التحقق من الشهادة واسم المضيف مقابل مخزن النظام ولا `--tls-ca-file`. مخزن الثقة كيتحمّل مرة وحدة للسكان وكيتعاود يستعمل ف كل فحص HTTPS. اتصال TCP ومصافحة TLS كيتحسب ليهم الوقت بشكل منفصل، يعني البورت اللي كيقبل الاتصال ولكن كيوقف ف المصافحة كيتسجّل `open` مع `tls_error`، ماشي `filtered`. إلا فشل التحقق، النتيجة كتسجّل `cert_verified: false` و `cert_verify_error`؛ وما كيعاودش المحاولة بإعدادات أضعف ولا كيبعث طلب HTTP. تفاصيل الشهادة وهيدرات HTTP كيتجمعو غير من بعد ما ينجح التحقق. عطيه حزمة CA الصحيحة للخدمات اللي كتستعمل CA خاص. التقارير القديمة يقدرو يكونو فيها `cert_read_unverified`، واللي الفحوصات الحالية ما بقاتش كتنتجها.

أسرار SNMP كتتقرا غير من متغيرات البيئة ولا من الملفات (`--snmp-*-file`، ولا المتغير المقابل `HOSTCENSUS_SNMP_*_FILE`)، وعمرها ما كتتقرا من قيم سطر الأوامر، حيت المستخدمين المحليين الآخرين يقدرو يشوفوها ف لائحة العمليات. `--snmp-community` و `--snmp-auth-key` و `--snmp-priv-key` بقيمة مباشرة كيخرجو بالكود 2 وكيعطيو سمية البديل. ملف السر خاصو يكون UTF-8 ما خاويش وبحجم ما كيفوتش 4096 بايت؛ كيتجاهل سطر جديد واحد ف اللخر، وتحديد متغير وملف ف نفس الوقت لنفس السر كيتعتبر خطأ. الأخطاء كتذكر اسم الملف ولكن عمرها ما كطبع المحتوى ديالو. تقارير السكان والتاريخ ما كيدخلوش قيم الاعتمادات بشكل مقصود. أداة التصدير عندها خيار منفصل وصريح `--include-credentials` مشروح لتحت. وجود community كيختار SNMPv2c؛ ووجود user كيختار SNMPv3، مع المصادقة ملي كيتعطى مفتاح auth ومع التشفير (privacy) ملي كيتعطاو المفاتيح بجوج (`snmp_security_level` كيسجّل شنو تستعمل). hostcensus كيرفض، بكود الخروج 2، يجمع بين community ومستخدم v3، ولا يستعمل مفتاح privacy بلا مفتاح auth، ولا يستعمل مفاتيح بلا مستخدم، وعمره ما كيعاود استعلام v3 فاشل بـ v2c ولا بمستوى أمان أقل. الوكلاء اللي كيهضرو غير بـ v1/v2c كيتجاهلو اكتشاف v3 اللي بلا اعتمادات، داكشي علاش كيبانو محلولين غير ملي كتعطي community.

نص البانر كيتصفّى باش يبقاو غير الحروف القابلة للطباعة وكيتحدّ ف 256 حرف قبل ما يتخزن ولا يتعرض. القراءات حتى هي محدودة: 4 KiB لكل سطر، 4 KiB لرسالة الترحيب ديال MySQL، و 16 KiB لهيدرات HTTP. معرف محرك SNMP اللي كيكون طولو كثر من 32 أوكتي كيتقطع قبل التخزين. HTTP و HTTPS كيبعثو هيدر Host بعنوان IPv6 بين معقوفتين وبإضافة البورت ملي ما كيكونش 80 ولا 443. خلايا CSV اللي كتبدا برموز صيغ الجداول الحسابية كتتزاد ليها بادئة باش الخلية تبقى نص عادي.

### الحدود

تشغيل واحد كيقبل بحد أقصى 65,536 عنوان، 64 خدمة، و 524,288 فحص (عدد الأجهزة مضروب ف عدد الخدمات)؛ الطلبات اللي كبر من هادشي كتخرج بالكود 2 قبل ما يتبعث حتى حاجة. `--concurrency` محدود ف 4096 socket. كل فحص عندو مهلة قاطعة كتساوي ربعة المرات المهلة ديالو. فحوصات الاتصال (`tcp`، `ssh`، `mysql`، `http`) كتستعمل 0.3 ثانية إلا ما حدداتش الخدمة قيمة `timeout`. أما SNMP و HTTPS فكيستعملو `--timeout` (الافتراضي 1.0) ملي ما كتكونش مهلة محددة. الفحص اللي كيوصل للمهلة القاطعة كيتسجّل `unknown` مع "probe timed out" ف `errors`. أعطال الـ sockets المحلية (بحال ملي كيساليو واصفات الملفات file descriptors) حتى هي كتتسجل `unknown` مع تسجيل الخطأ؛ وعمرها ما كتحسب بورت مفلتر ولا جهاز طافي. قبل الفحص، hostcensus كيرفع الحد المرن (soft limit) للملفات المفتوحة ف اتجاه الحد الصارم باش يكفي `--concurrency` زائد 64 واصف؛ وإلا ما قدرش، فحص preflight ديال `open files` كيفشل و `scan` كيخرج بالكود 1 قبل ما يبعث أي ترافيك. اكتشاف Nmap كيستعمل مهلة 30 ثانية لكل جهاز. البريفيكس كيتعطى لـ nmap بصيغة CIDR، والمسح كيفشل بالكود 1 ملي nmap كيرجع عدد عناوين قل من اللي تعطاتو (مثلاً اسم ما قدرش يحلو) ف بلاصة ما يعلّم الأجهزة كأنها طافية. الهدف اللي كيكون hostname كيتحل مرة وحدة وكتتعطى هاد العنوان لـ nmap، باش الاكتشاف والفحوصات يوصلو لنفس الجهاز. البريفيكس الكامل كيكون عملية nmap وحدة بمهلة فرعية ديال 35 ثانية لكل 256 عنوان، مقربة للأعلى. عمليات المسح اللي فيها استثناءات كتستعمل دفعات ديال 256 جهاز ومهلة 35 ثانية لكل دفعة. إنشاء العمال محدود بشكل مستقل على حجم النطاق. Reverse DNS وحل أسماء المضيفين عندهم مهلة منفصلة ديال جوج ثواني؛ الاستعلام اللي ما كيرجعش كيتخلّى عليه ف الخيط (thread) ديالو، باش ما يقدرش يخلي hostcensus خدام فوق هاد الحدود. بحد أقصى 16 استعلام كيخدمو ف نفس الوقت، والاستعلام المتروك كيبقى شاد بلاصتو حتى يرجع، باش عدد الخيوط المعلقة يبقى محدود؛ وإلا تعلّقو بـ 16 كاملين، الاستعلامات اللي جاية من بعد كتتسنى بلاصة خاوية خارج مهلة الجوج ثواني (اللي كتبدا غير ملي كتخوى شي بلاصة) حتى يوقف `--deadline` السكان. `NetworkScanner` ملي كيتستعمل كمكتبة بلا `deadline` يقدر يتسنى بلاصة خاوية بلا نهاية. و `--deadline` (الافتراضي ساعة وحدة) كيحدّد التشغيل كامل فوق هاد الحدود كلها.

### إعداد الخدمات

تقدر تبدل الخدمات بملف TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` كيكون واحد من `tcp` ولا `ssh` ولا `mysql` ولا `http` ولا `https` ولا `snmp`، وكيرجع افتراضياً لاسم الخدمة إلا كان داك الاسم نوع فحص، وإلا كيولي `tcp`. غير `snmp` بوحدو اللي كيستعمل UDP. أسماء الخدمات كتكون حروف صغيرة، أرقام، `-` و `_`. ما يمكنش لجوج خدمات يتشاركو نفس البورت والبروتوكول؛ حيت التاريخ كيسجّل حالة وحدة لهاد الثنائي. `timeout` اختياري، بالثواني، وعلى الأقل 0.05. فحوصات الاتصال (`tcp`، `ssh`، `mysql`، `http`) كتستعمل افتراضياً 0.3 ثانية. `snmp` و `https` كيستعملو `--timeout` ديال السكان ملي الخدمة ما كتحددش `timeout`. و `--timeout` ما كيبدّلش المهلة اللي ديجا محددة ف الخدمة.

تقارير JSON هي وثائق مرقّمة بالإصدار (`"format": "hostcensus-report"`، `"version": 1`) كتسجّل الهدف والخدمات المفحوصة والإعدادات حدا `devices`؛ و `--format json` بلا `-o` كيكتب التقرير ف stdout ف بلاصة الجدول. كل مخرج JSON عندو مخطط منشور؛ شوف [مخرجات JSON](../../../docs/json-output.md). الأجهزة كتحافظ على الحقول الأصلية `ip` و `alive` و `ssh` و `snmp` و `mysql` و `hostname` و `errors` وكتزيد لائحة `services` فيها لكل فحص `name` و `port` و `protocol` و `state` (`open`، `closed`، `filtered`، ولا `unknown` ملي الفحص فشل محلياً ولا وصل لمهلتو)، و `version` و `details`. مخرجات CSV كتزيد ف اللخر عمودي `services` و `versions` للخدمات المحلولة. القيم المنطقية `ssh` و `snmp` و `mysql` كتتبع الخدمات اللي عندها بالضبط هاد الأسماء.


## بروفايلات الجرد، الفحص المسبق (preflight)، والتاريخ المحلي

البروفايلات المسمية كتشارك نفس ملف TOML مع تعريفات `[services]` الموجودة. نسخ
[hostcensus.example.toml](../../../hostcensus.example.toml) لـ `hostcensus.toml` وحدد الشبكات
اللي كتسيّرها:

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

الأمر `preflight` كيحدد الخيارات والبروفايلات بنفس الطريقة اللي كيديرها `scan` بالضبط، بما فيها `--concurrency` لفحص الملفات المفتوحة، يعني إلا داز preflight بنجاح، فراه `scan` غادي يبدا بنفس الخطة.

البروفايلات كتقبل `network` و `exclusions` و `services` و `ports` و `backend` و `timeout` و `concurrency` و `max_hosts`. الحقول `services` و `ports` كتستعمل نفس صيغة اللوائح المفصولة بفواصل. خيارات CLI الصريحة كتغلب إعدادات البروفايل؛ وخيارات `--exclude` المتكررة كتتزاد على استثناءات البروفايل. الشبكة الصريحة مع `--profile` خاصها تكون داخلة ف نطاق IP/CIDR ديال داك البروفايل. أسماء المضيفين كتبقى مدعومة للسكان المباشر، ولكن ما يمكنش تتجمع مع استثناءات IP. حدود الأجهزة كتطبق قبل الاستثناءات؛ والسقف الكلي للفحوصات كيبقى يتطبق من بعد. الأجهزة المستثناة كتحيّد من فحوصات الخدمات ومن اكتشاف Nmap الاختياري بجوج.

كل سكان كيدير فحوصات preflight محلية قبل ما يبعث أي ترافيك للأهداف: حدود الأهداف والفحوصات، صلاحية الوصول لمسارات الإخراج، توفر البرنامج التنفيذي ولا الغلاف ديال Nmap (إلا كان مطلوب)، بنية قاعدة بيانات التاريخ، وحزمة TLS CA المكونفيغورية. `preflight` كيعرض مخرجات JSON وما كيديرش سكان للأهداف وما كينشئش قاعدة بيانات تاريخ. كيكتب مؤقتاً ملف مجاور باش يجرب صلاحية الوصول لمسار الإخراج بلا ما يبدّل المحتوى اللي كاين. الباكاند الافتراضي asyncio كيبقى ما كيحتاج لا Nmap لا root. مسارات الإخراج خاصها تكون مختلفة على بعضياتها وعلى ملف إعدادات الإدخال، بما فيها الروابط الصلبة (hard links)؛ والروابط الرمزية (symlinks) ف مسارات الإخراج كترفض. الفحوصات الفاشلة كترجع 1؛ والنطاق ولا الإعدادات اللي ما صالحاش كترجع 2.

كتابة التقارير وملفات التصدير كتحتاج دعم `O_NOFOLLOW`. ف الأنظمة اللي ما فيهاش هاد الدعم، بما فيها Windows، هاد الكتابات كتفشل بلا ما تفتح ولا تفرّغ الملف الهدف. التقارير الجديدة وسكريبتات التصدير كتتكتب بصلاحيات المالك بوحدو (وضع 0600)؛ وتبديل ملف موجود كيحافظ على الصلاحيات ديالو. الكتابة لـ named pipe ما فيه حتى قارئ كتفشل ديك الساعة ف بلاصة ما تبقى تتسنى. قاعدة بيانات `--history` الجديدة حتى هي كتتنشأ للمالك بوحدو؛ والقاعدة اللي ديجا كاينة كتحافظ على الوضع ديالها. رسائل السجل ديما كتمشي لـ stderr، باش stdout يبقى فيه غير النتائج. وملفات التصدير اللي فيها اعتمادات ديما كتفرض الوضع 0600.

التاريخ اختياري وكيكمّل لقطات JSON اللي ديجا كاينة والأمر `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

استعمل المعرفات (IDs) من `history`؛ المثال كيفترض قاعدة بيانات جديدة. اللقطات كتتخزن بمعاملات (transactionally) مع أوقات البداية والنهاية بـ UTC، إصدار الحزمة، الإعدادات الفعلية اللي ماشي سرية، الملخصات، وجميع ملاحظات الأجهزة والخدمات، بما فيها الأخطاء ديال كل جهاز. الملاحظات الناقصة ديال الأجهزة كيتحافظ عليها. عمليات التشغيل الملغاة ما كتتسجلش. وعقود أكواد الخروج الحالية ديال التقرير واللقطة والتصدير والسكان كتبقى محفوظة.

الأمر `history` كيعرض ملخصات JSON بلا ما يقرا جميع بيانات الأجهزة التاريخية.
أما `compare` فكيقرا جوج سكانات مسجّلين، وكيشرط نفس هويات الأهداف ونفس البورتات المختارة، وكيعطيك تغييرات الاستجابة والحالة وحالة البورتات. معرف السكان الأقدم خاصو يكون قبل المعرف الأحدث. ملي كيكونو السكانين بجوج سجلو `timeout` ولا `backend` وكانت القيم مختلفة، التقرير كيذكر تحذير وكيكمل المقارنة ديال الملاحظات. وقت انتظار مختلف يقدر يخلي بورت مفلتر يبان بحال محلول. أخطاء السكان وملاحظات البورتات المجهولة كيتعلمو بأنهم ما مأكدّينش ف بلاصة ما يتعاملو بحال اختفاء ولا إغلاق مؤكد: الأجهزة اللي فيها أخطاء كتبان ف `uncertain_hosts`، وكل انتقال بورت كيدخل فيه `unknown` (بما فيها unknown ف السكانين بجوج) كيتسجّل ف `unconfirmed_ports` ف بلاصة `port_changes`، من غير البورت اللي محلول ف السكان الأحدث، واللي كيتحسب تغيير بورت. `compare` و `diff` كيصنّفو البورتات بنفس القاعدة.
`no_longer_responding` كتعني غياب الجواب، ماشي دليل على أن الجهاز تحيّد.
كود الخروج 0 ديال السكان ما كيضمنش أن كل جهاز جاوب: شوف الأخطاء ديال كل جهاز. نجاح المقارنة كيرجع 0 سواء كانو تغييرات ولا لا؛ بينما `diff` ديال الملفات كيحافظ على عقد كود الخروج 3. والتاريخ غير المدعوم ولا الخاسر كيرجع 1.

التاريخ كيخزن معلومات ديال الجرد، يعني اختار مجلد محلي محمي مزيان. ملفات البروفايلات والإعدادات المخزّنة ما فيهاش اعتمادات SNMP؛ التعامل مع الاعتمادات كيبقى عبر خيارات وقت التشغيل ومتغيرات البيئة الحالية.

## مقارنة الجرد (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

اللقطة هي ملف JSON فيه `format: "hostcensus-snapshot"`، و `version: 1`، وإصدار hostcensus، ووقت الإنشاء بـ UTC، والهدف، و `timeout` و `backend` ديال السكان إلا كان السكان سجّلهم، والخدمات اللي تفحصات، والأجهزة الحية بنفس الشكل ديال تقرير `-o`. الأجهزة الطافية ما كتكونش فيه. الأمر `diff` كيقبل حتى تقارير `scan -o` العادية ديال JSON، بما فيها اللي من قبل ما يكون حقل `services`.

الأمر `diff` كيعطيك الأجهزة الجديدة والمختفية، البورتات اللي تحلات ولا تسدات ف الأجهزة اللي كاينة ف السكانين بجوج، والخدمات اللي تبدّل فيها `version`. البورتات اللي تفحصات غير ف سكان واحد من الجوج ما كتتقارنش، وكيخرج تحذير كيعلمك بهادشي. الملاحظات الفاشلة عمرها ما كتتقرا كـ "ما كاين حتى تغيير": البورت اللي كيكون `unknown` ف شي واحد من السكانين وماشي محلول ف السكان الأحدث كيتسجّل تحت `unconfirmed`، ماشي `closed`، بقيمة `before` كتكون `open` ولا `unknown` ولا `not-open` (تفحص وتلقى مسدود ولا مفلتر) وقيمة `after` كتكون `unknown` ولا `not-open`؛ أما البورت اللي محلول دابا فكيتسجّل تحت `opened` واخا يكون الفحص القديم فشل. الجهاز اللي فحوصاتو كلها فشلات بلا جواب ف أي من السكانين كيتسجّل تحت `unsettled_hosts` (بـ `before`/`after` قيمتها `up` ولا `uncertain` ولا `absent`، بما فيها إلا فشل ف السكانين بجوج ولا كان غايب من الملف الآخر) ف بلاصة `vanished_hosts`؛ وإلا جاوب ف السكان الأحدث فكيتسجّل حتى كجهاز جديد مع البورتات المحلولة ديالو. اللقطات كتحافظ على هاد الأجهزة الفاشلة على ود هاد السبب. كيبان حتى تحذير ملي الأهداف كتختلف، وملي الملفين بجوج سجلو timeout ولا backend وكانت القيم مختلفة. و `-o PATH` كيكتب صيغة JSON ف ملف حتى هي.

التقرير اللي جاي من سكان توقف بسبب `--deadline` (`"complete": false`) كيكون فيه غير الأجهزة اللي وصل ليها، داكشي علاش `diff` و `export` كيرفضوه بكود الخروج 2. الخيار `--allow-partial` كيقبلو مع تحذير ف stderr: ديك الساعة `diff` كيدير الأجهزة اللي السكان الناقص ما ذكرهاش كاع تحت `unsettled_hosts` كـ `unscanned` ف بلاصة مختفية (والجهاز اللي سجّلو طافي كيبقى مختفي)، وكيرد `partial` تساوي true وعمره ما كيقول ما كاين حتى تغيير، أما `export` فكيكتب تحذير ف راس السكريبت.

أكواد الخروج ديال `diff`: الكود `0` ما كاين حتى تغيير، الكود `3` تلقاو تغييرات ولا ملاحظات ما قدراتش تتأكد ولا مدخلات ناقصة (`changed` كتكون true فوقاش ما كانت أي لائحة، بما فيها `unsettled_hosts` و `unconfirmed`، ما خاوياش، ولا كانت `partial` تساوي true)، الكود `2` ملف ناقص ولا ما كيتقراش ولا ماشي لقطة مدعومة ولا ناقص بلا `--allow-partial`، الكود `1` ما قدرش يكتب ملف `-o`.

## التصدير لـ Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (تفريعة من Cacti 1.2.31) ما عندوش استيراد جماعي للأجهزة من ملف. الطريقة المدعومة باش تزيد الأجهزة من سكريبت هي `cli/add_device.php`، جهاز واحد ف كل استدعاء، بمعاملات `--option=value`. الأمر `hostcensus export` كيكتب سكريبت POSIX `sh` فيه هاد الاستدعاءات:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

كل جهاز حي كيولي `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- الأجهزة اللي نجح فيها استعلام SNMP ديال السكان كتاخد `--version=2 --community=...` ولا `--version=3 --username=... --authproto=... --password=...` (زائد `--privproto`/`--privpass` على ود authPriv)، و `--port` و `--avail=snmp`. تصدير SNMPv3 كيحتاج `--snmp-user`، و noAuthNoPriv كيترفض حيت `add_device.php` كيطلب كلمة مرور v3.
- الأجهزة الأخرى كتاخد `--version=0 --avail=ping`، مع `--ping_method=tcp --ping_port=` لأول بورت TCP محلول، ولا ICMP إلا ما كان حتى واحد.
- `--notes` كيعرض الخدمات المحلولة والإصدارات ديالها. و `--description` كيكون اسم reverse-DNS إلا كان بسيط (حروف، أرقام، `.`، `_`، `-`)، وإلا كيكون الـ IP، وكيتصاوب باش يكون فريد، حيت `add_device.php` كيتعامل مع الوصف اللي ديجا كاين على أنو تحديث لذاك الجهاز.

كل قيمة كيتحقق منها وكتتحمى بالاقتباس ديال الشيل بـ `shlex.quote`. بشكل افتراضي ما كيتكتب حتى سر SNMP: السكريبت كيقرا `HOSTCENSUS_SNMP_COMMUNITY` ولا `HOSTCENSUS_SNMP_AUTH_KEY` ولا `HOSTCENSUS_SNMP_PRIV_KEY` وقت التشغيل وكيوقف إلا كان شي واحد منهم ما مضبوطش. الخيار `--include-credentials` كيكتب القيم من متغيرات البيئة هادي داخل السكريبت ف بلاصة داكشي، كينشئو بالوضع 0600، وكيسجّل تحذير. `add_device.php` براسو كيطبع community وكيستقبل الأسرار كمعاملات، واللي كتكون باينة ف لائحة العمليات ديال سيرفر Kadupul ملي كل استدعاء كيكون خدام.

`add_device.php` كيخرج بالكود 1 ف حالة التكرار والأخطاء؛ السكريبت كيكمّل، كيحسب حالات الفشل، وكيخرج بالكود 1 إلا كان شي جهاز ما تزادش. معرفات القوالب كتجي من `php cli/add_device.php --list-host-templates`. أكواد الخروج ديال `export`: الكود `0` تكتب بنجاح، الكود `2` مدخلات ما كتتقراش ولا سكان ناقص بلا `--allow-partial` ولا بيانات ما يمكنش تتصدّر بأمان، الكود `1` ما قدرش يكتب السكريبت.

## الترقيم وطريقة الإطلاق

hostcensus كيتبع [Semantic Versioning](https://semver.org/spec/v2.0.0.html): الإصلاحات المتوافقة كتزيد ف رقم التصحيح (patch)، الميزات المتوافقة والإشعارات بالإلغاء التدريجي كتزيد ف الرقم الفرعي (minor)، والتغييرات اللي كتكسّر التوافق كتزيد ف الرقم الرئيسي (major). الأوامر والخيارات وأكواد الخروج ومخططات JSON هي العقد العام؛ والسلوك اللي معلن باللي غادي يتحيّد كيبقى خدام حتى للإصدار الرئيسي الجاي، إلا إلا احتاج شي إصلاح أمني يبدّلو قبل (وديك الساعة سجل التغييرات كيشرح علاش).

أداة release-please كتفتح PR ديال الإطلاق من عناوين Conventional Commit على `main`، وكتحدث `pyproject.toml` و `uv.lock` و `CHANGES.md`. ملي كيتدمج، كيتنشأ التاغ `vMAJOR.MINOR.PATCH` ومسودة إصدار على GitHub، والـ CI كيرفق ليها حزمة wheel مختبرة وتوزيعة المصدر ومجاميع التحقق (checksums)؛ و GitHub كيخزّن شهادات إثبات البناء (build attestations) ديال هاد الملفات عبر واجهة attestations API. المشرف كيراجع المسودة وكينشرها غير ملي كيتّرفقو الملفات. الإصدارات ما عمرها كتتبدل من بعد النشر.

النشر الموثوق على PyPI (trusted publishing) اختياري وكيحتاج ملكية المشروع، وناشر موثوق (trusted publisher)، وبيئة `pypi`. كينشر نفس حزم الإطلاق المتحقّق منها بلا ما يعاود البناء ولا يخزن رمز API. الإصدارات اللي عليها تاغ ف هاد المستودع العمومي كتولّد شهادات إثبات الحزم ديال GitHub؛ أما التفريعات الخاصة فكتحتاج خطة مدعومة وتفعيل صريح. شوف [دليل الإطلاق الكامل](../../../docs/releasing.md) على ود الإعداد والأوامر المضبوطة وإعادة المحاولة.

## التطوير

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

أدوات التطوير كاينة ف مجموعات اعتماديات [PEP 735](https://peps.python.org/pep-0735/) ف ملف `pyproject.toml` (`dev`، `fuzz`، `build`)، داكشي علاش عمرها ما كتبان ف البيانات الوصفية ديال الحزمة المنشورة. `uv.lock` هو ملف القفل الوحيد؛ والـ CI كيثبّت بالأمر `uv sync --locked` وكيفشل إلا كان ملف القفل قديم. اختار المفسّر بـ `uv python`، ولا mise (`mise exec python@3.14 -- uv sync --locked`)، ولا أي Python 3.12+.

الـ CI كيفرض حد أدنى ديال 90% لتغطية الاختبارات ف الحزمة. اختبارات الوحدة فيها سيرفرات loopback مضبوطة وحالات اختبار بلا إنترنت ديال البروفايلات والتاريخ ومدقق الإطلاق؛ ومختبر Compose كيشغّل OpenSSH و MariaDB و nginx و net-snmp على جسر معزول. شغّلو بالأمر `make test-integration`. شوف [CONTRIBUTING.md](../../../CONTRIBUTING.md) و[أدوات الإطلاق](../../../scripts/README.md).

حاوية التشغيل كتخدم بـ UID/GID 10001 بلا مجلد home وبلا دخول شيل وبلا pip، وتقدر تكتب ف `/app/output`. عطي لهاد المستخدم صلاحية الكتابة على أي مجلد إخراج مركّب (mounted). ما كتحتاج حتى امتيازات (capabilities) وكتخدم مع نظام ملفات جذر للقراءة فقط، يعني تقدر تشغّلها بحال هاكا:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap كيستعمل سلوك اكتشاف TCP غير المميز ف هاد الحاوية. والـ CI كيفشل بناء الصورة على أي ثغرة HIGH ولا CRITICAL قابلة للإصلاح كيبلغ عليها Trivy.

## فحوصات سلسلة التوريد

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
كيخدم على main وكل سيمانة، كينشر النقطة الحقيقية ديالو، وكيرفع النتائج لـ GitHub code scanning. الإجراءات (Actions) وصور الحاويات الأساسية مثبتة بهاشات غير قابلة للتغيير؛ واعتماديات Python محلولة ف `uv.lock`. أخطاء Bandit كتفشّل CI، واختبارات التعمية المحدودة بـ Atheris كتختبر محللات SSH و MySQL و HTTP والشهادات و SNMPv3 BER بلا اتصال بالشبكة.

Scorecard كيقيس حتى نشاط المراجعة التاريخي، تنوّع المساهمين، ومصدر الإطلاقات (provenance). هاد النقط كتعكس أدلة فعلية؛ وماشي ادعاء باللي كل فحص حوكمة ولا إطلاق تاريخي محقق. شوف [SECURITY.md](../../../SECURITY.md) و[مصدر الإطلاقات](../../../docs/releasing.md).

## التعريب واللغات

رسائل سطر الأوامر وجداول الملخص والمقارنة ف التيرمينال كتدعم 45 لغة ومحلية (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) بلا حتى اعتمادية تشغيل زايدة. اختيار اللغة كيحترم `--lang`، ومن بعد `LC_ALL` و `LC_MESSAGES` و `LANG`، وكيرجع لـ `en` كخيار افتراضي. مخططات JSON وأعمدة CSV وسكريبتات التصدير كتبقى نفسها وما كتتبدلش ف جميع اللغات.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## المساهمة

المساهمات خاصها يكون فيها مثال قابل لإعادة الإنتاج، وتحافظ على عقود سطر الأوامر وصيغ البيانات الموثّقة، وتدوز فحوصات الجودة اللي الفوق. شوف [CONTRIBUTING.md](../../../CONTRIBUTING.md) على ود طريقة عمل التطوير، و[دليل الإطلاق](../../../docs/releasing.md) على ود قرارات التوافق والترقيم.

## الأمان وحالة الرخصة

شوف [SECURITY.md](../../../SECURITY.md) على ود التبليغ الخاص والإصدارات المدعومة.
hostcensus مرخّص تحت [رخصة MIT](../../../LICENSE).

ترويسات ملفات المصدر كتستعمل معرفات SPDX وكتحافظ على حقوق المساهمين من تاريخ Git. شوف [AUTHORS.md](../../../AUTHORS.md) على ود الإسناد. ملفات التقاط الاختبارات الثنائية وملف القفل المولّد كيستعملو ملفات `.license` مجاورة؛ ونص رخصة MIT كاين ف `LICENSES/MIT.txt`.
