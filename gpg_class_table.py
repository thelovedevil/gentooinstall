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
from utils import test_gpg_options
from ui.table import Table # New import

# Global variables will be initialized within curses.wrapper context

class Crypt_Table(): # This class seems unrelated to GpG_Table, but is in the same file.
                      # It needs separate refactoring to use CursedPrinter if it's used.
                      # For now, I will leave its curses initialization as is, but it's a TODO.
    def __init__(self):
        self.screen = None

    def start(self):
        # curses.wrapper(self.main_curses) # TODO: Refactor Crypt_Table as well
        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(True)
            self.main(self.screen)
        finally:
            self.screen.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()

    def main(self, stdscr):
        self.screen = stdscr
        self.screen.clear()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        # self.crypt_options_digest(sources_testcrypt) # sources_testcrypt is not defined
        # This part of Crypt_Table seems broken or incomplete without sources_testcrypt
        pass


def gpg_options_digest(stdscr, printer: CursedPrinter, sources, ascii_image_path="Pictures/black_white004.jpg"):
    if sources is None:
        sources = test_gpg_options()
        
    x = 0
    special_address_list = []

    dictionary_variable = sources

    if dictionary_variable.empty:
        printer.display_text(["No options found to display."], color_pair=2)
        stdscr.getch()
        return []

    max_y, max_x = stdscr.getmaxyx()
    table_height = max_y - 2 # Allocate most of the screen for the table
    table_width = max_x // 2
    
    table_widget = Table(stdscr, printer, dictionary_variable, table_height, table_width)
    
    ascii_art_obj = AsciiArt(ascii_image_path)
    ascii_art_x_pos = max_x // 2 + 5

    def draw_screen():
        stdscr.clear()
        printer.display_text(["GPG Options Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
        
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
            selected_item_value = list(table_result.values())[0] if isinstance(table_result, dict) else table_result.iloc[0]
            special_address_list.append(selected_item_value)
            printer.display_text([f"Selected: {selected_item_value}"])
            stdscr.getch()
        
        # Handle ASCII art scrolling
        if (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
            printer.handle_input(x)
        
        draw_screen() # Redraw after every input

    return special_address_list

class GpG_Table():
    def __init__(self):
        self.screen = None
        self.printer = None
    
    def start(self):
        curses.wrapper(self.main_curses)

    def main_curses(self, stdscr):
        self.screen = stdscr
        self.printer = CursedPrinter(stdscr)
        sources = test_gpg_options() # Call the utility function
        self.main(stdscr, self.printer, sources)


    def main(self, stdscr, printer: CursedPrinter, sources):
        self.screen = stdscr
        self.printer = printer
        self.screen.clear()
        gpg_options_digest(stdscr, printer, sources)

if __name__ == "__main__":
    app = GpG_Table()
    app.start()
