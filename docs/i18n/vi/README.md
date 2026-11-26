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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · **Tiếng Việt** · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus là một công cụ dòng lệnh (CLI) bằng Python dùng để kiểm kê dịch vụ có thể lặp lại trên các mạng do bạn quản trị. Công cụ này ghi lại những gì thiết bị đang mở ra, so sánh các kết quả quan sát theo thời gian và tạo tập lệnh nhập cho Kadupul. Backend mặc định sử dụng socket asyncio không cần quyền root; tính năng khám phá tùy chọn bằng Nmap có thể nhận diện các host ngoài những cổng dịch vụ đã cấu hình.

## Vì sao chọn hostcensus

Một báo cáo cổng đơn lẻ không cho biết lần quan sát tiếp theo có thực sự thay đổi hay chỉ đơn giản là gặp lỗi. hostcensus kết hợp trạng thái dịch vụ rõ ràng, các probe có giới hạn, hồ sơ quét tái sử dụng được và lịch sử cục bộ. Người vận hành có thể lặp lại cùng một phạm vi quét, kiểm tra lỗi và phân biệt giữa những quan sát chưa chắc chắn với các thay đổi đã được xác nhận.

- **Bằng chứng dịch vụ:** Nhận diện SSH, gói chào MySQL, header HTTP, thông tin chứng chỉ TLS, cũng như khám phá SNMP hoặc truy vấn system-MIB có xác thực.
- **Phạm vi lặp lại được:** Hồ sơ TOML đặt tên sẵn, danh sách loại trừ cộng dồn, dịch vụ cấu hình linh hoạt, giới hạn host/probe và số lượng worker có ràng buộc.
- **Kiểm tra trước khi gửi lưu lượng:** Quy trình kiểm tra trước cục bộ xác thực mục tiêu, công cụ, quyền truy cập đích ghi, lược đồ lịch sử và các gói CA TLS đã cấu hình.
- **Lịch sử kiểm kê:** Các bản chụp SQLite theo giao dịch lưu giữ toàn bộ quan sát; kết quả so sánh vẫn hiển thị rõ lỗi của trình quét và các trạng thái không xác định.
- **Đầu ra tương thích đa hệ thống:** Báo cáo trên terminal, JSON và CSV, bản chụp tệp có phiên bản và tập lệnh nhập cho Kadupul.

CI bao phủ Python 3.12, 3.13 và 3.14 trên Linux và macOS, cùng với một môi trường tích hợp Compose được kiểm soát. Mã nguồn sử dụng các type alias hiện đại, kết quả preflight định kiểu rõ ràng, các hồ sơ dạng slot chỉ nhận tham số từ khóa và dọn dẹp bất đồng bộ có cấu trúc trong khi vẫn duy trì tương thích với các phiên bản runtime đó. Xem [Phiên bản và phát hành](../../../docs/releasing.md) để biết cam kết tương thích SemVer và quy trình phát hành trên GitHub. Huy hiệu phát hành mô tả các bản dựng đã công bố, không phải mã nguồn hiện tại trong checkout: thẻ phát hành mới nhất hiện là `v0.3.0`, trong khi bản checkout này dùng phiên bản gói `3.0.0`. Hãy cài đặt trực tiếp từ bản checkout để sử dụng các tính năng kiểm kê được tài liệu hóa tại đây.

