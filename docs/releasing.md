# Versioning and releases

netprobe follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The
version in `pyproject.toml` is the single source of truth; `uv.lock` records the same
package version. `netprobe version` reads installed package metadata.

## Public compatibility contract

Version changes cover documented CLI options and defaults, exit codes, report
fields and their meaning, snapshot/history formats, supported Python versions,
and the exported Python API in `netprobe.__all__`.

| Change | Bump | Example |
| --- | --- | --- |
| Backward-compatible correction | Patch | `3.1.0` → `3.1.1` |
| Backward-compatible feature or deprecation | Minor | `3.1.1` → `3.2.0` |
| Incompatible API, CLI, output, default, or runtime support change | Major | `3.2.0` → `4.0.0` |

Adding optional report fields is normally a minor change; removing or changing an
existing field's meaning requires a major change. Internal refactoring that
preserves behavior does not itself require a major release. Released versions,
tags, and published distribution bytes are never replaced. Corrections receive a
new version.

Development changes accumulate under `## Unreleased` in `CHANGES.md`. The version
changes in a reviewed release-preparation PR rather than after every feature merge.
Use conventional PR titles such as `feat:`, `fix:`, and `docs:` to aid review;
maintainers choose the bump based on the compatibility contract, not title alone.
GitHub-generated notes can categorize PRs using `.github/release.yml` labels, while
the committed changelog remains the source of the release description.

## Prereleases

Stable versions use `MAJOR.MINOR.PATCH`. The supported prerelease subset is
`MAJOR.MINOR.PATCH-alpha.N`, `-beta.N`, or `-rc.N`, without leading zeros or build
metadata. Python distribution versions use the corresponding PEP 440 spelling:

| Git tag | Package metadata |
| --- | --- |
| `v3.2.0-alpha.1` | `3.2.0a1` |
| `v3.2.0-beta.2` | `3.2.0b2` |
| `v3.2.0-rc.1` | `3.2.0rc1` |
| `v3.2.0` | `3.2.0` |

The helper validates ordering, including prereleases before a stable version.
A prerelease must have its own release notes. Supported prereleases are marked
as prereleases in GitHub; stable releases are promoted separately.

## Prepare a release PR

Start from up-to-date `main` with a clean checkout:

```bash
git switch main
git pull --ff-only
git switch -c release/3.1.0
mise exec python@3.14 -- uv sync --locked --extra dev
mise exec python@3.14 -- python scripts/release.py prepare minor --dry-run
mise exec python@3.14 -- python scripts/release.py prepare minor
mise exec python@3.14 -- python scripts/release.py check
mise exec python@3.14 -- uv sync --locked --extra dev
```

Replace `minor` with `major`, `patch`, or an explicit version such as
`3.2.0-rc.1`. The helper updates only the project version, its lockfile entry, and
the changelog: it moves nonempty Unreleased notes to a dated version section and
leaves a fresh Unreleased heading. It performs no Git operations or uploads.

Review those changes, run the usual checks, commit with `git commit -s`, push, and
open a release-preparation PR. Merge after all applicable checks and reviews pass.
If the PR includes an actual dependency change, refresh `uv.lock` separately with
`uv lock` and review the resulting dependency diff.

## Tag and build

After the preparation PR is merged, tag that exact commit:

```bash
git switch main
git pull --ff-only
mise exec python@3.14 -- python scripts/release.py check --tag v3.1.0
git tag -a v3.1.0 -m "Release v3.1.0"
git push origin v3.1.0
```

Use the version actually prepared. A `v*` tag starts `.github/workflows/release.yml`.
The workflow checks that the tag agrees with project and lockfile metadata, the
notes are complete, Unreleased has no pending content, and the tagged commit is
reachable from `main`. It then:

