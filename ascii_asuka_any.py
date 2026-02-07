#!/usr/bin/env python3

import curses
import locale

locale.setlocale(locale.LC_ALL, '')
from ui.printer import CursedPrinter
from ui.ascii_art import AsciiArt


def main(stdscr):
    # Curses setup is handled by curses.wrapper and CursedPrinter
    printer = CursedPrinter(stdscr)
    
    # Instantiate AsciiArt with the correct path
    ascii_art_obj = AsciiArt("resources/asuka_original_resized.jpg")
    
    # Display ASCII art
    max_y, max_x = stdscr.getmaxyx()
    printer.display_ascii_art(
        ascii_art_obj,
        row=0,
        col=0,
        width_ratio=0.9, # Take 90% of the screen width
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

if __name__ == "__main__":
    curses.wrapper(main)
