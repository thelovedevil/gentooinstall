#!/usr/bin/env python3

import curses
import subprocess
import logging
import json
import pandas as pd
import sys # For sys.exit
import moby_dick # Assuming moby_dick provides text strings

# Import the new UI components
from ui.printer import CursedPrinter
from ui.input import Input

# Import utility functions
from utils import test_crypt_options, test_dd_options, test_gpg_options

# Import refactored table classes if their digest methods are still directly needed
# For now, I will assume their digest methods will be called with stdscr and printer
# from cryptsetup_table import crypt_options_digest
# from block_device_class_table import block_digest
# from dd_class_table import dd_options_digest
# from gpg_class_table import gpg_options_digest

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


# Placeholder for a simpler way to get options, assuming actual selection is curses-driven
def get_options_from_user(printer: CursedPrinter, input_handler: Input, prompt_message: str):
    printer.display_text([prompt_message])
    num_entries_str = input_handler.input_string("Enter number of entries: ")
    options = []
    try:
        num_entries = int(num_entries_str)
        for i in range(num_entries):
            key = input_handler.input_string(f"Enter option {i+1} key: ")
            value = input_handler.input_string(f"Enter option {i+1} value: ")
            options.append(key)
            options.append(value)
    except ValueError:
        printer.display_text(["Invalid number entered. Returning empty options."], color_pair=2)
    return options


def block_options_input(printer: CursedPrinter, input_handler: Input, stdscr):
    printer.display_text(["filling in block_options process"])
    # TODO: Integrate with refactored block_digest from block_device_class_table
    # For now, direct user input
    return get_options_from_user(printer, input_handler, "Enter block device options:")


def crypt_options_input(printer: CursedPrinter, input_handler: Input, stdscr):
    printer.display_text(["filling in crypt_options process"])
    # TODO: Integrate with refactored crypt_options_digest from cryptsetup_table
    # For now, direct user input
    return get_options_from_user(printer, input_handler, "Enter cryptsetup options:")


def overwrite_options_input(printer: CursedPrinter, input_handler: Input, stdscr):
    printer.display_text(["filling in overwrite_options process"])
    # TODO: Integrate with refactored dd_options_digest
    return get_options_from_user(printer, input_handler, "Enter overwrite options (e.g., if=/dev/zero bs=4M count=10):")


def dd_options_input(printer: CursedPrinter, input_handler: Input, stdscr):
    printer.display_text(["filling in dd_options process"])
    # TODO: Integrate with refactored dd_options_digest
    return get_options_from_user(printer, input_handler, "Enter dd options (e.g., if=/dev/urandom bs=8M count=1):")


def gpg_options_input(printer: CursedPrinter, input_handler: Input, stdscr):
    printer.display_text(["filling in gpg_options process"])
    printer.display_text(["!!! gpg_options must be written in for accuracy using 'r' command !!!"])
    # TODO: Integrate with refactored gpg_options_digest
    return get_options_from_user(printer, input_handler, "Enter gpg options (e.g., --symmetric --cipher-algo AES256):")


def key_file_input(printer: CursedPrinter, input_handler: Input, stdscr):
    printer.display_text(["now entering key file input from prior cryptsetup keyfile"])
    printer.display_text(["simply enter the same value as used for prior key file"])
    # TODO: Integrate with refactored gpg_options_digest for selection
    return get_options_from_user(printer, input_handler, "Enter key file options (e.g., --keyfile /path/to/key):")


def name_physical_volume(printer: CursedPrinter, input_handler: Input): 
    printer.display_text(['lastly please enter a name for a logical volume management (LVM) physical volume <: press enter >'])
    name = input_handler.input_string("LVM physical volume name: ")
    return name    


