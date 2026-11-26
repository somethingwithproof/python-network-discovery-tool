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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · **עברית** · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus הוא כלי CLI ב-Python לביצוע סקירת מלאי שירותים (service inventory) חוזרת ונשנית ברשתות שבניהולכם. הכלי מתעד אילו שירותים המכשירים חושפים, משווה תצפיות לאורך זמן ומייצר סקריפטים לייבוא אל Kadupul. מנוע ברירת המחדל משתמש ב-sockets של asyncio ללא הרשאות root; גילוי אופציונלי באמצעות Nmap מאפשר לזהות מארחים מעבר לפורטי השירות המוגדרים.

## מדוע hostcensus

דוח פורטים חד-פעמי אינו מסביר אם התצפית הבאה השתנתה או פשוט נכשלה. hostcensus משלב מצבי שירות מפורשים, בדיקות תוחמות (bounded probes), פרופילי סריקה רב-פעמיים והיסטוריה מקומית. מפעילים יכולים לחזור על אותו היקף סריקה, לבחון שגיאות ולהבחין בין תצפיות לא ודאיות לבין שינויים מאומתים.

- **ראיות שירות:** זיהוי SSH, ברכות פתיחה של MySQL, כותרות HTTP, תצפיות תעודות TLS, וכן גילוי SNMP או שאילתות system-MIB עם הרשאות.
- **היקף חוזר ונשנה:** פרופילי TOML בעלי שם, החרגות מצטברות, שירותים ניתנים להגדרה, תקרות מארחים/בדיקות ועובדים (workers) תחומי-מקביליות.
- **בדיקות לפני תעבורת רשת:** בדיקת מוכנות מקומית (preflight) המאמתת יעדים, כלים, גישה ליעד השמירה, סכמת היסטוריה וחבילות CA מוגדרות עבור TLS.
- **היסטוריית מלאי:** תמונות מצב (snapshots) טרנזקציוניות ב-SQLite השומרות את כל התצפיות; השוואות שומרות על נראות של כשלי סורק ומצבים לא ידועים.
- **פלט תואם למערכות אחרות:** דוחות טרמינל, JSON ו-CSV, תמונות מצב קובץ מנוהלות גרסאות, וסקריפטי ייבוא ל-Kadupul.

CI מכסה את Python 3.12, 3.13 ו-3.14 ב-Linux וב-macOS, בנוסף למעבדת אינטגרציה מבוקרת ב-Compose. הקוד משתמש בכינויי טיפוסים מודרניים (type aliases), תוצאות preflight מוקלדות (typed), פרופילים עם keyword-only ו-slots, וניקוי אסינכרוני מובנה תוך שמירה על תמיכה בגרסאות זמן ריצה אלו. ראו [ניהול גרסאות ושחרורים](../../../docs/releasing.md) עבור חוזה התאימות של SemVer ותהליך השחרור ב-GitHub. תגית השחרור מתארת ארטיפקטים שפורסמו, ולא את העותק המקומי הנוכחי: התגית המפורסמת האחרונה היא כרגע `v0.3.0`, בעוד שענף זה משתמש בגרסת חבילה `3.0.0`. התקינו מתוך העותק המקומי כדי להשתמש בתכונות המלאי המתועדות כאן.

