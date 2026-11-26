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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · **简体中文** · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus 是一个 Python 命令行工具，用于对你所管理的网络执行可重复的服务资产盘点。它能记录设备暴露的服务、跨时间对比观测结果，并生成 Kadupul 导入脚本。默认后端无需 root 权限即可使用 asyncio 套接字进行探测；可选的 Nmap 主机发现功能还能识别配置服务端口之外的在线主机。

## 为什么选择 hostcensus

单次的端口扫描报告无法说明下一次观测结果究竟是发生了真实变化，还是仅仅探测失败。hostcensus 将明确的服务状态、有界探测、可复用的扫描配置文件以及本地历史记录结合在一起。运维人员可以针对同一范围重复扫描、排查错误，并将不确定的观测结果与已确认的变更区分开来。

- **服务证据：** 支持 SSH 标识、MySQL 握手问候、HTTP 响应头、TLS 证书观测，以及 SNMP 发现或带凭据的 system-MIB 查询。
- **可重复的扫描范围：** 支持具名 TOML 配置文件、增量排除项、可配置服务、主机数/探测数上限以及受限的并发工作协程。
- **发包前预检：** 本地预检会校验目标、工具、输出目标访问权限、历史记录数据库模式以及配置的 TLS CA 证书包。
- **资产历史记录：** 事务性 SQLite 快照会保留所有观测结果；对比功能会明确保留扫描器故障和未知状态。
- **可互操作的输出：** 支持终端表格、JSON 和 CSV 报告、带版本的文件快照以及 Kadupul 导入脚本。

CI 在 Linux 和 macOS 上覆盖了 Python 3.12、3.13 和 3.14，并包含一个受控的 Compose 集成测试环境。代码在保持兼容这些运行时版本的同时，采用了现代类型别名、强类型预检结果、仅限关键字参数且使用 slots 的配置类，以及结构化异步清理机制。有关 SemVer 兼容性契约和 GitHub 发布流程，请参阅[版本控制与发布](../../../docs/releasing.md)。发布徽章展示的是已发布的构建产物，而非当前检出代码：目前最新发布标签为 `v0.3.0`，而当前检出代码使用的包版本为 `3.0.0`。请直接从当前检出目录安装，以使用本文档介绍的资产盘点功能。