Bắt đầu với [cài đặt](#install), sau đó xem [hồ sơ và lịch sử](#inventory-profiles-preflight-and-local-history). Để biết chi tiết tích hợp, xem [dấu vân tay dịch vụ](#fingerprints), [so sánh tệp](#inventory-diff) và [xuất sang Kadupul](#kadupul-export).

<a name="install"></a>

## Cài đặt

Yêu cầu Python 3.12 trở lên; ma trận kiểm thử hỗ trợ Python 3.12–3.14. Từ bản checkout này, cài đặt các gói phụ thuộc runtime đã khóa phiên bản:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Đối với tính năng khám phá host tùy chọn bằng Nmap, hãy cài đặt tệp thực thi Nmap bằng trình quản lý gói của hệ điều hành; không cần thêm gói Python nào. Đầu ra XML của Nmap được phân tích bằng defusedxml, một gói phụ thuộc cốt lõi, nên việc mở rộng thực thể bị từ chối. hostcensus chạy trực tiếp `nmap` tìm thấy trên `PATH` với danh sách tham số cố định, thời hạn thực thi tăng theo kích thước tiền tố mạng và giới hạn đầu ra 64 MiB. Không cần Nmap đối với backend mặc định.

## Chuyển đổi từ netprobe

hostcensus là tên gọi mới của netprobe, được phát hành từ phiên bản 3.0.0. Dự án chưa từng được xuất bản lên PyPI dưới bất kỳ tên nào trong hai tên này, nên việc cài đặt đều thực hiện từ bản checkout hoặc bản phát hành trên GitHub. Kho lưu trữ GitHub vẫn giữ nguyên tên cũ.

| Trước đây | Hiện tại | Khả năng tương thích |
| --- | --- | --- |
| Gói phân phối `netprobe` | `hostcensus` | Cài đặt lại từ bản checkout; không có gói mang tên cũ. |
| Lệnh `netprobe` | `hostcensus` | `netprobe` vẫn chạy và in một dòng cảnh báo lỗi thời lên stderr. Mã thoát và stdout không đổi. Sẽ bị gỡ bỏ trong bản phát hành chính tiếp theo. |
| Các biến môi trường `NETPROBE_*` | `HOSTCENSUS_*` | Biến `NETPROBE_*` vẫn được dùng khi biến `HOSTCENSUS_*` tương ứng chưa được thiết lập, kèm một cảnh báo lên stderr nêu tên biến (không bao giờ in giá trị). `HOSTCENSUS_*` được ưu tiên khi cả hai cùng tồn tại. Sẽ bị gỡ bỏ trong bản phát hành chính tiếp theo. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Thay đổi không tương thích ngược.** Không có lớp chuyển tiếp import; hãy cập nhật các câu lệnh import. |
| Thẻ image Docker `network-discovery:test` (chỉ trong CI) và người dùng container `netprobe` | `hostcensus:test`, người dùng `hostcensus` | Chưa từng có image nào được đẩy lên registry. Hãy build lại image và sử dụng entrypoint `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Tệp hiện có mang tên mặc định cũ vẫn được dùng kèm cảnh báo khi tệp mang tên mới chưa tồn tại. Các đường dẫn `--config` và `--history` chỉ định tường minh không bị ảnh hưởng. |
| Báo cáo và bản chụp có `"format": "netprobe-report"` hoặc `"netprobe-snapshot"`, và trường `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` và `export` vẫn nạp được các tệp tạo theo tên cũ, và các JSON Schema đã công bố chấp nhận cả hai cách viết. Tệp mới dùng tên mới. Cơ sở dữ liệu lịch sử SQLite không thay đổi và nạp như trước. |
| Tập lệnh Kadupul từ `netprobe export` | Tập lệnh từ `hostcensus export` | Tập lệnh cũ vẫn hoạt động và vẫn đọc `NETPROBE_SNMP_*` khi chạy. Tập lệnh mới đọc `HOSTCENSUS_SNMP_*`. |

## Ví dụ nhanh

Chạy từ container kiểm thử của môi trường tích hợp được mô tả trong mục Phát triển; phần đầu ra đã được rút gọn:

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

## Mã thoát

| Lệnh | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | đã ghi nhận quan sát/báo cáo | lỗi preflight/backend, lịch sử hoặc ghi báo cáo/bản chụp | mục tiêu, tùy chọn, cấu hình hoặc giới hạn không hợp lệ | - | đạt `--deadline`; đã ghi báo cáo một phần, bỏ qua lịch sử và bản chụp |
| `preflight` | các kiểm tra đều đạt | kiểm tra cục bộ thất bại | mục tiêu/cấu hình không hợp lệ hoặc đích ghi xung đột | - | - |
| `profiles` | đã liệt kê các hồ sơ hợp lệ | - | cấu hình hoặc lựa chọn không đọc được/không hợp lệ | - | - |
| `history` | đã liệt kê các bản tóm tắt | lịch sử bị thiếu, không hợp lệ hoặc không được hỗ trợ | tùy chọn CLI không hợp lệ | - | - |
| `compare` | đã tạo kết quả so sánh, kể cả khi có thay đổi | lịch sử không đọc được, phạm vi/thứ tự không tương thích hoặc lỗi ghi | tùy chọn CLI không hợp lệ | - | - |
| `diff` | không có thay đổi | không thể ghi tệp `-o` | đầu vào bị thiếu, không đọc được hoặc không hỗ trợ, hoặc bản quét chưa hoàn chỉnh nhưng thiếu `--allow-partial` | phát hiện thay đổi, quan sát chưa xác nhận hoặc bản quét chưa hoàn chỉnh | - |
| `export` | đã ghi tập lệnh | không thể ghi tập lệnh | đầu vào không đọc được, bản quét chưa hoàn chỉnh thiếu `--allow-partial` hoặc dữ liệu không thể xuất an toàn | - | - |

## Cấu trúc mã nguồn

| Mô-đun | Nhiệm vụ |
| --- | --- |
| `cli.py` | Tùy chọn dòng lệnh, phân giải hồ sơ, preflight, quét và xuất báo cáo |
| `scanner.py`, `probes.py` | Mở rộng mục tiêu, worker có giới hạn, khám phá host và quan sát dịch vụ |
| `config.py`, `profiles.py` | Định nghĩa dịch vụ và các hồ sơ kiểm kê đã xác thực |
| `models.py`, `output.py` | Kiểu dữ liệu kết quả và hiển thị terminal/JSON/CSV |
| `history.py`, `diff.py` | Lịch sử SQLite và so sánh bản chụp tệp theo phiên bản |
| `preflight.py` | Kiểm tra cục bộ và tra cứu phiên bản Nmap có giới hạn |
| `export.py` | Tập lệnh nhập Kadupul đã xác thực và trích dẫn an toàn |

Mỗi quan sát dịch vụ ghi nhận trạng thái tách biệt với danh tính mà dịch vụ tự công bố. Thao tác đọc và thời hạn đều bị giới hạn; ngoại lệ của probe được giữ lại trong danh sách lỗi của host. Lịch sử SQLite sử dụng giao dịch, dọn dẹp kết nối tường minh và các đường dẫn liệt kê/so sánh chỉ đọc. Thông tin bí mật SNMP chỉ đi vào thông qua biến môi trường hoặc tệp bí mật; lịch sử kiểm kê chỉ lưu các thiết lập hiệu lực không chứa bí mật. Xem [Kiến trúc](../../../docs/architecture.md) để biết quy trình quét, các giới hạn và ranh giới tin cậy, và [SECURITY.md](../../../SECURITY.md#authorized-use) về phạm vi sử dụng hợp lệ.


## Cách sử dụng

Chỉ quét những mạng do bạn quản trị.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Tùy chọn | Ý nghĩa |
| --- | --- |
| `NETWORK` | CIDR, IP hoặc hostname; tùy chọn khi dùng `--profile`. Các định danh phạm vi IPv6 bị từ chối. |
| `-o, --output PATH` | Ghi báo cáo ra tệp. Định dạng theo phần mở rộng (`.json`, `.csv`); các phần mở rộng khác mặc định dùng JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Ép định dạng báo cáo. Không có tác dụng nếu thiếu `--output`. `.sh` chọn `kadupul`. |
| `-v, --verbose` | Ghi nhật ký gỡ lỗi chi tiết. |
| `-q, --quiet` | Ẩn kết quả, tiến trình và log thông tin; cảnh báo và lỗi vẫn xuất hiện trên stderr. |
| `--backend asyncio\|nmap` | Cách khám phá host. `asyncio` (mặc định) probe trực tiếp các cổng dịch vụ; `nmap` chạy ping sweep bằng nmap trước và cần tệp thực thi `nmap` trên `PATH`. |
| `--timeout SECONDS` | Thời gian chờ cho các probe không tự đặt ngân sách thời gian riêng (mặc định 1.0). Các connect probe tích hợp sẵn dùng 0.3 giây trừ khi bảng dịch vụ đặt `timeout`. |
| `--concurrency N` | Số lượng probe chạy song song cùng lúc (mặc định 256). |
| `--deadline SECONDS` | Dừng toàn bộ lượt quét, bao gồm cả quét nmap, sau khoảng thời gian này (mặc định 3600, tối đa 604800; biến môi trường `HOSTCENSUS_DEADLINE`). Các host đã hoàn tất được ghi vào báo cáo với `"complete": false`, không ghi lịch sử hay bản chụp, và `scan` thoát với mã 4. |
| `--config PATH` | Tệp TOML định nghĩa dịch vụ và các thiết lập `[profiles]` đặt tên tùy chọn. |
| `--profile NAME` | Dùng một hồ sơ đặt tên sẵn; mặc định đọc `hostcensus.toml` khi bỏ qua `--config`. |
| `--exclude IP/CIDR` | Thêm một mục loại trừ; lặp lại tùy ý. Một host IPv4 bị loại trừ cũng tự động loại trừ các địa chỉ IPv6 dẫn tới nó: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) và 6to4. Các mục tiêu và mục loại trừ dạng IPv4-mapped được xử lý như địa chỉ IPv4 tương ứng. |
| `--max-hosts N` | Giới hạn số địa chỉ được kiểm tra trước khi áp dụng loại trừ (mặc định/tối đa cứng là 65.536). |
| `--history PATH` | Ghi nhận lượt quét đã hoàn tất vào cơ sở dữ liệu lịch sử SQLite tùy chọn. |
| `--services NAMES` | Danh sách tên dịch vụ phân tách bằng dấu phẩy cần kiểm tra, theo đúng thứ tự đó (mặc định: tất cả). |
| `--ports SPEC` | Danh sách `NAME=PORT` (di chuyển cổng của một dịch vụ) hoặc `PORT` (thêm kiểm tra TCP thuần mang tên `tcp-PORT`) phân tách bằng dấu phẩy. |
| `--snmp-community-file PATH` | Tệp chứa chuỗi community SNMPv2c cho truy vấn system MIB. Biến môi trường: `HOSTCENSUS_SNMP_COMMUNITY` (giá trị) hoặc `HOSTCENSUS_SNMP_COMMUNITY_FILE` (đường dẫn). |
| `--snmp-user` | Tên người dùng SNMPv3. Biến môi trường: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (mặc định), `SHA224`, `SHA256`, `SHA384`, `SHA512` và tệp chứa cụm mật khẩu. Biến môi trường: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` hoặc `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (mặc định), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` và tệp chứa cụm mật khẩu. Biến môi trường: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` hoặc `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Đồng thời ghi một bản chụp có phiên bản cho lệnh `hostcensus diff`. |
| `--tls-ca-file PATH` | Xác minh chứng chỉ HTTPS theo gói PEM này thay cho kho chứng chỉ của hệ thống. Biến môi trường: `HOSTCENSUS_TLS_CA_FILE`. |

Theo mặc định, mỗi host được kiểm tra SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) và HTTPS (TCP 443). Các cổng TCP được kiểm tra bằng kết nối đầy đủ (full connect). SNMP được kiểm tra bằng yêu cầu khám phá engine SNMPv3, loại yêu cầu mà mọi agent SNMPv3 phải trả lời không cần thông tin xác thực; các agent chỉ hỗ trợ v1/v2c sẽ không được phát hiện qua probe này. Với backend asyncio, một host được tính là đang hoạt động khi bất kỳ probe nào nhận được phản hồi, bao gồm cả kết nối bị từ chối, vì vậy host nào đánh rơi mọi probe sẽ có `alive=false` và lỗi "Host is down"; điều này không chứng minh host bị tắt về mặt vật lý. Với `--backend nmap`, nmap quyết định host nào đang hoạt động (ICMP khi có quyền root, hoặc TCP 80/443 trong trường hợp khác).