def gpg_tty(printer: CursedPrinter): 
    try:
        # 'export' is a shell built-in, so shell=True is required
        subprocess.run(['export', 'GPG_TTY=$(tty)'], shell=True, check=True)
        printer.display_text(["GPG_TTY set successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting GPG_TTY: {e.stderr.strip()}")
        printer.display_text([f"Error setting GPG_TTY: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("Shell command 'export' not found. This might indicate a problem with shell environment.")
        printer.display_text(["Error: 'export' command not found. Cannot set GPG_TTY."], color_pair=2)

def over_write(printer: CursedPrinter, overwrite_command: list[str]):
    printer.display_text(["Starting disk overwrite..."])
    try:
        # Use Popen to handle piping for better error reporting
        dd_proc = subprocess.Popen(['sudo', 'dd'] + overwrite_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = dd_proc.communicate()
        if dd_proc.returncode != 0:
            raise subprocess.CalledProcessError(dd_proc.returncode, dd_proc.args, stdout, stderr)
        
        sync_proc = subprocess.run(['sync'], check=True, capture_output=True, text=True)
        printer.display_text(["Disk overwrite and sync completed successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during overwrite (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error during overwrite: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("dd or sync command not found. Ensure they are installed and in PATH.")
        printer.display_text(["Error: dd or sync command not found."], color_pair=2)


def luks_key(printer: CursedPrinter, dd_command: list[str], gpg_command: list[str], s_efi_dir: str):
    printer.display_text(["running process for luks key creation"])
    try:
        dd_proc = subprocess.Popen(['sudo', 'dd'] + dd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        gpg_cmd_full = ['gpg'] + gpg_command + [f"{s_efi_dir}/luks-key.gpg"]
        gpg_proc = subprocess.run(gpg_cmd_full, stdin=dd_proc.stdout, check=True, capture_output=True, text=True)
        dd_proc.stdout.close() # Allow dd_proc to receive SIGPIPE if gpg exits
        dd_proc.wait() # Wait for dd to finish
        if dd_proc.returncode != 0:
            raise subprocess.CalledProcessError(dd_proc.returncode, dd_proc.args, dd_proc.stdout, dd_proc.stderr)
        
        printer.display_text(["LUKS key created successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during LUKS key creation (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error during LUKS key creation: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("dd or gpg command not found. Ensure they are installed and in PATH.")
        printer.display_text(["Error: dd or gpg command not found."], color_pair=2)


def luks_process_one(printer: CursedPrinter, crypt_command: list[str], block_command: list[str]):              
    printer.display_text(["Starting LUKS format process..."])
    try:
        luks_process_cmd = ['sudo', 'cryptsetup'] + crypt_command + ['luksFormat'] + block_command
        subprocess.run(luks_process_cmd, check=True, capture_output=True, text=True)
        printer.display_text(["LUKS format completed successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during LUKS format (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error during LUKS format: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("cryptsetup command not found. Ensure it is installed and in PATH.")
        printer.display_text(["Error: cryptsetup command not found."], color_pair=2)


def luks_process_two(printer: CursedPrinter, key_file_command: list[str], block_command: list[str], physical_volume_name: str, s_efi_dir: str):
    printer.display_text(["Starting LUKS decrypt and open process..."])
    try:
        gpg_decrypt_cmd = ['sudo', 'gpg', '--decrypt', f"{s_efi_dir}/luks-key.gpg"]
        gpg_proc = subprocess.Popen(gpg_decrypt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        cryptsetup_open_cmd = ['cryptsetup'] + key_file_command + ['luksOpen'] + block_command + [physical_volume_name]
        cryptsetup_proc = subprocess.run(cryptsetup_open_cmd, stdin=gpg_proc.stdout, check=True, capture_output=True, text=True)
        gpg_proc.stdout.close()
        gpg_proc.wait()
        if gpg_proc.returncode != 0:
            raise subprocess.CalledProcessError(gpg_proc.returncode, gpg_proc.args, gpg_proc.stdout, gpg_proc.stderr)
        
        printer.display_text(["LUKS device decrypted and opened successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during LUKS decrypt/open (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error during LUKS decrypt/open: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("gpg or cryptsetup command not found. Ensure they are installed and in PATH.")
        printer.display_text(["Error: gpg or cryptsetup command not found."], color_pair=2)


# Main entry point for the curses application
def main_curses(stdscr):
    printer = CursedPrinter(stdscr)
    input_handler = Input(printer)

    printer.display_text([moby_dick.welcome_message()]) # Assuming moby_dick provides a welcome message
    printer.display_text(["Initializing options input run..."])

    # Collect inputs using the refactored input functions
    block_command = block_options_input(printer, input_handler, stdscr)
    dd_command = dd_options_input(printer, input_handler, stdscr)
    gpg_command = gpg_options_input(printer, input_handler, stdscr)
    overwrite_command = overwrite_options_input(printer, input_handler, stdscr)
    crypt_command = crypt_options_input(printer, input_handler, stdscr)
    key_file_command = key_file_input(printer, input_handler, stdscr)
    physical_volume_name = name_physical_volume(printer, input_handler)

    printer.display_text(["Collected Commands:"])
    printer.display_text([f"Block Command: {block_command}"])
    printer.display_text([f"DD Command: {dd_command}"])
    printer.display_text([f"GPG Command: {gpg_command}"])
    printer.display_text([f"Overwrite Command: {overwrite_command}"])
    printer.display_text([f"Crypt Command: {crypt_command}"])
    printer.display_text([f"Key File Command: {key_file_command}"])
    printer.display_text([f"Physical Volume Name: {physical_volume_name}"])

    # Execute commands with error handling
    gpg_tty(printer)
    over_write(printer, overwrite_command)
    luks_key(printer, dd_command, gpg_command, create_efi.s) # create_efi.s needs to be passed or derived
    luks_process_one(printer, crypt_command, block_command)
    luks_process_two(printer, key_file_command, block_command, physical_volume_name, create_efi.s) # create_efi.s needs to be passed or derived

    printer.display_text(["All options input processes completed. Press any key to exit."])
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main_curses)