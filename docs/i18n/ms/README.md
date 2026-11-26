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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · **Bahasa Melayu** · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus ialah CLI Python untuk inventori perkhidmatan yang boleh diulang pada rangkaian yang anda tadbir. Ia merekodkan apa yang didedahkan oleh peranti, membandingkan pemerhatian dari semasa ke semasa, dan menjana skrip import Kadupul. Backend lalai menggunakan soket asyncio tanpa root; penemuan Nmap pilihan boleh mengenal pasti hos di luar port perkhidmatan yang dikonfigurasikan.

## Mengapa hostcensus

Laporan port sekali sahaja tidak menjelaskan sama ada pemerhatian seterusnya telah berubah atau sekadar gagal. hostcensus menggabungkan keadaan perkhidmatan yang eksplisit, kuar terhad, profil imbasan yang boleh diguna semula, dan sejarah setempat. Pengendali boleh mengulang skop yang sama, memeriksa ralat, dan membezakan pemerhatian yang tidak pasti daripada perubahan yang disahkan.

- **Bukti perkhidmatan:** Pengenalpastian SSH, sapaan MySQL, pengepala HTTP, pemerhatian sijil TLS, serta penemuan SNMP atau pertanyaan system-MIB berkredensial.
- **Skop boleh diulang:** profil TOML bernama, pengecualian tambahan, perkhidmatan boleh dikonfigurasi, had hos/kuar, dan pekerja terhad.
- **Semakan sebelum trafik:** prapenerbangan setempat mengesahkan sasaran, alatan, akses destinasi, skema sejarah, dan himpunan CA TLS yang dikonfigurasikan.
- **Sejarah inventori:** petikan SQLite bertransaksi mengekalkan semua pemerhatian; perbandingan memastikan kegagalan pengimbas dan keadaan tidak diketahui kekal kelihatan.
- **Output saling kendali:** laporan terminal, JSON dan CSV, petikan fail berversi, dan skrip import Kadupul.

CI merangkumi Python 3.12, 3.13 dan 3.14 pada Linux dan macOS, serta makmal integrasi Compose yang terkawal. Kod ini menggunakan alias jenis moden, keputusan prapenerbangan berjenis, profil berslot kata kunci sahaja dan pembersihan async berstruktur sambil mengekalkan versi masa jalan tersebut. Lihat [Pemversian dan keluaran](../../../docs/releasing.md) untuk kontrak keserasian SemVer dan proses keluaran GitHub. Lencana keluaran menerangkan artifak yang diterbitkan, bukan salinan checkout: tag terkini yang diterbitkan pada masa ini ialah `v0.3.0`, manakala checkout ini menggunakan versi pakej `3.0.0`. Pasang daripada checkout untuk menggunakan ciri inventori yang didokumenkan di sini.

