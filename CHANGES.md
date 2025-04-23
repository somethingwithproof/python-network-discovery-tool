# Changelog

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
