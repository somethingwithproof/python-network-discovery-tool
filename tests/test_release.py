# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Release integrity checks run offline and never tag, commit, or publish."""

import importlib.util
import io
import json
import re
import sys
import tarfile
from pathlib import Path
from zipfile import ZipFile

import pytest


@pytest.fixture(scope="module")
def release():
    path = Path(__file__).parents[1] / "scripts" / "release.py"
    spec = importlib.util.spec_from_file_location("release_tools", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def project(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[build-system]\nrequires=["hatchling"]\n[project]\nname="netprobe"\nversion = "3.0.0"\n[tool.example]\nversion="keep-me"\n'
    )
    (tmp_path / "uv.lock").write_text(
        'version=1\n[[package]]\nname = "other"\nversion = "1.2.3"\n[[package]]\nname = "netprobe"\nversion = "3.0.0"\n'
    )
    (tmp_path / "CHANGES.md").write_text(
        "# Changelog\n\n## Version 3.0.0 (2026-10-08)\n\n- Initial v3 package.\n"
    )
    return tmp_path


@pytest.mark.parametrize("value", ["0.0.0", "3.1.0", "3.1.0-alpha.0", "3.1.0-beta.2", "3.1.0-rc.1"])
def test_version_roundtrip(release, value):
    version = release.parse_version(value)
    assert version.semantic == value
    assert version.tag == "v" + value
    assert release.parse_version(version.package, package=True) == version


@pytest.mark.parametrize(
    "value",
    [
        "v3.1.0",
        "03.1.0",
        "3.01.0",
        "3.1",
        "3.1.0+build",
        "3.1.0-rc.01",
        "3.1.0-dev.1",
        "3.1.0rc1",
        "٣.1.0",
        "3.1.0;anything",
    ],
)
def test_noncanonical_versions_rejected(release, value):
    with pytest.raises(ValueError):
        release.parse_version(value)


def test_prerelease_precedence(release):
    versions = [
        "3.0.0",
        "3.1.0-alpha.1",
        "3.1.0-alpha.2",
        "3.1.0-beta.0",
        "3.1.0-rc.1",
        "3.1.0",
        "3.1.1",
    ]
    keys = [release.parse_version(version).precedence for version in versions]
    assert keys == sorted(keys)
    assert len(set(keys)) == len(keys)


def release_please_bump(project, version, notes="### Features\n\n* add a thing\n"):
    """What a release-please PR changes: both versions and a new changelog entry."""
    for name in ("pyproject.toml", "uv.lock"):
        path = project / name
        path.write_text(path.read_text().replace('version = "3.0.0"', f'version = "{version}"'))
    changelog = project / "CHANGES.md"
    entry = (
        f"## [{version}](https://github.com/o/r/compare/v3.0.0...v{version}) (2026-11-10)\n\n"
        + notes
    )
    changelog.write_text(
        changelog.read_text().replace("## Version 3.0.0", entry + "\n## Version 3.0.0")
    )


def test_release_requires_matching_tag_notes_and_lock(release, project):
    with pytest.raises(ValueError, match="Tag must"):
        release.check_release(project, "v9.0.0")
    with pytest.raises(ValueError, match="backwards"):
        release.check_release(project, previous="4.0.0")
    assert release.check_release(project, "v3.0.0").semantic == "3.0.0"
    release_please_bump(project, "3.1.0")
    assert release.check_release(project, "v3.1.0", previous="3.0.0").semantic == "3.1.0"
    lock = project / "uv.lock"
    lock.write_text(
        lock.read_text().replace(
            'name = "netprobe"\nversion = "3.1.0"', 'name = "netprobe"\nversion = "3.0.0"'
        )
    )
    with pytest.raises(ValueError, match=r"uv\.lock disagree"):
        release.check_release(project, "v3.1.0")


def test_release_please_notes_stop_at_the_previous_release(release, project):
    release_please_bump(project, "3.1.0", "### Bug Fixes\n\n* **scan:** fix it\n")
    notes = release.release_notes(
        (project / "CHANGES.md").read_text(), release.parse_version("3.1.0")
    )
    assert notes == "### Bug Fixes\n\n* **scan:** fix it\n"


@pytest.mark.parametrize(
    "heading",
    [
        "## 3.1.0 (2026-11-10)",
        "## [3.1.0] (2026-11-10)",
        "## [3.1.0](https://x) 2026-11-10",
        "## [3.1.0](https://x) (2026-11-10) trailing",
        "## [3.1.00](https://x) (2026-11-10)",
    ],
)
def test_unrecognised_headings_are_not_release_notes(release, heading):
    with pytest.raises(ValueError, match=r"needs a dated 3\.1\.0 section"):
        release.release_notes(f"{heading}\n\n- notes\n", release.parse_version("3.1.0"))


def test_empty_release_notes_rejected(release):
    version = release.parse_version("3.0.0")
    with pytest.raises(ValueError, match="empty"):
        release.release_notes(
            "## Version 3.0.0 (2026-10-08)\n\n## Version 2.0.0 (2025-01-01)\nOld\n",
            version,
        )


@pytest.fixture
def distributions(tmp_path):
    def build(version="3.1.0", metadata_version=None, project_version=None):
        wheel = tmp_path / f"netprobe-{version}-py3-none-any.whl"
        metadata = (
            f"Metadata-Version: 2.4\nName: netprobe\nVersion: {metadata_version or version}\n"
        )
        with ZipFile(wheel, "w") as archive:
            archive.writestr(f"netprobe-{version}.dist-info/METADATA", metadata)
        source = tmp_path / f"netprobe-{version}.tar.gz"
        with tarfile.open(source, "w:gz") as archive:
            for name, text in {
                "PKG-INFO": metadata,
                "pyproject.toml": f'[project]\nname="netprobe"\nversion="{project_version or version}"\n',
            }.items():
                data = text.encode()
                info = tarfile.TarInfo(f"netprobe-{version}/{name}")
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        return tmp_path, [wheel, source]

    return build


def test_distributions_and_checksums(release, distributions):
    directory, files = distributions()
    assert release.check_distributions(directory, release.parse_version("3.1.0")) == files
    manifest = directory / "SHA256SUMS"
    release.write_checksums(files, manifest)
    release.verify_checksums(files, manifest)
    files[0].write_bytes(b"changed after build")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        release.verify_checksums(files, manifest)


@pytest.mark.parametrize("kind", ["metadata", "project", "filename", "missing"])
def test_distribution_version_mismatches_rejected(release, distributions, kind):
    directory, files = distributions(
        metadata_version="3.0.0" if kind == "metadata" else None,
        project_version="3.0.0" if kind == "project" else None,
    )
    if kind == "filename":
        files[0].rename(directory / "other.whl")
    elif kind == "missing":
        files[1].unlink()
    version = release.parse_version("3.1.0")
    with pytest.raises(ValueError):
        release.check_distributions(directory, version)


@pytest.mark.parametrize(
    "content", ["invalid", "0" * 64 + "  ../outside", "0" * 64 + "  unexpected.whl"]
)
def test_checksum_manifest_is_scoped_to_distributions(release, distributions, content):
    directory, files = distributions()
    path = directory / "SHA256SUMS"
    path.write_text(content + "\n")
    with pytest.raises(ValueError):
        release.verify_checksums(files, path)


@pytest.mark.parametrize("kind", ["parent", "absolute", "symlink"])
def test_artifact_paths_cannot_escape_selected_root(release, tmp_path, kind):
    root = tmp_path / "project"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    if kind == "parent":
        path = Path("../outside/notes.md")
    elif kind == "absolute":
        path = outside / "notes.md"
    else:
        (root / "linked").symlink_to(outside, target_is_directory=True)
        path = Path("linked/notes.md")
    with pytest.raises(ValueError, match="within the project root"):
        release.confined_path(path, root)
    assert not (outside / "notes.md").exists()


def test_checksum_output_cannot_overwrite_an_external_file(release, distributions):
    directory, files = distributions()
    outside = directory.parent / "outside-checksums"
    outside.write_text("preserve")
    with pytest.raises(ValueError, match="within the project root"):
        release.write_checksums(files, outside)
    assert outside.read_text() == "preserve"


def test_notes_relative_to_selected_root(release, project):
    version = release.parse_version("3.0.0")
    release.write_notes(project, Path("release-notes.md"), version)
    assert (project / "release-notes.md").read_text() == "- Initial v3 package.\n"


def test_cli_check_reports_failures(release, project, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["release.py", "--root", str(project), "check"])
    release.main()
    assert json.loads(capsys.readouterr().out)["tag"] == "v3.0.0"
    monkeypatch.setattr(
        sys, "argv", ["release.py", "--root", str(project), "check", "--tag", "v9.0.0"]
    )
    with pytest.raises(SystemExit) as error:
        release.main()
    assert error.value.code == 1
    assert "Release validation failed" in capsys.readouterr().err


ROOT = Path(__file__).parents[1]


def test_release_please_config_matches_the_release_checks():
    config = json.loads((ROOT / "release-please-config.json").read_text())
    manifest = json.loads((ROOT / ".release-please-manifest.json").read_text())
    package = config["packages"]["."]
    assert set(manifest) == {"."}
    assert package["release-type"] == "python"
    assert package["changelog-path"] == "CHANGES.md"
    # release.py expects vX.Y.Z tags, and the release build attaches its tested
    # artifacts to a draft that a maintainer publishes.
    assert package["include-v-in-tag"] is True
    assert package["include-component-in-tag"] is False
    assert package["draft"] is True
    assert package["force-tag-creation"] is True
    # The lock records the project's own version; release.py rejects a mismatch.
    (lock,) = package["extra-files"]
    assert lock == {
        "type": "toml",
        "path": "uv.lock",
        "jsonpath": "$.package[?(@.name==='netprobe')].version",
    }


def test_changelog_lets_release_please_insert_above_every_entry():
    """release-please inserts before the first match of this header pattern
    (DEFAULT_VERSION_HEADER_REGEX in its changelog updater). With no match it
    rewrites the file's own headings, so the first section must match."""

    changelog = (ROOT / "CHANGES.md").read_text()
    first_section = changelog.index("\n## ")
    assert re.search(r"\n###? v?[0-9[]", changelog, re.S).start() == first_section


def test_notes_are_required_only_when_a_release_is_prepared(release, project):
    (project / "CHANGES.md").write_text("# Changelog\n\n## Version 2.0.0 (2025-01-01)\n\n- Old.\n")
    # Between releases: same version as the base branch, no tag.
    assert release.check_release(project, previous="3.0.0").semantic == "3.0.0"
    assert release.check_release(project).semantic == "3.0.0"
    with pytest.raises(ValueError, match="needs a dated"):
        release.check_release(project, "v3.0.0")
    with pytest.raises(ValueError, match="needs a dated"):
        release.check_release(project, previous="2.9.0")
