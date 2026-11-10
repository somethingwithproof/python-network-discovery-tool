# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Every JSON document netprobe writes validates against its published schema."""

import json
from importlib.resources import files
from unittest.mock import MagicMock, patch

import pytest
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource
from typer.testing import CliRunner

from netprobe import cli
from netprobe.config import DEFAULT_SERVICES
from netprobe.diff import write_snapshot
from netprobe.models import Device, Service

SCHEMAS = {
    path.name: json.loads(path.read_text())
    for path in files("netprobe").joinpath("schemas").iterdir()
    if path.name.endswith(".schema.json")
}


def composed_targets(schemas):
    """(file, JSON pointer) of every subschema that is only used through allOf."""
    targets = set()
    for name, schema in schemas.items():
        for part in schema.get("allOf", []):
            ref = part.get("$ref", "")
            path, _, pointer = ref.partition("#")
            targets.add((path or name, pointer))
    return targets


def closed(node, name, pointer, skip):
    """Copy of a schema that rejects every property it does not declare.

    The published schemas accept unknown fields so that an additive change does
    not break consumers; the tests use closed copies so a field netprobe writes
    without documenting it fails here instead. unevaluatedProperties sees through
    allOf, so composed parts are left open and their composite is closed.
    Objects whose schema says additionalProperties: true stay open.
    """
    if isinstance(node, list):
        return [closed(item, name, f"{pointer}/{i}", skip) for i, item in enumerate(node)]
    if not isinstance(node, dict):
        return node
    copy = {key: closed(value, name, f"{pointer}/{key}", skip) for key, value in node.items()}
    if "properties" in copy and "additionalProperties" not in copy and (name, pointer) not in skip:
        copy["unevaluatedProperties"] = False
    return copy


def registry(schemas):
    return Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )


PUBLISHED = registry(SCHEMAS)
CLOSED_SCHEMAS = {
    name: closed(schema, name, "", composed_targets(SCHEMAS)) for name, schema in SCHEMAS.items()
}
CLOSED = registry(CLOSED_SCHEMAS)
runner = CliRunner()


