#!/bin/bash
# Script to test the Docker setup by scanning localhost

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing Docker Setup with Local Scan${NC}"
echo "====================================="

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

# Build the Docker image
echo -e "\n${YELLOW}Building Docker image...${NC}"
docker-compose build

# Create output directory if it doesn't exist
mkdir -p output
mkdir -p templates

# Get the local IP address
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}' || echo "127.0.0.1")
else
    # Default to localhost
    LOCAL_IP="127.0.0.1"
fi

echo -e "\n${YELLOW}Detected local IP: ${LOCAL_IP}${NC}"
echo "This will be used for a test scan."

# Run a scan on localhost
echo -e "\n${YELLOW}Running a test scan on localhost...${NC}"
echo "This will only scan your local machine and is safe to run."
echo "Press Ctrl+C to cancel or any key to continue..."
read -n 1 -s

# Run the scan with verbose output
echo -e "\n${YELLOW}Scanning ${LOCAL_IP}...${NC}"
docker-compose run --rm network-discovery "${LOCAL_IP}" -v -f html

# Check if the scan was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Test scan completed successfully!${NC}"
    echo "Check the output directory for the generated report."
    
    # List the output files
    echo -e "\n${YELLOW}Generated files:${NC}"
    ls -la output/
    
    echo -e "\n${GREEN}Docker setup is working correctly.${NC}"
    echo "You can now use the containerized network discovery tool for your network scans."
    echo "Example: docker-compose run network-discovery 192.168.1.0/24"
    echo "Or use the Makefile: make run ARGS='192.168.1.0/24'"
else
    echo -e "\n${RED}Test scan failed.${NC}"
    echo "Please check the error messages above and try again."
fi
