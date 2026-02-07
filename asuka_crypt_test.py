#!/usr/bin/env python3
from cursedprint import CursedPrint 
from utils import test_crypt_options
from ui.ascii_art import AsciiArt









class Crypt_Table():
    def __init__(self):
        self.screen = None

    def start(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.screen = stdscr
        self.screen.clear()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        

    def crypt_options_digest(self, sources):
        x = 0
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        special_address_list = []

        def return_options_dictionary():
            return sources
        
        dictionary_variable = return_options_dictionary()

        table = Table(stdscr, len(dictionary_variable), (len(dictionary_variable.columns)), 70, 100, 15, spacing=1, col_names=True)
        ascii_art = AsciiArt("/home/adrian/Downloads/keiko.jpg")

        m = 0 
        while m < len(dictionary_variable.columns):
            table.set_column_header(dictionary_variable.columns[m], m)
            m += 1
        numpy_table = dictionary_variable.to_numpy()
        m = 0
        while m < len(dictionary_variable):
            n = 0
            while n < (len(dictionary_variable.columns)):
                    table.set_cell(m, n, numpy_table[m][n])
                    n += 1
                
                
            m += 1
        while ( x != 'q'):
            table.refresh()
            ascii_art.draw_menu(stdscr)
            x = stdscr.getch()
            if ( x == curses.KEY_LEFT):
                table.cursor_left()
            elif ( x == curses.KEY_RIGHT):
                table.cursor_right()
            elif (x == curses.KEY_DOWN):
                table.cursor_down()
            elif (x == curses.KEY_UP):
                table.cursor_up()
            # if (x == ord('a')):
            # #     table.cursor_left()
            # # elif (x == ord('d')):
            # #     table.cursor_right()
            # # elif (x == ord('s')):
            #     table.cursor_down()
            elif (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                if ascii_art: 
                    ascii_art.handle_input(x)
            elif (x == ord('r')):
                table.user_input(stdscr)
            elif (x == ord('\n')):
                table_sources = table.select(stdscr)
                print_app = CursedPrint()
                print_app.start()
                print_app.start_print()
                print_app.print_curses(table_sources)
            
                #print_curses(stdscr, str(table.select(stdscr)))
                special_address = str(table.select(stdscr))
                special_address_list.append(special_address)
                print_app.print_curses(special_address_list)
                #print_curses(stdscr, str(special_address_list))

                
            
            
            

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        stdscr.clear()
        curses.endwin()

        return (special_address_list)
        
if __name__ == "__main__": 
    app = Crypt_Table()
    app.start()
    app.crypt_options_digest(sources)
    
    
    
    