<a name="fingerprints"></a>

### Dấu vân tay dịch vụ

Mỗi dịch vụ đang mở được lấy dấu vân tay từ dữ liệu nó gửi ra trước khi đăng nhập. Không có giao thức nào thực hiện xác thực ngoại trừ truy vấn SNMP, và chỉ khi bạn cung cấp thông tin xác thực.

| Probe | Dữ liệu đọc | `version` | Các khóa `details` |
| --- | --- | --- | --- |
| `ssh` | dòng định danh RFC 4253 | phần mềm, ví dụ `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | bắt tay khởi tạo MySQL/MariaDB | phiên bản máy chủ | `server_version`, `flavor`, `auth_plugin`, hoặc `error_code`/`error` |
| `http` | phản hồi `HEAD /` | header `Server` | `status`, `server` |
| `https` | bắt tay TLS, chứng chỉ, `HEAD /` | header `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | khám phá SNMPv3; khi có thông tin xác thực, GET sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; khi có thông tin xác thực: `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, hoặc `snmp_error` |

Mục tiêu dạng hostname được phân giải một lần cho mỗi host và mọi probe đều kết nối tới địa chỉ đó, được ghi lại dưới dạng `address` trong kết quả; tên miền chỉ dùng cho TLS SNI, xác minh chứng chỉ và header HTTP `Host`. Tên không phân giải được sẽ trả về các trạng thái `unknown` và lỗi `Cannot resolve`. Tên DNS ngược chỉ được giữ lại khi chứa các ký tự hợp lệ của hostname, và tối đa 16 lượt tra cứu chạy cùng lúc. HTTPS thực hiện xác minh chứng chỉ và hostname dựa trên kho tin cậy hệ thống hoặc `--tls-ca-file`. Kho tin cậy được nạp một lần cho cả lượt quét và dùng lại cho mọi probe HTTPS. Kết nối TCP và bắt tay TLS được tính giờ riêng biệt, nên một cổng chấp nhận kết nối nhưng bị treo ở bước bắt tay sẽ có trạng thái `open` kèm `tls_error`, chứ không phải `filtered`. Nếu xác minh thất bại, kết quả ghi nhận `cert_verified: false` và `cert_verify_error`; công cụ không thử lại với thiết lập yếu hơn và không gửi yêu cầu HTTP. Chi tiết chứng chỉ và header HTTP chỉ được thu thập sau khi xác minh thành công. Hãy cung cấp gói CA phù hợp cho các dịch vụ dùng CA nội bộ. Các báo cáo cũ hơn có thể chứa `cert_read_unverified`, trường mà các probe hiện tại không còn sinh ra nữa.

Thông tin bí mật SNMP chỉ được đọc từ biến môi trường hoặc từ tệp (`--snmp-*-file`, hoặc biến `HOSTCENSUS_SNMP_*_FILE` tương ứng), không bao giờ nhận trực tiếp từ giá trị trên dòng lệnh vì người dùng cục bộ khác có thể thấy trong danh sách tiến trình. `--snmp-community`, `--snmp-auth-key` và `--snmp-priv-key` kèm giá trị sẽ thoát với mã 2 và thông báo tùy chọn thay thế. Tệp bí mật phải là UTF-8 không rỗng có kích thước tối đa 4096 byte; một ký tự xuống dòng ở cuối được bỏ qua, và việc đặt cả biến môi trường lẫn tệp cho cùng một bí mật sẽ gây lỗi. Thông báo lỗi nêu tên tệp nhưng không bao giờ in nội dung tệp. Báo cáo quét và lịch sử không chủ đích lưu giá trị thông tin xác thực. Trình xuất có tùy chọn `--include-credentials` riêng và tường minh được mô tả bên dưới. Chuỗi community chọn SNMPv2c; tên người dùng chọn SNMPv3, có xác thực khi cung cấp auth key và có mã hóa riêng tư khi cung cấp cả hai khóa (`snmp_security_level` ghi lại mức đã dùng). hostcensus từ chối với mã thoát 2 nếu kết hợp community với người dùng v3, dùng khóa riêng tư mà không có khóa xác thực, hoặc dùng khóa mà không có tên người dùng, và không bao giờ thử lại truy vấn v3 thất bại bằng v2c hay mức bảo mật thấp hơn. Các agent chỉ nói v1/v2c sẽ bỏ qua gói khám phá v3 không cần xác thực, nên chúng chỉ hiển thị ở trạng thái mở khi có community được cung cấp.

Văn bản banner được lọc còn các ký tự in được và cắt gọn ở mức tối đa 256 ký tự trước khi lưu trữ hoặc hiển thị. Thao tác đọc cũng bị giới hạn: 4 KiB mỗi dòng, 4 KiB cho gói chào MySQL, 16 KiB cho các header HTTP. Engine ID của SNMP dài quá 32 octet sẽ bị cắt bớt trước khi lưu. HTTP và HTTPS gửi header Host với địa chỉ IPv6 đặt trong dấu ngoặc vuông và kèm số cổng khi khác 80 hoặc 443. Các ô CSV bắt đầu bằng ký tự kích hoạt công thức bảng tính được thêm tiền tố để ô luôn giữ ở dạng văn bản.

### Các giới hạn

Một lần chạy chấp nhận tối đa 65.536 địa chỉ, 64 dịch vụ và 524.288 probe (số host nhân số dịch vụ); yêu cầu lớn hơn sẽ thoát với mã 2 trước khi gửi bất kỳ gói tin nào. `--concurrency` bị giới hạn ở 4096 socket. Mỗi probe có thời hạn cứng bằng bốn lần ngân sách thời gian riêng của nó. Các connect probe (`tcp`, `ssh`, `mysql`, `http`) dùng 0.3 giây trừ khi dịch vụ đó đặt `timeout`. SNMP và HTTPS dùng `--timeout` (mặc định 1.0) khi dịch vụ không đặt riêng. Probe chạm ngưỡng thời hạn được báo cáo là `unknown` kèm "probe timed out" trong `errors`. Các lỗi socket cục bộ (ví dụ cạn kiệt file descriptor) cũng có trạng thái `unknown` kèm thông báo lỗi được ghi lại; chúng không bao giờ bị tính là cổng bị lọc hay host ngừng hoạt động. Trước khi gửi probe, hostcensus nâng giới hạn mềm số tệp mở lên gần giới hạn cứng để đủ cho `--concurrency` cộng thêm 64 descriptor; khi không thể nâng, bước kiểm tra preflight `open files` sẽ thất bại và `scan` thoát với mã 1 trước khi gửi lưu lượng. Khám phá bằng Nmap dùng thời gian chờ mỗi host là 30 giây. Tiền tố mạng được truyền cho nmap ở dạng CIDR, và lượt quét sẽ thất bại với mã thoát 1 khi nmap báo cáo ít địa chỉ hơn số địa chỉ được giao (ví dụ tên miền không phân giải được) thay vì đánh dấu các host đó là ngừng hoạt động. Mục tiêu dạng hostname được phân giải một lần và địa chỉ đó được truyền cho nmap, nên bước khám phá và các probe chạm đúng cùng một máy. Một tiền tố đầy đủ chạy trong một tiến trình nmap với thời hạn tiến trình con là 35 giây cho mỗi 256 địa chỉ, làm tròn lên. Lượt quét có mục loại trừ chia thành từng lô 256 host với thời hạn 35 giây cho mỗi lô. Việc tạo worker được giới hạn độc lập với kích thước dải mạng. Reverse DNS và phân giải hostname có thời hạn riêng là hai giây; một lời gọi phân giải không phản hồi sẽ bị bỏ lại trên luồng riêng của nó để không giữ hostcensus chạy quá các giới hạn này. Tối đa 16 lượt tra cứu chạy cùng lúc, và một lời gọi bị bỏ lại vẫn giữ khe của nó cho tới khi tự trả về, nhờ vậy số luồng bị treo luôn nằm trong giới hạn; nếu cả 16 luồng cùng treo, các lượt tra cứu sau sẽ xếp hàng chờ khe ngoài thời hạn hai giây (đồng hồ hai giây chỉ bắt đầu khi có khe trống) cho đến khi `--deadline` dừng lượt quét. `NetworkScanner` khi dùng như thư viện mà không truyền `deadline` có thể chờ khe như vậy vô thời hạn. `--deadline` (mặc định một giờ) bao trùm và giới hạn toàn bộ lượt chạy bên trên các mức này.

### Cấu hình dịch vụ

Các dịch vụ có thể được tùy chỉnh bằng tệp TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` là một trong `tcp`, `ssh`, `mysql`, `http`, `https` hoặc `snmp`, và mặc định lấy theo tên dịch vụ nếu tên đó là một loại probe, ngược lại dùng `tcp`. Chỉ `snmp` sử dụng UDP. Tên dịch vụ gồm chữ cái thường, chữ số, `-` và `_`. Hai dịch vụ không thể dùng chung một cổng và giao thức; lịch sử ghi nhận một trạng thái duy nhất cho cặp đó. `timeout` là tùy chọn, tính bằng giây và tối thiểu 0.05. Các probe kiểu kết nối (`tcp`, `ssh`, `mysql`, `http`) mặc định là 0.3 giây. `snmp` và `https` dùng `--timeout` của lượt quét khi dịch vụ không đặt `timeout`. `--timeout` không ghi đè ngân sách thời gian mà dịch vụ đã khai báo.

