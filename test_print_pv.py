#!/usr/bin/env python

import subprocess
import curses
import logging # For logging errors

from ui.printer import CursedPrinter
from ui.input import Input # If input is ever needed
from block_device_class_table import return_pandas # Assuming this is still needed and refactored
import moby_dick # Assuming this is still needed

def pv_display(printer: CursedPrinter):
    try:
        # It's good practice to provide full path for sudo commands in scripts
        # Or ensure sudo is in PATH and the user has NOPASSWD for pvdisplay
        pv_output = subprocess.run(['sudo', 'pvdisplay'], check=True, capture_output=True, text=True).stdout
        printer.display_text(pv_output.splitlines())
    except subprocess.CalledProcessError as e:
        printer.display_text([f"Error running pvdisplay: {e.stderr}"], color_pair=2)
    except FileNotFoundError:
        printer.display_text(["'pvdisplay' command not found. Is LVM installed?"], color_pair=2)

if __name__ == "__main__":
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        input_handler = Input(printer) # Instantiate Input handler

        printer.display_text(["Checking Physical Volumes..."])
        pv_display(printer)
        printer.display_text(["Press any key to exit."])
        stdscr.getch() # Wait for user input before exiting

    curses.wrapper(main_curses)
