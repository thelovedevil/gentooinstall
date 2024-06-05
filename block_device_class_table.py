#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from cursesprint import print_curses
from cursedprint import CursedPrint

def return_pandas():
    process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
    data = json.loads(process.stdout)
    df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
    df = (pd 
        .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
        .drop(columns=[0, "children"])
        .fillna("")
        .reset_index(drop=True)
        )
    print(df) 
    return df

stdscr = curses.initscr()
sources = return_pandas()

class Block_Table():

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

    def block_digest(self, sources):

        x = 0
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        
        special_address_list = []

        def return_block():
            return sources
        
        new_table = return_block()

        table = Table(stdscr, len(new_table), (len(new_table.columns)), 20, 100, 10, spacing=1, col_names=True)

        
        m = 0 
        while m < len(new_table.columns):
            table.set_column_header(new_table.columns[m], m)
            m += 1
        numpy_table = new_table.to_numpy()
        m = 0
        while m < len(new_table):
            n = 0
            while n < (len(new_table.columns)):
                    table.set_cell(m, n, numpy_table[m][n])
                    n += 1      
            
            m += 1
        table.refresh()
        while ( x != 'q'):
            table.refresh()
            x = stdscr.getkey()
            if ( x == 'a'):
                table.cursor_left()
            elif ( x == 'd'):
                table.cursor_right()
            elif (x == 's'):
                table.cursor_down()
            elif (x == 'w'):
                table.cursor_up()
            elif (x == '\n'):
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
    app = Block_Table()
    app.start()
    app.block_digest(sources)