Báo cáo JSON là các tài liệu có phiên bản (`"format": "hostcensus-report"`, `"version": 1`) ghi lại mục tiêu, các dịch vụ đã probe và thiết lập bên cạnh `devices`; `--format json` không kèm `-o` sẽ xuất báo cáo ra stdout thay cho dạng bảng. Mọi đầu ra JSON đều có lược đồ được công bố; xem [Đầu ra JSON](../../../docs/json-output.md). Các thiết bị giữ nguyên các trường gốc `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` và `errors`, đồng thời bổ sung danh sách `services` chứa `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, hoặc `unknown` khi probe lỗi cục bộ hay quá thời hạn), `version` và `details` của từng probe. Đầu ra CSV có thêm các cột `services` và `versions` ở cuối cho các dịch vụ đang mở. Các giá trị boolean `ssh`, `snmp` và `mysql` đi theo đúng các dịch vụ có tên chính xác như vậy.


<a name="inventory-profiles-preflight-and-local-history"></a>

## Hồ sơ kiểm kê, kiểm tra preflight và lịch sử cục bộ

Các hồ sơ đặt tên sẵn dùng chung tệp TOML với các định nghĩa `[services]` hiện có. Sao chép [hostcensus.example.toml](../../../hostcensus.example.toml) thành `hostcensus.toml` và thiết lập các mạng do bạn quản trị:

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

`preflight` phân giải các tùy chọn và hồ sơ giống hệt như `scan`, bao gồm cả `--concurrency` cho bước kiểm tra số tệp mở, nên khi preflight đạt nghĩa là `scan` sẽ khởi chạy với cùng kế hoạch đó.

Hồ sơ hỗ trợ các khóa `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency` và `max_hosts`. `services` và `ports` dùng cú pháp danh sách phân tách bằng dấu phẩy hiện có. Các tùy chọn CLI tường minh sẽ ghi đè thiết lập của hồ sơ; nhiều tùy chọn `--exclude` lặp lại sẽ cộng dồn vào danh sách loại trừ của hồ sơ. Mục tiêu mạng chỉ định tường minh đi kèm `--profile` phải nằm trong phạm vi IP/CIDR của hồ sơ đó. Hostname vẫn được hỗ trợ cho các lượt quét trực tiếp, nhưng không thể kết hợp với loại trừ IP. Giới hạn số host được áp dụng trước khi loại trừ; tổng giới hạn probe vẫn được áp dụng sau đó. Các host bị loại trừ được bỏ qua ở cả bước kiểm tra dịch vụ lẫn bước khám phá Nmap tùy chọn.

Mọi lượt quét đều thực hiện kiểm tra preflight cục bộ trước khi gửi lưu lượng tới mục tiêu: giới hạn mục tiêu/probe, quyền truy cập đích ghi, tính khả dụng của tệp thực thi/wrapper Nmap tùy chọn, lược đồ lịch sử và gói CA TLS đã cấu hình. `preflight` xuất báo cáo JSON và không quét mục tiêu hay tạo cơ sở dữ liệu lịch sử. Lệnh này tạm thời ghi một tệp cùng cấp để kiểm tra quyền ghi đích mà không làm thay đổi nội dung hiện có. Backend asyncio mặc định vẫn không đòi hỏi Nmap lẫn quyền root. Các đường dẫn đích phải tách biệt với nhau và tách biệt với cấu hình đầu vào, kể cả hard link; các symlink đích đều bị từ chối. Kiểm tra thất bại trả về mã 1; phạm vi/cấu hình không hợp lệ trả về mã 2.

Thao tác ghi báo cáo và xuất tệp yêu cầu hỗ trợ `O_NOFOLLOW`. Trên các nền tảng không hỗ trợ, bao gồm Windows, các thao tác ghi này sẽ thất bại mà không mở hay cắt xén tệp đích. Báo cáo và tập lệnh xuất mới được tạo với quyền chỉ dành cho chủ sở hữu (mode 0600); việc ghi đè lên tệp hiện có sẽ giữ nguyên quyền của tệp đó. Ghi vào một named pipe chưa có tiến trình đọc sẽ thất bại ngay lập tức thay vì chờ đợi. Tệp `--history` mới cũng được tạo với quyền chỉ chủ sở hữu; tệp lịch sử có sẵn giữ nguyên mode cũ. Các thông điệp log luôn đi ra stderr, vì vậy stdout chỉ chứa kết quả. Các bản xuất có chứa thông tin xác thực luôn bắt buộc đặt mode 0600.

Lịch sử là tính năng tùy chọn bổ sung cho các bản chụp JSON và lệnh `diff` hiện có:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Sử dụng các ID từ `history`; ví dụ giả định đây là một cơ sở dữ liệu mới. Các bản chụp được lưu theo giao dịch cùng thời điểm bắt đầu/kết thúc theo UTC, phiên bản gói, các thiết lập hiệu lực không chứa bí mật, phần tóm tắt và toàn bộ quan sát host/dịch vụ, bao gồm lỗi trên từng host. Các quan sát của những host chưa hoàn tất vẫn được giữ lại. Các lượt chạy bị hủy sẽ không được lưu. Các quy ước hiện có về báo cáo, bản chụp, xuất tệp và mã thoát của lệnh quét vẫn được giữ nguyên.

`history` liệt kê các bản tóm tắt JSON mà không cần đọc toàn bộ dữ liệu thiết bị lịch sử. `compare` đọc hai lượt quét đã lưu, yêu cầu danh tính mục tiêu và các cổng được chọn phải giống hệt nhau, rồi báo cáo các thay đổi về khả năng phản hồi, trạng thái và trạng thái cổng. ID của lượt quét trước phải đứng trước ID của lượt quét sau. Khi cả hai lượt quét đều có ghi nhận `timeout` hoặc `backend` và các giá trị đó khác nhau, báo cáo vẫn liệt kê một cảnh báo và vẫn so sánh các quan sát. Thời gian chờ khác nhau có thể khiến một cổng bị lọc trông như đang mở. Lỗi trình quét và các quan sát cổng `unknown` được gắn cờ là chưa chắc chắn thay vì coi là đã biến mất hoặc đã đóng một cách chắc chắn: các host có lỗi xuất hiện trong `uncertain_hosts`, và mọi chuyển đổi trạng thái cổng có liên quan đến `unknown` (bao gồm `unknown` ở cả hai lần quét) được liệt kê trong `unconfirmed_ports` thay vì `port_changes`, ngoại trừ trường hợp cổng đó ở trạng thái mở trong lần quét sau thì được tính là một thay đổi cổng. `compare` và `diff` phân loại cổng theo cùng một quy tắc. `no_longer_responding` nghĩa là không nhận được phản hồi, chứ không phải bằng chứng thiết bị đã bị gỡ bỏ. Mã thoát 0 của lệnh quét không đảm bảo mọi host đều đã phản hồi: hãy kiểm tra lỗi trên từng host. So sánh thành công trả về 0 bất kể có thay đổi hay không; lệnh `diff` trên tệp vẫn giữ nguyên quy ước mã thoát 3. Lịch sử không được hỗ trợ hoặc bị hỏng trả về mã 1.

Lịch sử lưu giữ thông tin kiểm kê, vì vậy hãy chọn một thư mục cục bộ được bảo vệ phù hợp. Tệp hồ sơ và các thiết lập được lưu không chứa thông tin xác thực SNMP; việc xử lý thông tin xác thực tiếp tục đi qua các tùy chọn thời gian chạy/biến môi trường hiện có.

<a name="inventory-diff"></a>

## So sánh kiểm kê (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Một bản chụp là tệp JSON có `format: "hostcensus-snapshot"`, `version: 1`, phiên bản hostcensus, thời gian tạo theo UTC, mục tiêu, `timeout` và `backend` của lượt quét khi lượt quét có ghi lại chúng, các dịch vụ đã probe và danh sách các host đang hoạt động theo cùng cấu trúc với báo cáo `-o`. Các host ngừng hoạt động bị lược bỏ. `diff` cũng chấp nhận các báo cáo JSON thông thường từ `scan -o`, kể cả các tệp có từ trước khi trường `services` ra đời.

`diff` báo cáo các host mới và đã biến mất, các cổng mở ra hoặc đóng lại trên những host có mặt ở cả hai lần quét, và các dịch vụ có `version` thay đổi. Những cổng chỉ được probe trong một trong hai lượt quét sẽ không được so sánh, kèm theo một cảnh báo nêu rõ điều đó. Các quan sát bị lỗi không bao giờ được hiểu là "không thay đổi": một cổng có trạng thái `unknown` ở một trong hai lượt quét và không mở ở lượt sau được liệt kê trong `unconfirmed`, chứ không phải `closed`, với `before` là `open`, `unknown` hoặc `not-open` (đã probe và đóng hoặc bị lọc) và `after` là `unknown` hoặc `not-open`; một cổng hiện đang mở được báo cáo trong `opened` ngay cả khi probe trước đó bị lỗi. Một host mà mọi probe đều lỗi không có phản hồi ở một trong hai lượt quét được liệt kê trong `unsettled_hosts` (với `before`/`after` là `up`, `uncertain` hoặc `absent`, kể cả khi host đó lỗi ở cả hai lượt quét hoặc thiếu ở tệp còn lại) thay cho `vanished_hosts`; nếu host đó trả lời ở lượt quét sau thì nó cũng được báo cáo là host mới kèm các cổng mở của nó. Các bản chụp giữ lại những host bị lỗi này vì lý do đó. Một cảnh báo cũng xuất hiện khi mục tiêu khác nhau, và khi cả hai tệp đều ghi nhận timeout hoặc backend với giá trị khác nhau. `-o PATH` đồng thời ghi dạng JSON ra tệp.

Báo cáo từ một lượt quét bị dừng bởi `--deadline` (`"complete": false`) chỉ liệt kê những host mà nó kịp chạm tới, nên `diff` và `export` từ chối nó với mã thoát 2. `--allow-partial` cho phép chấp nhận báo cáo đó kèm một cảnh báo lên stderr: khi đó `diff` liệt kê các host không hề có mặt trong bản quét chưa hoàn chỉnh vào `unsettled_hosts` với trạng thái `unscanned` thay vì coi là đã biến mất (host được ghi nhận là ngừng hoạt động vẫn tính là đã biến mất), đặt `partial` thành true và không bao giờ báo không thay đổi, còn `export` ghi một cảnh báo vào phần đầu của tập lệnh.

Các mã thoát của `diff`: `0` không có thay đổi, `3` phát hiện thay đổi, có quan sát chưa thể xác nhận hoặc đầu vào chưa hoàn chỉnh (`changed` là true bất cứ khi nào có danh sách khác rỗng, bao gồm `unsettled_hosts` và `unconfirmed`, hoặc `partial` là true), `2` thiếu tệp, không đọc được, không phải bản chụp được hỗ trợ hoặc chưa hoàn chỉnh mà thiếu `--allow-partial`, `1` không thể ghi tệp `-o`.

<a name="kadupul-export"></a>

## Xuất sang Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (một nhánh tách của Cacti 1.2.31) không có tính năng nhập tệp thiết bị hàng loạt. Cách được hỗ trợ để thêm thiết bị bằng tập lệnh là `cli/add_device.php`, mỗi lần gọi cho một thiết bị với các tham số `--option=value`. `hostcensus export` tạo ra một tập lệnh `sh` chuẩn POSIX chứa các lời gọi đó:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Mỗi host đang hoạt động trở thành `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Các host có truy vấn SNMP thành công trong lượt quét nhận `--version=2 --community=...` hoặc `--version=3 --username=... --authproto=... --password=...` (cộng thêm `--privproto`/`--privpass` cho authPriv), `--port` và `--avail=snmp`. Xuất SNMPv3 cần `--snmp-user`, và chế độ noAuthNoPriv bị từ chối vì `add_device.php` bắt buộc phải có mật khẩu v3.
- Các host khác nhận `--version=0 --avail=ping`, với `--ping_method=tcp --ping_port=` là cổng TCP mở đầu tiên, hoặc ICMP nếu không có cổng TCP nào mở.
- `--notes` liệt kê các dịch vụ đang mở và phiên bản. `--description` lấy tên reverse-DNS khi tên đó chỉ gồm ký tự đơn giản (chữ cái, chữ số, `.`, `_`, `-`), nếu không sẽ dùng IP, và được đảm bảo duy nhất vì `add_device.php` coi một mô tả đã tồn tại là thao tác cập nhật thiết bị đó.

