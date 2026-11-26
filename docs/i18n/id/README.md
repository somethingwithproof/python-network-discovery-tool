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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · **Bahasa Indonesia**

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus adalah CLI Python untuk inventarisasi layanan yang dapat diulang pada jaringan yang Anda kelola.
Alat ini mencatat apa yang diekspos oleh perangkat, membandingkan hasil pengamatan dari waktu ke waktu, dan menghasilkan
skrip impor Kadupul. Backend bawaannya menggunakan soket asyncio tanpa akses root;
penemuan Nmap opsional dapat mengidentifikasi host di luar port layanan yang dikonfigurasi.

## Mengapa hostcensus

Laporan port satu kali tidak menjelaskan apakah pengamatan berikutnya mengalami perubahan atau
sekadar gagal. hostcensus menggabungkan status layanan yang eksplisit, probe yang terukur batasnya, profil pemindaian
yang dapat digunakan ulang, dan riwayat lokal. Operator dapat mengulang cakupan yang sama, memeriksa
error, serta membedakan pengamatan yang belum pasti dari perubahan yang terkonfirmasi.

- **Bukti layanan:** identifikasi SSH, salam pembuka (greeting) MySQL, header HTTP, pengamatan
  sertifikat TLS, serta penemuan SNMP atau kueri system-MIB berkredensial.
- **Cakupan yang dapat diulang:** profil TOML bernama, pengecualian aditif, layanan yang dapat
  dikonfigurasi, batas host/probe, dan jumlah worker yang dibatasi.
- **Pemeriksaan sebelum lalu lintas jaringan:** preflight lokal memvalidasi target, alat, akses
  tujuan, skema riwayat, dan bundel CA TLS yang dikonfigurasi.
- **Riwayat inventaris:** snapshot SQLite transaksional menyimpan seluruh pengamatan;
  perbandingan tetap menampilkan kegagalan pemindai dan status tidak diketahui secara jelas.
- **Output yang interoperabel:** laporan terminal, JSON dan CSV, snapshot file berversi,
  dan skrip impor Kadupul.

CI mencakup Python 3.12, 3.13, dan 3.14 di Linux dan macOS, ditambah lab integrasi Compose
yang terkendali. Kodenya menggunakan alias tipe modern, hasil preflight bertipe,
profil berslot khusus kata kunci (keyword-only), dan pembersihan async terstruktur sambil tetap mempertahankan versi
runtime tersebut. Lihat [Pembuatan versi dan rilis](../../../docs/releasing.md) untuk kontrak kompatibilitas SemVer
dan proses rilis GitHub. Lencana rilis menggambarkan
artefak yang dipublikasikan, bukan checkout ini: tag terbaru yang dipublikasikan saat ini adalah
`v0.3.0`, sedangkan checkout ini menggunakan versi paket `3.0.0`. Instal dari checkout ini
untuk menggunakan fitur inventaris yang didokumentasikan di sini.

