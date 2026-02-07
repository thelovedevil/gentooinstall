#!/usr/bin/env python3
import curses
import locale

locale.setlocale(locale.LC_ALL, '')
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

        dictionary_variable = sources

        if dictionary_variable.empty:
            printer.display_text(["No block devices found to display."], color_pair=2)
            stdscr.getch()
            return []

        max_y, max_x = stdscr.getmaxyx()
        table_height = max_y - 2
        table_width = max_x // 2
        
        table_widget = Table(stdscr, printer, dictionary_variable, table_height, table_width)
        
        ascii_art_obj = AsciiArt("resources/keiko.jpg")
        ascii_art_x_pos = max_x // 2 + 5

        def draw_screen():
            stdscr.clear()
            printer.display_text(["Block Device Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
            
            table_widget.display()
            
            printer.display_ascii_art(
                ascii_art_obj,
                row=0,
                col=ascii_art_x_pos,
                width_ratio=0.4,
                height_ratio=0.9
            )
            stdscr.refresh()

        draw_screen() # Initial draw
        
        while (x != ord('q')):
            x = stdscr.getch()

            table_result = table_widget.handle_input(x)

            if table_result == 'quit':
                break
            elif table_result is not None:
                selected_item_value = table_result['PATH'] # Assuming 'PATH' is the column with device path
                special_address_list.append(selected_item_value)
                printer.display_text([f"Selected: {selected_item_value}"])
                stdscr.getch()
            
            # Handle ASCII art scrolling
            if (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                printer.handle_input(x)
            
            draw_screen() # Redraw after every input

        return special_address_list


if __name__ == "__main__":
    app = Block_Table()
    app.start()
