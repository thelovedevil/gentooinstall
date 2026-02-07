#!/usr/bin/env python3

import curses

from moby_dick import output_crime
import textwrap
from ui.ascii_art import AsciiArt
from utils import test_crypt_options
from ui.printer import CursedPrinter


string = output_crime()
sources = string
if __name__ == "__main__":
    def main(stdscr):
        printer = CursedPrinter(stdscr)
        
        # Determine appropriate width and height for text and ASCII art
        max_y, max_x = stdscr.getmaxyx()
        
        # Text display takes up left portion
        text_width_ratio = 0.6
        text_width = int(max_x * text_width_ratio)
        
        # ASCII art display takes up right portion
        ascii_art_x_pos = text_width + 2 # A small offset
        available_width_for_art = max_x - ascii_art_x_pos
        
        # Display text
        # The splitlines() might introduce empty strings, filter them out if needed
        text_to_display = str(sources).splitlines()
        printer.display_text(text_to_display, row=0, col=0) # Display text starting from top-left

        # Display ASCII art
        ascii_art_obj = AsciiArt("asuka_original_resized.jpg") # Placeholder path
        printer.display_ascii_art(
            ascii_art_obj,
            row=0,
            col=ascii_art_x_pos,
            width_ratio=available_width_for_art / max_x,
            height_ratio=0.9
        )
        
        # Main loop to keep the display active and handle input
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            # Handle scrolling for ASCII art
            printer.handle_input(key) 
            
            # Refresh the screen to show any changes (e.g., scrolling)
            stdscr.refresh()
            # Optionally clear parts of the screen if content overlaps
            # printer.clear_screen() 

    curses.wrapper(main)