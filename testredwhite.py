#!/usr/bin/env python3

import curses
from moby_dick import output_crime
import textwrap
from ui.ascii_art import AsciiArt
from utils import test_crypt_options
from ui.printer import CursedPrinter
from ui.input import Input


string = output_crime()
sources = string

if __name__ == "__main__":
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        input_handler = Input(printer)
        
        # Display the sources text
        printer.display_text(str(sources).splitlines(), row=0, col=0)

        # Example of displaying ascii art
        ascii_art_obj = AsciiArt("resources/genkai.jpg") # Use relative path
        # Assuming we want to display it on the right side of the screen
        max_y, max_x = stdscr.getmaxyx()
        ascii_art_x_pos = max_x // 2 + 5 # Place it roughly in the middle-right
        printer.display_ascii_art(
            ascii_art_obj,
            row=0,
            col=ascii_art_x_pos,
            width_ratio=0.4, # Take 40% of the screen width
            height_ratio=0.9 # Take 90% of the screen height
        )

        # Example of taking some input
        name = input_handler.input_string("Enter your name: ")
        printer.display_text([f"Hello, {name}!"], row=max_y - 2, col=0)
        printer.display_text(["Press 'q' to quit, or use WASD to scroll the image."], row=max_y - 1, col=0)

        # Main loop to keep the display active and handle input
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            # Handle scrolling for ASCII art
            printer.handle_input(key) 
            
            # Refresh the screen to show any changes (e.g., scrolling)
            stdscr.refresh()

    curses.wrapper(main_curses)