#!/bin/bash

# verify_env.sh
# Script to verify the development environment setup

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error message
error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# Function to print warning message
warning() {
    echo -e "${YELLOW}! $1${NC}"
}

# Function to check version
check_version() {
    local version=$1
    if [[ $version =~ ^Python\ 3\.11\.[0-9]+$ ]]; then
        return 0
    fi
    return 1
}

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    error "Virtual environment not found. Please create it using Python 3.11:
    /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv"
fi

# Activate virtual environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    warning "Virtual environment not activated. Attempting to activate..."
    source .venv/bin/activate
    if [ $? -eq 0 ]; then
        success "Virtual environment activated"
    else
        error "Failed to activate virtual environment"
    fi
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1)
if check_version "$PYTHON_VERSION"; then
    success "Python version is correct: $PYTHON_VERSION"
else
    error "Wrong Python version: $PYTHON_VERSION. Please use Python 3.11.x"
fi

# Check pip version and location
PIP_VERSION=$(pip --version)
success "Using pip: $PIP_VERSION"

# Verify package installation
if pip list | grep -q "python-network-discovery-tool"; then
    success "Package is installed"
else
    warning "Package not installed. Installing..."
    pip install -e .
    if [ $? -ne 0 ]; then
        error "Failed to install package"
    fi
    success "Package installed successfully"
fi

# Check required dependencies
REQUIRED_PACKAGES=(
    "pytest"
    "pytest-cov"
    "python-nmap"
    "redis"
    "openpyxl"
    "jinja2"
    "paramiko"
    "PyMySQL"
    "python-libnmap"
    "ijson"
)

echo "Checking required dependencies..."
MISSING_PACKAGES=()
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! pip list | grep -qi "^$package"; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
    success "All required dependencies are installed"
else
    warning "Installing missing dependencies: ${MISSING_PACKAGES[*]}"
    pip install "${MISSING_PACKAGES[@]}"
    if [ $? -eq 0 ]; then
        success "Dependencies installed successfully"
    else
        error "Failed to install dependencies"
    fi
fi

# Verify imports
echo "Verifying package imports..."
if python -c "import network_discovery" 2>/dev/null; then
    success "Package imports successfully"
else
    error "Failed to import package. Please check your installation"
fi

# Run basic test
echo "Running basic test verification..."
if pytest -v tests/test_device.py::TestDevice::test_init_minimal > /dev/null 2>&1; then
    success "Test verification passed"
else
    error "Test verification failed"
fi

# Final status report
echo -e "\n${GREEN}Environment Verification Summary:${NC}"
echo -e "  ${GREEN}•${NC} Python Version: $PYTHON_VERSION"
echo -e "  ${GREEN}•${NC} Pip: $PIP_VERSION"
echo -e "  ${GREEN}•${NC} Virtual Environment: $VIRTUAL_ENV"
echo -e "  ${GREEN}•${NC} Package: Installed and importable"
echo -e "  ${GREEN}•${NC} Dependencies: All required packages installed"
echo -e "  ${GREEN}•${NC} Tests: Basic verification passed"

echo -e "\n${YELLOW}Remember:${NC} Always activate the virtual environment with:"
echo -e "source .venv/bin/activate"
