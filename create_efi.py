#!/usr/bin/env python3



import subprocess
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
    string = moby_dick.entries()
    printer.display_text(string.splitlines())
    string_two = moby_dick.key_value()
    printer.display_text(string_two.splitlines())

    # This part was for CursedPrintRedWhiteUserInput which is now gone.
    # We will just proceed to ask for input.
    printer.display_text(["No dictionary received. Please enter manually."])
    n_str = input_handler.input_string("Enter number of entries (n): ")
    
    dictionary = {}
    if n_str.isdigit():
        n = int(n_str)
        for _ in range(n):
            key = input_handler.input_string("Enter key: ")
            value = input_handler.input_string(f"Enter value for {key}: ")
            dictionary[key] = value
    else:
        printer.display_text(["Invalid input for number of entries. Returning empty dictionary."])
    
    printer.display_text([f"Final dictionary: {dictionary}"])
    return dictionary



def main(printer: CursedPrinter, input_handler: Input):
    block_dev = Block_Table() # This might need to be initialized in a curses context as well.
                              # For now, let's assume Block_Table itself doesn't directly
                              # use curses, or it gets stdscr passed to it.

    string = moby_dick.following()
    printer.display_text(string.splitlines())
    
    mkdir(printer, input_handler)
    mount(printer, input_handler)

def mkdir(printer: CursedPrinter, input_handler: Input):
    directory_list = variable_dictionary(printer, input_handler)
    printer.display_text([f"Directory list for mkdir: {directory_list}"])
    # TODO: Replace 'menu' with a curses-aware selection mechanism, perhaps from curses_menu
    # For now, we will just take the first item as a placeholder or prompt for input
    # Assuming directory_list is a dictionary and we need a value from it
    if directory_list:
        s = input_handler.input_string("Enter directory name to create (from list): ") # Assuming the user picks from the list
        if s not in directory_list.values(): # Basic validation
            printer.display_text(["Warning: Entered directory not in list. Using first available."])
            s = list(directory_list.values())[0] if directory_list.values() else "efi"
    else:
        s = input_handler.input_string("Enter directory name to create: ")
        
    printer.display_text([f"Selected item: {s}"])
    subprocess.run(['sudo', 'mkdir', '-v', '-p', s])
    printer.display_text(["mkdir run"])

def mount(printer: CursedPrinter, input_handler: Input):
    directory_list = variable_dictionary(printer, input_handler)
    printer.display_text([f"Directory list for mount: {directory_list}"])
    # TODO: Replace 'menu' with a curses-aware selection mechanism
    # For now, we will just take the first item as a placeholder or prompt for input
    if directory_list:
        s = input_handler.input_string("Enter directory to mount (from list): ")
        if s not in directory_list.values(): # Basic validation
            printer.display_text(["Warning: Entered directory not in list. Using first available."])
            s = list(directory_list.values())[0] if directory_list.values() else "efi"
    else:
        s = input_handler.input_string("Enter directory to mount: ")
        
    printer.display_text([f"Selected item: {s}"])
    subprocess.run(['sudo', 'mount', '-v', '-t', s])
    printer.display_text(["mount run"])


if __name__ == "__main__":
    import curses
    
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        input_handler = Input(printer)
        main(printer, input_handler)

    curses.wrapper(main_curses)