Mọi giá trị đều được xác thực và trích dẫn cho shell bằng `shlex.quote`. Theo mặc định không có bí mật SNMP nào được ghi vào tệp: tập lệnh tự mở rộng `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` hoặc `HOSTCENSUS_SNMP_PRIV_KEY` lúc chạy và dừng lại nếu một trong số đó chưa được thiết lập. Ngược lại, `--include-credentials` ghi trực tiếp giá trị từ các biến môi trường đó vào tập lệnh, tạo tệp với mode 0600 và ghi log cảnh báo. Bản thân `add_device.php` in ra chuỗi community và nhận bí mật dưới dạng tham số dòng lệnh, vốn có thể nhìn thấy trong danh sách tiến trình trên máy chủ Kadupul trong lúc mỗi lệnh đang chạy.

`add_device.php` thoát với mã 1 khi gặp trùng lặp hoặc lỗi; tập lệnh vẫn chạy tiếp, đếm số lượt thất bại và thoát với mã 1 nếu có bất kỳ thiết bị nào không được thêm vào. Các ID mẫu lấy từ `php cli/add_device.php --list-host-templates`. Mã thoát của `export`: `0` đã ghi xong, `2` đầu vào không đọc được, bản quét chưa hoàn chỉnh thiếu `--allow-partial` hoặc dữ liệu không thể xuất an toàn, `1` không thể ghi tập lệnh.

