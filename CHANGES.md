<!--
SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# Changelog

## [3.0.0](https://github.com/somethingwithproof/python-network-discovery-tool/compare/v0.3.0...v3.0.0) (2026-11-11)


### ⚠ BREAKING CHANGES

* the distribution and import package are now hostcensus. `import netprobe` and `python -m netprobe` no longer work and no shim is installed. The `netprobe` command and NETPROBE_* environment variables are deprecated and will be removed in the next major release. The Docker image tag is now hostcensus:test and the container user is hostcensus.
* **diff:** diff exits 3 instead of 0 for these transitions; unsettled_hosts before/after may be absent and unconfirmed before/after may be not-open. compare lists a port that was unknown and is now open under port_changes instead of unconfirmed_ports, matching diff's opened.
* **diff:** diff exits 3 instead of 0 for these transitions; unsettled_hosts before/after may be absent and unconfirmed before/after may be not-open. compare lists a port that was unknown and is now open under port_changes instead of unconfirmed_ports, matching diff's opened.
* **diff:** diff exits 3 instead of 0 for these transitions; unsettled_hosts before/after may be absent and unconfirmed before/after may be not-open. compare lists a port that was unknown and is now open under port_changes instead of unconfirmed_ports, matching diff's opened.
* **scan:** scans that run longer than an hour now stop and exit 4. Pass a larger --deadline (up to 604800 seconds) for long scans.
* **output:** `scan -o FILE.json` writes an object whose devices are under `devices` instead of a bare list, and `history` prints an object whose entries are under `scans`. Read `.devices` and `.scans`; see docs/json-output.md for the formats and the stability policy.
* **cli:** --snmp-community, --snmp-auth-key and --snmp-priv-key no longer accept values. Set NETPROBE_SNMP_COMMUNITY, NETPROBE_SNMP_AUTH_KEY and NETPROBE_SNMP_PRIV_KEY, or pass the matching --snmp-*-file option.
* **probes:** service `state` can be "unknown". Probe timeouts and probe exceptions were "filtered" and are now "unknown", and a host with only failed probes no longer carries the "Host is down" error.
* **probes:** service `state` can be "unknown". Probe timeouts and probe exceptions were "filtered" and are now "unknown", and a host with only failed probes no longer carries the "Host is down" error.

### Features