Mulakan dengan [pemasangan](#install), kemudian [profil dan sejarah](#inventory-profiles-preflight-and-local-history). Untuk butiran integrasi, lihat [cap jari perkhidmatan](#fingerprints), [perbandingan fail](#inventory-diff), dan [eksport Kadupul](#kadupul-export).

## Pemasangan

Python 3.12 atau lebih baharu diperlukan; Python 3.12–3.14 ialah matriks yang diuji. Dari checkout ini, pasang kebergantungan masa jalan yang dikunci:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Untuk penemuan hos Nmap pilihan, pasang fail boleh laku Nmap menggunakan pengurus pakej platform anda; tiada pakej Python tambahan diperlukan. Output XML Nmap dihuraikan dengan defusedxml, satu kebergantungan teras, supaya pengembangan entiti ditolak. hostcensus menjalankan `nmap` yang ditemui pada `PATH` secara terus dengan senarai argumen tetap, had masa yang meningkat mengikut saiz awalan, dan had output 64 MiB. Nmap tidak diperlukan untuk backend lalai.

## Berhijrah daripada netprobe

hostcensus ialah nama baharu bagi netprobe, yang dikeluarkan dalam versi 3.0.0. Projek ini tidak pernah diterbitkan ke PyPI di bawah mana-mana nama tersebut, jadi pemasangan datang daripada checkout atau keluaran GitHub. Repositori GitHub mengekalkan namanya.

| Dahulu | Kini | Keserasian |
| --- | --- | --- |
| Pengedaran `netprobe` | `hostcensus` | Pasang semula daripada checkout; tiada pakej nama lama. |
| Perintah `netprobe` | `hostcensus` | `netprobe` masih berjalan dan mencetak satu baris pengusangan pada stderr. Kod keluar dan stdout tidak berubah. Dibuang dalam keluaran utama seterusnya. |
| Pemboleh ubah persekitaran `NETPROBE_*` | `HOSTCENSUS_*` | Pemboleh ubah `NETPROBE_*` digunakan apabila pasangannya `HOSTCENSUS_*` tidak ditetapkan, dengan satu amaran stderr yang menamakan pemboleh ubah tersebut dan tidak sesekali nilainya. `HOSTCENSUS_*` diutamakan apabila kedua-duanya ditetapkan. Dibuang dalam keluaran utama seterusnya. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Memecahkan keserasian.** Tiada shim import dipasang; kemas kini import. |
| Tag imej Docker `network-discovery:test` (CI sahaja) dan pengguna kontena `netprobe` | `hostcensus:test`, pengguna `hostcensus` | Tiada imej registri pernah diterbitkan. Bina imej semula dan gunakan titik masuk `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Fail sedia ada dengan nama lalai lama masih digunakan, dengan amaran, selagi nama baharu tidak wujud. Laluan `--config` dan `--history` yang eksplisit tidak disentuh. |
| Laporan dan petikan dengan `"format": "netprobe-report"` atau `"netprobe-snapshot"`, serta medan `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` dan `export` masih memuatkan fail yang ditulis di bawah nama lama, dan Skema JSON yang diterbitkan menerima kedua-dua ejaan. Fail baharu menggunakan nama baharu. Pangkalan data sejarah SQLite tidak berubah dan dimuatkan seperti sebelum ini. |
| Skrip Kadupul daripada `netprobe export` | Skrip daripada `hostcensus export` | Skrip lama terus berfungsi dan masih membaca `NETPROBE_SNMP_*` apabila dijalankan. Skrip baharu membaca `HOSTCENSUS_SNMP_*`. |

## Contoh pantas

Dijalankan daripada kontena penguji makmal integrasi yang diterangkan di bawah Pembangunan; output dipangkas:

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

## Kod keluar

| Perintah | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | pemerhatian/laporan direkodkan | prapenerbangan/backend, sejarah, atau penulisan laporan/petikan gagal | sasaran, pilihan, konfigurasi, atau had tidak sah | - | `--deadline` dicapai; laporan separa ditulis, sejarah dan petikan dilangkau |
| `preflight` | semakan lulus | semakan setempat gagal | sasaran/konfigurasi tidak sah atau destinasi bercanggah | - | - |
| `profiles` | profil yang disahkan disenaraikan | - | konfigurasi atau pilihan tidak boleh dibaca/tidak sah | - | - |
| `history` | ringkasan disenaraikan | sejarah tiada, tidak sah, atau tidak disokong | pilihan CLI tidak sah | - | - |
| `compare` | perbandingan dihasilkan, termasuk apabila perubahan wujud | sejarah tidak boleh dibaca, skop/susunan tidak serasi, atau kegagalan penulisan | pilihan CLI tidak sah | - | - |
| `diff` | tiada perubahan | fail `-o` tidak dapat ditulis | input tiada, tidak boleh dibaca atau tidak disokong, atau imbasan tidak lengkap tanpa `--allow-partial` | perubahan ditemui, pemerhatian tidak disahkan, atau imbasan tidak lengkap | - |
| `export` | skrip ditulis | skrip tidak dapat ditulis | input tidak boleh dibaca, imbasan tidak lengkap tanpa `--allow-partial`, atau data yang tidak dapat dieksport dengan selamat | - | - |

## Susun atur

| Modul | Tanggungjawab |
| --- | --- |
| `cli.py` | Pilihan perintah, peleraian profil, prapenerbangan, pengimbasan dan pelaporan |
| `scanner.py`, `probes.py` | Pengembangan sasaran, pekerja terhad, penemuan hos dan pemerhatian perkhidmatan |
| `config.py`, `profiles.py` | Takrifan perkhidmatan dan profil inventori yang disahkan |
| `models.py`, `output.py` | Jenis keputusan dan pemaparan terminal/JSON/CSV |
| `history.py`, `diff.py` | Sejarah SQLite dan perbandingan petikan fail berversi |
| `preflight.py` | Semakan setempat dan carian versi Nmap terhad |
| `export.py` | Skrip import Kadupul yang disahkan dan dipetik dengan selamat |

Setiap pemerhatian perkhidmatan merekodkan keadaannya secara berasingan daripada identiti yang diiklankannya. Bacaan dan had masa dihadkan; pengecualian kuar kekal dalam ralat hos. Sejarah SQLite menggunakan transaksi, pembersihan sambungan eksplisit, serta laluan penyenaraian dan perbandingan baca sahaja. Rahsia SNMP hanya masuk melalui pemboleh ubah persekitaran atau fail rahsia; sejarah inventori menyimpan tetapan bukan rahsia yang berkuat kuasa. Lihat [Seni bina](../../../docs/architecture.md) untuk saluran paip imbasan, had dan sempadan kepercayaannya, dan [SECURITY.md](../../../SECURITY.md#authorized-use) untuk penggunaan yang dibenarkan.

## Penggunaan

Imbas hanya rangkaian yang anda tadbir.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Pilihan | Maksud |
| --- | --- |
| `NETWORK` | CIDR, IP, atau nama hos; pilihan dengan `--profile`. Pengecam skop IPv6 ditolak. |
| `-o, --output PATH` | Menulis laporan. Format mengikut sambungan (`.json`, `.csv`); sambungan lain berbalik kepada JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Memaksa format laporan. Tiada kesan tanpa `--output`. `.sh` memilih `kadupul`. |
| `-v, --verbose` | Pengelogan nyahpepijat. |
| `-q, --quiet` | Menyekat keputusan, kemajuan dan log maklumat; amaran dan ralat masih dipaparkan pada stderr. |
| `--backend asyncio\|nmap` | Penemuan hos. `asyncio` (lalai) menguar port perkhidmatan secara terus; `nmap` menjalankan sapuan ping nmap dahulu dan memerlukan fail boleh laku `nmap` pada `PATH`. |
| `--timeout SECONDS` | Menunggu kuar yang tidak menetapkan bajet sendiri (lalai 1.0). Kuar sambungan terbina dalam menggunakan 0.3s melainkan jadual perkhidmatan menetapkan `timeout`. |
| `--concurrency N` | Kuar yang sedang berjalan serentak (lalai 256). |
| `--deadline SECONDS` | Menghentikan keseluruhan imbasan, termasuk sapuan nmap, selepas tempoh ini (lalai 3600, maksimum 604800; env `HOSTCENSUS_DEADLINE`). Hos yang selesai ditulis ke laporan dengan `"complete": false`, tiada sejarah atau petikan ditulis, dan `scan` keluar dengan kod 4. |
| `--config PATH` | Takrifan perkhidmatan TOML dan tetapan `[profiles]` bernama pilihan. |
| `--profile NAME` | Menggunakan profil bernama; lalai kepada `hostcensus.toml` apabila `--config` ditinggalkan. |
| `--exclude IP/CIDR` | Menambah pengecualian; ulang mengikut keperluan. Hos IPv4 yang dikecualikan turut mengecualikan alamat IPv6 yang mencapainya: terpetakan IPv4 (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) dan 6to4. Sasaran dan pengecualian terpetakan IPv4 dianggap sebagai alamat IPv4 yang diwakilinya. |
| `--max-hosts N` | Had alamat yang disemak sebelum pengecualian (lalai/maksimum mutlak 65,536). |
| `--history PATH` | Merekodkan imbasan yang selesai dalam pangkalan data sejarah SQLite ikut serta. |
| `--services NAMES` | Senarai nama perkhidmatan dipisahkan koma untuk disemak, mengikut susunan tersebut (lalai: semua). |
| `--ports SPEC` | Senarai `NAME=PORT` (memindahkan perkhidmatan) atau `PORT` (menambah semakan TCP biasa bernama `tcp-PORT`) dipisahkan koma. |
| `--snmp-community-file PATH` | Fail yang menyimpan komuniti SNMPv2c untuk pertanyaan MIB sistem. Env: `HOSTCENSUS_SNMP_COMMUNITY` (nilainya) atau `HOSTCENSUS_SNMP_COMMUNITY_FILE` (laluannya). |
| `--snmp-user` | Pengguna SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (lalai), `SHA224`, `SHA256`, `SHA384`, `SHA512` dan fail yang menyimpan frasa laluan. Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` atau `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (lalai), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` dan fail yang menyimpan frasa laluan. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` atau `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Turut menulis petikan berversi untuk `hostcensus diff`. |
| `--tls-ca-file PATH` | Mengesahkan sijil HTTPS terhadap himpunan PEM ini dan bukannya stor sistem. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Secara lalai setiap hos disemak untuk SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) dan HTTPS (TCP 443). Port TCP diuji dengan sambungan penuh. SNMP diuji dengan permintaan penemuan enjin SNMPv3, yang mesti dijawab oleh mana-mana ejen SNMPv3 tanpa kredensial; ejen yang hanya menggunakan v1/v2c tidak akan dikesan oleh kuar ini. Dengan backend asyncio, hos dikira sebagai hidup apabila mana-mana kuar mendapat jawapan, termasuk sambungan yang ditolak, jadi hos yang menggugurkan setiap kuar mempunyai `alive=false` dan ralat "Host is down"; ini tidak membuktikan ia dimatikan secara fizikal. Dengan `--backend nmap`, nmap menentukan hos yang hidup (ICMP sebagai root, TCP 80/443 sebaliknya).

