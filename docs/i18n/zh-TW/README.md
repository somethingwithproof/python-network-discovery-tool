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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · **繁體中文** · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus 是一款 Python 命令列工具，用於在您管理的網路上執行可重複的服務盤點作業。它可以記錄裝置對外提供的服務、跨時間比對觀測結果，並產生 Kadupul 匯入指令碼。預設後端使用不需要 root 權限的 asyncio Socket；選用的 Nmap 探索功能則可識別設定服務連接埠以外的主機。

## 為什麼選擇 hostcensus

單次的連接埠報告無法說明下一次觀測時究竟是發生了變更，還是單純探測失敗。hostcensus 結合了明確的服務狀態、有上限的探測作業、可重複使用的掃描設定檔以及本地歷史紀錄。維運人員可以重複執行相同的掃描範圍、檢視錯誤資訊，並區分不確定的觀測結果與已確認的變更。

- **服務佐證資訊：**SSH 識別字串、MySQL 問候封包、HTTP 標頭、TLS 憑證觀測結果，以及 SNMP 探索或使用驗證憑證的 system-MIB 查詢。
- **可重複的掃描範圍：**具名的 TOML 設定檔、可疊加的排除清單、可組態的服務項目、主機與探測次數上限，以及受限的並行工作數量。
- **送出流量前的檢查：**本地預檢會驗證掃描目標、工具可用性、輸出目標存取權限、歷史資料庫結構描述，以及設定的 TLS CA 憑證套件。
- **盤點歷史紀錄：**交易式 SQLite 快照會保留所有觀測結果；比對作業會持續顯示掃描器錯誤與未知狀態。
- **互通的輸出格式：**終端機表格、JSON 與 CSV 報告、版本化檔案快照，以及 Kadupul 匯入指令碼。

CI 涵蓋 Linux 與 macOS 上的 Python 3.12、3.13 與 3.14，外加一個受控的 Compose 整合測試環境。程式碼採用現代化的型別別名、強型別預檢結果、僅限關鍵字引數的 slotted 設定檔以及結構化非同步清理機制，同時維持對上述執行階段版本的相容性。如需了解 SemVer 相容性契約與 GitHub 發行流程，請參閱[版本控制與發行流程](../../../docs/releasing.md)。發行徽章顯示的是已發布的產出物，而非目前簽出版本：目前的最新發布標籤為 `v0.3.0`，而此簽出版本使用的套件版本為 `3.0.0`。請從此簽出版本安裝，以使用此處文件所記載的盤點功能。

