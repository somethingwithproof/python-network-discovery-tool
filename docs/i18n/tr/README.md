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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · **Türkçe** · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus, yönettiğiniz ağlarda tekrarlanabilir servis envanteri çıkarmak için geliştirilmiş bir Python CLI aracıdır.
Cihazların dışa açtığı servisleri kaydeder, zaman içindeki gözlemleri karşılaştırır ve
Kadupul içe aktarma betikleri üretir. Varsayılan arka uç root yetkisi olmadan asyncio soketlerini kullanır;
isteğe bağlı Nmap keşfi ise yapılandırılan servis portlarının dışındaki ana bilgisayarları belirleyebilir.

## Neden hostcensus

Tek seferlik bir port raporu, bir sonraki gözlemin gerçekten değişip değişmediğini
yoksa yalnızca başarısız mı olduğunu açıklamaz. hostcensus; açık servis durumlarını, sınırlandırılmış yoklamaları,
yeniden kullanılabilir tarama profillerini ve yerel geçmişi bir araya getirir. Operatörler aynı kapsamı tekrarlayabilir,
hataları inceleyebilir ve belirsiz gözlemleri doğrulanmış değişikliklerden ayırt edebilir.

- **Servis kanıtları:** SSH kimlik tanımlaması, MySQL selamlamaları, HTTP başlıkları, TLS
  sertifika gözlemleri ve SNMP keşfi ya da kimlik bilgili system-MIB sorguları.
- **Tekrarlanabilir kapsam:** Adlandırılmış TOML profilleri, eklemeli hariç tutmalar, yapılandırılabilir
  servisler, ana bilgisayar/yoklama üst sınırları ve sınırlandırılmış çalışanlar.
- **Trafik öncesi kontroller:** Yerel ön kontrol; hedefleri, araçları, hedef erişimini,
  geçmiş şemasını ve yapılandırılmış TLS CA paketlerini doğrular.
- **Envanter geçmişi:** İşlemsel SQLite anlık görüntüleri tüm gözlemleri saklar;
  karşılaştırmalar tarayıcı hatalarını ve bilinmeyen durumları görünür tutar.
- **Birlikte çalışabilir çıktı:** Terminal, JSON ve CSV raporları, sürümlenmiş dosya anlık görüntüleri
  ve Kadupul içe aktarma betikleri.

CI; Linux ve macOS üzerinde Python 3.12, 3.13 ve 3.14 sürümlerinin yanı sıra kontrollü bir Compose
enteegrasyon laboratuvarını kapsar. Kod, bu çalışma zamanı sürümlerini korurken modern tür takma adları,
tiplendirilmiş ön kontrol sonuçları, yalnızca anahtar sözcük argümanlı slot tabanlı profiller ve
yapılandırılmış async temizleme kullanır. SemVer uyumluluk sözleşmesi ve GitHub sürüm süreci için
[Sürümleme ve yayınlar](../../../docs/releasing.md) belgesine bakın. Sürüm rozeti mevcut çalışma kopyasını değil
yayımlanan yapıları açıklar: şu anda en son yayımlanan etiket `v0.3.0` iken bu çalışma kopyası
`3.0.0` paket sürümünü kullanır. Burada belgelenen envanter özelliklerini kullanmak için çalışma
kopyasından kurulum yapın.