התחילו ב[התקנה](#install), ולאחר מכן עברו אל [פרופילים והיסטוריה](#inventory-profiles-preflight-and-local-history). לפרטי אינטגרציה, ראו [טביעות אצבע של שירותים](#fingerprints), [השוואת קבצים](#inventory-diff) ו[ייצוא ל-Kadupul](#kadupul-export).

## התקנה

נדרשת גרסת Python 3.12 ומעלה; מטריצת הבדיקות כוללת את Python 3.12–3.14. מתוך העותק המקומי (checkout) הזה, התקינו את תלויות זמן הריצה הנעולות:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

לגילוי מארחים אופציונלי עם Nmap, התקינו את קובץ ההרצה של Nmap באמצעות מנהל החבילות של הפלטפורמה שלכם; אין צורך בחבילת Python נוספת. פלט ה-XML של Nmap מנותח באמצעות defusedxml, תלות ליבה, כך שהרחבת ישויות (entity expansion) נדחית. hostcensus מריץ ישירות את `nmap` שנמצא ב-`PATH` עם רשימת ארגומנטים קבועה, מגבלת זמן הגדלה בהתאם לגודל הקידומת (prefix), ומגבלת פלט של 64 MiB. אין צורך ב-Nmap עבור מנוע ברירת המחדל.

## מעבר מ-netprobe

hostcensus הוא השם החדש של netprobe, ששוחרר בגרסה 3.0.0. הפרויקט מעולם לא פורסם ב-PyPI תחת אף אחד מהשמות, כך שהתקנות בוצעו מעותק מקומי או משחרור ב-GitHub. מאגר ה-GitHub שומר על שמו.

| היה | כעת | תאימות |
| --- | --- | --- |
| חבילת ההפצה `netprobe` | `hostcensus` | התקינו מחדש מהעותק המקומי; אין חבילה בשם הישן. |
| הפקודה `netprobe` | `hostcensus` | `netprobe` עדיין רצה ומדפיסה שורת התיישנות (deprecation) אחת ל-stderr. קודי היציאה והפלט ל-stdout נותרים ללא שינוי. יוסר בגרסה הראשית הבאה. |
| משתני סביבה `NETPROBE_*` | `HOSTCENSUS_*` | משתנה `NETPROBE_*` משמש כאשר התאום שלו `HOSTCENSUS_*` אינו מוגדר, עם אזהרה אחת ל-stderr המציינת את שמות המשתנים ולעולם לא את ערכיהם. `HOSTCENSUS_*` גובר כאשר שניהם מוגדרים. יוסר בגרסה הראשית הבאה. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **שינוי שובר תאימות.** לא מותקנת שכבת תאימות (import shim); עדכנו את ה-imports. |
| תגית תמונת Docker `network-discovery:test` (CI בלבד) ומשתמש קונטיינר `netprobe` | `hostcensus:test`, משתמש `hostcensus` | מעולם לא פורסמה תמונה ברישום (registry). בנו את התמונה מחדש והשתמשו ב-entrypoint של `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | קובץ קיים בשם ברירת המחדל הישן עדיין נמצא בשימוש, עם אזהרה, כל עוד השם החדש אינו קיים. נתיבים מפורשים עם `--config` ו-`--history` אינם מושפעים. |
| דוחות ותמונות מצב עם `"format": "netprobe-report"` או `"netprobe-snapshot"`, והשדה `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` ו-`export` עדיין טוענים קבצים שנכתבו תחת השם הישן, וסכמות ה-JSON שפורסמו מקבלות את שני האיותים. קבצים חדשים משתמשים בשמות החדשים. מסדי נתונים של היסטוריית SQLite נותרו ללא שינוי ונטענים כבעבר. |
| סקריפטי Kadupul מתוך `netprobe export` | סקריפטים מתוך `hostcensus export` | סקריפטים ישנים ממשיכים לעבוד ועדיין קוראים את `NETPROBE_SNMP_*` בעת הרצתם. סקריפטים חדשים קוראים את `HOSTCENSUS_SNMP_*`. |

## דוגמה מהירה

הריצו מקונטיינר הבדיקה (tester) של מעבדת האינטגרציה המתוארת תחת פיתוח; הפלט קוצר:

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

## קודי יציאה

| פקודה | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | תצפיות/דוח תועדו | כשל בבדיקת מוכנות (preflight)/מנוע, בהיסטוריה, או בכתיבת דוח/תמונת מצב | יעד, אפשרויות, תצורה או מגבלות לא תקינים | - | הגעה ל-`--deadline`; נכתב דוח חלקי, דילוג על היסטוריה ותמונת מצב |
| `preflight` | הבדיקות עברו | בדיקה מקומית נכשלה | יעד/תצורה לא תקינים או יעדי שמירה מתנגשים | - | - |
| `profiles` | פרופילים מאומתים הוצגו | - | תצורה או בחירה לא קריאים/לא תקינים | - | - |
| `history` | סיכומים הוצגו | היסטוריה חסרה, לא תקינה או לא נתמכת | אפשרויות CLI לא תקינות | - | - |
| `compare` | הופקה השוואה, כולל כאשר קיימים שינויים | היסטוריה לא קריאה, היקף/סדר לא תואמים, או כשל בכתיבה | אפשרויות CLI לא תקינות | - | - |
| `diff` | ללא שינויים | לא ניתן היה לכתוב את קובץ `-o` | קלט חסר, לא קריא או לא נתמך, או סריקה חלקית ללא `--allow-partial` | נמצאו שינויים, תצפיות לא מאומתות, או סריקה חלקית | - |
| `export` | הסקריפט נכתב | לא ניתן היה לכתוב את הסקריפט | קלט לא קריא, סריקה חלקית ללא `--allow-partial`, או נתונים שלא ניתן לייצא בבטחה | - | - |

## מבנה המודולים

| מודול | אחריות |
| --- | --- |
| `cli.py` | אפשרויות שורת פקודה, פתרון פרופילים, בדיקת מוכנות (preflight), סריקה והפקת דוחות |
| `scanner.py`, `probes.py` | הרחבת יעדים, עובדים תחומי-מקביליות, גילוי מארחים ותצפיות שירות |
| `config.py`, `profiles.py` | הגדרות שירותים ופרופילי מלאי מאומתים |
| `models.py`, `output.py` | טיפוסי תוצאות ועיבוד פלט לטרמינל/JSON/CSV |
| `history.py`, `diff.py` | היסטוריית SQLite והשוואות תמונות מצב מנוהלות גרסאות |
| `preflight.py` | בדיקות מקומיות ובירור גרסת Nmap תחום |
| `export.py` | סקריפטי ייבוא ל-Kadupul מאומתים ועם ציטוט תקין (quoted) |

כל תצפית שירות מתעדת את מצבה בנפרד מהזהות המוצהרת שלה. קריאות ומגבלות זמן הן תחומות; חריגות בבדיקות נשמרות בתוך שגיאות המארח. היסטוריית SQLite משתמשת בטרנזקציות, ניקוי חיבורים מפורש, ונתיבי קריאה בלבד להצגה ולהשוואה. סודות SNMP נכנסים רק דרך משתני סביבה או קובצי סודות; היסטוריית המלאי שומרת את ההגדרות הלא-סודיות שבפועל. ראו [ארכיטקטורה](../../../docs/architecture.md) עבור צינור הסריקה, מגבלותיו וגבולות האמון שלו, ו-[SECURITY.md](../../../SECURITY.md#authorized-use) עבור שימוש מורשה.


## שימוש

סרקו אך ורק רשתות שבניהולכם.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| אפשרות | משמעות |
| --- | --- |
| `NETWORK` | כתובת CIDR, IP או שם מארח; אופציונלי עם `--profile`. מזהי היקף (scope identifiers) של IPv6 נדחים. |
| `-o, --output PATH` | כתיבת דוח. הפורמט נקבע לפי הסיומת (`.json`, `.csv`); סיומות אחרות חוזרות כברירת מחדל ל-JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | כפיית פורמט הדוח. ללא השפעה בלי `--output`. `.sh` בוחר ב-`kadupul`. |
| `-v, --verbose` | רישום לוגים ברמת debug. |
| `-q, --quiet` | השתקה של תוצאות, התקדמות ולוגי מידע; אזהרות ושגיאות עדיין מופיעות ב-stderr. |
| `--backend asyncio\|nmap` | גילוי מארחים. `asyncio` (ברירת מחדל) בודק ישירות את פורטי השירות; `nmap` מריץ תחילה סריקת פינג (ping sweep) של nmap ודורש את קובץ ההרצה `nmap` ב-`PATH`. |
| `--timeout SECONDS` | זמן המתנה לבדיקות שאינן קובעות תקציב זמן משלהן (ברירת מחדל 1.0). בדיקות חיבור מובנות משתמשות ב-0.3 שניות אלא אם טבלת השירותים מגדירה `timeout`. |
| `--concurrency N` | מספר בדיקות שרצות במקביל ברגע נתון (ברירת מחדל 256). |
| `--deadline SECONDS` | עצירת הסריקה כולה, כולל סריקת nmap, לאחר פרק זמן זה (ברירת מחדל 3600, לכל היותר 604800; משתנה סביבה `HOSTCENSUS_DEADLINE`). מארחים שהסתיימו נכתבים לדוח עם `"complete": false`, לא נכתבת היסטוריה או תמונת מצב, ו-`scan` יוצא עם קוד 4. |
| `--config PATH` | הגדרות שירותים ב-TOML והגדרות `[profiles]` אופציונליות בעלות שם. |
| `--profile NAME` | שימוש בפרופיל בעל שם; ברירת המחדל היא `hostcensus.toml` כאשר `--config` מושמט. |
| `--exclude IP/CIDR` | הוספת החרגה; ניתן לחזור לפי הצורך. מארח IPv4 מוחרג מחריג גם את כתובות ה-IPv6 המגיעות אליו: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) ו-6to4. יעדים והחרגות מסוג IPv4-mapped מטופלים ככתובות ה-IPv4 שאותן הם מייצגים. |
| `--max-hosts N` | מגבלת כתובות הנבדקת לפני החרגות (ברירת מחדל/מקסימום קשיח 65,536). |
| `--history PATH` | תיעוד הסריקה שהושלמה במסד נתונים אופציונלי (opt-in) של היסטוריית SQLite. |
| `--services NAMES` | רשימה מופרדת בפסיקים של שמות שירותים לבדיקה, בסדר זה (ברירת מחדל: הכול). |
| `--ports SPEC` | רשימה מופרדת בפסיקים של `NAME=PORT` (הזזת שירות) או `PORT` (הוספת בדיקת TCP פשוטה בשם `tcp-PORT`). |
| `--snmp-community-file PATH` | קובץ המכיל את מחרוזת ה-community של SNMPv2c לשאילתת ה-MIB של המערכת. משתני סביבה: `HOSTCENSUS_SNMP_COMMUNITY` (הערך) או `HOSTCENSUS_SNMP_COMMUNITY_FILE` (הנתיב). |
| `--snmp-user` | משתמש SNMPv3. משתנה סביבה: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (ברירת מחדל), `SHA224`, `SHA256`, `SHA384`, `SHA512` וקובץ המכיל את סיסמת האימות. משתני סביבה: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` או `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (ברירת מחדל), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` וקובץ המכיל את סיסמת ההצפנה. משתני סביבה: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` או `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | כתיבת תמונת מצב מנוהלת גרסאות נוספת עבור `hostcensus diff`. |
| `--tls-ca-file PATH` | אימות תעודות HTTPS מול חבילת PEM זו במקום מול מאגר המערכת. משתנה סביבה: `HOSTCENSUS_TLS_CA_FILE`. |

כברירת מחדל, כל מארח נבדק עבור SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) ו-HTTPS (TCP 443). פורטי TCP נבדקים באמצעות חיבור מלא (full connect). SNMP נבדק באמצעות בקשת SNMPv3 engine-discovery, שכל סוכן SNMPv3 חייב לענות עליה ללא פרטי אימות; סוכנים המדברים v1/v2c בלבד לא יזוהו בבדיקה זו. עם מנוע asyncio, מארח נחשב חי (alive) כאשר בדיקה כלשהי מקבלת מענה, כולל חיבור שנדחה, כך שלמארח שמשמיט (drops) כל בדיקה יש `alive=false` והשגיאה `"Host is down"`; אין בכך הוכחה שהוא כבוי פיזית. עם `--backend nmap`, nmap קובע אילו מארחים חיים (ICMP כ-root, ו-TCP 80/443 אחרת).

