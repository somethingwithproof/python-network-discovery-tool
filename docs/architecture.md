<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Architecture

netprobe is one asyncio process. A scan runs these stages in order, and each
one either finishes or ends the run with a documented exit code before the next
starts:

1. **Plan** (`cli.py`). Command-line options, a named profile and the TOML
   service table are merged into one `ScanPlan`; options given on the command
   line win over the profile. SNMP secrets are read here, only from
   `NETPROBE_SNMP_*` variables or the files named by `--snmp-*-file`.
2. **Preflight** (`preflight.py`). Local checks only: the target parses and fits
   the host and probe limits, nmap exists when that backend is chosen, output and
   history paths are writable, the TLS CA bundle loads, and the open-file limit
   covers `--concurrency`. `netprobe preflight` runs the same function and
   prints the result. Nothing has been sent at this point.
3. **Expand** (`scanner.py`). The target becomes an ordered address list.
   Expansion is refused before any list is built if the range exceeds
   `--max-hosts`, and exclusions are applied afterwards.
4. **Discover** (optional). With `--backend nmap`, one `nmap -sn` process (or
   one per batch of 256 when there are exclusions) is run directly, without a
   shell, and its XML is read with a size cap and parsed with defusedxml.
5. **Probe** (`scanner.py`, `probes.py`). A fixed pool of workers takes hosts
   from the list. Each host's probes share a semaphore of `--concurrency` slots.
   Hostname targets are resolved once and every probe connects to that address.
   Reverse DNS runs in at most 16 threads at a time.
6. **Report** (`output.py`, `history.py`, `diff.py`, `export.py`). Results are
   rendered as a table, a versioned JSON document, CSV or a Kadupul script, and
   can be recorded as a snapshot and in SQLite history.

`diff`, `compare`, `history` and `export` read files or the history database
and never send traffic.

## Bounds

Every stage that touches the network or reads remote data has a limit, so a
large range or an unresponsive network cannot make a run grow without bound:

| What | Limit |
| --- | --- |
| Whole scan, nmap sweep included | `--deadline`, default 3600 s; partial report, exit 4 |
| One probe | four times its timeout, then reported `unknown` |
| Reverse DNS | 2 s per lookup, 16 lookups at once |
| nmap | 30 s per host; 35 s per 256 addresses per process; 64 MiB of XML |
| Hosts, services, probes | 65,536 hosts, 64 services, 524,288 probes per run |
| Sockets | `--concurrency`, default 256, at most 4096 |
| Data read from a service | 4 KiB banner lines and MySQL packets, 16 KiB of HTTP headers |
| Text stored from a service | 256 characters per field, non-printable characters replaced |

The README's Limits section explains how these interact with `--timeout` and
per-service timeouts.

## Trust boundaries

- **Remote services are untrusted.** Everything read from the network goes
  through a bounded parser in `probes.py` (SSH banner, MySQL handshake, HTTP
  headers, X.509 certificate, SNMPv3 BER) and is cleaned before it is stored.
  Atheris fuzzes those parsers in CI and Hypothesis property tests cover the BER
  walker. TLS observations require certificate and hostname verification.
- **The local user is trusted, the command line is not private.** Secrets never
  come from options, because other local users can read a process's arguments.
  Reports, history databases and scripts are created owner-only and are never
  written through a symbolic link.
- **Generated scripts quote every value.** `export` validates names and
  addresses and quotes each argument for `/bin/sh`. Credentials stay as
  environment references unless `--include-credentials` is given.
- **Tools are run directly.** nmap is found on `PATH` and run with an argument
  list. Targets that could be read as options (a leading `-`) or contain
  whitespace are rejected for every backend.

## Results and uncertainty

Each service observation is `open`, `closed`, `filtered` or `unknown`. `unknown`
means netprobe could not tell, for example because the probe timed out or a
local socket error occurred; it never means "down". `diff` and `compare` share
one port classification (`scan_settings.port_transition`): a port open in the
later scan is reported as opened, and any other transition with an `unknown`
side is unconfirmed, never "no change". A scan stopped by
`--deadline` writes no snapshot or history, because the hosts it never reached
would otherwise look vanished.

## Modules

| Module | Responsibility |
| --- | --- |
| `cli.py` | Commands, option and profile resolution, secret loading, orchestration |
| `scan_settings.py` | Shared settings, host ordering, port-transition classification and settings-difference warnings |
| `preflight.py` | Local checks before traffic |
| `scanner.py` | Target validation and expansion, nmap discovery, workers, deadlines |
| `probes.py` | Protocol probes and their parsers |
| `config.py`, `profiles.py` | Service definitions and named profiles |
| `models.py`, `output.py` | Result types, versioned JSON, CSV and table output |
| `diff.py`, `history.py` | Snapshot comparison and SQLite history |
| `export.py` | Kadupul `add_device.php` scripts |
| `schemas/` | JSON Schemas for every JSON document netprobe writes |
