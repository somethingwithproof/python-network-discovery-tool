# Implementation Plan for Network Discovery Tool Improvements

This document outlines the step-by-step plan for integrating the improvements into the main codebase.

## 1. Preparation

1. Create a new branch for the improvements:
   ```bash
   git checkout -b improvements
   ```

2. Remove redundant files from the root directory:
   ```bash
   git rm mail.py store.py spreadsheet.py database.py devices.py device.py discovery.py discover.py auto-discover.py test_redis.py test_scan.py ez_setup.py
   ```

## 2. Update Dependencies

1. Replace the current requirements.txt with the improved version:
   ```bash
   cp improvements/requirements.txt requirements.txt
   ```

2. Update setup.py with the improved version:
   ```bash
   cp improvements/setup.py setup.py
   ```

## 3. Implement Core Improvements

### 3.1. Domain Layer

1. Update the DeviceManager implementation with the improved version:
   ```bash
   cp improvements/device_manager_improved.py src/network_discovery/domain/device_manager.py
   ```

### 3.2. Infrastructure Layer

1. Update the JsonFileRepository implementation:
   ```bash
   cp improvements/json_repository_improved.py src/network_discovery/infrastructure/repository.py
   ```

2. Update the RedisRepository implementation in the repository.py file:
   - Add the improved RedisRepository class from improvements/redis_repository_improved.py to the repository.py file

### 3.3. Interface Layer

1. Update the CLI implementation:
   ```bash
   cp improvements/cli_improved.py src/network_discovery/interfaces/cli.py
   ```

## 4. Update Tests

1. Add the new tests for the improved components:
   ```bash
   cp improvements/test_redis_repository_improved.py tests/test_redis_repository.py
   cp improvements/test_json_repository_improved.py tests/test_json_repository.py
   cp improvements/test_device_manager_improved.py tests/test_device_manager.py
   cp improvements/test_cli_improved.py tests/test_cli.py
   ```

## 5. Update Documentation

1. Update the README.md with the improved version:
   ```bash
   cp improvements/README.md README.md
   ```

2. Update other documentation files as needed.

## 6. Testing

1. Run the tests to ensure everything works correctly:
   ```bash
   pytest
   ```

2. Run the linters to ensure code quality:
   ```bash
   flake8 src tests
   black src tests
   isort src tests
   mypy src tests
   ```

3. Run tox to test against multiple Python versions:
   ```bash
   tox
   ```

## 7. Manual Testing

1. Test the CLI with various options:
   ```bash
   python -m network_discovery.interfaces.cli 127.0.0.1
   python -m network_discovery.interfaces.cli 192.168.1.0/24 -f csv -o ./output
   ```

2. Test the API with a simple script:
   ```python
   import asyncio
   from network_discovery.core.discovery import DeviceDiscoveryService
   from network_discovery.infrastructure.scanner import NmapDeviceScanner
   from network_discovery.infrastructure.repository import JsonFileRepository
   from network_discovery.infrastructure.notification import ConsoleNotificationService
   from network_discovery.infrastructure.report import ReportGenerator

   async def main():
       scanner = NmapDeviceScanner()
       repository = JsonFileRepository("devices.json")
       notification_service = ConsoleNotificationService()
       report_service = ReportGenerator("./output", "./templates")
       discovery_service = DeviceDiscoveryService(
           scanner, repository, notification_service, report_service
       )
       device = await discovery_service.discover_device("127.0.0.1")
       print(device.status())

   if __name__ == "__main__":
       asyncio.run(main())
   ```

## 8. Finalization

1. Commit the changes:
   ```bash
   git add .
   git commit -m "feat: implement improvements to network discovery tool"
   ```

2. Create a pull request for review.

## 9. Post-Implementation

1. Update the package version in src/network_discovery/__init__.py.
2. Create a new release on GitHub.
3. Publish the updated package to PyPI:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Notes

- The implementation should be done incrementally, testing each component after it's updated.
- If any issues are found during testing, they should be fixed before proceeding to the next step.
- The improvements should maintain backward compatibility with the existing API.
