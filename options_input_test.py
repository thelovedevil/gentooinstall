#!/usr/bin/env python3
import curses as cur
from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses
from testtest import sources_testcrypt
from cryptsetup_table import crypt_options_digest, test_crypt_options

stdscr = cur.initscr()

crypt_sources = test_crypt_options()

def options_input():
    dictionary = {}
    print_curses(stdscr, "please enter the number of entries to enter n:")
    n = int(input("enter number of options: "))

    for i in range(n):
        print_curses(stdscr, "enter an option")
        option = []
        option = crypt_options_digest(stdscr, crypt_sources)
        command = []
        print_curses(stdscr, "enter the value for that option by pressing r")
        command = crypt_options_digest(stdscr, crypt_sources)
        final = [j for i in zip(option, command) for j in i]
        print(final)



def luks_process_prefab():              
    luks_process = subprocess.run(['sudo', 'cryptsetup', variable_one[0], variable_two[0], variable_three[0], variable_four[0], variable_five[0], variable_six[0], variable_seven[0], variable_eight[0], 'luksFormat', '/dev/sda'])

options_input()
