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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · **日本語** · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus は、自身が管理するネットワーク上で再現性のあるサービスインベントリを取得するための Python CLI です。デバイスが公開しているサービスを記録し、時系列での観測結果を比較して、Kadupul インポートスクリプトを生成します。デフォルトのバックエンドは root 権限なしで asyncio ソケットを使用します。オプションの Nmap ディスカバリを有効にすると、設定済みのサービスポート以外のホストも識別できます。

## hostcensus を使う理由

単発のポートレポートでは、次の観測で実際に変化があったのか、単に観測に失敗したのかを判別できません。hostcensus は、明示的なサービス状態、上限付きプローブ、再利用可能なスキャンプロファイル、およびローカル履歴を組み合わせています。運用者は同じスコープで繰り返しスキャンを実行し、エラーを確認し、不確実な観測結果と確定した変更を明確に区別できます。

- **サービスの証跡:** SSH 識別情報、MySQL グリーティング、HTTP ヘッダー、TLS 証明書の観測情報、および SNMP ディスカバリまたは認証情報を用いた system-MIB クエリ。
- **再現可能なスコープ:** 名前付き TOML プロファイル、追加可能な除外設定、設定可能なサービス、ホスト数・プローブ数の上限、および上限付きワーカー。
- **トラフィック送信前のチェック:** ローカルのプリフライトチェックにより、ターゲット、ツール、出力先へのアクセス権限、履歴スキーマ、設定された TLS CA バンドルを検証します。
- **インベントリ履歴:** トランザクション対応の SQLite スナップショットがすべての観測結果を保持し、比較時にはスキャナーの失敗や不明な状態も可視化したまま維持します。
- **相互運用性の高い出力:** ターミナル出力、JSON・CSV レポート、バージョン付きファイルスナップショット、および Kadupul インポートスクリプト。

CI は Linux および macOS 上の Python 3.12、3.13、3.14 と、制御された Compose 統合ラボを対象としています。コードではこれらのランタイムバージョンへの対応を維持しつつ、モダンな型エイリアス、型付きプリフライト結果、キーワード専用の slotted プロファイル、および構造化された非同期クリーンアップを使用しています。SemVer 互換性の規約と GitHub リリース手順については [バージョニングとリリース](../../../docs/releasing.md) を参照してください。リリースバッジは公開済みアーティファクトを示すものであり、チェックアウトの状態を示すものではありません。現在の最新公開タグは `v0.3.0` ですが、このチェックアウトのパッケージバージョンは `3.0.0` です。ここで説明するインベントリ機能を利用するには、チェックアウトからインストールしてください。

