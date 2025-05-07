#!/bin/bash
# Script to test the Docker setup for the network discovery tool

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing Docker setup for Network Discovery Tool${NC}"
echo "======================================================="

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

echo -e "${GREEN}✓${NC} Docker and Docker Compose are installed"

# Build the Docker image
echo -e "\n${YELLOW}Building Docker image...${NC}"
docker-compose build

echo -e "${GREEN}✓${NC} Docker image built successfully"

# Create output directory if it doesn't exist
mkdir -p output
mkdir -p templates

# Run the help command to verify the container works
echo -e "\n${YELLOW}Testing container with help command...${NC}"
docker-compose run --rm network-discovery --help

echo -e "\n${GREEN}✓${NC} Container is working correctly"

# Run a test with the test service
echo -e "\n${YELLOW}Running tests in container...${NC}"
docker-compose run --rm test -xvs tests/test_scanner.py

echo -e "\n${GREEN}✓${NC} Tests completed"

# Start a development shell
echo -e "\n${YELLOW}Starting development shell...${NC}"
echo "Type 'exit' to exit the shell"
docker-compose run --rm dev

echo -e "\n${GREEN}All tests passed! Docker setup is working correctly.${NC}"
echo "You can now use the containerized network discovery tool."
echo "Example: docker-compose run network-discovery 192.168.1.0/24"
