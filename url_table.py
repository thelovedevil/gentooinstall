#!/usr/bin/env python3

import curses
import locale

locale.setlocale(locale.LC_ALL, '')
import subprocess
import json
import pandas as pd
import logging

from ui.printer import CursedPrinter
from ui.table import Table
import beautiful_soup_test # Assuming sources_ is a variable from here

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


def return_pandas_dictionary(sources):
    # The 'sources' here is expected to be a pandas DataFrame from beautiful_soup_test
    return sources


def url_digest(stdscr, printer: CursedPrinter, sources):
    x = 0
    special_address_list = []

    dictionary_variable = return_pandas_dictionary(sources)

    if dictionary_variable.empty:
        printer.display_text(["No URLs found to display."], color_pair=2)
        stdscr.getch()
        return []

    max_y, max_x = stdscr.getmaxyx()
    table_height = max_y - 5 # Leave space for messages
    table_width = max_x # Use full width
    
    table_widget = Table(stdscr, printer, dictionary_variable, table_height, table_width)
    
    printer.display_text(["URL Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
    
    while (x != ord('q')):
        stdscr.clear() # Clear screen to redraw everything
        printer.display_text(["URL Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)

        table_widget.display() # Draw the table
        
        x = stdscr.getch()

        table_result = table_widget.handle_input(x) # Handle table input

        if table_result == 'quit':
            break
        elif table_result is not None:
            selected_item_value = table_result.iloc[0] # Assuming first column is the value we want (the URL)
            special_address_list.append(selected_item_value)
            printer.display_text([f"Selected: {selected_item_value}"])
            stdscr.getch() # Pause to show selection
            # Clear selection message (optional)
            printer.display_text([" " * max_x], row=max_y - 2, col=0) 
        
    return special_address_list


if __name__ == "__main__":
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        
        printer.display_text(["Loading URLs..."])
        # Assuming beautiful_soup_test.sources_ returns a pandas DataFrame
        # TODO: Refactor beautiful_soup_test to ensure it returns a DataFrame
        sources = beautiful_soup_test.sources_ 
        
        selected_urls = url_digest(stdscr, printer, sources)
        printer.display_text([f"Selected URLs: {selected_urls}"])
        printer.display_text(["Press any key to exit."])
        stdscr.getch()

    curses.wrapper(main_curses)