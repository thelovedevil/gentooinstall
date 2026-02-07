#!/usr/bin/env python3

import curses
from moby_dick import output_crime
import textwrap
from ui.printer import CursedPrinter
from ui.ascii_art import AsciiArt


string = output_crime() # Get some example text

if __name__ == "__main__":
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        
        # Display the text
        text_lines = str(string).splitlines()
        printer.display_text(text_lines, row=0, col=0)

        # Display ASCII art
        ascii_art_obj = AsciiArt("resources/tero.jpg") # Use relative path
        max_y, max_x = stdscr.getmaxyx()
        ascii_art_x_pos = max_x // 2 + 5 # Place it roughly in the middle-right
        printer.display_ascii_art(
            ascii_art_obj,
            row=0,
            col=ascii_art_x_pos,
            width_ratio=0.4, # Take 40% of the screen width
            height_ratio=0.9 # Take 90% of the screen height
        )

        printer.display_text(["Press 'q' to quit, or use WASD to scroll the image."], row=max_y - 1, col=0)

        # Main loop to keep the display active and handle input
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            # Handle scrolling for ASCII art
            printer.handle_input(key) 
            
            stdscr.refresh() # Refresh the screen to show any changes (e.g., scrolling)

    curses.wrapper(main_curses)