請先閱讀[安裝](#install)，接著參閱[設定檔與歷史紀錄](#inventory-profiles-preflight-and-local-history)。如需整合細節，請參閱[服務指紋辨識](#fingerprints)、[檔案比對](#inventory-diff)以及[匯出至 Kadupul](#kadupul-export)。

## 安裝

需要 Python 3.12 或更新版本；測試矩陣涵蓋 Python 3.12 至 3.14。請從此簽出版本安裝鎖定的執行階段相依套件：

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

若要使用選用的 Nmap 主機探索功能，請透過您平台的套件管理員安裝 Nmap 執行檔；不需要額外的 Python 套件。Nmap 的 XML 輸出會由核心相依套件 defusedxml 進行剖析，因此會拒絕實體擴展。hostcensus 會直接使用固定引數清單執行 `PATH` 上找到的 `nmap`，並搭配隨前置長度增長的期限以及 64 MiB 的輸出上限。預設後端不需要 Nmap。

## 從 netprobe 遷移

hostcensus 是 netprobe 在 3.0.0 版發布後的新名稱。本專案從未以任一名稱發布至 PyPI，因此安裝皆來自原始碼簽出版本或 GitHub 發行版。GitHub 儲存庫則維持原名稱。

| 舊稱 | 現稱 | 相容性 |
| --- | --- | --- |
| 發行套件 `netprobe` | `hostcensus` | 請從簽出版本重新安裝；不再提供舊名稱套件。 |
| `netprobe` 指令 | `hostcensus` | `netprobe` 仍可執行，並在 stderr 印出一行淘汰警告。結束代碼與 stdout 維持不變，將於下一個主要版本移除。 |
| `NETPROBE_*` 環境變數 | `HOSTCENSUS_*` | 當對應的 `HOSTCENSUS_*` 變數未設定時，會使用 `NETPROBE_*` 變數，並在 stderr 印出一行警告（僅列出變數名稱，絕不印出其值）。兩者皆有設定時，以 `HOSTCENSUS_*` 優先。將於下一個主要版本移除。 |
| `import netprobe`、`python -m netprobe` | `import hostcensus`、`python -m hostcensus` | **破壞性變更。** 未安裝匯入相容層，請更新匯入陳述式。 |
| Docker 映像檔標籤 `network-discovery:test`（僅限 CI）與容器使用者 `netprobe` | `hostcensus:test`、使用者 `hostcensus` | 從未發布至任何映像檔登錄庫。請重新建置映像檔並改用 `hostcensus` 進入點。 |
| `netprobe.toml`、`netprobe-history.sqlite3` | `hostcensus.toml`、`hostcensus-history.sqlite3` | 當新名稱檔案不存在時，仍會繼續使用舊預設名稱的現有檔案並顯示警告。明確指定的 `--config` 與 `--history` 路徑不受影響。 |
| 帶有 `"format": "netprobe-report"` 或 `"netprobe-snapshot"` 以及 `netprobe_version` 欄位的報告與快照 | `hostcensus-report`、`hostcensus-snapshot`、`hostcensus_version` | `diff` 與 `export` 仍可載入舊名稱寫入的檔案，且已發布的 JSON Schema 同時接受兩種拼法。新檔案會使用新名稱。SQLite 歷史資料庫未變更，可照常載入。 |
| 由 `netprobe export` 產生的 Kadupul 指令碼 | 由 `hostcensus export` 產生的指令碼 | 舊指令碼仍可正常運作，且執行時仍會讀取 `NETPROBE_SNMP_*`。新指令碼則讀取 `HOSTCENSUS_SNMP_*`。 |

## 快速範例

於「開發」章節所述整合測試環境的 tester 容器中執行；輸出經過精簡：

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

## 結束代碼

| 指令 | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | 已記錄觀測結果與報告 | 預檢/後端失敗，或歷史資料庫與報告/快照寫入失敗 | 無效的目標、選項、組態或上限設定 | - | 已達 `--deadline`；已寫入部分報告，略過歷史紀錄與快照 |
| `preflight` | 檢查通過 | 本地檢查失敗 | 無效的目標/組態或輸出路徑衝突 | - | - |
| `profiles` | 已列出通過驗證的設定檔 | - | 無法讀取或無效的組態或選取項目 | - | - |
| `history` | 已列出摘要 | 歷史資料庫遺失、無效或不支援 | 無效的命令列選項 | - | - |
| `compare` | 已產生比對結果（包含有變更的情況） | 無法讀取歷史資料庫、範圍/順序不相容或寫入失敗 | 無效的命令列選項 | - | - |
| `diff` | 無變更 | 無法寫入 `-o` 檔案 | 檔案遺失、無法讀取或不支援的輸入，或未指定 `--allow-partial` 的不完整掃描 | 發現變更、未確認的觀測結果或不完整的掃描 | - |
| `export` | 已寫入指令碼 | 無法寫入指令碼 | 無法讀取的輸入、未指定 `--allow-partial` 的不完整掃描，或無法安全匯出的資料 | - | - |

## 專案架構

| 模組 | 職責 |
| --- | --- |
| `cli.py` | 命令選項、設定檔解析、預檢、掃描與報告輸出 |
| `scanner.py`、`probes.py` | 目標展開、受限的並行工作數量、主機探索與服務觀測 |
| `config.py`、`profiles.py` | 服務定義與經驗證的盤點設定檔 |
| `models.py`、`output.py` | 結果型別與終端機/JSON/CSV 呈現 |
| `history.py`、`diff.py` | SQLite 歷史紀錄與版本化檔案快照比對 |
| `preflight.py` | 本地檢查與有上限的 Nmap 版本查詢 |
| `export.py` | 經檢核與安全跳脫引號的 Kadupul 匯入指令碼 |

每筆服務觀測都會將服務狀態與其宣告的識別資訊分開記錄。讀取大小與截止時間皆設有上限；探測例外狀況會保留在主機錯誤清單中。SQLite 歷史紀錄使用交易機制、明確的連線清理，以及唯讀的清單與比對路徑。SNMP 機密資訊僅透過環境變數或機密檔案傳入；盤點歷史紀錄只會儲存有效的非機密設定。如需了解掃描管線、其限制與信任邊界，請參閱[架構說明](../../../docs/architecture.md)，並參閱[SECURITY.md](../../../SECURITY.md#authorized-use)了解授權使用規範。


## 使用方式

僅掃描您所管理的網路。

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| 選項 | 說明 |
| --- | --- |
| `NETWORK` | CIDR、IP 或主機名稱；搭配 `--profile` 時為選填。拒絕包含 IPv6 範圍識別碼的位址。 |
| `-o, --output PATH` | 寫入報告檔案。格式依副檔名（`.json`、`.csv`）決定；其他副檔名則預設為 JSON。 |
| `-f, --format json\|csv\|kadupul\|auto` | 強制指定報告格式。未搭配 `--output` 時無效。`.sh` 會選用 `kadupul`。 |
| `-v, --verbose` | 輸出除錯層級記錄。 |
| `-q, --quiet` | 隱藏結果、進度與資訊性記錄；警告與錯誤仍會輸出至 stderr。 |
| `--backend asyncio\|nmap` | 主機探索方式。`asyncio`（預設）會直接探測服務連接埠；`nmap` 會先執行 nmap ping 掃描，且需在 `PATH` 上找到 `nmap` 執行檔。 |
| `--timeout SECONDS` | 未自行設定預算之探測作業的等待時間（預設 1.0）。除非服務表另有設定 `timeout`，否則內建的連線探測會使用 0.3 秒。 |
| `--concurrency N` | 同時執行中的探測數量（預設 256）。 |
| `--deadline SECONDS` | 超過此時間後停止整場掃描（包含 nmap 掃描，預設 3600 秒，最高 604800 秒；環境變數 `HOSTCENSUS_DEADLINE`）。已完成的主機將以 `"complete": false` 寫入報告，不會寫入歷史紀錄或快照，且 `scan` 會以代碼 4 結束。 |
| `--config PATH` | TOML 服務定義與選用的具名 `[profiles]` 設定。 |
| `--profile NAME` | 使用具名設定檔；省略 `--config` 時預設讀取 `hostcensus.toml`。 |
| `--exclude IP/CIDR` | 新增排除項目；可視需要重複指定。排除的 IPv4 主機也會一併排除可連抵該主機的 IPv6 位址：IPv4 對應位址（`::ffff:a.b.c.d`）、NAT64（`64:ff9b::/96`）與 6to4。IPv4 對應的目標與排除項目會視為其所代表的 IPv4 位址。 |
| `--max-hosts N` | 在套用排除清單前檢查的位址數量上限（預設與硬性上限皆為 65,536）。 |
| `--history PATH` | 將已完成的掃描記錄至選用的 SQLite 歷史資料庫。 |
| `--services NAMES` | 要檢查的服務名稱（以逗號分隔），並依該順序執行（預設：全部）。 |
| `--ports SPEC` | 以逗號分隔的 `NAME=PORT`（變更服務連接埠）或 `PORT`（新增名為 `tcp-PORT` 的純 TCP 檢查）。 |
| `--snmp-community-file PATH` | 存放用於系統 MIB 查詢之 SNMPv2c 社群字串的檔案。環境變數：`HOSTCENSUS_SNMP_COMMUNITY`（值）或 `HOSTCENSUS_SNMP_COMMUNITY_FILE`（路徑）。 |
| `--snmp-user` | SNMPv3 使用者名稱。環境變數：`HOSTCENSUS_SNMP_USER`。 |
| `--snmp-auth-protocol`、`--snmp-auth-key-file PATH` | `MD5`、`SHA`（預設）、`SHA224`、`SHA256`、`SHA384`、`SHA512`，以及存放密碼片語的檔案。環境變數：`HOSTCENSUS_SNMP_AUTH_PROTOCOL`、`HOSTCENSUS_SNMP_AUTH_KEY` 或 `HOSTCENSUS_SNMP_AUTH_KEY_FILE`。 |
| `--snmp-priv-protocol`、`--snmp-priv-key-file PATH` | `DES`、`AES`（預設）、`AES128`、`AES192`、`AES192C`、`AES256`、`AES256C`，以及存放密碼片語的檔案。環境變數：`HOSTCENSUS_SNMP_PRIV_PROTOCOL`、`HOSTCENSUS_SNMP_PRIV_KEY` 或 `HOSTCENSUS_SNMP_PRIV_KEY_FILE`。 |
| `--save-snapshot PATH` | 同時寫入一份供 `hostcensus diff` 使用的版本化快照。 |
| `--tls-ca-file PATH` | 改用此 PEM 憑證套件驗證 HTTPS 憑證，而非系統存放區。環境變數：`HOSTCENSUS_TLS_CA_FILE`。 |

預設情況下，每台主機都會檢查 SSH（TCP 22）、SNMP（UDP 161）、MySQL（TCP 3306）、HTTP（TCP 80）與 HTTPS（TCP 443）。TCP 連接埠會以完整連線測試。SNMP 則以 SNMPv3 引擎探索請求進行測試，任何 SNMPv3 代理程式皆須在無驗證憑證的情況下回應此請求；僅支援 v1/v2c 的代理程式不會被此探測偵測到。使用 asyncio 後端時，只要任一探測收到回應（包含連線遭拒），該主機即視為存活，因此丟棄所有探測封包的主機將會標記為 `alive=false` 並附帶錯誤訊息 "Host is down"；這並不證明該主機在實體上已關機。使用 `--backend nmap` 時，由 nmap 決定哪些主機存活（root 權限下使用 ICMP，否則使用 TCP 80/443）。

### 服務指紋辨識

每個開啟的服務都會根據其在登入前傳回的內容進行指紋辨識。除了在您提供驗證憑證時的 SNMP 查詢外，不會進行任何身分驗證。

| 探測器 | 讀取內容 | `version` | `details` 鍵值 |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 識別行 | 軟體名稱，例如 `OpenSSH_10.0` | `protocol`、`software`、`comments` |
| `mysql` | MySQL/MariaDB 初始交握 | 伺服器版本 | `server_version`、`flavor`、`auth_plugin`，或 `error_code`/`error` |
| `http` | `HEAD /` 回應 | `Server` 標頭 | `status`、`server` |
| `https` | TLS 交握、憑證、`HEAD /` | `Server` 標頭 | `tls_version`、`cert_verified`、`cert_verify_error`、`cert_subject`、`cert_issuer`、`cert_sans`、`cert_not_before`、`cert_not_after`（UTC ISO 8601）、`cert_self_signed`、`status`、`server` |
| `snmp` | SNMPv3 探索；若有驗證憑證，則執行 sysDescr、sysObjectID、sysName 的 GET 查詢 | sysDescr | `engine_id`；若有驗證憑證，則包含 `snmp_version`、`sys_descr`、`sys_object_id`、`sys_name`，或 `snmp_error` |

主機名稱目標對每台主機只會解析一次，且所有探測皆會連線至該位址（於結果中記錄為 `address`）；主機名稱僅用於 TLS SNI、憑證驗證與 HTTP `Host` 標頭。無法解析的名稱會回報 `unknown` 狀態與 `Cannot resolve` 錯誤。反向 DNS 名稱僅在包含合法主機名稱字元時才會保留，且同時最多執行 16 次查詢。HTTPS 會針對系統存放區或 `--tls-ca-file` 進行憑證與主機名稱驗證。信任存放區於整場掃描只會載入一次，並重複用於每個 HTTPS 探測。TCP 連線與 TLS 交握會分開計時，因此接受連線但交握停滯的連接埠會標記為 `open` 並附帶 `tls_error`，而非 `filtered`。若驗證失敗，結果會記錄 `cert_verified: false` 與 `cert_verify_error`；不會以較寬鬆的設定重試，也不會送出 HTTP 請求。唯有驗證成功後才會收集憑證詳細資訊與 HTTP 標頭。針對使用私有 CA 的服務，請提供正確的 CA 憑證套件。較舊的報告可能包含 `cert_read_unverified`，目前的探測器已不再產生該欄位。

SNMP 機密資訊僅從環境變數或檔案（`--snmp-*-file` 或對應的 `HOSTCENSUS_SNMP_*_FILE` 變數）讀取，絕不從命令列數值讀取，因為其他本地使用者可在程序清單中看見命令列引數。以數值指定 `--snmp-community`、`--snmp-auth-key` 與 `--snmp-priv-key` 時會以結束代碼 2 結束並指出替代選項。機密檔案必須為非空的 UTF-8 文字，且大小不超過 4096 位元組；結尾的單一換行符號會被忽略，若同時針對同一項機密設定環境變數與檔案則會視為錯誤。錯誤訊息會指出檔案路徑，但絕不會印出其內容。掃描報告與歷史紀錄不會刻意包含驗證憑證數值。匯出工具另有下方所述的明確 `--include-credentials` 選項。設定社群字串會選用 SNMPv2c；設定使用者名稱則會選用 SNMPv3，提供驗證金鑰時會啟用驗證，同時提供兩種金鑰時則會啟用加密（由 `snmp_security_level` 記錄層級）。hostcensus 會拒絕混用社群字串與 v3 使用者、在沒有驗證金鑰的情況下使用加密金鑰，或在沒有使用者的情況下使用金鑰（並以結束代碼 2 結束），且絕不會將失敗的 v3 查詢降級為 v2c 或較低的安全層級重試。僅支援 v1/v2c 的代理程式會忽略無憑證的 v3 探索，因此只有在提供社群字串時才會顯示為開啟。

橫幅文字在儲存或顯示前會精簡為可列印字元並截斷至最多 256 個字元。讀取大小同樣受限：每行 4 KiB、MySQL 問候封包 4 KiB、HTTP 標頭 16 KiB。超過 32 個位元組的 SNMP 引擎 ID 在儲存前會被截斷。HTTP 與 HTTPS 送出 `Host` 標頭時，IPv6 位址會以中括號包夾，且非 80 或 443 連接埠時會附帶連接埠號。以試算表公式觸發字元開頭的 CSV 儲存格會加上前綴，使其維持純文字格式。

### 上限與限制

單次執行最多接受 65,536 個位址、64 項服務，以及 524,288 次探測（主機數乘以服務數）；超過上限的請求會在送出任何流量前以結束代碼 2 結束。`--concurrency` 上限為 4096 個 Socket。每個探測都有其自身預算四倍的硬性期限。除非該服務另有設定 `timeout`，否則連線類探測（`tcp`、`ssh`、`mysql`、`http`）使用 0.3 秒。SNMP 與 HTTPS 在服務未設定 `timeout` 時使用 `--timeout`（預設 1.0）。達到期限的探測會回報為 `unknown`，並在 `errors` 中記錄 "probe timed out"。本地 Socket 失敗（例如檔案描述子耗盡）同樣回報為 `unknown` 並記錄錯誤；絕不會被計為已過濾的連接埠或離線主機。在開始探測前，hostcensus 會將開啟檔案數的軟限制調高至接近硬限制，以容納 `--concurrency` 加上 64 個描述子；若無法達成，預檢的 `open files` 檢查將會失敗，`scan` 會在送出流量前以代碼 1 結束。Nmap 探索採用 30 秒的主機逾時。網段前置以 CIDR 形式傳遞給 nmap；當 nmap 回報的位址數量少於傳入數量時（例如無法解析名稱），掃描會以代碼 1 失敗，而非將主機標記為離線。主機名稱目標只會解析一次並將該位址交給 nmap，確保探索與探測連往同一台機器。完整網段前置會以單一 nmap 程序執行，其子程序期限為每 256 個位址 35 秒（無條件進位）。包含排除清單的掃描會以 256 台主機為一批執行，每批期限為 35 秒。建立並行工作數量的上限與網段大小無關。反向 DNS 與主機名稱解析另有獨立的兩秒期限；永不回傳的解析器呼叫會被遺棄在專屬執行緒中，以免拖住 hostcensus 超過這些上限。同時最多執行 16 次查詢，被遺棄的呼叫在回傳前會繼續佔用其名額，因此卡住的執行緒數量維持在上限內；若 16 個名額全部卡住，後續查詢會在兩秒期限外排隊等候釋出名額（該名額釋出後才開始計時），直到 `--deadline` 終止掃描為止。將 `NetworkScanner` 作為函式庫使用且未設定 `deadline` 時，可能會無限期等候此類名額。除此之外，`--deadline`（預設一小時）會對整場執行設定總時間上限。

### 組態設定服務

可透過 TOML 檔案修改服務設定：

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` 可為 `tcp`、`ssh`、`mysql`、`http`、`https` 或 `snmp`；當服務名稱本身即為探測器名稱時預設為該名稱，否則預設為 `tcp`。僅有 `snmp` 使用 UDP。服務名稱僅限小寫字母、數字、`-` 與 `_`。兩個服務不能共用同一連接埠與通訊協定；歷史紀錄會為該組配對記錄單一狀態。`timeout` 為選填，單位為秒，至少 0.05。連線類探測（`tcp`、`ssh`、`mysql`、`http`）預設為 0.3 秒。若服務未設定 `timeout`，`snmp` 與 `https` 會使用掃描的 `--timeout`。`--timeout` 不會覆蓋服務本身已設定的預算。

JSON 報告為版本化文件（`"format": "hostcensus-report"`、`"version": 1`），會在 `devices` 旁記錄掃描目標、探測服務與設定；未指定 `-o` 而使用 `--format json` 時，報告會直接輸出至 stdout 而非表格。每種 JSON 輸出皆有公開的 Schema；請參閱 [JSON 輸出格式](../../../docs/json-output.md)。裝置物件保留原有的 `ip`、`alive`、`ssh`、`snmp`、`mysql`、`hostname` 與 `errors` 欄位，並新增 `services` 清單，包含各探測器的 `name`、`port`、`protocol`、`state`（`open`、`closed`、`filtered`，或在探測於本地失敗或超過期限時為 `unknown`）、`version` 與 `details`。CSV 輸出則會在尾端新增 `services` 與 `versions` 欄位，列出開啟的服務。`ssh`、`snmp` 與 `mysql` 布林值對應至完全同名的服務。


## 盤點設定檔、預檢與本地歷史紀錄

具名設定檔與既有的 `[services]` 定義共用同一個 TOML 檔案。請將 [hostcensus.example.toml](../../../hostcensus.example.toml) 複製為 `hostcensus.toml` 並設定您所管理的網路：

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

`preflight` 解析選項與設定檔的方式與 `scan` 完全相同（包含用於開啟檔案檢查的 `--concurrency`），因此通過預檢代表 `scan` 將以完全相同的計畫啟動。

設定檔接受 `network`、`exclusions`、`services`、`ports`、`backend`、`timeout`、`concurrency` 與 `max_hosts`。`services` 與 `ports` 沿用既有的逗號分隔清單語法。命令列明確指定的選項會覆蓋設定檔設定；重複指定的 `--exclude` 選項則會附加至設定檔的排除清單中。搭配 `--profile` 明確指定網路時，該網路必須包含在該設定檔的 IP/CIDR 範圍內。直接掃描仍支援主機名稱，但無法與 IP 排除清單並用。主機數量上限於套用排除清單前檢查；總探測數上限則於套用後檢查。被排除的主機在服務檢查與選用的 Nmap 探索中皆會略過。

每次掃描在送出目標流量前皆會執行本地預檢：檢查目標/探測上限、輸出目標存取權限、選用的 Nmap 執行檔/包裝器可用性、歷史資料庫結構描述，以及已設定的 TLS CA 憑證套件。`preflight` 會輸出 JSON 報告，且不會掃描目標或建立歷史資料庫。它會暫時寫入一個同層檔案以測試輸出目標存取權限，而不會更動現有內容。預設的 asyncio 後端依然不需要 Nmap 也不需要 root 權限。各輸出目標路徑之間，以及與輸入組態檔之間必須各自獨立（包含硬連結）；輸出目標不得為符號連結。檢查失敗回傳 1；無效的範圍或組態則回傳 2。

寫入報告與匯出檔案需要系統支援 `O_NOFOLLOW`。在不支援的平台上（包含 Windows），這些寫入操作會在開啟或截斷目標檔案前直接失敗。新建的報告與匯出指令碼僅限擁有者存取（權限模式 0600）；覆蓋現有檔案時則會保留其原有權限。寫入沒有讀取端的具名管線時會立即失敗，不會等待。新建的 `--history` 資料庫同樣為僅限擁有者存取；現有資料庫則維持其權限模式。記錄訊息一律輸出至 stderr，因此 stdout 只會包含結果內容。包含驗證憑證的匯出檔一律強制設定為權限模式 0600。

歷史紀錄為選用功能，與既有的 JSON 快照及 `diff` 指令相輔相成：

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

請使用 `history` 查詢到的 ID；上述範例假設為新建的資料庫。快照會以交易機制連同 UTC 開始/結束時間、套件版本、有效的非機密設定、摘要資訊，以及所有主機/服務觀測結果（包含各主機錯誤）一併儲存。未完成的主機觀測會予以保留，遭取消的執行則不會儲存。既有的報告、快照、匯出與掃描結束代碼契約皆維持不變。

`history` 會列出 JSON 摘要，而不讀取所有歷史裝置資料。`compare` 會讀取兩筆已儲存的掃描，要求兩者具備相同的目標識別資訊與選取的連接埠，並報告回應狀態、整體狀態與連接埠狀態的變更。較早的掃描 ID 必須排在較晚的 ID 之前。若兩次掃描皆記錄了 `timeout` 或 `backend` 且數值不同，報告會列出警告並照常進行比對。不同的等待時間可能會讓原本被過濾的連接埠看起來像開啟。掃描器錯誤與未知連接埠觀測會標記為不確定，而非視為已確認的消失或關閉：帶有錯誤的主機會出現在 `uncertain_hosts`，而所有涉及 `unknown` 的連接埠轉換（包含兩次掃描皆為 unknown 的情況）皆會列於 `unconfirmed_ports` 而非 `port_changes`，唯有在較晚掃描中呈現開啟的連接埠會列為連接埠變更。`compare` 與 `diff` 使用相同規則分類連接埠。`no_longer_responding` 代表未收到回應，而非裝置已被移除的證明。掃描結束代碼 0 不保證每台主機皆有回應：請檢視各主機的錯誤欄位。無論是否有變更，比對成功皆回傳 0；既有的檔案 `diff` 指令則保留其結束代碼 3 的契約。不支援或毀損的歷史資料庫會回傳 1。

歷史資料庫儲存了盤點資訊，請選擇受適當保護的本地目錄。設定檔與儲存的設定不包含 SNMP 驗證憑證；憑證處理仍透過既有的執行階段選項或環境變數進行。

## 盤點差異比對

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

快照為 JSON 格式，包含 `format: "hostcensus-snapshot"`、`version: 1`、hostcensus 版本、UTC 建立時間、掃描目標、掃描時記錄的 `timeout` 與 `backend`、受探測的服務，以及與 `-o` 報告相同結構的存活主機清單。離線主機不會列入其中。`diff` 也接受一般的 `scan -o` JSON 報告，包含尚未有 `services` 欄位之前的舊版報告。

`diff` 會報告新增與消失的主機、在兩次掃描中皆存在的主機上開啟或關閉的連接埠，以及 `version` 發生變更的服務。僅在兩次掃描其中之一探測過的連接埠不會進行比對，並會顯示警告。失敗的觀測結果絕不會被判讀為「無變更」：在任一次掃描中為 `unknown` 且在較晚掃描中並非開啟的連接埠，會列在 `unconfirmed` 而非 `closed` 之下，其 `before` 值為 `open`、`unknown` 或 `not-open`（已探測且為關閉或已過濾），`after` 值為 `unknown` 或 `not-open`；若該連接埠目前為開啟，即使較早探測失敗，仍會回報於 `opened` 之下。在任一次掃描中所有探測皆失敗且未收到任何回應的主機，會列在 `unsettled_hosts`（其 `before`/`after` 值為 `up`、`uncertain` 或 `absent`，包含兩次掃描皆失敗或另一份檔案缺少該主機的情況）而非 `vanished_hosts`；若它在較晚掃描中有回應，也會同時回報為新增主機並附上其開啟的連接埠。快照保留這些失敗主機正是基於此原因。當目標不同，或兩份檔案皆記錄了逾時或後端且數值不一致時，也會顯示警告。搭配 `-o PATH` 可同時將 JSON 格式結果寫入檔案。

因觸及 `--deadline` 而中止的掃描報告（`"complete": false`）僅列出已掃描到的主機，因此 `diff` 與 `export` 會以結束代碼 2 拒絕處理。指定 `--allow-partial` 可於 stderr 印出警告並接受該報告：`diff` 會將不完整掃描中完全未列出的主機列於 `unsettled_hosts` 並標記為 `unscanned`，而非視為消失（已標記為離線的主機仍視為消失），同時將 `partial` 設為 true 且絕不回報為無變更；`export` 則會在指令碼標頭寫入警告訊息。

`diff` 結束代碼：`0` 無變更、`3` 發現變更、無法確認的觀測結果或不完整的輸入（只要任何清單，包含 `unsettled_hosts` 與 `unconfirmed`，非空，或 `partial` 為 true，則 `changed` 即為 true）、`2` 檔案遺失、無法讀取、非受支援的快照格式，或未指定 `--allow-partial` 的不完整掃描、`1` 無法寫入 `-o` 檔案。

## 匯出至 Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul)（Cacti 1.2.31 的分支版本）不支援批次匯入裝置檔案。其支援透過指令碼新增裝置的方式為呼叫 `cli/add_device.php`，每次呼叫新增一台裝置，並傳入 `--option=value` 引數。`hostcensus export` 會產生包含這些呼叫的 POSIX `sh` 指令碼：

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

每台存活主機都會轉換為 `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`：

- 掃描時 SNMP 查詢成功的主機會取得 `--version=2 --community=...` 或 `--version=3 --username=... --authproto=... --password=...`（authPriv 另加 `--privproto`/`--privpass`）、`--port` 與 `--avail=snmp`。匯出 SNMPv3 需要 `--snmp-user`，且會拒絕 noAuthNoPriv，因為 `add_device.php` 要求必須提供 v3 密碼。
- 其他主機則取得 `--version=0 --avail=ping`，搭配 `--ping_method=tcp --ping_port=` 第一個開啟的 TCP 連接埠，若無開啟連接埠則改用 ICMP。
- `--notes` 列出開啟的服務與版本。`--description` 在反向 DNS 名稱為純文字（英文字母、數字、`.`、`_`、`-`）時使用該名稱，否則使用 IP，並會確保名稱唯一，因為 `add_device.php` 會將重複的描述視為更新該既有裝置。

每個數值皆經過驗證並使用 `shlex.quote` 進行 Shell 引號跳脫。預設不會將任何 SNMP 機密寫入檔案：指令碼會在執行時展開 `HOSTCENSUS_SNMP_COMMUNITY`、`HOSTCENSUS_SNMP_AUTH_KEY` 或 `HOSTCENSUS_SNMP_PRIV_KEY`，若任一變數未設定即停止執行。`--include-credentials` 則會改將這些環境變數的值直接寫入指令碼、以權限模式 0600 建立檔案，並記錄一則警告。`add_device.php` 本身會印出社群字串且以引數形式接收機密，因此在每次呼叫執行期間，這些機密資訊會出現在 Kadupul 伺服器的程序清單中。

`add_device.php` 遇到重複或錯誤時會以代碼 1 結束；產生的指令碼會繼續執行其餘項目、統計失敗次數，並在有任何裝置未成功新增時以代碼 1 結束。範本 ID 可透過 `php cli/add_device.php --list-host-templates` 取得。`export` 結束代碼：`0` 已寫入、`2` 無法讀取的輸入、未指定 `--allow-partial` 的不完整掃描，或無法安全匯出的資料、`1` 無法寫入指令碼。

## 版本控制與發行流程

hostcensus 遵循[語意化版本控制](https://semver.org/spec/v2.0.0.html)：相容的修正會遞增修訂版號（patch），相容的新功能或淘汰宣告會遞增次版號（minor），而破壞相容性的變更則會遞增主版號（major）。指令與選項、結束代碼以及 JSON Schema 皆屬於公開契約；除非基於安全修正必須提前變更（變更記錄會說明原因），否則已淘汰的行為將持續運作至下一個主要版本為止。

release-please 會根據 `main` 分支上的 Conventional Commit 標題開啟發行 PR，更新 `pyproject.toml`、`uv.lock` 與 `CHANGES.md`。合併該 PR 後會建立 `vMAJOR.MINOR.PATCH` 標籤與 GitHub 草稿發行版，CI 隨即將通過測試的 wheel、原始碼發行套件與總和檢查碼附加至該發行版；GitHub 透過其 attestations API 為這些檔案儲存建置證明。檔案附加完成後，維護者會審閱並發布該草稿。已發布的版本絕不會被覆寫替換。

PyPI 信任發布為選用機制，需要專案擁有權、設定信任發布者以及 `pypi` 環境。它會直接發布同一份經過檢查的發行產出物，無須重新建置或儲存 API 權杖。在此公開儲存庫中，標記的發行版本會產生 GitHub 產出物證明；私人分支複本則需要受支援的方案與明確啟用。如需完整設定步驟、確切指令與重試方式，請參閱[完整發行指南](../../../docs/releasing.md)。

## 開發

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

開發工具位於 `pyproject.toml` 中的 [PEP 735](https://peps.python.org/pep-0735/) 相依群組（`dev`、`fuzz`、`build`），因此絕不會出現在已發布的套件中繼資料中。`uv.lock` 為唯一的鎖定檔；CI 會使用 `uv sync --locked` 安裝，並在鎖定檔過期時失敗。請透過 `uv python`、mise（`mise exec python@3.14 -- uv sync --locked`）或任何 Python 3.12+ 環境選取直譯器。

CI 強制要求 90% 的套件測試覆蓋率下限。單元測試包含受控的迴路伺服器與離線設定檔/歷史紀錄/發行驗證案例；Compose 測試環境則會在隔離的橋接網路上執行 OpenSSH、MariaDB、nginx 與 net-snmp。請以 `make test-integration` 執行。另請參閱 [CONTRIBUTING.md](../../../CONTRIBUTING.md) 與[發行工具說明](../../../scripts/README.md)。

執行階段容器以 UID/GID 10001 身分執行，沒有家目錄、沒有 Shell 登入也沒有 pip，且可寫入 `/app/output`。請授予該使用者對任何掛載輸出目錄的寫入權限。該容器不需要任何系統權能，且可在唯讀根檔案系統下運作，因此可依以下方式執行：

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap 在此容器中會使用非特權的 TCP 探索行為。若 Trivy 報告任何可修補的 HIGH 或 CRITICAL 弱點，CI 的映像檔建置將會失敗。

## 供應鏈檢查

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) 會在 main 分支及每週定期執行、公開實際分數，並將結果上傳至 GitHub 程式碼掃描。Actions 與容器基底映像檔皆以不可變雜湊值固定；Python 相依套件則鎖定於 `uv.lock`。Bandit 檢查失敗會導致 CI 失敗，且受限的 Atheris 模糊測試會在無網路存取下測試 SSH、MySQL、HTTP、憑證與 SNMPv3 BER 剖析器。

Scorecard 也會衡量歷史審閱活動、貢獻者多樣性與發行來源證明。這些分數反映實際佐證，並不代表所有治理或歷史發行檢查皆已滿足。請參閱 [SECURITY.md](../../../SECURITY.md) 與[發行來源證明](../../../docs/releasing.md)。

## 在地化

命令列訊息與終端機摘要/差異表格支援 45 種語系（`en`、`de`、`es`、`fr`、`it`、`pt-BR`、`nl`、`ru`、`uk`、`ja`、`ko`、`zh-CN`、`zh-TW`、`ar`、`hi`、`pl`、`tr`、`sv`、`vi`、`id`、`af-ZA`、`am-ET`、`ar-EG`、`ar-MA`、`fr-MA`、`fr-SN`、`ha-NG`、`ig-NG`、`mg-MG`、`rw-RW`、`so-SO`、`sw-KE`、`xh-ZA`、`yo-NG`、`zu-ZA`、`bn`、`fa`、`he`、`mr`、`ta`、`te`、`th`、`ur`、`ms`、`fil`），且無須額外的執行階段相依套件。語系解析依序優先採用 `--lang`、`LC_ALL`、`LC_MESSAGES` 與 `LANG`，最後退回至 `en`。JSON Schema、CSV 欄位與匯出指令碼在所有語系下皆維持不變。

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## 貢獻指南

提交貢獻時應包含可重現的案例、維持既有文件記載的 CLI 與資料格式契約，並通過上述品質檢查。有關開發工作流程請參閱 [CONTRIBUTING.md](../../../CONTRIBUTING.md)，相容性與版本決策則請參閱[發行指南](../../../docs/releasing.md)。

## 安全性與授權狀態

有關私密通報流程與支援版本，請參閱 [SECURITY.md](../../../SECURITY.md)。hostcensus 採用 [MIT 授權條款](../../../LICENSE)。

原始碼標頭使用 SPDX 識別碼，並保留 Git 歷史中的貢獻者署名。署名詳情請參閱 [AUTHORS.md](../../../AUTHORS.md)。二進位測試擷取檔與產生的鎖定檔使用相鄰的 `.license` 檔案；MIT 授權全文位於 `LICENSES/MIT.txt`。
