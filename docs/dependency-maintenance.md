# Dependency maintenance

Dependabot maintains `pyproject.toml` and `uv.lock` through the native `uv`
ecosystem, pinned GitHub Actions, and the root Dockerfile. Weekly updates run on
Monday morning in America/Los_Angeles. Python runtime and development tools have
separate minor/patch groups; major upgrades remain individual PRs. Python security
updates have a separate group and follow GitHub's security-update scheduling.

Dependency PRs use existing repository labels and conventional `chore(deps)`
titles. Keep lockfile updates with their manifest changes. Validate Python changes
with the supported Python matrix, Ruff, strict mypy, and the Compose integration
lab. Run container checks for base-image updates.

The metadata-only auto-merge workflow uses `pull_request_target`, verifies the
Dependabot author and same-repository branch, and never checks out PR code.
Eligible uv and Actions minor/patch updates may queue squash auto-merge only when
main's rules require the listed CI and security gates. It does not submit automated
approvals. Docker and major updates require maintainer review. Auto-merge remains
inactive if those required checks are absent.

The main-branch rules should require all supported Python matrix jobs, lint,
typing, integration, parser fuzzing, Docker smoke tests, Bandit, CodeQL, SonarCloud,
and configured external security checks. Maintain required check names when
renaming jobs. A failed external service remains a merge blocker.

The inline lab images in `tests/integration/compose.yml` and runtime tool versions
embedded in mise configuration need explicit maintainer updates; the root Docker
entry does not maintain every embedded image or tool version.

See [uv's Dependabot integration](https://docs.astral.sh/uv/guides/integration/dependabot/)
and [GitHub's Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference).
