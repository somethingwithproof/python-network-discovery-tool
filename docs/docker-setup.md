# Docker Setup for Network Discovery Tool

This document provides detailed information about using Docker with the Network Discovery Tool.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system
- Basic knowledge of Docker and containerization

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/thomasvincent/python-network-discovery-tool.git
   cd python-network-discovery-tool
   ```

2. Set up environment variables (optional):
   ```bash
   ./setup-env.sh
   ```

3. Build and run the Docker container:
   ```bash
   docker-compose run network-discovery 192.168.1.0/24
   ```

4. Or use the Makefile:
   ```bash
   make run ARGS='192.168.1.0/24'
   ```

## Testing the Docker Setup

We provide a script to test your Docker setup:

```bash
./test-docker-setup.sh
```

This script will:
1. Build the Docker image
2. Run a test scan on your localhost
3. Generate a report in the output directory

## Docker Services

The `docker-compose.yml` file defines several services:

### network-discovery

This service runs the network discovery tool:

```bash
docker-compose run network-discovery [NETWORK] [OPTIONS]
```

Examples:
```bash
# Scan a network
docker-compose run network-discovery 192.168.1.0/24

# Scan a single device
docker-compose run network-discovery 192.168.1.1

# Generate a CSV report
docker-compose run network-discovery 192.168.1.0/24 -f csv
```

### dev

This service provides a development environment with all dependencies installed:

```bash
docker-compose run dev
```

This will start a bash shell in the container where you can run commands like:

```bash
# Run tests
pytest

# Run linters
flake8 src tests
black src tests
isort src tests
mypy src tests
```

### test

This service runs the test suite:

```bash
docker-compose run test
```

You can also run specific tests:

```bash
# Run a specific test file
docker-compose run test tests/test_scanner.py

# Run a specific test
docker-compose run test tests/test_scanner.py::TestNmapDeviceScanner::test_scan_device
```

## Environment Variables

The following environment variables can be set in the `.env` file or passed directly to Docker Compose:

| Variable | Description | Default |
|----------|-------------|---------|
| SSH_USER | Username for SSH authentication | zenossmon |
| SSH_KEY_FILE | Path to SSH key file | ~/.ssh/id_rsa.pub |
| MYSQL_USER | Username for MySQL authentication | (empty) |
| MYSQL_PASSWORD | Password for MySQL authentication | (empty) |

Example:
```bash
SSH_USER=admin MYSQL_PASSWORD=secret docker-compose run network-discovery 192.168.1.0/24
```

## Volumes

The Docker setup mounts several volumes:

| Container Path | Host Path | Description |
|----------------|-----------|-------------|
| /app/output | ./output | Directory for generated reports |
| /app/templates | ./templates | Directory for HTML templates |
| /root/.ssh | ~/.ssh | SSH keys for authentication (read-only) |

## Makefile

A Makefile is provided for convenience:

```bash
# Build the Docker image
make build

# Run the network discovery tool
make run ARGS='192.168.1.0/24'

# Run tests
make test

# Start a development shell
make dev

# Run linters
make lint

# Clean up
make clean
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with SSH keys, make sure your SSH key files have the correct permissions:

```bash
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

### Network Access

The Docker container needs access to the network you're scanning. If you're scanning an external network, make sure your Docker network settings allow this.

### Missing Dependencies

If you encounter errors about missing dependencies, try rebuilding the Docker image:

```bash
docker-compose build --no-cache
```

## Advanced Configuration

### Custom Dockerfile

You can create a custom Dockerfile based on the provided one:

```dockerfile
FROM network-discovery:latest

# Add your custom configurations here
RUN apt-get update && apt-get install -y your-package

# Add custom scripts
COPY custom-script.sh /app/
```

### Custom Docker Compose

You can create a custom Docker Compose file:

```yaml
version: '3.8'

services:
  custom-service:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./custom-output:/app/output
    environment:
      - SSH_USER=custom-user
```

## Security Considerations

- The Docker container mounts your SSH keys as read-only, but be careful with sensitive information.
- Avoid running the container with `--privileged` flag unless necessary.
- Consider using a dedicated SSH key pair for network scanning.
- Be cautious when scanning networks you don't own or have permission to scan.