请先阅读[安装](#install)，然后查看[配置方案与历史记录](#inventory-profiles-preflight-and-local-history)。如需了解集成细节，请参阅[服务指纹识别](#fingerprints)、[文件差异对比](#inventory-diff)和[Kadupul 导出](#kadupul-export)。

## 安装

需要 Python 3.12 或更高版本；已通过测试矩阵验证的版本为 Python 3.12 至 3.14。在当前检出目录中安装锁定的运行时依赖：

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

如需使用可选的 Nmap 主机发现功能，请通过所在平台的包管理器安装 Nmap 可执行文件，无需额外的 Python 软件包。Nmap 的 XML 输出通过核心依赖 defusedxml 进行解析，因此会拒绝实体扩展。hostcensus 会直接调用 `PATH` 中找到的 `nmap`，传入固定参数列表、随网段前缀规模增长的超时截止时间，以及 64 MiB 的输出上限。默认后端不需要 Nmap。

## 从 netprobe 迁移

hostcensus 是 netprobe 自 3.0.0 版本起启用的新名称。该项目此前未以任何名称发布到 PyPI，均通过源码检出或 GitHub Release 安装。GitHub 仓库名称保持不变。

| 原名称 | 现名称 | 兼容性 |
| --- | --- | --- |
| 分发包 `netprobe` | `hostcensus` | 请从当前检出目录重新安装；不再提供旧名称的软件包。 |
| `netprobe` 命令 | `hostcensus` | `netprobe` 仍可运行，并会在 stderr 输出一行弃用提示。退出码和 stdout 保持不变。将在下一个主版本中移除。 |
| `NETPROBE_*` 环境变量 | `HOSTCENSUS_*` | 当对应的 `HOSTCENSUS_*` 未设置时，仍会读取 `NETPROBE_*` 变量，并在 stderr 输出一次警告（仅列出变量名，绝不输出变量值）。两者同时设置时以 `HOSTCENSUS_*` 为准。将在下一个主版本中移除。 |
| `import netprobe`、`python -m netprobe` | `import hostcensus`、`python -m hostcensus` | **破坏性变更。** 未安装导入兼容层，请更新导入语句。 |
| Docker 镜像标签 `network-discovery:test`（仅限 CI）及容器用户 `netprobe` | `hostcensus:test`、用户 `hostcensus` | 从未向镜像仓库发布过镜像。请重新构建镜像并使用 `hostcensus` 入口点。 |
| `netprobe.toml`、`netprobe-history.sqlite3` | `hostcensus.toml`、`hostcensus-history.sqlite3` | 当新名称文件不存在时，仍会继续使用已有的旧默认名称文件并给出警告。显式指定的 `--config` 和 `--history` 路径不受影响。 |
| 包含 `"format": "netprobe-report"` 或 `"netprobe-snapshot"` 以及 `netprobe_version` 字段的报告和快照 | `hostcensus-report`、`hostcensus-snapshot`、`hostcensus_version` | `diff` 和 `export` 仍可加载旧名称格式的文件，已发布的 JSON Schema 也同时接受新旧两种拼写。新生成的文件使用新名称。SQLite 历史数据库结构未变，可照常加载。 |
| 由 `netprobe export` 生成的 Kadupul 脚本 | 由 `hostcensus export` 生成的脚本 | 旧脚本仍可正常运行，并在执行时继续读取 `NETPROBE_SNMP_*`。新生成的脚本读取 `HOSTCENSUS_SNMP_*`。 |

## 快速示例

在“开发”一节所述的集成测试环境中的 tester 容器内运行（输出已精简）：

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

## 退出码

| 命令 | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | 已记录观测结果/报告 | 预检/后端执行失败，或历史记录、报告、快照写入失败 | 无效的目标、选项、配置或限制参数 | - | 达到 `--deadline` 上限；已写入部分报告，跳过历史记录与快照 |
| `preflight` | 检查全部通过 | 本地检查失败 | 无效的目标/配置或输出路径冲突 | - | - |
| `profiles` | 已列出经校验的配置方案 | - | 无法读取或无效的配置/选择项 | - | - |
| `history` | 已列出摘要信息 | 历史数据库缺失、无效或不受支持 | 无效的 CLI 选项 | - | - |
| `compare` | 已生成对比结果（包括存在变更时） | 历史记录不可读、范围/顺序不兼容或写入失败 | 无效的 CLI 选项 | - | - |
| `diff` | 无变化 | 无法写入 `-o` 指定的文件 | 输入文件缺失、不可读、不受支持，或未加 `--allow-partial` 的不完整扫描 | 发现变更、存在未确认的观测结果或扫描不完整 | - |
| `export` | 已写入脚本 | 无法写入脚本 | 输入不可读、未加 `--allow-partial` 的不完整扫描，或包含无法安全导出的数据 | - | - |

## 代码结构

| 模块 | 职责 |
| --- | --- |
| `cli.py` | 命令选项解析、配置方案解析、预检、扫描与报告输出 |
| `scanner.py`、`probes.py` | 目标网段展开、有界工作协程、主机发现与服务观测 |
| `config.py`、`profiles.py` | 服务定义与经校验的盘点配置方案 |
| `models.py`、`output.py` | 结果数据模型以及终端/JSON/CSV 渲染 |
| `history.py`、`diff.py` | SQLite 历史记录与带版本的文件快照对比 |
| `preflight.py` | 本地检查与有界 Nmap 版本查询 |
| `export.py` | 经校验与安全引用的 Kadupul 导入脚本生成 |

每条服务观测记录都会将其端口状态与通告的身份信息分开保存。读取字节数和截止时间均有严格上限；探测异常会保留在主机错误记录中。SQLite 历史模块使用数据库事务、显式连接清理以及只读的列表和对比路径。SNMP 密钥仅通过环境变量或密钥文件传入；盘点历史记录仅存储生效的非敏感配置。有关扫描流水线、限制条件与信任边界，请参阅[架构说明](../../../docs/architecture.md)；有关授权使用规范，请参阅 [SECURITY.md](../../../SECURITY.md#authorized-use)。


## 用法

请仅扫描你所管理的网络。

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| 选项 | 含义 |
| --- | --- |
| `NETWORK` | CIDR 网段、IP 地址或主机名；使用 `--profile` 时为可选项。不接受带作用域标识符的 IPv6 地址。 |
| `-o, --output PATH` | 将报告写入文件。输出格式默认根据扩展名推断（`.json`、`.csv`）；其他扩展名默认回退为 JSON。 |
| `-f, --format json\|csv\|kadupul\|auto` | 强制指定报告格式。未指定 `--output` 时不生效。`.sh` 会选择 `kadupul`。 |
| `-v, --verbose` | 输出调试日志。 |
| `-q, --quiet` | 抑制常规结果、进度及提示性日志；警告和错误仍会输出到 stderr。 |
| `--backend asyncio\|nmap` | 主机发现后端。`asyncio`（默认）直接探测服务端口；`nmap` 会先执行一次 nmap ping 扫描，且要求 `PATH` 中存在 `nmap` 可执行文件。 |
| `--timeout SECONDS` | 未单独设置超时预算的探测器的等待时间（默认 1.0 秒）。除非服务配置表设置了 `timeout`，否则内置连接型探测器使用 0.3 秒。 |
| `--concurrency N` | 同时进行的探测任务并发数（默认 256）。 |
| `--deadline SECONDS` | 整个扫描任务（包括 nmap 扫描）的最长运行时间（默认 3600 秒，上限 604800 秒；环境变量 `HOSTCENSUS_DEADLINE`）。超时后已完成的宿主机会写入报告并标记 `"complete": false`，不写入历史记录和快照，`scan` 以退出码 4 退出。 |
| `--config PATH` | TOML 格式的服务定义及可选具名 `[profiles]` 配置文件。 |
| `--profile NAME` | 使用具名配置方案；省略 `--config` 时默认读取 `hostcensus.toml`。 |
| `--exclude IP/CIDR` | 添加排除地址或网段，可重复指定。排除某个 IPv4 主机时，也会同时排除能到达该主机的 IPv6 地址形式：IPv4 映射地址（`::ffff:a.b.c.d`）、NAT64（`64:ff9b::/96`）和 6to4 地址。IPv4 映射形式的目标和排除项均按其对应的 IPv4 地址处理。 |
| `--max-hosts N` | 在应用排除规则之前检查的地址数量上限（默认及硬性上限为 65,536）。 |
| `--history PATH` | 将已完成的扫描记录到可选启用的 SQLite 历史数据库中。 |
| `--services NAMES` | 逗号分隔的服务名称列表，按指定顺序检查（默认检查全部已定义服务）。 |
| `--ports SPEC` | 逗号分隔的端口规格：`NAME=PORT`（修改指定服务的端口）或 `PORT`（新增名为 `tcp-PORT` 的纯 TCP 检查）。 |
| `--snmp-community-file PATH` | 保存用于查询系统 MIB 的 SNMPv2c 团体字的文件路径。环境变量：`HOSTCENSUS_SNMP_COMMUNITY`（直接传值）或 `HOSTCENSUS_SNMP_COMMUNITY_FILE`（文件路径）。 |
| `--snmp-user` | SNMPv3 用户名。环境变量：`HOSTCENSUS_SNMP_USER`。 |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | 认证协议支持 `MD5`、`SHA`（默认）、`SHA224`、`SHA256`、`SHA384`、`SHA512`，以及保存认证密码短语的文件路径。环境变量：`HOSTCENSUS_SNMP_AUTH_PROTOCOL`、`HOSTCENSUS_SNMP_AUTH_KEY` 或 `HOSTCENSUS_SNMP_AUTH_KEY_FILE`。 |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | 加密协议支持 `DES`、`AES`（默认）、`AES128`、`AES192`、`AES192C`、`AES256`、`AES256C`，以及保存加密密码短语的文件路径。环境变量：`HOSTCENSUS_SNMP_PRIV_PROTOCOL`、`HOSTCENSUS_SNMP_PRIV_KEY` 或 `HOSTCENSUS_SNMP_PRIV_KEY_FILE`。 |
| `--save-snapshot PATH` | 同时保存一份用于 `hostcensus diff` 的带版本快照文件。 |
| `--tls-ca-file PATH` | 使用指定的 PEM 证书包而非系统证书库来校验 HTTPS 证书。环境变量：`HOSTCENSUS_TLS_CA_FILE`。 |

默认情况下，每台主机会检查 SSH（TCP 22）、SNMP（UDP 161）、MySQL（TCP 3306）、HTTP（TCP 80）和 HTTPS（TCP 443）。TCP 端口采用完整连接方式检测。SNMP 通过发送 SNMPv3 引擎发现请求进行检测，任何支持 SNMPv3 的代理都必须在无凭据状态下响应此请求；仅支持 v1/v2c 的代理不会被此探测识别。使用 asyncio 后端时，只要任意探测收到响应（包括连接被拒绝），主机即视为存活；因此丢弃所有探测包的主机状态为 `alive=false`，且错误信息为“Host is down”，但这并不证明设备在物理上已关机。使用 `--backend nmap` 时，由 nmap 判定主机是否存活（root 权限下使用 ICMP，否则探测 TCP 80/443）。

### 指纹识别

每个开放服务都会根据其在登录前返回的响应内容进行指纹识别。除 SNMP 查询外，所有探测均不进行身份认证；且 SNMP 认证仅在你提供了凭据时才会触发。

| 探测器 | 读取内容 | `version` | `details` 键名 |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 标识行 | 软件版本，例如 `OpenSSH_10.0` | `protocol`、`software`、`comments` |
| `mysql` | MySQL/MariaDB 初始握手包 | 服务端版本 | `server_version`、`flavor`、`auth_plugin`，或 `error_code`/`error` |
| `http` | `HEAD /` 响应 | `Server` 响应头 | `status`、`server` |
| `https` | TLS 握手、证书、`HEAD /` | `Server` 响应头 | `tls_version`、`cert_verified`、`cert_verify_error`、`cert_subject`、`cert_issuer`、`cert_sans`、`cert_not_before`、`cert_not_after`（UTC ISO 8601 格式）、`cert_self_signed`、`status`、`server` |
| `snmp` | SNMPv3 发现；提供凭据时执行 GET sysDescr、sysObjectID、sysName | sysDescr | `engine_id`；提供凭据时包含 `snmp_version`、`sys_descr`、`sys_object_id`、`sys_name`，或 `snmp_error` |

每个主机名目标只会解析一次，所有探测器均连接至该解析地址（在结果中记录为 `address`）；主机名本身仅用于 TLS SNI、证书校验以及 HTTP `Host` 请求头。无法解析的主机名会产生 `unknown` 状态并记录 `Cannot resolve` 错误。反向 DNS 名称仅在全部由合法主机名字符组成时才会保留，且同时最多运行 16 个解析查询。HTTPS 会使用系统证书库或 `--tls-ca-file` 指定的证书进行证书与主机名校验。信任库在每次扫描开始时加载一次，并由所有 HTTPS 探测复用。TCP 连接与 TLS 握手分别计时，因此接受连接但握手卡住的端口会被标记为 `open` 并附带 `tls_error`，而非 `filtered`。如果校验失败，结果会记录 `cert_verified: false` 和 `cert_verify_error`，绝不会降级配置重试或继续发送 HTTP 请求。只有在校验成功后，才会收集证书详情和 HTTP 响应头。对于使用私有 CA 签发证书的服务，请提供正确的 CA 证书包。旧版报告中可能包含 `cert_read_unverified` 字段，当前版本的探测器已不再生成该字段。

SNMP 密钥仅能从环境变量或文件（`--snmp-*-file` 或对应的 `HOSTCENSUS_SNMP_*_FILE` 变量）中读取，绝不接受通过命令行参数直接传入明文值，因为本地其他用户可在进程列表中看到命令行参数。若为 `--snmp-community`、`--snmp-auth-key` 或 `--snmp-priv-key` 传入值，程序将以退出码 2 退出并提示应改用的替代参数。密钥文件必须为非空 UTF-8 编码且不超过 4096 字节；文件末尾的单个换行符会被忽略；同时为同一密钥设置环境变量和文件将报错。错误信息只会指出文件名，绝不打印文件内容。扫描报告和历史记录均不会主动包含凭据值。导出工具提供了单独且显式的 `--include-credentials` 选项（见下文）。指定团体字将启用 SNMPv2c；指定用户则启用 SNMPv3：提供认证密钥时启用认证，同时提供认证密钥和加密密钥时启用加密（实际级别记录在 `snmp_security_level` 中）。hostcensus 会拒绝以下配置并以退出码 2 退出：同时提供团体字与 v3 用户、未提供认证密钥而使用加密密钥、或未指定用户而提供密钥；同时绝不会将失败的 v3 查询降级为 v2c 或更低安全级别进行重试。仅支持 v1/v2c 的代理会忽略无凭据的 v3 发现包，因此只有在提供团体字时才会显示为开放。

横幅文本在存储或显示前会过滤为可打印字符并截断至最多 256 个字符。网络读取同样受限：每行上限 4 KiB，MySQL 握手问候上限 4 KiB，HTTP 响应头上限 16 KiB。超过 32 字节的 SNMP 引擎 ID 在存储前会被截断。发送 HTTP 和 HTTPS 请求时，若目标为 IPv6 地址，Host 请求头会将其放入方括号内；若端口不是 80 或 443，则会附带端口号。对于以电子表格公式触发字符开头的 CSV 单元格，系统会添加前缀以确保其保持纯文本格式。

### 限制与边界

单次运行最多接受 65,536 个地址、64 项服务以及 524,288 次探测（主机数乘以服务数）；超出限制的请求会在发送任何流量前以退出码 2 退出。`--concurrency` 的上限为 4096 个套接字。每个探测器的硬性截止时间为其自身超时预算的 4 倍。连接型探测器（`tcp`、`ssh`、`mysql`、`http`）默认使用 0.3 秒，除非相应服务单独设置了 `timeout`。SNMP 和 HTTPS 在未单独设置时使用 `--timeout`（默认 1.0 秒）。达到截止时间的探测器会报告为 `unknown`，并在 `errors` 中记录“probe timed out”。本地套接字故障（例如文件描述符耗尽）同样报告为 `unknown` 并记录错误信息，绝不会被误判为端口被过滤或主机离线。在开始探测前，hostcensus 会尝试将打开文件数软限制向硬限制提升，以容纳 `--concurrency` 加上 64 个描述符；若无法满足，`open files` 预检将失败，`scan` 会在发送流量前以退出码 1 退出。Nmap 主机发现对单台主机采用 30 秒超时。网段前缀以 CIDR 格式传给 nmap，若 nmap 报告的地址数少于传入数量（例如无法解析的名称），扫描会以退出码 1 失败，而不是将这些主机标记为离线。主机名目标会先解析一次再将 IP 地址传给 nmap，以确保主机发现和端口探测访问的是同一台机器。完整网段会作为单个 nmap 进程运行，其子进程截止时间按每 256 个地址 35 秒向上取整计算。包含排除规则的扫描会按每批 256 台主机分批执行，每批截止时间为 35 秒。工作协程的创建数量独立于地址范围大小，始终受控。反向 DNS 和主机名解析拥有独立的 2 秒截止时间；永不返回的解析调用会被留在其独立线程中放弃等待，从而不会导致 hostcensus 超出上述时间限制。同时最多运行 16 个解析查询，被放弃的调用在返回前会继续占用其槽位，因此卡住的线程总数有明确上限；如果 16 个槽位全部挂起，后续查询会在 2 秒截止时间之外排队等待空闲槽位（2 秒计时从获得槽位时开始），直到 `--deadline` 终止扫描。将 `NetworkScanner` 作为库使用且未传入 `deadline` 时，可能会无限期等待此类槽位。在上述限制之上，`--deadline`（默认 1 小时）对整次运行的总时长进行兜底限制。

### 配置服务

可以通过 TOML 文件修改服务配置：

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` 的可选值为 `tcp`、`ssh`、`mysql`、`http`、`https` 或 `snmp`；当服务名本身就是探测器名称时默认取该名称，否则默认为 `tcp`。仅 `snmp` 使用 UDP。服务名称由小写字母、数字、`-` 和 `_` 组成。两个服务不能共用同一端口和协议；历史记录会对该端口/协议对保存唯一的状态。`timeout` 为可选项，单位为秒，最小为 0.05。连接型探测器（`tcp`、`ssh`、`mysql`、`http`）默认为 0.3 秒。`snmp` 和 `https` 在服务未设置 `timeout` 时使用扫描的 `--timeout` 参数。`--timeout` 不会覆盖服务配置中已有的超时预算。

JSON 报告是带版本号的文档（`"format": "hostcensus-report"`、`"version": 1`），除了 `devices` 字段外，还会记录扫描目标、探测的服务列表及配置参数；未指定 `-o` 时使用 `--format json` 会将报告输出到 stdout 而非终端表格。所有 JSON 输出均有公开的模式定义，请参阅 [JSON 输出规范](../../../docs/json-output.md)。每个设备对象保留原有的 `ip`、`alive`、`ssh`、`snmp`、`mysql`、`hostname` 和 `errors` 字段，并新增 `services` 列表，包含每个探测器的 `name`、`port`、`protocol`、`state`（`open`、`closed`、`filtered`，或在本地失败及超时时为 `unknown`）、`version` 和 `details`。CSV 输出在末尾增加了用于记录开放服务的 `services` 和 `versions` 两列。`ssh`、`snmp` 和 `mysql` 这三个布尔字段与同名服务的状态保持一致。


## 盘点配置方案、预检与本地历史记录

具名配置方案与现有的 `[services]` 定义共用同一个 TOML 文件。将 [hostcensus.example.toml](../../../hostcensus.example.toml) 复制为 `hostcensus.toml`，并填入你所管理的网络：

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

`preflight` 解析选项与配置方案的逻辑与 `scan` 完全一致（包括用于检查打开文件数限制的 `--concurrency`），因此预检通过意味着 `scan` 将以相同的执行计划启动。

配置方案支持 `network`、`exclusions`、`services`、`ports`、`backend`、`timeout`、`concurrency` 和 `max_hosts` 字段。`services` 和 `ports` 沿用现有的逗号分隔列表语法。显式传入的 CLI 选项会覆盖配置方案中的设置；重复指定 `--exclude` 会在配置方案排除列表的基础上追加排除项。搭配 `--profile` 显式指定的网络必须包含在该配置方案的 IP/CIDR 范围之内。直接扫描仍支持主机名，但主机名不能与 IP 排除规则组合使用。主机数量上限在应用排除规则前检查，而总探测次数上限在排除之后仍会生效。被排除的主机既不会进行服务检查，也不会参与可选的 Nmap 主机发现。

每次扫描在向目标发送流量前都会执行本地预检：检查目标/探测数量限制、输出目标路径访问权限、可选 Nmap 可执行文件/封装器可用性、历史数据库模式以及配置的 TLS CA 证书包。`preflight` 会输出 JSON 报告，不会实际扫描目标，也不会创建历史数据库。它会通过临时写入同级文件来测试输出目标的写入权限，而不会修改已有文件内容。默认的 asyncio 后端依然既不需要 Nmap 也不需要 root 权限。各输出路径之间以及输出路径与输入配置文件之间必须互不相同（包括硬链接）；目标路径若为符号链接将被拒绝。预检失败返回退出码 1；范围或配置无效返回退出码 2。

报告和导出脚本的写入要求操作系统支持 `O_NOFOLLOW`。在不支持该标志的平台（包括 Windows）上，写入操作会直接失败，而不会打开或截断目标文件。新建的报告和导出脚本权限为仅所有者可读写（模式 0600）；替换已有文件时会保留其原有权限。向没有读取端的命名管道写入会立即失败，而不会阻塞等待。新建的 `--history` 数据库同样仅限所有者访问；已存在的数据库保留其原有权限模式。日志信息始终输出到 stderr，以确保 stdout 仅包含结果数据。包含凭据的导出文件始终强制使用 0600 权限。

历史记录为可选开启功能，与现有的 JSON 快照及 `diff` 命令形成互补：

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

请使用 `history` 返回的扫描 ID（上例假设使用的是新建数据库）。快照以事务方式保存，记录 UTC 开始/结束时间、包版本、生效的非敏感配置、摘要信息以及所有主机/服务的观测结果（包括每台主机的错误信息）。未完整探测的主机观测结果也会保留。被取消的运行不会保存。现有的报告、快照、导出及扫描退出码契约均保持不变。

`history` 会列出 JSON 摘要信息，而无需读取所有历史设备详情负载。`compare` 会读取两次已保存的扫描记录，要求两者的目标标识和所选端口完全一致，并报告可达性、状态及端口状态变化。较早的扫描 ID 必须位于较晚的 ID 之前。当两次扫描均记录了 `timeout` 或 `backend` 且其值不同时，报告会列出警告但仍继续对比观测结果。不同的超时等待时间可能会使原本被过滤的端口看起来呈开放状态。扫描器错误和未知端口观测结果会被标记为不确定，而非视为已确认的消失或关闭：出现错误的主机会出现在 `uncertain_hosts` 中，涉及 `unknown` 的所有端口状态变化（包括两次扫描均为 unknown）都会列入 `unconfirmed_ports` 而非 `port_changes`，但若端口在较晚的扫描中变为开放，则计为端口变更。`compare` 和 `diff` 采用相同的端口分类规则。`no_longer_responding` 仅表示未收到响应，并不能证明设备已被移除。扫描退出码为 0 并不保证每台主机都响应了探测：请检查各主机的错误信息。无论是否存在变更，`compare` 成功时均返回退出码 0；现有的文件 `diff` 命令仍保留发现变更返回退出码 3 的契约。不支持或已损坏的历史数据库返回退出码 1。

历史数据库保存着网络资产盘点信息，因此请选择具有适当权限保护的本地目录。配置文件和已存储的设置均不包含 SNMP 凭据；凭据处理继续沿用现有的运行时选项或环境变量机制。

## 盘点差异对比（diff）

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

快照文件为 JSON 格式，包含 `format: "hostcensus-snapshot"`、`version: 1`、hostcensus 版本号、UTC 创建时间、扫描目标、扫描时记录的 `timeout` 和 `backend`（如有）、已探测的服务列表，以及与 `-o` 报告结构相同的存活主机列表。离线主机不包含在内。`diff` 同样支持普通的 `scan -o` JSON 报告，包括在 `services` 字段引入之前生成的旧报告。

`diff` 会报告新增和消失的主机、两次扫描中均存在的主机上新开放或新关闭的端口，以及 `version` 发生变化的服务。仅在其中一次扫描中探测的端口不参与对比，并会输出警告提示。失败的观测结果绝不会被解读为“无变化”：若某个端口在任一次扫描中为 `unknown` 且在后一次扫描中未开放，它将被列入 `unconfirmed` 而非 `closed`，其中 `before` 为 `open`、`unknown` 或 `not-open`（已探测且处于关闭或被过滤状态），`after` 为 `unknown` 或 `not-open`；若端口当前处于开放状态，即使先前的探测失败，也会报告在 `opened` 中。如果某台主机在任一次扫描中所有探测均失败且无任何响应，它会被列入 `unsettled_hosts`（`before`/`after` 取值为 `up`、`uncertain` 或 `absent`，包括两次均失败或另一文件中缺失的情况）而非 `vanished_hosts`；如果该主机在后一次扫描中正常响应，它还会作为新增主机连同其开放端口一并报告。快照会保留这些探测失败的主机正是出于此原因。此外，当扫描目标不一致，或两个文件均记录了超时时间/后端且值不相同时，也会给出警告。指定 `-o PATH` 还可将 JSON 格式的对比结果写入文件。

因触发 `--deadline` 而提前终止的扫描报告（`"complete": false`）仅包含已扫描到的主机，因此 `diff` 和 `export` 默认会拒绝处理并以退出码 2 退出。传入 `--allow-partial` 可允许处理此类报告，同时在 stderr 输出警告：此时 `diff` 会将不完整扫描完全未列出的主机归入 `unsettled_hosts` 并标记为 `unscanned`，而不是视为消失（报告中已明确列为离线的主机仍视为消失），将 `partial` 设为 true，且绝不会报告“无变化”；`export` 则会在生成的脚本头部写入一条警告。

`diff` 退出码说明：`0` 表示无变化；`3` 表示发现变更、存在无法确认的观测结果或输入不完整（只要包含 `unsettled_hosts` 和 `unconfirmed` 在内的任一列表非空，或 `partial` 为 true，`changed` 即为 true）；`2` 表示文件缺失、不可读、不是受支持的快照格式，或未加 `--allow-partial` 的不完整报告；`1` 表示无法写入 `-o` 指定的文件。

## Kadupul 导出

[Kadupul](https://github.com/kadupulhq/kadupul)（Cacti 1.2.31 的一个分支版本）没有批量设备文件导入功能。其官方支持通过脚本添加设备的方式是调用 `cli/add_device.php`，每次调用添加一台设备并传入 `--option=value` 参数。`hostcensus export` 会生成包含这些调用命令的 POSIX `sh` 脚本：

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

每台存活主机都会生成一条 `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` 命令：

- 扫描期间 SNMP 查询成功的主机会带有 `--version=2 --community=...` 或 `--version=3 --username=... --authproto=... --password=...`（若为 authPriv 还会附带 `--privproto`/`--privpass`）、`--port` 以及 `--avail=snmp`。导出 SNMPv3 需要指定 `--snmp-user`，且拒绝使用 noAuthNoPriv 模式，因为 `add_device.php` 必须提供 v3 密码。
- 其他主机会带有 `--version=0 --avail=ping`；若有开放的 TCP 端口，则附带 `--ping_method=tcp --ping_port=`（取第一个开放的 TCP 端口），否则使用 ICMP。
- `--notes` 列出开放的服务及其版本。`--description` 在反向 DNS 名称为纯常规字符（字母、数字、`.`、`_`、`-`）时使用该名称，否则使用 IP 地址，并保证其唯一性，因为 `add_device.php` 会将已存在的描述视为对对应设备的更新操作。

所有参数值都会经过校验并使用 `shlex.quote` 进行 shell 转义。默认情况下不会写入任何 SNMP 密钥：生成的脚本会在运行时展开 `HOSTCENSUS_SNMP_COMMUNITY`、`HOSTCENSUS_SNMP_AUTH_KEY` 或 `HOSTCENSUS_SNMP_PRIV_KEY`，若其中任一必需变量未设置则立即终止。传入 `--include-credentials` 会将上述环境变量的值直接写入脚本，以 0600 权限创建该文件，并记录一条警告。需要注意，`add_device.php` 本身会打印团体字并通过命令行参数接收密钥，因此每次调用执行期间，这些密钥在 Kadupul 服务器的进程列表中均可见。

遇到重复设备或错误时，`add_device.php` 会以退出码 1 退出；生成的脚本会继续处理其余主机并统计失败次数，若有任意设备未能添加成功，脚本最终以退出码 1 退出。模板 ID 可通过 `php cli/add_device.php --list-host-templates` 查询。`export` 退出码说明：`0` 表示脚本写入成功；`2` 表示输入不可读、未加 `--allow-partial` 的不完整扫描，或包含无法安全导出的数据；`1` 表示脚本写入失败。

## 版本控制与发布流程

hostcensus 遵循[语义化版本控制（SemVer）](https://semver.org/spec/v2.0.0.html)：兼容性修复递增修订号（patch），兼容性新特性/弃用变更递增次版本号（minor），破坏性兼容性变更递增主版本号（major）。命令与选项、退出码以及 JSON Schema 构成公开契约；已弃用的行为会保留至下一个主版本发布，除非安全修复要求提前调整（届时会在变更日志中说明原因）。

release-please 会根据 `main` 分支上的 Conventional Commit 提交标题自动创建发布 PR，更新 `pyproject.toml`、`uv.lock` 和 `CHANGES.md` 中的版本号。合并该 PR 后会创建 `vMAJOR.MINOR.PATCH` 标签及 GitHub Release 草稿，随后 CI 会将经过测试的 wheel 包、源码分发包及校验和文件上传至该草稿；GitHub 会通过其证明（attestations）API 为这些文件存储构建证明。文件上传完成后，由维护者审核并正式发布该草稿。已发布的版本绝不会被替换。

PyPI 可信发布（trusted publishing）为可选配置，需要具备项目所有权、配置受信任的发布者以及 `pypi` 环境。它无需重新构建或存储 API 令牌即可直接发布相同的经检验发布产物。本公开仓库中的带标签版本会自动生成 GitHub 产物证明；私有复刻（fork）仓库需要受支持的套餐计划并显式启用。有关环境设置、具体命令及重试步骤，请参阅[完整发布指南](../../../docs/releasing.md)。

## 开发

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

开发工具定义在 `pyproject.toml` 的 [PEP 735](https://peps.python.org/pep-0735/) 依赖组（`dev`、`fuzz`、`build`）中，因此绝不会出现在已发布软件包的元数据中。`uv.lock` 是唯一的锁文件；CI 使用 `uv sync --locked` 安装依赖，若锁文件过期则会构建失败。可通过 `uv python`、mise（`mise exec python@3.14 -- uv sync --locked`）或任意 Python 3.12+ 解释器来选择运行环境。

CI 强制要求代码覆盖率不低于 90%。单元测试包含受控的环回测试服务器以及离线的配置方案/历史记录/发布校验用例；Compose 集成测试环境在隔离网桥上运行 OpenSSH、MariaDB、nginx 和 net-snmp。可通过 `make test-integration` 运行集成测试。另请参阅 [CONTRIBUTING.md](../../../CONTRIBUTING.md) 和[发布工具说明](../../../scripts/README.md)。

运行时容器以 UID/GID 10001 身份运行，无主目录、无登录 shell 且未安装 pip，仅可写入 `/app/output`。请确保该用户对挂载的任意输出目录拥有写入权限。容器不需要任何特权能力，并支持只读根文件系统，因此可按如下方式运行：

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

在此容器内，Nmap 会使用其非特权 TCP 主机发现模式。只要 Trivy 扫描报告任何可修复的 HIGH 或 CRITICAL 级别漏洞，CI 的镜像构建就会失败。

## 供应链安全检查

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) 会在 main 分支及每周定期运行，公布真实评分并将检测结果上传至 GitHub 代码扫描。GitHub Actions 和容器基础镜像均通过不可变哈希固定；Python 依赖通过 `uv.lock` 锁定。Bandit 检查未通过会导致 CI 失败，同时在无网络访问的环境下使用有界 Atheris 模糊测试对 SSH、MySQL、HTTP、证书以及 SNMPv3 BER 解析器进行测试。

Scorecard 还会评估历史评审活动、贡献者多样性以及发布溯源信息。这些评分反映的是实际客观证据，并不代表已满足所有治理或历史发布检查项。请参阅 [SECURITY.md](../../../SECURITY.md) 和[发布溯源说明](../../../docs/releasing.md)。

## 本地化支持

CLI 消息及终端摘要/差异对比表格支持 45 种语言区域（`en`、`de`、`es`、`fr`、`it`、`pt-BR`、`nl`、`ru`、`uk`、`ja`、`ko`、`zh-CN`、`zh-TW`、`ar`、`hi`、`pl`、`tr`、`sv`、`vi`、`id`、`af-ZA`、`am-ET`、`ar-EG`、`ar-MA`、`fr-MA`、`fr-SN`、`ha-NG`、`ig-NG`、`mg-MG`、`rw-RW`、`so-SO`、`sw-KE`、`xh-ZA`、`yo-NG`、`zu-ZA`、`bn`、`fa`、`he`、`mr`、`ta`、`te`、`th`、`ur`、`ms`、`fil`），且无需任何额外运行时依赖。语言解析优先级依次为 `--lang`、`LC_ALL`、`LC_MESSAGES` 和 `LANG`，若均未匹配则回退为 `en`。在所有语言区域下，JSON Schema、CSV 列名以及导出的脚本均保持不变。

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## 参与贡献

提交贡献时应附带可复现的用例，保持文档中规定的 CLI 与数据格式契约，并通过上述各项质量检查。有关开发工作流，请参阅 [CONTRIBUTING.md](../../../CONTRIBUTING.md)；有关兼容性与版本决策，请参阅[发布指南](../../../docs/releasing.md)。

## 安全性与许可证状态

有关漏洞私密报告方式及受支持的版本，请参阅 [SECURITY.md](../../../SECURITY.md)。hostcensus 基于 [MIT 许可证](../../../LICENSE)授权发布。

源码文件头均使用 SPDX 标识符，并保留 Git 历史中的贡献者署名。署名详情请参阅 [AUTHORS.md](../../../AUTHORS.md)。二进制测试抓包文件及生成的锁文件采用同目录的 `.license` 声明文件；MIT 许可证全文位于 `LICENSES/MIT.txt`。