### Cap jari

Setiap perkhidmatan terbuka dicap jari daripada apa yang dihantarnya sebelum sebarang log masuk. Tiada apa-apa yang mengesahkan kecuali pertanyaan SNMP, dan hanya apabila anda membekalkan kredensial.

| Kuar | Membaca | `version` | Kunci `details` |
| --- | --- | --- | --- |
| `ssh` | baris pengenalan RFC 4253 | perisian, cth. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | jabat tangan awal MySQL/MariaDB | versi pelayan | `server_version`, `flavor`, `auth_plugin`, atau `error_code`/`error` |
| `http` | respons `HEAD /` | pengepala `Server` | `status`, `server` |
| `https` | jabat tangan TLS, sijil, `HEAD /` | pengepala `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | penemuan SNMPv3; dengan kredensial, GET bagi sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; dengan kredensial `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, atau `snmp_error` |

Sasaran nama hos dileraikan sekali bagi setiap hos dan setiap kuar bersambung ke alamat tersebut, direkodkan sebagai `address` dalam keputusan; nama tersebut hanya digunakan untuk TLS SNI, pengesahan sijil dan pengepala `Host` HTTP. Nama yang tidak dapat dileraikan memberikan keadaan `unknown` dan ralat `Cannot resolve`. Nama DNS terbalik disimpan hanya apabila ia mengandungi aksara nama hos, dan maksimum 16 carian berjalan serentak. HTTPS menggunakan pengesahan sijil dan nama hos terhadap stor sistem atau `--tls-ca-file`. Stor kepercayaan dimuatkan sekali untuk imbasan dan diguna semula bagi setiap kuar HTTPS. Sambungan TCP dan jabat tangan TLS ditetapkan masanya secara berasingan, jadi port yang menerima sambungan tetapi menangguhkan jabat tangan adalah `open` dengan `tls_error`, bukan `filtered`. Jika pengesahan gagal, keputusan merekodkan `cert_verified: false` dan `cert_verify_error`; ia tidak mencuba semula dengan tetapan yang lebih lemah atau menghantar permintaan HTTP. Butiran sijil dan pengepala HTTP dikumpul hanya selepas pengesahan berjaya. Bekalkan himpunan CA yang betul untuk perkhidmatan CA peribadi. Laporan lama mungkin mengandungi `cert_read_unverified`, yang tidak lagi dihasilkan oleh kuar semasa.