* Add comprehensive E2E testing + rename to netprobe ([94c387e](https://github.com/somethingwithproof/python-network-discovery-tool/commit/94c387e6fe62e85d989616ad2f8891f35f486b1f))
* add Dependabot auto-merge workflow ([f390937](https://github.com/somethingwithproof/python-network-discovery-tool/commit/f390937798e345b8a1fc0e29dcc8698638f7b801))
* budget connect probes apart from SNMP and TLS ([#104](https://github.com/somethingwithproof/python-network-discovery-tool/issues/104)) ([da3ae4d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/da3ae4de5d414ede63e11e97649963cd6f39a16c))
* **ci:** add Dependabot auto-merge configuration ([f44606e](https://github.com/somethingwithproof/python-network-discovery-tool/commit/f44606ef84060ec915dec6c15869000508b44031))
* **cli:** read SNMP secrets only from the environment or files ([#132](https://github.com/somethingwithproof/python-network-discovery-tool/issues/132)) ([71b2e7d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/71b2e7da3e3caeb88b892d824d2ec5c9d24dfdfd))
* Complete rewrite with modern 2026 architecture ([4e8fc20](https://github.com/somethingwithproof/python-network-discovery-tool/commit/4e8fc20c26c6c8a20375989ff13ea7fda90c4db4))
* configure services from TOML and the command line ([#85](https://github.com/somethingwithproof/python-network-discovery-tool/issues/85)) ([9a6a8b8](https://github.com/somethingwithproof/python-network-discovery-tool/commit/9a6a8b8bf512fae3dab611ae9a1158c0069fbdd6))
* export scans as a Kadupul add_device.php script ([#88](https://github.com/somethingwithproof/python-network-discovery-tool/issues/88)) ([852d3be](https://github.com/somethingwithproof/python-network-discovery-tool/commit/852d3be9b9e925b02b34ff4497212664d2efc2eb))
* fingerprint SSH, MySQL, HTTP(S) and SNMP services ([#86](https://github.com/somethingwithproof/python-network-discovery-tool/issues/86)) ([e75300a](https://github.com/somethingwithproof/python-network-discovery-tool/commit/e75300a68a2f8dc3d5aee4e8d5bc32a4b0c5222a))
* implement enterprise-class release process ([0706684](https://github.com/somethingwithproof/python-network-discovery-tool/commit/0706684e63b412dfb008358034a91564fbedc88e))
* implement Google Python style guide ([3236e96](https://github.com/somethingwithproof/python-network-discovery-tool/commit/3236e96b141b368a5354c0d5dfc6b2049930b678))
* **output:** version every JSON document and publish schemas ([#137](https://github.com/somethingwithproof/python-network-discovery-tool/issues/137)) ([d4c5227](https://github.com/somethingwithproof/python-network-discovery-tool/commit/d4c5227e2046ecf28331ff12a7a084aad2a0a911))
* probe services with asyncio sockets and make nmap optional ([#84](https://github.com/somethingwithproof/python-network-discovery-tool/issues/84)) ([1b8ef84](https://github.com/somethingwithproof/python-network-discovery-tool/commit/1b8ef844d746343140c8513621085362bec1184e))
* save scan snapshots and diff them ([#87](https://github.com/somethingwithproof/python-network-discovery-tool/issues/87)) ([7510af5](https://github.com/somethingwithproof/python-network-discovery-tool/commit/7510af5f36b727926f189bc9927558dc85259cc2))
* **scan:** bound the whole scan with --deadline ([#140](https://github.com/somethingwithproof/python-network-discovery-tool/issues/140)) ([df9dfe0](https://github.com/somethingwithproof/python-network-discovery-tool/commit/df9dfe0087ac06a7785d4db31140e65933d840ed))


### Bug Fixes

* add missing dependencies to requirements.txt ([#17](https://github.com/somethingwithproof/python-network-discovery-tool/issues/17)) ([3ac52f8](https://github.com/somethingwithproof/python-network-discovery-tool/commit/3ac52f80fd4fb054406d9b5de7547838ba1f84d6))
* **ci:** use specific runner labels, fix codeql concurrency ([d50fcb9](https://github.com/somethingwithproof/python-network-discovery-tool/commit/d50fcb953547f06938633cbebb3063d5c94a9df4))
* **cli:** log to stderr, honour --quiet, and keep history private ([#128](https://github.com/somethingwithproof/python-network-discovery-tool/issues/128)) ([21f755b](https://github.com/somethingwithproof/python-network-discovery-tool/commit/21f755ba0206be5d722044d47d79b64314e4e834))
* complete test and remove unused imports ([5b11ff5](https://github.com/somethingwithproof/python-network-discovery-tool/commit/5b11ff5661cb0c164c22d24658533b24fd302553))
* create .env with 0600 before writing the MySQL password ([#77](https://github.com/somethingwithproof/python-network-discovery-tool/issues/77)) ([95fae59](https://github.com/somethingwithproof/python-network-discovery-tool/commit/95fae59406576bf74a62324e235cc58987aa6f28))
* **diff:** never report a failed observation as no change ([#144](https://github.com/somethingwithproof/python-network-discovery-tool/issues/144)) ([c7f125d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/c7f125d3e323913aea0e8cdb82d86bdd752f745b))
* **diff:** refuse incomplete scan reports unless --allow-partial ([#150](https://github.com/somethingwithproof/python-network-discovery-tool/issues/150)) ([e42199a](https://github.com/somethingwithproof/python-network-discovery-tool/commit/e42199ad1b807c6806ba612a13f9162ef34fcc15))
* **diff:** validate and clean snapshot and report contents on load ([#149](https://github.com/somethingwithproof/python-network-discovery-tool/issues/149)) ([932bd34](https://github.com/somethingwithproof/python-network-discovery-tool/commit/932bd34a1725fa996a960cca0f4c267c28c63ff0))
* **export:** keep generated Kadupul descriptions unique ([#133](https://github.com/somethingwithproof/python-network-discovery-tool/issues/133)) ([635ac01](https://github.com/somethingwithproof/python-network-discovery-tool/commit/635ac019e6c04725fc7ebec04f808756c8de6a29))
* improve pytest configuration for stability ([7045d31](https://github.com/somethingwithproof/python-network-discovery-tool/commit/7045d31260ca09c03f991e2a600aec3c0a751ee8))
* keep scan output on the path the operator named ([#102](https://github.com/somethingwithproof/python-network-discovery-tool/issues/102)) ([037405f](https://github.com/somethingwithproof/python-network-discovery-tool/commit/037405f4fc29c5b47e31f4f7955c5d1c49ba3825))
* **nmap:** run nmap directly and parse its XML with defusedxml ([#129](https://github.com/somethingwithproof/python-network-discovery-tool/issues/129)) ([3f9a82d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/3f9a82d026f0061b7b6ed42f9e75a1e336ae13e0))
* **probes:** abort the HTTPS connection instead of waiting for close_notify ([#146](https://github.com/somethingwithproof/python-network-discovery-tool/issues/146)) ([af57af0](https://github.com/somethingwithproof/python-network-discovery-tool/commit/af57af00d13a2546b75b8dbfc3a0bdac66d26169))
* **probes:** report local socket errors and probe deadlines as unknown ([#126](https://github.com/somethingwithproof/python-network-discovery-tool/issues/126)) ([05b9474](https://github.com/somethingwithproof/python-network-discovery-tool/commit/05b94747969647b9d12324a1d93346fb8f116bed))
* **probes:** resolve hostname targets once and time TLS separately ([#127](https://github.com/somethingwithproof/python-network-discovery-tool/issues/127)) ([0a586b4](https://github.com/somethingwithproof/python-network-discovery-tool/commit/0a586b4faf6136a92fe14ec08140cc8f8a8d775a))
* refine bandit configuration to only flag high-level issues ([b240939](https://github.com/somethingwithproof/python-network-discovery-tool/commit/b240939545a4cc971494b95b2dd4b49148f773ac))
* reject trailing newlines in validated names ([#131](https://github.com/somethingwithproof/python-network-discovery-tool/issues/131)) ([12bd441](https://github.com/somethingwithproof/python-network-discovery-tool/commit/12bd441a625f8df08dfcccb1e7778c4267373421))
* remove duplicate code and unused imports ([101b4e4](https://github.com/somethingwithproof/python-network-discovery-tool/commit/101b4e436770a2c2230637c6593d9a3ee79f6aa1))
* remove EOL Python 3.8 support ([1b10a1c](https://github.com/somethingwithproof/python-network-discovery-tool/commit/1b10a1cdaae7ee0758071daf820ce31b09af5185))
* remove redundant MySQL timeout exception catch ([#95](https://github.com/somethingwithproof/python-network-discovery-tool/issues/95)) ([d1feeb9](https://github.com/somethingwithproof/python-network-discovery-tool/commit/d1feeb967251f759d96c1eb21d0dec66d6dea2bc))
* remove unused imports and fix URL substring sanitization ([561d295](https://github.com/somethingwithproof/python-network-discovery-tool/commit/561d295b5369cd7c2f7efe043e33f38196292687))
* remove unused pytest import and result variables ([2bdd41e](https://github.com/somethingwithproof/python-network-discovery-tool/commit/2bdd41e5501a3ac1ef9e4df8293ea87d2c653a40))
* remove unused variables and fix line length ([b142b6d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/b142b6d3a62444f4168e4550c8eeb577b0ddac4f))
* resolve CI, Docker Build, and Bandit workflow failures ([65f8182](https://github.com/somethingwithproof/python-network-discovery-tool/commit/65f81829133dd5af800cfb1d8fed244885522cc2))
* resolve flake8 linting errors in test_repository.py ([90548c6](https://github.com/somethingwithproof/python-network-discovery-tool/commit/90548c66fa7236423e6a7f92eb35079c620ecce5))
* resolve remaining flake8 linting errors ([6d785de](https://github.com/somethingwithproof/python-network-discovery-tool/commit/6d785de034f2a9bc28f55225f738aa99724bc6d5))
* resolve Sonar findings and strengthen OpenSSF checks ([#93](https://github.com/somethingwithproof/python-network-discovery-tool/issues/93)) ([b70f389](https://github.com/somethingwithproof/python-network-discovery-tool/commit/b70f389921b0575768ea974cfde64b97e825d7b2))
* **scan:** apply exclusions to IPv6 spellings of excluded IPv4 hosts ([#147](https://github.com/somethingwithproof/python-network-discovery-tool/issues/147)) ([c30c066](https://github.com/somethingwithproof/python-network-discovery-tool/commit/c30c066d1a14aeeddb8ab2149f44d11bc7e84cce))
* **scan:** fail closed when nmap scans fewer addresses than requested ([#145](https://github.com/somethingwithproof/python-network-discovery-tool/issues/145)) ([9842a88](https://github.com/somethingwithproof/python-network-discovery-tool/commit/9842a880b78560e2c87bd70f8e85381cf856e0e6))
* **scan:** keep hung resolver calls from outlasting --deadline ([#148](https://github.com/somethingwithproof/python-network-discovery-tool/issues/148)) ([2b494d9](https://github.com/somethingwithproof/python-network-discovery-tool/commit/2b494d9e09e37fe2f6fcc4b87b4f8a67de1f8a7f))
* **scan:** sweep the pinned address of a hostname target with nmap ([#151](https://github.com/somethingwithproof/python-network-discovery-tool/issues/151)) ([7a9cec8](https://github.com/somethingwithproof/python-network-discovery-tool/commit/7a9cec8eb09908669c47091ea41ff93747e04b1e))
* **security:** add explicit permissions to GitHub Actions workflows ([1f89891](https://github.com/somethingwithproof/python-network-discovery-tool/commit/1f8989158b3b115df3042b7a8d0cf8eb988d08a6))
* **security:** address security vulnerabilities ([c2ebbe2](https://github.com/somethingwithproof/python-network-discovery-tool/commit/c2ebbe2fac9091aa3851e06ee98798d58dc67313))
* **security:** resolve potential shell injection vulnerability (B601) ([a0c6d03](https://github.com/somethingwithproof/python-network-discovery-tool/commit/a0c6d039a6256358a57f9a16652f0389a3c62141))
* **security:** update dependencies to resolve vulnerabilities ([e046a0f](https://github.com/somethingwithproof/python-network-discovery-tool/commit/e046a0fcc2cc73bd7ecea7c70dde6396e983ecfb))
* update Bandit workflow action versions and add workflow_dispatch ([5e98331](https://github.com/somethingwithproof/python-network-discovery-tool/commit/5e98331c49e66e818f5f2c482688a74261f3b157))
* Update docker/setup-buildx-action from v3 to v4 ([ce4b3f2](https://github.com/somethingwithproof/python-network-discovery-tool/commit/ce4b3f2726c8a44be68b25c74b1f996fac72c248))
* validate scan targets and give each nmap call its own scanner ([#81](https://github.com/somethingwithproof/python-network-discovery-tool/issues/81)) ([b4d3275](https://github.com/somethingwithproof/python-network-discovery-tool/commit/b4d327544bcf4748ec7289852f1353807a2b6026))


### Performance Improvements

* load the TLS trust store once per scan ([#103](https://github.com/somethingwithproof/python-network-discovery-tool/issues/103)) ([ef56ab9](https://github.com/somethingwithproof/python-network-discovery-tool/commit/ef56ab94ca086f23de602215165b64f9740fd4e3))


### Documentation

* add MkDocs with Material theme ([#5](https://github.com/somethingwithproof/python-network-discovery-tool/issues/5)) ([5a30083](https://github.com/somethingwithproof/python-network-discovery-tool/commit/5a3008361b4836cf0735638783b758ad4bf8635d))
* clarify project scope and verify README badges ([#78](https://github.com/somethingwithproof/python-network-discovery-tool/issues/78)) ([100d452](https://github.com/somethingwithproof/python-network-discovery-tool/commit/100d45228791a8b80ece6f4bb1aa646ec0bef04c))
* describe netprobe 3.0.0 and bump the version ([#89](https://github.com/somethingwithproof/python-network-discovery-tool/issues/89)) ([ffe435e](https://github.com/somethingwithproof/python-network-discovery-tool/commit/ffe435eb19967fbd428a7d33de1fdcd1c9718069))
* describe the scan pipeline, its limits and authorized use ([#142](https://github.com/somethingwithproof/python-network-discovery-tool/issues/142)) ([4888c9d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/4888c9daffa9e33b6bad68b92eadc0db3e9b0b33))
* document scan options, requirements and exit codes ([#82](https://github.com/somethingwithproof/python-network-discovery-tool/issues/82)) ([6421d9d](https://github.com/somethingwithproof/python-network-discovery-tool/commit/6421d9d437837b63276ae156c7ab44430d9d5615))
* remove AI attribution from README ([ad62a37](https://github.com/somethingwithproof/python-network-discovery-tool/commit/ad62a37b225114f7161173c1c7f92ad579aeeaa1))


### Code Refactoring

* rename the project to hostcensus ([#152](https://github.com/somethingwithproof/python-network-discovery-tool/issues/152)) ([d707821](https://github.com/somethingwithproof/python-network-discovery-tool/commit/d7078214391d49a3f3706d94b00da779a2ee0bca))

### [Notes for 3.0.0 written before release automation]

release-please writes each release's section above this block from
Conventional Commit titles; the 3.0.0 section it inserts ends with this block,
so these notes are part of the 3.0.0 release notes. They were kept by hand while
3.0.0 was prepared; it was never tagged before release automation took over, and
v0.3.0 is the last release.

#### Overview drafted on 2026-10-08

3.0.0 is a major release. The JSON report only gained fields, which alone
would be a minor bump, but several behaviours that scripts can depend on
changed: host liveness, the default service set, exit code 1, the Python API
of `NetworkScanner`, and python-nmap is no longer installed by default.

##### Breaking changes
- The project is renamed from netprobe to hostcensus: the distribution, the
  `hostcensus` import package and command, and `HOSTCENSUS_*` environment
  variables. `import netprobe` and `python -m netprobe` stop working. The
  `netprobe` command and `NETPROBE_*` variables remain as deprecated aliases
  until the next major release, and old reports, snapshots, history databases and
  default file names still load. See "Migrating from netprobe" in the README.
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

##### Features
- `services` list in JSON (name, port, protocol, state, version, details) and
  `services`/`versions` CSV columns; existing fields keep their names.
- Fingerprints: SSH identification, MySQL/MariaDB handshake, HTTP `Server`,
  TLS certificate with recorded verification result, SNMP system MIB with
  v2c or v3 credentials from `NETPROBE_SNMP_*`.
- `--config` TOML services, `--services`, `--ports`, `--timeout`,
  `--concurrency`, `--tls-ca-file`.
- `--save-snapshot` and `netprobe diff` (exit 3 on changes).
- `netprobe export` and `scan -o file.sh`: Kadupul `cli/add_device.php` script.

##### Other
- Code moved to `src/netprobe/`; `python -m netprobe` works.
- Unused scripts, configs and docs for the removed `network_discovery`
  package were deleted.
- Docker compose integration lab and CI job.

#### Later changes

- Refuse report writes when the platform cannot open files without following symlinks, and create new reports and export scripts with owner-only permissions. Existing file permissions remain unchanged; exports containing credentials still force mode 0600.
- Treat a service rename on a unique port/protocol as the same open port while preserving distinct services in older snapshots.
- Warn when per-service probe timeouts differ between history records or snapshots, using the recorded scan timeout for older services without an explicit budget.
- Give connect probes a 0.3s budget, warn when compared scans used different timeouts or backends, and scale the full-prefix nmap deadline with host count.
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
