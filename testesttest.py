#!/usr/bin/env python3

import subprocess
import logging
import curses # Need for curses.wrapper and stdscr

# Assuming beautiful_soup_test.py is refactored and its sources_ is accessible or passed
# For now, let's create a mock sources_ for demonstration
class MockSources:
    def __init__(self):
        self.some_data = ["item1", "item2", "item3"]
    def to_numpy(self):
        return [[x] for x in self.some_data] # Simulate numpy array from pandas

# sources_ = MockSources() # TODO: Integrate with actual beautiful_soup_test.sources_

# Import the refactored block_digest from block_device_table
from block_device_table import block_digest
from ui.printer import CursedPrinter

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


def stty(printer: CursedPrinter):
    printer.display_text(["Setting stty to sane mode..."])
    try:
        subprocess.run(['stty', 'sane'], check=True)
        printer.display_text(["stty set to sane."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting stty sane: {e.stderr.strip()}")
        printer.display_text([f"Error setting stty sane: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("stty command not found. Ensure it is installed and in your PATH.")
        printer.display_text(["Error: stty command not found."], color_pair=2)


def test_list(stdscr, printer: CursedPrinter, sources_data):
    printer.display_text(["Running test_list..."])
    # block_digest expects stdscr, printer, sources
    test_result = block_digest(stdscr, printer, sources_data)
    printer.display_text([f"test_list result: {test_result}"])
    return test_result

def test_list_two(stdscr, printer: CursedPrinter, sources_data):
    printer.display_text(["Running test_list_two..."])
    # block_digest expects stdscr, printer, sources
    test_result = block_digest(stdscr, printer, sources_data)
    printer.display_text([f"test_list_two result: {test_result}"])
    return test_result


if __name__ == "__main__":
    def main_curses(stdscr):
        printer = CursedPrinter(stdscr)
        # input_handler = Input(printer) # If input is ever needed

        printer.display_text(["Starting testesttest script..."])
        
        # Load sources_ data
        # TODO: Integrate with actual beautiful_soup_test.sources_
        sources_data = MockSources() 

        stty(printer)

        list_one_result = test_list(stdscr, printer, sources_data)
        printer.display_text([f"List one result: {list_one_result}"])

        list_two_result = test_list_two(stdscr, printer, sources_data)
        printer.display_text([f"List two result: {list_two_result}"])

        printer.display_text(["testesttest script completed. Press any key to exit."])
        stdscr.getch()

    curses.wrapper(main_curses)
