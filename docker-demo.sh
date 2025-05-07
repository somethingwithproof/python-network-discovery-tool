#!/bin/bash
# Script to demonstrate Docker functionality

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Network Discovery Tool - Docker Demo${NC}"
echo "======================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p output templates

# Build the Docker image
echo -e "\n${YELLOW}Step 1: Building Docker image...${NC}"
docker-compose build
echo -e "${GREEN}✓${NC} Docker image built successfully"

# Show help information
echo -e "\n${YELLOW}Step 2: Showing help information...${NC}"
docker-compose run --rm network-discovery --help
echo -e "${GREEN}✓${NC} Help information displayed"

# Run a test with the test service
echo -e "\n${YELLOW}Step 3: Running a simple test...${NC}"
docker-compose run --rm test -xvs tests/test_scanner.py::TestNmapDeviceScanner::test_is_alive
echo -e "${GREEN}✓${NC} Test completed"

# Start a development shell
echo -e "\n${YELLOW}Step 4: Starting a development shell...${NC}"
echo "This will open a bash shell in the container."
echo "You can run commands like 'pytest', 'flake8', etc."
echo "Type 'exit' to exit the shell."
echo ""
echo -e "${BLUE}Press Enter to continue or Ctrl+C to exit...${NC}"
read

# Use PS1='$ ' to make the prompt simpler for demo purposes
docker-compose run --rm dev bash -c "PS1='$ ' bash"

echo -e "\n${GREEN}Docker demo completed successfully!${NC}"
echo "You can now use the containerized network discovery tool for your network scans."
echo "Example: docker-compose run network-discovery 192.168.1.0/24"
echo "Or use the Makefile: make run ARGS='192.168.1.0/24'"
