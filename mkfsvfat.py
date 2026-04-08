#!/usr/bin/env python3

import subprocess
import json
import pandas as pd
import curses
import logging

from ui.printer import CursedPrinter
from block_device_class_table import Block_Table # Block_Table should be refactored already
from utils import return_pandas

# Configure logging


def mkfs_vfat(stdscr, printer: CursedPrinter, block_table_app: Block_Table, pandas_block_devices: pd.DataFrame):
    printer.display_text(["Formatting a block device to FAT32 (mkfs.vfat)."])
    printer.display_text(["Please select the device to format."])

    # The block_digest method now requires stdscr and printer
    format_block_device_list = block_table_app.block_digest(stdscr, printer, pandas_block_devices)
    
    if not format_block_device_list:
        printer.display_text(["No device selected for mkfs.vfat. Aborting."], color_pair=2)
        return

    selected_device = format_block_device_list[0] # Assuming block_digest returns a list and we take the first
    
    try:
        subprocess.run(['sudo', 'mkfs.vfat', '-F32', selected_device], check=True)
        printer.display_text([f"Successfully formatted {selected_device} to FAT32."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error formatting {selected_device} (exit code {e.returncode}): {e.stderr.strip()}")
        printer.display_text([f"Error formatting {selected_device}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("mkfs.vfat command not found. Ensure it is installed and in your PATH.")
        printer.display_text(["Error: mkfs.vfat command not found."], color_pair=2)


if __name__ == "__main__":
    from ui.printer import CursedPrinter # Ensure CursedPrinter is imported

    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        # input_handler = Input(printer) # Uncomment if input beyond getch is needed

        printer.display_text(["Initializing mkfsvfat process..."])
        
        block_table_app = Block_Table()
        block_table_app.main_curses(stdscr) # Initialize Block_Table's curses context

        # Ensure block_table_app's printer is set after main_curses is called
        # This is a bit tricky, ideally Block_Table would return its printer or share it
        # For now, we will pass the main_curses printer to mkfs_vfat.
        
        pandas_block_devices = return_pandas()
        if pandas_block_devices.empty:
            printer.display_text(["Failed to load block device data. Exiting mkfsvfat."], color_pair=2)
            stdscr.getch()
            return
        
        mkfs_vfat(stdscr, printer, block_table_app, pandas_block_devices)
        
        printer.display_text(["mkfsvfat script completed. Press any key to exit."])
        stdscr.getch()

    curses.wrapper(main_curses)
