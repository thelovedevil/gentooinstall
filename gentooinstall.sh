#!/bin/bash
set -e

echo "Preparing installer environment..."

# 1. Create the temporary virtual environment
python3 -m venv /tmp/gentoo_installer_env

# 2. Activate it (redirects 'python3' and 'pip' to this environment)
source /tmp/gentoo_installer_env/bin/activate

# 3 Install curses-menu into this temporary environment
pip install --quiet -r requirements.txt

# 4. Run your main menu script
echo "Starting Gentoo Installer...."
python3 main_menu.py

# 5 Clean up by deactivating the environment once the script is closed
deactivate
