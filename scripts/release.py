#!/usr/bin/env python3
"""Prepare and validate releases without committing, tagging, or publishing."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from email.parser import Parser
from pathlib import Path
from typing import Literal
from zipfile import BadZipFile, ZipFile

_NUMBER = r"(0|[1-9][0-9]*)"
_SEMVER = re.compile(rf"^{_NUMBER}\.{_NUMBER}\.{_NUMBER}(?:-(alpha|beta|rc)\.{_NUMBER})?$")
_PACKAGE = re.compile(rf"^{_NUMBER}\.{_NUMBER}\.{_NUMBER}(?:(a|b|rc){_NUMBER})?$")
type Bump = Literal["major", "minor", "patch"]


@dataclass(frozen=True, slots=True)
class ReleaseVersion:
    major: int
    minor: int
    patch: int
    phase: str | None = None
    serial: int = 0

    @property
    def semantic(self) -> str:
        core = f"{self.major}.{self.minor}.{self.patch}"
        return f"{core}-{self.phase}.{self.serial}" if self.phase else core

    @property
    def package(self) -> str:
        core = f"{self.major}.{self.minor}.{self.patch}"
        suffix = {"alpha": "a", "beta": "b", "rc": "rc"}
        return f"{core}{suffix[self.phase]}{self.serial}" if self.phase else core

    @property
    def tag(self) -> str:
        return f"v{self.semantic}"

    @property
    def precedence(self) -> tuple[int, int, int, int, int]:
        rank = {"alpha": 0, "beta": 1, "rc": 2, None: 3}
        return self.major, self.minor, self.patch, rank[self.phase], self.serial


def parse_version(value: str, *, package: bool = False) -> ReleaseVersion:
    match = (_PACKAGE if package else _SEMVER).fullmatch(value)
    if match is None:
        raise ValueError(
            "Use MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-{alpha,beta,rc}.N; no leading zeros or build metadata"
        )
    major, minor, patch, phase, serial = match.groups()
    if package:
        phase = {"a": "alpha", "b": "beta", "rc": "rc", None: None}[phase]
    return ReleaseVersion(int(major), int(minor), int(patch), phase, int(serial or 0))


def project_version(root: Path) -> ReleaseVersion:
    document = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    return parse_version(document["project"]["version"], package=True)


def next_version(current: ReleaseVersion, bump: Bump) -> ReleaseVersion:
    if bump == "major":
        return ReleaseVersion(current.major + 1, 0, 0)
    if bump == "minor":
        return ReleaseVersion(current.major, current.minor + 1, 0)
    return ReleaseVersion(current.major, current.minor, current.patch + 1)


def release_notes(changelog: str, version: ReleaseVersion) -> str:
    heading = (
        rf"^## Version {re.escape(version.semantic)} \([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}\)\s*\n"
    )
    match = re.search(heading, changelog, re.MULTILINE)
    if match is None:
        raise ValueError(f"CHANGES.md needs a dated Version {version.semantic} section")
    body = changelog[match.end() :]
    following = re.search(r"^## ", body, re.MULTILINE)
    notes = body[: following.start()] if following else body
    if not notes.strip():
        raise ValueError("Release notes must not be empty")
    return notes.strip() + "\n"


def _replace_project_version(text: str, value: str) -> str:
    section = re.search(r"^\[project\]\s*\n.*?(?=^\[|\Z)", text, re.MULTILINE | re.DOTALL)
    if section is None:
        raise ValueError("Missing [project] metadata")
    replacement, count = re.subn(
        r'^version\s*=\s*["\'][^"\']+["\']',
        f'version = "{value}"',
        section.group(),
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError("Expected one project version assignment")
    return text[: section.start()] + replacement + text[section.end() :]


def _replace_lock_version(text: str, value: str) -> str:
    entries = list(
        re.finditer(
            r"^\[\[package\]\]\s*\n.*?(?=^\[\[package\]\]|\Z)", text, re.MULTILINE | re.DOTALL
        )
    )
    matches = [
        entry for entry in entries if re.search(r'^name = "netprobe"$', entry.group(), re.MULTILINE)
    ]
    if len(matches) != 1:
        raise ValueError("uv.lock must contain exactly one netprobe entry")
    entry = matches[0]
    replacement, count = re.subn(
        r'^version = "[^"]+"', f'version = "{value}"', entry.group(), count=1, flags=re.MULTILINE
    )
    if count != 1:
        raise ValueError("Missing netprobe lockfile version")
    return text[: entry.start()] + replacement + text[entry.end() :]


def prepare(root: Path, version: ReleaseVersion, *, dry_run: bool = False) -> list[str]:
    current = project_version(root)
    if version.precedence <= current.precedence:
        raise ValueError(f"New version must be greater than {current.semantic}")
    check_lock(root, current)
    project = (root / "pyproject.toml").read_text(encoding="utf-8")
    lock = (root / "uv.lock").read_text(encoding="utf-8")
    changelog = (root / "CHANGES.md").read_text(encoding="utf-8")
    match = re.search(r"^## Unreleased\s*\n(.*?)(?=^## |\Z)", changelog, re.MULTILINE | re.DOTALL)
    if match is None or not match.group(1).strip():
        raise ValueError("Add nonempty release notes under ## Unreleased first")
    if re.search(rf"^## Version {re.escape(version.semantic)}(?: |$)", changelog, re.MULTILINE):
        raise ValueError("That release already has a changelog section")
    date = datetime.now(UTC).date().isoformat()
    section = (
        f"## Unreleased\n\n## Version {version.semantic} ({date})\n\n{match.group(1).strip()}\n\n"
    )
    changes = {
        "pyproject.toml": _replace_project_version(project, version.package),
        "uv.lock": _replace_lock_version(lock, version.package),
        "CHANGES.md": changelog[: match.start()] + section + changelog[match.end() :],
    }
    # Calculate and validate every replacement before writing any file.
    parse_version(tomllib.loads(changes["pyproject.toml"])["project"]["version"], package=True)
    tomllib.loads(changes["uv.lock"])
    release_notes(changes["CHANGES.md"], version)
    if not dry_run:
        for filename, content in changes.items():
            (root / filename).write_text(content, encoding="utf-8")
    return list(changes)


def check_lock(root: Path, version: ReleaseVersion) -> None:
    document = tomllib.loads((root / "uv.lock").read_text(encoding="utf-8"))
    packages = [entry for entry in document["package"] if entry["name"] == "netprobe"]
    if len(packages) != 1 or packages[0]["version"] != version.package:
        raise ValueError("Package version and uv.lock disagree")


def check_release(
    root: Path, tag: str | None = None, previous: str | None = None
) -> ReleaseVersion:
    version = project_version(root)
    check_lock(root, version)
    if tag is not None and tag != version.tag:
        raise ValueError(f"Tag must be {version.tag} for package {version.package}")
    if (
        previous is not None
        and version.precedence < parse_version(previous, package=True).precedence
    ):
        raise ValueError("Package version must not move backwards")
    changelog = (root / "CHANGES.md").read_text(encoding="utf-8")
    pending = re.search(r"^## Unreleased\s*\n(.*?)(?=^## |\Z)", changelog, re.MULTILINE | re.DOTALL)
    if tag is not None and pending is not None and pending.group(1).strip():
        raise ValueError("Move Unreleased notes into a new version section before tagging")
    release_notes(changelog, version)
    return version


def check_distributions(directory: Path, version: ReleaseVersion) -> list[Path]:
    wheels, sources = sorted(directory.glob("*.whl")), sorted(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sources) != 1:
        raise ValueError("Expected exactly one wheel and one source distribution")
    wheel, source = wheels[0], sources[0]
    if (
        not wheel.name.startswith(f"netprobe-{version.package}-")
        or source.name != f"netprobe-{version.package}.tar.gz"
    ):
        raise ValueError("Distribution filenames disagree with the release version")
    with ZipFile(wheel) as archive:
        metadata = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(metadata) != 1:
            raise ValueError("Wheel must contain exactly one metadata document")
        wheel_info = Parser().parsestr(archive.read(metadata[0]).decode("utf-8"))
    with tarfile.open(source, "r:gz") as archive:
        prefix = f"netprobe-{version.package}"
        metadata_file = archive.extractfile(f"{prefix}/PKG-INFO")
        project_file = archive.extractfile(f"{prefix}/pyproject.toml")
        if metadata_file is None or project_file is None:
            raise ValueError("Source distribution metadata is missing")
        source_info = Parser().parsestr(metadata_file.read().decode("utf-8"))
        project = tomllib.loads(project_file.read().decode("utf-8"))
    for info in (wheel_info, source_info):
        if info["Name"] != "netprobe" or info["Version"] != version.package:
            raise ValueError("Distribution metadata disagrees with release")
    if project["project"]["version"] != version.package:
        raise ValueError("Source project version disagrees with release")
    return [wheel, source]


def write_checksums(files: list[Path], output: Path) -> None:
    lines = []
    for path in files:
        with path.open("rb") as stream:
            lines.append(f"{hashlib.file_digest(stream, 'sha256').hexdigest()}  {path.name}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_checksums(files: list[Path], source: Path) -> None:
    entries = source.read_text(encoding="utf-8").splitlines()
    expected = {}
    for entry in entries:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", entry)
        if match is None or match[2] in expected:
            raise ValueError("Invalid checksum manifest")
        expected[match[2]] = match[1]
    if set(expected) != {path.name for path in files}:
        raise ValueError("Checksums must cover exactly the release distributions")
    for path in files:
        with path.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != expected[path.name]:
                raise ValueError(f"Checksum mismatch: {path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_command = commands.add_parser(
        "prepare", help="Prepare version, lockfile and changelog for a reviewed PR"
    )
    prepare_command.add_argument(
        "version", help="major, minor, patch, or an explicit SemVer release"
    )
    prepare_command.add_argument("--dry-run", action="store_true")
    check_command = commands.add_parser(
        "check", help="Validate metadata, notes and optional tag/distributions"
    )
    check_command.add_argument("--tag")
    check_command.add_argument("--previous-version")
    check_command.add_argument("--dist", type=Path)
    check_command.add_argument("--notes", type=Path)
    check_command.add_argument("--checksums", type=Path)
    check_command.add_argument("--verify-checksums", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            current = project_version(args.root)
            version = (
                next_version(current, args.version)
                if args.version in ("major", "minor", "patch")
                else parse_version(args.version)
            )
            changed = prepare(args.root, version, dry_run=args.dry_run)
            print(
                json.dumps(
                    {
                        "version": version.package,
                        "tag": version.tag,
                        "files": changed,
                        "dry_run": args.dry_run,
                    }
                )
            )
        else:
            version = check_release(args.root, args.tag, args.previous_version)
            if args.notes:
                args.notes.write_text(
                    release_notes((args.root / "CHANGES.md").read_text(encoding="utf-8"), version),
                    encoding="utf-8",
                )
            if args.dist:
                files = check_distributions(args.dist, version)
                if args.checksums:
                    write_checksums(files, args.checksums)
                if args.verify_checksums:
                    verify_checksums(files, args.verify_checksums)
            elif args.checksums or args.verify_checksums:
                raise ValueError("Checksum options require --dist")
            print(
                json.dumps(
                    {
                        "version": version.package,
                        "tag": version.tag,
                        "prerelease": version.phase is not None,
                    }
                )
            )
    except (OSError, KeyError, TypeError, ValueError, tarfile.TarError, BadZipFile) as exc:
        parser.exit(1, f"Release validation failed: {exc}\n")


if __name__ == "__main__":
    main()
