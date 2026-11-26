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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · **Español** · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus es una CLI en Python para realizar inventarios repetibles de servicios en redes que administras.
Registra lo que exponen los dispositivos, compara observaciones a lo largo del tiempo y genera
scripts de importación para Kadupul. El backend predeterminado utiliza sockets de asyncio sin privilegios de root;
el descubrimiento opcional con Nmap permite identificar hosts más allá de los puertos de servicio configurados.

## Por qué hostcensus

Un informe puntual de puertos no explica si la siguiente observación cambió o
simplemente falló. hostcensus combina estados de servicio explícitos, sondeos acotados, perfiles
de escaneo reutilizables e historial local. Los operadores pueden repetir el mismo alcance, inspeccionar
errores y distinguir las observaciones inciertas de los cambios confirmados.

- **Evidencia de servicios:** identificación SSH, saludos de MySQL, encabezados HTTP, observaciones de
  certificados TLS y descubrimiento SNMP o consultas system-MIB con credenciales.
- **Alcance repetible:** perfiles TOML con nombre, exclusiones aditivas, servicios
  configurables, límites de hosts/sondeos y trabajadores acotados.
- **Comprobaciones antes de generar tráfico:** la verificación previa local valida destinos, herramientas, acceso
  al destino, esquema del historial y paquetes de CA TLS configurados.
- **Historial de inventario:** las instantáneas transaccionales en SQLite conservan todas las observaciones;
  las comparaciones mantienen visibles los fallos del escáner y los estados desconocidos.
- **Salida interoperable:** informes de terminal, JSON y CSV, instantáneas de archivo versionadas
  y scripts de importación para Kadupul.

CI cubre Python 3.12, 3.13 y 3.14 en Linux y macOS, además de un laboratorio de integración
controlado con Compose. El código utiliza alias de tipos modernos, resultados tipados de verificación previa,
perfiles con slots y argumentos solo de palabra clave, y limpieza asíncrona estructurada manteniendo esas
versiones de ejecución. Consulta [Versionado y publicaciones](../../../docs/releasing.md) para ver el contrato de compatibilidad SemVer
y el proceso de publicación en GitHub. La insignia de publicación describe los
artefactos publicados, no la copia local: la última etiqueta publicada es actualmente
`v0.3.0`, mientras que esta copia local usa la versión de paquete `3.0.0`. Instala desde la copia local
para usar las funciones de inventario aquí documentadas.