def validator(name, *, published=False):
    """Closed validator by default; published=True uses the shipped schema."""
    schemas, store = (SCHEMAS, PUBLISHED) if published else (CLOSED_SCHEMAS, CLOSED)
    return Draft202012Validator(
        schemas[f"{name}-v1.schema.json"],
        registry=store,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


def devices():
    up = Device(
        "10.0.0.1",
        alive=True,
        ssh=True,
        hostname="web.example",
        services=[
            Service("ssh", 22, "tcp", "open", "OpenSSH_10.0", {"protocol": "2.0"}),
            Service("http", 80, "tcp", "unknown"),
        ],
        address="10.0.0.1",
    )
    down = Device("10.0.0.2", errors=["Host is down"], address="10.0.0.2")
    return [up, down]


def scan(tmp_path, *args):
    scanner = MagicMock()

    async def scan_network(network, progress=None):
        return devices()

    scanner.scan_network = scan_network
    with patch.object(cli, "NetworkScanner", return_value=scanner):
        return runner.invoke(cli.app, ["scan", "10.0.0.0/30", *args])


def test_every_schema_is_valid_and_ids_are_unique():
    assert sorted(SCHEMAS) == [
        f"{name}-v1.schema.json"
        for name in ("common", "compare", "diff", "history", "preflight", "report", "snapshot")
    ]
    for schema in SCHEMAS.values():
        Draft202012Validator.check_schema(schema)
    assert len({schema["$id"] for schema in SCHEMAS.values()}) == len(SCHEMAS)


def test_report_file_matches_schema(tmp_path):
    out = tmp_path / "report.json"
    result = scan(tmp_path, "-o", str(out))
    assert result.exit_code == 0, result.output
    document = json.loads(out.read_text())
    validator("report").validate(document)
    assert [d["ip"] for d in document["devices"]] == ["10.0.0.1", "10.0.0.2"]


def test_report_on_stdout_is_one_json_document(tmp_path):
    result = scan(tmp_path, "--format", "json")
    assert result.exit_code == 0, result.output
    validator("report").validate(json.loads(result.stdout))


def test_snapshot_matches_schema(tmp_path):
    path = tmp_path / "snap.json"
    write_snapshot(path, "10.0.0.0/30", DEFAULT_SERVICES, devices(), timeout=1.0, backend="asyncio")
    document = json.loads(path.read_text())
    validator("snapshot").validate(document)
    assert [d["ip"] for d in document["devices"]] == ["10.0.0.1"]


def test_diff_output_matches_schema(tmp_path):
    old, new = tmp_path / "old.json", tmp_path / "new.json"
    first = devices()
    second = devices()
    second[0].services = [Service("ssh", 22, "tcp", "unknown"), Service("http", 80, "tcp", "open")]
    write_snapshot(old, "10.0.0.0/30", DEFAULT_SERVICES, first)
    write_snapshot(new, "10.0.0.0/30", DEFAULT_SERVICES, [*second, Device("10.0.0.3", alive=True)])
    result = runner.invoke(cli.app, ["diff", str(old), str(new), "-f", "json"])
    assert result.exit_code == 3, result.output
    document = json.loads(result.stdout)
    validator("diff").validate(document)
    # The run must exercise the lists the schema constrains most tightly.
    assert document["unconfirmed"]
    assert document["opened"]
    assert document["new_hosts"]


@pytest.mark.parametrize("name", ["report", "snapshot", "diff"])
def test_schemas_reject_an_unknown_version(name):
    check = validator(name)
    check.validate({**_minimal(name), "version": 1})
    newer = {**_minimal(name), "version": 2}
    with pytest.raises(ValidationError, match="1 was expected"):
        check.validate(newer)


@pytest.mark.parametrize("name", ["report", "snapshot", "diff"])
def test_published_schemas_accept_fields_added_later(name):
    """Adding an optional field is not a new version, so v1 consumers must accept it."""
    document = {**_minimal(name), "version": 1, "added_in_a_minor_release": True}
    validator(name, published=True).validate(document)
    closed_check = validator(name)
    with pytest.raises(ValidationError, match="added_in_a_minor_release"):
        closed_check.validate(document)


def test_date_time_formats_are_checked():
    document = {**_minimal("report"), "version": 1, "created": "yesterday"}
    check = validator("report")
    with pytest.raises(ValidationError, match="is not a 'date-time'"):
        check.validate(document)


def _minimal(name):
    if name == "diff":
        side = {"source": "", "created": "", "target": ""}
        lists = ["new_hosts", "vanished_hosts", "opened", "closed", "version_changes"]
        lists += ["unsettled_hosts", "unconfirmed", "warnings"]
        return {"format": "netprobe-diff", "changed": False, "old": side, "new": side} | {
            key: [] for key in lists
        }
    return {
        "format": f"netprobe-{name}",
        "netprobe_version": "0",
        "created": "2026-01-01T00:00:00+00:00",
        "target": "10.0.0.1",
        "services": [],
        "devices": [],
    }


def test_preflight_output_matches_schema():
    result = runner.invoke(cli.app, ["preflight", "127.0.0.1", "--services", "ssh"])
    assert result.exit_code == 0, result.output
    validator("preflight").validate(json.loads(result.stdout))


def test_history_and_compare_output_match_schemas(tmp_path):
    store = tmp_path / "history.sqlite3"
    for _ in range(2):
        result = scan(tmp_path, "-q", "--history", str(store))
        assert result.exit_code == 0, result.output
    listed = runner.invoke(cli.app, ["history", "--history", str(store)])
    assert listed.exit_code == 0, listed.output
    listing = json.loads(listed.stdout)
    validator("history").validate(listing)
    assert [scan_["id"] for scan_ in listing["scans"]] == [2, 1]

    compared = runner.invoke(cli.app, ["compare", "1", "2", "--history", str(store)])
    assert compared.exit_code == 0, compared.output
    report = json.loads(compared.stdout)
    validator("compare").validate(report)
    assert report["unconfirmed_ports"]  # http was unknown in both scans
