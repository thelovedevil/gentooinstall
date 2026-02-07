#!/usr/bin/env python3

import curses
from curses_menu import CursesMenu
from ui.printer import CursedPrinter
from ui.ascii_art import AsciiArt


def main(stdscr):
    # Curses setup is handled by curses.wrapper and CursedPrinter
    printer = CursedPrinter(stdscr)
    
    # Instantiate AsciiArt with the correct path
    ascii_art_obj = AsciiArt("resources/asuka_original_resized.jpg")
    
    # Create the CursesMenu instance
    menu = CursesMenu(title="Menu", subtitle="Select an option", width=curses.COLS // 2, ascii_art=ascii_art_obj)
    
    # This example demonstrates how you might display some initial text
    printer.display_text(["Welcome to the asuka.ascii menu!"], row=0, col=0)
    printer.display_text(["Use arrow keys to navigate, 'q' to quit."], row=1, col=0)
    
    # The CursesMenu handles its own main loop, including drawing itself and the ascii art
    # The ascii_art is passed to CursesMenu directly, and CursesMenu uses its internal printer
    # to draw it.
    menu.start()
    _ = menu.join() # Wait for the menu to exit

if __name__ == "__main__":
    curses.wrapper(main)