[Kurulum](#install) ile başlayın, ardından [profiller ve geçmiş](#inventory-profiles-preflight-and-local-history) bölümüne geçin.
Entegrasyon ayrıntıları için [servis parmak izleri](#fingerprints),
[dosya karşılaştırmaları](#inventory-diff) ve [Kadupul dışa aktarma](#kadupul-export) bölümlerine bakın.

## Kurulum

Python 3.12 veya daha yeni bir sürüm gereklidir; test edilen matris Python 3.12-3.14 aralığıdır. Bu
çalışma kopyasından kilitli çalışma zamanı bağımlılıklarını kurun:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

İsteğe bağlı Nmap ana bilgisayar keşfi için platformunuzun paket yöneticisini kullanarak Nmap çalıştırılabilir
dosyasını kurun; ek bir Python paketi gerekmez. Nmap'in XML çıktısı temel bağımlılıklardan biri olan
defusedxml ile ayrıştırılır, bu nedenle varlık genişletme (entity expansion) reddedilir. hostcensus,
`PATH` üzerinde bulunan `nmap` ikilisini sabit bir argüman listesi, alt ağ ön eki boyutuna göre büyüyen
bir zaman sınırı ve 64 MiB çıktı üst sınırıyla doğrudan çalıştırır. Varsayılan arka uç için Nmap gerekli değildir.

## netprobe'dan geçiş

hostcensus, 3.0.0 sürümünde yayımlanan netprobe'un yeni adıdır. Proje hiçbir ad altında
PyPI'da yayımlanmamıştır; bu nedenle kurulumlar bir çalışma kopyasından veya bir GitHub
sürümünden yapılmıştır. GitHub deposu adını korur.

| Önceki | Şimdi | Uyumluluk |
| --- | --- | --- |
| `netprobe` dağıtımı | `hostcensus` | Çalışma kopyasından yeniden kurun; eski adla bir paket yoktur. |
| `netprobe` komutu | `hostcensus` | `netprobe` hâlâ çalışır ve stderr'e bir kullanımdan kaldırma satırı yazar. Çıkış kodları ve stdout değişmemiştir. Bir sonraki ana sürümde kaldırılacaktır. |
| `NETPROBE_*` ortam değişkenleri | `HOSTCENSUS_*` | İlgili `HOSTCENSUS_*` karşılığı ayarlanmadığında `NETPROBE_*` değişkeni kullanılır ve değerlerini asla yazdırmadan yalnızca değişken adlarını belirten tek bir stderr uyarısı verilir. Her ikisi de ayarlıysa `HOSTCENSUS_*` geçerli olur. Bir sonraki ana sürümde kaldırılacaktır. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Uyumluluğu bozan değişiklik.** İçe aktarma uyumluluk katmanı kurulmaz; içe aktarmaları güncelleyin. |
| Docker imaj etiketi `network-discovery:test` (yalnızca CI) ve kapsayıcı kullanıcısı `netprobe` | `hostcensus:test`, kullanıcı `hostcensus` | Hiçbir kayıt defteri imajı yayımlanmamıştır. İmajı yeniden oluşturun ve `hostcensus` giriş noktasını kullanın. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Yeni ad mevcut değilken eski varsayılan ada sahip bir dosya varsa bir uyarıyla birlikte kullanılmaya devam edilir. Açıkça belirtilen `--config` ve `--history` yollarına dokunulmaz. |
| `"format": "netprobe-report"` veya `"netprobe-snapshot"` içeren raporlar ve anlık görüntüler ile `netprobe_version` alanı | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` ve `export` eski adla yazılan dosyaları yüklemeye devam eder ve yayımlanan JSON Şemaları her iki yazımı da kabul eder. Yeni dosyalar yeni adları kullanır. SQLite geçmiş veritabanları değişmemiştir ve eskisi gibi yüklenir. |
| `netprobe export` çıktısı Kadupul betikleri | `hostcensus export` çıktısı betikler | Eski betikler çalışmaya devam eder ve çalıştırıldıklarında hâlâ `NETPROBE_SNMP_*` değişkenlerini okur. Yeni betikler `HOSTCENSUS_SNMP_*` okur. |

## Hızlı örnek

Geliştirme bölümünde açıklanan entegrasyon laboratuvarının tester kapsayıcısından çalıştırılmıştır; çıktı kısaltılmıştır:

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

## Çıkış kodları

| Komut | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | gözlemler/rapor kaydedildi | ön kontrol/arka uç, geçmiş ya da rapor/anlık görüntü yazımı başarısız | geçersiz hedef, seçenekler, yapılandırma veya sınırlar | - | `--deadline` süresine ulaşıldı; kısmi rapor yazıldı, geçmiş ve anlık görüntü atlandı |
| `preflight` | kontroller başarılı | yerel kontrol başarısız | geçersiz hedef/yapılandırma veya çakışan hedefler | - | - |
| `profiles` | doğrulanan profiller listelendi | - | okunamayan/geçersiz yapılandırma veya seçim | - | - |
| `history` | özetler listelendi | eksik, geçersiz veya desteklenmeyen geçmiş | geçersiz CLI seçenekleri | - | - |
| `compare` | değişiklikler olduğunda bile karşılaştırma üretildi | okunamayan geçmiş, uyumsuz kapsam/sıra veya yazma hatası | geçersiz CLI seçenekleri | - | - |
| `diff` | değişiklik yok | `-o` dosyası yazılamadı | eksik, okunamayan veya desteklenmeyen girdi ya da `--allow-partial` olmadan tamamlanmamış tarama | değişiklik bulundu, doğrulanmamış gözlemler veya tamamlanmamış tarama | - |
| `export` | betik yazıldı | betik yazılamadı | okunamayan girdi, `--allow-partial` olmadan tamamlanmamış tarama veya güvenli biçimde dışa aktarılamayan veri | - | - |

## Yapı

| Modül | Sorumluluk |
| --- | --- |
| `cli.py` | Komut seçenekleri, profil çözümleme, ön kontrol, tarama ve raporlama |
| `scanner.py`, `probes.py` | Hedef genişletme, sınırlandırılmış çalışanlar, ana bilgisayar keşfi ve servis gözlemleri |
| `config.py`, `profiles.py` | Servis tanımları ve doğrulanmış envanter profilleri |
| `models.py`, `output.py` | Sonuç türleri ve terminal/JSON/CSV oluşturma |
| `history.py`, `diff.py` | SQLite geçmişi ve sürümlenmiş dosya-anlık görüntü karşılaştırmaları |
| `preflight.py` | Yerel kontroller ve sınırlandırılmış Nmap sürüm sorgusu |
| `export.py` | Doğrulanmış ve kabuk alıntılaması yapılmış Kadupul içe aktarma betikleri |

Her servis gözlemi, durumunu duyurulan kimliğinden ayrı olarak kaydeder.
Okumalar ve zaman sınırları sınırlandırılmıştır; yoklama istisnaları ana bilgisayar hatalarında kalır. SQLite
geçmişi işlemleri, açık bağlantı temizlemeyi ve salt okunur listeleme ile
karşılaştırma yollarını kullanır. SNMP gizli bilgileri yalnızca ortam değişkenleri veya gizli
dosyalar üzerinden girer; envanter geçmişi gizli olmayan etkin ayarları saklar. Tarama ardışık düzeni, sınırları ve güven
sınırları için [Mimari](../../../docs/architecture.md) belgesine, yetkili kullanım için
[SECURITY.md](../../../SECURITY.md#authorized-use) belgesine bakın.


## Kullanım

Yalnızca yönettiğiniz ağları tarayın.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Seçenek | Anlamı |
| --- | --- |
| `NETWORK` | CIDR, IP veya ana bilgisayar adı; `--profile` ile isteğe bağlıdır. IPv6 kapsam tanımlayıcıları reddedilir. |
| `-o, --output PATH` | Rapor yazar. Biçim uzantıyı izler (`.json`, `.csv`); diğer uzantılar varsayılan olarak JSON'a döner. |
| `-f, --format json\|csv\|kadupul\|auto` | Rapor biçimini zorlar. `--output` olmadan etkisi yoktur. `.sh` uzantısı `kadupul` seçer. |
| `-v, --verbose` | Hata ayıklama günlüklemesi. |
| `-q, --quiet` | Sonuçları, ilerlemeyi ve bilgilendirme günlüklerini gizler; uyarılar ve hatalar stderr üzerinde görünmeye devam eder. |
| `--backend asyncio\|nmap` | Ana bilgisayar keşfi. `asyncio` (varsayılan) servis portlarını doğrudan yoklar; `nmap` önce bir nmap ping taraması çalıştırır ve `PATH` üzerinde `nmap` çalıştırılabilir dosyasını gerektirir. |
| `--timeout SECONDS` | Kendi bütçesini belirlemeyen yoklamalar için bekleme süresi (varsayılan 1.0). Yerleşik bağlantı yoklamaları servis tablosu `timeout` belirtmediği sürece 0.3s kullanır. |
| `--concurrency N` | Aynı anda yürütülecek yoklama sayısı (varsayılan 256). |
| `--deadline SECONDS` | nmap taraması dahil tüm taramayı bu süreden sonra durdurur (varsayılan 3600, en fazla 604800; ortam değişkeni `HOSTCENSUS_DEADLINE`). Tamamlanan ana bilgisayarlar rapora `"complete": false` ile yazılır, geçmiş veya anlık görüntü yazılmaz ve `scan` 4 çıkış koduyla sonlanır. |
| `--config PATH` | TOML servis tanımları ve isteğe bağlı adlandırılmış `[profiles]` ayarları. |
| `--profile NAME` | Adlandırılmış bir profil kullanır; `--config` verilmediğinde varsayılan olarak `hostcensus.toml` dosyasına bakar. |
| `--exclude IP/CIDR` | Hariç tutma ekler; gerektiği kadar tekrarlanabilir. Hariç tutulan bir IPv4 ana bilgisayarı kendisine ulaşan IPv6 adreslerini de hariç tutar: IPv4 eşlemeli (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) ve 6to4. IPv4 eşlemeli hedefler ve hariç tutmalar temsil ettikleri IPv4 adresleri olarak ele alınır. |
| `--max-hosts N` | Hariç tutmalardan önce kontrol edilen adres sınırı (varsayılan/kesin üst sınır 65.536). |
| `--history PATH` | Tamamlanan taramayı isteğe bağlı bir SQLite geçmiş veritabanına kaydeder. |
| `--services NAMES` | Kontrol edilecek servis adlarının virgülle ayrılmış listesi, belirtilen sırada (varsayılan: tümü). |
| `--ports SPEC` | `NAME=PORT` (bir servisi taşı) veya `PORT` (`tcp-PORT` adlı düz bir TCP kontrolü ekle) biçiminde virgülle ayrılmış liste. |
| `--snmp-community-file PATH` | Sistem MIB sorgusu için SNMPv2c topluluk dizesini tutan dosya. Ortam değişkeni: `HOSTCENSUS_SNMP_COMMUNITY` (değer) veya `HOSTCENSUS_SNMP_COMMUNITY_FILE` (dosya yolu). |
| `--snmp-user` | SNMPv3 kullanıcısı. Ortam değişkeni: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (varsayılan), `SHA224`, `SHA256`, `SHA384`, `SHA512` ve parolayı tutan dosya. Ortam değişkeni: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` veya `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (varsayılan), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` ve parolayı tutan dosya. Ortam değişkeni: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` veya `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Ayrıca `hostcensus diff` için sürümlenmiş bir anlık görüntü yazar. |
| `--tls-ca-file PATH` | HTTPS sertifikalarını sistem deposu yerine bu PEM paketine göre doğrular. Ortam değişkeni: `HOSTCENSUS_TLS_CA_FILE`. |

Varsayılan olarak her ana bilgisayar SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) ve HTTPS (TCP 443) için kontrol edilir. TCP portları tam bağlantı ile test edilir. SNMP, herhangi bir SNMPv3 aracısının kimlik bilgisi olmadan yanıtlaması gereken bir SNMPv3 motor keşif isteğiyle test edilir; yalnızca v1/v2c konuşan aracılar bu yoklama tarafından algılanmaz. asyncio arka ucunda, reddedilen bir bağlantı dahil olmak üzere herhangi bir yoklama yanıt aldığında ana bilgisayar canlı sayılır; bu nedenle her yoklamayı düşüren bir ana bilgisayarda `alive=false` ve "Host is down" hatası görünür; bu, fiziksel olarak kapalı olduğunu kanıtlamaz. `--backend nmap` ile hangi ana bilgisayarların canlı olduğuna nmap karar verir (root olarak ICMP, aksi halde TCP 80/443).

### Parmak izleri

Açık olan her servis, oturum açmadan önce gönderdiği verilerden parmak izi çıkarılarak tanımlanır. Yalnızca siz kimlik bilgisi sağladığınızda çalışan SNMP sorgusu dışında hiçbir şey kimlik doğrulaması yapmaz.

| Yoklama | Okuduğu | `version` | `details` anahtarları |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 kimlik satırı | yazılım, ör. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | MySQL/MariaDB ilk el sıkışması | sunucu sürümü | `server_version`, `flavor`, `auth_plugin` veya `error_code`/`error` |
| `http` | `HEAD /` yanıtı | `Server` başlığı | `status`, `server` |
| `https` | TLS el sıkışması, sertifika, `HEAD /` | `Server` başlığı | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 keşfi; kimlik bilgileriyle sysDescr, sysObjectID, sysName GET isteği | sysDescr | `engine_id`; kimlik bilgileriyle `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` veya `snmp_error` |

Ana bilgisayar adı hedefi ana bilgisayar başına bir kez çözümlenir ve her yoklama sonuçlarda `address` olarak kaydedilen bu adrese bağlanır; ad yalnızca TLS SNI, sertifika doğrulaması ve HTTP `Host` başlığı için kullanılır. Çözümlenemeyen bir ad `unknown` durumları ve `Cannot resolve` hatası üretir. Ters DNS adları yalnızca ana bilgisayar adı karakterleri içerdiğinde saklanır ve aynı anda en fazla 16 sorgu çalışır. HTTPS, sistem deposuna veya `--tls-ca-file` dosyasına göre sertifika ve ana bilgisayar adı doğrulaması kullanır. Güven deposu tarama için bir kez yüklenir ve her HTTPS yoklamasında yeniden kullanılır. TCP bağlantısı ve TLS el sıkışması ayrı ayrı zamanlanır; bu nedenle bağlantıyı kabul eden ancak el sıkışmasını askıda bırakan bir port `filtered` değil `tls_error` ile `open` olur. Doğrulama başarısız olursa sonuç `cert_verified: false` ve `cert_verify_error` kaydeder; daha zayıf ayarlarla yeniden denemez veya HTTP isteği göndermez. Sertifika ayrıntıları ve HTTP başlıkları yalnızca doğrulama başarılı olduktan sonra toplanır. Özel CA servisleri için doğru CA paketini sağlayın. Eski raporlarda mevcut yoklamaların artık üretmediği `cert_read_unverified` bulunabilir.

SNMP gizli bilgileri, işlem listesinde diğer yerel kullanıcıların görebileceği komut satırı değerlerinden değil, yalnızca ortam değişkenlerinden veya dosyalardan (`--snmp-*-file` ya da eşleşen `HOSTCENSUS_SNMP_*_FILE` değişkeni) okunur. Değer alan `--snmp-community`, `--snmp-auth-key` ve `--snmp-priv-key` seçenekleri 2 çıkış koduyla sonlanır ve yerine kullanılacak seçeneği belirtir. Gizli bir dosya en fazla 4096 bayt boyutunda, boş olmayan UTF-8 olmalıdır; sondaki bir yeni satır yok sayılır ve aynı gizli bilgi için hem değişken hem dosya ayarlamak hatadır. Hatalar dosya adını belirtir ancak içeriğini asla yazdırmaz. Tarama raporları ve geçmiş kasıtlı olarak kimlik bilgisi değerlerini içermez. Dışa aktarıcı, aşağıda açıklanan ayrı ve açık bir `--include-credentials` seçeneğine sahiptir. Bir topluluk dizesi SNMPv2c'yi seçer; bir kullanıcı ise auth anahtarı verildiğinde kimlik doğrulamalı, her iki anahtar verildiğinde gizlilik korumalı SNMPv3'ü seçer (`snmp_security_level` hangisi olduğunu kaydeder). hostcensus; bir topluluk dizesini v3 kullanıcısıyla birleştirmeyi, auth anahtarı olmadan gizlilik anahtarı kullanmayı veya kullanıcı olmadan anahtar kullanmayı 2 çıkış koduyla reddeder ve başarısız olan bir v3 sorgusunu asla v2c ya da daha düşük bir güvenlik düzeyiyle yeniden denemez. Yalnızca v1/v2c konuşan aracılar kimlik bilgisiz v3 keşfini yok sayar, bu nedenle yalnızca bir topluluk dizesi sağlandığında açık görünürler.

Başlık (banner) metni yazdırılabilir karakterlere indirgenir ve saklanmadan veya gösterilmeden önce 256 karakterle sınırlandırılır. Okumalar da sınırlandırılmıştır: satır başına 4 KiB, MySQL selamlaması için 4 KiB, HTTP başlıkları için 16 KiB. 32 sekizliden uzun bir SNMP motor kimliği saklanmadan önce kırpılır. HTTP ve HTTPS, köşeli parantez içinde bir IPv6 adresiyle ve 80 ya da 443 olmadığında port numarasıyla bir Host başlığı gönderir. Hesap tablosu formül tetikleyicisiyle başlayan CSV hücrelerine, hücrenin metin olarak kalması için ön ek eklenir.

### Sınırlar

Tek bir çalıştırma en fazla 65.536 adres, 64 servis ve 524.288 yoklama (ana bilgisayar sayısı çarpı servis sayısı) kabul eder; daha büyük istekler hiçbir şey gönderilmeden 2 çıkış koduyla sonlanır. `--concurrency` en fazla 4096 soketle sınırlandırılmıştır. Her yoklamanın kendi bütçesinin dört katı kadar kesin bir zaman sınırı vardır. Bağlantı yoklamaları (`tcp`, `ssh`, `mysql`, `http`), ilgili servis `timeout` ayarlamadığı sürece 0.3 saniye kullanır. SNMP ve HTTPS kendi değerini ayarlamadığında `--timeout` (varsayılan 1.0) değerini kullanır. Zaman sınırına ulaşan bir yoklama, `errors` içinde "probe timed out" ile `unknown` olarak raporlanır. Yerel soket hataları da (örneğin dosya tanımlayıcılarının tükenmesi) kaydedilen hatayla birlikte `unknown` olur; asla filtrelenmiş bir port veya kapalı bir ana bilgisayar olarak sayılmazlar. Yoklamadan önce hostcensus, `--concurrency` artı 64 tanımlayıcıya sığacak şekilde açık dosya yumuşak sınırını sert sınıra doğru yükseltir; bunu yapamadığında `open files` ön kontrolü başarısız olur ve `scan` trafik göndermeden 1 koduyla çıkar. Nmap keşfi 30 saniyelik bir ana bilgisayar zaman aşımı kullanır. Bir alt ağ ön eki nmap'e CIDR biçiminde iletilir ve nmap kendisine verilenden daha az adres bildirdiğinde (örneğin çözümleyemediği bir ad nedeniyle) ana bilgisayarları kapalı işaretlemek yerine tarama 1 çıkış koduyla başarısız olur. Ana bilgisayar adı hedefi bir kez çözümlenir ve nmap'e bu adres verilir; böylece keşif ve yoklamalar aynı makineye ulaşır. Tam bir ön ek, alt süreç zaman sınırı her 256 adres için yukarı yuvarlanarak 35 saniye olan tek bir nmap sürecidir. Hariç tutmalar içeren taramalar 256 ana bilgisayarlık gruplar ve her grup için 35 saniyelik bir zaman sınırı kullanır. Çalışan oluşturma, aralık boyutundan bağımsız olarak sınırlandırılmıştır. Ters DNS ve ana bilgisayar adı çözümlemesinin ayrı bir iki saniyelik zaman sınırı vardır; hiç dönmeyen bir çözümleyici çağrısı kendi iş parçacığında terk edilir, böylece hostcensus'u bu sınırların ötesinde çalışır durumda tutamaz. Aynı anda en fazla 16 sorgu çalışır ve terk edilen bir çağrı dönene kadar yuvasını tutar, bu sayede takılı kalan iş parçacıklarının sayısı sınırlı kalır; 16 yuvanın tümü askıda kalırsa, sonraki sorgular `--deadline` taramayı durdurana kadar iki saniyelik zaman sınırının dışında (bu süre bir yuva boşaldığında başlar) bir yuva için sıraya girer. `deadline` olmadan kütüphane olarak kullanılan `NetworkScanner`, böyle bir yuva için süresiz bekleyebilir. Bunların üzerinde `--deadline` (varsayılan bir saat) tüm çalıştırmayı sınırlar.

### Servisleri yapılandırma

Servisler bir TOML dosyasıyla değiştirilebilir:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` değeri `tcp`, `ssh`, `mysql`, `http`, `https` veya `snmp` değerlerinden biridir ve servis adı bir yoklama adı olduğunda varsayılan olarak servis adını, aksi halde `tcp` değerini alır. Yalnızca `snmp` UDP kullanır. Servis adları küçük harfler, rakamlar, `-` ve `_` içerir. İki servis aynı port ve protokolü paylaşamaz; geçmiş bu çift için tek bir durum kaydeder. `timeout` isteğe bağlıdır, saniye cinsindendir ve en az 0.05'tir. Bağlantı tarzı yoklamalar (`tcp`, `ssh`, `mysql`, `http`) varsayılan olarak 0.3 saniye kullanır. `snmp` ve `https`, servis `timeout` ayarlamadığında taramanın `--timeout` değerini kullanır. `--timeout`, servisin zaten sahip olduğu bir bütçeyi değiştirmez.

JSON raporları, hedefi, yoklanan servisleri ve ayarları `devices` yanında kaydeden sürümlenmiş belgelerdir (`"format": "hostcensus-report"`, `"version": 1`); `-o` olmadan `--format json`, tablo yerine raporu stdout'a yazar. Her JSON çıktısının yayımlanmış bir şeması vardır; bkz. [JSON çıktısı](../../../docs/json-output.md). Cihazlar özgün `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` ve `errors` alanlarını korur ve her yoklamanın `name`, `port`, `protocol`, `state` (yoklama yerel olarak başarısız olduğunda veya zaman sınırına ulaştığında `open`, `closed`, `filtered` veya `unknown`), `version` ve `details` bilgilerini içeren bir `services` listesi ekler. CSV çıktısı açık olanlar için sonda `services` ve `versions` sütunları kazanır. `ssh`, `snmp` ve `mysql` mantıksal değerleri tam olarak bu adlara sahip servisleri izler.


## Envanter profilleri, ön kontrol ve yerel geçmiş

Adlandırılmış profiller, mevcut `[services]` tanımlarıyla aynı TOML dosyasını paylaşır.
[hostcensus.example.toml](../../../hostcensus.example.toml) dosyasını `hostcensus.toml` olarak kopyalayın ve yönettiğiniz ağları ayarlayın:

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

`preflight`, açık dosya kontrolü için `--concurrency` dahil olmak üzere seçenekleri ve profilleri tam olarak `scan` gibi çözümler;
bu nedenle başarılı bir ön kontrol, `scan` komutunun aynı planla başlayacağı anlamına gelir.

Profiller `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` ve `max_hosts` ayarlarını kabul eder. `services` ve `ports` mevcut virgülle ayrılmış liste
söz dizimini kullanır. Açık CLI seçenekleri profil ayarlarını geçersiz kılar; tekrarlanan `--exclude`
seçenekleri profil hariç tutmalarına eklenir. `--profile` ile verilen açık bir ağ,
o profilin IP/CIDR kapsamı içinde yer almalıdır. Ana bilgisayar adları doğrudan taramalar için
desteklenmeye devam eder ancak IP hariç tutmalarıyla birleştirilemez. Ana bilgisayar sınırları hariç tutmalardan önce
uygulanır; toplam yoklama üst sınırı ise sonrasında uygulanmaya devam eder. Hariç tutulan ana bilgisayarlar
hem servis kontrollerinden hem de isteğe bağlı Nmap keşfinden çıkarılır.

Her tarama, hedef trafikten önce yerel ön kontroller gerçekleştirir: hedef/yoklama
sınırları, hedef erişimi, isteğe bağlı Nmap çalıştırılabilir dosya/sarmalayıcı kullanılabilirliği, geçmiş
şeması ve yapılandırılmış bir TLS CA paketi. `preflight` JSON raporlar ve hedefleri taramaz
ya da bir geçmiş veritabanı oluşturmaz. Mevcut içeriği değiştirmeden hedef erişimini test etmek için
geçici olarak kardeş bir dosya yazar. Varsayılan asyncio arka ucu
hâlâ ne Nmap ne de root gerektirir. Hedef yolları sabit bağlantılar dahil olmak üzere
birbirinden ve girdi yapılandırmasından farklı olmalıdır; hedef sembolik bağlantıları
reddedilir. Başarısız kontroller 1 döndürür; geçersiz kapsam/yapılandırma 2 döndürür.

Rapor ve dışa aktarma yazma işlemleri `O_NOFOLLOW` desteği gerektirir. Windows dahil bunun bulunmadığı platformlarda,
bu yazma işlemleri hedefi açmadan veya kesmeden başarısız olur. Yeni raporlar ve dışa aktarma betikleri yalnızca sahip erişimlidir (kip 0600);
mevcut bir dosyanın değiştirilmesi izinlerini korur. Okuyucusu olmayan bir adlandırılmış boruya yazma işlemi beklemek yerine hemen başarısız olur.
Yeni bir `--history` veritabanı da yalnızca sahip erişimli oluşturulur; mevcut olan kipini korur. Günlük iletileri her zaman stderr'e gider,
böylece stdout yalnızca sonuçları taşır. Kimlik bilgisi içeren dışa aktarmalar her zaman 0600 kipini zorlar.

Geçmiş isteğe bağlıdır ve mevcut JSON anlık görüntülerini ile `diff` komutunu tamamlar:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

`history` çıktısındaki kimlikleri kullanın; örnek yeni bir veritabanı varsayar. Anlık görüntüler
UTC başlangıç/bitiş zamanları, paket sürümü, gizli olmayan etkin
ayarlar, özetler ve ana bilgisayar başına hatalar dahil tüm ana bilgisayar/servis gözlemleriyle işlemsel olarak saklanır.
Tamamlanmamış ana bilgisayar gözlemleri korunur. İptal edilen çalıştırmalar kaydedilmez. Mevcut
rapor, anlık görüntü, dışa aktarma ve tarama çıkış kodu sözleşmeleri korunur.

`history`, tüm geçmiş cihaz yüklerini okumadan JSON özetlerini listeler.
`compare`, kaydedilmiş iki taramayı okur, özdeş hedef kimlikleri ve seçili
portlar gerektirir ve yanıt verebilirlik, durum ile port durumu değişikliklerini bildirir. Daha önceki
tarama kimliği daha sonraki kimlikten önce gelmelidir. Her iki tarama da `timeout` veya `backend` kaydettiğinde
ve bu değerler farklı olduğunda, rapor bir uyarı listeler ve yine de gözlemleri karşılaştırır.
Farklı bir bekleme süresi, filtrelenmiş bir portun açık görünmesine neden olabilir. Tarayıcı hataları
ve bilinmeyen port gözlemleri, doğrulanmış kaybolma veya kapanma olarak ele alınmak yerine belirsiz olarak işaretlenir:
hatalı ana bilgisayarlar `uncertain_hosts` içinde görünür ve
`unknown` içeren her port geçişi (her iki taramada da bilinmeyen dahil), daha sonraki taramada açık olan bir port hariç (`port_changes` olarak sayılır)
`port_changes` yerine `unconfirmed_ports` içinde listelenir.
`compare` ve `diff` portları aynı kuralla sınıflandırır.
`no_longer_responding` cihazın kaldırıldığının kanıtı değil, yanıt alınamaması anlamına gelir.
Tarama çıkış kodu 0 her ana bilgisayarın yanıt verdiğini garanti etmez: ana bilgisayar başına hataları inceleyin.
Karşılaştırma başarısı, değişiklik olup olmadığına bakılmaksızın 0 döndürür; mevcut dosya `diff` komutu
3 çıkış kodu sözleşmesini korur. Desteklenmeyen veya bozuk geçmiş 1 döndürür.

Geçmiş envanter bilgilerini saklar, bu nedenle uygun biçimde korunan yerel bir
dizin seçin. Profil dosyaları ve saklanan ayarlar SNMP kimlik bilgilerini içermez;
kimlik bilgisi yönetimi mevcut çalışma zamanı seçenekleri/ortam değişkenleri aracılığıyla devam eder.

## Envanter karşılaştırması (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Anlık görüntü; `format: "hostcensus-snapshot"`, `version: 1`, hostcensus sürümü, UTC oluşturulma zamanı, hedef, tarama kaydettiyse tarama `timeout` ve `backend` değerleri, yoklanan servisler ve `-o` raporuyla aynı biçimde canlı ana bilgisayarları içeren bir JSON belgesidir. Kapalı ana bilgisayarlar dışarıda bırakılır. `diff`, `services` alanının var olmasından önce oluşturulanlar dahil olmak üzere düz `scan -o` JSON raporlarını da kabul eder.

`diff`; yeni ve kaybolan ana bilgisayarları, her ikisinde de bulunan ana bilgisayarlarda açılan veya kapanan portları ve `version` değeri değişen servisleri raporlar. İki taramadan yalnızca birinde yoklanan portlar karşılaştırılmaz ve bunu belirten bir uyarı gösterilir. Başarısız gözlemler asla "değişiklik yok" olarak yorumlanmaz: her iki taramadan birinde `unknown` olan ve sonraki taramada açık olmayan bir port `closed` yerine `unconfirmed` altında `before` değeri `open`, `unknown` veya `not-open` (yoklandı ve kapalı ya da filtrelenmiş) ve `after` değeri `unknown` veya `not-open` olacak şekilde listelenir; önceki yoklama başarısız olsa bile şimdi açık olan bir port `opened` altında raporlanır. İki taramadan birinde tüm yoklamaları yanıt alamadan başarısız olan bir ana bilgisayar, `vanished_hosts` yerine `unsettled_hosts` altında (`before`/`after` değerleri `up`, `uncertain` veya `absent` olarak; her iki taramada da başarısız olduğunda veya diğer dosyada eksik olduğunda dahil) listelenir; sonraki taramada yanıt verirse açık portlarıyla birlikte yeni bir ana bilgisayar olarak da raporlanır. Anlık görüntüler bu nedenle bu başarısız ana bilgisayarları korur. Hedefler farklı olduğunda ve her iki dosya da bir zaman aşımı veya arka uç kaydettiğinde ve bu değerler farklı olduğunda da bir uyarı görünür. `-o PATH` JSON biçimini bir dosyaya da yazar.

`--deadline` nedeniyle durdurulan bir taramadan (`"complete": false`) gelen rapor yalnızca ulaşabildiği ana bilgisayarları listeler, bu nedenle `diff` ve `export` bu raporu 2 çıkış koduyla reddeder. `--allow-partial` bunu stderr üzerinde bir uyarıyla kabul eder: `diff` bu durumda tamamlanmamış taramanın hiç listelemediği ana bilgisayarları kaybolmuş yerine `unsettled_hosts` altında `unscanned` olarak listeler (kapalı olarak listelediği bir ana bilgisayar yine kaybolmuş sayılır), `partial` değerini true olarak ayarlar ve asla değişiklik yok raporlamaz; `export` ise betik başlığına bir uyarı yazar.

`diff` çıkış kodları: `0` değişiklik yok, `3` değişiklik bulundu, doğrulanamayan gözlemler veya tamamlanmamış girdi (`unsettled_hosts` ve `unconfirmed` dahil herhangi bir liste boş olmadığında ya da `partial` true olduğunda `changed` true olur), `2` bir dosya eksik, okunamıyor, desteklenen bir anlık görüntü değil veya `--allow-partial` olmadan tamamlanmamış, `1` `-o` dosyası yazılamadı.

## Kadupul dışa aktarma

[Kadupul](https://github.com/kadupulhq/kadupul) (Cacti 1.2.31 çatalı), toplu cihaz dosyası içe aktarma özelliğine sahip değildir. Bir betikten cihaz eklemek için desteklediği yol, her çağrıda bir cihaz olmak üzere `--option=value` argümanlarıyla `cli/add_device.php` kullanmaktır. `hostcensus export` bu çağrılardan oluşan bir POSIX `sh` betiği yazar:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Canlı olan her ana bilgisayar `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` satırına dönüşür:

- Taramanın SNMP sorgusunun başarılı olduğu ana bilgisayarlar `--version=2 --community=...` veya `--version=3 --username=... --authproto=... --password=...` (authPriv için ayrıca `--privproto`/`--privpass`), `--port` ve `--avail=snmp` alır. SNMPv3 dışa aktarımı `--snmp-user` gerektirir ve `add_device.php` bir v3 parolası gerektirdiğinden noAuthNoPriv reddedilir.
- Diğer ana bilgisayarlar `--version=0 --avail=ping` ile birlikte ilk açık TCP portu için `--ping_method=tcp --ping_port=`, hiç yoksa ICMP alır.
- `--notes` açık servisleri ve sürümleri listeler. `--description`, sade olduğunda (harfler, rakamlar, `.`, `_`, `-`) ters DNS adı, aksi halde IP adresidir ve `add_device.php` mevcut bir açıklamayı o cihazda güncelleme olarak ele aldığı için benzersiz hale getirilir.

Her değer doğrulanır ve `shlex.quote` ile kabuk alıntılaması yapılır. Varsayılan olarak hiçbir SNMP gizli bilgisi yazılmaz: betik çalıştırma zamanında `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` veya `HOSTCENSUS_SNMP_PRIV_KEY` değişkenlerini genişletir ve biri ayarlanmamışsa durur. `--include-credentials` bunun yerine bu ortam değişkenlerindeki değerleri betiğe yazar, dosyayı 0600 kipiyle oluşturur ve bir uyarı günlüğü kaydeder. `add_device.php` topluluk dizesini yazdırır ve gizli bilgileri argüman olarak alır; bu bilgiler her çağrı çalışırken Kadupul sunucusunun işlem listesinde görünür.

`add_device.php` yinelenenler ve hatalar için 1 ile çıkar; betik devam eder, hataları sayar ve herhangi bir cihaz eklenmediyse 1 ile çıkar. Şablon kimlikleri `php cli/add_device.php --list-host-templates` komutundan gelir. `export` çıkış kodları: `0` yazıldı, `2` okunamayan girdi, `--allow-partial` olmadan tamamlanmamış tarama veya güvenli biçimde dışa aktarılamayan veri, `1` betik yazılamadı.

## Sürümleme ve yayın süreci

hostcensus [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standartlarını izler: uyumlu
düzeltmeler yama sürümünü, uyumlu özellikler/kullanımdan kaldırmalar alt
sürümü ve uyumluluğu bozan değişiklikler ana sürümü artırır.
Komutlar ve seçenekler, çıkış kodları ve JSON şemaları genel sözleşmeyi oluşturur;
bir güvenlik düzeltmesi daha erken değiştirmeyi gerektirmediği sürece (bu durumda değişiklik günlüğü nedenini açıklar)
kullanımdan kaldırılan davranışlar bir sonraki ana sürüme kadar çalışmaya devam eder.

release-please, `main` üzerindeki Conventional Commit başlıklarından bir sürüm PR'ı açarak
`pyproject.toml`, `uv.lock` ve `CHANGES.md` dosyalarını günceller. Bu PR'ın birleştirilmesi
`vMAJOR.MINOR.PATCH` etiketini ve bir taslak GitHub sürümünü oluşturur; CI buna test edilmiş bir
wheel, kaynak dağıtımı ve sağlama toplamları ekler; GitHub ise attestations API'si aracılığıyla bu dosyalar için
derleme onayları saklar. Dosyalar eklendikten sonra bir bakımcı taslağı inceler ve
yayımlar. Sürümler asla değiştirilmez.

PyPI güvenilir yayımlama isteğe bağlıdır ve proje sahipliği, güvenilir bir
yayıncı ve `pypi` ortamını gerektirir. Yeniden derlemeden veya bir API belirteci saklamadan
aynı kontrol edilmiş sürüm yapılarını yayımlar. Bu herkese açık depodaki etiketlenmiş sürümler
GitHub yapı onayları üretir; özel çatallar desteklenen bir plan ve açık onay gerektirir.
Kurulum, tam komutlar ve yeniden denemeler için
[eksiksiz sürüm kılavuzuna](../../../docs/releasing.md) bakın.

## Geliştirme

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Geliştirme araçları `pyproject.toml` içindeki [PEP 735](https://peps.python.org/pep-0735/) bağımlılık
gruplarında (`dev`, `fuzz`, `build`) yer alır, bu nedenle yayımlanan paket meta verilerinde asla görünmezler.
`uv.lock` tek kilit dosyasıdır; CI `uv sync --locked` ile kurulum yapar ve kilit dosyası güncelliğini yitirdiğinde
başarısız olur. Yorumlayıcıyı `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) veya herhangi bir
Python 3.12+ ile seçin.

CI, %90 paket kapsama tabanı uygular. Birim testleri kontrollü loopback
sunucularını ve çevrimdışı profil/geçmiş/sürüm doğrulayıcı senaryolarını içerir; Compose laboratuvarı
yalıtılmış bir köprü üzerinde OpenSSH, MariaDB, nginx ve net-snmp çalıştırır.
`make test-integration` ile çalıştırın. Bkz. [CONTRIBUTING.md](../../../CONTRIBUTING.md) ve
[sürüm araçları](../../../scripts/README.md).

Çalışma zamanı kapsayıcısı ev dizini, kabuk oturumu ve pip olmadan UID/GID 10001 olarak çalışır
ve `/app/output` dizinine yazabilir. Bağlanan herhangi bir çıktı dizini için bu kullanıcıya
yazma erişimi verin. Hiçbir yetenek gerektirmez ve salt okunur kök dosya sistemiyle çalışır,
bu nedenle şu şekilde çalıştırılabilir:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap bu kapsayıcıda ayrıcalıksız TCP keşif davranışını kullanır. CI, Trivy'nin bildirdiği
düzeltilebilir herhangi bir HIGH veya CRITICAL güvenlik açığında imaj derlemesini başarısız kılar.

## Tedarik zinciri kontrolleri

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
main dalında ve haftalık olarak çalışır, gerçek puanını yayımlar ve bulguları GitHub
kod taramasına yükler. Actions ve kapsayıcı tabanları değişmez karmalarla sabitlenmiştir; Python
bağımlılıkları `uv.lock` içinde çözümlenir. Bandit hataları CI'ı başarısız kılar ve sınırlandırılmış Atheris
fuzz testi SSH, MySQL, HTTP, sertifika ve SNMPv3 BER ayrıştırıcılarını
ağ erişimi olmadan çalıştırır.

Scorecard ayrıca geçmiş inceleme etkinliğini, katkıda bulunan çeşitliliğini ve
sürüm kökenini de ölçer. Bu puanlar gerçek kanıtları yansıtır; her yönetişim veya
geçmiş sürüm kontrolünün karşılandığı iddiası değildir. Bkz.
[SECURITY.md](../../../SECURITY.md) ve [sürüm kökeni](../../../docs/releasing.md).

## Yerelleştirme

CLI iletileri ve terminal özet/diff tabloları, sıfır ek çalışma zamanı bağımlılığıyla 45 yerel ayarı (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) destekler. Çözümleme sırasıyla `--lang`, ardından `LC_ALL`, `LC_MESSAGES` ve `LANG` değerlerini dikkate alır ve `en` ayarına geri döner. JSON şemaları, CSV sütunları ve dışa aktarma betikleri tüm yerel ayarlarda değişmeden kalır.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Katkıda bulunma

Katkılar yeniden üretilebilir bir örnek içermeli, belgelenen CLI ve
veri biçimi sözleşmelerini korumalı ve yukarıdaki kalite kontrollerinden geçmelidir. Geliştirme iş akışı için
[CONTRIBUTING.md](../../../CONTRIBUTING.md) ve uyumluluk ile sürümleme kararları için
[sürüm kılavuzu](../../../docs/releasing.md) belgelerine bakın.

## Güvenlik ve lisans durumu

Özel bildirimler ve desteklenen sürümler için [SECURITY.md](../../../SECURITY.md) belgesine bakın.
hostcensus [MIT Lisansı](../../../LICENSE) altında lisanslanmıştır.

Kaynak üstbilgileri SPDX tanımlayıcılarını kullanır ve Git geçmişinden gelen katkıda bulunan
emeğini korur. Atıf için [AUTHORS.md](../../../AUTHORS.md) belgesine bakın. İkili test yakalamaları ve
oluşturulan kilit dosyası bitişik `.license` dosyalarını kullanır; MIT metni `LICENSES/MIT.txt` içindedir.