### טביעות אצבע של שירותים

כל שירות פתוח מזוהה לפי טביעת אצבע מתוך מה שהוא שולח לפני כל התחברות. דבר אינו מאמת זהות מלבד שאילתת SNMP, וזאת רק כאשר אתם מספקים פרטי אימות.

| בדיקה | מה נקרא | `version` | מפתחות `details` |
| --- | --- | --- | --- |
| `ssh` | שורת זיהוי לפי RFC 4253 | תוכנה, לדוגמה `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | לחיצת יד ראשונית של MySQL/MariaDB | גרסת שרת | `server_version`, `flavor`, `auth_plugin`, או `error_code`/`error` |
| `http` | תגובת `HEAD /` | כותרת `Server` | `status`, `server` |
| `https` | לחיצת יד TLS, תעודה, `HEAD /` | כותרת `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | גילוי SNMPv3; עם פרטי אימות, בקשת GET ל-sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; עם פרטי אימות `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, או `snmp_error` |

שם מארח כיעד נפתר (resolved) פעם אחת לכל מארח וכל בדיקה מתחברת לכתובת זו, המתועדת כ-`address` בתוצאות; השם משמש רק עבור TLS SNI, אימות תעודה וכותרת `Host` של HTTP. שם שאינו נפתר מניב מצבי `unknown` ושגיאת `Cannot resolve`. שמות DNS הפוכים (Reverse DNS) נשמרים רק כאשר הם מכילים תווי שם מארח, ולכל היותר 16 חיפושים רצים בו-זמנית. HTTPS משתמש באימות תעודה ושם מארח מול מאגר המערכת או מול `--tls-ca-file`. מאגר האמון נטען פעם אחת עבור הסריקה ונעשה בו שימוש חוזר לכל בדיקת HTTPS. חיבור ה-TCP ולחיצת היד של TLS נמדדים בזמן בנפרד, כך שפורט שמקבל חיבורים אך תוקע את לחיצת היד מסומן כ-`open` עם `tls_error`, ולא כ-`filtered`. אם האימות נכשל, התוצאה מתעדת `cert_verified: false` ו-`cert_verify_error`; היא אינה מנסה שוב עם הגדרות חלשות יותר ואינה שולחת בקשת HTTP. פרטי התעודה וכותרות HTTP נאספים רק לאחר שהאימות מצליח. ספקו את חבילת ה-CA הנכונה עבור שירותים עם CA פרטי. דוחות ישנים יותר עשויים להכיל `cert_read_unverified`, שבדיקות נוכחיות אינן מפיקות עוד.

סודות SNMP נקראים רק ממשתני סביבה או מקבצים (`--snmp-*-file`, או משתנה `HOSTCENSUS_SNMP_*_FILE` התואם), לעולם לא מערכים בשורת הפקודה, שמשתמשים מקומיים אחרים יכולים לראות ברשימת התהליכים. `--snmp-community`, `--snmp-auth-key` ו-`--snmp-priv-key` עם ערך יוצאים עם קוד 2 ומציינים את הדגל החלופי. קובץ סוד חייב להיות UTF-8 לא ריק באורך של עד 4096 בתים; תו שורה חדשה אחד בסוף מתעלם, והגדרה של משתנה וקובץ יחד עבור אותו סוד היא שגיאה. שגיאות מציינות את שם הקובץ אך לעולם אינן מדפיסות את תוכנו. דוחות סריקה והיסטוריה אינם כוללים במתכוון ערכי פרטי אימות. למייצא יש אפשרות נפרדת ומפורשת `--include-credentials` המתוארת להלן. מחרוזת community בוחרת SNMPv2c; משתמש בוחר SNMPv3, עם אימות כאשר ניתן מפתח אימות ועם הצפנה (privacy) כאשר ניתנים שני המפתחות (`snmp_security_level` מתעד איזה מהם). hostcensus מסרב, עם קוד יציאה 2, לשלב community עם משתמש v3, להשתמש במפתח הצפנה ללא מפתח אימות, או להשתמש במפתחות ללא משתמש, והוא לעולם אינו מנסה שוב שאילתת v3 שנכשלה עם v2c או עם רמת אבטחה נמוכה יותר. סוכנים המדברים v1/v2c בלבד מתעלמים מגילוי v3 נטול פרטי האימות, ולכן הם מופיעים כפתוחים רק כאשר מסופקת מחרוזת community.

טקסט באנר מצומצם לתווים ניתנים להדפסה ומוגבל ל-256 תווים לפני שמירתו או הצגתו. גם קריאות תחומות: 4 KiB לשורה, 4 KiB לברכת פתיחה של MySQL, ו-16 KiB של כותרות HTTP. מזהה מנוע (engine ID) של SNMP שאורכו עולה על 32 אוקטטות נחתך לפני שמירתו. HTTP ו-HTTPS שולחים כותרת Host עם כתובת IPv6 בסוגריים מרובעים ועם הפורט כאשר אינו 80 או 443. תאי CSV שמתחילים בטריגר של נוסחת גיליון אלקטרוני מקבלים קידומת כדי שהתא יישאר טקסט.

### מגבלות

הרצה אחת מקבלת לכל היותר 65,536 כתובות, 64 שירותים ו-524,288 בדיקות (מארחים כפול שירותים); בקשות גדולות יותר יוצאות עם קוד 2 לפני שנשלחת תעבורה כלשהי. `--concurrency` מוגבל ל-4096 sockets. לכל בדיקה יש מגבלת זמן קשיחה של פי ארבעה מתקציב הזמן שלה עצמה. בדיקות חיבור (`tcp`, `ssh`, `mysql`, `http`) משתמשות ב-0.3 שניות אלא אם אותו שירות מגדיר `timeout`. SNMP ו-HTTPS משתמשים ב-`--timeout` (ברירת מחדל 1.0) כאשר אינם מגדירים ערך משלהם. בדיקה המגיעה למגבלת הזמן מדווחת כ-`unknown` עם `"probe timed out"` בתוך `errors`. כשלי socket מקומיים (לדוגמה, מיצוי מתארי קבצים) מדווחים גם הם כ-`unknown` כשהשגיאה מתועדת; הם לעולם אינם נחשבים כפורט מסונן (filtered) או כמארח כבוי. לפני הבדיקות, hostcensus מעלה את המגבלה הרכה (soft limit) של קבצים פתוחים לכיוון המגבלה הקשיחה כדי להכיל את `--concurrency` ועוד 64 מתארים; כאשר אינו יכול לעשות זאת, בדיקת המוכנות `open files` נכשלת ו-`scan` יוצא עם קוד 1 לפני שליחת תעבורה. גילוי Nmap משתמש במגבלת זמן של 30 שניות למארח. קידומת מועברת אל nmap בצורת CIDR, וסריקה נכשלת עם קוד יציאה 1 כאשר nmap מדווח על פחות כתובות מאלו שניתנו לו (לדוגמה, שם שאינו יכול לפתור) במקום לסמן מארחים ככבויים. שם מארח כיעד נפתר פעם אחת ו-nmap מקבל כתובת זו, כך שהגילוי והבדיקות מגיעים לאותה מכונה. קידומת מלאה היא תהליך nmap יחיד שמגבלת הזמן של תת-התהליך שלו היא 35 שניות עבור כל 256 כתובות, מעוגל כלפי מעלה. סריקות עם החרגות משתמשות באצוות (batches) של 256 מארחים ובמגבלת זמן של 35 שניות לכל אצווה. יצירת עובדים (workers) תחומה ללא תלות בגודל הטווח. ל-Reverse DNS ולפתרון שמות מארחים יש מגבלת זמן נפרדת של שתי שניות; קריאת resolver שלעולם אינה חוזרת ננטשת על ה-thread שלה, כך שאינה יכולה להשאיר את hostcensus רץ מעבר למגבלות אלו. לכל היותר 16 חיפושים רצים במקביל, וקריאה שננטשה שומרת על המשבצת (slot) שלה עד שהיא חוזרת, כך שמספר ה-threads התקועים נשאר תחום; אם כל ה-16 נתקעים, חיפושים מאוחרים יותר ממתינים בתור למשבצת מחוץ למגבלת הזמן של שתי השניות (שמתחילה ברגע שמשבצת מתפנה) עד ש-`--deadline` עוצר את הסריקה. `NetworkScanner` בשימוש כספרייה ללא `deadline` עלול להמתין למשבצת כזו ללא הגבלת זמן. `--deadline` (ברירת מחדל שעה אחת) תוחם את ההרצה כולה מעבר למגבלות אלו.

### הגדרת שירותים

ניתן לשנות שירותים באמצעות קובץ TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` הוא אחד מבין `tcp`, `ssh`, `mysql`, `http`, `https` או `snmp` וברירת המחדל שלו היא שם השירות כאשר זהו שם של בדיקה, אחרת `tcp`. רק `snmp` משתמש ב-UDP. שמות שירותים מורכבים מאותיות קטנות באנגלית, ספרות, `-` ו-`_`. שני שירותים אינם יכולים לחלוק פורט ופרוטוקול; ההיסטוריה מתעדת מצב אחד עבור זוג זה. `timeout` הוא אופציונלי, בשניות, ולפחות 0.05. בדיקות בסגנון חיבור (`tcp`, `ssh`, `mysql`, `http`) משתמשות כברירת מחדל ב-0.3 שניות. `snmp` ו-`https` משתמשים ב-`--timeout` של הסריקה כאשר השירות אינו מגדיר `timeout`. `--timeout` אינו מחליף תקציב שכבר מוגדר לשירות.