Mulai dengan [instalasi](#install), lalu [profil dan riwayat](#inventory-profiles-preflight-and-local-history).
Untuk detail integrasi, lihat [sidik jari layanan](#fingerprints),
[perbandingan file](#inventory-diff), dan [ekspor Kadupul](#kadupul-export).

## Instalasi

Diperlukan Python 3.12 atau yang lebih baru; Python 3.12–3.14 adalah matriks yang telah diuji. Dari
checkout ini, instal dependensi runtime yang terkunci:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Untuk penemuan host Nmap opsional, instal executable Nmap menggunakan pengelola paket
platform Anda; tidak diperlukan paket Python tambahan. Output XML Nmap diurai dengan
defusedxml, dependensi inti, sehingga ekspansi entitas ditolak. hostcensus menjalankan
`nmap` yang ditemukan di `PATH` secara langsung dengan daftar argumen tetap, batas waktu yang bertambah
seiring ukuran prefiks, dan batas output 64 MiB. Nmap tidak diperlukan untuk backend bawaan.

## Migrasi dari netprobe

hostcensus adalah nama baru dari netprobe, yang dirilis pada versi 3.0.0. Proyek ini tidak pernah
dipublikasikan ke PyPI dengan nama mana pun, sehingga instalasi berasal dari checkout atau rilis
GitHub. Repositori GitHub tetap mempertahankan namanya.

| Sebelumnya | Sekarang | Kompatibilitas |
| --- | --- | --- |
| Distribusi `netprobe` | `hostcensus` | Instal ulang dari checkout; tidak ada paket dengan nama lama. |
| Perintah `netprobe` | `hostcensus` | `netprobe` masih dapat dijalankan dan mencetak satu baris peringatan penghentian (deprecation) ke stderr. Kode keluar dan stdout tidak berubah. Akan dihapus pada rilis mayor berikutnya. |
| Variabel lingkungan `NETPROBE_*` | `HOSTCENSUS_*` | Variabel `NETPROBE_*` digunakan ketika pasangannya `HOSTCENSUS_*` tidak diatur, dengan satu peringatan stderr yang menyebutkan nama variabel tanpa pernah menyebutkan nilainya. `HOSTCENSUS_*` diutamakan jika keduanya diatur. Akan dihapus pada rilis mayor berikutnya. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Memutus kompatibilitas (Breaking).** Tidak ada shim impor yang terpasang; perbarui impor Anda. |
| Tag image Docker `network-discovery:test` (khusus CI) dan pengguna kontainer `netprobe` | `hostcensus:test`, pengguna `hostcensus` | Tidak ada image registri yang pernah dipublikasikan. Bangun ulang image dan gunakan entrypoint `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | File yang ada dengan nama bawaan lama tetap digunakan, disertai peringatan, selama nama baru belum ada. Path eksplisit `--config` dan `--history` tidak terpengaruh. |
| Laporan dan snapshot dengan `"format": "netprobe-report"` atau `"netprobe-snapshot"`, serta field `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` dan `export` tetap dapat memuat file yang ditulis dengan nama lama, dan Skema JSON yang dipublikasikan menerima kedua penulisan tersebut. File baru menggunakan nama baru. Basis data riwayat SQLite tidak berubah dan dimuat seperti sebelumnya. |
| Skrip Kadupul dari `netprobe export` | Skrip dari `hostcensus export` | Skrip lama tetap berfungsi dan masih membaca `NETPROBE_SNMP_*` saat dijalankan. Skrip baru membaca `HOSTCENSUS_SNMP_*`. |

## Contoh cepat

Dijalankan dari kontainer penguji pada lab integrasi yang dijelaskan di bagian Pengembangan; output dipangkas:

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

## Kode keluar

| Perintah | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | pengamatan/laporan tercatat | preflight/backend, riwayat, atau penulisan laporan/snapshot gagal | target, opsi, konfigurasi, atau batas tidak valid | - | `--deadline` tercapai; laporan parsial ditulis, riwayat dan snapshot dilewati |
| `preflight` | pemeriksaan lulus | pemeriksaan lokal gagal | target/konfigurasi tidak valid atau tujuan saling bertabrakan | - | - |
| `profiles` | profil tervalidasi ditampilkan | - | konfigurasi atau pilihan tidak dapat dibaca/tidak valid | - | - |
| `history` | ringkasan ditampilkan | riwayat tidak ada, tidak valid, atau tidak didukung | opsi CLI tidak valid | - | - |
| `compare` | perbandingan dihasilkan, termasuk saat ada perubahan | riwayat tidak dapat dibaca, cakupan/urutan tidak kompatibel, atau penulisan gagal | opsi CLI tidak valid | - | - |
| `diff` | tidak ada perubahan | file `-o` tidak dapat ditulis | input hilang, tidak dapat dibaca atau tidak didukung, atau pemindaian tidak lengkap tanpa `--allow-partial` | perubahan ditemukan, pengamatan belum terkonfirmasi, atau pemindaian tidak lengkap | - |
| `export` | skrip ditulis | skrip tidak dapat ditulis | input tidak dapat dibaca, pemindaian tidak lengkap tanpa `--allow-partial`, atau data tidak dapat diekspor dengan aman | - | - |

## Struktur modul

| Modul | Tanggung jawab |
| --- | --- |
| `cli.py` | Opsi perintah, resolusi profil, preflight, pemindaian, dan pelaporan |
| `scanner.py`, `probes.py` | Ekspansi target, worker terbatas, penemuan host, dan pengamatan layanan |
| `config.py`, `profiles.py` | Definisi layanan dan profil inventaris yang tervalidasi |
| `models.py`, `output.py` | Tipe hasil serta rendering terminal/JSON/CSV |
| `history.py`, `diff.py` | Riwayat SQLite dan perbandingan snapshot file berversi |
| `preflight.py` | Pemeriksaan lokal dan pencarian versi Nmap terbatas |
| `export.py` | Skrip impor Kadupul yang tervalidasi dan ter-quote dengan aman |

Setiap pengamatan layanan mencatat statusnya secara terpisah dari identitas yang diumumkan.
Pembacaan dan batas waktu dibatasi; pengecualian probe tetap tercatat pada error host. Riwayat SQLite
menggunakan transaksi, pembersihan koneksi eksplisit, serta jalur pembacaan daftar dan
perbandingan yang hanya-baca (read-only). Rahasia SNMP hanya masuk melalui variabel lingkungan atau file
rahasia; riwayat inventaris hanya menyimpan pengaturan efektif yang tidak bersifat rahasia. Lihat
[Arsitektur](../../../docs/architecture.md) untuk alur kerja pemindaian, batasannya, dan batas
kepercayaannya, serta [SECURITY.md](../../../SECURITY.md#authorized-use) untuk penggunaan yang diizinkan.


## Penggunaan

Pindai hanya jaringan yang Anda kelola.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opsi | Arti |
| --- | --- |
| `NETWORK` | CIDR, IP, atau nama host; opsional jika menggunakan `--profile`. Pengidentifikasi cakupan IPv6 ditolak. |
| `-o, --output PATH` | Tulis laporan. Format mengikuti ekstensi (`.json`, `.csv`); ekstensi lain kembali ke JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Paksa format laporan. Tidak berpengaruh tanpa `--output`. `.sh` memilih `kadupul`. |
| `-v, --verbose` | Logging debug. |
| `-q, --quiet` | Sembunyikan hasil, progres, dan log informasi; peringatan dan error tetap muncul di stderr. |
| `--backend asyncio\|nmap` | Penemuan host. `asyncio` (bawaan) melakukan probe langsung ke port layanan; `nmap` menjalankan ping sweep nmap terlebih dahulu dan membutuhkan executable `nmap` di `PATH`. |
| `--timeout SECONDS` | Waktu tunggu untuk probe yang tidak menetapkan anggarannya sendiri (bawaan 1.0). Probe koneksi bawaan menggunakan 0.3 detik kecuali tabel layanan menetapkan `timeout`. |
| `--concurrency N` | Jumlah probe yang berjalan bersamaan (bawaan 256). |
| `--deadline SECONDS` | Hentikan seluruh pemindaian, termasuk sweep nmap, setelah durasi ini (bawaan 3600, maksimal 604800; env `HOSTCENSUS_DEADLINE`). Host yang selesai ditulis ke laporan dengan `"complete": false`, tidak ada riwayat atau snapshot yang ditulis, dan `scan` keluar dengan kode 4. |
| `--config PATH` | Definisi layanan TOML dan pengaturan `[profiles]` bernama opsional. |
| `--profile NAME` | Gunakan profil bernama; bawaan ke `hostcensus.toml` jika `--config` dihilangkan. |
| `--exclude IP/CIDR` | Tambahkan pengecualian; ulangi sesuai kebutuhan. Host IPv4 yang dikecualikan juga mengecualikan alamat IPv6 yang mengarah ke sana: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`), dan 6to4. Target dan pengecualian IPv4-mapped diperlakukan sebagai alamat IPv4 yang dirujuknya. |
| `--max-hosts N` | Batas alamat yang diperiksa sebelum pengecualian (bawaan/maksimum keras 65.536). |
| `--history PATH` | Catat pemindaian yang selesai ke dalam basis data riwayat SQLite opsional (opt-in). |
| `--services NAMES` | Daftar nama layanan dipisahkan koma untuk diperiksa, sesuai urutan tersebut (bawaan: semua). |
| `--ports SPEC` | Daftar dipisahkan koma berupa `NAME=PORT` (pindahkan layanan) atau `PORT` (tambahkan pemeriksaan TCP biasa bernama `tcp-PORT`). |
| `--snmp-community-file PATH` | File berisi community SNMPv2c untuk kueri MIB sistem. Env: `HOSTCENSUS_SNMP_COMMUNITY` (nilainya) atau `HOSTCENSUS_SNMP_COMMUNITY_FILE` (path-nya). |
| `--snmp-user` | Pengguna SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (bawaan), `SHA224`, `SHA256`, `SHA384`, `SHA512` dan file berisi frasa sandi (passphrase). Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` atau `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (bawaan), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` dan file berisi frasa sandi. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` atau `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Tulis juga snapshot berversi untuk `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifikasi sertifikat HTTPS terhadap bundel PEM ini alih-alih penyimpanan sistem. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Secara bawaan setiap host diperiksa untuk SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80), dan HTTPS (TCP 443). Port TCP diuji dengan koneksi penuh. SNMP diuji dengan permintaan penemuan mesin (engine-discovery) SNMPv3, yang wajib dijawab oleh agen SNMPv3 mana pun tanpa kredensial; agen yang hanya mendukung v1/v2c tidak akan terdeteksi oleh probe ini. Dengan backend asyncio, sebuah host dianggap hidup apabila ada probe yang mendapat jawaban, termasuk penolakan koneksi, sehingga host yang menjatuhkan (drop) setiap probe memiliki `alive=false` dan error "Host is down"; ini tidak membuktikan bahwa host tersebut mati secara fisik. Dengan `--backend nmap`, nmap menentukan host mana yang hidup (ICMP sebagai root, atau TCP 80/443 jika bukan root).

### Sidik jari layanan

Setiap layanan yang terbuka diidentifikasi sidik jarinya dari apa yang dikirimkannya sebelum login apa pun. Tidak ada yang melakukan autentikasi kecuali kueri SNMP, dan itu pun hanya jika Anda memberikan kredensial.

| Probe | Membaca | `version` | Kunci `details` |
| --- | --- | --- | --- |
| `ssh` | baris identifikasi RFC 4253 | perangkat lunak, mis. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | jabat tangan awal MySQL/MariaDB | versi server | `server_version`, `flavor`, `auth_plugin`, atau `error_code`/`error` |
| `http` | respons `HEAD /` | header `Server` | `status`, `server` |
| `https` | jabat tangan TLS, sertifikat, `HEAD /` | header `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | penemuan SNMPv3; dengan kredensial, GET dari sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; dengan kredensial `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, atau `snmp_error` |

Target nama host diresolusi satu kali per host dan setiap probe terhubung ke alamat tersebut, yang dicatat sebagai `address` di hasil; nama tersebut hanya digunakan untuk SNI TLS, verifikasi sertifikat, dan header `Host` HTTP. Nama yang tidak dapat diresolusi menghasilkan status `unknown` dan error `Cannot resolve`. Nama DNS balik (reverse DNS) hanya disimpan jika berisi karakter nama host yang valid, dan maksimal 16 pencarian berjalan bersamaan. HTTPS menggunakan verifikasi sertifikat dan nama host terhadap penyimpanan sistem atau `--tls-ca-file`. Penyimpanan kepercayaan (trust store) dimuat satu kali untuk seluruh pemindaian dan digunakan ulang untuk setiap probe HTTPS. Koneksi TCP dan jabat tangan TLS dihitung waktunya secara terpisah, sehingga port yang menerima koneksi tetapi macet saat jabat tangan berstatus `open` dengan `tls_error`, bukan `filtered`. Jika verifikasi gagal, hasilnya mencatat `cert_verified: false` dan `cert_verify_error`; probe tidak mencoba ulang dengan pengaturan yang lebih lemah atau mengirim permintaan HTTP. Detail sertifikat dan header HTTP hanya dikumpulkan setelah verifikasi berhasil. Berikan bundel CA yang tepat untuk layanan dengan CA privat. Laporan versi lama mungkin berisi `cert_read_unverified`, yang tidak lagi dihasilkan oleh probe saat ini.

Rahasia SNMP hanya dibaca dari variabel lingkungan atau dari file (`--snmp-*-file`, atau variabel `HOSTCENSUS_SNMP_*_FILE` yang sesuai), tidak pernah dari nilai baris perintah, yang dapat dilihat oleh pengguna lokal lain di daftar proses. `--snmp-community`, `--snmp-auth-key`, dan `--snmp-priv-key` yang disertai nilai akan keluar dengan kode 2 dan menyebutkan penggantinya. File rahasia harus berupa UTF-8 tidak kosong berukuran maksimal 4096 byte; satu baris baru di akhir diabaikan, dan mengatur variabel sekaligus file untuk rahasia yang sama merupakan suatu error. Pesan error menyebutkan nama filenya tetapi tidak pernah mencetak isinya. Laporan pemindaian dan riwayat tidak secara sengaja menyertakan nilai kredensial. Pengekspor memiliki opsi `--include-credentials` terpisah dan eksplisit yang dijelaskan di bawah. Community memilih SNMPv2c; user memilih SNMPv3, dengan autentikasi bila kunci auth diberikan dan privasi bila kedua kunci diberikan (`snmp_security_level` mencatat tingkat yang digunakan). hostcensus menolak, dengan kode keluar 2, penggabungan community dengan user v3, penggunaan kunci privasi tanpa kunci auth, atau penggunaan kunci tanpa user, serta tidak pernah mencoba ulang kueri v3 yang gagal dengan v2c atau tingkat keamanan yang lebih rendah. Agen yang hanya mendukung v1/v2c mengabaikan penemuan v3 tanpa kredensial, sehingga hanya tampil sebagai terbuka apabila community diberikan.

Teks banner disederhanakan menjadi karakter yang dapat dicetak dan dibatasi maksimal 256 karakter sebelum disimpan atau ditampilkan. Pembacaan juga dibatasi: 4 KiB per baris, 4 KiB untuk salam pembuka MySQL, dan 16 KiB untuk header HTTP. ID mesin SNMP yang lebih panjang dari 32 oktet dipotong sebelum disimpan. HTTP dan HTTPS mengirim header Host dengan alamat IPv6 di dalam tanda kurung siku serta menyertakan port apabila bukan 80 atau 443. Sel CSV yang diawali dengan pemicu rumus spreadsheet diberi prefiks agar sel tersebut tetap berupa teks.

### Batasan

Satu kali proses menerima maksimal 65.536 alamat, 64 layanan, dan 524.288 probe (host dikalikan layanan); permintaan yang lebih besar akan keluar dengan kode 2 sebelum lalu lintas apa pun dikirim. `--concurrency` dibatasi hingga 4096 soket. Setiap probe memiliki batas waktu keras sebesar empat kali anggarannya sendiri. Probe koneksi (`tcp`, `ssh`, `mysql`, `http`) menggunakan 0.3 detik kecuali layanan tersebut menetapkan `timeout`. SNMP dan HTTPS menggunakan `--timeout` (bawaan 1.0) jika tidak menetapkan nilai sendiri. Probe yang mencapai batas waktu dilaporkan sebagai `unknown` dengan "probe timed out" di `errors`. Kegagalan soket lokal (misalnya kehabisan deskriptor file) juga berstatus `unknown` dengan error yang tercatat; hal ini tidak pernah dihitung sebagai port terfilter atau host mati. Sebelum melakukan probe, hostcensus menaikkan batas lunak (soft limit) file terbuka mendekati batas keras (hard limit) agar cukup untuk `--concurrency` ditambah 64 deskriptor; apabila tidak memungkinkan, pemeriksaan preflight `open files` gagal dan `scan` keluar dengan kode 1 sebelum mengirim lalu lintas. Penemuan Nmap menggunakan batas waktu host 30 detik. Prefiks diteruskan ke nmap dalam bentuk CIDR, dan sweep gagal dengan kode keluar 1 apabila nmap melaporkan lebih sedikit alamat daripada yang diberikan (misalnya nama yang tidak dapat diresolusi) alih-alih menandai host sebagai mati. Target nama host diresolusi satu kali dan nmap diberikan alamat tersebut, sehingga penemuan dan probe menjangkau mesin yang sama. Prefiks penuh dijalankan dalam satu proses nmap dengan batas waktu subproses 35 detik untuk setiap 256 alamat, dibulatkan ke atas. Sweep dengan pengecualian menggunakan batch berisi 256 host dan batas waktu 35 detik untuk setiap batch. Pembuatan worker dibatasi secara independen dari ukuran rentang. DNS balik dan resolusi nama host memiliki batas waktu terpisah selama dua detik; panggilan resolver yang tidak pernah kembali ditinggalkan di thread-nya sendiri, sehingga tidak dapat membuat hostcensus terus berjalan melewati batas ini. Maksimal 16 pencarian berjalan bersamaan, dan panggilan yang ditinggalkan tetap mempertahankan slotnya hingga selesai, sehingga jumlah thread yang macet tetap terbatas; jika ke-16 slot macet semua, pencarian berikutnya mengantre menunggu slot di luar batas waktu dua detik (yang mulai dihitung setelah slot bebas) hingga `--deadline` menghentikan pemindaian. `NetworkScanner` yang digunakan sebagai pustaka tanpa `deadline` dapat menunggu slot semacam itu tanpa batas waktu. `--deadline` (bawaan satu jam) membatasi keseluruhan proses di atas semua batasan ini.

### Mengonfigurasi layanan

Layanan dapat diubah menggunakan file TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` adalah salah satu dari `tcp`, `ssh`, `mysql`, `http`, `https`, atau `snmp` dan bawaannya adalah nama layanan jika nama tersebut merupakan probe, atau `tcp` jika bukan. Hanya `snmp` yang menggunakan UDP. Nama layanan berupa huruf kecil, angka, `-`, dan `_`. Dua layanan tidak boleh berbagi port dan protokol yang sama; riwayat mencatat satu status untuk pasangan tersebut. `timeout` bersifat opsional, dalam detik, dan minimal 0.05. Probe bergaya koneksi (`tcp`, `ssh`, `mysql`, `http`) bawaannya 0.3 detik. `snmp` dan `https` menggunakan `--timeout` pemindaian jika layanan tidak menetapkan `timeout`. `--timeout` tidak menggantikan anggaran waktu yang sudah ditetapkan oleh layanan.

Laporan JSON adalah dokumen berversi (`"format": "hostcensus-report"`, `"version": 1`) yang mencatat target, layanan yang di-probe, dan pengaturan di samping `devices`; `--format json` tanpa `-o` menulis laporan ke stdout alih-alih tabel. Setiap output JSON memiliki skema yang dipublikasikan; lihat [Output JSON](../../../docs/json-output.md). Perangkat tetap mempertahankan field asli `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname`, dan `errors` serta menambahkan daftar `services` berisi `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, atau `unknown` ketika probe gagal secara lokal atau mencapai batas waktunya), `version`, dan `details` untuk setiap probe. Output CSV mendapatkan kolom tambahan di akhir berupa `services` dan `versions` untuk layanan yang terbuka. Nilai boolean `ssh`, `snmp`, dan `mysql` mengikuti layanan dengan nama yang persis sama.


