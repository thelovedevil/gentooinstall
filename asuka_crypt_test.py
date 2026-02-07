#!/usr/bin/env python3
import curses
from curseXcel import Table
import numpy
from ui.printer import CursedPrinter 
from utils import test_crypt_options
from ui.ascii_art import AsciiArt









class Crypt_Table():
    def __init__(self):
        self.screen = None

    def start(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.screen = stdscr
        self.printer = CursedPrinter(stdscr) # Instantiate CursedPrinter
        # curses setup is handled by CursedPrinter
        self.screen.clear()
        

    def crypt_options_digest(self, stdscr, printer: CursedPrinter, sources):
        x = 0
        # Curses setup is handled by CursedPrinter and main()
        special_address_list = []

        def return_options_dictionary():
            return sources
        
        dictionary_variable = return_options_dictionary()

        # table = Table(stdscr, len(dictionary_variable), (len(dictionary_variable.columns)), 70, 100, 15, spacing=1, col_names=True)
        # Use curses.newpad for table display
        table_rows, table_cols = stdscr.getmaxyx()
        # Adjusted size for the pad, ensuring it's not smaller than actual content
        pad_height = len(dictionary_variable) + 5 if not dictionary_variable.empty else 5 
        table_pad = curses.newpad(pad_height, table_cols) 

        # Populate table_pad with data, similar to how Table class would
        # For now, let's just print a placeholder using the printer
        printer.display_text(["Table display is under refactoring. Showing raw data for now:"])
        # Check if dictionary_variable is not empty before attempting to_string()
        if not dictionary_variable.empty:
            printer.display_text(dictionary_variable.to_string().splitlines())
        else:
            printer.display_text(["No data to display in table."])


        # Assuming AsciiArt object is created and passed, or instantiated here
        ascii_art_obj = AsciiArt("resources/keiko.jpg") # Use relative path
        printer.display_ascii_art(ascii_art_obj, row=0, col=70, width_ratio=0.3, height_ratio=0.9) # Example positioning

        while (x != ord('q')):
            stdscr.refresh()
            # table.refresh() # This needs to be replaced with direct pad refresh
            # For now, we'll rely on printer's refresh
            printer.display_ascii_art(ascii_art_obj, row=0, col=70, width_ratio=0.3, height_ratio=0.9) # Refresh ASCII art

            x = stdscr.getch() # Use stdscr.getch directly

            if (x == curses.KEY_LEFT):
                # table.cursor_left() # Needs refactoring
                pass
            elif (x == curses.KEY_RIGHT):
                # table.cursor_right() # Needs refactoring
                pass
            elif (x == curses.KEY_DOWN):
                # table.cursor_down() # Needs refactoring
                pass
            elif (x == curses.KEY_UP):
                # table.cursor_up() # Needs refactoring
                pass
            elif (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                printer.handle_input(x) # Handle scrolling for ascii art
            elif (x == ord('r')):
                # table.user_input(stdscr) # Needs refactoring
                pass
            elif (x == ord('\n')):
                # table_sources = table.select(stdscr) # Needs refactoring
                table_sources = "Selected item placeholder" # Placeholder
                printer.display_text(str(table_sources).splitlines())
                special_address = str(table_sources)
                special_address_list.append(special_address)
                printer.display_text(special_address_list)
        
        # Curses teardown is handled by curses.wrapper
        return (special_address_list)
        
if __name__ == "__main__": 
    app = Crypt_Table()
    # app.start() is replaced by curses.wrapper
    def run_crypt_table(stdscr):
        app.main(stdscr) # Set up curses context and printer
        # Now call crypt_options_digest with stdscr and printer
        app.crypt_options_digest(stdscr, app.printer, sources)

    curses.wrapper(run_crypt_table)
    
    
    
    