#!/usr/bin/env python3

import subprocess
import locale

locale.setlocale(locale.LC_ALL, '')
import json
import pandas as pd
import curses
import logging

from ui.printer import CursedPrinter
from block_device_class_table import block_digest # Import block_digest

import moby_dick # Assuming moby_dick provides text strings

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


def return_pandas():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk for pandas: {e.stderr}")
        return {"blockdevices": []}
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output for pandas.")
        return {"blockdevices": []}
    except FileNotFoundError:
        logging.error("lsblk command not found. Please ensure lsblk is installed and in your PATH.")
        return {"blockdevices": []}


def fdisk_process(stdscr, printer: CursedPrinter, pandas_block_devices: pd.DataFrame): 
    string = moby_dick.fdisk_process()
    printer.display_text(string.splitlines())
    
    selected_device_list = block_digest(stdscr, printer, pandas_block_devices)
    
    if not selected_device_list:
        printer.display_text(["No device selected for cfdisk. Aborting."], color_pair=2)
        return

    selected_device_path = selected_device_list[0] # Assuming block_digest returns a list and we take the first
    
    printer.display_text([f"Starting cfdisk on {selected_device_path}..."])
    try:
        subprocess.run(['sudo', 'cfdisk', selected_device_path], check=True)
        printer.display_text([f"cfdisk completed successfully on {selected_device_path}."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running cfdisk on {selected_device_path} (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error running cfdisk on {selected_device_path}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("cfdisk command not found. Ensure it is installed and in your PATH.")
        printer.display_text(["Error: cfdisk command not found."], color_pair=2)


if __name__ == "__main__":
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        # input_handler = Input(printer) # Uncomment if input is needed

        printer.display_text(["Initializing fdisk process..."])
        
        pandas_block_devices = return_pandas()
        if pandas_block_devices.empty:
            printer.display_text(["Failed to load block device data. Exiting."], color_pair=2)
            stdscr.getch()
            return
        
        fdisk_process(stdscr, printer, pandas_block_devices)
        
        printer.display_text(["fdisk_process script completed. Press any key to exit."])
        stdscr.getch()

    curses.wrapper(main_curses)
