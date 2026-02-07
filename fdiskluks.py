#!/usr/bin/env python3

import logging
import os
import sys
import shutil
import subprocess
from subprocess import Popen, PIPE
import json
import pandas as pd
# from inputastring import input_string # Replaced by ui.input.Input
# import cursesprint # Not used
# from cursesscrollmenu import menu # Replaced by CursesMenu or direct input

from ui.input import Input
from ui.printer import CursedPrinter
from cryptsetup_table import crypt_options_digest
from utils import test_crypt_options
from gpg_table import test_gpg_options, gpg_options_digest # These are utility functions now
from dd_table import test_dd_options, dd_options_digest # These are utility functions now
from block_device_class_table import block_digest # Import the function directly
import curses # Need to import curses for curses.wrapper and key constants

# Global app instances will be managed within main_curses
# print_app = CursedPrint() # Replaced by CursedPrinter instance
# print_app.start() # Replaced by CursedPrinter instance
# print_app.start_print() # Not needed with CursedPrinter

def return_blockdev_name():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        # printer.display_text([f"Error running lsblk: {e.stderr}"], color_pair=2) # Use printer if available
        logging.error(f"Error running lsblk: {e.stderr}")
        return {"blockdevices": []}
    except json.JSONDecodeError:
        # printer.display_text(["Error decoding lsblk JSON output."], color_pair=2)
        logging.error("Error decoding lsblk JSON output.")
        return {"blockdevices": []}


def check_uefi(printer: CursedPrinter):
    if os.path.exists("/sys/firmware/efi"): 
        printer.display_text(["booted UEFI"])
    else: 
        printer.display_text(["booted BIOS"])

def return_pandas():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        data = json.loads(process.stdout)
        df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
        df = (pd 
            .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
            .drop(columns=[0, "children"])
            .fillna("")
            .reset_index(drop=True)
            ) 
        return df
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk for pandas: {e.stderr}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output for pandas.")
        return pd.DataFrame()

class BlockDevice:
    def __init__(self, block_devices):
        self.block_devices = block_devices.get("blockdevices", [])
        for device in self.block_devices:
                for key, value in block_devices.items():
                        setattr(self, key, value)

        def __iter__(self):
                for value in self.block_devices.values():
                        yield value

        def blockdeviceiter(self):
                return iter(self.block_device.values())

def fdisk_process(printer: CursedPrinter, stdscr, pandas_block_devices): 
    printer.display_text(["fdisk process about to be run on selected block device"])
    printer.display_text(["please select exactly one block device"])
    # block_digest is from block_device_class_table.py and needs refactoring too
    # Assuming block_digest will return a list of selected devices
    selected_device = block_digest(stdscr, printer, pandas_block_devices) # Pass printer and stdscr
    
    if not selected_device:
        printer.display_text(["No device selected for fdisk."], color_pair=2)
        return

    # Assuming block_device_json_only is available or generated.
    block_device_json_only = return_blockdev_name()
    block_device_selection_list = BlockDevice(block_device_json_only)

    found_match = False
    for item in block_device_selection_list.block_devices:
        if item['path'] == str(selected_device[0]):
            printer.display_text(["successfully matched input string to device path"])
            printer.display_text([str(item)])
            printer.display_text([str(item['path'])])
            try:
                subprocess.run(['sudo', 'fdisk', selected_device[0]], check=True)
                printer.display_text([f"fdisk completed on {selected_device[0]}"])
                found_match = True
            except subprocess.CalledProcessError as e:
                printer.display_text([f"Error running fdisk on {selected_device[0]}: {e.stderr}"], color_pair=2)
            break
    if not found_match:
        printer.display_text(["no match <press enter>"])


def mkfs_vfat(printer: CursedPrinter, stdscr, pandas_block_devices):
    printer.display_text(["the selected usb key will now be formatted to fat32 using mkfs"])
    printer.display_text(["from the prompt menu select the path for said device"])
    # block_digest needs stdscr and printer
    format_block_device = block_digest(stdscr, printer, pandas_block_devices)
    if not format_block_device:
        printer.display_text(["No device selected for mkfs.vfat."], color_pair=2)
        return

    try:
        subprocess.run(['mkfs.vfat', '-F32', format_block_device[0]], check=True)
        printer.display_text(["successfully formatted device -F32"])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error running mkfs.vfat on {format_block_device[0]}: {e.stderr}"], color_pair=2)


def variable_dictionary(printer: CursedPrinter, input_handler: Input):
    printer.display_text(["please enter the number of entries to enter n: "])
    n_str = input_handler.input_string("Enter n: ")
    
    dictionary = {}
    if n_str.isdigit():
        n = int(n_str)
        printer.display_text(["now enter key value pair followed by <: enter > of each item in dictionary <: press enter >"])
        for _ in range(n):
            key = input_handler.input_string("Enter key: ")
            value = input_handler.input_string(f"Enter value for {key}: ")
            dictionary[key] = value
    else:
        printer.display_text(["Invalid input for n. Returning empty dictionary."], color_pair=2)
    return dictionary

def mkdir(printer: CursedPrinter, directory_name: str):
    try:
        subprocess.run(['mkdir', '-v', directory_name], check=True)
        printer.display_text([f"Successfully created directory: {directory_name}"])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error creating directory {directory_name}: {e.stderr}"], color_pair=2)

