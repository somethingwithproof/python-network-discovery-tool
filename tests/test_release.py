"""Release integrity checks run offline and never tag, commit, or publish."""

import importlib.util
import io
import json
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
        "# Changelog\n\n## Unreleased\n\n- New inventory features.\n\n## Version 3.0.0 (2026-10-08)\n\n- Initial v3 package.\n"
    )
    return tmp_path


@pytest.mark.parametrize("value", ["0.0.0", "3.1.0", "3.1.0-alpha.0", "3.1.0-beta.2", "3.1.0-rc.1"])
def test_version_roundtrip(release, value):
    version = release.parse_version(value)
    assert version.semantic == value and version.tag == "v" + value
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
    assert keys == sorted(keys) and len(set(keys)) == len(keys)


@pytest.mark.parametrize(
    "bump,expected", [("major", "4.0.0"), ("minor", "3.5.0"), ("patch", "3.4.6")]
)
def test_semantic_bumps(release, bump, expected):
    assert release.next_version(release.parse_version("3.4.5"), bump).semantic == expected


def test_prepare_updates_only_project_version_lock_and_unreleased_notes(release, project):
    version = release.parse_version("3.1.0-rc.1")
    files = release.prepare(project, version)
    assert files == ["pyproject.toml", "uv.lock", "CHANGES.md"]
    assert release.project_version(project).package == "3.1.0rc1"
    assert 'version="keep-me"' in (project / "pyproject.toml").read_text()
    assert 'version = "1.2.3"' in (project / "uv.lock").read_text()
    assert "New inventory features" in release.release_notes(
        (project / "CHANGES.md").read_text(), version
    )
    assert release.check_release(project, "v3.1.0-rc.1") == version


def test_dry_run_does_not_write(release, project):
    before = {path: path.read_bytes() for path in project.iterdir()}
    release.prepare(project, release.parse_version("3.1.0"), dry_run=True)
    assert before == {path: path.read_bytes() for path in project.iterdir()}


@pytest.mark.parametrize("value", ["2.9.9", "3.0.0", "3.0.0-rc.1"])
def test_prepare_refuses_older_or_equal_versions(release, project, value):
    with pytest.raises(ValueError, match="greater"):
        release.prepare(project, release.parse_version(value))


@pytest.mark.parametrize(
    "problem", ["missing_notes", "empty_notes", "duplicate_release", "wrong_lock"]
)
def test_invalid_prepare_leaves_all_files_unchanged(release, project, problem):
    changelog = project / "CHANGES.md"
    if problem == "missing_notes":
        changelog.write_text("# Changelog\n")
    elif problem == "empty_notes":
        changelog.write_text(
            "# Changelog\n\n## Unreleased\n\n## Version 3.0.0 (2026-10-08)\n\n- Old.\n"
        )
    elif problem == "duplicate_release":
        changelog.write_text(
            changelog.read_text() + "\n## Version 3.1.0 (2026-10-08)\n\n- Duplicate.\n"
        )
    else:
        path = project / "uv.lock"
        path.write_text(path.read_text().replace('version = "3.0.0"', 'version = "3.0.1"'))
    before = {path: path.read_bytes() for path in project.iterdir()}
    with pytest.raises(ValueError):
        release.prepare(project, release.parse_version("3.1.0"))
    assert before == {path: path.read_bytes() for path in project.iterdir()}


def test_release_requires_matching_tag_notes_and_lock(release, project):
    with pytest.raises(ValueError, match="Tag must"):
        release.check_release(project, "v9.0.0")
    with pytest.raises(ValueError, match="Unreleased"):
        release.check_release(project, "v3.0.0")
    with pytest.raises(ValueError, match="backwards"):
        release.check_release(project, previous="4.0.0")
    release.prepare(project, release.parse_version("3.1.0"))
    assert release.check_release(project, "v3.1.0", previous="3.0.0").semantic == "3.1.0"


def test_empty_release_notes_rejected(release):
    with pytest.raises(ValueError, match="empty"):
        release.release_notes(
            "## Version 3.0.0 (2026-10-08)\n\n## Version 2.0.0 (2025-01-01)\nOld\n",
            release.parse_version("3.0.0"),
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
    with pytest.raises(ValueError):
        release.check_distributions(directory, release.parse_version("3.1.0"))


@pytest.mark.parametrize(
    "content", ["invalid", "0" * 64 + "  ../outside", "0" * 64 + "  unexpected.whl"]
)
def test_checksum_manifest_is_scoped_to_distributions(release, distributions, content):
    directory, files = distributions()
    path = directory / "SHA256SUMS"
    path.write_text(content + "\n")
    with pytest.raises(ValueError):
        release.verify_checksums(files, path)


def test_cli_prepare_dry_run_and_check(release, project, monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "argv", ["release.py", "--root", str(project), "prepare", "minor", "--dry-run"]
    )
    release.main()
    assert json.loads(capsys.readouterr().out)["tag"] == "v3.1.0"
    monkeypatch.setattr(
        sys, "argv", ["release.py", "--root", str(project), "check", "--tag", "v9.0.0"]
    )
    with pytest.raises(SystemExit) as error:
        release.main()
    assert error.value.code == 1
    assert "Release validation failed" in capsys.readouterr().err
