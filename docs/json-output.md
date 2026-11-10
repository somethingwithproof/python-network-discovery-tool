<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# JSON output

Every JSON document hostcensus writes is an object with a `format` name and an
integer `version`. A JSON Schema (draft 2020-12) for each one ships inside the
package under `hostcensus/schemas/` and is tested against real command output.

| `format` | Written by | Schema |
| --- | --- | --- |
| `hostcensus-report` | `scan -o FILE.json`, or `scan --format json` on stdout | `report-v1.schema.json` |
| `hostcensus-snapshot` | `scan --save-snapshot FILE` | `snapshot-v1.schema.json` |
| `hostcensus-diff` | `diff OLD NEW -f json` | `diff-v1.schema.json` |
| `hostcensus-preflight` | `preflight` | `preflight-v1.schema.json` |
| `hostcensus-history` | `history` | `history-v1.schema.json` |
| `hostcensus-compare` | `compare BEFORE AFTER` | `compare-v1.schema.json` |

`common-v1.schema.json` holds the device, service and scan-envelope
definitions that the others reference.

Load a schema from an installed package:

```python
import json
from importlib.resources import files

schema = json.loads(files("hostcensus").joinpath("schemas/report-v1.schema.json").read_text())
```

## Reports and snapshots

Reports and snapshots share one envelope: `hostcensus_version` (`netprobe_version` in files written before the rename), `created` (UTC,
ISO 8601), `target`, `complete`, the probed `services` with their port, protocol, probe and
timeout, the scan `timeout` and `backend`, and `devices`. A report lists every
scanned device. A snapshot lists only devices that answered or had a probe
fail, so that `diff` can tell a failed observation from a vanished host.
`complete` is false only in a report from a scan stopped by `--deadline`; its
`devices` then lists just the hosts that finished, and no snapshot is written. `diff` and `export` refuse such a report unless `--allow-partial` is given.

Each device keeps the original `ip`, `alive`, `ssh`, `snmp`, `mysql`,
`hostname` and `errors` fields, the `services` it probed with their `state`
(`open`, `closed`, `filtered` or `unknown`), and `address`, the address every
probe used. `ip` is the target as given, so for a hostname target it is the
name; an IPv4-mapped IPv6 target (`::ffff:a.b.c.d`) is recorded as the IPv4
address it reaches.

`diff` and `export` read reports, snapshots, and the bare device lists that
hostcensus 2.x wrote. Files are untrusted input: `diff`, `export` and `compare`
refuse a device whose `ip` is not an address or hostname in the form hostcensus
writes (exit 2, or 1 for history), and `diff` and `export` strip control
characters from hostnames, service names, versions and settings before use.

Documents written before the project was renamed carry `netprobe-` format names
(`netprobe-report`, `netprobe-snapshot`, and so on). The schemas accept both
spellings, `diff` and `export` still load old reports and snapshots, and new
files use `hostcensus-`. The old spelling is dropped in the next major release.

## Stability

Within one `version`, hostcensus only adds optional fields. Removing or renaming
a field, changing its type or meaning, or adding a required field produces a
new `version` and a new schema file, and is a breaking change released in a
new major version (see the versioning policy in the README). Consumers should
check `format` and `version` and ignore fields they do not know; the published
schemas allow unknown properties for the same reason, so a document from a later
minor release still validates against the schema of its `version`.

The terminal table and log messages are for people and may change in any
release; use the JSON documents for automation.
