#!/usr/bin/env python3

import curses
from curseXcel import Table # Keep for now, but its usage will change
import subprocess
import json
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


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
        # Removed print(df)
        return df
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk for pandas: {e.stderr}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output for pandas.")
        return pd.DataFrame()
    except FileNotFoundError:
        logging.error("lsblk command not found. Ensure lsblk is installed and in your PATH.")
        return pd.DataFrame()


def block_digest(stdscr, printer, sources):
    x = 0
    special_block_list = []

    # The Table class from curseXcel needs significant refactoring or replacement.
    # For now, we will display the raw pandas DataFrame using the new printer.
    printer.display_text(["Available Block Devices:"])
    if not sources.empty:
        printer.display_text(sources.to_string().splitlines())
    else:
        printer.display_text(["No block devices found."])

    printer.display_text(["Use arrow keys to navigate (placeholder), 'q' to quit, Enter to select (placeholder)."])
    
    # Simulate table interaction using input_handler if available, otherwise raw getch
    # For simplicity, let's just make it a quit loop for now
    while ( x != ord('q')):
        stdscr.refresh()
        x = stdscr.getch()
        if x == ord('\n'):
            # Placeholder for selection
            selected_item = input("Enter selected device path (e.g., /dev/sda): ") # Temporarily using basic input
            special_block_list.append(selected_item)
            printer.display_text([f"Selected: {selected_item}"])
        elif x == ord('q'):
            break

    return special_block_list


if __name__ == "__main__":
    from ui.printer import CursedPrinter

    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        # input_handler = Input(printer) # If input is needed beyond getch

        printer.display_text(["Loading block device data..."])
        sources = return_pandas()
        if sources.empty:
            printer.display_text(["Failed to load block device data. Exiting."], color_pair=2)
            stdscr.getch()
            return
        
        selected_devices = block_digest(stdscr, printer, sources)
        printer.display_text([f"Selected devices: {selected_devices}"])
        printer.display_text(["Press any key to exit."])
        stdscr.getch() # Wait for user input before exiting

    curses.wrapper(main_curses)
