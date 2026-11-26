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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · **한국어** · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus는 사용자가 관리하는 네트워크에서 반복 가능한 서비스 인벤토리 수집을 수행하는 Python CLI 도구입니다.
장치가 노출하는 서비스를 기록하고, 시간 경과에 따른 관측 결과를 비교하며,
Kadupul 가져오기 스크립트를 생성합니다. 기본 백엔드는 root 권한 없이 asyncio 소켓을 사용하며,
선택 사항인 Nmap 검색을 통해 설정된 서비스 포트 외의 호스트도 식별할 수 있습니다.

## hostcensus를 사용하는 이유

일회성 포트 보고서만으로는 다음 관측 결과가 실제로 변경된 것인지, 아니면 단순히
실패한 것인지 알 수 없습니다. hostcensus는 명시적 서비스 상태, 제한된 프로브, 재사용 가능한
스캔 프로파일 및 로컬 기록을 결합합니다. 운영자는 동일한 범위를 반복 스캔하고,
오류를 점검하며, 불확실한 관측과 확정된 변경 사항을 구분할 수 있습니다.

- **서비스 증거:** SSH 식별 정보, MySQL 인사말(greeting), HTTP 헤더, TLS
  인증서 관측 결과, SNMP 검색 또는 자격 증명을 사용한 system-MIB 쿼리.
- **반복 가능한 범위:** 이름 지정된 TOML 프로파일, 누적 제외 목록, 구성 가능한
  서비스, 호스트/프로브 상한 및 제한된 워커 수.
- **트래픽 전송 전 점검:** 로컬 사전 점검(preflight)으로 대상, 도구, 출력 대상
  접근 권한, 기록 스키마 및 설정된 TLS CA 번들을 검증합니다.
- **인벤토리 기록:** 트랜잭션 기반 SQLite 스냅샷이 모든 관측 결과를 보존하며,
  비교 시에도 스캐너 실패와 알 수 없음(`unknown`) 상태를 그대로 표시합니다.
- **상호 운용 가능한 출력:** 터미널, JSON 및 CSV 보고서, 버전이 지정된 파일 스냅샷,
  Kadupul 가져오기 스크립트.

CI는 Linux 및 macOS 환경의 Python 3.12, 3.13, 3.14와 격리된 Compose
통합 랩을 검증합니다. 코드는 이러한 런타임 버전을 지원하면서도 최신 타입 별칭,
타입이 지정된 사전 점검 결과, 키워드 전용 슬롯(slotted) 프로파일 및 구조화된 비동기 정리를
사용합니다. SemVer 호환성 계약과 GitHub 릴리스 프로세스는
[버전 관리 및 릴리스](../../../docs/releasing.md)를 참조하세요. 릴리스 배지는 현재 체크아웃이 아니라
게시된 아티팩트를 기준으로 합니다. 현재 최신 게시 태그는 `v0.3.0`이며, 이 체크아웃은
패키지 버전 `3.0.0`을 사용합니다. 여기에 문서화된 인벤토리 기능을 사용하려면 체크아웃에서 직접 설치하세요.

