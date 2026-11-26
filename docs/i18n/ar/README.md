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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · **العربية** · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

أداة hostcensus هي واجهة سطر أوامر بلغة Python لجرد الخدمات بشكل قابل للتكرار على الشبكات التي تديرها. تسجل الأداة ما تكشف عنه الأجهزة، وتقارن الملاحظات بمرور الوقت، وتنشئ نصوص استيراد لـ Kadupul. تستخدم الواجهة الخلفية الافتراضية مقابس asyncio دون صلاحيات الجذر؛ كما يمكن للاكتشاف الاختياري عبر Nmap تحديد المضيفين خارج نطاق منافذ الخدمات المهيأة.

## لماذا hostcensus

لا يوضح تقرير المنافذ لمرة واحدة ما إذا كانت الملاحظة التالية قد تغيرت أم أنها فشلت فحسب. تجمع أداة hostcensus بين حالات الخدمة الصريحة، والمسابير المقيدة، وملفات تعريف الفحص القابلة لإعادة الاستخدام، والسجل المحلي. يمكن للمشغلين تكرار النطاق نفسه، وفحص الأخطاء، والتمييز بين الملاحظات غير المؤكدة والتغييرات المؤكدة.

- **أدلة الخدمات:** تعريف SSH، وتحيات MySQL، وترويسات HTTP، وملاحظات شهادات TLS، واكتشاف SNMP أو استعلامات system-MIB المعتمدة على بيانات الاعتماد.
- **نطاق قابل للتكرار:** ملفات تعريف TOML مسماة، واستثناءات تراكمية، وخدمات قابلة للتهيئة، وحدود قصوى للمضيفين والمسابير، وعاملو تنفيذ مقيدون.
- **فحوصات قبل حركة الشبكة:** يتحقق الفحص المسبق المحلي من الأهداف، والأدوات، وإمكانية الوصول إلى الوجهة، ومخطط السجل، وحزم مرجع التصديق (CA) لـ TLS المهيأة.
- **سجل الجرد:** تحتفظ لقطات SQLite المعاملاتية بجميع الملاحظات؛ وتبقي المقارنات إخفاقات الماسح الضوئي والحالات غير المعروفة مرئية.
- **مخرجات قابلة للتشغيل البيني:** تقارير الطرفية، وتقارير JSON وCSV، ولقطات ملفات بإصدارات محددة، ونصوص استيراد Kadupul.

يغطي التكامل المستمر (CI) إصدارات Python 3.12 و3.13 و3.14 على Linux وmacOS، بالإضافة إلى مختبر تكامل Compose خاضع للتحكم. يستخدم الكود أسماء الأنواع المستعارة الحديثة، ونتائج الفحص المسبق ذات الأنواع المحددة، وملفات التعريف ذات الفتحات (slotted) والمعاملات المفتاحية فقط، والتنظيف غير المتزامن المهيكل مع الحفاظ على التوافق مع إصدارات التشغيل تلك. راجع [إدارة الإصدارات والإطلاقات](../../../docs/releasing.md) للاطلاع على عقد توافق SemVer وعملية الإصدار على GitHub. تصف شارة الإصدار الحزم المنشورة وليس نسخة المستودع الحالية: أحدث وسم منشور حاليًا هو `v0.3.0`، بينما تستخدم هذه النسخة من المستودع إصدار الحزمة `3.0.0`. ثبّت من نسخة المستودع لاستخدام ميزات الجرد الموثقة هنا.