Rahsia SNMP dibaca hanya daripada pemboleh ubah persekitaran atau daripada fail (`--snmp-*-file`, atau pemboleh ubah `HOSTCENSUS_SNMP_*_FILE` yang sepadan), tidak sesekali daripada nilai baris perintah, yang boleh dilihat oleh pengguna setempat lain dalam senarai proses. `--snmp-community`, `--snmp-auth-key` dan `--snmp-priv-key` dengan nilai akan keluar dengan kod 2 dan menamakan penggantinya. Fail rahsia mestilah UTF-8 tidak kosong berukuran maksimum 4096 bait; satu baris baharu di penghujung diabaikan, dan menetapkan kedua-dua pemboleh ubah dan fail untuk rahsia yang sama adalah satu ralat. Ralat menamakan fail tersebut tetapi tidak sesekali mencetak kandungannya. Laporan imbasan dan sejarah tidak menyertakan nilai kredensial secara sengaja. Pengeksport mempunyai pilihan `--include-credentials` yang berasingan dan eksplisit seperti yang diterangkan di bawah. Komuniti memilih SNMPv2c; pengguna memilih SNMPv3, dengan pengesahan apabila kunci auth diberikan dan privasi apabila kedua-dua kunci diberikan (`snmp_security_level` merekodkan pilihannya). hostcensus menolak, dengan kod keluar 2, untuk menggabungkan komuniti dengan pengguna v3, menggunakan kunci privasi tanpa kunci auth, atau menggunakan kunci tanpa pengguna, dan ia tidak pernah mencuba semula pertanyaan v3 yang gagal dengan v2c atau tahap keselamatan yang lebih rendah. Ejen yang hanya menggunakan v1/v2c mengabaikan penemuan v3 tanpa kredensial, jadi ia dipaparkan sebagai terbuka hanya apabila komuniti dibekalkan.

Teks sepanduk dikurangkan kepada aksara boleh cetak dan dihadkan pada 256 aksara sebelum disimpan atau dipaparkan. Bacaan juga dihadkan: 4 KiB setiap baris, 4 KiB untuk sapaan MySQL, 16 KiB pengepala HTTP. ID enjin SNMP yang lebih panjang daripada 32 oktet dipangkas sebelum disimpan. HTTP dan HTTPS menghantar pengepala Host dengan alamat IPv6 dalam kurungan siku dan bersama port apabila ia bukan 80 atau 443. Sel CSV yang bermula dengan pencetus formula hamparan diberi awalan supaya sel kekal sebagai teks.

### Had

Satu jalanan menerima maksimum 65,536 alamat, 64 perkhidmatan, dan 524,288 kuar (hos didarab dengan perkhidmatan); permintaan yang lebih besar keluar dengan kod 2 sebelum apa-apa dihantar. `--concurrency` dihadkan pada 4096 soket. Setiap kuar mempunyai had masa mutlak empat kali ganda bajetnya sendiri. Kuar sambungan (`tcp`, `ssh`, `mysql`, `http`) menggunakan 0.3 saat melainkan perkhidmatan tersebut menetapkan `timeout`. SNMP dan HTTPS menggunakan `--timeout` (lalai 1.0) apabila ia tidak menetapkannya. Kuar yang mencapai had masa dilaporkan sebagai `unknown` dengan "probe timed out" dalam `errors`. Kegagalan soket setempat (contohnya kehabisan deskriptor fail) juga menjadi `unknown` dengan ralat direkodkan; ia tidak sesekali dikira sebagai port ditapis atau hos mati. Sebelum menguar, hostcensus menaikkan had lembut fail terbuka ke arah had keras untuk memuatkan `--concurrency` ditambah 64 deskriptor; apabila tidak berjaya, semakan prapenerbangan `open files` gagal dan `scan` keluar dengan kod 1 sebelum menghantar trafik. Penemuan Nmap menggunakan had masa hos 30 saat. Awalan dihantar ke nmap dalam bentuk CIDR, dan sapuan gagal dengan kod keluar 1 apabila nmap melaporkan alamat yang lebih sedikit daripada yang diberikan kepadanya (contohnya nama yang tidak dapat dileraikannya) berbanding menandakan hos sebagai mati. Sasaran nama hos dileraikan sekali dan nmap diberikan alamat tersebut, supaya penemuan dan kuar sampai ke mesin yang sama. Awalan penuh ialah satu proses nmap yang mempunyai had masa subproses selama 35 saat bagi setiap 256 alamat, dibundarkan ke atas. Sapuan dengan pengecualian menggunakan kelompok 256 hos dan had masa 35 saat bagi setiap kelompok. Penciptaan pekerja dihadkan secara bebas daripada saiz julat. DNS terbalik dan peleraian nama hos mempunyai had masa dua saat yang berasingan; panggilan peleraian yang tidak pernah kembali ditinggalkan pada bebenangnya sendiri, jadi ia tidak dapat memastikan hostcensus terus berjalan melepasi had ini. Maksimum 16 carian berjalan serentak, dan panggilan yang ditinggalkan mengekalkan slotnya sehingga ia kembali, jadi bilangan bebenang yang tersekat kekal terhad; jika kesemua 16 terhenti, carian seterusnya beratur menunggu slot di luar had masa dua saat (yang bermula sebaik sahaja slot tersedia) sehingga `--deadline` menghentikan imbasan. `NetworkScanner` yang digunakan sebagai pustaka tanpa `deadline` boleh menunggu slot sedemikian tanpa had masa. `--deadline` (lalai satu jam) mengehadkan keseluruhan jalanan di samping had-had ini.