まず [インストール](#install) から始め、次に [プロファイルと履歴](#inventory-profiles-preflight-and-local-history) に進んでください。連携の詳細については、[サービスフィンガープリント](#fingerprints)、[ファイル比較](#inventory-diff)、および [Kadupul エクスポート](#kadupul-export) を参照してください。

## インストール

Python 3.12 以降が必要です（テスト済みマトリクスは Python 3.12–3.14）。このチェックアウトから、ロックされたランタイム依存関係をインストールします:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

オプションの Nmap ホストディスカバリを使用する場合は、ご利用のプラットフォームのパッケージマネージャーで Nmap 実行ファイルをインストールしてください。追加の Python パッケージは不要です。Nmap の XML 出力はコア依存関係である defusedxml で解析されるため、エンティティ展開は拒否されます。hostcensus は `PATH` 上で見つかった `nmap` を、固定の引数リスト、プレフィックスサイズに応じて増加するデッドライン、および 64 MiB の出力上限付きで直接実行します。デフォルトのバックエンドでは Nmap は不要です。

## netprobe からの移行

hostcensus は、3.0.0 でリリースされた netprobe の新しい名称です。このプロジェクトはどちらの名前でも PyPI には公開されておらず、インストールはチェックアウトまたは GitHub リリースから行われてきました。GitHub リポジトリ名は従来のまま維持されます。

| 変更前 | 変更後 | 互換性 |
| --- | --- | --- |
| ディストリビューション `netprobe` | `hostcensus` | チェックアウトから再インストールしてください。旧名称のパッケージはありません。 |
| `netprobe` コマンド | `hostcensus` | `netprobe` も引き続き動作し、stderr に非推奨の警告を 1 行出力します。終了コードと stdout は変更されません。次のメジャーリリースで削除されます。 |
| `NETPROBE_*` 環境変数 | `HOSTCENSUS_*` | 対応する `HOSTCENSUS_*` 変数が未設定の場合に `NETPROBE_*` 変数が使用され、変数名のみ（値は含まない）を含む警告が stderr に 1 回出力されます。両方設定されている場合は `HOSTCENSUS_*` が優先されます。次のメジャーリリースで削除されます。 |
| `import netprobe`、`python -m netprobe` | `import hostcensus`、`python -m hostcensus` | **破壊的変更。** インポート用の互換シムはインストールされないため、インポート文を更新してください。 |
| Docker イメージタグ `network-discovery:test`（CI 専用）およびコンテナユーザー `netprobe` | `hostcensus:test`、ユーザー `hostcensus` | レジストリイメージが公開されたことはありません。イメージを再ビルドし、`hostcensus` エントリポイントを使用してください。 |
| `netprobe.toml`、`netprobe-history.sqlite3` | `hostcensus.toml`、`hostcensus-history.sqlite3` | 新しい名前のファイルが存在しない間は、旧デフォルト名の既存ファイルが警告付きで引き続き使用されます。明示的な `--config` および `--history` パスは影響を受けません。 |
| `"format": "netprobe-report"` または `"netprobe-snapshot"`、および `netprobe_version` フィールドを含むレポートとスナップショット | `hostcensus-report`、`hostcensus-snapshot`、`hostcensus_version` | `diff` と `export` は旧名称で書き出されたファイルも引き続き読み込み可能で、公開されている JSON スキーマも両方の表記を受け入れます。新しいファイルには新しい名称が使用されます。SQLite 履歴データベースに変更はなく、以前と同様に読み込めます。 |
| `netprobe export` による Kadupul スクリプト | `hostcensus export` によるスクリプト | 古いスクリプトも引き続き動作し、実行時には `NETPROBE_SNMP_*` を読み込みます。新しいスクリプトは `HOSTCENSUS_SNMP_*` を読み込みます。 |

## クイック例

「開発」セクションで説明する統合ラボのテスターコンテナから実行した例です（出力は一部省略）:

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

## 終了コード

| コマンド | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | 観測結果・レポートを記録 | プリフライト/バックエンドの失敗、履歴またはレポート/スナップショットの書き込み失敗 | 無効なターゲット、オプション、設定、または上限超過 | - | `--deadline` に到達。部分レポートを書き込み、履歴とスナップショットはスキップ |
| `preflight` | チェック成功 | ローカルチェック失敗 | 無効なターゲット/設定、または出力先の競合 | - | - |
| `profiles` | 検証済みプロファイルを一覧表示 | - | 設定または選択の読み込み不可/無効 | - | - |
| `history` | サマリーを一覧表示 | 履歴の欠落、無効、または非対応 | 無効な CLI オプション | - | - |
| `compare` | 比較結果を出力（変更がある場合を含む） | 履歴の読み込み不可、スコープ/順序の非互換、または書き込み失敗 | 無効な CLI オプション | - | - |
| `diff` | 変更なし | `-o` ファイルを書き込めなかった | 入力の欠落、読み込み不可または非対応、あるいは `--allow-partial` なしの不完全なスキャン | 変更を検出、未確認の観測結果あり、または不完全なスキャン | - |
| `export` | スクリプトを書き込み | スクリプトを書き込めなかった | 入力の読み込み不可、`--allow-partial` なしの不完全なスキャン、または安全にエクスポートできないデータ | - | - |

## モジュール構成

| モジュール | 責務 |
| --- | --- |
| `cli.py` | コマンドオプション、プロファイル解決、プリフライト、スキャンおよびレポート出力 |
| `scanner.py`, `probes.py` | ターゲット展開、上限付きワーカー、ホストディスカバリおよびサービス観測 |
| `config.py`, `profiles.py` | サービス定義および検証済みインベントリプロファイル |
| `models.py`, `output.py` | 結果型およびターミナル/JSON/CSV レンダリング |
| `history.py`, `diff.py` | SQLite 履歴およびバージョン付きファイルスナップショットの比較 |
| `preflight.py` | ローカルチェックおよび上限付き Nmap バージョン確認 |
| `export.py` | 検証・クォート済みの Kadupul インポートスクリプト生成 |

各サービス観測は、その状態（state）を通知された識別情報（advertised identity）とは分けて記録します。読み込みとデッドラインには上限が設定されており、プローブ中の例外はホストエラーとして保持されます。SQLite 履歴はトランザクション、明示的な接続クリーンアップ、および読み取り専用の一覧表示・比較パスを使用します。SNMP シークレットは環境変数またはシークレットファイル経由でのみ渡され、インベントリ履歴にはシークレットを含まない実効設定のみが保存されます。スキャンパイプライン、各種上限、信頼境界については [アーキテクチャ](../../../docs/architecture.md) を、許可された利用範囲については [SECURITY.md](../../../SECURITY.md#authorized-use) を参照してください。


## 使い方

自身が管理するネットワークのみをスキャンしてください。

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| オプション | 説明 |
| --- | --- |
| `NETWORK` | CIDR、IP、またはホスト名（`--profile` 使用時は省略可）。IPv6 スコープ識別子は拒否されます。 |
| `-o, --output PATH` | レポートを書き出します。形式は拡張子（`.json`、`.csv`）に従い、その他の拡張子は JSON にフォールバックします。 |
| `-f, --format json\|csv\|kadupul\|auto` | レポート形式を強制指定します。`--output` なしでは効果がありません。`.sh` は `kadupul` を選択します。 |
| `-v, --verbose` | デバッグログを出力します。 |
| `-q, --quiet` | 結果、進捗、および情報ログを抑制します。警告とエラーは引き続き stderr に出力されます。 |
| `--backend asyncio\|nmap` | ホストディスカバリ方式。`asyncio`（デフォルト）はサービスポートを直接プローブします。`nmap` は先に nmap の ping スイープを実行するため、`PATH` 上に `nmap` 実行ファイルが必要です。 |
| `--timeout SECONDS` | 独自の予算を設定していないプローブの待機時間（デフォルト 1.0）。組み込みの接続プローブは、サービステーブルで `timeout` が設定されていない限り 0.3 秒を使用します。 |
| `--concurrency N` | 同時に実行するプローブ数（デフォルト 256）。 |
| `--deadline SECONDS` | nmap スイープを含むスキャン全体をこの時間（秒）で停止します（デフォルト 3600、最大 604800、環境変数 `HOSTCENSUS_DEADLINE`）。完了したホストは `"complete": false` としてレポートに書き出され、履歴とスナップショットは書き込まれず、`scan` は終了コード 4 で終了します。 |
| `--config PATH` | TOML 形式のサービス定義およびオプションの名前付き `[profiles]` 設定。 |
| `--profile NAME` | 名前付きプロファイルを使用します。`--config` を省略した場合のデフォルトは `hostcensus.toml` です。 |
| `--exclude IP/CIDR` | 除外対象を追加します（必要に応じて複数回指定可能）。除外された IPv4 ホストは、それに到達する IPv6 アドレス（IPv4 マップアドレス `::ffff:a.b.c.d`、NAT64 `64:ff9b::/96`、6to4）も除外します。IPv4 マップのターゲットおよび除外指定は、それらが表す IPv4 アドレスとして扱われます。 |
| `--max-hosts N` | 除外適用前にチェックされるアドレス数の上限（デフォルトおよびハード上限は 65,536）。 |
| `--history PATH` | 完了したスキャンをオプトインの SQLite 履歴データベースに記録します。 |
| `--services NAMES` | チェックするサービス名のカンマ区切りリスト（指定順で実行、デフォルトはすべて）。 |
| `--ports SPEC` | `NAME=PORT`（サービスのポート変更）または `PORT`（`tcp-PORT` という名前のプレーン TCP チェックを追加）のカンマ区切りリスト。 |
| `--snmp-community-file PATH` | system MIB クエリ用の SNMPv2c コミュニティ名を格納したファイル。環境変数: `HOSTCENSUS_SNMP_COMMUNITY`（値）または `HOSTCENSUS_SNMP_COMMUNITY_FILE`（パス）。 |
| `--snmp-user` | SNMPv3 ユーザー名。環境変数: `HOSTCENSUS_SNMP_USER`。 |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`、`SHA`（デフォルト）、`SHA224`、`SHA256`、`SHA384`、`SHA512`、およびパスフレーズを格納したファイル。環境変数: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`、`HOSTCENSUS_SNMP_AUTH_KEY` または `HOSTCENSUS_SNMP_AUTH_KEY_FILE`。 |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`、`AES`（デフォルト）、`AES128`、`AES192`、`AES192C`、`AES256`、`AES256C`、およびパスフレーズを格納したファイル。環境変数: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`、`HOSTCENSUS_SNMP_PRIV_KEY` または `HOSTCENSUS_SNMP_PRIV_KEY_FILE`。 |
| `--save-snapshot PATH` | `hostcensus diff` 用のバージョン付きスナップショットも同時に書き出します。 |
| `--tls-ca-file PATH` | システムストアの代わりにこの PEM バンドルに対して HTTPS 証明書を検証します。環境変数: `HOSTCENSUS_TLS_CA_FILE`。 |

デフォルトでは、各ホストに対して SSH（TCP 22）、SNMP（UDP 161）、MySQL（TCP 3306）、HTTP（TCP 80）、HTTPS（TCP 443）がチェックされます。TCP ポートはフルコネクトでテストされます。SNMP は SNMPv3 エンジンディスカバリリクエストでテストされます。SNMPv3 エージェントは認証情報なしでこのリクエストに応答する必要がありますが、v1/v2c のみに対応するエージェントはこのプローブでは検出されません。asyncio バックエンドでは、接続拒否を含め何らかの応答を返したプローブがあればホストは生存（alive）とみなされるため、すべてのプローブをドロップするホストは `alive=false` となり「Host is down」エラーが記録されますが、これは物理的に停止していることを証明するものではありません。`--backend nmap` を指定した場合、どのホストが生存しているかは nmap が判定します（root 権限時は ICMP、それ以外は TCP 80/443）。

### フィンガープリント

open な各サービスは、ログイン前に送信される内容からフィンガープリントが取得されます。認証を行うのは SNMP クエリのみであり、それも認証情報を指定した場合に限られます。

| プローブ | 読み取り対象 | `version` | `details` キー |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 識別行 | ソフトウェア名（例: `OpenSSH_10.0`） | `protocol`、`software`、`comments` |
| `mysql` | MySQL/MariaDB 初期ハンドシェイク | サーバーバージョン | `server_version`、`flavor`、`auth_plugin`、または `error_code`/`error` |
| `http` | `HEAD /` レスポンス | `Server` ヘッダー | `status`、`server` |
| `https` | TLS ハンドシェイク、証明書、`HEAD /` | `Server` ヘッダー | `tls_version`、`cert_verified`、`cert_verify_error`、`cert_subject`、`cert_issuer`、`cert_sans`、`cert_not_before`、`cert_not_after`（UTC ISO 8601）、`cert_self_signed`、`status`、`server` |
| `snmp` | SNMPv3 ディスカバリ。認証情報ありの場合は sysDescr、sysObjectID、sysName の GET | sysDescr | `engine_id`。認証情報ありの場合は `snmp_version`、`sys_descr`、`sys_object_id`、`sys_name`、または `snmp_error` |

ホスト名ターゲットはホストごとに 1 回だけ名前解決され、すべてのプローブはそのアドレスに接続します（結果には `address` として記録されます）。ホスト名は TLS SNI、証明書検証、および HTTP `Host` ヘッダーにのみ使用されます。名前解決できない場合は `unknown` 状態と `Cannot resolve` エラーになります。逆引き DNS 名はホスト名として有効な文字のみを含む場合に保持され、同時に実行されるルックアップは最大 16 件です。HTTPS はシステムストアまたは `--tls-ca-file` に対して証明書とホスト名の検証を行います。トラストストアはスキャンにつき 1 回だけ読み込まれ、すべての HTTPS プローブで再利用されます。TCP 接続と TLS ハンドシェイクは別々にタイムアウト計測されるため、接続は受け入れるもののハンドシェイクで停止するポートは `filtered` ではなく `tls_error` 付きの `open` となります。検証に失敗した場合、結果には `cert_verified: false` と `cert_verify_error` が記録され、より弱い設定での再試行や HTTP リクエストの送信は行われません。証明書詳細と HTTP ヘッダーは検証が成功した後にのみ収集されます。プライベート CA を使用するサービスには正しい CA バンドルを指定してください。古いレポートには `cert_read_unverified` が含まれる場合がありますが、現在のプローブでは生成されません。

SNMP シークレットは環境変数またはファイル（`--snmp-*-file` または対応する `HOSTCENSUS_SNMP_*_FILE` 変数）からのみ読み込まれ、他のローカルユーザーがプロセス一覧から参照できるコマンドライン引数からは決して読み込みません。値を伴う `--snmp-community`、`--snmp-auth-key`、`--snmp-priv-key` は終了コード 2 で終了し、代替手段を表示します。シークレットファイルは 4096 バイト以下の空でない UTF-8 である必要があり、末尾の改行 1 つは無視されます。同じシークレットに対して環境変数とファイルの両方を設定するとエラーになります。エラーメッセージにはファイル名が含まれますが、中身は決して出力されません。スキャンレポートと履歴には意図的に認証情報の値を含めない設計になっています。エクスポーターには後述の独立した明示的オプション `--include-credentials` があります。コミュニティを指定すると SNMPv2c が選択され、ユーザーを指定すると SNMPv3 が選択されます。認証キーを指定すると認証が有効になり、両方のキーを指定すると暗号化（privacy）が有効になります（どちらが使われたかは `snmp_security_level` に記録されます）。hostcensus は、コミュニティと v3 ユーザーの併用、認証キーなしでの暗号化キーの使用、ユーザーなしでのキーの使用を終了コード 2 で拒否し、失敗した v3 クエリを v2c やより低いセキュリティレベルで再試行することは決してありません。v1/v2c のみに対応するエージェントは認証情報なしの v3 ディスカバリを無視するため、コミュニティが指定された場合にのみ open として表示されます。

バナーテキストは印字可能な文字のみに整理され、保存または表示の前に 256 文字を上限として切り詰められます。読み込みサイズにも上限があり、1 行あたり 4 KiB、MySQL グリーティングは 4 KiB、HTTP ヘッダーは 16 KiB です。32 オクテットを超える SNMP エンジン ID は保存前に切り詰められます。HTTP および HTTPS は、IPv6 アドレスを角括弧で囲み、80 または 443 以外のポートの場合はポート番号を付けた Host ヘッダーを送信します。表計算ソフトの数式トリガーで始まる CSV セルには、テキストとして維持されるようプレフィックスが付与されます。

### 上限と制限

1 回の実行で受け付ける上限は、最大 65,536 アドレス、64 サービス、および 524,288 プローブ（ホスト数 × サービス数）です。これを超えるリクエストはトラフィックを送信する前に終了コード 2 で終了します。`--concurrency` の上限は 4096 ソケットです。各プローブには、自身の予算の 4 倍のハードデッドラインが設定されます。接続プローブ（`tcp`、`ssh`、`mysql`、`http`）は、そのサービスで `timeout` が設定されていない限り 0.3 秒を使用します。SNMP と HTTPS は、個別設定がない場合に `--timeout`（デフォルト 1.0）を使用します。デッドラインに達したプローブは `unknown` として報告され、`errors` に "probe timed out" が記録されます。ローカルのソケット障害（例: ファイルディスクリプタの枯渇）もエラーが記録されたうえで `unknown` となり、フィルタされたポートやダウン状態のホストとして扱われることはありません。プローブ実行前に、hostcensus は `--concurrency` に 64 を加えたディスクリプタ数を確保できるよう、オープンファイル数のソフトリミットをハードリミットに向けて引き上げます。引き上げられない場合は `open files` プリフライトチェックが失敗し、`scan` はトラフィック送信前に終了コード 1 で終了します。Nmap ディスカバリは 30 秒のホストタイムアウトを使用します。プレフィックスは CIDR 形式で nmap に渡され、nmap が渡された数より少ないアドレスしか報告しなかった場合（例: 名前解決できない名前）、ホストをダウンとみなすのではなく終了コード 1 でスイープを失敗させます。ホスト名ターゲットは 1 回解決されてそのアドレスが nmap に渡されるため、ディスカバリとプローブは同じマシンに到達します。除外なしのフルプレフィックスは 1 つの nmap プロセスで実行され、サブプロセスのデッドラインは 256 アドレスごとに 35 秒（切り上げ）です。除外を含むスイープでは 256 ホストずつのバッチを使用し、各バッチに 35 秒のデッドラインを設定します。ワーカーの作成数はアドレス範囲のサイズとは無関係に上限が設けられています。逆引き DNS とホスト名の解決には別の 2 秒デッドラインがあり、応答を返さないリゾルバ呼び出しは専用スレッド上に放棄されるため、これらの上限を超えて hostcensus が実行され続けることはありません。同時に実行されるルックアップは最大 16 件であり、放棄された呼び出しは戻るまでスロットを占有し続けるため、ハングしたスレッドの数は上限内に抑えられます。16 スロットすべてがハングした場合、後続のルックアップは 2 秒デッドラインの外側で空きスロットを待機し（デッドラインはスロットが空いた時点から開始）、`--deadline` がスキャンを停止するまで待ちます。`deadline` を指定せずにライブラリとして `NetworkScanner` を使用した場合、このようなスロットを無期限に待機する可能性があります。さらにこれら全体の上限として、`--deadline`（デフォルト 1 時間）が実行全体を制御します。

### サービスの設定

サービスは TOML ファイルで変更できます:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` には `tcp`、`ssh`、`mysql`、`http`、`https`、`snmp` のいずれかを指定します。デフォルトは、サービス名がプローブ名と一致する場合はその名前、それ以外は `tcp` です。UDP を使用するのは `snmp` のみです。サービス名には小文字の英字、数字、`-`、`_` を使用します。2 つのサービスで同じポートとプロトコルの組み合わせを共有することはできません（履歴はそのペアに対して 1 つの状態を記録します）。`timeout` は省略可能な秒数で、0.05 以上を指定します。接続型プローブ（`tcp`、`ssh`、`mysql`、`http`）のデフォルトは 0.3 秒です。`snmp` と `https` は、サービスに `timeout` が設定されていない場合にスキャンの `--timeout` を使用します。`--timeout` はサービスに既に設定されている予算を上書きしません。

JSON レポートはバージョン付きドキュメント（`"format": "hostcensus-report"`、`"version": 1`）であり、`devices` と並んでターゲット、プローブしたサービス、設定を記録します。`-o` なしで `--format json` を指定すると、テーブルの代わりにレポートが stdout に出力されます。すべての JSON 出力には公開スキーマがあります。詳細は [JSON 出力](../../../docs/json-output.md) を参照してください。デバイスには従来の `ip`、`alive`、`ssh`、`snmp`、`mysql`、`hostname`、`errors` フィールドに加えて、各プローブの `name`、`port`、`protocol`、`state`（`open`、`closed`、`filtered`、またはプローブがローカルで失敗もしくはデッドラインに達した場合は `unknown`）、`version`、`details` を含む `services` リストが追加されます。CSV 出力には、open 状態のサービス向けに末尾の `services` および `versions` 列が追加されます。`ssh`、`snmp`、`mysql` の真偽値は、完全にその名前のサービスに従います。


## インベントリプロファイル、プリフライト、およびローカル履歴

名前付きプロファイルは既存の `[services]` 定義と同じ TOML ファイルを共有します。[hostcensus.example.toml](../../../hostcensus.example.toml) を `hostcensus.toml` にコピーし、自身が管理するネットワークを設定してください:

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

`preflight` はオープンファイル数チェック用の `--concurrency` を含め、`scan` とまったく同じ方法でオプションとプロファイルを解決します。そのため、プリフライトが成功すれば `scan` も同じプランで開始されます。

プロファイルでは `network`、`exclusions`、`services`、`ports`、`backend`、`timeout`、`concurrency`、`max_hosts` を指定できます。`services` と `ports` には既存のカンマ区切りリスト構文を使用します。明示的な CLI オプションはプロファイル設定を上書きし、`--exclude` オプションを繰り返すとプロファイルの除外設定に追加されます。`--profile` とともに明示的なネットワークを指定する場合、そのネットワークはプロファイルの IP/CIDR スコープ内に含まれている必要があります。直接スキャンではホスト名も引き続きサポートされますが、IP 除外と組み合わせることはできません。ホスト数上限は除外適用前に適用され、総プローブ数上限は除外適用後にも適用されます。除外されたホストはサービスチェックとオプションの Nmap ディスカバリの両方から除外されます。

すべてのスキャンはターゲットへのトラフィック送信前にローカルのプリフライトチェックを実行します（ターゲット・プローブ数の上限、出力先へのアクセス権、オプションの Nmap 実行ファイル/ラッパーの可用性、履歴スキーマ、設定された TLS CA バンドル）。`preflight` は JSON を報告し、ターゲットのスキャンや履歴データベースの作成は行いません。既存の内容を変更せずに、同じディレクトリに一時ファイルを作成して出力先へのアクセスをテストします。デフォルトの asyncio バックエンドでは、引き続き Nmap も root 権限も不要です。出力先パスはハードリンクを含め、互いに、および入力設定ファイルと異なる必要があります。出力先のシンボリックリンクは拒否されます。チェック失敗時は終了コード 1、無効なスコープ/設定の場合は終了コード 2 を返します。

レポートおよびエクスポートの書き込みには `O_NOFOLLOW` のサポートが必要です。Windows を含む非対応プラットフォームでは、出力先を開いたり切り詰めたりすることなく書き込みが失敗します。新規作成されるレポートおよびエクスポートスクリプトは所有者のみ読み書き可能（モード 0600）で作成され、既存ファイルを置き換える場合は元のパーミッションが保持されます。読み手のいない名前付きパイプへの書き込みは待機せず即座に失敗します。新規の `--history` データベースも所有者専用で作成され、既存のものは元のモードを保持します。ログメッセージは常に stderr に出力されるため、stdout には結果のみが出力されます。認証情報を含むエクスポートでは常にモード 0600 が強制されます。

履歴機能はオプトインであり、既存の JSON スナップショットおよび `diff` コマンドを補完します:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

`history` から取得した ID を使用してください（上の例は新しいデータベースを想定しています）。スナップショットは UTC の開始/終了時刻、パッケージバージョン、シークレットを含まない実効設定、サマリー、およびホストごとのエラーを含むすべてのホスト/サービス観測結果とともにトランザクションで保存されます。不完全なホスト観測結果も保持されます。キャンセルされた実行は保存されません。既存のレポート、スナップショット、エクスポート、およびスキャン終了コードの契約は維持されます。

`history` はすべての過去のデバイスペイロードを読み込むことなく JSON サマリーを一覧表示します。`compare` は保存された 2 つのスキャンを読み込み、同一のターゲット識別子と選択ポートを要求したうえで、応答性、ステータス、ポート状態の変化を報告します。古い方のスキャン ID は新しい方の ID より前である必要があります。両方のスキャンに `timeout` または `backend` が記録されており、それらの値が異なる場合、レポートには警告が記載されますが観測結果の比較は継続されます。待機時間が異なると、フィルタされたポートが open に見える場合があります。スキャナーのエラーや unknown のポート観測結果は、確定的な消失やクローズとして扱うのではなく不確実（uncertain）としてフラグ付けされます。エラーのあるホストは `uncertain_hosts` に表示され、`unknown` を含むすべてのポート遷移（両方のスキャンで unknown の場合を含む）は `port_changes` ではなく `unconfirmed_ports` に一覧表示されます。ただし、後のスキャンで open になったポートはポート変更として扱われます。`compare` と `diff` は同じルールでポートを分類します。`no_longer_responding` は応答がないことを意味し、デバイスの撤去を証明するものではありません。スキャンの終了コード 0 はすべてのホストが応答したことを保証するものではないため、ホストごとのエラーを確認してください。比較に成功した場合は変更の有無にかかわらず 0 を返します。既存のファイル `diff` は終了コード 3 の契約を維持します。非対応または破損した履歴の場合は 1 を返します。

履歴にはインベントリ情報が保存されるため、適切に保護されたローカルディレクトリを選択してください。プロファイルファイルと保存された設定には SNMP 認証情報は含まれません。認証情報の扱いは引き続き既存のランタイムオプションまたは環境変数を通じて行われます。

## インベントリ差分（diff）

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

スナップショットは `format: "hostcensus-snapshot"`、`version: 1`、hostcensus のバージョン、UTC 作成時刻、ターゲット、スキャン時に記録されていれば `timeout` と `backend`、プローブされたサービス、および `-o` レポートと同じ形式の生存ホストを含む JSON です。ダウン状態のホストは除外されます。`diff` は通常の `scan -o` JSON レポート（`services` フィールドが存在する前のものを含む）も受け付けます。

`diff` は、新規追加および消失したホスト、両方に存在するホスト上で open または closed になったポート、および `version` が変化したサービスを報告します。2 つのスキャンのうち片方でのみプローブされたポートは比較されず、その旨の警告が出力されます。失敗した観測結果が「変更なし」として解釈されることはありません。どちらかのスキャンで `unknown` であり後のスキャンで open でないポートは、`closed` ではなく `unconfirmed` に記載され、`before` には `open`・`unknown`・`not-open`（プローブの結果 closed または filtered）のいずれかが、`after` には `unknown` または `not-open` が記録されます。現在のスキャンで open なポートは、以前のプローブが失敗していた場合でも `opened` に報告されます。どちらかのスキャンですべてのプローブが応答なく失敗したホストは、`vanished_hosts` ではなく `unsettled_hosts` に記載されます（`before`/`after` には `up`、`uncertain`、`absent` が入り、両方のスキャンで失敗した場合や一方のファイルに存在しない場合も含まれます）。後のスキャンで応答した場合は、open ポートを持つ新しいホストとしても報告されます。スナップショットがこれらの失敗したホストを保持しているのはこのためです。ターゲットが異なる場合、および両方のファイルに記録された timeout または backend の値が異なる場合にも警告が表示されます。`-o PATH` を指定すると JSON 形式をファイルにも書き出します。

`--deadline` によって停止されたスキャンのレポート（`"complete": false`）には到達したホストのみが記載されるため、`diff` と `export` は終了コード 2 でこれを拒否します。`--allow-partial` を指定すると stderr に警告を出したうえで受け入れます。その場合、`diff` は不完全なスキャンにまったく記載されていないホストを消失ではなく `unsettled_hosts` に `unscanned` として記載し（down として記載されていたホストは引き続き消失扱いになります）、`partial` を true に設定して「変更なし」とは報告しません。`export` はスクリプトヘッダーに警告を書き込みます。

`diff` の終了コード: `0` は変更なし、`3` は変更の検出・確認できない観測結果・不完全な入力（`unsettled_hosts` や `unconfirmed` を含むいずれかのリストが空でない場合、または `partial` が true の場合は常に `changed` が true になります）、`2` はファイルの欠落・読み込み不可・非対応スナップショット・`--allow-partial` なしの不完全な入力、`1` は `-o` ファイルの書き込み失敗です。

## Kadupul エクスポート

[Kadupul](https://github.com/kadupulhq/kadupul)（Cacti 1.2.31 のフォーク）にはファイルによる一括デバイスインポート機能がありません。スクリプトからデバイスを追加する公式の方法は `cli/add_device.php` であり、1 回の呼び出しにつき 1 台のデバイスを `--option=value` 引数で指定します。`hostcensus export` はこれらの呼び出しからなる POSIX `sh` スクリプトを生成します:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

生存している各ホストは `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` に変換されます:

- スキャンの SNMP クエリが成功したホストには、`--version=2 --community=...` または `--version=3 --username=... --authproto=... --password=...`（authPriv の場合はさらに `--privproto`/`--privpass`）、`--port`、`--avail=snmp` が付与されます。SNMPv3 エクスポートには `--snmp-user` が必要であり、`add_device.php` が v3 パスワードを要求するため noAuthNoPriv は拒否されます。
- その他のホストには `--version=0 --avail=ping` が付与され、最初の open な TCP ポートを用いた `--ping_method=tcp --ping_port=`、または open な TCP ポートがない場合は ICMP が設定されます。
- `--notes` には open なサービスとバージョンが一覧表示されます。`--description` には、逆引き DNS 名が単純な文字列（英字、数字、`.`、`_`、`-`）である場合はその名前、そうでなければ IP アドレスが使用され、`add_device.php` が既存の description をそのデバイスへの更新として扱うため、一意になるように調整されます。

すべての値は検証され、`shlex.quote` でシェルクォートされます。デフォルトでは SNMP シークレットは書き込まれず、スクリプトは実行時に `HOSTCENSUS_SNMP_COMMUNITY`、`HOSTCENSUS_SNMP_AUTH_KEY`、または `HOSTCENSUS_SNMP_PRIV_KEY` を展開し、未設定のものがあれば停止します。`--include-credentials` を指定すると、代わりにそれらの環境変数の値をスクリプト内に書き込み、モード 0600 で作成して警告をログ出力します。なお、`add_device.php` 自体はコミュニティ名を出力し、シークレットを引数として受け取るため、各呼び出しの実行中は Kadupul サーバーのプロセス一覧に表示されます。

`add_device.php` は重複およびエラー時に終了コード 1 で終了します。生成されたスクリプトは処理を継続して失敗回数を数え、追加できなかったデバイスが 1 台でもあれば終了コード 1 で終了します。テンプレート ID は `php cli/add_device.php --list-host-templates` で確認できます。`export` の終了コード: `0` は書き込み完了、`2` は入力の読み込み不可・`--allow-partial` なしの不完全なスキャン・安全にエクスポートできないデータ、`1` はスクリプトの書き込み失敗です。

## バージョニングとリリースプロセス

hostcensus は [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に従います。互換性のある修正はパッチバージョンを、互換性のある機能追加および非推奨化はマイナーバージョンを、互換性を損なう変更はメジャーバージョンをそれぞれインクリメントします。コマンドとオプション、終了コード、および JSON スキーマが公開契約（パブリックコントラクト）となります。非推奨となった動作は、セキュリティ修正により早期の変更が必要な場合（その場合は変更履歴に理由を記載します）を除き、次のメジャーリリースまで引き続き動作します。

release-please は `main` の Conventional Commit タイトルに基づいてリリース PR を作成し、`pyproject.toml`、`uv.lock`、`CHANGES.md` のバージョンを更新します。この PR をマージすると `vMAJOR.MINOR.PATCH` タグとドラフトの GitHub リリースが作成され、CI がテスト済みの wheel、ソースディストリビューション、チェックサムを添付します。GitHub は attestations API を通じてそれらのファイルのビルド証明書（attestation）を保存します。ファイルが添付された後、メンテナーがレビューしてドラフトを公開します。リリースが差し替えられることはありません。

PyPI の Trusted Publishing はオプトイン方式であり、プロジェクトの所有権、Trusted Publisher の設定、および `pypi` 環境が必要です。これにより、再ビルドや API トークンの保存を行うことなく、検証済みの同じリリースアーティファクトを公開できます。この公開リポジトリにおけるタグ付きリリースでは GitHub アーティファクト証明書が生成されますが、プライベートフォークでは対応プランと明示的なオプトインが必要です。セットアップ手順、具体的なコマンド、再試行方法については [完全なリリースガイド](../../../docs/releasing.md) を参照してください。

## 開発

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

開発ツールは `pyproject.toml` 内の [PEP 735](https://peps.python.org/pep-0735/) 依存関係グループ（`dev`、`fuzz`、`build`）に配置されているため、公開パッケージのメタデータには含まれません。`uv.lock` が唯一のロックファイルであり、CI は `uv sync --locked` でインストールを実行し、ロックファイルが古い場合は失敗します。インタプリタは `uv python`、mise（`mise exec python@3.14 -- uv sync --locked`）、または任意の Python 3.12+ で選択してください。

CI はパッケージ全体で 90% のカバレッジ下限を強制しています。ユニットテストには制御されたループバックサーバーやオフラインのプロファイル/履歴/リリース検証ケースが含まれます。Compose ラボは隔離されたブリッジ上で OpenSSH、MariaDB、nginx、net-snmp を実行します。`make test-integration` で実行できます。詳細は [CONTRIBUTING.md](../../../CONTRIBUTING.md) および [リリースツール](../../../scripts/README.md) を参照してください。

ランタイムコンテナはホームディレクトリ、シェルログイン、pip なしの UID/GID 10001 として実行され、`/app/output` に書き込むことができます。マウントする出力ディレクトリにはこのユーザーへの書き込み権限を与えてください。ケイパビリティは不要で、読み取り専用のルートファイルシステムでも動作するため、次のように実行できます:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

このコンテナ内では、Nmap は非特権の TCP ディスカバリ動作を使用します。CI は Trivy が修正可能な HIGH または CRITICAL の脆弱性を報告した場合、イメージビルドを失敗させます。

## サプライチェーンチェック

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) が main ブランチおよび週次で実行され、実際のスコアを公開するとともに検出結果を GitHub コードスキャンにアップロードします。Actions とコンテナベースイメージはイミュータブルなハッシュでピン留めされており、Python 依存関係は `uv.lock` で解決されます。Bandit の失敗は CI を失敗させ、ネットワークアクセスなしの上限付き Atheris ファジングが SSH、MySQL、HTTP、証明書、および SNMPv3 BER パーサーをテストします。

Scorecard は過去のレビュー活動、コントリビューターの多様性、リリースの来歴（provenance）も計測します。これらのスコアは実際の証跡を反映したものであり、ガバナンスや過去のリリースチェックすべてを満たしていることを主張するものではありません。詳細は [SECURITY.md](../../../SECURITY.md) および [リリースの来歴](../../../docs/releasing.md) を参照してください。

## ローカライゼーション

CLI メッセージおよびターミナルのサマリー/diff テーブルは、追加のランタイム依存関係なしで 45 のロケール（`en`、`de`、`es`、`fr`、`it`、`pt-BR`、`nl`、`ru`、`uk`、`ja`、`ko`、`zh-CN`、`zh-TW`、`ar`、`hi`、`pl`、`tr`、`sv`、`vi`、`id`、`af-ZA`、`am-ET`、`ar-EG`、`ar-MA`、`fr-MA`、`fr-SN`、`ha-NG`、`ig-NG`、`mg-MG`、`rw-RW`、`so-SO`、`sw-KE`、`xh-ZA`、`yo-NG`、`zu-ZA`、`bn`、`fa`、`he`、`mr`、`ta`、`te`、`th`、`ur`、`ms`、`fil`）に対応しています。ロケールの解決は `--lang`、次に `LC_ALL`、`LC_MESSAGES`、`LANG` の順で優先され、`en` にフォールバックします。JSON スキーマ、CSV 列、およびエクスポートスクリプトはすべてのロケールで共通です。

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## コントリビューション

コントリビューションには再現可能なケースを含め、ドキュメント化された CLI およびデータ形式の契約を維持し、上記の品質チェックに合格する必要があります。開発ワークフローについては [CONTRIBUTING.md](../../../CONTRIBUTING.md) を、互換性とバージョニングの判断基準については [リリースガイド](../../../docs/releasing.md) を参照してください。

## セキュリティとライセンス状況

非公開の脆弱性報告およびサポート対象バージョンについては [SECURITY.md](../../../SECURITY.md) を参照してください。hostcensus は [MIT License](../../../LICENSE) のもとでライセンスされています。

ソースヘッダーには SPDX 識別子が使用され、Git 履歴からのコントリビュータークレジットが保持されています。著作権表示については [AUTHORS.md](../../../AUTHORS.md) を参照してください。バイナリのテストキャプチャと生成されたロックファイルには隣接する `.license` ファイルが使用されており、MIT ライセンスの全文は `LICENSES/MIT.txt` にあります。