## Quy trình đánh phiên bản và phát hành

hostcensus tuân theo [Semantic Versioning](https://semver.org/spec/v2.0.0.html): các bản vá tương thích tăng số phiên bản patch, tính năng tương thích hoặc thông báo lỗi thời tăng số minor, và thay đổi phá vỡ tương thích tăng số major. Các lệnh và tùy chọn, mã thoát và các lược đồ JSON là hợp đồng công khai; hành vi đã đánh dấu lỗi thời vẫn tiếp tục hoạt động cho đến bản phát hành chính tiếp theo, trừ khi bản vá bảo mật buộc phải thay đổi sớm hơn (khi đó changelog sẽ nêu rõ lý do).

release-please mở một PR phát hành từ các tiêu đề Conventional Commit trên nhánh `main`, nâng phiên bản trong `pyproject.toml`, `uv.lock` và `CHANGES.md`. Khi hợp nhất PR đó, thẻ `vMAJOR.MINOR.PATCH` và một bản phát hành nháp trên GitHub sẽ được tạo ra, rồi CI đính kèm gói wheel đã kiểm thử, bản phân phối mã nguồn và các mã kiểm tra checksum; GitHub lưu trữ chứng thực bản dựng cho các tệp đó thông qua API attestations. Một người bảo trì sẽ rà soát và công bố bản nháp sau khi các tệp đã được đính kèm. Các bản phát hành không bao giờ bị ghi đè thay thế.

Cơ chế xuất bản tin cậy PyPI mang tính tùy chọn và yêu cầu quyền sở hữu dự án, một trusted publisher và môi trường `pypi`. Cơ chế này xuất bản đúng các tệp phát hành đã kiểm tra đó mà không cần build lại hay lưu API token. Các bản phát hành gắn thẻ trong kho lưu trữ công khai này tạo ra chứng thực artifact trên GitHub; các nhánh fork riêng tư đòi hỏi gói dịch vụ được hỗ trợ và bật tùy chọn tường minh. Xem [hướng dẫn phát hành đầy đủ](../../../docs/releasing.md) để biết cách thiết lập, các lệnh chính xác và cách thử lại.

## Phát triển

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Các công cụ phát triển nằm trong các nhóm phụ thuộc [PEP 735](https://peps.python.org/pep-0735/) trong `pyproject.toml` (`dev`, `fuzz`, `build`), nên chúng không bao giờ xuất hiện trong siêu dữ liệu của gói đã xuất bản. `uv.lock` là tệp khóa duy nhất; CI cài đặt bằng `uv sync --locked` và báo lỗi khi tệp khóa bị cũ. Chọn trình thông dịch bằng `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) hoặc bất kỳ bản Python 3.12+ nào.

CI áp dụng mức độ bao phủ mã tối thiểu 90% cho gói. Các bài kiểm thử đơn vị bao gồm máy chủ loopback có kiểm soát và các kịch bản kiểm tra hồ sơ/lịch sử/trình xác thực phát hành ngoại tuyến; môi trường lab Compose chạy OpenSSH, MariaDB, nginx và net-snmp trên một cầu nối mạng cô lập. Chạy môi trường này bằng `make test-integration`. Xem [CONTRIBUTING.md](../../../CONTRIBUTING.md) và [công cụ phát hành](../../../scripts/README.md).

Container runtime chạy với UID/GID 10001, không có thư mục home, không có shell đăng nhập và không có pip, và có thể ghi vào `/app/output`. Hãy cấp quyền ghi cho người dùng đó trên mọi thư mục đầu ra được gắn kết. Container không cần Linux capability nào và hoạt động tốt với hệ thống tệp gốc chỉ đọc, nên có thể chạy như sau:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap sử dụng hành vi khám phá TCP không cần đặc quyền trong container này. CI đánh trượt quá trình build image nếu Trivy báo cáo bất kỳ lỗ hổng HIGH hoặc CRITICAL nào có thể khắc phục được.

## Kiểm tra chuỗi cung ứng

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) chạy trên nhánh main và hàng tuần, công bố điểm số thực tế và tải các phát hiện lên hệ thống quét mã của GitHub. Các Action và base image container đều được ghim theo mã băm bất biến; các gói phụ thuộc Python được cố định trong `uv.lock`. Lỗi từ Bandit làm CI thất bại, và kiểm thử fuzz bằng Atheris có giới hạn sẽ kiểm tra các bộ phân tích SSH, MySQL, HTTP, chứng chỉ và SNMPv3 BER mà không cần truy cập mạng.

Scorecard cũng đo lường lịch sử hoạt động rà soát, sự đa dạng người đóng góp và nguồn gốc phát hành. Các điểm số đó phản ánh bằng chứng thực tế; chúng không phải tuyên bố rằng mọi tiêu chí quản trị hay lịch sử phát hành đều đã được thỏa mãn. Xem [SECURITY.md](../../../SECURITY.md) và [nguồn gốc phát hành](../../../docs/releasing.md).

## Bản địa hóa

Thông báo CLI và các bảng tóm tắt/so sánh trên terminal hỗ trợ 45 ngôn ngữ (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) mà không cần thêm bất kỳ gói phụ thuộc runtime nào. Thứ tự phân giải ưu tiên `--lang`, tiếp đến là `LC_ALL`, `LC_MESSAGES` và `LANG`, cuối cùng lùi về `en`. Các lược đồ JSON, cột CSV và tập lệnh xuất không thay đổi trên tất cả các ngôn ngữ.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Đóng góp

Các đóng góp nên đi kèm một trường hợp có thể tái hiện được, bảo toàn các hợp đồng CLI và định dạng dữ liệu đã tài liệu hóa, và vượt qua các bước kiểm tra chất lượng nêu trên. Xem [CONTRIBUTING.md](../../../CONTRIBUTING.md) để biết quy trình phát triển và [hướng dẫn phát hành](../../../docs/releasing.md) cho các quyết định về tương thích và đánh phiên bản.

## Trạng thái bảo mật và giấy phép

Xem [SECURITY.md](../../../SECURITY.md) để biết quy trình báo cáo riêng tư và các phiên bản được hỗ trợ.
hostcensus được cấp phép theo [Giấy phép MIT](../../../LICENSE).

Phần đầu tệp mã nguồn sử dụng định danh SPDX và bảo toàn ghi nhận đóng góp từ lịch sử Git. Xem [AUTHORS.md](../../../AUTHORS.md) để biết thông tin tác giả. Các tệp dữ liệu kiểm thử nhị phân và tệp khóa được sinh tự động sử dụng các tệp `.license` đi kèm; toàn văn MIT nằm tại `LICENSES/MIT.txt`.