### Mengkonfigurasi perkhidmatan

Perkhidmatan boleh diubah dengan fail TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` ialah salah satu daripada `tcp`, `ssh`, `mysql`, `http`, `https` atau `snmp` dan lalai kepada nama perkhidmatan apabila nama itu ialah kuar, jika tidak `tcp`. Hanya `snmp` menggunakan UDP. Nama perkhidmatan ialah huruf kecil, digit, `-` dan `_`. Dua perkhidmatan tidak boleh berkongsi port dan protokol yang sama; sejarah merekodkan satu keadaan untuk pasangan tersebut. `timeout` adalah pilihan, dalam saat, dan sekurang-kurangnya 0.05. Kuar gaya sambungan (`tcp`, `ssh`, `mysql`, `http`) lalai kepada 0.3 saat. `snmp` dan `https` menggunakan `--timeout` imbasan apabila perkhidmatan tidak menetapkan `timeout`. `--timeout` tidak menggantikan bajet yang sudah dimiliki oleh perkhidmatan.

Laporan JSON ialah dokumen berversi (`"format": "hostcensus-report"`, `"version": 1`) yang merekodkan sasaran, perkhidmatan yang dikuar dan tetapan di sebelah `devices`; `--format json` tanpa `-o` menulis laporan ke stdout dan bukannya jadual. Setiap output JSON mempunyai skema yang diterbitkan; lihat [Output JSON](../../../docs/json-output.md). Peranti mengekalkan medan asal `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` dan `errors` serta menambah senarai `services` dengan `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, atau `unknown` apabila kuar gagal secara setempat atau mencapai had masanya), `version` dan `details` bagi setiap kuar. Output CSV memperoleh lajur `services` dan `versions` di hujung untuk perkhidmatan yang terbuka. Boolean `ssh`, `snmp` dan `mysql` mengikut perkhidmatan dengan nama tersebut secara tepat.

## Profil inventori, prapenerbangan, dan sejarah setempat

Profil bernama berkongsi fail TOML dengan takrifan `[services]` sedia ada. Salin [hostcensus.example.toml](../../../hostcensus.example.toml) ke `hostcensus.toml` dan tetapkan rangkaian yang anda tadbir:

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

`preflight` meleraikan pilihan dan profil tepat seperti yang dilakukan oleh `scan`, termasuk `--concurrency` untuk semakan fail terbuka, jadi prapenerbangan yang lulus bermakna `scan` akan bermula dengan pelan yang sama.

Profil menerima `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency`, dan `max_hosts`. `services` dan `ports` menggunakan sintaks senarai dipisahkan koma sedia ada. Pilihan CLI eksplisit mengatasi tetapan profil; pilihan `--exclude` yang diulang ditambah kepada pengecualian profil. Rangkaian eksplisit dengan `--profile` mestilah terkandung dalam skop IP/CIDR profil tersebut. Nama hos kekal disokong untuk imbasan terus, tetapi tidak boleh digabungkan dengan pengecualian IP. Had hos terpakai sebelum pengecualian; had kuar keseluruhan masih terpakai selepas itu. Hos yang dikecualikan ditinggalkan daripada kedua-dua semakan perkhidmatan dan penemuan Nmap pilihan.

Setiap imbasan melakukan semakan prapenerbangan setempat sebelum trafik sasaran: had sasaran/kuar, akses destinasi, ketersediaan fail boleh laku/pembalut Nmap pilihan, skema sejarah, dan himpunan CA TLS yang dikonfigurasikan. `preflight` melaporkan JSON dan tidak mengimbas sasaran atau mencipta pangkalan data sejarah. Ia menulis fail seinduk buat sementara waktu untuk menguji akses destinasi tanpa mengubah kandungan sedia ada. Backend asyncio lalai masih tidak memerlukan Nmap mahupun root. Laluan destinasi mestilah berbeza antara satu sama lain dan konfigurasi input, termasuk pautan keras; pautan simbolik destinasi ditolak. Semakan yang gagal mengembalikan 1; skop/konfigurasi tidak sah mengembalikan 2.

