<!--
SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Changelog

## Unreleased

- Fail closed on TLS certificate or hostname verification errors; private-CA services require `--tls-ca-file` for certificate and HTTP observations.
- Refactor CLI orchestration, history validation, profiles, preflight, comparisons, and tests to resolve project-wide Sonar findings.

- Define the SemVer compatibility contract and stable/prerelease tag mapping.
- Replace legacy release helpers and duplicate upload workflows with reviewed version preparation, validated tag builds, draft GitHub releases, checksums, and optional trusted publishing.
- Add offline release-integrity regression tests and locked build/metadata-validation tools.
- Update the README with accurate workflow badges, setup commands, inventory contracts, and operation limits.

- Add named TOML inventory profiles with network scope, additive exclusions, and resource settings.
- Add local preflight checks and a standalone JSON preflight command.
- Add opt-in transactional SQLite history and comparisons that preserve uncertain observations.
- Apply exclusions to optional Nmap discovery as well as service probes; reject scoped IPv6 targets and bound Nmap subprocess duration.
- Add Python 3.14 to CI and locked dependency installation.
- Use modern type statements, typed preflight results, keyword-only slotted profiles, and bounded structured concurrency while retaining Python 3.12 compatibility.

## Version 3.0.0 (2026-10-08)

3.0.0 is a major release. The JSON report only gained fields, which alone
would be a minor bump, but several behaviours that scripts can depend on
changed: host liveness, the default service set, exit code 1, the Python API
of `NetworkScanner`, and python-nmap is no longer installed by default.

### Breaking changes
- Probes use asyncio sockets instead of nmap. A host is alive when any probe
  is answered (a refused connection counts); hosts that drop every probe are
  now reported down where nmap's ICMP ping may have found them. Use
  `--backend nmap` for an nmap ping sweep.
- python-nmap moved to the optional `nmap` extra.
- HTTP (80) and HTTPS (443) are probed by default alongside SSH, SNMP and MySQL.
- SNMP is detected with an SNMPv3 discovery request and no longer needs root;
  v1/v2c-only agents are found only when a community is given.
- Exit code 1 from `scan` now means the nmap backend is unavailable (it used
  to mean nmap was missing for every scan).
- Scans over 524,288 probes (hosts x services) or 64 services, and
  `--concurrency` above 4096, are refused with exit code 2.
- `NetworkScanner` takes keyword options and no longer exposes the nmap
  `PortScanner` or the `_check_alive`/`_check_port` helpers.

### Features
- `services` list in JSON (name, port, protocol, state, version, details) and
  `services`/`versions` CSV columns; existing fields keep their names.
- Fingerprints: SSH identification, MySQL/MariaDB handshake, HTTP `Server`,
  TLS certificate with recorded verification result, SNMP system MIB with
  v2c or v3 credentials from `NETPROBE_SNMP_*`.
- `--config` TOML services, `--services`, `--ports`, `--timeout`,
  `--concurrency`, `--tls-ca-file`.
- `--save-snapshot` and `netprobe diff` (exit 3 on changes).
- `netprobe export` and `scan -o file.sh`: Kadupul `cli/add_device.php` script.

### Other
- Code moved to `src/netprobe/`; `python -m netprobe` works.
- Unused scripts, configs and docs for the removed `network_discovery`
  package were deleted.
- Docker compose integration lab and CI job.

## Version 0.4.0 (2025-04-23)

### Features
- feat(docker): add containerization for simplified testing and deployment
  - Added Dockerfile and docker-compose.yml for containerization
  - Created helper scripts for Docker setup and testing
  - Added Makefile for common Docker operations
  - Updated documentation with Docker usage instructions
  - Added GitHub Actions workflow for Docker CI
  - Configured environment variables and .dockerignore

## Version 0.3.0 (2025-04-22)

### Features
- feat: implemented enterprise-class release process with tagging, GitHub releases, and release notes
- feat: added release automation scripts for version management
- feat: added GitHub Actions workflows for CI/CD and release automation
- feat: added comprehensive release documentation

## Version 0.2.0 (2025-04-22)

### Features
- Added MkDocs documentation with Material theme
- Improved project structure with proper testing
- Added comprehensive test suite

### Security
- Fixed code scanning alert: Incomplete URL substring sanitization
- Fixed code scanning alert: Accepting unknown SSH host keys when using Paramiko
- Bumped Twisted from 23.10.0 to 24.7.0rc1 to address security vulnerabilities

### Improvements
- Removed VSCode settings from project
- Synchronized branch structure (main, develop, release all match master)
- Removed stale branches

## Previous Changes

### Consolidated Codebase

- Removed Twisted dependency from requirements.txt and setup.py as the codebase has pivoted to using asyncio.
- Created a cleanup script (cleanup_legacy_files.py) to remove redundant files from the root directory that have been replaced by the newer asyncio-based implementation in the src directory.
- The script backs up the redundant files to a timestamped directory before removing them.

### Improved Error Handling

#### Scanner.py

- Enhanced error handling in the check_ssh method to differentiate between:
  - Authentication errors
  - SSH protocol errors
  - Connection timeouts
  - Connection refused errors
  - Command execution errors
- Enhanced error handling in the check_mysql method to differentiate between:
  - Authentication errors (error code 1045)
  - Connection errors (error code 2003)
  - Database not found errors (error code 1049)
  - Query execution errors
- Enhanced error handling in the check_snmp method to differentiate between:
  - MIB loading errors
  - Connection errors
  - Query errors

### Improved Test Coverage

- Created a comprehensive test file for the scanner.py module (tests/test_scanner.py) that includes tests for:
  - Scanning devices (alive and not alive)
  - Checking if a device is alive
  - Checking if a port is open
  - Checking SSH, MySQL, and SNMP services
  - Error handling during scanning

### Other Improvements

- Added asyncio dependency to requirements.txt and setup.py to explicitly declare this dependency.
- Updated version constraints for dependencies to ensure compatibility.

## Next Steps

The following items still need to be addressed:

1. Run linters (Black/Flake8) across the entire codebase.
2. Replace `__del__` methods with context managers where appropriate (e.g., in any remaining database or spreadsheet managers).
3. Further increase test coverage for other modules, particularly:
   - infrastructure/report.py
   - infrastructure/notification.py
   - core/discovery.py
4. Update documentation to match the final consolidated codebase.
