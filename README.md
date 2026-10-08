# netprobe

[![CI configuration](https://img.shields.io/badge/CI-configured-blue)](./.github/workflows/ci.yml)
[![Python requirement](https://img.shields.io/badge/Python_requirement-%3E%3D3.12-blue)](./pyproject.toml)

netprobe finds hosts on a network you administer, identifies the services they run from what those services announce before login, records the result as JSON, CSV or a snapshot, reports what changed between two snapshots, and turns an inventory into a script that adds the devices to [Kadupul](https://github.com/kadupulhq/kadupul).

It runs as an ordinary user with plain asyncio sockets. nmap is optional and only used for host discovery.

## Install

Python 3.12 or newer is required. From this checkout:

```bash
uv venv
uv pip install -e .            # add '.[nmap]' for --backend nmap (also needs the nmap binary)
.venv/bin/netprobe --help
```

## Quick example

Run from the tester container of the integration lab described under Development; output trimmed:

```console
$ netprobe scan 172.30.57.8/29 --services ssh,http,snmp --save-snapshot after.json
┃ IP Address   ┃ Hostname       ┃ SSH ┃ SNMP ┃ MySQL ┃ Open services  ┃ Status ┃
│ 172.30.57.10 │ netprobe-it-s… │ ✅  │  ❌  │  ❌   │ ssh:22         │ UP     │
│              │                │     │      │       │ OpenSSH_10.0   │        │
│ 172.30.57.13 │ netprobe-it-w… │ ❌  │  ❌  │  ❌   │ http:80        │ UP     │
│              │                │     │      │       │ nginx/1.28.3   │        │

$ netprobe diff before.json after.json; echo "exit=$?"
Warning: targets differ: 172.30.57.10 vs 172.30.57.8/29
│ new host │ 172.30.57.13 │ http:80/tcp  │ netprobe-it-web-1.netprobe-it_lab   │
exit=3

$ netprobe export after.json -o kadupul-import.sh --template 1
$ grep 57.13 kadupul-import.sh
add --description=netprobe-it-web-1.netprobe-it_lab --ip=172.30.57.13 --template=1 --version=0 --avail=ping --ping_method=tcp --ping_port=80 '--notes=netprobe: http:80/tcp nginx/1.28.3'
```

## Exit codes

| Command | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| `scan` | success | nmap backend unavailable, or a report/snapshot could not be written | invalid target, option or config, or a scan over the size limits | |
| `diff` | no changes | `-o` file could not be written | missing, unreadable or unsupported input | changes found |
| `export` | script written | script could not be written | unreadable input, or data that cannot be exported safely | |

## Layout

`src/netprobe/` holds `cli.py` (Typer commands), `scanner.py` (target expansion, host discovery, limits), `probes.py` (one function per service type and the `PROBES` table), `config.py` (default services and TOML loading), `models.py`, `output.py` (table, JSON, CSV), `diff.py` (snapshots and comparison) and `export.py` (Kadupul script).

## Usage

Scan only networks you administer.

```bash
netprobe scan 192.168.1.0/24              # table of alive hosts
netprobe scan 192.168.1.1 -o results.json # JSON report
netprobe scan 10.0.0.0/24 -o report.csv   # CSV report
netprobe scan 10.0.0.0/24 -q -o out.json  # no table, file only
```

| Option | Meaning |
| --- | --- |
| `NETWORK` | CIDR range, IP address, or hostname. Ranges over 65536 addresses are rejected. |
| `-o, --output PATH` | Write a report. The format follows the extension (`.json`, `.csv`); other extensions fall back to JSON. |
| `-f, --format json\|csv\|kadupul\|auto` | Force the report format. Has no effect without `--output`. `.sh` selects `kadupul`. |
| `-v, --verbose` | Debug logging. |
| `-q, --quiet` | Suppress the results table. |
| `--backend asyncio\|nmap` | Host discovery. `asyncio` (default) probes the service ports directly; `nmap` runs an nmap ping sweep first and needs `pip install 'netprobe[nmap]'` plus the `nmap` binary. |
| `--timeout SECONDS` | Wait per probe (default 1.0). |
| `--concurrency N` | Probes in flight at once (default 256). |
| `--config PATH` | TOML file whose `[services]` table adds or replaces services. |
| `--services NAMES` | Comma list of service names to check, in that order (default: all). |
| `--ports SPEC` | Comma list of `NAME=PORT` (move a service) or `PORT` (add a plain TCP check named `tcp-PORT`). |
| `--snmp-community` | SNMPv2c community for the system MIB query. Env: `NETPROBE_SNMP_COMMUNITY`. |
| `--snmp-user` | SNMPv3 user. Env: `NETPROBE_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key` | `MD5`, `SHA` (default), `SHA224`, `SHA256`, `SHA384`, `SHA512` and the passphrase. Env: `NETPROBE_SNMP_AUTH_PROTOCOL`, `NETPROBE_SNMP_AUTH_KEY`. |
| `--snmp-priv-protocol`, `--snmp-priv-key` | `DES`, `AES` (default), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` and the passphrase. Env: `NETPROBE_SNMP_PRIV_PROTOCOL`, `NETPROBE_SNMP_PRIV_KEY`. |
| `--save-snapshot PATH` | Also write a versioned snapshot for `netprobe diff`. |
| `--tls-ca-file PATH` | Verify HTTPS certificates against this PEM bundle instead of the system store. Env: `NETPROBE_TLS_CA_FILE`. |

By default each host is checked for SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) and HTTPS (TCP 443). TCP ports are tested with a full connect. SNMP is tested with an SNMPv3 engine-discovery request, which any SNMPv3 agent must answer without credentials; agents that only speak v1/v2c will not be detected by this probe. With the asyncio backend a host counts as alive when any probe gets an answer, including a refused connection, so a host that drops every probe is reported down. With `--backend nmap`, nmap decides which hosts are alive (ICMP as root, TCP 80/443 otherwise).

### Fingerprints

Each open service is fingerprinted from what it sends before any login. Nothing authenticates except the SNMP query, and only when you supply credentials.

| Probe | Reads | `version` | `details` keys |
| --- | --- | --- | --- |
| `ssh` | RFC 4253 identification line | software, e.g. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | MySQL/MariaDB initial handshake | server version | `server_version`, `flavor`, `auth_plugin`, or `error_code`/`error` |
| `http` | `HEAD /` response | `Server` header | `status`, `server` |
| `https` | TLS handshake, certificate, `HEAD /` | `Server` header | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | SNMPv3 discovery; with credentials, GET of sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; with credentials `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, or `snmp_error` |

HTTPS certificates are verified first, against the system store or `--tls-ca-file`. If verification fails, the failure is recorded in `cert_verified: false` and `cert_verify_error`, and the certificate is then read over an unverified connection so it can still be inventoried; such results carry `cert_read_unverified: true`. Nothing is sent over that connection except the `HEAD` request.

SNMP credentials are read from options or environment variables. Prefer the environment variables: command-line values are visible to other local users in the process list. Credentials are never logged or written to any output. A community selects SNMPv2c; a user selects SNMPv3, with authentication when an auth key is given and privacy when both keys are given (`snmp_security_level` records which). netprobe refuses, with exit code 2, to combine a community with a v3 user, to use a privacy key without an auth key, or to use keys without a user, and it never retries a failed v3 query with v2c or a lower security level. Passing a secret as an option logs a warning naming the matching environment variable. Agents that only speak v1/v2c ignore the credential-free v3 discovery, so they show as open only when a community is supplied.

Banner text is reduced to printable characters and capped at 256 characters before it is stored or shown. Reads are bounded too: 4 KiB per line, 4 KiB for a MySQL greeting, 16 KiB of HTTP headers.

### Limits

One run accepts at most 65,536 addresses, 64 services, and 524,288 probes (hosts times services); larger requests exit with code 2 before anything is sent. `--concurrency` is capped at 4096 sockets. Every probe, including the nmap-backend and SNMP paths, has a hard deadline of four times `--timeout`; a probe that hits it is reported as `filtered` with "probe timed out" in `errors`.

### Configuring services

Services can be changed with a TOML file:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` is one of `tcp`, `ssh`, `mysql`, `http`, `https` or `snmp` and defaults to the service name when that is a probe, else `tcp`. Only `snmp` uses UDP. Service names are lowercase letters, digits, `-` and `_`.

Results keep the original `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` and `errors` fields and add a `services` list with each probe's `name`, `port`, `protocol`, `state` (`open`, `closed` or `filtered`), `version` and `details`. CSV output gains trailing `services` and `versions` columns for the open ones. The `ssh`, `snmp` and `mysql` booleans follow the services with exactly those names.


## Inventory profiles, preflight, and local history

Named profiles share a TOML file with the existing `[services]` definitions. Copy
[netprobe.example.toml](netprobe.example.toml) to `netprobe.toml` and set networks
that you administer:

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
netprobe profiles --config netprobe.toml
netprobe preflight --profile office --config netprobe.toml
netprobe scan --profile office --config netprobe.toml -o report.json
```

Profiles accept `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency`, and `max_hosts`. `services` and `ports` use the existing comma-list
syntax. Explicit CLI options override profile settings; repeated `--exclude`
options add to profile exclusions. An explicit network with `--profile` must be
contained in that profile's IP/CIDR scope. Hostnames remain supported for direct
scans, but cannot be combined with IP exclusions. Host limits apply before
exclusions; the total probe cap still applies afterward. Excluded hosts are
omitted from both service checks and optional Nmap discovery.

Every scan performs local preflight checks before target traffic: target/probe
limits, destination access, optional Nmap executable/wrapper availability, history
schema, and a configured TLS CA bundle. `preflight` reports JSON and does not scan
targets or create a history database. It temporarily writes a sibling file to test
destination access without changing existing contents. The default asyncio backend
still requires neither Nmap nor root. Destination paths must be distinct from each
other and the input configuration, including hard links; destination symlinks are
rejected. Failed checks return 1; invalid scope/configuration returns 2.

History is opt-in and complements the existing JSON snapshots and `diff` command:

```bash
mkdir -p output
netprobe scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
netprobe scan --profile office --history output/inventory.sqlite3
netprobe history --history output/inventory.sqlite3 --limit 20
netprobe compare 1 2 --history output/inventory.sqlite3
netprobe compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Use IDs from `history`; the example assumes a new database. Snapshots are stored
transactionally with UTC start/end times, package version, effective non-secret
settings, summaries, and all host/service observations, including per-host errors.
Incomplete host observations are retained. Cancelled runs are not saved. Existing
report, snapshot, export, and scan exit-code contracts are preserved.

`history` lists JSON summaries without reading all historical device payloads.
`compare` reads two saved scans, requires identical target identities and selected
ports, and reports responsiveness, status, and port-state changes. The earlier
scan ID must precede the later ID. Scanner errors and unknown port observations
are flagged as uncertain rather than treated as confirmed disappearance or closure.
`no_longer_responding` means lack of a response, not proof of device removal.
Comparison success returns 0 whether or not changes exist; existing file `diff`
retains its exit code 3 contract. Unsupported or corrupt history returns 1.

History stores inventory information, so choose an appropriately protected local
directory. Profile files and stored settings do not contain SNMP credentials;
credential handling continues through the existing runtime options/environment.

## Inventory diff

```bash
netprobe scan 10.0.0.0/24 -q --save-snapshot monday.json
netprobe scan 10.0.0.0/24 -q --save-snapshot tuesday.json
netprobe diff monday.json tuesday.json             # table
netprobe diff monday.json tuesday.json -f json     # JSON on stdout
```

A snapshot is JSON with `format: "netprobe-snapshot"`, `version: 1`, the netprobe version, the UTC creation time, the target, the services that were probed, and the alive hosts in the same shape as the `-o` report. Down hosts are left out. `diff` also accepts plain `scan -o` JSON reports, including ones from before the `services` field existed.

`diff` reports new and vanished hosts, ports that opened or closed on hosts present in both, and services whose `version` changed. Ports that were probed in only one of the two scans are not compared, and a warning says so; a warning also appears when the targets differ. `-o PATH` writes the JSON form to a file as well.

`diff` exit codes: `0` no changes, `3` changes found, `2` a file is missing, unreadable or not a supported snapshot, `1` the `-o` file could not be written.

## Kadupul export

[Kadupul](https://github.com/kadupulhq/kadupul) (a fork of Cacti 1.2.31) has no bulk device file import. Its supported way to add devices from a script is `cli/add_device.php`, one device per call, with `--option=value` arguments. `netprobe export` writes a POSIX `sh` script of those calls:

```bash
netprobe scan 10.0.0.0/24 -q --save-snapshot inventory.json
netprobe export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: netprobe scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export NETPROBE_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Each alive host becomes `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hosts where the scan's SNMP query succeeded get `--version=2 --community=...` or `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` for authPriv), `--port` and `--avail=snmp`. SNMPv3 export needs `--snmp-user`, and noAuthNoPriv is refused because `add_device.php` requires a v3 password.
- Other hosts get `--version=0 --avail=ping`, with `--ping_method=tcp --ping_port=` the first open TCP port, or ICMP if none.
- `--notes` lists the open services and versions. `--description` is the reverse-DNS name when it is plain (letters, digits, `.`, `_`, `-`), else the IP, and is made unique, because `add_device.php` treats an existing description as an update to that device.

Every value is validated and shell-quoted with `shlex.quote`. By default no SNMP secret is written: the script expands `NETPROBE_SNMP_COMMUNITY`, `NETPROBE_SNMP_AUTH_KEY` or `NETPROBE_SNMP_PRIV_KEY` at run time and stops if one is unset. `--include-credentials` writes the values from those environment variables into the script instead, creates it with mode 0600, and logs a warning. `add_device.php` itself prints the community and receives secrets as arguments, which are visible in the Kadupul server's process list while each call runs.

`add_device.php` exits 1 for duplicates and errors; the script continues, counts failures, and exits 1 if any device was not added. Template ids come from `php cli/add_device.php --list-host-templates`. `export` exit codes: `0` written, `2` unreadable input or data that cannot be exported safely, `1` the script could not be written.

## Development

```bash
uv pip install -e ".[dev]"
make lint        # ruff check, ruff format --check, mypy (strict)
make test        # unit tests with coverage; CI fails under 90%
```

Integration tests run against a docker compose lab (OpenSSH, MariaDB, nginx with a self-signed certificate, net-snmp) on the private subnet 172.30.57.0/24, from a tester container on the same network: `make test-integration`. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [release scripts](scripts/README.md) for other workflows.

## Security and license status

See [SECURITY.md](SECURITY.md). Package metadata declares MIT, but this checkout has no `LICENSE` file. Confirm the intended license grant before redistribution.
