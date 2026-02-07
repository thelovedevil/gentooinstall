#!/usr/bin/env python3

from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses


def main(stdscr):
    stdscr = curses.initscr()
    stdscr.clear()


def crypt_options_digest(stdscr, sources):

    x = 0
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    special_address_list = []

    def return_options_dictionary():
        return sources
    
    dictionary_variable = return_options_dictionary()

    table = Table(stdscr, len(dictionary_variable), (len(dictionary_variable.columns)), 140, 100, 15, spacing=1, col_names=True)

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
        x = stdscr.getkey()
        if ( x == 'a'):
            table.cursor_left()
        elif ( x == 'd'):
            table.cursor_right()
        elif (x == 's'):
            table.cursor_down()
        elif (x == 'w'):
            table.cursor_up()
        elif (x == 'r'):
            table.user_input(stdscr)
        elif (x == '\n'):
            print_curses(stdscr, str(table.select(stdscr)))
            special_address = str(table.select(stdscr))
            special_address_list.append(special_address)
            print_curses(stdscr, str(special_address_list))
    
    
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
    curses.wrapper(main)

