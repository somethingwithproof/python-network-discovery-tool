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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · **العربية (مصر)** · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus هي أداة CLI مكتوبة بـ Python عشان تعمل جرد متكرر للخدمات على الشبكات اللي بتديرها.
الأداة بتسجل الأجهزة فاتحة إيه، وبتقارن الملاحظات دي مع الوقت، وبتطلعلك سكريبتات استيراد لـ Kadupul. الـ backend الافتراضي بيستخدم asyncio sockets من غير صلاحيات root، وكمان فيه اكتشاف اختياري بـ Nmap يقدر يتعرف على الأجهزة حتى برا بورتات الخدمات اللي متظبطة.

## ليه hostcensus

تقرير البورتات اللي بيتعمل مرة واحدة مش بيوضحلك هل النتيجة الجديدة فعلا اتغيرت ولا الفحص بس فشل. hostcensus بتجمع بين حالات واضحة للخدمات، وفحوصات محدودة بوقت وعدد، وبروفايلات فحص تقدر تعيد استخدامها، وسجل محلي. المشغلين يقدروا يعيدوا نفس النطاق تاني، ويفحصوا الأخطاء، ويفرقوا بين الملاحظات اللي مش متأكدين منها والتغييرات المؤكدة.

- **أدلة الخدمات:** تعريف SSH، وتحيات MySQL، وهيدرز HTTP، وملاحظات شهادات TLS، واكتشاف SNMP أو استعلامات system-MIB ببيانات دخول.
- **نطاق قابل للتكرار:** بروفايلات TOML بأسماء، واستثناءات تقدر تزود عليها، وخدمات قابلة للتعديل، وحدود لعدد الأجهزة والفحوصات، وعمال (workers) بعدد محدود.
- **فحوصات قبل ما يطلع أي ترافيك:** فحص preflight محلي بيتأكد من الأهداف والأدوات وصلاحية الوصول لمسارات الحفظ ومخطط السجل وملفات TLS CA اللي متظبطة.
- **سجل الجرد:** لقطات SQLite بتتحفظ بـ transactions وبتحتفظ بكل الملاحظات، والمقارنات بتخلي أخطاء الفحص والحالات المجهولة باينة قدامك.
- **مخرجات متوافقة مع أدوات تانية:** تقارير على الـ terminal وبصيغ JSON و CSV، ولقطات ملفات بإصدارات محددة، وسكريبتات استيراد لـ Kadupul.

الـ CI بيغطي Python 3.12 و 3.13 و 3.14 على Linux و macOS، ده غير معمل تكامل مضبوط بـ Compose. الكود بيستخدم type aliases حديثة، ونتائج preflight بأنواع محددة، وبروفايلات keyword-only slotted، وتنظيف async منظم مع الحفاظ على دعم نفس نسخ التشغيل دي. شوف [الإصدارات وطريقة النشر](../../../docs/releasing.md) عشان تعرف اتفاقية التوافق لـ SemVer وخطوات النشر على GitHub. شارة الإصدار بتوصف الملفات المنشورة مش النسخة الحالية من الكود: آخر تاج منشور دلوقتي هو `v0.3.0`، بينما النسخة دي من الكود بتستخدم رقم إصدار الحزمة `3.0.0`. ثبت الأداة من النسخة دي عشان تستخدم مميزات الجرد اللي مشروحة هنا.

