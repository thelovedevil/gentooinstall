#!/usr/bin/env python3

import curses
# from curseXcel import Table # Removed
import subprocess
import json
import pandas as pd
import logging

from ui.printer import CursedPrinter
from ui.table import Table # New import

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


class DictionaryDevice:
    def __init__(self, dictionary_devices):
        self.dictionary_devices = dictionary_devices.get("blockdevices",[])
        for device in self.dictionary_devices:
                for key, value in dictionary_devices.items():
                        setattr(self, key, value)

        def __iter__(self):
            for device in self.dictionary_devices:
                for value in self.dictionary_devices.values():
                        yield value

        def dictionarydeviceiter(self):
            return iter(self.dictionary_devices.values())

def dictionary_test_table(dictionary_command_line):
    return DictionaryDevice(dictionary_command_line)


def run_lsblk():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk: {e.stderr}")
        return {"blockdevices": []}
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output.")
        return {"blockdevices": []}
    except FileNotFoundError:
        logging.error("lsblk command not found. Please ensure lsblk is installed and in your PATH.")
        return {"blockdevices": []}

def return_pandas():
    data = run_lsblk()
    if not data or not data.get("blockdevices"):
        return pd.DataFrame()
    
    df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
    df = (pd 
        .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
        .drop(columns=[0, "children"])
        .fillna("")
        .reset_index(drop=True)
        )
    return df

def return_blockdev_name():
    return run_lsblk()


def main(stdscr, printer: CursedPrinter, new_table: pd.DataFrame):
    x = 0
    # Removed redundant curses init and setup as CursedPrinter handles it

    block_devices = return_blockdev_name() # Get block devices in raw JSON form
    dict_table = dictionary_test_table(block_devices) # Not used after initial dict_table = new_table.

    m = 0
    # The index() function and associated logic seems incomplete or specific to a very particular table structure
    # For now, we will skip this and assume new_table is already prepared.
    
    # Instantiate ui.table.Table
    max_y, max_x = stdscr.getmaxyx()
    table_height = max_y - 2
    table_width = max_x
    
    table_widget = Table(stdscr, printer, new_table, table_height, table_width)
    
    def draw_screen():
        stdscr.clear()
        printer.display_text(["Block Device Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
        table_widget.display()
        stdscr.refresh()

    draw_screen() # Initial draw
    
    while (x != ord('q')):
        x = stdscr.getch()

        table_result = table_widget.handle_input(x)

        if table_result == 'quit':
            break
        elif table_result is not None:
            selected_item_value = table_result['PATH'] # Assuming 'PATH' is the column with device path
            printer.display_text([f"Selected: {selected_item_value}"])
            stdscr.getch() # Pause to show selection
        
        draw_screen() # Redraw after every input
if __name__ == "__main__":
    from ui.printer import CursedPrinter # Ensure CursedPrinter is imported
    from ui.input import Input # Ensure Input is imported if needed in main

    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        input_handler = Input(printer) # Instantiate Input handler
        
        printer.display_text(["Loading block device data for cursestable..."])
        new_table = return_pandas()
        if new_table.empty:
            printer.display_text(["Failed to load block device data. Exiting."], color_pair=2)
            stdscr.getch()
            return
        
        main(stdscr, printer, new_table) # Pass printer and new_table to main
        
        printer.display_text(["cursestable script completed. Press any key to exit."])
        stdscr.getch() # Wait for user input before exiting

    curses.wrapper(main_curses)