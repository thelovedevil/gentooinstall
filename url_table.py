#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from beautiful_soup_test import sources_
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses


def return_pandas_dictionary(dictionary):
    return dictionary

dictionary_variable = return_pandas_dictionary(sources_)

def main(stdscr):
    x = 0
    stdscr = curses.initscr()
    

    table = Table(stdscr, len(dictionary_variable), (len(dictionary_variable.columns)), 20, 100, 10, spacing=1, col_names=True)

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
            print_curses(str(table.select(stdscr)))
            
            
    
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
curses.wrapper(main)