Penulisan laporan dan eksport memerlukan sokongan `O_NOFOLLOW`. Pada platform tanpanya, termasuk Windows, penulisan ini gagal tanpa membuka atau memangkaskan destinasi. Laporan baharu dan skrip eksport adalah untuk pemilik sahaja (mod 0600); menggantikan fail sedia ada mengekalkan kebenarannya. Menulis ke paip bernama tanpa pembaca gagal serta-merta dan bukannya menunggu. Pangkalan data `--history` baharu juga dicipta untuk pemilik sahaja; yang sedia ada mengekalkan modnya. Mesej log sentiasa dihantar ke stderr, jadi stdout hanya membawa keputusan. Eksport yang mengandungi kredensial sentiasa memaksa mod 0600.

Sejarah adalah secara ikut serta dan melengkapkan petikan JSON serta perintah `diff` sedia ada:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Gunakan ID daripada `history`; contoh ini mengandaikan pangkalan data baharu. Petikan disimpan secara bertransaksi dengan masa mula/tamat UTC, versi pakej, tetapan bukan rahsia yang berkuat kuasa, ringkasan, dan semua pemerhatian hos/perkhidmatan, termasuk ralat setiap hos. Pemerhatian hos yang tidak lengkap dikekalkan. Jalanan yang dibatalkan tidak disimpan. Kontrak laporan, petikan, eksport, dan kod keluar imbasan sedia ada dikekalkan.

`history` menyenaraikan ringkasan JSON tanpa membaca semua muatan peranti sejarah. `compare` membaca dua imbasan yang disimpan, memerlukan identiti sasaran dan port terpilih yang serupa, serta melaporkan perubahan tindak balas, status, dan keadaan port. ID imbasan yang lebih awal mesti mendahului ID yang lebih lewat. Apabila kedua-dua imbasan merekodkan `timeout` atau `backend` dan nilai tersebut berbeza, laporan menyenaraikan amaran dan tetap membandingkan pemerhatian tersebut. Tempoh menunggu yang berbeza boleh membuatkan port yang ditapis kelihatan terbuka. Ralat pengimbas dan pemerhatian port yang tidak diketahui ditandakan sebagai tidak pasti dan bukannya dianggap sebagai kehilangan atau penutupan yang disahkan: hos yang mempunyai ralat dipaparkan dalam `uncertain_hosts`, dan setiap peralihan port yang melibatkan `unknown` (termasuk tidak diketahui dalam kedua-dua imbasan) disenaraikan dalam `unconfirmed_ports` dan bukannya `port_changes`, kecuali port yang terbuka dalam imbasan yang lebih lewat, yang merupakan perubahan port. `compare` dan `diff` mengklasifikasikan port dengan peraturan yang sama. `no_longer_responding` bermaksud ketiadaan respons, bukan bukti penyingkiran peranti. Kod keluar imbasan 0 tidak menjamin setiap hos bertindak balas: periksa ralat setiap hos. Kejayaan perbandingan mengembalikan 0 sama ada perubahan wujud atau tidak; `diff` fail sedia ada mengekalkan kontrak kod keluar 3 miliknya. Sejarah yang tidak disokong atau rosak mengembalikan 1.

Sejarah menyimpan maklumat inventori, jadi pilih direktori setempat yang dilindungi dengan sewajarnya. Fail profil dan tetapan yang disimpan tidak mengandungi kredensial SNMP; pengendalian kredensial diteruskan melalui pilihan/persekitaran masa jalan sedia ada.

## Perbezaan inventori

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Petikan ialah JSON dengan `format: "hostcensus-snapshot"`, `version: 1`, versi hostcensus, masa penciptaan UTC, sasaran, `timeout` dan `backend` imbasan apabila imbasan merekodkannya, perkhidmatan yang dikuar, dan hos yang hidup dalam bentuk yang sama seperti laporan `-o`. Hos yang mati tidak disertakan. `diff` juga menerima laporan JSON `scan -o` biasa, termasuk laporan sebelum medan `services` wujud.

`diff` melaporkan hos baharu dan hos yang hilang, port yang dibuka atau ditutup pada hos yang wujud dalam kedua-duanya, dan perkhidmatan yang `version` miliknya berubah. Port yang dikuar dalam hanya satu daripada dua imbasan tidak dibandingkan, dan amaran akan menyatakannya. Pemerhatian yang gagal tidak sesekali dibaca sebagai "tiada perubahan": port yang berkeadaan `unknown` dalam mana-mana imbasan dan tidak terbuka dalam imbasan yang lebih lewat disenaraikan di bawah `unconfirmed`, bukan `closed`, dengan `before` bernilai `open`, `unknown` atau `not-open` (dikuar dan ditutup atau ditapis) dan `after` bernilai `unknown` atau `not-open`; port yang terbuka sekarang dilaporkan di bawah `opened` walaupun kuar sebelumnya gagal. Hos yang semua kuarnya gagal tanpa jawapan dalam mana-mana imbasan disenaraikan di bawah `unsettled_hosts` (dengan `before`/`after` bernilai `up`, `uncertain` atau `absent`, termasuk apabila ia gagal dalam kedua-dua imbasan atau tiada dalam fail satu lagi) dan bukannya `vanished_hosts`; jika ia menjawab dalam imbasan yang lebih lewat, ia turut dilaporkan sebagai hos baharu dengan port terbukanya. Petikan menyimpan hos yang gagal tersebut atas sebab ini. Amaran juga muncul apabila sasaran berbeza, dan apabila kedua-dua fail merekodkan timeout atau backend serta nilai tersebut berbeza. `-o PATH` menulis bentuk JSON ke fail juga.

