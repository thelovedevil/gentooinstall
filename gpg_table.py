#!/usr/bin/env python3

import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses

stdscr = curses.initscr()
def test_gpg_options():
    command = ["gpg", "--help"]
    cryptsetup_process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE)
    awk_command = ["awk", "{print substr($0,0,30)}"]
    awk_process = subprocess.Popen(awk_command, text=True, stdin=cryptsetup_process.stdout, stdout=subprocess.PIPE)
    sed_one_command = ["sed", "s/,/:/"]
    sed_one_process = subprocess.Popen(sed_one_command, text=True, stdin=awk_process.stdout, stdout=subprocess.PIPE)
    sed_two_command = ["sed", "1, 21d"]
    sed_two_process = subprocess.Popen(sed_two_command, text=True, stdin=sed_one_process.stdout, stdout=subprocess.PIPE)
    head_command = ["head", "-n-54"]
    head_process = subprocess.Popen(head_command, text=True, stdin=sed_two_process.stdout, stdout=subprocess.PIPE)
    sed_three_command = ["sed", "-e", "s/-[?a-zA-Z]: / /g"]
    sed_three_process = subprocess.Popen(sed_three_command, text=True, stdin=head_process.stdout, stdout=subprocess.PIPE)
    sed_four_command = ["sed", "-e", "s/=[a-zA-Z]*/ /g"]
    sed_four_process = subprocess.Popen(sed_four_command, text=True, stdin=sed_three_process.stdout, stdout=subprocess.PIPE)
    output, error = sed_four_process.communicate()
    variable = output.split()
    print(variable)
    df = pd.DataFrame(variable)
    df.columns = ['options']
    return df

sources_testcrypt = test_gpg_options()

def main(stdscr):
    stdscr = curses.initscr()
    stdscr.clear()

def gpg_options_digest(stdscr, sources):

    x = 0
    stdscr = curses.initscr()
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

if __name__ == "__gpg_options_digest__":
    curses.wrapper(url_digest)

