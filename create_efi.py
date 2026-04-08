#!/usr/bin/env python3

import locale
import subprocess

locale.setlocale(locale.LC_ALL, '')
from block_device_class_table import Block_Table
import json
import pandas as pd
from ui.input import Input
import moby_dick
from ui.printer import CursedPrinter # New import for the refactored printer

# Input and printer apps need to be initialized within curses.wrapper
# For now, I will use temporary standard print for debugging
# print_app = CursedPrinter(stdscr) # This needs to be done within a curses context
# input_app = Input(print_app) # Input also needs a printer



def variable_dictionary(printer: CursedPrinter, input_handler: Input):
    from ui.input import CursesTextScrollWithInput
    
    scroll_app = CursesTextScrollWithInput(printer)
    
    content = moby_dick.entries() + "\n" + moby_dick.key_value()
    
    # This will show the text, allow scrolling, and then ask for dict input
    dictionary = scroll_app.display_and_get_dict(content, ascii_image_path="Pictures/black_white005.jpg")
    
    if not dictionary:
        printer.display_text(["No dictionary received. Returning empty dictionary."])
        return {}
    
    if isinstance(dictionary, str):
        # Fallback if user entered something else
        return {dictionary: dictionary}
        
    printer.display_text([f"Final dictionary: {dictionary}"])
    return dictionary



def main(printer: CursedPrinter, input_handler: Input):
    string = moby_dick.following()
    printer.display_text(string.splitlines())
    
    directory_list = variable_dictionary(printer, input_handler)
    
    if directory_list:
        mkdir(printer, input_handler, directory_list)
        mount(printer, input_handler, directory_list)
    else:
        printer.display_text(["No directories provided. Skipping operations."])

def mkdir(printer: CursedPrinter, input_handler: Input, directory_list: dict):
    printer.display_text([f"Directory map: {directory_list}"])
    s = input_handler.input_string("Enter directory path to create (e.g. /mnt/gentoo/boot/efi): ")
    
    if s:
        subprocess.run(['sudo', 'mkdir', '-v', '-p', s])
        printer.display_text([f"mkdir -p {s} run"])

def mount(printer: CursedPrinter, input_handler: Input, directory_list: dict):
    printer.display_text([f"Directory map: {directory_list}"])
    
    dev = input_handler.input_string("Enter block device path (e.g. /dev/sda1): ")
    mnt = input_handler.input_string("Enter mount point path (e.g. /mnt/gentoo/boot/efi): ")
    
    if dev and mnt:
        subprocess.run(['sudo', 'mount', '-v', dev, mnt])
        printer.display_text([f"mount {dev} {mnt} run"])


if __name__ == "__main__":
    import curses
    
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        input_handler = Input(printer)
        main(printer, input_handler)

    curses.wrapper(main_curses)
