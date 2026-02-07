#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
import curses
import json # for url_table.url_digest output processing
import pandas as pd # for url_table.url_digest output processing

from ui.printer import CursedPrinter
# from ui.input import Input # If input is ever needed for this script

# Assuming url_table.py and beautiful_soup_test.py are also refactored
# For now, let's assume url_table.url_digest returns a list of URLs
import url_table
import beautiful_soup_test # Assuming sources_ is a variable from here

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


def root(printer: CursedPrinter):
    printer.display_text(["Attempting to switch to root user..."])
    try:
        # 'sudo su root' is often used for interactive shell. For scripting, it's better
        # to ensure the script itself is run with sudo, or use specific sudo commands.
        # If interactive shell is intended, the script would block here.
        # For non-interactive use, assume commands will be prefixed with sudo.
        subprocess.run(["sudo", "true"], check=True) # Check if sudo works
        printer.display_text(["Sudo access confirmed."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get sudo access: {e.stderr.strip()}")
        printer.display_text(["Error: Failed to get sudo access. Please run script with sudo or configure it."], color_pair=2)
        sys.exit(1) # Exit if cannot get root privileges


def change_mnt_gentoo(printer: CursedPrinter, path: str = "/mnt/gentoo/"):
    printer.display_text([f"Changing directory to {path}"])
    try:
        os.chdir(path)
        printer.display_text([f"Successfully changed directory to {path}."])
    except OSError as e:
        logging.error(f"Failed to change directory to {path}: {e}")
        printer.display_text([f"Error: Failed to change directory to {path}. Ensure it exists."], color_pair=2)
        sys.exit(1)


def wget_stage3_tar_xz(printer: CursedPrinter, url_list: list, index: int = 0):
    if not url_list or index >= len(url_list):
        printer.display_text([f"Error: URL list is empty or index {index} is out of bounds."], color_pair=2)
        return False
    
    url = "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/" + str(url_list[index])
    printer.display_text([f"Attempting to download: {url}"])
    try:
        subprocess.run(["wget", "-c", url], check=True)
        printer.display_text([f"Download of {url_list[index]} successful."])
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Wget command failed for {url_list[index]} (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error downloading {url_list[index]}: {e.stderr.strip()}"], color_pair=2)
        return False
    except FileNotFoundError:
        logging.error("Wget command not found. Please ensure wget is installed and in your PATH.")
        printer.display_text(["Error: Wget command not found. Please install wget."], color_pair=2)
        return False


def gpg_key_recv(printer: CursedPrinter, key_id: str = "13EBBDBEDE7A12775DFDB1BABB572E0E2D182910"):
    printer.display_text([f"Receiving GPG key {key_id}..."])
    try:
        subprocess.run(["gpg", "--keyserver", "hkps://keys.gentoo.org", "--recv-keys", key_id], check=True)
        printer.display_text([f"GPG key {key_id} received successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to receive GPG key {key_id}: {e.stderr.strip()}")
        printer.display_text([f"Error receiving GPG key {key_id}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("gpg command not found. Please ensure GnuPG is installed and in your PATH.")
        printer.display_text(["Error: GPG command not found. Please install GnuPG."], color_pair=2)


def gpg_key_fingerprint(printer: CursedPrinter, key_id: str = "2D182910"):
    printer.display_text([f"Verifying GPG key fingerprint for {key_id}..."])
    try:
        subprocess.run(["gpg", "--fingerprint", key_id], check=True)
        printer.display_text([f"GPG key fingerprint for {key_id} verified."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to verify GPG key fingerprint for {key_id}: {e.stderr.strip()}")
        printer.display_text([f"Error verifying GPG key fingerprint for {key_id}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("gpg command not found.")
        printer.display_text(["Error: GPG command not found."], color_pair=2)


def gpg_import(printer: CursedPrinter, key_file: str = "/usr/share/openpgp-keys/gentoo-release.asc"):
    printer.display_text([f"Importing GPG key from {key_file}..."])
    try:
        subprocess.run(["gpg", "--import", key_file], check=True)
        printer.display_text([f"GPG key from {key_file} imported successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to import GPG key from {key_file}: {e.stderr.strip()}")
        printer.display_text([f"Error importing GPG key from {key_file}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("gpg command not found.")
        printer.display_text(["Error: GPG command not found."], color_pair=2)


def gpg_check(printer: CursedPrinter, filename: str):
    printer.display_text([f"Verifying GPG signature for {filename}..."])
    try:
        subprocess.run(["gpg", "--verify", filename], check=True)
        printer.display_text([f"GPG signature for {filename} verified successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to verify GPG signature for {filename}: {e.stderr.strip()}")
        printer.display_text([f"Error verifying GPG signature for {filename}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("gpg command not found.")
        printer.display_text(["Error: GPG command not found."], color_pair=2)


def sha256sum_check(printer: CursedPrinter, filename: str):
    printer.display_text([f"Verifying SHA256 checksum for {filename}..."])
    try:
        subprocess.run(["sha256sum", "--check", filename], check=True)
        printer.display_text([f"SHA256 checksum for {filename} verified successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to verify SHA256 checksum for {filename}: {e.stderr.strip()}")
        printer.display_text([f"Error verifying SHA256 checksum for {filename}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("sha256sum command not found. Ensure it is installed and in your PATH.")
        printer.display_text(["Error: sha256sum command not found."], color_pair=2)


def test_unpack(printer: CursedPrinter, stage3_filename: str):
    printer.display_text([f"Unpacking {stage3_filename}..."])
    tar_command = f"tar xvJpf {stage3_filename} --xattrs-include='*.*' --numeric-owner"
    try:
        # Use shell=True for complex shell commands like those with globs or brace expansion
        subprocess.run(tar_command, shell=True, check=True)
        printer.display_text([f"{stage3_filename} unpacked successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to unpack {stage3_filename}: {e.stderr.strip()}")
        printer.display_text([f"Error unpacking {stage3_filename}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("tar command not found. Ensure it is installed and in your PATH.")
        printer.display_text(["Error: tar command not found."], color_pair=2)


# Main entry point for the curses application
def main_curses(stdscr):
    printer = CursedPrinter(stdscr)
    # input_handler = Input(printer) # If input is needed beyond getch for this script

    printer.display_text(["Starting Gentoo Stage3 Download and Verification..."])

    # Get special_address_list from url_table.url_digest
    # This requires url_table.url_digest to be refactored to work without direct stdscr access
    # or to be wrapped in its own curses context if it requires user interaction.
    # For now, we will create a mock list for demonstration.
    # TODO: Properly integrate url_table.url_digest
    
    # Assuming url_table.url_digest returns a list of relevant filenames
    try:
        # Assuming url_table.url_digest can be called with a printer and stdscr
        # if it needs user interaction for selection, otherwise it should just return data.
        # For simplicity in this refactoring, let's assume it can be called without it for getting the list.
        # This is a temporary assumption that needs to be verified after url_table is refactored.
        # Here's how it would look if it was a data-only function:
        stage3_urls_data = url_table.url_digest(None, beautiful_soup_test.sources_) # Assuming sources_ from beautiful_soup_test
        special_address_list = [item[0] for item in stage3_urls_data.to_numpy()] # Extracting filenames
        
    except Exception as e:
        logging.error(f"Could not retrieve stage3 URLs: {e}")
        printer.display_text([f"Error: Could not retrieve stage3 URLs: {e}"], color_pair=2)
        special_address_list = ["stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz"] # Fallback

    if not special_address_list:
        printer.display_text(["No stage3 URL found. Exiting."], color_pair=2)
        stdscr.getch()
        return

    # Assuming stage3_filename is the first item in the list for now
    stage3_filename = special_address_list[0]
    sha_filename = special_address_list[2] # Assuming DIGESTS file is at index 2
    sha256_digest_filename = special_address_list[3] if len(special_address_list) > 3 else stage3_filename + ".sha256"


    # 1. Switch to root and change directory
    root(printer)
    change_mnt_gentoo(printer)

    # 2. Download stage3 and related files
    if not wget_stage3_tar_xz(printer, special_address_list, 0): # stage3.tar.xz
        printer.display_text(["Failed to download stage3 archive. Aborting."], color_pair=2)
        stdscr.getch()
        return
    if not wget_stage3_tar_xz(printer, special_address_list, 1): # stage3.tar.xz.contents
        printer.display_text(["Failed to download stage3.tar.xz.contents. Aborting."], color_pair=2)
        stdscr.getch()
        return
    if not wget_stage3_tar_xz(printer, special_address_list, 2): # stage3.tar.xz.DIGESTS
        printer.display_text(["Failed to download stage3.tar.xz.DIGESTS. Aborting."], color_pair=2)
        stdscr.getch()
        return
    if not wget_stage3_tar_xz(printer, special_address_list, 3): # stage3.tar.xz.sha256
        printer.display_text(["Failed to download stage3.tar.xz.sha256. Aborting."], color_pair=2)
        stdscr.getch()
        return

    # 3. GPG Key management
    gpg_key_recv(printer)
    gpg_key_fingerprint(printer)
    gpg_import(printer)

    # 4. Verification
    # Use the actual filename from the list or a hardcoded one for now
    # The original code uses a hardcoded name for verification, which is brittle.
    # stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.sha256
    # Let's assume the correct sha256 digest filename is derived from stage3_filename
    
    gpg_check(printer, sha256_digest_filename)
    sha256sum_check(printer, sha256_digest_filename)
    gpg_check(printer, sha_filename) # Also check DIGESTS file
    # gpg_key_verify(printer, sha256_digest_filename) # Redundant with gpg_check

    # 5. Unpack stage3
    test_unpack(printer, stage3_filename)

    printer.display_text(["Stage3 download and verification completed. Press any key to exit."])
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main_curses)