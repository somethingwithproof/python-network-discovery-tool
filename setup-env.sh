#!/bin/bash
# Script to set up environment variables for Docker

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Network Discovery Tool - Environment Setup${NC}"
echo "================================================="
echo ""
echo -e "${BLUE}This script will help you set up environment variables for Docker.${NC}"
echo "These variables will be used for authentication when scanning devices."
echo ""

# Create .env file if it doesn't exist
ENV_FILE=".env"
touch $ENV_FILE

# SSH User
echo -e "${YELLOW}SSH User Configuration${NC}"
echo "------------------------"
read -p "Enter SSH username [zenossmon]: " ssh_user
ssh_user=${ssh_user:-zenossmon}

# SSH Key File
echo ""
echo -e "${YELLOW}SSH Key File Configuration${NC}"
echo "----------------------------"
default_key="$HOME/.ssh/id_rsa.pub"
read -p "Enter SSH key file path [$default_key]: " ssh_key_file
ssh_key_file=${ssh_key_file:-$default_key}

# MySQL User
echo ""
echo -e "${YELLOW}MySQL Configuration${NC}"
echo "---------------------"
read -p "Enter MySQL username (leave empty to skip): " mysql_user

# MySQL Password
if [ ! -z "$mysql_user" ]; then
    read -s -p "Enter MySQL password: " mysql_password
    echo ""
fi

# Write to .env file
echo "# Environment variables for Network Discovery Tool" > $ENV_FILE
echo "# Generated on $(date)" >> $ENV_FILE
echo "" >> $ENV_FILE
echo "# SSH Configuration" >> $ENV_FILE
echo "SSH_USER=$ssh_user" >> $ENV_FILE
echo "SSH_KEY_FILE=$ssh_key_file" >> $ENV_FILE
echo "" >> $ENV_FILE
echo "# MySQL Configuration" >> $ENV_FILE
echo "MYSQL_USER=$mysql_user" >> $ENV_FILE
echo "MYSQL_PASSWORD=$mysql_password" >> $ENV_FILE

echo ""
echo -e "${GREEN}Environment variables have been saved to $ENV_FILE${NC}"
echo "You can now run Docker commands with these environment variables:"
echo ""
echo "  docker-compose run network-discovery 192.168.1.0/24"
echo ""
echo "Or use the Makefile:"
echo ""
echo "  make run ARGS='192.168.1.0/24'"
echo ""
echo -e "${YELLOW}Note:${NC} The .env file contains sensitive information and should not be committed to version control."
