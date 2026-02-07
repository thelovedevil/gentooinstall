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
from utils import test_dd_options # Need to import this after moving
from ui.table import Table # New import

# Global variables will be initialized within curses.wrapper context

class Dd_Table():
    def __init__ (self):
        self.screen = None
        self.printer = None
    
    def start(self):
        curses.wrapper(self.main_curses)

    def main_curses(self, stdscr):
        self.screen = stdscr
        self.printer = CursedPrinter(stdscr)
        sources = test_dd_options() # Call the utility function
        self.main(stdscr, self.printer, sources)


    def main(self, stdscr, printer: CursedPrinter, sources):
        self.screen = stdscr
        self.printer = printer
        self.screen.clear()
        self.dd_options_digest(stdscr, printer, sources)
        

    def dd_options_digest(self, stdscr, printer: CursedPrinter, sources):
        x = 0
        special_address_list = []

        dictionary_variable = sources

        if dictionary_variable.empty:
            printer.display_text(["No options found to display."], color_pair=2)
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
            printer.display_text(["DD Options Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
            
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
                selected_item_value = table_result.iloc[0]
                special_address_list.append(selected_item_value)
                printer.display_text([f"Selected: {selected_item_value}"])
                stdscr.getch()
            
            # Handle ASCII art scrolling
            if (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                printer.handle_input(x)
            
            draw_screen() # Redraw after every input

        return special_address_list

if __name__ == "__main__":
    app = Dd_Table()
    app.start()
