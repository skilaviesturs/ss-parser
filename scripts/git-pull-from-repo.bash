#!/bin/bash

# Define color variables
YELLOW="\033[1;33m"
RESET="\033[0m"

# Resolve script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read SSH key name from file into variable
KEY_NAME="$(<"$SCRIPT_DIR/ssh-key.txt")"

# Build full key path
KEY_PATH="$HOME/.ssh/$KEY_NAME"

# Initiate secure session with ssh key
eval "$(ssh-agent -s)" && ssh-add "$KEY_PATH"

# Get updates from git
echo -e "${YELLOW}Pulling updates from git...${RESET}"
cd ~/a-backend && git fetch origin main --depth=1 && git reset --hard origin/main


# End of script
echo -e "🏁 ${YELLOW}Update script completed.${RESET}"