דוחות JSON הם מסמכים מנוהלי גרסאות (`"format": "hostcensus-report"`, `"version": 1`) המתעדים את היעד, השירותים שנבדקו וההגדרות לצד `devices`; `--format json` ללא `-o` כותב את הדוח ל-stdout במקום הטבלה. לכל פלט JSON יש סכמה מפורסמת; ראו [פלט JSON](../../../docs/json-output.md). מכשירים שומרים על השדות המקוריים `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` ו-`errors` ומוסיפים רשימת `services` עם `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, או `unknown` כאשר הבדיקה נכשלה מקומית או הגיעה למגבלת הזמן שלה), `version` ו-`details` של כל בדיקה. פלט CSV מקבל עמודות נגררות `services` ו-`versions` עבור השירותים הפתוחים. השדות הבוליאניים `ssh`, `snmp` ו-`mysql` עוקבים אחר השירותים בעלי שמות אלה בדיוק.


## פרופילי מלאי, בדיקת מוכנות והיסטוריה מקומית

פרופילים בעלי שם חולקים קובץ TOML עם הגדרות `[services]` הקיימות. העתיקו את [hostcensus.example.toml](../../../hostcensus.example.toml) אל `hostcensus.toml` והגדירו רשתות שבניהולכם:

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

`preflight` פותר אפשרויות ופרופילים בדיוק כפי ש-`scan` עושה, כולל `--concurrency` לבדיקת הקבצים הפתוחים, כך ש-preflight עובר פירושו ש-`scan` יתחיל עם אותה תוכנית.

פרופילים מקבלים `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency` ו-`max_hosts`. `services` ו-`ports` משתמשים בתחביר הקיים של רשימה מופרדת בפסיקים. אפשרויות CLI מפורשות גוברות על הגדרות הפרופיל; אפשרויות `--exclude` חוזרות מתווספות להחרגות הפרופיל. רשת מפורשת עם `--profile` חייבת להיות מוכלת בהיקף ה-IP/CIDR של אותו פרופיל. שמות מארחים נותרים נתמכים עבור סריקות ישירות, אך לא ניתן לשלבם עם החרגות IP. מגבלות מארחים חלות לפני החרגות; תקרת הבדיקות הכוללת עדיין חלה לאחר מכן. מארחים מוחרגים מושמטים הן מבדיקות השירות והן מגילוי Nmap האופציונלי.

כל סריקה מבצעת בדיקות מוכנות מקומיות לפני תעבורה אל היעד: מגבלות יעד/בדיקה, גישה ליעד השמירה, זמינות קובץ הרצה/מעטפת אופציונליים של Nmap, סכמת היסטוריה וחבילת TLS CA מוגדרת. `preflight` מדווח ב-JSON ואינו סורק יעדים או יוצר מסד נתונים של היסטוריה. הוא כותב זמנית קובץ אח (sibling file) כדי לבדוק גישת כתיבה ליעד מבלי לשנות תוכן קיים. מנוע ברירת המחדל asyncio עדיין אינו דורש לא Nmap ולא הרשאות root. נתיבי יעד חייבים להיות נפרדים זה מזה ומתצורת הקלט, כולל קישורים קשיחים (hard links); קישורים סמליים (symlinks) כיעדי פלט נדחים. בדיקות שנכשלות מחזירות 1; היקף/תצורה לא תקינים מחזירים 2.

כתיבת דוחות וייצוא דורשות תמיכה ב-`O_NOFOLLOW`. בפלטפורמות בלעדיה, כולל Windows, כתיבות אלו נכשלות מבלי לפתוח או לקצוץ (truncate) את היעד. דוחות וסקריפטי יייצוא חדשים נוצרים להרשאות בעלים בלבד (mode 0600); החלפת קובץ קיים משמרת את הרשאותיו. כתיבה אל צינור בעל שם (named pipe) ללא קורא נכשלת מיד במקום להמתין. מסד נתונים חדש של `--history` נוצר אף הוא לבעלים בלבד; מסד נתונים קיים שומר על ההרשאות שלו. הודעות לוג תמיד מופנות ל-stderr, כך ש-stdout נושא תוצאות בלבד. ייצואים המכילים פרטי אימות כופים תמיד mode 0600.

ההיסטוריה היא opt-in ומשלימה את תמונות המצב ב-JSON ואת הפקודה `diff` הקיימים:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

השתמשו במזהים (IDs) מתוך `history`; הדוגמה מניחה מסד נתונים חדש. תמונות מצב נשמרות באופן טרנזקציוני עם זמני התחלה/סיום ב-UTC, גרסת חבילה, הגדרות לא-סודיות שבפועל, סיכומים וכל תצפיות המארח/שירות, כולל שגיאות לפי מארח. תצפיות מארח חלקיות נשמרות. הרצות שבוטלו אינן נשמרות. חוזי קודי היציאה הקיימים של דוח, תמונת מצב, ייצוא וסריקה נשמרים.

`history` מציג סיכומי JSON מבלי לקרוא את כל מטעני המכשירים ההיסטוריים. `compare` קורא שתי סריקות שמורות, דורש זהויות יעד ופורטים נבחרים זהים, ומדווח על שינויים בזמינות תגובה, במצב ובמצבי פורטים. מזהה הסריקה המוקדמת יותר חייב לקדם למזהה המאוחר יותר. כאשר שתי הסריקות תיעדו `timeout` או `backend` וערכים אלו שונים, הדוח מציג אזהרה ועדיין משווה את התצפיות. זמן המתנה שונה עלול לגרום לפורט מסונן להיראות פתוח. שגיאות סורק ותצפיות פורט במצב `unknown` מסומנות כלא ודאיות במקום להיות מטופלות כהיעלמות או סגירה מאומתות: מארחים עם שגיאות מופיעים תחת `uncertain_hosts`, וכל מעבר מצב של פורט המערב `unknown` (כולל `unknown` בשתי הסריקות) רשום תחת `unconfirmed_ports` במקום `port_changes`, למעט פורט שפתוח בסריקה המאוחרת יותר, המוגדר כשינוי פורט. `compare` ו-`diff` מסווגים פורטים לפי אותו כלל. `no_longer_responding` משמעו היעדר תגובה, לא הוכחה להסרת המכשיר. קוד יציאה 0 של סריקה אינו מבטיח שכל מארח הגיב: בדקו את השגיאות לפי מארח. השלמת השוואה בהצלחה מחזירה 0 בין אם קיימים שינויים ובין אם לא; פקודת `diff` הקיימת לקבצים שומרת על חוזה קוד יציאה 3 שלה. היסטוריה לא נתמכת או פגומה מחזירה 1.

ההיסטוריה שומרת מידע מלאי, לכן בחרו תיקייה מקומית מוגנת כראוי. קובצי פרופיל והגדרות שמורות אינם מכילים פרטי אימות של SNMP; הטיפול בפרטי אימות ממשיך דרך אפשרויות זמן הריצה/משתני הסביבה הקיימים.

## השוואת מלאי (Inventory diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

תמונת מצב היא קובץ JSON עם `format: "hostcensus-snapshot"`, `version: 1`, גרסת hostcensus, זמן היצירה ב-UTC, היעד, ה-`timeout` וה-`backend` של הסריקה כאשר הסריקה תיעדה אותם, השירותים שנבדקו, והמארחים החיים באותו מבנה כמו דוח `-o`. מארחים כבויים מושמטים. `diff` מקבל גם דוחות JSON רגילים של `scan -o`, כולל דוחות מלפני שהשדה `services` היה קיים.

`diff` מדווח על מארחים חדשים ונעלמים, פורטים שנפתחו או נסגרו במארחים הקיימים בשתי הסריקות, ושירותים שערך ה-`version` שלהם השתנה. פורטים שנבדקו רק באחת משתי הסריקות אינם מושווים, ואזהרה מציינת זאת. תצפיות כושלות לעולם אינן מפורשות כ"ללא שינוי": פורט שמצבו `unknown` באחת הסריקות ואינו פתוח בסריקה המאוחרת יותר מופיע תחת `unconfirmed`, ולא תחת `closed`, עם ערך `before` של `open`, `unknown` או `not-open` (נבדק ונמצא סגור או מסונן) ו-`after` של `unknown` או `not-open`; פורט שפתוח כעת מדווח תחת `opened` גם אם הבדיקה הקודמת נכשלה. מארח שכל בדיקותיו נכשלו ללא מענה באחת משתי הסריקות מופיע תחת `unsettled_hosts` (עם `before`/`after` של `up`, `uncertain` או `absent`, כולל כאשר נכשל בשתי הסריקות או חסר מהקובץ השני) במקום `vanished_hosts`; אם הוא עונה בסריקה המאוחרת יותר הוא מדווח גם כמארח חדש עם הפורטים הפתוחים שלו. תמונות מצב שומרות מארחים כושלים אלו מסיבה זו. אזהרה מופיעה גם כאשר היעדים שונים, וכאשר שני הקבצים תיעדו timeout או backend וערכים אלו שונים. `-o PATH` כותב גם את גרסת ה-JSON לקובץ.

דוח מסריקה שנעצרה על ידי `--deadline` (`"complete": false`) מפרט רק את המארחים שאליהם הגיעה, ולכן `diff` ו-`export` דוחים אותו עם קוד יציאה 2. `--allow-partial` מקבל אותו עם אזהרה ל-stderr: במקרה זה `diff` מפרט מארחים שהסריקה החלקית כלל לא ציינה תחת `unsettled_hosts` בתור `unscanned` במקום נעלמים (מארח שהיא רשמה ככבוי עדיין נחשב נעלם), מגדיר את `partial` ל-true ולעולם אינו מדווח על היעדר שינוי, ו-`export` כותב אזהרה לתוך כותרת הסקריפט.

קודי היציאה של `diff`: `0` ללא שינויים, `3` נמצאו שינויים, תצפיות שלא ניתן היה לאמת, או קלט חלקי (`changed` הוא true בכל פעם שרשימה כלשהי, כולל `unsettled_hosts` ו-`unconfirmed`, אינה ריקה, או ש-`partial` הוא true), `2` קובץ חסר, לא קריא, אינו תמונת מצב נתמכת, או חלקי ללא `--allow-partial`, `1` לא ניתן היה לכתוב את קובץ `-o`.

## ייצוא ל-Kadupul

ל-[Kadupul](https://github.com/kadupulhq/kadupul) (מזלג של Cacti 1.2.31) אין ייבוא המוני מקובץ מכשירים. הדרך הנתמכת להוסיף מכשירים מסקריפט היא `cli/add_device.php`, מכשיר אחד בכל קריאה, עם ארגומנטים מסוג `--option=value`. `hostcensus export` כותב סקריפט POSIX `sh` של קריאות אלו:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

כל מארח חי הופך ל-`php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- מארחים שבהם שאילתת ה-SNMP של הסריקה הצליחה מקבלים `--version=2 --community=...` או `--version=3 --username=... --authproto=... --password=...` (ועוד `--privproto`/`--privpass` עבור authPriv), `--port` ו-`--avail=snmp`. ייצוא SNMPv3 דורש `--snmp-user`, ו-noAuthNoPriv נדחה משום ש-`add_device.php` דורש סיסמת v3.
- מארחים אחרים מקבלים `--version=0 --avail=ping`, עם `--ping_method=tcp --ping_port=` כפורט ה-TCP הפתוח הראשון, או ICMP אם אין כזה.
- `--notes` מפרט את השירותים והגרסאות הפתוחים. `--description` הוא שם ה-reverse-DNS כאשר הוא פשוט (אותיות, ספרות, `.`, `_`, `-`), אחרת כתובת ה-IP, והוא הופך לייחודי, משום ש-`add_device.php` מתייחס לתיאור קיים כעדכון של אותו מכשיר.