1. Installs Python 3.14 and uv through `mise`, and installs locked development tools.
2. Runs Ruff, formatting, strict mypy, and tests with the existing 90% coverage floor.
3. Builds a wheel and source distribution once, using the installed locked build backend.
4. Runs strict Twine metadata checks and validates both distributions against the version.
5. Generates `SHA256SUMS` and retains the same distribution files as workflow artifacts.
6. Creates a **draft** GitHub release with changelog notes and the tested files.

Pull requests changing release configuration exercise the validation/build path
without tagging, creating a release, requesting signing tokens, or publishing.
The manual Release workflow accepts an existing tag for retrying a failed build.
It refuses to replace an existing release or its assets.

Review the draft assets and notes, then publish through the GitHub Releases UI or
with your own authenticated GitHub CLI:

```bash
gh release edit v3.1.0 --draft=false --latest
```

For a prerelease, use its prerelease tag and `--latest=false`. Promotion is a
maintainer action: workflows do not publish their own drafts. This also avoids
[GitHub's restriction on downstream workflow events generated by `GITHUB_TOKEN`](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
Enable immutable releases in repository settings where available. Attach all
artifacts before promotion; published release contents should remain unchanged.

## Checksums and build provenance

The release job installs locked dependencies from wheels, builds the project once
with its locked build backend, and installs that wheel for regression testing.
It does not run dependency source builds. The optional source-only Nmap wrapper is
covered by the regular CI jobs; release tests use the mocked system boundary.

Release helper artifact paths must stay inside the selected `--root` (the current
directory by default). Relative artifact paths are resolved against that root;
checksum manifests must stay beside their distributions. Parent traversal and
symlinks that resolve outside these boundaries are rejected.

Every draft includes checksums. Download the assets from a published release and
run `sha256sum -c SHA256SUMS` in the download directory to detect accidental changes.
Checksums alone do not authenticate a publisher.

GitHub artifact attestations are enabled for public repositories. Private
repositories must have a GitHub plan that supports attestations and explicitly
set `ARTIFACT_ATTESTATIONS_ENABLED=true`. This repository is public, so tagged
releases generate attestations automatically. An enabled
attestation failure blocks draft creation; it is not silently ignored.
[GitHub documents the plan requirements and verification workflow](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations).

When attestations were generated:

```bash
gh attestation verify netprobe-3.1.0-py3-none-any.whl \
  -R somethingwithproof/python-network-discovery-tool
```

This process provides GitHub build provenance where supported; it does not claim a
particular SLSA level. The old independent provenance build is retired so signatures
and attached files cannot refer to different builds.

## Optional PyPI publishing

PyPI publishing is **disabled by default**. Before enabling it:

1. Confirm ownership of the `netprobe` project on PyPI.
2. Configure a [PyPI trusted publisher](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
   for owner `somethingwithproof`, repository `python-network-discovery-tool`,
   workflow `publish.yml`, and environment `pypi`.
3. Create the GitHub `pypi` environment and configure appropriate reviewers and
   release-tag restrictions.
4. Set repository variable `PYPI_PUBLISH_ENABLED=true`.

A maintainer publishing the draft triggers `.github/workflows/publish.yml`.
The job waits for configured environment approval, downloads the **existing**
release wheel/source distribution and checksum manifest, validates the tag,
version, metadata and checksums, then publishes with short-lived OIDC credentials.
It does not rebuild, use a stored API token, or skip conflicting existing versions.
Publishing is performed by the official PyPA publishing action.

For a retry, manually run Publish to PyPI with an existing **published** tag.
Never rerun an upload to replace an existing PyPI version. After a partial upload,
inspect which files exist and resolve it through the registry's supported process;
if the release needs changes, prepare a new version.

## Retired paths

The old GitFlow helpers, development-version bumper, independent tag-based release
notes, duplicate PyPI uploader, Maven-targeted Python upload, and independent SLSA
build are removed. Use the preparation helper, tag build, draft promotion, and
optional trusted-publisher workflow described here. No `develop` branch or
post-release `.dev0` mutation is required.
