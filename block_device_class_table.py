#!/usr/bin/env python3
import curses
# from curseXcel import Table # Removed
import subprocess
import json
import pandas as pd
from ui.printer import CursedPrinter
from ui.ascii_art import AsciiArt
from ui.table import Table # New import

def return_pandas():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk for pandas: {e.stderr}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output for pandas.")
        return pd.DataFrame()
    except FileNotFoundError:
        logging.error("lsblk command not found. Ensure lsblk is installed and in your PATH.")
        return pd.DataFrame()


class Block_Table():

    def __init__(self):
        self.screen = None
        self.printer = None

    def start(self):
        curses.wrapper(self.main_curses)

    def main_curses(self, stdscr):
        self.screen = stdscr
        self.printer = CursedPrinter(stdscr)
        # Assuming sources is passed or generated here
        sources = return_pandas() # Get data from pandas
        if sources.empty:
            self.printer.display_text(["No block devices found to display."], color_pair=2)
            stdscr.getch()
            return
        self.main(stdscr, self.printer, sources)


    def main(self, stdscr, printer: CursedPrinter, sources):
        self.screen = stdscr
        self.printer = printer
        self.screen.clear()
        self.block_digest(stdscr, printer, sources)

    def block_digest(self, stdscr, printer: CursedPrinter, sources):
        x = 0
        special_address_list = []

        def return_block():
            return sources
        
        new_table = return_block()

        # Instantiate ui.table.Table
        max_y, max_x = stdscr.getmaxyx()
        table_height = max_y // 2 # Allocate half screen height for table
        table_width = max_x // 2  # Allocate half screen width for table
        
        table_widget = Table(stdscr, printer, new_table, table_height, table_width)
        
        ascii_art_obj = AsciiArt("resources/keiko.jpg") # Use relative path
        ascii_art_x_pos = max_x // 2 + 5 # Place it roughly in the middle-right
        
        printer.display_text(["Block Device Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
        
        while (x != ord('q')):
            stdscr.clear() # Clear screen to redraw everything
            printer.display_text(["Block Device Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)

            table_widget.display() # Draw the table
            
            printer.display_ascii_art(
                ascii_art_obj,
                row=0,
                col=ascii_art_x_pos,
                width_ratio=0.4,
                height_ratio=0.9
            ) # Refresh ASCII art
            
            x = stdscr.getch()

            table_result = table_widget.handle_input(x) # Handle table input

            if table_result == 'quit':
                break
            elif table_result is not None:
                selected_item_value = table_result['PATH'] # Assuming 'PATH' is the column with device path
                special_address_list.append(selected_item_value)
                printer.display_text([f"Selected: {selected_item_value}"])
                stdscr.getch() # Pause to show selection
                # Clear selection message (optional)
                printer.display_text([" " * max_x], row=max_y - 2, col=0) 
            
            # Handle scrolling for ASCII art, if not handled by table_widget
            if (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                printer.handle_input(x) # Handle scrolling for ascii art
        return special_address_list


if __name__ == "__main__":
    app = Block_Table()
    app.start()