## Profil inventaris, preflight, dan riwayat lokal

Profil bernama berbagi file TOML yang sama dengan definisi `[services]` yang sudah ada. Salin
[hostcensus.example.toml](../../../hostcensus.example.toml) ke `hostcensus.toml` dan tetapkan jaringan
yang Anda kelola:

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

`preflight` menyelesaikan opsi dan profil persis seperti `scan`, termasuk
`--concurrency` untuk pemeriksaan file terbuka, sehingga preflight yang lulus berarti `scan` akan
memulai dengan rencana yang sama.

Profil menerima `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, dan `max_hosts`. `services` dan `ports` menggunakan sintaks daftar dipisahkan koma
yang sudah ada. Opsi CLI eksplisit menimpa pengaturan profil; opsi `--exclude` yang diulang
menambahkan ke pengecualian profil. Jaringan eksplisit bersama `--profile` harus
tercakup dalam ruang lingkup IP/CIDR profil tersebut. Nama host tetap didukung untuk pemindaian
langsung, tetapi tidak dapat digabungkan dengan pengecualian IP. Batas host berlaku sebelum
pengecualian; batas total probe tetap berlaku sesudahnya. Host yang dikecualikan
diabaikan dari pemeriksaan layanan maupun penemuan Nmap opsional.

Setiap pemindaian melakukan pemeriksaan preflight lokal sebelum lalu lintas ke target dikirim: batas
target/probe, akses tujuan, ketersediaan executable/wrapper Nmap opsional, skema
riwayat, dan bundel CA TLS yang dikonfigurasi. `preflight` melaporkan JSON dan tidak memindai
target atau membuat basis data riwayat. Perintah ini menulis file seinduk (sibling file) secara sementara untuk menguji
akses tujuan tanpa mengubah isi yang ada. Backend asyncio bawaan
tetap tidak memerlukan Nmap maupun root. Path tujuan harus berbeda satu sama
lain dan berbeda dari konfigurasi input, termasuk hard link; symlink tujuan
ditolak. Pemeriksaan yang gagal mengembalikan 1; cakupan/konfigurasi tidak valid mengembalikan 2.

Penulisan laporan dan ekspor memerlukan dukungan `O_NOFOLLOW`. Pada platform tanpanya,
termasuk Windows, penulisan ini gagal tanpa membuka atau memotong (truncate) tujuan.
Laporan dan skrip ekspor baru bersifat hanya-pemilik (mode 0600); mengganti file yang ada mempertahankan
izinnya. Menulis ke named pipe tanpa pembaca langsung gagal alih-alih menunggu. Basis data `--history` baru juga dibuat hanya-pemilik; basis data yang sudah ada mempertahankan modenya. Pesan log selalu masuk ke stderr, sehingga stdout hanya membawa hasil. Ekspor yang berisi kredensial selalu memaksa mode 0600.

Riwayat bersifat opt-in dan melengkapi snapshot JSON serta perintah `diff` yang sudah ada:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Gunakan ID dari `history`; contoh di atas mengasumsikan basis data baru. Snapshot disimpan
secara transaksional bersama waktu mulai/selesai UTC, versi paket, pengaturan efektif non-rahasia,
ringkasan, dan seluruh pengamatan host/layanan, termasuk error per host.
Pengamatan host yang tidak lengkap tetap dipertahankan. Proses yang dibatalkan tidak disimpan. Kontrak
laporan, snapshot, ekspor, dan kode keluar pemindaian yang ada tetap dipertahankan.

`history` menampilkan ringkasan JSON tanpa membaca seluruh payload perangkat historis.
`compare` membaca dua pemindaian tersimpan, mensyaratkan identitas target dan port terpilih yang identik,
serta melaporkan perubahan responsivitas, status, dan status port. ID pemindaian yang lebih awal
harus mendahului ID yang lebih baru. Ketika kedua pemindaian mencatat `timeout` atau `backend`
dan nilainya berbeda, laporan mencantumkan peringatan dan tetap membandingkan
pengamatan tersebut. Waktu tunggu yang berbeda dapat membuat port yang terfilter tampak terbuka. Error pemindai
dan pengamatan port `unknown` ditandai sebagai belum pasti alih-alih diperlakukan sebagai
hilangnya atau tertutupnya layanan yang terkonfirmasi: host yang mengalami error muncul di `uncertain_hosts`, dan
setiap transisi port yang melibatkan `unknown` (termasuk `unknown` di kedua pemindaian) tercantum
di `unconfirmed_ports` alih-alih `port_changes`, kecuali port yang berstatus terbuka pada
pemindaian berikutnya, yang dicatat sebagai perubahan port. `compare` dan `diff` mengklasifikasikan port dengan aturan yang sama.
`no_longer_responding` berarti tidak adanya respons, bukan bukti bahwa perangkat telah dilepas.
Kode keluar pemindaian 0 tidak menjamin setiap host merespons: periksa error per host. Perbandingan yang berhasil mengembalikan 0 terlepas dari ada tidaknya perubahan; `diff` file yang sudah ada
mempertahankan kontrak kode keluar 3 miliknya. Riwayat yang tidak didukung atau rusak mengembalikan 1.

Riwayat menyimpan informasi inventaris, jadi pilih direktori lokal yang terlindungi dengan tepat.
File profil dan pengaturan tersimpan tidak memuat kredensial SNMP;
penanganan kredensial tetap berjalan melalui opsi runtime/variabel lingkungan yang sudah ada.

## Perbandingan inventaris (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Snapshot adalah JSON dengan `format: "hostcensus-snapshot"`, `version: 1`, versi hostcensus, waktu pembuatan UTC, target, `timeout` dan `backend` pemindaian jika dicatat oleh pemindaian, layanan yang di-probe, serta host yang hidup dalam format yang sama dengan laporan `-o`. Host yang mati tidak disertakan. `diff` juga menerima laporan JSON `scan -o` biasa, termasuk yang berasal dari versi sebelum field `services` ada.

`diff` melaporkan host yang baru muncul dan yang menghilang, port yang terbuka atau tertutup pada host yang ada di keduanya, serta layanan yang `version`-nya berubah. Port yang hanya di-probe di salah satu dari dua pemindaian tidak dibandingkan, dan peringatan akan menjelaskannya. Pengamatan yang gagal tidak pernah dibaca sebagai "tidak ada perubahan": port yang berstatus `unknown` di salah satu pemindaian dan tidak terbuka di pemindaian berikutnya dicantumkan di bawah `unconfirmed`, bukan `closed`, dengan `before` berupa `open`, `unknown`, atau `not-open` (di-probe dan tertutup atau terfilter) serta `after` berupa `unknown` atau `not-open`; port yang sekarang terbuka dilaporkan di bawah `opened` meskipun probe sebelumnya gagal. Host yang seluruh probe-nya gagal tanpa jawaban di salah satu pemindaian dicantumkan di bawah `unsettled_hosts` (dengan `before`/`after` berupa `up`, `uncertain`, atau `absent`, termasuk ketika gagal di kedua pemindaian atau tidak ada di file lainnya) alih-alih `vanished_hosts`; jika host tersebut menjawab di pemindaian berikutnya, ia juga dilaporkan sebagai host baru beserta port terbukanya. Snapshot menyimpan host yang gagal tersebut karena alasan ini. Peringatan juga muncul apabila targetnya berbeda, dan apabila kedua file mencatat timeout atau backend yang nilainya berbeda. `-o PATH` juga menulis bentuk JSON ke dalam file.

Laporan dari pemindaian yang dihentikan oleh `--deadline` (`"complete": false`) hanya mencantumkan host yang sempat dijangkaunya, sehingga `diff` dan `export` menolaknya dengan kode keluar 2. `--allow-partial` menerimanya dengan peringatan di stderr: `diff` kemudian mencantumkan host yang sama sekali tidak tercantum dalam pemindaian tidak lengkap di bawah `unsettled_hosts` sebagai `unscanned` alih-alih menghilang (host yang dicantumkan sebagai mati tetap dianggap menghilang), mengatur `partial` ke true dan tidak pernah melaporkan tidak ada perubahan, sedangkan `export` menulis peringatan ke dalam header skrip.

Kode keluar `diff`: `0` tidak ada perubahan, `3` perubahan ditemukan, pengamatan yang tidak dapat dikonfirmasi, atau input tidak lengkap (`changed` bernilai true kapan pun ada daftar, termasuk `unsettled_hosts` dan `unconfirmed`, yang tidak kosong, atau `partial` bernilai true), `2` file tidak ada, tidak dapat dibaca, bukan snapshot yang didukung, atau tidak lengkap tanpa `--allow-partial`, `1` file `-o` tidak dapat ditulis.

## Ekspor Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (fork dari Cacti 1.2.31) tidak memiliki fitur impor file perangkat massal. Cara yang didukung untuk menambahkan perangkat melalui skrip adalah `cli/add_device.php`, satu perangkat per pemanggilan, dengan argumen `--option=value`. `hostcensus export` menulis skrip POSIX `sh` berisi pemanggilan tersebut:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Setiap host yang hidup menjadi `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Host yang kueri SNMP pemindaiannya berhasil mendapatkan `--version=2 --community=...` atau `--version=3 --username=... --authproto=... --password=...` (ditambah `--privproto`/`--privpass` untuk authPriv), `--port`, dan `--avail=snmp`. Ekspor SNMPv3 membutuhkan `--snmp-user`, dan noAuthNoPriv ditolak karena `add_device.php` mewajibkan kata sandi v3.
- Host lainnya mendapatkan `--version=0 --avail=ping`, dengan `--ping_method=tcp --ping_port=` berupa port TCP terbuka pertama, atau ICMP jika tidak ada.
- `--notes` mencantumkan layanan terbuka dan versinya. `--description` adalah nama reverse-DNS jika berupa karakter biasa (huruf, angka, `.`, `_`, `-`), jika tidak maka menggunakan IP, dan dibuat unik karena `add_device.php` memperlakukan deskripsi yang sudah ada sebagai pembaruan terhadap perangkat tersebut.