Comienza con la [instalación](#install) y luego revisa [perfiles e historial](#inventory-profiles-preflight-and-local-history).
Para detalles de integración, consulta [huellas de servicios](#fingerprints),
[comparación de archivos](#inventory-diff) y [exportación a Kadupul](#kadupul-export).

## Instalación

Se requiere Python 3.12 o superior; la matriz probada es Python 3.12–3.14. Desde esta
copia local, instala las dependencias de ejecución bloqueadas:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Para el descubrimiento opcional de hosts con Nmap, instala el ejecutable de Nmap mediante el gestor
de paquetes de tu plataforma; no se necesita ningún paquete adicional de Python. La salida XML de Nmap se analiza con
defusedxml, una dependencia principal, por lo que se rechaza la expansión de entidades. hostcensus ejecuta
directamente el binario `nmap` encontrado en `PATH` con una lista fija de argumentos, un plazo límite que crece
con el tamaño del prefijo y un tope de salida de 64 MiB. Nmap no es necesario para el backend predeterminado.

## Migración desde netprobe

hostcensus es el nuevo nombre de netprobe, lanzado en la versión 3.0.0. El proyecto nunca se
publicó en PyPI bajo ninguno de los dos nombres, por lo que las instalaciones provenían de una copia local o de una publicación
en GitHub. El repositorio de GitHub mantiene su nombre.

| Antes | Ahora | Compatibilidad |
| --- | --- | --- |
| Distribución `netprobe` | `hostcensus` | Reinstala desde la copia local; no existe un paquete con el nombre anterior. |
| Comando `netprobe` | `hostcensus` | `netprobe` sigue ejecutándose e imprime una línea de obsolescencia en stderr. Los códigos de salida y stdout no cambian. Se eliminará en la próxima versión principal. |
| Variables de entorno `NETPROBE_*` | `HOSTCENSUS_*` | Se usa una variable `NETPROBE_*` cuando su equivalente `HOSTCENSUS_*` no está definida, con una advertencia en stderr que nombra las variables y nunca sus valores. `HOSTCENSUS_*` prevalece cuando ambas están definidas. Se eliminará en la próxima versión principal. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Cambio incompatible.** No se instala ningún adaptador de importación; actualiza las importaciones. |
| Etiqueta de imagen Docker `network-discovery:test` (solo CI) y usuario de contenedor `netprobe` | `hostcensus:test`, usuario `hostcensus` | Nunca se publicó ninguna imagen en un registro. Vuelve a compilar la imagen y usa el punto de entrada `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Un archivo existente con el nombre predeterminado anterior se sigue usando, con una advertencia, mientras el nuevo nombre no exista. Las rutas explícitas `--config` y `--history` no se modifican. |
| Informes e instantáneas con `"format": "netprobe-report"` o `"netprobe-snapshot"`, y el campo `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` y `export` siguen cargando archivos escritos con el nombre anterior, y los esquemas JSON publicados aceptan ambas grafías. Los archivos nuevos usan los nombres nuevos. Las bases de datos de historial SQLite no cambian y se cargan como antes. |
| Scripts de Kadupul generados con `netprobe export` | Scripts generados con `hostcensus export` | Los scripts antiguos siguen funcionando y continúan leyendo `NETPROBE_SNMP_*` al ejecutarse. Los scripts nuevos leen `HOSTCENSUS_SNMP_*`. |

## Ejemplo rápido

Ejecutado desde el contenedor de pruebas del laboratorio de integración descrito en Desarrollo; salida recortada:

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

## Códigos de salida

| Comando | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | observaciones/informe registrados | fallo de verificación previa/backend, historial o escritura de informe/instantánea | destino, opciones, configuración o límites no válidos | - | se alcanzó `--deadline`; se escribió informe parcial, se omitieron el historial y la instantánea |
| `preflight` | comprobaciones superadas | falló una comprobación local | destino/configuración no válidos o destinos en conflicto | - | - |
| `profiles` | perfiles validados listados | - | configuración o selección ilegible o no válida | - | - |
| `history` | resúmenes listados | historial ausente, no válido o no compatible | opciones de CLI no válidas | - | - |
| `compare` | comparación generada, incluso cuando existen cambios | historial ilegible, alcance/orden incompatible o fallo de escritura | opciones de CLI no válidas | - | - |
| `diff` | sin cambios | no se pudo escribir el archivo `-o` | entrada ausente, ilegible o no compatible, o un escaneo incompleto sin `--allow-partial` | cambios encontrados, observaciones sin confirmar o escaneo incompleto | - |
| `export` | script escrito | no se pudo escribir el script | entrada ilegible, un escaneo incompleto sin `--allow-partial`, o datos que no pueden exportarse de forma segura | - | - |

## Estructura

| Módulo | Responsabilidad |
| --- | --- |
| `cli.py` | Opciones de comando, resolución de perfiles, verificación previa, escaneo e informes |
| `scanner.py`, `probes.py` | Expansión de destinos, trabajadores acotados, descubrimiento de hosts y observaciones de servicios |
| `config.py`, `profiles.py` | Definiciones de servicios y perfiles de inventario validados |
| `models.py`, `output.py` | Tipos de resultado y renderizado en terminal/JSON/CSV |
| `history.py`, `diff.py` | Historial en SQLite y comparaciones de instantáneas de archivo versionadas |
| `preflight.py` | Comprobaciones locales y consulta acotada de versión de Nmap |
| `export.py` | Scripts de importación para Kadupul validados y con comillas seguras |

Cada observación de servicio registra su estado por separado de su identidad anunciada.
Las lecturas y los plazos límite están acotados; las excepciones de sondeo permanecen en los errores del host. El historial
SQLite utiliza transacciones, limpieza explícita de conexiones y rutas de solo lectura para listar y
comparar. Los secretos SNMP entran únicamente mediante variables de entorno o archivos de
secretos; el historial de inventario almacena la configuración efectiva no secreta. Consulta
[Arquitectura](../../../docs/architecture.md) para conocer el flujo de escaneo, sus límites y fronteras de
confianza, y [SECURITY.md](../../../SECURITY.md#authorized-use) para el uso autorizado.


## Uso

Escanea únicamente redes que administres.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opción | Significado |
| --- | --- |
| `NETWORK` | CIDR, IP o nombre de host; opcional con `--profile`. Se rechazan los identificadores de ámbito IPv6. |
| `-o, --output PATH` | Escribe un informe. El formato sigue la extensión (`.json`, `.csv`); otras extensiones recurren a JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Fuerza el formato del informe. No tiene efecto sin `--output`. `.sh` selecciona `kadupul`. |
| `-v, --verbose` | Registro de depuración. |
| `-q, --quiet` | Suprime resultados, progreso y registros informativos; las advertencias y errores siguen apareciendo en stderr. |
| `--backend asyncio\|nmap` | Descubrimiento de hosts. `asyncio` (predeterminado) sondea directamente los puertos de servicio; `nmap` ejecuta primero un barrido ping con nmap y requiere el ejecutable `nmap` en `PATH`. |
| `--timeout SECONDS` | Tiempo de espera para sondeos que no establecen su propio presupuesto (predeterminado 1.0). Los sondeos de conexión integrados usan 0.3s a menos que la tabla de servicios establezca `timeout`. |
| `--concurrency N` | Sondeos simultáneos en curso (predeterminado 256). |
| `--deadline SECONDS` | Detiene todo el escaneo, incluido el barrido de nmap, tras este tiempo (predeterminado 3600, máximo 604800; variable de entorno `HOSTCENSUS_DEADLINE`). Los hosts finalizados se escriben en el informe con `"complete": false`, no se escribe historial ni instantánea y `scan` sale con código 4. |
| `--config PATH` | Definiciones de servicios en TOML y configuración opcional de `[profiles]` con nombre. |
| `--profile NAME` | Usa un perfil con nombre; toma `hostcensus.toml` de forma predeterminada cuando se omite `--config`. |
| `--exclude IP/CIDR` | Agrega una exclusión; repítelo según sea necesario. Un host IPv4 excluido también excluye las direcciones IPv6 que lo alcanzan: IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) y 6to4. Los destinos y exclusiones IPv4-mapped se tratan como las direcciones IPv4 que representan. |
| `--max-hosts N` | Límite de direcciones comprobado antes de las exclusiones (predeterminado y máximo estricto 65,536). |
| `--history PATH` | Registra el escaneo completado en una base de datos de historial SQLite opcional. |
| `--services NAMES` | Lista separada por comas de nombres de servicio a comprobar, en ese orden (predeterminado: todos). |
| `--ports SPEC` | Lista separada por comas de `NAME=PORT` (mover un servicio) o `PORT` (agregar una comprobación TCP simple llamada `tcp-PORT`). |
| `--snmp-community-file PATH` | Archivo que contiene la comunidad SNMPv2c para la consulta del MIB del sistema. Env: `HOSTCENSUS_SNMP_COMMUNITY` (el valor) o `HOSTCENSUS_SNMP_COMMUNITY_FILE` (la ruta). |
| `--snmp-user` | Usuario SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (predeterminado), `SHA224`, `SHA256`, `SHA384`, `SHA512` y un archivo con la frase de paso. Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` o `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (predeterminado), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` y un archivo con la frase de paso. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` o `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Escribe además una instantánea versionada para `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifica los certificados HTTPS contra este paquete PEM en lugar del almacén del sistema. Env: `HOSTCENSUS_TLS_CA_FILE`. |

De forma predeterminada, en cada host se comprueban SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) y HTTPS (TCP 443). Los puertos TCP se prueban con una conexión completa. SNMP se prueba con una solicitud de descubrimiento de motor SNMPv3, a la que cualquier agente SNMPv3 debe responder sin credenciales; los agentes que solo hablan v1/v2c no serán detectados por este sondeo. Con el backend asyncio, un host se considera activo cuando cualquier sondeo obtiene respuesta, incluida una conexión rechazada, de modo que un host que descarta todos los sondeos tiene `alive=false` y el error "Host is down"; esto no demuestra que esté apagado físicamente. Con `--backend nmap`, nmap decide qué hosts están activos (ICMP como root, TCP 80/443 en caso contrario).

### Huellas de servicios

Cada servicio abierto se identifica a partir de lo que envía antes de cualquier inicio de sesión. Nada se autentica excepto la consulta SNMP, y solo cuando proporcionas credenciales.

| Sondeo | Lee | `version` | Claves de `details` |
| --- | --- | --- | --- |
| `ssh` | línea de identificación RFC 4253 | software, p. ej. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | saludo inicial de MySQL/MariaDB | versión del servidor | `server_version`, `flavor`, `auth_plugin`, o `error_code`/`error` |
| `http` | respuesta `HEAD /` | encabezado `Server` | `status`, `server` |
| `https` | negociación TLS, certificado, `HEAD /` | encabezado `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (ISO 8601 UTC), `cert_self_signed`, `status`, `server` |
| `snmp` | descubrimiento SNMPv3; con credenciales, GET de sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; con credenciales `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name` o `snmp_error` |

Un destino especificado por nombre de host se resuelve una vez por host y cada sondeo se conecta a esa dirección, registrada como `address` en los resultados; el nombre se usa únicamente para TLS SNI, verificación del certificado y el encabezado HTTP `Host`. Un nombre que no se resuelve produce estados `unknown` y un error `Cannot resolve`. Los nombres de DNS inverso se conservan solo cuando contienen caracteres válidos de nombre de host, y se ejecutan como máximo 16 consultas a la vez. HTTPS utiliza verificación de certificado y nombre de host contra el almacén del sistema o `--tls-ca-file`. El almacén de confianza se carga una vez para el escaneo y se reutiliza en cada sondeo HTTPS. La conexión TCP y el saludo TLS se cronometran por separado, de modo que un puerto que acepta conexiones pero detiene el saludo TLS queda como `open` con `tls_error`, no como `filtered`. Si la verificación falla, el resultado registra `cert_verified: false` y `cert_verify_error`; no reintenta con ajustes más débiles ni envía una solicitud HTTP. Los detalles del certificado y los encabezados HTTP se recopilan solo tras completarse con éxito la verificación. Proporciona el paquete de CA correcto para servicios con CA privada. Los informes antiguos pueden contener `cert_read_unverified`, que los sondeos actuales ya no generan.

Los secretos SNMP se leen únicamente desde variables de entorno o desde archivos (`--snmp-*-file`, o la variable `HOSTCENSUS_SNMP_*_FILE` correspondiente), nunca desde valores en la línea de comandos, que otros usuarios locales pueden ver en la lista de procesos. `--snmp-community`, `--snmp-auth-key` y `--snmp-priv-key` con un valor terminan con código de salida 2 e indican el reemplazo. Un archivo de secreto debe contener UTF-8 no vacío de como máximo 4096 bytes; se ignora un salto de línea final, y configurar tanto una variable como un archivo para el mismo secreto es un error. Los errores nombran el archivo pero nunca imprimen su contenido. Los informes de escaneo y el historial no incluyen intencionadamente valores de credenciales. El exportador tiene una opción separada y explícita `--include-credentials` descrita más adelante. Una comunidad selecciona SNMPv2c; un usuario selecciona SNMPv3, con autenticación cuando se proporciona una clave de autenticación y privacidad cuando se proporcionan ambas claves (`snmp_security_level` registra cuál se usó). hostcensus rechaza, con código de salida 2, combinar una comunidad con un usuario v3, usar una clave de privacidad sin una clave de autenticación o usar claves sin un usuario, y nunca reintenta una consulta v3 fallida con v2c ni con un nivel de seguridad inferior. Los agentes que solo hablan v1/v2c ignoran el descubrimiento v3 sin credenciales, por lo que aparecen como abiertos únicamente cuando se proporciona una comunidad.

El texto de los banners se reduce a caracteres imprimibles y se limita a 256 caracteres antes de almacenarse o mostrarse. Las lecturas también están acotadas: 4 KiB por línea, 4 KiB para un saludo de MySQL, 16 KiB de encabezados HTTP. Un ID de motor SNMP de más de 32 octetos se trunca antes de almacenarse. HTTP y HTTPS envían un encabezado Host con la dirección IPv6 entre corchetes y con el puerto cuando no es 80 ni 443. Las celdas CSV que comienzan con un disparador de fórmula de hoja de cálculo reciben un prefijo para que la celda siga siendo texto.

### Límites

Una ejecución acepta como máximo 65,536 direcciones, 64 servicios y 524,288 sondeos (hosts por servicios); las solicitudes mayores salen con código 2 antes de enviar nada. `--concurrency` tiene un tope de 4096 sockets. Cada sondeo tiene un plazo límite estricto de cuatro veces su propio presupuesto. Los sondeos de conexión (`tcp`, `ssh`, `mysql`, `http`) usan 0.3 segundos salvo que ese servicio establezca `timeout`. SNMP y HTTPS usan `--timeout` (predeterminado 1.0) cuando no fijan uno. Un sondeo que alcanza el plazo límite se notifica como `unknown` con "probe timed out" en `errors`. Los fallos locales de socket (por ejemplo, quedarse sin descriptores de archivo) también quedan como `unknown` con el error registrado; nunca cuentan como puerto filtrado ni como host inactivo. Antes de sondear, hostcensus eleva el límite blando de archivos abiertos hacia el límite estricto para dar cabida a `--concurrency` más 64 descriptores; cuando no puede hacerlo, la comprobación previa `open files` falla y `scan` sale con código 1 antes de enviar tráfico. El descubrimiento con Nmap usa un tiempo de espera de host de 30 segundos. Un prefijo se pasa a nmap en formato CIDR, y un barrido falla con salida 1 cuando nmap informa menos direcciones de las que recibió (por ejemplo, un nombre que no puede resolver) en lugar de marcar hosts como inactivos. Un destino especificado por nombre de host se resuelve una vez y se pasa esa dirección a nmap, de modo que el descubrimiento y los sondeos alcanzan la misma máquina. Un prefijo completo corresponde a un proceso nmap cuyo plazo límite de subproceso es de 35 segundos por cada 256 direcciones, redondeado hacia arriba. Los barridos con exclusiones usan lotes de 256 hosts y un plazo límite de 35 segundos por lote. La creación de trabajadores está acotada con independencia del tamaño del rango. El DNS inverso y la resolución de nombres de host tienen un plazo límite separado de dos segundos; una llamada al resolvedor que nunca retorna se abandona en su propio hilo, por lo que no puede mantener a hostcensus ejecutándose más allá de estos límites. Como máximo se ejecutan 16 consultas a la vez, y una llamada abandonada conserva su ranura hasta que retorna, de modo que el número de hilos bloqueados permanece acotado; si los 16 se quedan colgados, las consultas posteriores esperan en cola por una ranura fuera del plazo límite de dos segundos (que comienza cuando una ranura queda libre) hasta que `--deadline` detiene el escaneo. `NetworkScanner` usado como biblioteca sin `deadline` puede esperar indefinidamente por una de estas ranuras. `--deadline` (una hora por defecto) acota toda la ejecución por encima de estos límites.

### Configuración de servicios

Los servicios pueden modificarse con un archivo TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` es uno de `tcp`, `ssh`, `mysql`, `http`, `https` o `snmp`, y toma por defecto el nombre del servicio cuando este coincide con un sondeo, o `tcp` en caso contrario. Solo `snmp` usa UDP. Los nombres de servicio se componen de letras minúsculas, dígitos, `-` y `_`. Dos servicios no pueden compartir puerto y protocolo; el historial registra un único estado para ese par. `timeout` es opcional, en segundos, y al menos 0.05. Los sondeos de tipo conexión (`tcp`, `ssh`, `mysql`, `http`) usan 0.3 segundos por defecto. `snmp` y `https` usan el `--timeout` del escaneo cuando el servicio no establece `timeout`. `--timeout` no reemplaza un presupuesto que el servicio ya tenga definido.

Los informes JSON son documentos versionados (`"format": "hostcensus-report"`, `"version": 1`) que registran el destino, los servicios sondeados y la configuración junto a `devices`; `--format json` sin `-o` escribe el informe en stdout en lugar de la tabla. Cada salida JSON tiene un esquema publicado; consulta [Salida JSON](../../../docs/json-output.md). Los dispositivos conservan los campos originales `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` y `errors` y añaden una lista `services` con `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, o `unknown` cuando el sondeo falló localmente o alcanzó su plazo límite), `version` y `details` de cada sondeo. La salida CSV añade las columnas finales `services` y `versions` para los que están abiertos. Los booleanos `ssh`, `snmp` y `mysql` corresponden a los servicios con exactamente esos nombres.


## Perfiles de inventario, verificación previa e historial local

Los perfiles con nombre comparten un archivo TOML con las definiciones `[services]` existentes. Copia
[hostcensus.example.toml](../../../hostcensus.example.toml) a `hostcensus.toml` y configura redes
que administres:

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

`preflight` resuelve opciones y perfiles exactamente igual que `scan`, incluido
`--concurrency` para la comprobación de archivos abiertos, por lo que una verificación previa superada significa que `scan`
iniciará con el mismo plan.

Los perfiles aceptan `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` y `max_hosts`. `services` y `ports` usan la sintaxis existente de lista separada por comas. Las opciones explícitas de la CLI anulan la configuración del perfil; las opciones `--exclude` repetidas
se suman a las exclusiones del perfil. Una red explícita con `--profile` debe estar
contenida en el alcance IP/CIDR de ese perfil. Los nombres de host siguen siendo compatibles para escaneos
directos, pero no pueden combinarse con exclusiones IP. Los límites de hosts se aplican antes de las
exclusiones; el tope total de sondeos sigue aplicándose después. Los hosts excluidos se
omiten tanto en las comprobaciones de servicios como en el descubrimiento opcional con Nmap.

Cada escaneo realiza comprobaciones locales previas antes de enviar tráfico al destino: límites de destino/sondeo,
acceso de destino, disponibilidad opcional del ejecutable/envoltorio de Nmap, esquema del historial
y un paquete de CA TLS configurado. `preflight` informa en JSON y no escanea
destinos ni crea una base de datos de historial. Escribe temporalmente un archivo hermano para probar
el acceso al destino sin alterar el contenido existente. El backend predeterminado asyncio
sigue sin requerir Nmap ni privilegios de root. Las rutas de destino deben ser distintas entre
sí y respecto a la configuración de entrada, incluidos los enlaces duros; los enlaces simbólicos de destino se
rechazan. Las comprobaciones fallidas devuelven 1; un alcance o configuración no válidos devuelven 2.

Las escrituras de informes y exportaciones requieren soporte de `O_NOFOLLOW`. En plataformas sin él,
incluido Windows, estas escrituras fallan sin abrir ni truncar el destino.
Los informes y scripts de exportación nuevos son solo para el propietario (modo 0600); reemplazar un archivo existente conserva sus
permisos. Escribir en una tubería con nombre sin lector falla de inmediato en lugar de esperar. Una nueva base de datos `--history` también se crea solo para el propietario; una existente conserva su modo. Los mensajes de registro van siempre a stderr, por lo que stdout solo transporta resultados. Las exportaciones que contienen credenciales siempre fuerzan el modo 0600.

El historial es opcional y complementa las instantáneas JSON existentes y el comando `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Usa los ID de `history`; el ejemplo supone una base de datos nueva. Las instantáneas se almacenan
de forma transaccional con marcas de tiempo UTC de inicio/fin, versión del paquete, configuración efectiva no secreta,
resúmenes y todas las observaciones de hosts/servicios, incluidos los errores por host.
Las observaciones incompletas de hosts se conservan. Las ejecuciones canceladas no se guardan. Se preservan los
contratos existentes de códigos de salida para informe, instantánea, exportación y escaneo.

`history` lista resúmenes JSON sin leer todas las cargas históricas de dispositivos.
`compare` lee dos escaneos guardados, exige identidades de destino y puertos seleccionados idénticos,
e informa cambios de respuesta, estado y estado de puertos. El ID del escaneo anterior
debe preceder al ID posterior. Cuando ambos escaneos registraron `timeout` o `backend`
y esos valores difieren, el informe incluye una advertencia y aun así compara las
observaciones. Un tiempo de espera distinto puede hacer que un puerto filtrado parezca abierto. Los errores del escáner
y las observaciones de puertos desconocidos se marcan como inciertos en lugar de tratarse como
desaparición o cierre confirmados: los hosts con errores aparecen en `uncertain_hosts`, y
cada transición de puerto que involucre `unknown` (incluido unknown en ambos escaneos) se lista
en `unconfirmed_ports` en lugar de `port_changes`, salvo un puerto que esté abierto en el
escaneo posterior, que sí es un cambio de puerto. `compare` y `diff` clasifican los puertos con la misma regla.
`no_longer_responding` significa ausencia de respuesta, no prueba de retirada del dispositivo.
Un código de salida 0 en el escaneo no garantiza que todos los hosts respondieran: inspecciona los errores por host. Una comparación exitosa devuelve 0 existan o no cambios; el comando de archivos `diff` existente
mantiene su contrato de código de salida 3. Un historial no compatible o dañado devuelve 1.

El historial almacena información de inventario, por lo que debes elegir un directorio local
adecuadamente protegido. Los archivos de perfil y la configuración almacenada no contienen credenciales SNMP;
el manejo de credenciales continúa realizándose mediante las opciones de ejecución o el entorno existentes.

## Diferencias de inventario

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Una instantánea es un JSON con `format: "hostcensus-snapshot"`, `version: 1`, la versión de hostcensus, la hora de creación en UTC, el destino, los valores `timeout` y `backend` del escaneo cuando este los registró, los servicios sondeados y los hosts activos con la misma estructura que el informe `-o`. Los hosts inactivos se omiten. `diff` también acepta informes JSON simples de `scan -o`, incluidos los generados antes de que existiera el campo `services`.

`diff` informa hosts nuevos y desaparecidos, puertos que se abrieron o cerraron en hosts presentes en ambos escaneos y servicios cuya `version` cambió. Los puertos sondeados en solo uno de los dos escaneos no se comparan, y una advertencia lo indica. Las observaciones fallidas nunca se interpretan como "sin cambios": un puerto que sea `unknown` en cualquiera de los dos escaneos y no esté abierto en el posterior se lista bajo `unconfirmed`, no en `closed`, con `before` igual a `open`, `unknown` o `not-open` (sondeado y cerrado o filtrado) y `after` igual a `unknown` o `not-open`; un puerto que ahora está abierto se informa en `opened` incluso si el sondeo anterior falló. Un host cuyos sondeos fallaron todos sin respuesta en alguno de los escaneos se lista en `unsettled_hosts` (con `before`/`after` igual a `up`, `uncertain` o `absent`, incluso cuando falló en ambos escaneos o falta en el otro archivo) en lugar de `vanished_hosts`; si responde en el escaneo posterior, también se informa como host nuevo con sus puertos abiertos. Las instantáneas conservan esos hosts fallidos por este motivo. También aparece una advertencia cuando los destinos difieren y cuando ambos archivos registraron un `timeout` o `backend` y esos valores difieren. `-o PATH` escribe también la forma JSON en un archivo.

Un informe de un escaneo detenido por `--deadline` (`"complete": false`) solo enumera los hosts que alcanzó, por lo que `diff` y `export` lo rechazan con código de salida 2. `--allow-partial` lo acepta con una advertencia en stderr: `diff` lista entonces los hosts que el escaneo incompleto no incluyó en absoluto bajo `unsettled_hosts` como `unscanned` en lugar de desaparecidos (un host listado como inactivo sigue constando como desaparecido), establece `partial` en verdadero y nunca informa ausencia de cambios, y `export` escribe una advertencia en la cabecera del script.

Códigos de salida de `diff`: `0` sin cambios, `3` cambios encontrados, observaciones que no pudieron confirmarse o una entrada incompleta (`changed` es verdadero siempre que cualquier lista, incluidas `unsettled_hosts` y `unconfirmed`, no esté vacía, o `partial` sea verdadero), `2` falta un archivo, es ilegible, no es una instantánea compatible o está incompleto sin `--allow-partial`, `1` no se pudo escribir el archivo `-o`.

## Exportación a Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (una bifurcación de Cacti 1.2.31) no dispone de importación masiva de dispositivos desde archivo. Su forma compatible de añadir dispositivos desde un script es `cli/add_device.php`, un dispositivo por llamada, con argumentos `--option=value`. `hostcensus export` escribe un script `sh` POSIX con esas llamadas:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Cada host activo se convierte en `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Los hosts donde la consulta SNMP del escaneo tuvo éxito obtienen `--version=2 --community=...` o `--version=3 --username=... --authproto=... --password=...` (además de `--privproto`/`--privpass` para authPriv), `--port` y `--avail=snmp`. La exportación SNMPv3 necesita `--snmp-user`, y se rechaza noAuthNoPriv porque `add_device.php` requiere una contraseña v3.
- Los demás hosts obtienen `--version=0 --avail=ping`, con `--ping_method=tcp --ping_port=` del primer puerto TCP abierto, o ICMP si no hay ninguno.
- `--notes` enumera los servicios abiertos y sus versiones. `--description` es el nombre de DNS inverso cuando es simple (letras, dígitos, `.`, `_`, `-`), o la IP en caso contrario, y se hace único, porque `add_device.php` trata una descripción existente como una actualización de ese dispositivo.

Cada valor se valida y se entrecomilla para shell con `shlex.quote`. De forma predeterminada no se escribe ningún secreto SNMP: el script expande `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` o `HOSTCENSUS_SNMP_PRIV_KEY` en tiempo de ejecución y se detiene si alguno no está definido. `--include-credentials` escribe en su lugar los valores de esas variables de entorno en el script, lo crea con modo 0600 y registra una advertencia. El propio `add_device.php` imprime la comunidad y recibe secretos como argumentos, que son visibles en la lista de procesos del servidor Kadupul mientras se ejecuta cada llamada.

`add_device.php` termina con código 1 ante duplicados y errores; el script continúa, cuenta los fallos y termina con código 1 si algún dispositivo no se añadió. Los ID de plantilla provienen de `php cli/add_device.php --list-host-templates`. Códigos de salida de `export`: `0` escrito, `2` entrada ilegible, un escaneo incompleto sin `--allow-partial` o datos que no pueden exportarse de forma segura, `1` no se pudo escribir el script.

## Versionado y proceso de publicación

hostcensus sigue el [Versionado Semántico](https://semver.org/spec/v2.0.0.html): las correcciones
compatibles incrementan la versión de parche, las funciones y obsolescencias compatibles incrementan la
versión menor, y los cambios incompatibles incrementan la versión mayor.
Los comandos y opciones, los códigos de salida y los esquemas JSON constituyen el contrato público;
el comportamiento obsoleto sigue funcionando hasta la próxima versión principal, salvo que una
corrección de seguridad requiera cambiarlo antes (en cuyo caso el registro de cambios explica por qué).

release-please abre un PR de publicación a partir de los títulos de Conventional Commits en `main`,
actualizando `pyproject.toml`, `uv.lock` y `CHANGES.md`. Al fusionarlo se crea la etiqueta
`vMAJOR.MINOR.PATCH` y un borrador de publicación en GitHub, al que CI adjunta un wheel
probado, la distribución de código fuente y sumas de verificación; GitHub almacena atestaciones de compilación para
esos archivos mediante su API de atestaciones. Un mantenedor revisa y publica el
borrador una vez adjuntados los archivos. Las publicaciones nunca se reemplazan.

La publicación de confianza en PyPI es opcional y requiere la titularidad del proyecto, un publicador de
confianza y el entorno `pypi`. Publica los mismos artefactos de publicación verificados
sin recompilar ni almacenar un token de API. Las publicaciones etiquetadas en este repositorio
público generan atestaciones de artefactos en GitHub; las bifurcaciones privadas requieren un plan
compatible y activación explícita. Consulta la
[guía completa de publicación](../../../docs/releasing.md) para ver la configuración, los comandos exactos y los reintentos.

## Desarrollo

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Las herramientas de desarrollo residen en los grupos de dependencias [PEP 735](https://peps.python.org/pep-0735/)
en `pyproject.toml` (`dev`, `fuzz`, `build`), por lo que nunca aparecen en los
metadatos del paquete publicado. `uv.lock` es el único archivo de bloqueo; CI instala con
`uv sync --locked` y falla cuando el archivo de bloqueo está desactualizado. Selecciona el intérprete con
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) o cualquier Python 3.12+.

CI exige un mínimo del 90% de cobertura del paquete. Las pruebas unitarias incluyen servidores
de bucle local controlados y casos sin conexión de perfiles/historial/validador de publicaciones; el laboratorio Compose ejecuta
OpenSSH, MariaDB, nginx y net-snmp en un puente aislado. Ejecútalo con
`make test-integration`. Consulta [CONTRIBUTING.md](../../../CONTRIBUTING.md) y
[herramientas de publicación](../../../scripts/README.md).

El contenedor de ejecución se ejecuta con UID/GID 10001 sin directorio personal, sin shell
de inicio de sesión ni pip, y puede escribir en `/app/output`. Da acceso de escritura a ese usuario en
cualquier directorio de salida montado. No necesita capacidades especiales y funciona con un
sistema de archivos raíz de solo lectura, por lo que puede ejecutarse así:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap utiliza su comportamiento de descubrimiento TCP sin privilegios en este contenedor. CI hace fallar
la compilación de la imagen ante cualquier vulnerabilidad HIGH o CRITICAL corregible que informe Trivy.

## Comprobaciones de la cadena de suministro

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
se ejecuta en main y semanalmente, publica su puntuación real y sube los hallazgos al análisis
de código de GitHub. Las acciones y las bases de contenedores están fijadas por hashes inmutables; las dependencias
de Python se resuelven en `uv.lock`. Los fallos de Bandit hacen fallar CI, y las pruebas de fuzzing acotadas con Atheris
ejercitan los analizadores SSH, MySQL, HTTP, de certificados y SNMPv3 BER
sin acceso a la red.

Scorecard también mide la actividad histórica de revisiones, la diversidad de colaboradores y
la procedencia de las publicaciones. Esas puntuaciones reflejan evidencia real; no constituyen afirmaciones
de que se cumpla cada comprobación de gobernanza o de publicaciones históricas. Consulta
[SECURITY.md](../../../SECURITY.md) y [procedencia de publicaciones](../../../docs/releasing.md).

## Localización

Los mensajes de la CLI y las tablas de resumen/diferencias en terminal admiten 45 configuraciones regionales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) sin dependencias adicionales en tiempo de ejecución. La resolución respeta `--lang`, luego `LC_ALL`, `LC_MESSAGES` y `LANG`, recurriendo a `en` por defecto. Los esquemas JSON, las columnas CSV y los scripts de exportación permanecen sin cambios en todas las configuraciones regionales.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Contribuciones

Las contribuciones deben incluir un caso reproducible, preservar los contratos documentados de CLI y
formato de datos, y superar las comprobaciones de calidad anteriores. Consulta
[CONTRIBUTING.md](../../../CONTRIBUTING.md) para ver el flujo de trabajo de desarrollo y
[la guía de publicación](../../../docs/releasing.md) para decisiones sobre compatibilidad y versionado.

## Seguridad y estado de la licencia

Consulta [SECURITY.md](../../../SECURITY.md) para la notificación privada y las versiones compatibles.
hostcensus se distribuye bajo la [Licencia MIT](../../../LICENSE).

Las cabeceras de código fuente usan identificadores SPDX y conservan los créditos de los colaboradores del historial
de Git. Consulta [AUTHORS.md](../../../AUTHORS.md) para la atribución. Las capturas binarias de prueba y el
archivo de bloqueo generado usan archivos `.license` adyacentes; el texto de la licencia MIT está en `LICENSES/MIT.txt`.
