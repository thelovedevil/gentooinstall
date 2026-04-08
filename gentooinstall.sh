#!/bin/bash
# System-agnostic Gentoo Installer Bootstrap Script

set -e

# Define the virtual environment directory
VENV_DIR=".venv"

echo "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# 1. Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Upgrade pip and install dependencies
echo "Installing/Updating dependencies from requirements.txt..."
"$VENV_DIR/bin/python3" -m pip install --upgrade pip
"$VENV_DIR/bin/python3" -m pip install -r requirements.txt

# 3. Run the main menu
echo "Starting Gentoo Installer..."
"$VENV_DIR/bin/python3" main_menu.py