ابدأ بـ [التثبيت](#install)، ثم [ملفات التعريف والسجل](#inventory-profiles-preflight-and-local-history). للاطلاع على تفاصيل التكامل، راجع [بصمات الخدمات](#fingerprints)، و[مقارنات الملفات](#inventory-diff)، و[تصدير Kadupul](#kadupul-export).

## التثبيت

يلزم وجود Python 3.12 أو أحدث؛ والإصدارات Python 3.12-3.14 هي المصفوفة المختبرة. من نسخة المستودع هذه، ثبّت تبعيات وقت التشغيل المثبتة:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

للحصول على اكتشاف المضيفين الاختياري عبر Nmap، ثبّت ملف Nmap التنفيذي باستخدام مدير الحزم الخاص بنظامك؛ ولا يلزم أي حزمة Python إضافية. يُحلل مخرج XML الخاص بـ Nmap باستخدام defusedxml، وهي تبعية أساسية، لذا يُرفض توسيع الكيانات (entity expansion). تشغل hostcensus أداة `nmap` الموجودة في `PATH` مباشرة بقائمة وسائط ثابتة، وموعد نهائي يزداد مع حجم البادئة، وحد أقصى للمخرجات يبلغ 64 MiB. لا يلزم Nmap للواجهة الخلفية الافتراضية.

## الترحيل من netprobe

hostcensus هو الاسم الجديد لأداة netprobe، الصادر في الإصدار 3.0.0. لم يُنشر المشروع أبدًا على PyPI تحت أي من الاسمين، لذا كانت عمليات التثبيت تتم من نسخة مستودع أو إصدار GitHub. يحتفظ مستودع GitHub باسمه.

| سابقًا | الآن | التوافق |
| --- | --- | --- |
| التوزيعة `netprobe` | `hostcensus` | أعد التثبيت من نسخة المستودع؛ لا توجد حزمة بالاسم القديم. |
| الأمر `netprobe` | `hostcensus` | لا يزال `netprobe` يعمل ويطبع سطر إهمال واحدًا على stderr. رموز الخروج وstdout لم تتغير. سيُزال في الإصدار الرئيسي التالي. |
| متغيرات البيئة `NETPROBE_*` | `HOSTCENSUS_*` | يُستخدم المتغير `NETPROBE_*` عندما يكون نظيره `HOSTCENSUS_*` غير مضبوط، مع تحذير واحد على stderr يذكر أسماء المتغيرات دون قيمها أبدًا. يسود `HOSTCENSUS_*` عند ضبط كليهما. سيُزال في الإصدار الرئيسي التالي. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **تغيير جذري.** لم يُثبت أي محول استيراد؛ حدّث عبارات الاستيراد. |
| وسم صورة Docker `network-discovery:test` (للتكامل المستمر فقط) ومستخدم الحاوية `netprobe` | `hostcensus:test`، المستخدم `hostcensus` | لم تُنشر أي صورة في السجل أبدًا. ابنِ الصورة مجددًا واستخدم نقطة الدخول `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | لا يزال الملف الموجود بالاسم الافتراضي القديم يُستخدم، مع تحذير، ما دام الاسم الجديد غير موجود. تبقى مسارات `--config` و`--history` الصريحة دون تغيير. |
| التقارير واللقطات التي تحتوي على `"format": "netprobe-report"` أو `"netprobe-snapshot"`، وحقل `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | لا يزال `diff` و`export` يحملان الملفات المكتوبة بالاسم القديم، وتقبل مخططات JSON المنشورة كلا التهجئتين. تستخدم الملفات الجديدة الأسماء الجديدة. لم تتغير قواعد بيانات سجل SQLite وتُحمل كما في السابق. |
| نصوص Kadupul من `netprobe export` | نصوص من `hostcensus export` | تستمر النصوص القديمة في العمل ولا تزال تقرأ `NETPROBE_SNMP_*` عند تشغيلها. تقرأ النصوص الجديدة `HOSTCENSUS_SNMP_*`. |

## مثال سريع

شُغّل من حاوية الاختبار لمختبر التكامل الموصوف ضمن قسم التطوير؛ المخرجات مختصرة:

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

## رموز الخروج

| الأمر | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | تم تسجيل الملاحظات/التقرير | فشل الفحص المسبق/الواجهة الخلفية أو السجل أو كتابة التقرير/اللقطة | هدف أو خيارات أو تهيئة أو حدود غير صالحة | - | تم بلوغ `--deadline`؛ كُتب تقرير جزئي، وتُخطي السجل واللقطة |
| `preflight` | نجحت الفحوصات | فشل فحص محلي | هدف/تهيئة غير صالحة أو وجهات متعارضة | - | - |
| `profiles` | تم سرد ملفات التعريف المتحقق منها | - | تهيئة أو تحديد غير قابل للقراءة/غير صالح | - | - |
| `history` | تم سرد الملخصات | سجل مفقود أو غير صالح أو غير مدعوم | خيارات CLI غير صالحة | - | - |
| `compare` | تم إنتاج المقارنة، بما في ذلك عند وجود تغييرات | سجل غير قابل للقراءة، أو نطاق/ترتيب غير متوافق، أو فشل في الكتابة | خيارات CLI غير صالحة | - | - |
| `diff` | لا توجد تغييرات | تعذرت كتابة ملف `-o` | مدخل مفقود أو غير قابل للقراءة أو غير مدعوم، أو فحص غير مكتمل دون `--allow-partial` | تم العثور على تغييرات، أو ملاحظات غير مؤكدة، أو فحص غير مكتمل | - |
| `export` | تم كتابة النص البرمجي | تعذرت كتابة النص البرمجي | مدخل غير قابل للقراءة، أو فحص غير مكتمل دون `--allow-partial`، أو بيانات لا يمكن تصديرها بأمان | - | - |

## البنية

| الوحدة | المسؤولية |
| --- | --- |
| `cli.py` | خيارات الأوامر، وحل ملفات التعريف، والفحص المسبق، والمسح وإعداد التقارير |
| `scanner.py`, `probes.py` | توسيع الأهداف، والعاملون المقيدون، واكتشاف المضيفين وملاحظات الخدمات |
| `config.py`, `profiles.py` | تعريفات الخدمات وملفات تعريف الجرد المتحقق منها |
| `models.py`, `output.py` | أنواع النتائج وعرض مخرجات الطرفية وJSON وCSV |
| `history.py`, `diff.py` | سجل SQLite ومقارنات لقطات الملفات ذات الإصدارات المحددة |
| `preflight.py` | الفحوصات المحلية والبحث المقيد عن إصدار Nmap |
| `export.py` | نصوص استيراد Kadupul المتحقق منها والمقتبسة بأمان |

تسجل كل ملاحظة خدمة حالتها بشكل منفصل عن هويتها المعلنة. تخضع عمليات القراءة والمواعيد النهائية لحدود؛ وتبقى استثناءات المسابير ضمن أخطاء المضيف. يستخدم سجل SQLite المعاملات، والتنظيف الصريح للاتصالات، ومسارات السرد والمقارنة للقراءة فقط. تدخل أسرار SNMP فقط عبر متغيرات البيئة أو ملفات الأسرار؛ ويخزن سجل الجرد الإعدادات الفعلية غير السرية. راجع [البنية المعمارية](../../../docs/architecture.md) للاطلاع على خط أنابيب المسح وحدوده وحدود الثقة، و[SECURITY.md](../../../SECURITY.md#authorized-use) للاستخدام المصرح به.


## الاستخدام

افحص فقط الشبكات التي تديرها.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| الخيار | المعنى |
| --- | --- |
| `NETWORK` | عنوان CIDR أو IP أو اسم مضيف؛ اختياري مع `--profile`. تُرفض معرفات نطاق IPv6. |
| `-o, --output PATH` | كتابة تقرير. يتبع التنسيق الامتداد (`.json`، `.csv`)؛ وتعود الامتدادات الأخرى إلى JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | فرض تنسيق التقرير. لا أثر له دون `--output`. يختار `.sh` تنسيق `kadupul`. |
| `-v, --verbose` | تسجيل بيانات التصحيح (debug). |
| `-q, --quiet` | إخفاء النتائج والتقدم والسجلات المعلوماتية؛ وتستمر التحذيرات والأخطاء في الظهور على stderr. |
| `--backend asyncio\|nmap` | اكتشاف المضيفين. يفحص `asyncio` (الافتراضي) منافذ الخدمات مباشرة؛ ويشغل `nmap` مسح ping باستخدام nmap أولًا ويتطلب وجود الملف التنفيذي `nmap` في `PATH`. |
| `--timeout SECONDS` | الانتظار للمسابير التي لا تحدد ميزانيتها الخاصة (الافتراضي 1.0). تستخدم مسابير الاتصال المضمنة 0.3 ثانية ما لم يحدد جدول الخدمة قيمة `timeout`. |
| `--concurrency N` | عدد المسابير قيد التشغيل في وقت واحد (الافتراضي 256). |
| `--deadline SECONDS` | إيقاف المسح بأكمله، بما في ذلك مسح nmap، بعد هذه المدة (الافتراضي 3600، والحد الأقصى 604800؛ متغير البيئة `HOSTCENSUS_DEADLINE`). تُكتب المضيفات التي انتهت في التقرير مع `"complete": false`، ولا يُكتب سجل أو لقطة، ويخرج `scan` بالرمز 4. |
| `--config PATH` | تعريفات خدمات TOML وإعدادات `[profiles]` مسماة اختيارية. |
| `--profile NAME` | استخدام ملف تعريف مسمى؛ يكون الافتراضي `hostcensus.toml` عند حذف `--config`. |
| `--exclude IP/CIDR` | إضافة استثناء؛ كرره حسب الحاجة. يستثني مضيف IPv4 المستثنى أيضًا عناوين IPv6 التي تصل إليه: المعينة لـ IPv4 (`::ffff:a.b.c.d`)، وNAT64 (`64:ff9b::/96`) و6to4. تُعامل الأهداف والاستثناءات المعينة لـ IPv4 باعتبارها عناوين IPv4 التي تشير إليها. |
| `--max-hosts N` | حد العناوين الذي يُتحقق منه قبل الاستثناءات (الافتراضي/الحد الأقصى الصارم 65,536). |
| `--history PATH` | تسجيل المسح المكتمل في قاعدة بيانات سجل SQLite اختيارية. |
| `--services NAMES` | قائمة مفصولة بفواصل لأسماء الخدمات المراد فحصها، بهذا الترتيب (الافتراضي: الكل). |
| `--ports SPEC` | قائمة مفصولة بفواصل من `NAME=PORT` (لنقل خدمة) أو `PORT` (لإضافة فحص TCP بسيط باسم `tcp-PORT`). |
| `--snmp-community-file PATH` | ملف يحمل سلسلة مجتمع SNMPv2c لاستعلام system MIB. متغير البيئة: `HOSTCENSUS_SNMP_COMMUNITY` (القيمة) أو `HOSTCENSUS_SNMP_COMMUNITY_FILE` (المسار). |
| `--snmp-user` | مستخدم SNMPv3. متغير البيئة: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`، `SHA` (الافتراضي)، `SHA224`، `SHA256`، `SHA384`، `SHA512` وملف يحمل عبارة المرور. متغير البيئة: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`، `HOSTCENSUS_SNMP_AUTH_KEY` أو `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`، `AES` (الافتراضي)، `AES128`، `AES192`، `AES192C`، `AES256`، `AES256C` وملف يحمل عبارة المرور. متغير البيئة: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`، `HOSTCENSUS_SNMP_PRIV_KEY` أو `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | كتابة لقطة بإصدار محدد أيضًا لـ `hostcensus diff`. |
| `--tls-ca-file PATH` | التحقق من شهادات HTTPS مقابل حزمة PEM هذه بدلًا من مخزن النظام. متغير البيئة: `HOSTCENSUS_TLS_CA_FILE`. |

بشكل افتراضي يُفحص كل مضيف بحثًا عن SSH (منفذ TCP 22) وSNMP (منفذ UDP 161) وMySQL (منفذ TCP 3306) وHTTP (منفذ TCP 80) وHTTPS (منفذ TCP 443). تُختبر منافذ TCP باتصال كامل. ويُختبر SNMP بطلب اكتشاف محرك SNMPv3، والذي يجب على أي وكيل SNMPv3 الرد عليه دون بيانات اعتماد؛ ولن يكتشف هذا المسبار الوكلاء الذين يتحدثون v1/v2c فقط. مع الواجهة الخلفية asyncio، يُعد المضيف نشطًا عندما يحصل أي مسبار على استجابة، بما في ذلك الاتصال المرفوض، لذلك يكون للمضيف الذي يسقط كل مسبار `alive=false` والخطأ "Host is down"؛ ولا يثبت هذا أنه متوقف فعليًا. مع `--backend nmap`، يقرر nmap المضيفين النشطين (ICMP بصلاحيات الجذر، وTCP 80/443 في الحالات الأخرى).

### البصمات

تُؤخذ بصمة كل خدمة مفتوحة مما ترسله قبل أي تسجيل دخول. لا شيء يجري مصادقة باستثناء استعلام SNMP، وفقط عند تقديم بيانات الاعتماد.

| المسبار | ما يقرأه | `version` | مفاتيح `details` |
| --- | --- | --- | --- |
| `ssh` | سطر التعريف RFC 4253 | البرمجية، مثل `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | المصافحة الأولية لـ MySQL/MariaDB | إصدار الخادم | `server_version`, `flavor`, `auth_plugin`، أو `error_code`/`error` |
| `http` | استجابة `HEAD /` | ترويسة `Server` | `status`, `server` |
| `https` | مصافحة TLS، الشهادة، `HEAD /` | ترويسة `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | اكتشاف SNMPv3؛ ومع بيانات الاعتماد، GET لـ sysDescr وsysObjectID وsysName | sysDescr | `engine_id`؛ ومع بيانات الاعتماد `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`، أو `snmp_error` |

يُحلل الهدف المحدد باسم مضيف مرة واحدة لكل مضيف ويتصل كل مسبار بذلك العنوان، المسجل بوصفه `address` في النتائج؛ ويُستخدم الاسم فقط لـ TLS SNI، والتحقق من الشهادة، وترويسة `Host` في HTTP. الاسم الذي لا يُحل يعطي حالات `unknown` وخطأ `Cannot resolve`. لا يُحتفظ بأسماء DNS العكسية إلا عندما تحتوي على محارف أسماء المضيفين، ويعمل بحد أقصى 16 استعلام بحث في وقت واحد. يستخدم HTTPS التحقق من الشهادة واسم المضيف مقابل مخزن النظام أو `--tls-ca-file`. يُحمل مخزن الثقة مرة واحدة للمسح ويُعاد استخدامه لكل مسبار HTTPS. يُقاس زمن اتصال TCP ومصافحة TLS بشكل منفصل، لذا فإن المنفذ الذي يقبل الاتصالات ولكنه يوقف المصافحة يكون `open` مع `tls_error` وليس `filtered`. إذا فشل التحقق، تسجل النتيجة `cert_verified: false` و`cert_verify_error`؛ ولا تعيد المحاولة بإعدادات أضعف ولا ترسل طلب HTTP. لا تُجمع تفاصيل الشهادة وترويسات HTTP إلا بعد نجاح التحقق. قدّم حزمة CA الصحيحة لخدمات مرجع التصديق الخاص. قد تحتوي التقارير الأقدم على `cert_read_unverified`، وهو ما لم تعد المسابير الحالية تنتجه.

تُقرأ أسرار SNMP فقط من متغيرات البيئة أو من الملفات (`--snmp-*-file`، أو المتغير المطابق `HOSTCENSUS_SNMP_*_FILE`)، ولا تُقرأ أبدًا من قيم سطر الأوامر، التي يمكن للمستخدمين المحليين الآخرين رؤيتها في قائمة العمليات. تخرج الخيارات `--snmp-community` و`--snmp-auth-key` و`--snmp-priv-key` عند إعطائها قيمة برمز الخروج 2 وتذكر البديل. يجب أن يكون ملف السر بترميز UTF-8 غير فارغ وبحجم 4096 بايت على الأكثر؛ ويُتجاهل سطر جديد أخير واحد، ويُعد ضبط كل من متغير وملف للسر نفسه خطأً. تذكر الأخطاء اسم الملف لكنها لا تطبع محتوياته أبدًا. لا تتضمن تقارير المسح والسجل قيم بيانات الاعتماد عن قصد. ويمتلك المصدّر خيار `--include-credentials` صريحًا ومنفصلًا موصوفًا أدناه. تحدد سلسلة المجتمع (community) بروتوكول SNMPv2c؛ ويحدد المستخدم بروتوكول SNMPv3، مع المصادقة عند إعطاء مفتاح مصادقة والخصوصية عند إعطاء كلا المفتاحين (يسجل `snmp_security_level` أيًّا منهما). ترفض hostcensus، برمز الخروج 2، الجمع بين سلسلة مجتمع ومستخدم v3، أو استخدام مفتاح خصوصية دون مفتاح مصادقة، أو استخدام مفاتيح دون مستخدم، ولا تعيد أبدًا محاولة استعلام v3 فاشل باستخدام v2c أو مستوى أمان أدنى. يتجاهل الوكلاء الذين يتحدثون v1/v2c فقط اكتشاف v3 الخالي من بيانات الاعتماد، لذا يظهرون كمفتوحين فقط عند تقديم سلسلة مجتمع.

يُختصر نص اللافتة (banner) إلى المحارف القابلة للطباعة ويُقيد بـ 256 محرفًا قبل تخزينه أو عرضه. كما أن عمليات القراءة مقيدة أيضًا: 4 KiB لكل سطر، و4 KiB لتحية MySQL، و16 KiB لترويسات HTTP. يُقتطع معرف محرك SNMP الأطول من 32 ثمانية (octets) قبل تخزينه. يرسل HTTP وHTTPS ترويسة Host مع عنوان IPv6 بين قوسين معقوفين ومع المنفذ عندما لا يكون 80 أو 443. وتُسبق خلايا CSV التي تبدأ بمحفز صيغة جداول البيانات ببادئة بحيث تبقى الخلية نصًا.

### الحدود

يقبل التشغيل الواحد بحد أقصى 65,536 عنوانًا، و64 خدمة، و524,288 مسبارًا (عدد المضيفين مضروبًا في عدد الخدمات)؛ وتخرج الطلبات الأكبر برمز الخروج 2 قبل إرسال أي شيء. يُقيد `--concurrency` بـ 4096 مقبسًا. ولكل مسبار موعد نهائي صارم يبلغ أربعة أضعاف ميزانيته الخاصة. تستخدم مسابير الاتصال (`tcp`، `ssh`، `mysql`، `http`) مهلة 0.3 ثانية ما لم تحدد تلك الخدمة `timeout`. ويستخدم SNMP وHTTPS قيمة `--timeout` (الافتراضية 1.0) عندما لا تحدد الخدمة قيمة. يُبلغ عن المسبار الذي يبلغ الموعد النهائي بوصفه `unknown` مع "probe timed out" في `errors`. كما تُعد إخفاقات المقابس المحلية (مثل نفاد واصفات الملفات) `unknown` مع تسجيل الخطأ؛ ولا تُحسب أبدًا كمنفذ مرشّح (filtered) أو مضيف متوقف. قبل بدء الفحص، ترفع hostcensus الحد المرن للملفات المفتوحة نحو الحد الصارم ليستوعب `--concurrency` مضافًا إليها 64 واصفًا؛ وعندما تعجز عن ذلك، يفشل فحص `open files` المسبق ويخرج `scan` بالرمز 1 قبل إرسال حركة الشبكة. يستخدم اكتشاف Nmap مهلة 30 ثانية للمضيف. تُمرر البادئة إلى nmap بصيغة CIDR، ويفشل المسح بالرمز 1 عندما يبلغ nmap عن عناوين أقل مما أُعطي (مثل اسم لا يمكنه حله) بدلًا من اعتبار المضيفين متوقفين. يُحلل الهدف المحدد باسم مضيف مرة واحدة ويُعطى nmap ذلك العنوان، بحيث يصل الاكتشاف والمسابير إلى الجهاز نفسه. البادئة الكاملة هي عملية nmap واحدة يبلغ موعدها النهائي للعملية الفرعية 35 ثانية لكل 256 عنوانًا، مقربةً للأعلى. تستخدم عمليات المسح التي تتضمن استثناءات دفعات من 256 مضيفًا وموعدًا نهائيًا قدره 35 ثانية لكل دفعة. إنشاء العاملين مقيد بشكل مستقل عن حجم النطاق. يمتلك DNS العكسي وتحليل أسماء المضيفين موعدًا نهائيًا منفصلًا قدره ثانيتان؛ ويُترك استدعاء المحلل الذي لا يعود أبدًا في خيطه الخاص، بحيث لا يمكنه إبقاء hostcensus قيد التشغيل بعد هذه الحدود. يعمل بحد أقصى 16 استعلام بحث في وقت واحد، ويحتفظ الاستدعاء المتروك بخانته حتى يعود، بحيث يظل عدد الخيوط العالقة مقيدًا؛ وإذا علقت الخانات الـ 16 جميعها، تصطف استعلامات البحث اللاحقة لخانة خارج الموعد النهائي ذي الثانيتين (الذي يبدأ بمجرد توفر خانة) حتى يوقف `--deadline` المسح. ويمكن لـ `NetworkScanner` المستخدم كمكتبة دون `deadline` أن ينتظر مثل هذه الخانة إلى أجل غير مسمى. ويقيد `--deadline` (الافتراضي ساعة واحدة) التشغيل بأكمله فوق كل ذلك.

### تهيئة الخدمات

يمكن تغيير الخدمات باستخدام ملف TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

تكون قيمة `probe` واحدة من `tcp` أو `ssh` أو `mysql` أو `http` أو `https` أو `snmp`، وتأخذ اسم الخدمة افتراضيًا عندما يكون اسمًا لمسبار، وإلا فتكون `tcp`. يستخدم `snmp` فقط بروتوكول UDP. تتكون أسماء الخدمات من أحرف صغيرة وأرقام و`-` و`_`. لا يمكن لخدمتين مشاركة المنفذ والبروتوكول نفسيهما؛ يسجل السجل حالة واحدة لذلك الزوج. المعامل `timeout` اختياري، بالثواني، ولا يقل عن 0.05. تستخدم المسابير من نمط الاتصال (`tcp`، `ssh`، `mysql`، `http`) مهلة 0.3 ثانية افتراضيًا. ويستخدم `snmp` و`https` قيمة `--timeout` الخاصة بالمسح عندما لا تحدد الخدمة `timeout`. لا يستبدل `--timeout` ميزانية تمتلكها الخدمة بالفعل.

تقارير JSON هي مستندات بإصدار محدد (`"format": "hostcensus-report"`، `"version": 1`) تسجل الهدف والخدمات المفحوصة والإعدادات بجانب `devices`؛ ويكتب `--format json` دون `-o` التقرير إلى stdout بدلًا من الجدول. يمتلك كل مخرج JSON مخططًا منشورًا؛ راجع [مخرجات JSON](../../../docs/json-output.md). تحتفظ الأجهزة بحقول `ip` و`alive` و`ssh` و`snmp` و`mysql` و`hostname` و`errors` الأصلية وتضيف قائمة `services` تتضمن `name` و`port` و`protocol` و`state` (`open`، أو `closed`، أو `filtered`، أو `unknown` عندما يفشل المسبار محليًا أو يبلغ موعده النهائي) و`version` و`details` لكل مسبار. وتكتسب مخرجات CSV عمودين لاحقين هما `services` و`versions` للخدمات المفتوحة. وتتبع القيم المنطقية `ssh` و`snmp` و`mysql` الخدمات التي تحمل تلك الأسماء بالضبط.


## ملفات تعريف الجرد والفحص المسبق والسجل المحلي

تتشارك ملفات التعريف المسماة ملف TOML مع تعريفات `[services]` الحالية. انسخ [hostcensus.example.toml](../../../hostcensus.example.toml) إلى `hostcensus.toml` وحدد الشبكات التي تديرها:

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

يحل `preflight` الخيارات وملفات التعريف تمامًا كما يفعل `scan`، بما في ذلك `--concurrency` لفحص الملفات المفتوحة، لذا فإن نجاح الفحص المسبق يعني أن `scan` سيبدأ بالخطة نفسها.

تقبل ملفات التعريف كلًا من `network` و`exclusions` و`services` و`ports` و`backend` و`timeout` و`concurrency` و`max_hosts`. وتستخدم `services` و`ports` صيغة القائمة المفصولة بفواصل الحالية. تتجاوز خيارات CLI الصريحة إعدادات ملف التعريف؛ وتُضاف خيارات `--exclude` المتكررة إلى استثناءات ملف التعريف. يجب أن تكون الشبكة الصريحة مع `--profile` محتواة ضمن نطاق IP/CIDR لملف التعريف هذا. تظل أسماء المضيفين مدعومة لعمليات المسح المباشرة، ولكن لا يمكن دمجها مع استثناءات IP. تُطبق حدود المضيفين قبل الاستثناءات؛ ولا يزال الحد الإجمالي للمسابير يُطبق بعد ذلك. وتُستبعد المضيفات المستثناة من كل من فحوصات الخدمات واكتشاف Nmap الاختياري.

يجري كل مسح فحوصات مسبقة محلية قبل حركة الشبكة نحو الأهداف: حدود الأهداف/المسابير، والوصول إلى الوجهة، وتوفر الملف التنفيذي/المغلف الاختياري لـ Nmap، ومخطط السجل، وحزمة TLS CA المهيأة. يُخرج `preflight` تقريرًا بصيغة JSON ولا يمسح الأهداف ولا ينشئ قاعدة بيانات للسجل. يكتب ملفًا شقيقًا مؤقتًا لاختبار الوصول إلى الوجهة دون تغيير المحتويات الحالية. لا تزال الواجهة الخلفية الافتراضية asyncio لا تتطلب Nmap ولا صلاحيات الجذر. يجب أن تكون مسارات الوجهات متمايزة عن بعضها البعض وعن تهيئة الإدخال، بما في ذلك الروابط الصلبة (hard links)؛ وتُرفض الروابط الرمزية (symlinks) للوجهات. ترجع الفحوصات الفاشلة الرمز 1؛ ويرجع النطاق/التهيئة غير الصالحة الرمز 2.

تتطلب عمليات كتابة التقارير والتصدير دعم `O_NOFOLLOW`. وعلى المنصات التي تفتقر إليه، بما في ذلك Windows، تفشل عمليات الكتابة هذه دون فتح الوجهة أو اقتطاعها. تكون التقارير ونصوص التصدير الجديدة للمالك فقط (الوضع 0600)؛ ويحافظ استبدال ملف موجود على أذوناته. تفشل الكتابة إلى أنبوب مسمى (named pipe) دون قارئ فورًا بدلًا من الانتظار. كما تُنشأ قاعدة بيانات `--history` الجديدة للمالك فقط؛ وتحتفظ القاعدة الموجودة بوضعها. تذهب رسائل السجل دائمًا إلى stderr، بحيث لا يحمل stdout سوى النتائج. وتفرض عمليات التصدير التي تتضمن بيانات اعتماد دائمًا الوضع 0600.

السجل اختياري ويكمّل لقطات JSON الحالية وأمر `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

استخدم المعرفات من `history`؛ يفترض المثال قاعدة بيانات جديدة. تُخزن اللقطات معاملاتيًا مع أوقات البدء والانتهاء بتوقيت UTC، وإصدار الحزمة، والإعدادات الفعلية غير السرية، والملخصات، وجميع ملاحظات المضيفين والخدمات، بما في ذلك الأخطاء لكل مضيف. ويُحتفظ بملاحظات المضيفين غير المكتملة. لا تُحفظ عمليات التشغيل الملغاة. وتُصان عقود رموز الخروج الحالية للتقارير واللقطات والتصدير والمسح.

يسرد `history` ملخصات JSON دون قراءة جميع حمولات الأجهزة التاريخية. يقرأ `compare` عمليتي مسح محفوظتين، ويتطلب تطابق هويات الأهداف والمنافذ المحددة، ويبلغ عن تغييرات الاستجابة والحالة وحالة المنافذ. يجب أن يسبق معرف المسح الأقدم المعرف الأحدث. عندما يسجل كلا المسحين `timeout` أو `backend` وتختلف تلك القيم، يدرج التقرير تحذيرًا ويستمر في مقارنة الملاحظات. قد يجعل زمن الانتظار المختلف المنفذ المرشّح يبدو مفتوحًا. تُوسم أخطاء الماسح الضوئي وملاحظات المنافذ غير المعروفة بوصفها غير مؤكدة بدلًا من معاملتها كاختفاء أو إغلاق مؤكد: تظهر المضيفات التي بها أخطاء في `uncertain_hosts`، ويُدرج كل انتقال منفذ يتضمن `unknown` (بما في ذلك كونه غير معروف في كلا المسحين) في `unconfirmed_ports` بدلًا من `port_changes`، باستثناء المنفذ المفتوح في المسح الأحدث، والذي يُعد تغيير منفذ. يصنف `compare` و`diff` المنافذ بالقاعدة نفسها. يعني `no_longer_responding` عدم وجود استجابة، وليس دليلًا على إزالة الجهاز. لا يضمن رمز خروج المسح 0 استجابة كل مضيف: افحص الأخطاء لكل مضيف. يرجع نجاح المقارنة 0 سواء وُجدت تغييرات أم لا؛ ويحتفظ أمر `diff` للملفات بعقد رمز الخروج 3 الخاص به. ويرجع السجل غير المدعوم أو التالف الرمز 1.

يخزن السجل معلومات الجرد، لذا اختر دليلًا محليًا محميًا بشكل مناسب. لا تحتوي ملفات التعريف والإعدادات المخزنة على بيانات اعتماد SNMP؛ ويستمر التعامل مع بيانات الاعتماد عبر خيارات وقت التشغيل وبيئته الحالية.

## مقارنة الجرد

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

اللقطة هي مستند JSON يحتوي على `format: "hostcensus-snapshot"`، و`version: 1`، وإصدار hostcensus، ووقت الإنشاء بتوقيت UTC، والهدف، وقيمتي `timeout` و`backend` للمسح عندما يسجلهما المسح، والخدمات التي فُحصت، والمضيفين النشطين بالشكل نفسه لتقرير `-o`. وتُستبعد المضيفات المتوقفة. يقبل `diff` أيضًا تقارير `scan -o` العادية بصيغة JSON، بما في ذلك تلك التي تسبق وجود حقل `services`.

يبلغ `diff` عن المضيفين الجدد والمختفين، والمنافذ التي فُتحت أو أُغلقت على مضيفين موجودين في كليهما، والخدمات التي تغير `version` الخاص بها. ولا تُقارن المنافذ التي فُحصت في أحد المسحين فقط، ويوضح تحذير ذلك. ولا تُفسر الملاحظات الفاشلة أبدًا على أنها "لا تغيير": المنفذ الذي يكون `unknown` في أي من المسحين وليس مفتوحًا في المسح اللاحق يُدرج ضمن `unconfirmed`، وليس `closed`، مع `before` بقيمة `open` أو `unknown` أو `not-open` (مفحوص ومغلق أو مرشّح) و`after` بقيمة `unknown` أو `not-open`؛ أما المنفذ المفتوح الآن فيُبلغ عنه ضمن `opened` حتى لو فشل المسبار الأسبق. المضيف الذي فشلت جميع مسابيره دون إجابة في أي من المسحين يُدرج ضمن `unsettled_hosts` (مع `before`/`after` بقيمة `up` أو `uncertain` أو `absent`، بما في ذلك عند فشله في كلا المسحين أو غيابه عن الملف الآخر) بدلًا من `vanished_hosts`؛ وإذا استجاب في المسح اللاحق يُبلغ عنه أيضًا كمضيف جديد بمنافذه المفتوحة. وتحتفظ اللقطات بتلك المضيفات الفاشلة لهذا السبب. كما يظهر تحذير عندما تختلف الأهداف، وعندما يسجل كلا الملفين مهلة أو واجهة خلفية وتختلف تلك القيم. ويكتب `-o PATH` الصيغة بصيغة JSON إلى ملف أيضًا.

التقرير الناتج عن مسح أوقفه `--deadline` (`"complete": false`) لا يسرد سوى المضيفين الذين وصل إليهم، لذا يرفضه `diff` و`export` برمز الخروج 2. ويقبله `--allow-partial` مع تحذير على stderr: يدرج `diff` حينها المضيفين الذين لم يدرجهم المسح غير المكتمل إطلاقًا ضمن `unsettled_hosts` بوصفهم `unscanned` بدلًا من مختفين (المضيف الذي أدرجه كمتوقف يظل مختفيًا)، ويضبط `partial` على true ولا يبلغ أبدًا عن عدم وجود تغيير، ويكتب `export` تحذيرًا في ترويسة النص البرمجي.

رموز خروج `diff`: `0` لا توجد تغييرات، `3` تم العثور على تغييرات، أو ملاحظات تعذر تأكيدها، أو مدخل غير مكتمل (يكون `changed` صحيحًا كلما كانت أي قائمة، بما في ذلك `unsettled_hosts` و`unconfirmed`، غير فارغة، أو كان `partial` صحيحًا)، `2` ملف مفقود، أو غير قابل للقراءة، أو ليس لقطة مدعومة، أو غير مكتمل دون `--allow-partial`، `1` تعذرت كتابة ملف `-o`.

## تصدير Kadupul

لا يدعم [Kadupul](https://github.com/kadupulhq/kadupul) (وهو تفرع من Cacti 1.2.31) استيراد ملفات الأجهزة بالجملة. وطريقته المدعومة لإضافة الأجهزة من نص برمجي هي `cli/add_device.php`، جهاز واحد في كل استدعاء، باستخدام وسائط `--option=value`. يكتب `hostcensus export` نصًا برمجيًا متوافقًا مع POSIX `sh` يحتوي على تلك الاستدعاءات:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

يتحول كل مضيف نشط إلى `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- تحصل المضيفات التي نجح فيها استعلام SNMP أثناء المسح على `--version=2 --community=...` أو `--version=3 --username=... --authproto=... --password=...` (بالإضافة إلى `--privproto`/`--privpass` لوضع authPriv)، و`--port` و`--avail=snmp`. يتطلب تصدير SNMPv3 الخيار `--snmp-user`، ويُرفض وضع noAuthNoPriv لأن `add_device.php` يتطلب كلمة مرور v3.
- تحصل المضيفات الأخرى على `--version=0 --avail=ping`، مع ضبط `--ping_method=tcp --ping_port=` على أول منفذ TCP مفتوح، أو ICMP إذا لم يوجد.
- يسرد `--notes` الخدمات المفتوحة وإصداراتها. ويكون `--description` هو اسم DNS العكسي عندما يكون بسيطًا (أحرف، أرقام، `.`، `_`، `-`)، وإلا فيكون عنوان IP، ويُجعل فريدًا، لأن `add_device.php` يعامل الوصف الموجود باعتباره تحديثًا لذلك الجهاز.

يُتحقق من كل قيمة وتُقتبس للصدفة باستخدام `shlex.quote`. افتراضيًا لا يُكتب أي سر SNMP: يوسع النص البرمجي `HOSTCENSUS_SNMP_COMMUNITY` أو `HOSTCENSUS_SNMP_AUTH_KEY` أو `HOSTCENSUS_SNMP_PRIV_KEY` وقت التشغيل ويتوقف إذا كان أحدها غير مضبوط. يكتب `--include-credentials` القيم من متغيرات البيئة تلك في النص البرمجي بدلًا من ذلك، وينشئه بالوضع 0600، ويسجل تحذيرًا. يطبع `add_device.php` نفسه سلسلة المجتمع ويتلقى الأسرار كوسائط، والتي تكون مرئية في قائمة عمليات خادم Kadupul أثناء تشغيل كل استدعاء.

يخرج `add_device.php` بالرمز 1 للتكرارات والأخطاء؛ ويواصل النص البرمجي العمل، ويحصي الإخفاقات، ويخرج بالرمز 1 إذا لم يُضف أي جهاز. تأتي معرفات القوالب من `php cli/add_device.php --list-host-templates`. رموز خروج `export`: `0` تمت الكتابة، `2` مدخل غير قابل للقراءة، أو مسح غير مكتمل دون `--allow-partial`، أو بيانات لا يمكن تصديرها بأمان، `1` تعذرت كتابة النص البرمجي.

## إدارة الإصدارات وعملية الإطلاق

تتبع hostcensus معيار [التسلسل الدلالي للإصدارات (Semantic Versioning)](https://semver.org/spec/v2.0.0.html): تزيد الإصلاحات المتوافقة رقم إصدار التصحيح (patch)، وتزيد الميزات/الإهمالات المتوافقة رقم الإصدار الثانوي (minor)، وتزيد التغييرات الكاسرة للتوافق رقم الإصدار الرئيسي (major). تشكل الأوامر والخيارات ورموز الخروج ومخططات JSON العقد العام؛ ويستمر السلوك المهمل في العمل حتى الإصدار الرئيسي التالي، ما لم يتطلب إصلاح أمني تغييره في وقت أبكر (ويوضح سجل التغييرات السبب حينها).

تفتح أداة release-please طلب سحب (PR) للإصدار استنادًا إلى عناوين Conventional Commit على الفرع `main`، مع تحديث أرقام الإصدار في `pyproject.toml` و`uv.lock` و`CHANGES.md`. ويؤدي دمجه إلى إنشاء الوسم `vMAJOR.MINOR.PATCH` ومسودة إصدار على GitHub، حيث يرفق التكامل المستمر (CI) حزمة wheel مختبرة، وتوزيعة المصدر، ومجاميع التحقق؛ ويخزن GitHub شهادات إثبات البناء لتلك الملفات عبر واجهة برمجة تطبيقات الإثباتات (attestations API) الخاصة به. يراجع أحد المشرفين المسودة وينشرها بمجرد إرفاق الملفات. ولا تُستبدل الإصدارات أبدًا.

النشر الموثوق على PyPI اختياري ويتطلب ملكية المشروع، وناشرًا موثوقًا، وبيئة `pypi`. وينشر مخرجات الإصدار المفحوصة نفسها دون إعادة البناء أو تخزين رمز API. وتولد الإصدارات الموسومة في هذا المستودع العام إثباتات مخرجات GitHub؛ بينما تتطلب التفرعات الخاصة خطة مدعومة وتفعيلًا صريحًا. راجع [دليل الإصدار الكامل](../../../docs/releasing.md) للإعداد والأوامر الدقيقة وإعادة المحاولات.

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

توجد أدوات التطوير في مجموعات تبعيات [PEP 735](https://peps.python.org/pep-0735/) داخل `pyproject.toml` (`dev`, `fuzz`, `build`)، لذا لا تظهر أبدًا في البيانات الوصفية للحزمة المنشورة. يعد `uv.lock` ملف القفل الوحيد؛ ويثبت التكامل المستمر (CI) باستخدام `uv sync --locked` ويفشل عندما يكون ملف القفل قديمًا. اختر المفسر باستخدام `uv python`، أو mise (`mise exec python@3.14 -- uv sync --locked`)، أو أي إصدار Python 3.12+.

يفرض التكامل المستمر حدًا أدنى لتغطية الحزمة بنسبة 90%. وتشمل اختبارات الوحدة خوادم استرجاع (loopback) خاضعة للتحكم وحالات غير متصلة للتحقق من ملفات التعريف والسجل والإصدار؛ ويشغل مختبر Compose كلًا من OpenSSH وMariaDB وnginx وnet-snmp على جسر معزول. شغّله باستخدام `make test-integration`. راجع [CONTRIBUTING.md](../../../CONTRIBUTING.md) و[أدوات الإصدار](../../../scripts/README.md).

تعمل حاوية وقت التشغيل بمعرف مستخدم ومجموعة UID/GID 10001 دون دليل رئيسي، ودون تسجيل دخول إلى الصدفة، ودون pip، ويمكنها الكتابة إلى `/app/output`. امنح ذلك المستخدم صلاحية الكتابة إلى أي دليل مخرجات مُركّب. ولا تحتاج إلى أي قدرات (capabilities) وتعمل مع نظام ملفات جذري للقراءة فقط، لذا يمكن تشغيلها كالتالي:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

يستخدم Nmap سلوك اكتشاف TCP غير المتميز الخاص به في هذه الحاوية. ويفشل التكامل المستمر بناء الصورة عند وجود أي ثغرة أمنية قابلة للإصلاح بمستوى HIGH أو CRITICAL يبلغ عنها Trivy.

## فحوصات سلسلة التوريد

يعمل [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) على الفرع main وأسبوعيًا، وينشر درجته الحقيقية، ويرفع النتائج إلى فحص الكود في GitHub. وتُثبت إجراءات GitHub وقواعد الحاويات بتجزئات غير قابلة للتغيير؛ كما تُحل تبعيات Python في `uv.lock`. وتؤدي إخفاقات Bandit إلى فشل التكامل المستمر، ويختبر التشويش (fuzzing) المقيد عبر Atheris محللات SSH وMySQL وHTTP والشهادات وSNMPv3 BER دون وصول إلى الشبكة.

يقيس Scorecard أيضًا نشاط المراجعة التاريخي، وتنوع المساهمين، ومنشأ الإصدارات. تعكس هذه الدرجات أدلة فعلية؛ وليست ادعاءات باستيفاء كل فحص للحوكمة أو الإصدارات التاريخية. راجع [SECURITY.md](../../../SECURITY.md) و[منشأ الإصدارات](../../../docs/releasing.md).

## التوطين واللغات

تدعم رسائل واجهة سطر الأوامر وجداول الملخص والمقارنة في الطرفية 45 لغة وإعدادًا محليًا (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) دون أي تبعيات إضافية لوقت التشغيل. يعتمد تحديد اللغة على `--lang` أولًا، ثم `LC_ALL`، و`LC_MESSAGES`، و`LANG`، مع الرجوع إلى `en` عند عدم التوفر. وتبقى مخططات JSON وأعمدة CSV ونصوص التصدير البرمجية دون تغيير عبر جميع اللغات.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## المساهمة

ينبغي أن تتضمن المساهمات حالة قابلة لإعادة الإنتاج، وأن تحافظ على عقود واجهة سطر الأوامر وتنسيقات البيانات الموثقة، وأن تجتاز فحوصات الجودة المذكورة أعلاه. راجع [CONTRIBUTING.md](../../../CONTRIBUTING.md) للاطلاع على سير عمل التطوير و[دليل الإصدار](../../../docs/releasing.md) لقرارات التوافق وإدارة الإصدارات.

## الأمان وحالة الترخيص

راجع [SECURITY.md](../../../SECURITY.md) للإبلاغ الخاص والإصدارات المدعومة. ترخّص أداة hostcensus بموجب [رخصة MIT](../../../LICENSE).

تستخدم ترويسات المصادر معرفات SPDX وتحافظ على حقوق المساهمين من سجل Git. راجع [AUTHORS.md](../../../AUTHORS.md) للاطلاع على الإسناد. وتستخدم ملفات التقاط الاختبارات الثنائية وملف القفل المولد ملفات `.license` مجاورة؛ ويتوفر نص رخصة MIT في `LICENSES/MIT.txt`.