Laporan daripada imbasan yang dihentikan oleh `--deadline` (`"complete": false`) hanya menyenaraikan hos yang sempat dicapai, jadi `diff` dan `export` menolaknya dengan kod keluar 2. `--allow-partial` menerimanya dengan amaran pada stderr: `diff` kemudian menyenaraikan hos yang langsung tidak disenaraikan oleh imbasan tidak lengkap itu di bawah `unsettled_hosts` sebagai `unscanned` dan bukannya hilang (hos yang disenaraikan sebagai mati masih dianggap hilang), menetapkan `partial` kepada true dan tidak pernah melaporkan tiada perubahan, manakala `export` menulis amaran ke dalam pengepala skrip.

Kod keluar `diff`: `0` tiada perubahan, `3` perubahan ditemui, pemerhatian yang tidak dapat disahkan, atau input tidak lengkap (`changed` adalah true apabila mana-mana senarai, termasuk `unsettled_hosts` dan `unconfirmed`, tidak kosong, atau `partial` adalah true), `2` fail tiada, tidak boleh dibaca, bukan petikan yang disokong, atau tidak lengkap tanpa `--allow-partial`, `1` fail `-o` tidak dapat ditulis.

## Eksport Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (cabang bagi Cacti 1.2.31) tidak mempunyai import fail peranti secara pukal. Cara yang disokong untuk menambah peranti daripada skrip ialah `cli/add_device.php`, satu peranti bagi setiap panggilan, dengan argumen `--option=value`. `hostcensus export` menulis skrip POSIX `sh` bagi panggilan tersebut:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Setiap hos yang hidup menjadi `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hos yang pertanyaan SNMP imbasannya berjaya mendapat `--version=2 --community=...` atau `--version=3 --username=... --authproto=... --password=...` (ditambah `--privproto`/`--privpass` untuk authPriv), `--port` dan `--avail=snmp`. Eksport SNMPv3 memerlukan `--snmp-user`, dan noAuthNoPriv ditolak kerana `add_device.php` memerlukan kata laluan v3.
- Hos lain mendapat `--version=0 --avail=ping`, dengan `--ping_method=tcp --ping_port=` port TCP terbuka yang pertama, atau ICMP jika tiada.
- `--notes` menyenaraikan perkhidmatan dan versi yang terbuka. `--description` ialah nama DNS terbalik apabila ia ringkas (huruf, digit, `.`, `_`, `-`), jika tidak IP, dan dijadikan unik, kerana `add_device.php` menganggap perihalan sedia ada sebagai kemas kini kepada peranti tersebut.

Setiap nilai disahkan dan dipetik untuk shell dengan `shlex.quote`. Secara lalai tiada rahsia SNMP ditulis: skrip mengembangkan `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` atau `HOSTCENSUS_SNMP_PRIV_KEY` pada masa jalanan dan berhenti jika salah satu tidak ditetapkan. `--include-credentials` sebaliknya menulis nilai daripada pemboleh ubah persekitaran tersebut ke dalam skrip, menciptanya dengan mod 0600, dan melog amaran. `add_device.php` sendiri mencetak komuniti dan menerima rahsia sebagai argumen, yang kelihatan dalam senarai proses pelayan Kadupul semasa setiap panggilan berjalan.

`add_device.php` keluar dengan kod 1 untuk pendua dan ralat; skrip diteruskan, mengira kegagalan, dan keluar dengan kod 1 jika mana-mana peranti tidak berjaya ditambah. ID templat datang daripada `php cli/add_device.php --list-host-templates`. Kod keluar `export`: `0` ditulis, `2` input tidak boleh dibaca, imbasan tidak lengkap tanpa `--allow-partial`, atau data yang tidak dapat dieksport dengan selamat, `1` skrip tidak dapat ditulis.

## Pemversian dan proses keluaran