Setiap nilai divalidasi dan di-quote untuk shell dengan `shlex.quote`. Secara bawaan tidak ada rahasia SNMP yang ditulis: skrip melakukan ekspansi `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY`, atau `HOSTCENSUS_SNMP_PRIV_KEY` saat dijalankan dan berhenti jika ada yang tidak diatur. `--include-credentials` justru menulis nilai dari variabel lingkungan tersebut ke dalam skrip, membuatnya dengan mode 0600, dan mencatat peringatan. `add_device.php` sendiri mencetak community dan menerima rahasia sebagai argumen, yang terlihat di daftar proses server Kadupul selama setiap pemanggilan berjalan.

`add_device.php` keluar dengan kode 1 untuk duplikat dan error; skrip tetap melanjutkan, menghitung kegagalan, dan keluar dengan kode 1 jika ada perangkat yang tidak berhasil ditambahkan. ID templat diperoleh dari `php cli/add_device.php --list-host-templates`. Kode keluar `export`: `0` ditulis, `2` input tidak dapat dibaca, pemindaian tidak lengkap tanpa `--allow-partial`, atau data tidak dapat diekspor dengan aman, `1` skrip tidak dapat ditulis.

## Pembuatan versi dan proses rilis

hostcensus mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html): perbaikan
yang kompatibel menaikkan versi patch, fitur/penghentian (deprecation) yang kompatibel menaikkan
versi minor, dan perubahan yang memutus kompatibilitas menaikkan versi mayor.
Perintah dan opsi, kode keluar, serta skema JSON merupakan kontrak publik;
perilaku yang dihentikan tetap berfungsi hingga rilis mayor berikutnya, kecuali
perbaikan keamanan mengharuskan perubahannya lebih cepat (changelog akan menjelaskan alasannya).