כל ערך מאומת ומצוטט ל-shell באמצעות `shlex.quote`. כברירת מחדל לא נכתב שום סוד SNMP: הסקריפט מרחיב את `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` או `HOSTCENSUS_SNMP_PRIV_KEY` בזמן ריצה ונעצר אם אחד מהם אינו מוגדר. `--include-credentials` כותב במקום זאת את הערכים מאותם משתני סביבה לתוך הסקריפט, יוצר אותו עם mode 0600, ורושם אזהרה. `add_device.php` עצמו מדפיס את ה-community ומקבל סודות כארגומנטים, החשופים ברשימת התהליכים של שרת Kadupul בזמן שכל קריאה רצה.

`add_device.php` יוצא עם קוד 1 עבור כפילויות ושגיאות; הסקריפט ממשיך, סופר כשלים ויוצא עם קוד 1 אם מכשיר כלשהו לא נוסף. מזהי תבניות (template ids) מגיעים מ-`php cli/add_device.php --list-host-templates`. קודי היציאה של `export`: `0` נכתב, `2` קלט לא קריא, סריקה חלקית ללא `--allow-partial`, או נתונים שלא ניתן לייצא בבטחה, `1` לא ניתן היה לכתוב את הסקריפט.

## ניהול גרסאות ותהליך שחרור