hostcensus mematuhi [Semantic Versioning](https://semver.org/spec/v2.0.0.html): pembaikan yang serasi menaikkan versi tampalan, ciri/pengusangan yang serasi menaikkan versi minor, dan perubahan keserasian yang memecahkan menaikkan versi utama. Perintah dan pilihan, kod keluar serta skema JSON adalah kontrak awam; tingkah laku yang diusangkan terus berfungsi sehingga keluaran utama seterusnya, melainkan pembaikan keselamatan memerlukan perubahannya lebih awal (log perubahan kemudiannya menyatakan sebabnya).

release-please membuka PR keluaran daripada tajuk Conventional Commit pada `main`, menaikkan versi dalam `pyproject.toml`, `uv.lock` dan `CHANGES.md`. Penggabungannya mencipta tag `vMAJOR.MINOR.PATCH` dan draf keluaran GitHub, yang mana CI melampirkan wheel yang telah diuji, pengedaran sumber dan hasil tambah semak; GitHub menyimpan pengesahan binaan untuk fail tersebut melalui API pengesahannya. Penyelenggara menyemak dan menerbitkan draf tersebut setelah fail dilampirkan. Keluaran tidak sesekali diganti.

Penerbitan dipercayai PyPI adalah ikut serta dan memerlukan pemilikan projek, penerbit dipercayai dan persekitaran `pypi`. Ia menerbitkan artifak keluaran yang telah disemak yang sama tanpa membina semula atau menyimpan token API. Keluaran bertag dalam repositori awam ini menjana pengesahan artifak GitHub; cabang peribadi memerlukan pelan yang disokong dan ikut serta secara eksplisit. Lihat [panduan keluaran lengkap](../../../docs/releasing.md) untuk persediaan, perintah tepat dan cubaan semula.

## Pembangunan

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Alatan pembangunan berada dalam kumpulan kebergantungan [PEP 735](https://peps.python.org/pep-0735/) dalam `pyproject.toml` (`dev`, `fuzz`, `build`), jadi ia tidak pernah muncul dalam metadata pakej yang diterbitkan. `uv.lock` ialah satu-satunya fail kunci; CI memasang dengan `uv sync --locked` dan gagal apabila fail kunci sudah lapuk. Pilih pentafsir dengan `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), atau mana-mana Python 3.12+.

CI menguatkuasakan had minimum liputan pakej sebanyak 90%. Ujian unit merangkumi pelayan gelung balik terkawal dan kes profil/sejarah/pengesah keluaran luar talian; makmal Compose menjalankan OpenSSH, MariaDB, nginx dan net-snmp pada jambatan terasing. Jalankannya dengan `make test-integration`. Lihat [CONTRIBUTING.md](../../../CONTRIBUTING.md) dan [alatan keluaran](../../../scripts/README.md).

Kontena masa jalan berjalan sebagai UID/GID 10001 tanpa direktori rumah, tanpa log masuk shell dan tanpa pip, serta boleh menulis ke `/app/output`. Berikan pengguna tersebut akses tulis ke mana-mana direktori output yang dilekapkan. Ia tidak memerlukan keupayaan khas dan berfungsi dengan sistem fail root baca sahaja, jadi ia boleh dijalankan sebagai:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap menggunakan tingkah laku penemuan TCP tanpa keistimewaan dalam kontena ini. CI menggagalkan binaan imej pada sebarang kerentanan HIGH atau CRITICAL yang boleh dibaiki yang dilaporkan oleh Trivy.

## Semakan rantaian bekalan

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) berjalan pada main dan setiap minggu, menerbitkan skor sebenarnya, dan memuat naik penemuan ke pengimbasan kod GitHub. Actions dan imej asas kontena dipinkan mengikut cincangan tidak boleh ubah; kebergantungan Python dileraikan dalam `uv.lock`. Kegagalan Bandit menggagalkan CI, dan fuzzing Atheris terhad menguji penghurai SSH, MySQL, HTTP, sijil dan SNMPv3 BER tanpa akses rangkaian.

Scorecard turut mengukur aktiviti semakan sejarah, kepelbagaian penyumbang, dan asal usul keluaran. Skor tersebut mencerminkan bukti sebenar; ia bukan dakwaan bahawa setiap semakan tadbir urus atau keluaran sejarah dipenuhi. Lihat [SECURITY.md](../../../SECURITY.md) dan [asal usul keluaran](../../../docs/releasing.md).

## Penyetempatan

Mesej CLI dan jadual ringkasan/perbezaan terminal menyokong 45 lokal (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) tanpa kebergantungan masa jalan tambahan. Peleraian menghormati `--lang`, kemudian `LC_ALL`, `LC_MESSAGES`, dan `LANG`, dengan sandaran kepada `en`. Skema JSON, lajur CSV, dan skrip eksport kekal tidak berubah merentas semua lokal.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Sumbangan

Sumbangan hendaklah menyertakan kes yang boleh dihasilkan semula, mengekalkan kontrak CLI dan format data yang didokumenkan, serta lulus semakan kualiti di atas. Lihat [CONTRIBUTING.md](../../../CONTRIBUTING.md) untuk aliran kerja pembangunan dan [panduan keluaran](../../../docs/releasing.md) untuk keputusan keserasian dan pemversian.

## Status keselamatan dan lesen

Lihat [SECURITY.md](../../../SECURITY.md) untuk pelaporan peribadi dan versi yang disokong. hostcensus dilesenkan di bawah [Lesen MIT](../../../LICENSE).

Pengepala sumber menggunakan pengecam SPDX dan mengekalkan kredit penyumbang daripada sejarah Git. Lihat [AUTHORS.md](../../../AUTHORS.md) untuk atribusi. Tangkapan ujian binari dan fail kunci yang dijana menggunakan fail `.license` bersebelahan; teks MIT terdapat dalam `LICENSES/MIT.txt`.