release-please membuka PR rilis dari judul Conventional Commit di `main`,
menaikkan versi di `pyproject.toml`, `uv.lock`, dan `CHANGES.md`. Penggabungannya (merge) membuat
tag `vMAJOR.MINOR.PATCH` dan draf rilis GitHub, yang kemudian dilampiri CI dengan wheel teruji,
distribusi sumber, dan checksum; GitHub menyimpan atestasi build untuk
file-file tersebut melalui API atestasinya. Pengelola meninjau dan memublikasikan
draf setelah file terlampir. Rilis tidak pernah ditimpa ulang.

Publikasi tepercaya PyPI bersifat opt-in dan memerlukan kepemilikan proyek, penerbit
tepercaya (trusted publisher), dan lingkungan `pypi`. Proses ini memublikasikan artefak rilis teruji yang sama
tanpa membangun ulang atau menyimpan token API. Rilis bertag di repositori publik
ini menghasilkan atestasi artefak GitHub; fork privat memerlukan paket yang
didukung dan opt-in eksplisit. Lihat
[panduan rilis lengkap](../../../docs/releasing.md) untuk penyiapan, perintah persis, dan percobaan ulang.

## Pengembangan

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Alat pengembangan berada dalam grup dependensi [PEP 735](https://peps.python.org/pep-0735/)
di `pyproject.toml` (`dev`, `fuzz`, `build`), sehingga tidak pernah muncul di metadata
paket yang dipublikasikan. `uv.lock` adalah satu-satunya lockfile; CI menginstal dengan
`uv sync --locked` dan gagal jika lockfile usang. Pilih interpreter dengan
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), atau Python 3.12+ apa pun.