먼저 [설치](#install)를 진행한 다음 [프로파일 및 기록](#inventory-profiles-preflight-and-local-history)을 확인하세요.
연동 세부 정보는 [서비스 핑거프린트](#fingerprints),
[파일 비교](#inventory-diff), [Kadupul 내보내기](#kadupul-export)를 참조하세요.

<a name="install"></a>

## 설치

Python 3.12 이상이 필요하며, Python 3.12–3.14 환경에서 테스트되었습니다. 이 체크아웃에서
잠금(locked)된 런타임 의존성을 설치하세요:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

선택 사항인 Nmap 호스트 검색을 사용하려면 플랫폼의 패키지 관리자를 통해 Nmap 실행 파일을
설치하세요. 추가 Python 패키지는 필요하지 않습니다. Nmap의 XML 출력은 핵심 의존성인
defusedxml로 파싱되므로 엔티티 확장이 거부됩니다. hostcensus는 `PATH`에서 찾은
`nmap`을 고정된 인수 목록, 프리픽스 크기에 비례하여 증가하는 제한 시간(deadline), 그리고 64 MiB 출력 상한과 함께
직접 실행합니다. 기본 백엔드에는 Nmap이 필요하지 않습니다.

## netprobe에서 마이그레이션

hostcensus는 3.0.0에서 변경된 netprobe의 새 이름입니다. 이 프로젝트는 두 이름 중
어느 것으로도 PyPI에 게시된 적이 없으므로, 설치는 체크아웃 또는 GitHub 릴리스를 통해 이루어집니다.
GitHub 저장소 이름은 그대로 유지됩니다.

| 이전 | 현재 | 호환성 |
| --- | --- | --- |
| 배포판 `netprobe` | `hostcensus` | 체크아웃에서 다시 설치하세요. 이전 이름의 패키지는 없습니다. |
| `netprobe` 명령 | `hostcensus` | `netprobe`는 여전히 실행되며 stderr에 지원 중단(deprecation) 안내 한 줄을 출력합니다. 종료 코드와 stdout은 동일합니다. 다음 메이저 릴리스에서 제거됩니다. |
| `NETPROBE_*` 환경 변수 | `HOSTCENSUS_*` | 대응하는 `HOSTCENSUS_*` 변수가 설정되지 않은 경우 `NETPROBE_*` 변수가 사용되며, 값은 출력하지 않고 변수 이름만 알리는 stderr 경고를 한 번 출력합니다. 둘 다 설정되면 `HOSTCENSUS_*`가 우선합니다. 다음 메이저 릴리스에서 제거됩니다. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **호환성이 깨지는 변경.** 임포트 심(shim)이 설치되지 않으므로 임포트 구문을 수정하세요. |
| Docker 이미지 태그 `network-discovery:test` (CI 전용) 및 컨테이너 사용자 `netprobe` | `hostcensus:test`, 사용자 `hostcensus` | 레지스트리에 이미지가 게시된 적은 없습니다. 이미지를 다시 빌드하고 `hostcensus` 엔트리포인트를 사용하세요. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | 새 이름의 파일이 없을 때 이전 기본 이름의 기존 파일이 있으면 경고와 함께 계속 사용됩니다. 명시적인 `--config` 및 `--history` 경로는 영향을 받지 않습니다. |
| `"format": "netprobe-report"` 또는 `"netprobe-snapshot"`과 `netprobe_version` 필드가 포함된 보고서 및 스냅샷 | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff`와 `export`는 이전 이름으로 작성된 파일도 계속 불러오며, 게시된 JSON Schema도 두 표기를 모두 허용합니다. 새 파일은 새 이름을 사용합니다. SQLite 기록 데이터베이스는 변경되지 않았으며 이전과 동일하게 불러옵니다. |
| `netprobe export`로 생성된 Kadupul 스크립트 | `hostcensus export`로 생성된 스크립트 | 기존 스크립트는 계속 동작하며 실행 시 여전히 `NETPROBE_SNMP_*`를 읽습니다. 새 스크립트는 `HOSTCENSUS_SNMP_*`를 읽습니다. |

## 빠른 예제

개발(Development) 섹션에 설명된 통합 랩의 테스터 컨테이너에서 실행한 예시이며 출력 일부는 생략되었습니다:

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

## 종료 코드

| 명령 | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | 관측 결과/보고서 기록 완료 | 사전 점검/백엔드, 기록 또는 보고서/스냅샷 쓰기 실패 | 잘못된 대상, 옵션, 구성 또는 제한 초과 | - | `--deadline` 도달; 부분 보고서 작성됨, 기록 및 스냅샷 건너뜀 |
| `preflight` | 점검 통과 | 로컬 점검 실패 | 잘못된 대상/구성 또는 충돌하는 출력 경로 | - | - |
| `profiles` | 검증된 프로파일 목록 출력됨 | - | 읽을 수 없거나 잘못된 구성 또는 선택 항목 | - | - |
| `history` | 요약 목록 출력됨 | 기록이 없거나 잘못되었거나 지원되지 않음 | 잘못된 CLI 옵션 | - | - |
| `compare` | 변경 사항이 있는 경우를 포함해 비교 결과 생성됨 | 읽을 수 없는 기록, 호환되지 않는 범위/순서 또는 쓰기 실패 | 잘못된 CLI 옵션 | - | - |
| `diff` | 변경 사항 없음 | `-o` 파일을 쓸 수 없음 | 입력이 없거나 읽을 수 없거나 지원되지 않거나, `--allow-partial` 없는 불완전한 스캔 | 변경 사항 발견, 미확인 관측 결과 또는 불완전한 스캔 | - |
| `export` | 스크립트 작성 완료 | 스크립트를 쓸 수 없음 | 읽을 수 없는 입력, `--allow-partial` 없는 불완전한 스캔 또는 안전하게 내보낼 수 없는 데이터 | - | - |

## 구조

| 모듈 | 역할 |
| --- | --- |
| `cli.py` | 명령 옵션, 프로파일 해석, 사전 점검, 스캔 및 보고서 생성 |
| `scanner.py`, `probes.py` | 대상 확장, 제한된 워커, 호스트 검색 및 서비스 관측 |
| `config.py`, `profiles.py` | 서비스 정의 및 검증된 인벤토리 프로파일 |
| `models.py`, `output.py` | 결과 타입 및 터미널/JSON/CSV 렌더링 |
| `history.py`, `diff.py` | SQLite 기록 및 버전 지정 파일 스냅샷 비교 |
| `preflight.py` | 로컬 점검 및 제한된 Nmap 버전 조회 |
| `export.py` | 검증 및 셸 이스케이프 처리된 Kadupul 가져오기 스크립트 |

각 서비스 관측 결과는 서비스가 알린 식별 정보와 별도로 상태를 기록합니다.
읽기 작업과 제한 시간에는 상한이 적용되며, 프로브 예외는 호스트 오류에 기록됩니다. SQLite
기록은 트랜잭션, 명시적 연결 정리, 읽기 전용 목록 조회 및 비교 경로를 사용합니다.
SNMP 비밀 값은 환경 변수 또는 비밀 파일로만 전달되며, 인벤토리 기록에는 비밀 값을 제외한
실제 적용 설정만 저장됩니다. 스캔 파이프라인, 제한 사항 및 신뢰 경계는
[아키텍처](../../../docs/architecture.md)를, 허용된 사용 범위는 [SECURITY.md](../../../SECURITY.md#authorized-use)를 참조하세요.


## 사용법

직접 관리하는 네트워크만 스캔하세요.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| 옵션 | 설명 |
| --- | --- |
| `NETWORK` | CIDR, IP 또는 호스트 이름(`--profile` 사용 시 선택 사항). IPv6 스코프 식별자는 거부됩니다. |
| `-o, --output PATH` | 보고서를 파일로 기록합니다. 형식은 확장자(`.json`, `.csv`)를 따르며, 그 외 확장자는 JSON으로 처리됩니다. |
| `-f, --format json\|csv\|kadupul\|auto` | 보고서 형식을 강제 지정합니다. `--output` 없이는 효과가 없습니다. `.sh`는 `kadupul`을 선택합니다. |
| `-v, --verbose` | 디버그 로깅을 활성화합니다. |
| `-q, --quiet` | 결과, 진행 상황 및 정보 로그를 숨깁니다. 경고와 오류는 계속 stderr에 출력됩니다. |
| `--backend asyncio\|nmap` | 호스트 검색 방식. `asyncio`(기본값)는 서비스 포트를 직접 프로브하고, `nmap`은 먼저 nmap ping 스윕을 실행하므로 `PATH`에 `nmap` 실행 파일이 필요합니다. |
| `--timeout SECONDS` | 자체 시간 제한을 설정하지 않은 프로브의 대기 시간(기본값 1.0). 내장 연결 프로브는 서비스 테이블에 `timeout`이 지정되지 않은 경우 0.3초를 사용합니다. |
| `--concurrency N` | 동시에 실행할 프로브 수(기본값 256). |
| `--deadline SECONDS` | nmap 스윕을 포함한 전체 스캔을 이 시간이 지나면 중단합니다(기본값 3600, 최대 604800; 환경 변수 `HOSTCENSUS_DEADLINE`). 완료된 호스트만 `"complete": false` 상태로 보고서에 기록되고, 기록이나 스냅샷은 저장되지 않으며, `scan`은 종료 코드 4를 반환합니다. |
| `--config PATH` | TOML 서비스 정의 및 선택적 이름 지정 `[profiles]` 설정 파일. |
| `--profile NAME` | 이름 지정된 프로파일 사용. `--config`를 생략하면 기본값으로 `hostcensus.toml`을 사용합니다. |
| `--exclude IP/CIDR` | 제외 대상을 추가합니다(필요한 만큼 반복 지정 가능). 제외된 IPv4 호스트는 해당 호스트에 도달하는 IPv6 주소인 IPv4 매핑(`::ffff:a.b.c.d`), NAT64(`64:ff9b::/96`), 6to4 주소도 함께 제외합니다. IPv4 매핑 대상과 제외 항목은 대응하는 IPv4 주소로 취급됩니다. |
| `--max-hosts N` | 제외 적용 전에 확인되는 주소 수 제한(기본값이자 최대 상한 65,536). |
| `--history PATH` | 완료된 스캔을 선택적 SQLite 기록 데이터베이스에 저장합니다. |
| `--services NAMES` | 점검할 서비스 이름의 쉼표 구분 목록(지정된 순서대로 실행, 기본값: 전체). |
| `--ports SPEC` | `NAME=PORT`(서비스 포트 변경) 또는 `PORT`(`tcp-PORT`라는 이름의 일반 TCP 점검 추가)의 쉼표 구분 목록. |
| `--snmp-community-file PATH` | system MIB 쿼리용 SNMPv2c 커뮤니티 문자열이 들어 있는 파일. 환경 변수: `HOSTCENSUS_SNMP_COMMUNITY`(값) 또는 `HOSTCENSUS_SNMP_COMMUNITY_FILE`(경로). |
| `--snmp-user` | SNMPv3 사용자. 환경 변수: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA`(기본값), `SHA224`, `SHA256`, `SHA384`, `SHA512` 및 암호 구문(passphrase)이 들어 있는 파일. 환경 변수: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` 또는 `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES`(기본값), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` 및 암호 구문(passphrase)이 들어 있는 파일. 환경 변수: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` 또는 `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | `hostcensus diff`용 버전 지정 스냅샷도 함께 저장합니다. |
| `--tls-ca-file PATH` | 시스템 저장소 대신 이 PEM 번들을 기준으로 HTTPS 인증서를 검증합니다. 환경 변수: `HOSTCENSUS_TLS_CA_FILE`. |

기본적으로 각 호스트에 대해 SSH(TCP 22), SNMP(UDP 161), MySQL(TCP 3306), HTTP(TCP 80), HTTPS(TCP 443)를 점검합니다. TCP 포트는 완전 연결(full connect)로 테스트합니다. SNMP는 SNMPv3 엔진 검색(engine-discovery) 요청으로 테스트하며, 모든 SNMPv3 에이전트는 자격 증명 없이도 이에 응답해야 합니다. v1/v2c만 지원하는 에이전트는 이 프로브로 탐지되지 않습니다. asyncio 백엔드에서는 연결 거부를 포함해 어떤 프로브라도 응답을 받으면 해당 호스트를 활성(alive) 상태로 간주하므로, 모든 프로브를 드롭하는 호스트는 `alive=false`와 `"Host is down"` 오류로 기록됩니다. 다만 이것이 호스트가 물리적으로 꺼져 있음을 증명하지는 않습니다. `--backend nmap`을 사용하면 nmap이 호스트 활성 여부를 결정합니다(root 권한이면 ICMP, 아니면 TCP 80/443).

<a name="fingerprints"></a>

### 핑거프린트

열려 있는 각 서비스는 로그인 전에 전송하는 데이터를 기반으로 핑거프린팅됩니다. SNMP 쿼리를 제외하면 어떤 프로브도 인증을 시도하지 않으며, SNMP 역시 사용자가 자격 증명을 제공한 경우에만 인증을 수행합니다.

| 프로브 | 읽는 항목 | `version` | `details` 키 |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 식별 줄 | 소프트웨어 (예: `OpenSSH_10.0`) | `protocol`, `software`, `comments` |
| `mysql` | MySQL/MariaDB 초기 핸드셰이크 | 서버 버전 | `server_version`, `flavor`, `auth_plugin` 또는 `error_code`/`error` |
| `http` | `HEAD /` 응답 | `Server` 헤더 | `status`, `server` |
| `https` | TLS 핸드셰이크, 인증서, `HEAD /` | `Server` 헤더 | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 검색; 자격 증명 제공 시 sysDescr, sysObjectID, sysName GET 조회 | sysDescr | `engine_id`; 자격 증명 제공 시 `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` 또는 `snmp_error` |

호스트 이름 대상은 호스트당 한 번만 이름 해석(resolve)되며, 모든 프로브는 그 결과 주소(결과에 `address`로 기록됨)로 연결합니다. 호스트 이름은 TLS SNI, 인증서 검증 및 HTTP `Host` 헤더에만 사용됩니다. 해석되지 않는 이름은 `unknown` 상태와 `Cannot resolve` 오류를 반환합니다. 역방향 DNS 이름은 호스트 이름 허용 문자로만 구성된 경우에만 유지되며, 동시에 최대 16개의 조회만 실행됩니다. HTTPS는 시스템 저장소 또는 `--tls-ca-file`을 기준으로 인증서와 호스트 이름을 검증합니다. 신뢰 저장소는 스캔당 한 번만 불러와 모든 HTTPS 프로브에서 재사용합니다. TCP 연결과 TLS 핸드셰이크는 시간 제한을 별도로 측정하므로, 연결을 수락했지만 핸드셰이크에서 멈추는 포트는 `filtered`가 아니라 `tls_error`가 포함된 `open` 상태로 기록됩니다. 검증에 실패하면 결과에 `cert_verified: false`와 `cert_verify_error`를 기록하며, 더 약한 설정으로 재시도하거나 HTTP 요청을 보내지 않습니다. 인증서 세부 정보와 HTTP 헤더는 검증이 성공한 후에만 수집됩니다. 사설 CA를 사용하는 서비스에는 올바른 CA 번들을 제공하세요. 이전 보고서에는 `cert_read_unverified`가 포함될 수 있으나, 현재 프로브는 더 이상 이 필드를 생성하지 않습니다.

SNMP 비밀 값은 환경 변수 또는 파일(`--snmp-*-file` 또는 대응하는 `HOSTCENSUS_SNMP_*_FILE` 변수)에서만 읽으며, 다른 로컬 사용자가 프로세스 목록에서 볼 수 있는 명령줄 인수의 값으로는 받지 않습니다. `--snmp-community`, `--snmp-auth-key`, `--snmp-priv-key`에 값을 직접 전달하면 대체 옵션을 안내하며 종료 코드 2로 종료됩니다. 비밀 파일은 비어 있지 않은 최대 4096바이트의 UTF-8 파일이어야 하며, 끝의 개행 문자 1개는 무시됩니다. 동일한 비밀 값에 대해 환경 변수와 파일을 동시에 설정하면 오류가 발생합니다. 오류 메시지는 파일 이름을 표시할 수 있지만 파일 내용은 절대 출력하지 않습니다. 스캔 보고서와 기록에는 자격 증명 값을 의도적으로 포함하지 않습니다. 내보내기 도구에는 아래에 설명된 별도의 명시적 `--include-credentials` 옵션이 있습니다. 커뮤니티를 지정하면 SNMPv2c가 선택되고, 사용자를 지정하면 SNMPv3가 선택됩니다(인증 키가 주어지면 auth, 두 키가 모두 주어지면 priv 적용; `snmp_security_level`에 기록됨). hostcensus는 커뮤니티와 v3 사용자를 함께 쓰거나, 인증 키 없이 암호화(privacy) 키만 사용하거나, 사용자 없이 키를 사용하는 조합을 거부하고 종료 코드 2를 반환하며, 실패한 v3 쿼리를 v2c나 더 낮은 보안 수준으로 절대 재시도하지 않습니다. v1/v2c만 지원하는 에이전트는 자격 증명 없는 v3 검색을 무시하므로 커뮤니티를 제공한 경우에만 열림(open)으로 표시됩니다.

배너 텍스트는 인쇄 가능한 문자로 축소되고 저장 또는 표시되기 전에 256자로 제한됩니다. 읽기 크기에도 상한이 있습니다: 줄당 4 KiB, MySQL 인사말 4 KiB, HTTP 헤더 16 KiB. 32옥텟보다 긴 SNMP 엔진 ID는 저장 전에 잘립니다. HTTP와 HTTPS는 IPv6 주소를 대괄호로 감싸고, 포트가 80이나 443이 아닐 때는 포트 번호를 포함한 `Host` 헤더를 전송합니다. 스프레드시트 수식 트리거 문자로 시작하는 CSV 셀은 텍스트로 유지되도록 접두사가 붙습니다.

### 제한 사항

한 번의 실행에서 최대 65,536개 주소, 64개 서비스, 524,288개 프로브(호스트 수 × 서비스 수)까지 허용되며, 이를 초과하는 요청은 패킷을 전송하기 전에 종료 코드 2로 종료됩니다. `--concurrency`는 최대 4096개 소켓으로 제한됩니다. 각 프로브에는 자체 시간 예산의 4배에 해당하는 절대 제한 시간(hard deadline)이 적용됩니다. 연결 프로브(`tcp`, `ssh`, `mysql`, `http`)는 해당 서비스에 `timeout`이 설정되어 있지 않으면 0.3초를 사용합니다. SNMP와 HTTPS는 개별 설정이 없을 때 `--timeout`(기본값 1.0)을 사용합니다. 제한 시간에 도달한 프로브는 `errors`에 "probe timed out"이 기록된 `unknown` 상태로 보고됩니다. 로컬 소켓 오류(예: 파일 디스크립터 고갈) 역시 오류 내용과 함께 `unknown`으로 기록되며, 필터링된 포트나 다운된 호스트로 집계되지 않습니다. 프로빙 전 hostcensus는 `--concurrency`에 64개 디스크립터를 더한 값을 수용할 수 있도록 열린 파일(open-file) 소프트 제한을 하드 제한까지 상향 조정합니다. 이를 확보할 수 없으면 `open files` 사전 점검이 실패하고 `scan`은 트래픽을 보내기 전에 종료 코드 1로 종료됩니다. Nmap 검색은 30초의 호스트 타임아웃을 사용합니다. 프리픽스는 CIDR 형식으로 nmap에 전달되며, nmap이 전달받은 것보다 적은 수의 주소를 보고하면(예: 해석할 수 없는 이름) 호스트를 다운 상태로 표시하는 대신 종료 코드 1로 스윕을 실패 처리합니다. 호스트 이름 대상은 한 번만 해석되어 그 주소가 nmap에 전달되므로, 검색 단계와 프로브가 동일한 머신에 도달합니다. 전체 프리픽스는 단일 nmap 프로세스로 실행되며 하위 프로세스 제한 시간은 256개 주소당 35초(올림)입니다. 제외 목록이 있는 스윕은 256개 호스트 단위의 배치와 배치당 35초 제한 시간을 사용합니다. 워커 생성 수는 대역 크기와 무관하게 제한됩니다. 역방향 DNS 및 호스트 이름 해석에는 별도의 2초 제한 시간이 적용되며, 반환되지 않는 리졸버 호출은 해당 스레드에 남겨 둔 채 중단되므로 hostcensus가 이 제한을 넘어 계속 실행되지 않습니다. 동시에 최대 16개의 조회만 실행되며, 중단된 호출은 반환될 때까지 슬롯을 점유하므로 멈춘 스레드 수가 제한됩니다. 16개 슬롯이 모두 멈추면 이후 조회는 슬롯이 빌 때까지 2초 제한 시간(슬롯을 확보한 시점부터 시작) 밖에서 대기하며, `--deadline`에 도달하면 스캔이 중단됩니다. `deadline` 없이 라이브러리로 사용되는 `NetworkScanner`는 이러한 슬롯을 무기한 대기할 수 있습니다. `--deadline`(기본값 1시간)은 이 모든 제한 위에서 전체 실행 시간을 제한합니다.

### 서비스 구성

TOML 파일로 서비스를 변경할 수 있습니다:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe`는 `tcp`, `ssh`, `mysql`, `http`, `https`, `snmp` 중 하나이며, 서비스 이름이 프로브 이름과 같으면 그 값을 기본값으로 사용하고 그렇지 않으면 `tcp`를 사용합니다. `snmp`만 UDP를 사용합니다. 서비스 이름은 소문자, 숫자, `-`, `_`만 사용할 수 있습니다. 두 서비스가 동일한 포트와 프로토콜을 공유할 수 없으며, 기록에서는 해당 포트/프로토콜 쌍에 대해 하나의 상태만 저장합니다. `timeout`은 선택 사항(초 단위)이며 최소 0.05 이상이어야 합니다. 연결 방식 프로브(`tcp`, `ssh`, `mysql`, `http`)의 기본값은 0.3초입니다. `snmp`와 `https`는 서비스에 `timeout`이 설정되지 않은 경우 스캔의 `--timeout`을 사용합니다. `--timeout`은 서비스에 이미 설정된 시간 예산을 덮어쓰지 않습니다.

JSON 보고서는 버전이 지정된 문서(`"format": "hostcensus-report"`, `"version": 1`)로, `devices`와 함께 대상, 프로브된 서비스 및 설정을 기록합니다. `-o` 없이 `--format json`을 지정하면 표 대신 stdout에 보고서를 출력합니다. 모든 JSON 출력에는 게시된 스키마가 있으며, 자세한 내용은 [JSON 출력](../../../docs/json-output.md)을 참조하세요. 각 장치 객체는 기존의 `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname`, `errors` 필드를 유지하면서, 각 프로브의 `name`, `port`, `protocol`, `state`(`open`, `closed`, `filtered`, 또는 프로브가 로컬에서 실패했거나 제한 시간에 도달한 경우 `unknown`), `version`, `details`를 담은 `services` 목록을 추가합니다. CSV 출력에서는 끝에 열려 있는 서비스에 대한 `services` 및 `versions` 열이 추가됩니다. `ssh`, `snmp`, `mysql` 불리언 필드는 정확히 해당 이름의 서비스 결과를 따릅니다.


<a name="inventory-profiles-preflight-and-local-history"></a>

## 인벤토리 프로파일, 사전 점검 및 로컬 기록

이름이 지정된 프로파일은 기존 `[services]` 정의와 동일한 TOML 파일을 공유합니다.
[hostcensus.example.toml](../../../hostcensus.example.toml)을 `hostcensus.toml`로 복사하고
직접 관리하는 네트워크를 설정하세요:

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

`preflight`는 열린 파일 점검을 위한 `--concurrency`를 포함해 `scan`과 완전히 동일한 방식으로
옵션과 프로파일을 해석하므로, 사전 점검을 통과하면 `scan`도 동일한 계획으로 시작됩니다.

프로파일은 `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, `max_hosts`를 지원합니다. `services`와 `ports`는 기존의 쉼표 구분 목록
문법을 사용합니다. 명시적인 CLI 옵션은 프로파일 설정을 덮어쓰며, 반복된 `--exclude`
옵션은 프로파일의 제외 목록에 추가됩니다. `--profile`과 함께 명시적인 네트워크를 지정하는 경우,
해당 프로파일의 IP/CIDR 범위에 포함되어야 합니다. 직접 스캔에서는 호스트 이름도 계속 지원되지만
IP 제외 목록과는 함께 사용할 수 없습니다. 호스트 수 제한은 제외 적용 전에 검사되며,
전체 프로브 상한은 제외 적용 후에도 적용됩니다. 제외된 호스트는 서비스 점검과 선택 사항인
Nmap 검색 모두에서 빠집니다.

모든 스캔은 대상 트래픽을 보내기 전에 로컬 사전 점검을 수행합니다: 대상/프로브 제한,
출력 대상 접근 권한, 선택적 Nmap 실행 파일/래퍼 사용 가능 여부, 기록 스키마, 설정된 TLS CA 번들.
`preflight`는 JSON으로 결과를 보고하며 대상을 스캔하거나 기록 데이터베이스를 생성하지 않습니다.
기존 내용을 변경하지 않고 출력 대상 쓰기 권한을 테스트하기 위해 임시 형제 파일(sibling file)을 작성합니다.
기본 asyncio 백엔드는 여전히 Nmap도 root 권한도 필요하지 않습니다. 출력 대상 경로는
하드 링크를 포함하여 서로 간에, 그리고 입력 구성 파일과도 달라야 하며, 대상 경로의 심볼릭 링크는 거부됩니다.
점검 실패 시 1, 잘못된 범위/구성 시 2를 반환합니다.

보고서 및 내보내기 쓰기에는 `O_NOFOLLOW` 지원이 필요합니다. Windows를 포함해 이를 지원하지 않는
플랫폼에서는 대상 파일을 열거나 잘라내지(truncate) 않고 쓰기가 실패합니다.
새 보고서와 내보내기 스크립트는 소유자 전용(모드 0600)으로 생성되며, 기존 파일을 덮어쓸 때는
기존 권한을 유지합니다. 읽기 측(reader)이 없는 명명된 파이프(named pipe)에 쓰기를 시도하면 대기하지 않고
즉시 실패합니다. 새 `--history` 데이터베이스 역시 소유자 전용으로 생성되며, 기존 파일은 권한 모드를 유지합니다.
로그 메시지는 항상 stderr로 출력되므로 stdout에는 결과만 전달됩니다. 자격 증명이 포함된 내보내기 파일은
항상 모드 0600을 강제합니다.

기록 기능은 선택적(opt-in)으로 동작하며 기존의 JSON 스냅샷 및 `diff` 명령을 보완합니다:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

`history`에서 얻은 ID를 사용하세요(예제는 새 데이터베이스를 가정합니다). 스냅샷은
UTC 시작/종료 시각, 패키지 버전, 비밀 값을 제외한 실제 적용 설정, 요약, 그리고 호스트별 오류를 포함한
모든 호스트/서비스 관측 결과와 함께 트랜잭션으로 저장됩니다.
불완전한 호스트 관측 결과도 보존됩니다. 취소된 실행은 저장되지 않습니다. 기존의
보고서, 스냅샷, 내보내기 및 스캔 종료 코드 계약은 그대로 유지됩니다.

`history`는 과거 장치 페이로드 전체를 읽지 않고 JSON 요약 목록을 출력합니다.
`compare`는 저장된 두 스캔을 읽어 대상 식별 정보와 선택된 포트가 동일한지 확인한 뒤
응답성, 상태 및 포트 상태 변경 사항을 보고합니다. 이전 스캔 ID가 이후 ID보다 앞서야 합니다.
두 스캔 모두 `timeout` 또는 `backend`를 기록했고 그 값이 서로 다른 경우, 보고서에 경고를
표시하면서도 관측 결과를 비교합니다. 대기 시간이 다르면 필터링된 포트가 열려 있는 것처럼 보일 수 있습니다.
스캐너 오류와 `unknown` 포트 관측은 확정된 소멸이나 닫힘으로 간주하지 않고 불확실한 항목으로 표시됩니다:
오류가 발생한 호스트는 `uncertain_hosts`에 표시되며, `unknown`이 포함된 모든 포트 전환(두 스캔 모두
unknown인 경우 포함)은 이후 스캔에서 포트가 열려 있는 경우(포트 변경으로 처리)를 제외하고
`port_changes` 대신 `unconfirmed_ports`에 나열됩니다. `compare`와 `diff`는 동일한 규칙으로 포트를 분류합니다.
`no_longer_responding`은 응답이 없음을 의미할 뿐 장치 제거를 증명하지는 않습니다.
스캔 종료 코드 0이 모든 호스트의 응답을 보장하지는 않으므로 호스트별 오류를 확인하세요.
비교가 성공하면 변경 여부와 무관하게 0을 반환하며, 기존 파일 `diff`는 종료 코드 3 계약을 유지합니다.
지원되지 않거나 손상된 기록은 1을 반환합니다.

기록 데이터베이스에는 인벤토리 정보가 저장되므로 적절히 보호된 로컬 디렉터리를 선택하세요.
프로파일 파일과 저장된 설정에는 SNMP 자격 증명이 포함되지 않으며,
자격 증명 처리는 기존의 런타임 옵션/환경 변수를 통해 계속 이루어집니다.

<a name="inventory-diff"></a>

## 인벤토리 diff

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

스냅샷은 `format: "hostcensus-snapshot"`, `version: 1`, hostcensus 버전, UTC 생성 시각, 대상, 스캔 시 기록된 경우의 `timeout` 및 `backend`, 프로브된 서비스 목록, 그리고 `-o` 보고서와 동일한 형태의 활성 호스트 목록을 포함하는 JSON입니다. 다운된 호스트는 제외됩니다. `diff`는 `services` 필드가 존재하기 전에 작성된 보고서를 포함해 일반 `scan -o` JSON 보고서도 입력으로 받습니다.

`diff`는 새로 추가되거나 사라진 호스트, 두 스캔 모두에 존재하는 호스트에서 열리거나 닫힌 포트, 그리고 `version`이 변경된 서비스를 보고합니다. 두 스캔 중 한쪽에서만 프로브된 포트는 비교하지 않으며 경고를 출력합니다. 실패한 관측 결과는 절대 "변경 없음"으로 처리되지 않습니다. 두 스캔 중 어느 한쪽에서 `unknown`이고 이후 스캔에서 열려 있지 않은 포트는 `closed`가 아니라 `unconfirmed` 아래에 `before` (`open`, `unknown`, 또는 프로브되었으나 닫혔거나 필터링된 `not-open`) 및 `after` (`unknown` 또는 `not-open`) 값과 함께 기록됩니다. 이전 프로브가 실패했더라도 현재 열려 있는 포트는 `opened`로 보고됩니다. 두 스캔 중 한쪽에서 모든 프로브가 응답 없이 실패한 호스트는(양쪽 스캔 모두에서 실패했거나 다른 파일에 없는 경우 포함) `vanished_hosts` 대신 `unsettled_hosts`에 `before`/`after` 값(`up`, `uncertain` 또는 `absent`)과 함께 나열되며, 이후 스캔에서 응답하면 열린 포트와 함께 새 호스트로도 보고됩니다. 스냅샷이 실패한 호스트를 보존하는 이유도 이 때문입니다. 대상이 서로 다른 경우, 그리고 두 파일 모두에 timeout이나 backend가 기록되어 있는데 그 값이 다른 경우에도 경고가 표시됩니다. `-o PATH`를 지정하면 JSON 형식을 파일로도 저장합니다.

`--deadline`으로 중단된 스캔의 보고서(`"complete": false`)는 도달한 호스트만 나열하므로, `diff`와 `export`는 이를 종료 코드 2로 거부합니다. `--allow-partial`을 사용하면 stderr 경고를 출력하고 이를 허용합니다. 이때 `diff`는 불완전한 스캔에 전혀 포함되지 않은 호스트를 사라진 호스트가 아닌 `unsettled_hosts` 아래에 `unscanned`로 표시하고(다운으로 기록된 호스트는 여전히 사라짐으로 처리), `partial`을 true로 설정하며 변경 없음으로 보고하지 않습니다. `export`는 스크립트 헤더에 경고를 기록합니다.

`diff` 종료 코드: `0` 변경 사항 없음, `3` 변경 사항 발견, 확인할 수 없는 관측 결과 존재, 또는 불완전한 입력(`unsettled_hosts`와 `unconfirmed`를 포함한 목록 중 하나라도 비어 있지 않거나 `partial`이 true이면 `changed`는 true가 됨), `2` 파일이 없거나 읽을 수 없거나 지원되는 스냅샷이 아니거나 `--allow-partial` 없이 불완전한 스캔을 전달함, `1` `-o` 파일을 쓸 수 없음.

<a name="kadupul-export"></a>

## Kadupul 내보내기

[Kadupul](https://github.com/kadupulhq/kadupul)(Cacti 1.2.31 포크)은 파일 기반 대량 장치 가져오기를 지원하지 않습니다. 스크립트에서 장치를 추가할 때 공식적으로 지원되는 방법은 호출당 하나의 장치를 `--option=value` 인수로 전달해 `cli/add_device.php`를 실행하는 것입니다. `hostcensus export`는 이러한 호출들로 구성된 POSIX `sh` 스크립트를 생성합니다:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

각 활성 호스트는 `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` 명령으로 변환됩니다:

- 스캔의 SNMP 쿼리가 성공한 호스트에는 `--version=2 --community=...` 또는 `--version=3 --username=... --authproto=... --password=...`(authPriv의 경우 `--privproto`/`--privpass` 추가), `--port`, `--avail=snmp`가 지정됩니다. SNMPv3 내보내기에는 `--snmp-user`가 필요하며, `add_device.php`가 v3 비밀번호를 요구하므로 noAuthNoPriv는 거부됩니다.
- 그 외 호스트에는 `--version=0 --avail=ping`이 지정되며, 열린 TCP 포트가 있으면 첫 번째 포트로 `--ping_method=tcp --ping_port=`가, 없으면 ICMP가 설정됩니다.
- `--notes`에는 열린 서비스와 버전이 나열됩니다. `--description`은 역방향 DNS 이름이 일반 문자(영문자, 숫자, `.`, `_`, `-`)로만 구성된 경우 해당 이름을, 그렇지 않으면 IP를 사용하며, `add_device.php`가 기존 설명과 일치하면 해당 장치를 업데이트하므로 고유하게 만들어집니다.

모든 값은 검증을 거친 후 `shlex.quote`로 셸 이스케이프 처리됩니다. 기본적으로 SNMP 비밀 값은 스크립트에 기록되지 않습니다. 대신 스크립트가 실행 시점에 `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` 또는 `HOSTCENSUS_SNMP_PRIV_KEY`를 확장하며, 필요한 변수가 설정되어 있지 않으면 중단됩니다. `--include-credentials` 옵션을 사용하면 해당 환경 변수의 값을 스크립트에 직접 기록하고, 파일을 모드 0600으로 생성하며 경고를 로그에 남깁니다. 참고로 `add_device.php` 자체는 커뮤니티 문자열을 출력하고 비밀 값을 인수로 전달받으므로, 각 호출이 실행되는 동안 Kadupul 서버의 프로세스 목록에 해당 값이 노출됩니다.

`add_device.php`는 중복이나 오류가 발생하면 종료 코드 1을 반환합니다. 생성된 스크립트는 다음 장치로 계속 진행하면서 실패 횟수를 세고, 추가되지 않은 장치가 하나라도 있으면 종료 코드 1로 종료합니다. 템플릿 ID는 `php cli/add_device.php --list-host-templates`로 확인할 수 있습니다. `export` 종료 코드: `0` 작성 완료, `2` 읽을 수 없는 입력, `--allow-partial` 없는 불완전한 스캔 또는 안전하게 내보낼 수 없는 데이터, `1` 스크립트를 쓸 수 없음.

## 버전 관리 및 릴리스 프로세스

hostcensus는 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)을 따릅니다.
호환되는 수정은 패치(patch) 버전을, 호환되는 기능 추가 및 지원 중단 안내는 마이너(minor) 버전을,
호환성이 깨지는 변경은 메이저(major) 버전을 올립니다.
명령과 옵션, 종료 코드 및 JSON 스키마가 공개 계약에 해당하며,
지원 중단(deprecated)된 동작은 보안 수정으로 인해 조기 변경이 필요한 경우(이 경우 변경 로그에 사유 명시)가
아니라면 다음 메이저 릴리스까지 계속 동작합니다.

release-please는 `main` 브랜치의 Conventional Commit 제목을 바탕으로 릴리스 PR을 생성하여
`pyproject.toml`, `uv.lock`, `CHANGES.md`의 버전을 올립니다. 이 PR을 병합하면
`vMAJOR.MINOR.PATCH` 태그와 초안(draft) GitHub 릴리스가 생성되고, CI가 검증된
wheel, 소스 배포판 및 체크섬을 첨부하며, GitHub는 attestations API를 통해
해당 파일의 빌드 증명(attestation)을 저장합니다. 파일 첨부가 완료되면 메인테이너가
초안을 검토하고 게시합니다. 한 번 게시된 릴리스는 교체하지 않습니다.

PyPI 신뢰할 수 있는 게시(trusted publishing)는 선택 사항이며 프로젝트 소유권,
신뢰할 수 있는 게시자 및 `pypi` 환경이 필요합니다. 이는 API 토큰을 저장하거나 다시 빌드하지 않고
동일한 검증된 릴리스 아티팩트를 게시합니다. 이 공개 저장소의 태그된 릴리스는
GitHub 아티팩트 증명을 생성하며, 비공개 포크에서는 지원되는 요금제와 명시적 활성화가 필요합니다.
설정 방법, 정확한 명령 및 재시도 절차는 [전체 릴리스 가이드](../../../docs/releasing.md)를 참조하세요.

## 개발

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

개발 도구는 `pyproject.toml`의 [PEP 735](https://peps.python.org/pep-0735/) 의존성
그룹(`dev`, `fuzz`, `build`)에 정의되어 있어 게시되는 패키지 메타데이터에 포함되지 않습니다.
`uv.lock`이 단일 잠금 파일이며, CI는 `uv sync --locked`로 설치하고 잠금 파일이 오래된 경우 실패합니다.
인터프리터는 `uv python`, mise(`mise exec python@3.14 -- uv sync --locked`) 또는 Python 3.12 이상 중
하나를 선택해 사용할 수 있습니다.

CI는 패키지 테스트 커버리지 하한선 90%를 강제합니다. 단위 테스트에는 격리된 루프백 서버와
오프라인 프로파일/기록/릴리스 검증기 케이스가 포함되며, Compose 랩은 격리된 브리지 네트워크에서
OpenSSH, MariaDB, nginx, net-snmp를 실행합니다. 통합 테스트는 `make test-integration`으로 실행하세요.
자세한 내용은 [CONTRIBUTING.md](../../../CONTRIBUTING.md)와 [릴리스 도구](../../../scripts/README.md)를 참조하세요.

런타임 컨테이너는 홈 디렉터리, 셸 로그인 및 pip 없이 UID/GID 10001로 실행되며
`/app/output`에 쓸 수 있습니다. 마운트된 출력 디렉터리가 있다면 해당 사용자에게 쓰기 권한을 부여하세요.
추가 리눅스 커널 권한(capabilities)이 필요 없고 읽기 전용 루트 파일 시스템에서도 동작하므로 다음과 같이 실행할 수 있습니다:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

이 컨테이너에서 Nmap은 비특권 TCP 검색 방식으로 동작합니다. CI는 Trivy가 보고하는 수정 가능한
HIGH 또는 CRITICAL 등급 취약점이 하나라도 있으면 이미지 빌드를 실패 처리합니다.

## 공급망 보안 점검

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)가
main 브랜치와 매주 정기적으로 실행되어 실제 점수를 공개하고 결과를 GitHub 코드 스캐닝에 업로드합니다.
Actions와 컨테이너 베이스 이미지는 변경 불가능한 해시로 고정되며, Python 의존성은 `uv.lock`에서 관리됩니다.
Bandit 검사 실패 시 CI가 실패하며, 제한된 Atheris 퍼징은 네트워크 접근 없이 SSH, MySQL, HTTP,
인증서 및 SNMPv3 BER 파서를 테스트합니다.

Scorecard는 과거 리뷰 활동, 기여자 다양성 및 릴리스 출처 증명(provenance)도 측정합니다.
이 점수는 실제 증거를 반영하는 지표이며, 모든 거버넌스 또는 과거 릴리스 점검을 충족했다는 주장은 아닙니다.
자세한 내용은 [SECURITY.md](../../../SECURITY.md)와 [릴리스 출처 증명](../../../docs/releasing.md)을 참조하세요.

## 현지화

CLI 메시지와 터미널 요약/diff 표는 추가 런타임 의존성 없이 45개 로캘(`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`)을 지원합니다. 로캘 결정은 `--lang`, 그다음 `LC_ALL`, `LC_MESSAGES`, `LANG` 순서를 따르며 기본 폴백은 `en`입니다. JSON 스키마, CSV 열 및 내보내기 스크립트는 모든 로캘에서 동일하게 유지됩니다.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## 기여하기

기여 시에는 재현 가능한 사례를 포함하고, 문서화된 CLI 및 데이터 형식 계약을 유지하며,
위의 품질 검사를 통과해야 합니다. 개발 워크플로는 [CONTRIBUTING.md](../../../CONTRIBUTING.md)를,
호환성 및 버전 관리 결정 사항은 [릴리스 가이드](../../../docs/releasing.md)를 참조하세요.

## 보안 및 라이선스 상태

비공개 취약점 제보 및 지원되는 버전은 [SECURITY.md](../../../SECURITY.md)를 참조하세요.
hostcensus는 [MIT License](../../../LICENSE)에 따라 라이선스가 부여됩니다.

소스 파일 헤더는 SPDX 식별자를 사용하며 Git 기록의 기여자 크레딧을 유지합니다.
저작자 표시는 [AUTHORS.md](../../../AUTHORS.md)를 참조하세요. 바이너리 테스트 캡처와
생성된 잠금 파일은 인접한 `.license` 파일을 사용하며, MIT 라이선스 전문은 `LICENSES/MIT.txt`에 있습니다.
