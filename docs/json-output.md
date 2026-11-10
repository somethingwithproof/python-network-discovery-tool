<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# JSON output

Every JSON document netprobe writes is an object with a `format` name and an
integer `version`. A JSON Schema (draft 2020-12) for each one ships inside the
package under `netprobe/schemas/` and is tested against real command output.

| `format` | Written by | Schema |
| --- | --- | --- |
| `netprobe-report` | `scan -o FILE.json`, or `scan --format json` on stdout | `report-v1.schema.json` |
| `netprobe-snapshot` | `scan --save-snapshot FILE` | `snapshot-v1.schema.json` |
| `netprobe-diff` | `diff OLD NEW -f json` | `diff-v1.schema.json` |
| `netprobe-preflight` | `preflight` | `preflight-v1.schema.json` |
| `netprobe-history` | `history` | `history-v1.schema.json` |
| `netprobe-compare` | `compare BEFORE AFTER` | `compare-v1.schema.json` |

`common-v1.schema.json` holds the device, service and scan-envelope
definitions that the others reference.

Load a schema from an installed package:

```python
import json
from importlib.resources import files

schema = json.loads(files("netprobe").joinpath("schemas/report-v1.schema.json").read_text())
```

## Reports and snapshots

Reports and snapshots share one envelope: `netprobe_version`, `created` (UTC,
ISO 8601), `target`, the probed `services` with their port, protocol, probe and
timeout, the scan `timeout` and `backend`, and `devices`. A report lists every
scanned device. A snapshot lists only devices that answered or had a probe
fail, so that `diff` can tell a failed observation from a vanished host.

Each device keeps the original `ip`, `alive`, `ssh`, `snmp`, `mysql`,
`hostname` and `errors` fields, the `services` it probed with their `state`
(`open`, `closed`, `filtered` or `unknown`), and `address`, the address every
probe used. `ip` is the target as given, so for a hostname target it is the
name.

`diff` and `export` read reports, snapshots, and the bare device lists that
netprobe 2.x wrote.

## Stability

Within one `version`, netprobe only adds optional fields. Removing or renaming
a field, changing its type or meaning, or adding a required field produces a
new `version` and a new schema file, and is a breaking change released in a
new major version (see the versioning policy in the README). Consumers should
check `format` and `version` and ignore fields they do not know; the published
schemas allow unknown properties for the same reason, so a document from a later
minor release still validates against the schema of its `version`.

The terminal table and log messages are for people and may change in any
release; use the JSON documents for automation.