CI memberlakukan batas minimum cakupan (coverage) paket sebesar 90%. Pengujian unit mencakup server loopback
terkendali serta kasus profil/riwayat/validator-rilis luring; lab Compose menjalankan
OpenSSH, MariaDB, nginx, dan net-snmp pada bridge terisolasi. Jalankan dengan
`make test-integration`. Lihat [CONTRIBUTING.md](../../../CONTRIBUTING.md) dan
[alat rilis](../../../scripts/README.md).

Kontainer runtime berjalan sebagai UID/GID 10001 tanpa direktori home, tanpa login
shell, dan tanpa pip, serta dapat menulis ke `/app/output`. Berikan akses tulis kepada pengguna tersebut ke
direktori output mana pun yang di-mount. Kontainer ini tidak memerlukan kapabilitas khusus dan berfungsi dengan
sistem file root hanya-baca, sehingga dapat dijalankan sebagai:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap menggunakan perilaku penemuan TCP tanpa hak istimewa di kontainer ini. CI menggagalkan
pembuatan image pada setiap kerentanan HIGH atau CRITICAL yang dapat diperbaiki yang dilaporkan oleh Trivy.

## Pemeriksaan rantai pasok

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
berjalan di main dan secara mingguan, memublikasikan skor aktualnya, dan mengunggah temuan ke pemindaian kode
GitHub. Action dan image dasar kontainer disematkan dengan hash yang tidak dapat diubah; dependensi Python
diselesaikan di `uv.lock`. Kegagalan Bandit menggagalkan CI, dan fuzzing Atheris terbatas
menguji parser SSH, MySQL, HTTP, sertifikat, dan SNMPv3 BER
tanpa akses jaringan.

