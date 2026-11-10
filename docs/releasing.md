<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Versioning and releases

netprobe follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The
version in `pyproject.toml` is the single source of truth; `uv.lock` records the same
package version. `netprobe version` reads installed package metadata.

## Public compatibility contract

These are public, and a release that changes them incompatibly is a **major**
version:

- **Commands and options**: the `netprobe` subcommands, their arguments, option
  names, accepted values, defaults and environment variables.
- **Exit codes**: the meaning of each status in the README's exit-code table.
- **JSON documents**: every document described in [JSON output](json-output.md)
  and its schema in `src/netprobe/schemas`. Removing or renaming a field, changing
  its type or meaning, or tightening what a schema accepts needs a new document
  `version` and a major release. Adding an optional field is a minor change.
- **Stored data**: snapshot and SQLite history formats netprobe must still read.
- **Runtime support**: the supported Python versions (3.12–3.14) and the Python
  API exported in `netprobe.__all__`.

| Change | Bump | Example |
| --- | --- | --- |
| Backward-compatible correction | Patch | `3.1.0` → `3.1.1` |
| Backward-compatible feature or deprecation | Minor | `3.1.1` → `3.2.0` |
| Incompatible change to anything listed above | Major | `3.2.0` → `4.0.0` |

Log text, table layout, Rich formatting, and fields marked experimental in the
docs are not part of the contract. Internal refactoring that preserves behavior
needs no major release. Released versions, tags and published distribution bytes
are never replaced; corrections get a new version.

## Deprecation policy

A public behavior is deprecated before it is removed:

1. The release that deprecates it is at least a minor release. Its changelog
   entry says what replaces it, and using it logs a warning on stderr (JSON on
   stdout is never changed to carry the warning).
2. It keeps working for every later release in that major series, and for at
   least 90 days after the deprecating release.
3. It is removed only in a major release, listed under breaking changes.

Security fixes are the exception: when keeping a behavior would leave users
exposed (for example a secret accepted on the command line), it may change in the
next release, with the reason in the changelog and a breaking-change footer.

## How versions are chosen

[release-please](https://github.com/googleapis/release-please) derives the next
version and the changelog from [Conventional Commits](https://www.conventionalcommits.org/)
on `main`, so every PR title (the squash-merge subject) must follow the format,
which the **PR title** workflow checks:

| Commit | Release | Changelog section |
| --- | --- | --- |
| `fix: ...`, `fix(scan): ...` | patch | Bug Fixes |
| `feat: ...` | minor | Features |
| `perf: ...` | patch | Performance Improvements |
| `feat!: ...`, `fix(cli)!: ...`, or a `BREAKING CHANGE:` footer | major | Breaking Changes |
| `build`, `chore`, `ci`, `docs`, `refactor`, `style`, `test` | none | not listed |

Mark every change to the public contract with `!` and explain the migration in a
`BREAKING CHANGE:` footer; release-please copies the footer into the changelog.

## Release flow

1. After each push to `main`, `.github/workflows/release-please.yml` opens or
   updates one release PR titled `chore(main): release X.Y.Z`. It bumps
   `pyproject.toml` and netprobe's entry in `uv.lock`, adds a dated section at the
   top of `CHANGES.md`, and updates `.release-please-manifest.json`. Edit the
   release by adding commits to `main`, not to the release PR, which is rewritten.
2. A maintainer reviews the release PR like any other: the version, the
   generated notes and the release checks, which validate exactly what will be
   tagged. Merging it is the decision to release.
3. On that merge release-please creates the `vX.Y.Z` tag and an empty **draft**
   GitHub release with the changelog notes, then calls
   `.github/workflows/release.yml` for the tag. That workflow checks that the tag,
   project version, lockfile and changelog agree and that the commit is on
   `main`, then:
   1. installs the locked tools, runs Ruff, formatting, strict mypy and the tests
      with the 90% coverage floor;
   2. builds a wheel and source distribution once and runs strict Twine checks
      against the version;
   3. writes `SHA256SUMS`, creates GitHub artifact attestations for the files,
      and attaches them to the draft.
4. A maintainer reviews the draft's files and notes and publishes it, in the
   GitHub UI or with `gh release edit vX.Y.Z --draft=false --latest`. Publishing
   triggers the optional PyPI workflow below. Workflows never publish their own
   drafts.

Tags pushed with `GITHUB_TOKEN` do not start other workflows, which is why
release-please calls the build directly. Pull requests opened with `GITHUB_TOKEN`
do not start CI either: set a `RELEASE_PLEASE_TOKEN` secret (a GitHub App or
fine-grained token with contents and pull-requests write) so the release PR's
required checks run. `scripts/release.py check` validates metadata, notes and
artifacts; release-please does the preparation.

A tag pushed by hand still starts the same build and creates the draft itself,
and the manual **Release** workflow rebuilds an existing tag after a failure. Both
refuse to touch a published release or one that already has assets.

### Overriding the version

To force a version, for example the first automated release, set `release-as` in
`release-please-config.json`, or add a `Release-As: X.Y.Z` footer to a commit on
`main`. Remove `release-as` after that release, or every later release PR will
propose the same version.

## Prereleases

Stable versions use `MAJOR.MINOR.PATCH`. The release checks also accept
`MAJOR.MINOR.PATCH-alpha.N`, `-beta.N` and `-rc.N`, without leading zeros or build
metadata. Python distribution versions use the matching PEP 440 spelling:

| Git tag | Package metadata |
| --- | --- |
| `v3.2.0-alpha.1` | `3.2.0a1` |
| `v3.2.0-beta.2` | `3.2.0b2` |
| `v3.2.0-rc.1` | `3.2.0rc1` |
| `v3.2.0` | `3.2.0` |

This release-please configuration creates stable releases only. The checks still
accept prerelease tags pushed by hand, and those are marked as prereleases on
GitHub.

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

1. Choose the PyPI distribution name. `netprobe` is already registered on PyPI
   by an unrelated project, so the `name` in `pyproject.toml` (and the environment
   URL in `publish.yml`) must change to a name this project owns before publishing.
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
build are removed. Use release-please, the tag build, draft promotion, and the
optional trusted-publisher workflow described here. `scripts/release.py prepare`
is replaced by release-please. No `develop` branch or
post-release `.dev0` mutation is required.
