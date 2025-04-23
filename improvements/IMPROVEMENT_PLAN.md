# Network Discovery Tool Improvement Plan

## Issues Identified

1. **Redundant Files**: Multiple Python files in the root directory (`mail.py`, `store.py`, `spreadsheet.py`, `database.py`, `devices.py`, `device.py`, `discovery.py`, `discover.py`, `auto-discover.py`) that seem to be older versions or experiments. Some use `Twisted` while the `src` code uses `asyncio`.

2. **Inconsistent Architecture**: The presence of `discovery.py` and `discover.py` in the root alongside `src/network_discovery/core/discovery.py` is confusing.

3. **Test Coverage**: Current coverage is around 62.57%, with significant gaps in:
   - Error handling paths in most modules
   - Service check logic in `scanner.py` (SSH, SNMP, MySQL interactions)
   - `RedisRepository`, `EmailNotificationService`, and `ReportGenerator` implementations
   - Core `DeviceDiscoveryService` logic

4. **Repository Implementations**: 
   - `RedisRepository.get_all` uses `redis.keys("device:*")`, which is discouraged in production Redis environments
   - `JsonFileRepository._load_data` loads the entire file into memory, which could be inefficient for large datasets

5. **Error Handling**: 
   - Too broad exception handling in many places
   - Inconsistent logging levels
   - Lack of specific error feedback to users

6. **Dependency Management**: 
   - Inconsistencies between `setup.py` and `requirements.txt`
   - Outdated dependencies

## Improvement Plan

### 1. Code Cleanup

- Remove redundant files from the root directory
- Consolidate all code into the `src` structure
- Remove `ez_setup.py` as it's no longer needed

### 2. Architecture Improvements

- Ensure consistent architecture throughout the codebase
- Improve the `DeviceManager` implementation to use a dictionary for faster lookups
- Enhance error handling with more specific exceptions and consistent logging
- Improve the CLI interface with better input validation and error feedback

### 3. Test Coverage Improvements

- Add tests for error handling paths
- Add tests for `RedisRepository`, `EmailNotificationService`, and `ReportGenerator`
- Add tests for the core `DeviceDiscoveryService` logic
- Add integration tests for Redis, MySQL, and other external services

### 4. Repository Improvements

- Refactor `RedisRepository.get_all` to avoid using `KEYS` command
- Optimize `JsonFileRepository._load_data` for large datasets

### 5. Dependency Management

- Consolidate dependencies between `setup.py` and `requirements.txt`
- Update outdated dependencies

### 6. Documentation

- Update `README.md` to reflect the current structure and usage
- Add more detailed documentation for each module

## Implementation Steps

1. **Clean up redundant files**
2. **Improve core components**
3. **Enhance error handling**
4. **Improve test coverage**
5. **Update dependencies**
6. **Update documentation**