Scorecard juga mengukur aktivitas peninjauan historis, keragaman kontributor, dan
provenance rilis. Skor tersebut mencerminkan bukti aktual; skor itu bukan klaim
bahwa setiap pemeriksaan tata kelola atau rilis historis telah terpenuhi. Lihat
[SECURITY.md](../../../SECURITY.md) dan [provenance rilis](../../../docs/releasing.md).

## Lokalisasi

Pesan CLI dan tabel ringkasan/diff terminal mendukung 45 lokal (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) tanpa dependensi runtime tambahan. Resolusi memprioritaskan `--lang`, lalu `LC_ALL`, `LC_MESSAGES`, dan `LANG`, dengan fallback ke `en`. Skema JSON, kolom CSV, dan skrip ekspor tetap tidak berubah di semua lokal.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Berkontribusi

Kontribusi harus menyertakan kasus yang dapat direproduksi, mempertahankan kontrak CLI dan
format data yang terdokumentasi, serta lulus pemeriksaan kualitas di atas. Lihat
[CONTRIBUTING.md](../../../CONTRIBUTING.md) untuk alur kerja pengembangan dan
[panduan rilis](../../../docs/releasing.md) untuk keputusan kompatibilitas dan pembuatan versi.

## Status keamanan dan lisensi

Lihat [SECURITY.md](../../../SECURITY.md) untuk pelaporan privat dan versi yang didukung.
hostcensus dilisensikan di bawah [Lisensi MIT](../../../LICENSE).

Header sumber menggunakan pengidentifikasi SPDX dan mempertahankan kredit kontributor dari riwayat
Git. Lihat [AUTHORS.md](../../../AUTHORS.md) untuk atribusi. Tangkapan uji biner dan
lockfile yang dihasilkan menggunakan file `.license` yang berdekatan; teks MIT berada di `LICENSES/MIT.txt`.
