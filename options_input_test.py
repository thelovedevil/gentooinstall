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
import itertools

stdscr = cur.initscr()

crypt_sources = test_crypt_options()

def options_input():
    dictionary = {}
    print_curses(stdscr, "please enter the number of entries to enter n:")
    n = int(input("enter range of list to create: <should only need value (1) >"))

    for i in range(n):
        print_curses(stdscr, "enter options by scrolling selecting with enter then looping back through and selecting again")
        option = []
        option = crypt_options_digest(stdscr, crypt_sources)
        value = []
        print_curses(stdscr,"enter the value for that option in the same manner by pressing r filling and selecting with enter")
        value = crypt_options_digest(stdscr, crypt_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

command = []  
command = options_input()
print(command)


def luks_process_prefab():              
    luks_process = subprocess.run(['sudo', 'cryptsetup'] + command + ['luksFormat', '/dev/sda'])

luks_process_prefab()