def mount(printer: CursedPrinter, mount_point: str, device: str):
    try:
        subprocess.run(['mount', '-v', '-t', mount_point, device], check=True) # Assuming mount_point is filesystem type
        printer.display_text([f"Successfully mounted {device} to {mount_point}"])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error mounting {device} to {mount_point}: {e.stderr}"], color_pair=2)


def gpg_tty(printer: CursedPrinter): 
    try:
        subprocess.run(['export', 'GPG_TTY=$(tty)'], shell=True, check=True) # shell=True for export
        printer.display_text(["GPG_TTY set successfully."])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error setting GPG_TTY: {e.stderr}"], color_pair=2)


def luks_key(printer: CursedPrinter, s_efi_dir: str):
    # This command uses pipes, so Popen is more appropriate or carefully constructed shell=True
    # For simplicity and error handling, breaking it down or using shell=True
    command = f"dd if=/dev/urandom bs=8388607 count=1 | gpg --symmetric --cipher-algo AES256 --output {s_efi_dir}/luks-key.gpg"
    try:
        subprocess.run(command, shell=True, check=True)
        printer.display_text(["LUKS key created successfully."])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error creating LUKS key: {e.stderr}"], color_pair=2)

def luks_process_prefab(printer: CursedPrinter, luks_dictionary, luks_device: str):              
    try:
        luks_process_cmd = ['cryptsetup', '--cipher', luks_dictionary.cipher, '--key-size', luks_dictionary.keysize, '--hash', luks_dictionary.hash, '--key-file', luks_dictionary.keyfile, 'luksFormat', luks_device]
        subprocess.run(luks_process_cmd, check=True)
        printer.display_text(["LUKS format completed successfully."])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error formatting LUKS device: {e.stderr}"], color_pair=2)

def luks_key_decrypt(printer: CursedPrinter, s_efi_dir: str, variable_crypt_options, luks_device: str, physical_volume_name: str):
    # This command uses pipes, so Popen is more appropriate or carefully constructed shell=True
    command = f"sudo gpg --decrypt {s_efi_dir}/luks-key.gpg | cryptsetup {variable_crypt_options[0]} luksOpen {luks_device} {physical_volume_name}"
    try:
        subprocess.run(command, shell=True, check=True)
        printer.display_text(["LUKS key decrypted and opened successfully."])
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error decrypting/opening LUKS device: {e.stderr}"], color_pair=2)

# Main entry point for the curses application
def main_curses(stdscr):
    printer = CursedPrinter(stdscr)
    input_handler = Input(printer)

    printer.display_text(["Initializing fdiskluks setup..."])
    check_uefi(printer)

    # Re-fetch pandas_block_devices inside the curses context
    pandas_block_devices = return_pandas()
    if pandas_block_devices.empty:
        printer.display_text(["No block devices found. Exiting."], color_pair=2)
        stdscr.getch() # Wait for user to acknowledge
        return

    block_device_json_only = return_blockdev_name()
    block_device_selection_list = BlockDevice(block_device_json_only)

    printer.display_text(["showing all available block devices"])
    printer.display_text(str(pandas_block_devices).splitlines())

    # Placeholder for user interaction, assume values are collected manually or via another UI
    # fdisk_process(printer, stdscr, pandas_block_devices) # Requires further UI refactoring

    # Example calls with placeholders for user interaction
    # format_block_device = block_digest(stdscr, printer, pandas_block_devices) # Need to implement actual block_digest usage
    # mkfs_vfat(printer, stdscr, pandas_block_devices)

    # Example usage for variable_dictionary
    # user_dict = variable_dictionary(printer, input_handler)
    # printer.display_text([f"User provided dictionary: {user_dict}"])

    # Simulating s (EFI directory name)
    s_efi_dir = input_handler.input_string("Enter EFI directory name: ")
    mkdir(printer, s_efi_dir)
    mount(printer, "vfat", "/dev/some_efi_partition") # Placeholder device and type

    # Luks setup
    # luks_dictionary_prefab values
    luks_dictionary_values = {
        "cipher": input_handler.input_string("Enter LUKS cipher (e.g., aes-xts): "),
        "keysize": input_handler.input_string("Enter LUKS keysize (e.g., 512): "),
        "hash" : input_handler.input_string("Enter LUKS hash (e.g., sha256): "),
        "keyfile" : input_handler.input_string("Enter LUKS keyfile path (e.g., /keyfile): "),
    }
    luks_dictionary_obj = LuksContainer(luks_dictionary_values)
    luks_device_path = input_handler.input_string("Enter LUKS device path (e.g., /dev/sdaX): ")

    luks_process_prefab(printer, luks_dictionary_obj, luks_device_path)
    luks_key(printer, s_efi_dir) # Requires s_efi_dir

    physical_volume_name = input_handler.input_string("Enter LVM physical volume name: ")

    crypt_options = test_crypt_options() # From utils
    variable_crypt_options = crypt_options_digest(stdscr, printer, crypt_options) # Assuming crypt_options_digest is refactored

    luks_key_decrypt(printer, s_efi_dir, variable_crypt_options, luks_device_path, physical_volume_name)

    printer.display_text(["fdiskluks script completed. Press any key to exit."])
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main_curses)