hostcensus פועל לפי [Semantic Versioning](https://semver.org/spec/v2.0.0.html): תיקונים תואמים מעלים את גרסת ה-patch, תכונות תואמות/התראות התיישנות מעלות את גרסת ה-minor, ושינויים שוברי תאימות מעלים את גרסת ה-major. פקודות ואפשרויות, קודי יציאה וסכמות ה-JSON הם החוזה הציבורי; התנהגות שהוכרזה כמיושנת ממשיכה לעבוד עד הגרסה הראשית הבאה, אלא אם תיקון אבטחה מחייב לשנותה מוקדם יותר (ואז יומן השינויים מסביר מדוע).

release-please פותח release PR מכותרות ה-Conventional Commit ב-`main`, ומקדם את `pyproject.toml`, `uv.lock` ו-`CHANGES.md`. מיזוג שלו יוצר את התגית `vMAJOR.MINOR.PATCH` וטיוטת שחרור ב-GitHub, שאליה CI מצרף wheel שנבדק, הפצת קוד מקור (source distribution) וסיכומי ביקורת (checksums); GitHub שומר build attestations לקבצים אלו דרך ה-attestations API שלו. מתחזק סוקר ומפרסם את הטיוטה ברגע שהקבצים מצורפים. שחרורים לעולם אינם מוחלפים.

פרסום מהימן (trusted publishing) ל-PyPI הוא opt-in ודורש בעלות על הפרויקט, מפרסם מהימן (trusted publisher) וסביבת `pypi`. הוא מפרסם את אותם ארטיפקטי שחרור שנבדקו מבלי לבנות מחדש או לשמור אסימון API. שחרורים מתויגים במאגר ציבורי זה מייצרים artifact attestations של GitHub; מזלגות פרטיים דורשים תוכנית נתמכת ו-opt-in מפורש. ראו את [מדריך השחרור המלא](../../../docs/releasing.md) עבור הגדרות, פקודות מדויקות וניסיונות חוזרים.

## פיתוח

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

כלי פיתוח נמצאים בקבוצות תלויות של [PEP 735](https://peps.python.org/pep-0735/) בקובץ `pyproject.toml` (`dev`, `fuzz`, `build`), כך שלעולם אינם מופיעים במטא-דאטה של החבילה המפורסמת. `uv.lock` הוא קובץ הנעילה היחיד; CI מתקין עם `uv sync --locked` ונכשל כאשר קובץ הנעילה אינו מעודכן. בחרו את המפרש (interpreter) באמצעות `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), או כל Python 3.12+.

CI אוכף רף כיסוי (coverage floor) של 90% לחבילה. בדיקות יחידה כוללות שרתי loopback מבוקרים ומקרי בדיקה אופליין של פרופילים/היסטוריה/מאמת-שחרור; מעבדת ה-Compose מריצה OpenSSH, MariaDB, nginx ו-net-snmp על גשר מבודד. הריצו אותה באמצעות `make test-integration`. ראו [CONTRIBUTING.md](../../../CONTRIBUTING.md) ו-[כלי שחרור](../../../scripts/README.md).

קונטיינר זמן הריצה פועל כ-UID/GID 10001 ללא תיקיית בית, ללא התחברות ל-shell וללא pip, ויכול לכתוב אל `/app/output`. תנו למשתמש זה גישת כתיבה לכל תיקיית פלט שמחוברת (mounted). הוא אינו זקוק ליכולות מיוחדות (capabilities) ועובד עם מערכת קבצים שורש לקריאה בלבד, כך שניתן להריצו כך:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap משתמש בהתנהגות גילוי ה-TCP חסרת ההרשאות שלו בקונטיינר זה. CI מכשיל את בניית התמונה על כל פגיעות ברמת HIGH או CRITICAL הניתנת לתיקון ש-Trivy מדווח עליה.

## בדיקות שרשרת אספקה

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) רץ ב-main וכן מדי שבוע, מפרסם את הציון האמיתי שלו ומעלה ממצאים אל סריקת הקוד של GitHub. Actions ובסיסי קונטיינרים מוצמדים לפי גיבובים (hashes) בלתי ניתנים לשינוי; תלויות Python נפתרות בקובץ `uv.lock`. כשלים של Bandit מכשילים את ה-CI, ו-fuzzing תחום של Atheris מפעיל את המנתחים של SSH, MySQL, HTTP, תעודות ו-SNMPv3 BER ללא גישה לרשת.

Scorecard מודד גם פעילות סקירת קוד היסטורית, גיוון תורמים ומקור שחרורים (release provenance). ציונים אלו משקפים ראיות בפועל; הם אינם טענה שכל בדיקת ממשל או שחרור היסטורי מתקיימת. ראו [SECURITY.md](../../../SECURITY.md) ו-[מקור שחרורים](../../../docs/releasing.md).

## לוקליזציה

הודעות CLI וטבלאות סיכום/diff בטרמינל תומכות ב-45 אזורים ושפות (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ללא כל תלויות זמן ריצה נוספות. בחירת השפה מכבדת את `--lang`, ולאחר מכן את `LC_ALL`, `LC_MESSAGES` ו-`LANG`, עם חזרה ל-`en`. סכמות JSON, עמודות CSV וסקריפטי ייצוא נותרים ללא שינוי בכל השפות.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## תרומה לפרויקט

תרומות צריכות לכלול מקרה ניתן לשחזור, לשמר את חוזי ה-CLI ופורמטי הנתונים המתועדים, ולעבור את בדיקות האיכות שלעיל. ראו [CONTRIBUTING.md](../../../CONTRIBUTING.md) עבור תהליך הפיתוח ו-[מדריך השחרור](../../../docs/releasing.md) עבור החלטות תאימות וניהול גרסאות.

## אבטחה ומצב רישיון

ראו [SECURITY.md](../../../SECURITY.md) לדיווח פרטי ולגרסאות נתמכות. hostcensus מורשה תחת [רישיון MIT](../../../LICENSE).

כותרות קוד המקור משתמשות במזהי SPDX ומשמרות קרדיטים של תורמים מהיסטוריית ה-Git. ראו [AUTHORS.md](../../../AUTHORS.md) לייחוס. לכידות בדיקה בינאריות וקובץ הנעילה המיוצר משתמשים בקובצי `.license` סמוכים; נוסח ה-MIT נמצא ב-`LICENSES/MIT.txt`.