ابدأ بـ [التثبيت](#install)، وبعدين شوف [البروفايلات والسجل](#inventory-profiles-preflight-and-local-history).
وللتفاصيل بتاعة التكامل، شوف [بصمات الخدمات](#fingerprints)،
و[مقارنة الملفات](#inventory-diff)، و[التصدير لـ Kadupul](#kadupul-export).

<a name="install"></a>

## التثبيت

محتاج Python 3.12 أو أحدث؛ النسخ المختبرة هي من Python 3.12 لحد 3.14. من نسخة الكود دي، ثبت الاعتماديات المقفولة للتشغيل:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

عشان تستخدم اكتشاف الأجهزة الاختياري بـ Nmap، ثبت برنامج Nmap من مدير الحزم بتاع نظامك؛ مش محتاج أي حزمة Python زيادة. مخرجات XML بتاعة Nmap بتتقرأ بـ defusedxml، ودي اعتمادية أساسية، فبيتم رفض entity expansion. أداة hostcensus بتشغل `nmap` اللي موجود في `PATH` مباشرة بقائمة بارامترات ثابتة، ومهلة زمنية بتكبر مع حجم الـ prefix، وحد أقصى للمخرجات 64 MiB. مش هتحتاج Nmap مع الـ backend الافتراضي.

## التحويل من netprobe

hostcensus هو الاسم الجديد لـ netprobe، ونزل في الإصدار 3.0.0. المشروع عمره ما اتنشر على PyPI بأي اسم من الاتنين، فالتثبيت كان دايما من نسخة الكود أو من إصدار على GitHub. مستودع GitHub لسه محتفظ بنفس اسمه.

| كان | دلوقتي | التوافق |
| --- | --- | --- |
| الحزمة `netprobe` | `hostcensus` | عيد التثبيت من نسخة الكود؛ مفيش حزمة بالاسم القديم. |
| أمر `netprobe` | `hostcensus` | `netprobe` لسه شغال وبيطبع سطر تحذير واحد على stderr إنه قديم وهيتلغي. أكواد الخروج و stdout زي ما هم. هيتشال في الإصدار الرئيسي اللي جاي. |
| متغيرات البيئة `NETPROBE_*` | `HOSTCENSUS_*` | متغير `NETPROBE_*` بيشتغل لو المتغير المقابل ليه في `HOSTCENSUS_*` مش متظبط، مع تحذير واحد على stderr بيذكر أسماء المتغيرات بس ومش بيطبع قيمها أبدا. `HOSTCENSUS_*` بيكسب لو الاتنين موجودين. هيتشال في الإصدار الرئيسي اللي جاي. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **تغيير جذري (Breaking).** مفيش طبقة توافق للاستيراد؛ لازم تحدث أوامر الـ import. |
| تاج صورة Docker اسمه `network-discovery:test` (للـ CI بس) ومستخدم الكونتينر `netprobe` | `hostcensus:test`، المستخدم `hostcensus` | عمره ما اتنشر image على أي registry. ابني الصورة من جديد واستخدم `hostcensus` كـ entrypoint. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | لو فيه ملف موجود بالاسم الافتراضي القديم هيفضل شغال مع تحذير، طول ما الاسم الجديد مش موجود. المسارات الصريحة اللي بتتحدد بـ `--config` و `--history` مش بتتأثر. |
| التقارير واللقطات اللي فيها `"format": "netprobe-report"` أو `"netprobe-snapshot"`، وحقل `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | أمري `diff` و `export` لسه بيقروا الملفات المكتوبة بالاسم القديم، ومخططات JSON Schemas المنشورة بتقبل الكتابتين. الملفات الجديدة بتستخدم الأسماء الجديدة. قواعد بيانات سجل SQLite ما اتغيرتش وبتفتح زي زمان. |
| سكريبتات Kadupul من `netprobe export` | سكريبتات من `hostcensus export` | السكريبتات القديمة لسه شغالة وبتقرأ `NETPROBE_SNMP_*` لما بتشتغل. السكريبتات الجديدة بتقرأ `HOSTCENSUS_SNMP_*`. |

## مثال سريع

اتشغل من كونتينر الاختبار في معمل التكامل المشروح تحت قسم التطوير؛ والمخرجات مختصرة:

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
| `scan` | الملاحظات والتقرير اتسجلوا | فشل في preflight أو الـ backend أو السجل أو كتابة التقرير أو اللقطة | هدف أو خيارات أو إعدادات أو حدود غلط | - | وصل لـ `--deadline`؛ اتكتب تقرير جزئي وتجاهل حفظ السجل واللقطة |
| `preflight` | الفحوصات نجحت | فحص محلي فشل | هدف أو إعدادات غلط أو تعارض في مسارات الحفظ | - | - |
| `profiles` | تم عرض البروفايلات السليمة | - | إعدادات أو اختيار مش مقري أو غلط | - | - |
| `history` | تم عرض الملخصات | السجل مش موجود أو بايظ أو مش مدعوم | خيارات CLI غلط | - | - |
| `compare` | طلعت المقارنة حتى لو فيه تغييرات | السجل مش مقري أو النطاق والترتيب مش متوافقين أو فشل في الكتابة | خيارات CLI غلط | - | - |
| `diff` | مفيش تغييرات | ما قدرش يكتب ملف `-o` | ملف ناقص أو مش مقري أو مش مدعوم أو فحص ناقص من غير `--allow-partial` | لقى تغييرات أو ملاحظات غير مؤكدة أو فحص ناقص | - |
| `export` | السكريبت اتكتب | ما قدرش يكتب السكريبت | ملف مش مقري أو فحص ناقص من غير `--allow-partial` أو بيانات ما ينفعش تتصدر بأمان | - | - |

## تقسيمة المشروع

| الوحدة (Module) | المسؤولية |
| --- | --- |
| `cli.py` | خيارات الأوامر، وتجهيز البروفايلات، و preflight، والفحص، وكتابة التقارير |
| `scanner.py`, `probes.py` | توسيع الأهداف، والعمال المحدودين، واكتشاف الأجهزة وملاحظات الخدمات |
| `config.py`, `profiles.py` | تعريفات الخدمات وبروفايلات الجرد المتحققة |
| `models.py`, `output.py` | أنواع النتائج وعرض الـ terminal و JSON و CSV |
| `history.py`, `diff.py` | سجل SQLite ومقارنات ملفات اللقطات اللي ليها إصدارات |
| `preflight.py` | الفحوصات المحلية والتحقق المحدود من نسخة Nmap |
| `export.py` | سكريبتات استيراد Kadupul المتحققة والمقتبسة بأمان |

كل ملاحظة لخدمة بتسجل حالتها لوحدها بعيد عن الهوية اللي الخدمة بتعلن عنها.
عمليات القراءة والمُهل الزمنية محدودة؛ وأخطاء الفحص بتفضل في أخطاء الجهاز. سجل SQLite
بيستخدم transactions وتنظيف صريح للاتصالات ومسارات للقراءة بس للعرض والمقارنة.
أسرار SNMP بتدخل بس عن طريق متغيرات البيئة أو ملفات الأسرار؛ وسجل الجرد بيحفظ
الإعدادات الفعلية اللي مفيهاش أسرار. شوف
[البنية المعمارية](../../../docs/architecture.md) عشان تعرف خطوات الفحص وحدوده وحدود الثقة،
وشوف [SECURITY.md](../../../SECURITY.md#authorized-use) للاستخدام المصرح بيه.


## طريقة الاستخدام

افحص بس الشبكات اللي إنت بتديرها.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| الخيار | المعنى |
| --- | --- |
| `NETWORK` | CIDR أو IP أو hostname؛ اختياري مع `--profile`. معرفات نطاق IPv6 بتترفض. |
| `-o, --output PATH` | بيكتب تقرير. الصيغة بتمشي على الامتداد (`.json`، `.csv`)؛ أي امتداد تاني بيرجع لـ JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | بيجبر صيغة التقرير. مالوش تأثير من غير `--output`. الامتداد `.sh` بيختار `kadupul`. |
| `-v, --verbose` | تسجيل تفصيلي للـ debug. |
| `-q, --quiet` | بيخفي النتائج وشريط التقدم والرسائل العادية؛ التحذيرات والأخطاء لسه بتظهر على stderr. |
| `--backend asyncio\|nmap` | اكتشاف الأجهزة. `asyncio` (الافتراضي) بيفحص بورتات الخدمات مباشرة؛ `nmap` بيعمل ping sweep بـ nmap الأول وبيحتاج برنامج `nmap` يكون في `PATH`. |
| `--timeout SECONDS` | وقت الانتظار للفحوصات اللي مش متحدد لها وقت خاص (الافتراضي 1.0). فحوصات الاتصال الجاهزة بتستخدم 0.3 ثانية إلا لو جدول الخدمة محدد `timeout`. |
| `--concurrency N` | عدد الفحوصات الشغالة في نفس الوقت (الافتراضي 256). |
| `--deadline SECONDS` | بيوقف الفحص كله، بما فيه فحص nmap، بعد الوقت ده (الافتراضي 3600، وأقصى حاجة 604800؛ متغير البيئة `HOSTCENSUS_DEADLINE`). الأجهزة اللي خلصت بتتكتب في التقرير مع `"complete": false`، ومفيش سجل أو لقطة بتتكتب، وأمر `scan` بيخرج بكود 4. |
| `--config PATH` | ملف TOML فيه تعريفات الخدمات وإعدادات `[profiles]` الاختيارية بالأسماء. |
| `--profile NAME` | بيستخدم بروفايل بالاسم؛ بيرجع تلقائيا لـ `hostcensus.toml` لما `--config` مش بيتكتب. |
| `--exclude IP/CIDR` | بيضيف استثناء؛ تقدر تكرره زي ما تحب. استثناء جهاز IPv4 بيستثني كمان عناوين IPv6 اللي بتوصله: IPv4-mapped (`::ffff:a.b.c.d`) و NAT64 (`64:ff9b::/96`) و 6to4. أهداف واستثناءات IPv4-mapped بتتعامل كأنها عناوين IPv4 اللي بتشير ليها. |
| `--max-hosts N` | حد العناوين اللي بيتفحص قبل الاستثناءات (الافتراضي والحد الأقصى الصارم 65,536). |
| `--history PATH` | بيسجل الفحص المكتمل في قاعدة بيانات SQLite اختيارية للسجل. |
| `--services NAMES` | قائمة أسماء الخدمات مفصولة بفاصلة عشان تتفحص بنفس الترتيب (الافتراضي: الكل). |
| `--ports SPEC` | قائمة مفصولة بفاصلة بالشكل `NAME=PORT` (عشان تنقل خدمة لبورت تاني) أو `PORT` (عشان تزود فحص TCP عادي اسمه `tcp-PORT`). |
| `--snmp-community-file PATH` | ملف فيه الـ SNMPv2c community لاستعلام system MIB. متغير البيئة: `HOSTCENSUS_SNMP_COMMUNITY` (القيمة) أو `HOSTCENSUS_SNMP_COMMUNITY_FILE` (المسار). |
| `--snmp-user` | مستخدم SNMPv3. متغير البيئة: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (الافتراضي), `SHA224`, `SHA256`, `SHA384`, `SHA512` وملف فيه كلمة السر. متغير البيئة: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` أو `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (الافتراضي), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` وملف فيه كلمة السر. متغير البيئة: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` أو `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | بيكتب كمان لقطة بإصدار محدد عشان تستخدمها مع `hostcensus diff`. |
| `--tls-ca-file PATH` | بيتأكد من شهادات HTTPS قدام ملف PEM ده بدل مخزن النظام. متغير البيئة: `HOSTCENSUS_TLS_CA_FILE`. |

بشكل افتراضي كل جهاز بيتفحص على SSH (TCP 22) و SNMP (UDP 161) و MySQL (TCP 3306) و HTTP (TCP 80) و HTTPS (TCP 443). بورتات TCP بتتجرب باتصال كامل. و SNMP بيتجرب بطلب اكتشاف محرك SNMPv3، واللي أي عميل SNMPv3 لازم يرد عليه من غير بيانات دخول؛ العملاء اللي بيتكلموا v1/v2c بس مش هتظهر في الفحص ده. مع الـ asyncio backend، الجهاز بيتحسب شغال لما أي فحص ياخد رد، حتى لو كان رفض اتصال، فالجهاز اللي بيسقط كل الفحوصات بياخد `alive=false` وخطأ "Host is down"؛ وده مش معناه بالضرورة إنه مطفي فعليا. ومع `--backend nmap`، برنامج nmap هو اللي بيقرر أنهي أجهزة شغالة (بـ ICMP لو شغال بـ root، وبـ TCP 80/443 غير كده).

<a name="fingerprints"></a>

### بصمات الخدمات (Fingerprints)

كل خدمة مفتوحة بيتاخد لها بصمة من اللي بتبعته قبل أي تسجيل دخول. مفيش حاجة بتعمل مصادقة غير استعلام SNMP، وده بس لما تديله بيانات دخول.

| الفحص | بيقرأ إيه | `version` | مفاتيح `details` |
| --- | --- | --- | --- |
| `ssh` | سطر تعريف RFC 4253 | البرنامج، زي `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | مصافحة البداية بتاعة MySQL/MariaDB | إصدار السيرفر | `server_version`, `flavor`, `auth_plugin`، أو `error_code`/`error` |
| `http` | رد `HEAD /` | هيدر `Server` | `status`, `server` |
| `https` | مصافحة TLS والشهادة و `HEAD /` | هيدر `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (بتوقيت UTC بصيغة ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | اكتشاف SNMPv3؛ وببيانات الدخول بيعمل GET لـ sysDescr و sysObjectID و sysName | sysDescr | `engine_id`؛ ومع بيانات الدخول `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`، أو `snmp_error` |

الهدف اللي مكتوب كـ hostname بيتحلل مرة واحدة لكل جهاز وكل فحص بيتصل بالعنوان ده، وبيتسجل في النتائج تحت `address`؛ والاسم نفسه بيستخدم بس لـ TLS SNI، والتحقق من الشهادة، وهيدر `Host` في HTTP. الاسم اللي ما بيتحللش بيدي حالات `unknown` وخطأ `Cannot resolve`. أسماء Reverse DNS بتفضل محفوظة بس لما تكون فيها حروف صالحة لأسماء المضيفين، وبحد أقصى 16 عملية بحث في نفس الوقت. HTTPS بيستخدم التحقق من الشهادة واسم المضيف قدام مخزن النظام أو `--tls-ca-file`. مخزن الثقة بيتحمل مرة واحدة للفحص كله وبيتكرر استخدامه لكل فحوصات HTTPS. اتصال TCP ومصافحة TLS بيتحسب وقتهم لوحدهم، فالبورت اللي بيقبل الاتصال بس بيقف في المصافحة بيبقى `open` ومعاه `tls_error` مش `filtered`. لو التحقق فشل، النتيجة بتسجل `cert_verified: false` و `cert_verify_error`؛ ومش بتجرب تاني بإعدادات أضعف ولا بتبعت طلب HTTP. تفاصيل الشهادة وهيدرز HTTP بتتجمع بس بعد ما التحقق ينجح. حط ملف CA الصح للخدمات اللي بتستخدم Private CA. التقارير القديمة ممكن يكون فيها `cert_read_unverified`، وده ما بقتش الفحوصات الحالية بتطلعه.

أسرار SNMP بتتقرأ بس من متغيرات البيئة أو من ملفات (`--snmp-*-file`، أو متغير `HOSTCENSUS_SNMP_*_FILE` المقابل ليه)، ومش بتتاخد أبدا كقيم من سطر الأوامر عشان المستخدمين التانيين على نفس الجهاز ممكن يشوفوها في قائمة العمليات. لو استخدمت `--snmp-community` أو `--snmp-auth-key` أو `--snmp-priv-key` بقيمة، البرنامج بيخرج بكود 2 وبيقولك البديل. ملف السر لازم يكون UTF-8 ومش فاضي وبحد أقصى 4096 بايت؛ سطر جديد واحد في الآخر بيتجاهله، ولو حطيت متغير بيئة وملف لنفس السر في نفس الوقت بيطلع خطأ. الأخطاء بتذكر اسم الملف بس عمرها ما بتطبع محتواه. تقارير الفحص والسجل مش بيتضمنوا قيم بيانات الدخول عن قصد. أداة التصدير ليها خيار منفصل وصريح اسمه `--include-credentials` مشروح تحت. الـ community بيختار SNMPv2c؛ والـ user بيختار SNMPv3، مع مصادقة لو حطيت auth key وتشفير لو حطيت المفتاحين سوا (و `snmp_security_level` بيسجل أنهي مستوى اشتغل). hostcensus بترفض بكود خروج 2 إنك تجمع بين community ومستخدم v3، أو تستخدم privacy key من غير auth key، أو تستخدم مفاتيح من غير مستخدم، وعمرها ما بتعيد استعلام v3 فاشل على v2c أو بمستوى أمان أقل. العملاء اللي بيتكلموا v1/v2c بس بيتجاهلوا اكتشاف v3 اللي من غير بيانات دخول، فبيظهروا مفتوحين بس لما تديلهم community.

نص البانر بيتنضف عشان يفضل فيه الحروف القابلة للطباعة بس، وبيقف عند حد 256 حرف قبل ما يتحفظ أو يتعرض. عمليات القراءة كمان محدودة: 4 KiB لكل سطر، و 4 KiB لتحية MySQL، و 16 KiB لهيدرز HTTP. معرف محرك SNMP اللي أطول من 32 بايت بيتقص قبل ما يتحفظ. HTTP و HTTPS بيبعتوا هيدر Host فيه عنوان IPv6 جوا أقواس مربعة ومعاه رقم البورت لو مش 80 أو 443. خلايا CSV اللي بتبدأ برمز معادلة في برامج الجداول بيتحط قبلها بادئة عشان تفضل نص عادي.

### الحدود والقيود

التشغيلة الواحدة بتقبل بحد أقصى 65,536 عنوان، و 64 خدمة، و 524,288 فحص (عدد الأجهزة مضروب في عدد الخدمات)؛ أي طلب أكبر من كده بيخرج بكود 2 قبل ما يبعت أي حاجة. خيار `--concurrency` حده الأقصى 4096 سوكيت. كل فحص ليه مهلة نهائية صارمة أربع أضعاف وقته المخصص. فحوصات الاتصال (`tcp`, `ssh`, `mysql`, `http`) بتستخدم 0.3 ثانية إلا لو الخدمة محددة `timeout`. أما SNMP و HTTPS فبيستخدموا `--timeout` (الافتراضي 1.0) لو مش محدد ليهم وقت. أي فحص يوصل للمهلة النهائية بيتسجل كـ `unknown` ومعاه "probe timed out" في `errors`. أخطاء السوكيت المحلية (زي إن الـ file descriptors تخلص) برضو بتتسجل كـ `unknown` مع الخطأ؛ وعمرها ما بتتحسب بورت متفلتر أو جهاز مطفي. قبل ما يبدأ الفحص، hostcensus بترفع الحد المرن للملفات المفتوحة ناحية الحد الأقصى عشان يكفي `--concurrency` زائد 64 descriptor؛ ولو ما قدرتش، فحص `open files` في الـ preflight بيفشل وأمر `scan` بيخرج بكود 1 قبل ما يبعت أي ترافيك. اكتشاف Nmap بيستخدم مهلة 30 ثانية لكل جهاز. الـ prefix بيتبعت لـ nmap بصيغة CIDR، والفحص بيفشل بكود خروج 1 لما nmap يرجع عناوين أقل من اللي اتبعتتله (مثلا اسم ما قدرش يحلله) بدل ما يعتبر الأجهزة مطفية. الهدف اللي هو hostname بيتحلل مرة واحدة وبيتديله العنوان لـ nmap، عشان الاكتشاف والفحوصات يوصلوا لنفس الجهاز. الـ prefix الكامل بيبقى عملية nmap واحدة مهلتها 35 ثانية لكل 256 عنوان مقربة لفوق. الفحوصات اللي فيها استثناءات بتشتغل في دفعات كل دفعة 256 جهاز وبمهلة 35 ثانية لكل دفعة. إنشاء العمال (workers) محدود ومش مرتبط بحجم النطاق. عمليات Reverse DNS وتحليل أسماء المضيفين ليها مهلة منفصلة ثانيتين؛ لو عملية تحليل ما رجعتش بتتساب على الـ thread بتاعها عشان ما تفضلش مشغلة hostcensus بعد الحدود دي. بحد أقصى 16 عملية تحليل شغالة في نفس الوقت، والعملية المتسابة بتفضل حاجزة مكانها لحد ما ترجع عشان عدد الـ threads المعلقة يفضل محدود؛ ولو الـ 16 كلهم علقوا، الطلبات اللي بعدها بتستنى دورها برا مهلة الثانيتين (اللي بتبدأ أول ما مكان يفضى) لحد ما `--deadline` يوقف الفحص. لو استخدمت `NetworkScanner` كمكتبة من غير `deadline` ممكن تستنى مكان فاضي إلى ما لا نهاية. خيار `--deadline` (الافتراضي ساعة واحدة) بيحكم وقت التشغيلة كلها فوق كل ده.

### إعداد الخدمات

تقدر تعدل الخدمات عن طريق ملف TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

قيمة `probe` بتكون واحدة من `tcp` أو `ssh` أو `mysql` أو `http` أو `https` أو `snmp` وبتاخد اسم الخدمة تلقائيا لو الاسم ده واحد من أنواع الفحص دي، وإلا بتبقى `tcp`. خدمة `snmp` بس هي اللي بتستخدم UDP. أسماء الخدمات بتبقى حروف صغيرة وأرقام و `-` و `_`. ما ينفعش خدمتين يتشاركوا نفس البورت والبروتوكول؛ السجل بيحفظ حالة واحدة للزوج ده. خيار `timeout` اختياري، بالثواني، وأقل قيمة 0.05. فحوصات الاتصال (`tcp`, `ssh`, `mysql`, `http`) الافتراضي بتاعها 0.3 ثانية. و `snmp` و `https` بيستخدموا `--timeout` بتاع الفحص لو الخدمة مش محددة `timeout`. خيار `--timeout` مش بيبدل وقت مخصص الخدمة أصلا محدداه.

تقارير JSON عبارة عن مستندات ليها إصدار (`"format": "hostcensus-report"`, `"version": 1`) بتسجل الهدف والخدمات اللي اتفحصت والإعدادات جنب `devices`؛ ولو كتبت `--format json` من غير `-o` التقرير بيتطبع على stdout بدل الجدول. كل مخرج JSON ليه مخطط (schema) منشور؛ شوف [مخرجات JSON](../../../docs/json-output.md). الأجهزة بتحتفظ بحقول `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` و `errors` الأصلية وبتزود قائمة `services` فيها لكل فحص `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`، أو `unknown` لو الفحص فشل محليا أو خلص وقته), `version` و `details`. ومخرجات CSV بيزيد عليها في الآخر عمودين `services` و `versions` للخدمات المفتوحة. قيم الـ boolean بتاعة `ssh`, `snmp` و `mysql` بتمشي ورا الخدمات اللي بنفس الأسماء دي بالظبط.


<a name="inventory-profiles-preflight-and-local-history"></a>

## بروفايلات الجرد، وفحص ما قبل التشغيل، والسجل المحلي

البروفايلات اللي بأسماء بتتشارك نفس ملف TOML مع تعريفات `[services]` الموجودة. انسخ
[hostcensus.example.toml](../../../hostcensus.example.toml) لملف `hostcensus.toml` وحط الشبكات
اللي بتديرها:

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

أمر `preflight` بيجهز الخيارات والبروفايلات بالظبط زي `scan`، بما في ذلك
`--concurrency` لفحص الملفات المفتوحة، يعني لو preflight نجح فـ `scan`
هيبدأ بنفس الخطة.

البروفايلات بتقبل `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, و `max_hosts`. خيارات `services` و `ports` بتستخدم نفس طريقة القائمة المفصولة بفاصلة.
خيارات CLI الصريحة بتلغي إعدادات البروفايل؛ وتكرار `--exclude` بيزود على استثناءات البروفايل.
لو كتبت شبكة صريحة مع `--profile` لازم تكون جوا نطاق IP/CIDR بتاع البروفايل ده.
أسماء المضيفين (Hostnames) لسه مدعومة للفحص المباشر، بس ما ينفعش تتجمع مع استثناءات IP.
حدود عدد الأجهزة بتتطبق قبل الاستثناءات؛ وحد إجمالي الفحوصات لسه بيتطبق بعدها.
الأجهزة المستثناة بتتشال من فحوصات الخدمات وكمان من اكتشاف Nmap الاختياري.

كل فحص بيعمل فحوصات preflight محلية قبل ما يبعت أي ترافيك للأهداف: حدود الأهداف والفحوصات،
وصلاحية الوصول لمسارات الحفظ، وتوفر برنامج أو wrapper لـ Nmap لو مستخدمه، ومخطط السجل،
وملف TLS CA لو متظبط. أمر `preflight` بيطلع تقرير JSON ومش بيفحص الأهداف ولا بيعمل
قاعدة بيانات للسجل. هو بيكتب ملف مؤقت جنبه عشان يجرب صلاحية الكتابة من غير ما يغير المحتوى الموجود.
الـ asyncio backend الافتراضي لسه مش محتاج لا Nmap ولا root. مسارات الحفظ لازم تكون مختلفة
عن بعضها وعن ملف الإعدادات اللي بتقرأ منه، بما فيها الـ hard links؛ والروابط الرمزية (symlinks)
لمسارات الحفظ بتترفض. الفحوصات الفاشلة بترجع 1؛ والنطاق أو الإعدادات الغلط بترجع 2.

كتابة التقارير وملفات التصدير بتحتاج دعم `O_NOFOLLOW`. على الأنظمة اللي مفيهاش ده،
زي Windows، الكتابة دي بتفشل من غير ما تفتح الملف أو تمسح محتواه.
التقارير وسكريبتات التصدير الجديدة بتتعمل بصلاحية للمالك بس (mode 0600)؛ واستبدال ملف موجود
بيحافظ على صلاحياته. الكتابة في named pipe مفيش حد بيقرأ منه بتفشل فورا بدل ما تقف تستنى.
قاعدة بيانات `--history` الجديدة بتتعمل هي كمان للمالك بس؛ واللي موجودة بالفعل بتحتفظ بصلاحياتها.
رسائل الـ log دايما بتروح على stderr، عشان stdout يشيل النتائج بس. ملفات التصدير اللي فيها
بيانات دخول دايما بتجبر الصلاحية تكون mode 0600.

السجل اختياري وبيكمل لقطات JSON الموجودة وأمر `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

استخدم الأرقام (IDs) اللي بتطلع من `history`؛ المثال ده بيفترض قاعدة بيانات جديدة. اللقطات بتتحفظ
بشكل transactional مع أوقات البداية والنهاية بتوقيت UTC، وإصدار الحزمة، والإعدادات الفعلية اللي
مفيهاش أسرار، والملخصات، وكل ملاحظات الأجهزة والخدمات، بما فيها الأخطاء بتاعة كل جهاز.
ملاحظات الأجهزة غير المكتملة بتفضل محفوظة. التشغيلات اللي اتلغت مش بتتحفظ. اتفاقيات التقارير
واللقطات والتصدير وأكواد خروج الفحص الموجودة كلها محفوظة زي ما هي.

أمر `history` بيعرض ملخصات JSON من غير ما يقرأ كل بيانات الأجهزة التاريخية.
أمر `compare` بيقرأ فحصين محفوظين، وبيشترط نفس هوية الهدف ونفس البورتات المختارة،
وبيعرض تغييرات الاستجابة والحالة وحالات البورتات. رقم الفحص الأقدم لازم ييجي قبل الأحدث.
لو الفحصين مسجلين `timeout` أو `backend` والقيم مختلفة، التقرير بيطلع تحذير وبرضو بيكمل
مقارنة الملاحظات. اختلاف وقت الانتظار ممكن يخلي بورت متفلتر يبان مفتوح. أخطاء الفحص
وملاحظات البورتات المجهولة بيتعلم عليها إنها غير مؤكدة بدل ما تتعامل كأن الجهاز اختفى أو البورت
اتقفل فعلا: الأجهزة اللي فيها أخطاء بتظهر في `uncertain_hosts`، وكل انتقال بورت فيه `unknown`
(حتى لو كان unknown في الفحصين) بيتحط في `unconfirmed_ports` بدل `port_changes`، إلا لو
البورت بقى مفتوح في الفحص الأحدث فبيتحسب تغيير بورت. أمري `compare` و `diff` بيصنفوا
البورتات بنفس القاعدة. حالة `no_longer_responding` معناها إنه مفيش رد، مش إثبات إن الجهاز اتشال.
كود خروج 0 في الفحص مش بيضمن إن كل جهاز رد: راجع أخطاء كل جهاز. نجاح المقارنة بيرجع 0 سواء فيه
تغييرات أو لأ؛ بينما أمر `diff` على الملفات لسه محافظ على كود الخروج 3. السجل غير المدعوم أو التالف بيرجع 1.

السجل بيحفظ معلومات الجرد، فاختار مجلد محلي محمي كويس. ملفات البروفايل والإعدادات المحفوظة
مفيهاش بيانات دخول SNMP؛ التعامل مع بيانات الدخول بيفضل عن طريق خيارات التشغيل ومتغيرات البيئة الموجودة.

<a name="inventory-diff"></a>

## مقارنة الجرد (Inventory diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

اللقطة عبارة عن ملف JSON فيه `format: "hostcensus-snapshot"` و `version: 1` وإصدار hostcensus ووقت الإنشاء بتوقيت UTC والهدف و `timeout` و `backend` لو الفحص سجلهم، والخدمات اللي اتفحصت، والأجهزة الشغالة بنفس شكل تقرير `-o`. الأجهزة المطفية بتتساب برا. أمر `diff` بيقبل كمان تقارير JSON العادية اللي طالعة من `scan -o`، حتى اللي كانت من قبل ما حقل `services` يكون موجود.

أمر `diff` بيعرض الأجهزة الجديدة والأجهزة اللي اختفت، والبورتات اللي اتفتحت أو اتقفلت على أجهزة موجودة في الفحصين، والخدمات اللي اتغير فيها `version`. البورتات اللي اتفحصت في واحد بس من الفحصين مش بتتقارن، وبيظهر تحذير يقول كده. الملاحظات الفاشلة عمرها ما بتتقرأ كأنها "مفيش تغيير": أي بورت حالته `unknown` في أي من الفحصين ومش مفتوح في التاني بيتحط تحت `unconfirmed` مش `closed`، ومعاه `before` بقيمة `open` أو `unknown` أو `not-open` (اتفحص وطلع مقفول أو متفلتر) و `after` بقيمة `unknown` أو `not-open`؛ أما البورت اللي مفتوح دلوقتي بيتبلغ عنه تحت `opened` حتى لو الفحص اللي قبله فشل. الجهاز اللي كل فحوصاته فشلت من غير رد في أي من الفحصين بيتحط تحت `unsettled_hosts` (مع `before`/`after` بقيمة `up` أو `uncertain` أو `absent`، بما فيها لما يفشل في الفحصين أو يكون ناقص من الملف التاني) بدل `vanished_hosts`؛ ولو رد في الفحص الأحدث بيتسجل كمان كجهاز جديد ببورتاته المفتوحة. اللقطات بتحتفظ بالأجهزة الفاشلة دي عشان السبب ده. وكمان بيظهر تحذير لو الأهداف مختلفة، أو لو الملفين سجلوا timeout أو backend مختلفين. خيار `-o PATH` بيكتب شكل الـ JSON في ملف برضو.

التقرير اللي جاي من فحص وقفه `--deadline` (`"complete": false`) بيكون فيه الأجهزة اللي لحق يوصلها بس، فعشان كده `diff` و `export` بيرفضوه بكود خروج 2. خيار `--allow-partial` بيقبله مع تحذير على stderr: ساعتها `diff` بيحط الأجهزة اللي الفحص الناقص ما ذكرهاش خالص تحت `unsettled_hosts` كـ `unscanned` بدل ما تبقى مختفية (الجهاز اللي اتسجل إنه مطفي لسه بيتحسب مختفي)، وبيخلي `partial` بـ true وعمره ما بيقول إن مفيش تغيير، وأمر `export` بيكتب تحذير في هيدر السكريبت.

أكواد خروج `diff`: `0` مفيش تغييرات، `3` لقى تغييرات أو ملاحظات ما اتأكدتش أو مدخلات ناقصة (`changed` بتبقى true كل ما أي قائمة، بما فيها `unsettled_hosts` و `unconfirmed`، ما تكونش فاضية، أو لو `partial` بـ true)، `2` ملف ناقص أو مش مقري أو لقطة مش مدعومة أو فحص ناقص من غير `--allow-partial`، `1` ما قدرش يكتب ملف `-o`.

<a name="kadupul-export"></a>

## التصدير لـ Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (نسخة متفرعة من Cacti 1.2.31) مفيهاش استيراد جماعي للأجهزة من ملف. الطريقة المدعومة لإضافة الأجهزة من سكريبت هي `cli/add_device.php`، جهاز واحد في كل استدعاء، ببارامترات شكلها `--option=value`. أمر `hostcensus export` بيكتب سكريبت POSIX `sh` فيه الاستدعاءات دي:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

كل جهاز شغال بيتحول لـ `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- الأجهزة اللي نجح فيها استعلام SNMP بتاخد `--version=2 --community=...` أو `--version=3 --username=... --authproto=... --password=...` (زائد `--privproto`/`--privpass` لـ authPriv) و `--port` و `--avail=snmp`. تصدير SNMPv3 محتاج `--snmp-user`، ووضع noAuthNoPriv بيترفض عشان `add_device.php` بيشترط كلمة سر في v3.
- الأجهزة التانية بتاخد `--version=0 --avail=ping`، مع `--ping_method=tcp --ping_port=` لأول بورت TCP مفتوح، أو ICMP لو مفيش.
- خيار `--notes` بيسرد الخدمات المفتوحة وإصداراتها. و `--description` بيبقى اسم الـ reverse-DNS لو كان بسيط (حروف وأرقام و `.` و `_` و `-`)، وإلا بيبقى الـ IP، وبيتعمل فريد مش متكرر لأن `add_device.php` بيتعامل مع أي وصف موجود أصلا كأنه تحديث للجهاز ده.

كل قيمة بيتعملها تحقق واقتباس للشيل باستخدام `shlex.quote`. بشكل افتراضي مفيش أي سر لـ SNMP بيتكتب في السكريبت: السكريبت بيقرأ `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` أو `HOSTCENSUS_SNMP_PRIV_KEY` وقت التشغيل وبيقف لو أي واحد منهم مش متظبط. خيار `--include-credentials` بيكتب القيم من متغيرات البيئة دي جوا السكريبت بدل كده، وبيعمل الملف بصلاحية mode 0600، وبيسجل تحذير. خلي بالك إن `add_device.php` نفسه بيطبع الـ community وبيستلم الأسرار كبارامترات، ودي بتبقى باينة في قائمة العمليات على سيرفر Kadupul طول ما كل استدعاء شغال.

ملف `add_device.php` بيخرج بكود 1 للتكرارات والأخطاء؛ السكريبت بيكمل، ويعد الفشل، وبيخرج بكود 1 لو فيه أي جهاز ما اتضافش. أرقام القوالب (Template ids) بتجيبها من `php cli/add_device.php --list-host-templates`. أكواد خروج `export`: `0` اتكتب، `2` مدخلات مش مقرية أو فحص ناقص من غير `--allow-partial` أو بيانات ما ينفعش تتصدر بأمان، `1` ما قدرش يكتب السكريبت.

## الإصدارات وطريقة النشر

hostcensus بتتبع [Semantic Versioning](https://semver.org/spec/v2.0.0.html): الإصلاحات
المتوافقة بتزود رقم الـ patch، والمميزات المتوافقة والإلغاءات التدريجية بتزود رقم الـ minor،
والتغييرات اللي بتكسر التوافق بتزود رقم الـ major.
الأوامر والخيارات وأكواد الخروج ومخططات JSON هي العقد العام بتاعنا؛
السلوك اللي اتعلم عليه كقديم بيفضل شغال لحد الإصدار الرئيسي الجاي، إلا لو
إصلاح أمني اضطرنا نغيره بدري (وساعتها الـ changelog بيقول ليه).

أداة release-please بتفتح PR للإصدار من عناوين Conventional Commit على فرع `main`،
وبتحدث `pyproject.toml` و `uv.lock` و `CHANGES.md`. دمجه بيعمل تاج
`vMAJOR.MINOR.PATCH` ومسودة إصدار على GitHub، والـ CI بيرفق بيها wheel متختبر
و source distribution و checksums؛ و GitHub بيحفظ إثباتات البناء (build attestations)
للملفات دي عن طريق attestations API. أحد المشرفين بيراجع المسودة وينشرها
بمجرد ما الملفات تترفق. الإصدارات عمرها ما بتتبدل بعد النشر.

النشر الموثوق على PyPI اختياري وبيحتاج ملكية المشروع و trusted publisher
وبيئة `pypi`. بينشر نفس ملفات الإصدار اللي اتراجعت من غير ما يعيد بناءها
أو يحفظ API token. الإصدارات اللي ليها تاج في المستودع العام ده بتطلع GitHub
artifact attestations؛ والـ forks الخاصة بتحتاج خطة مدعومة وتفعيل صريح. شوف
[دليل النشر الكامل](../../../docs/releasing.md) للإعداد والأوامر بالظبط وإعادة المحاولة.

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

أدوات التطوير موجودة في مجموعات اعتماديات [PEP 735](https://peps.python.org/pep-0735/)
في ملف `pyproject.toml` (`dev`, `fuzz`, `build`)، عشان عمرها ما تظهر في
بيانات الحزمة المنشورة. ملف `uv.lock` هو ملف القفل الوحيد؛ والـ CI بيثبت بـ
`uv sync --locked` وبيفشل لو ملف القفل قديم. اختار المفسر عن طريق
`uv python` أو mise (`mise exec python@3.14 -- uv sync --locked`) أو أي Python 3.12+.

الـ CI بيلزم بحد أدنى لتغطية الاختبارات 90% على الحزمة. اختبارات الوحدة بتشمل سيرفرات loopback
مضبوطة وحالات اختبار أوفلاين للبروفايلات والسجل ومتحقق الإصدارات؛ ومعمل Compose بيشغل
OpenSSH و MariaDB و nginx و net-snmp على شبكة bridge معزولة. شغله عن طريق
`make test-integration`. شوف [CONTRIBUTING.md](../../../CONTRIBUTING.md) و
[أدوات النشر](../../../scripts/README.md).

كونتينر التشغيل بيشتغل بـ UID/GID 10001 من غير home directory ومن غير shell login
ومن غير pip، وبيقدر يكتب في `/app/output`. ادي للمستخدم ده صلاحية الكتابة على
أي مجلد مخرجات بتعمله mount. مش بيحتاج أي capabilities وبيشتغل مع
root filesystem للقراءة بس، فتقدر تشغله كده:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap بيستخدم سلوك اكتشاف TCP من غير صلاحيات عالية جوا الكونتينر ده. الـ CI بيفشل
بناء الصورة لو Trivy لقى أي ثغرة HIGH أو CRITICAL ليها إصلاح.

## فحوصات سلسلة التوريد

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
بيشتغل على main وكل أسبوع، وبينشر التقييم الحقيقي بتاعه، وبيرفع النتائج لـ GitHub
code scanning. الـ Actions وقواعد الكونتينرات متثبتة بـ hashes ثابتة؛ واعتماديات Python
متثبتة في `uv.lock`. أي فشل في Bandit بيفشل الـ CI، واختبارات Atheris fuzzing
المحدودة بتجرب محللات SSH و MySQL و HTTP والشهادات و SNMPv3 BER
من غير اتصال بالشبكة.

Scorecard بيقيس كمان نشاط المراجعة التاريخي، وتنوع المساهمين، ومصدر الإصدارات.
التقييمات دي بتعكس الأدلة الفعلية؛ ومش ادعاء إن كل فحوصات الحوكمة أو الإصدارات
التاريخية متحققة بالكامل. شوف [SECURITY.md](../../../SECURITY.md) و [مصدر الإصدارات](../../../docs/releasing.md).

## اللغات والتعريب

رسائل الـ CLI وجداول الملخص والمقارنة على الـ terminal بتدعم 45 لغة ولهجة (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) من غير أي اعتماديات تشغيل إضافية. اختيار اللغة بيمشي حسب `--lang`، وبعدين `LC_ALL` و `LC_MESSAGES` و `LANG`، وبيرجع لـ `en` لو مفيش. مخططات JSON وأعمدة CSV وسكريبتات التصدير بتفضل زي ما هي من غير تغيير في كل اللغات.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## المساهمة

المساهمات لازم يكون معاها حالة قابلة لإعادة الإنتاج، وتحافظ على عقود الـ CLI
وصيغ البيانات الموثقة، وتعدي فحوصات الجودة اللي فوق. شوف
[CONTRIBUTING.md](../../../CONTRIBUTING.md) عشان تعرف خطوات التطوير و
[دليل النشر](../../../docs/releasing.md) لقرارات التوافق والإصدارات.

## الأمان والترخيص

شوف [SECURITY.md](../../../SECURITY.md) عشان تعرف طريقة الإبلاغ الخاص والإصدارات المدعومة.
أداة hostcensus مرخصة تحت [رخصة MIT](../../../LICENSE).

ترويسات ملفات الكود بتستخدم معرفات SPDX وبتحافظ على حقوق المساهمين من تاريخ Git.
شوف [AUTHORS.md](../../../AUTHORS.md) لقائمة المساهمين. ملفات الالتقاط الثنائية للاختبارات
وملف القفل المولّد بيستخدموا ملفات `.license` جنبهم؛ ونص رخصة MIT موجود في `LICENSES/MIT.txt`.
