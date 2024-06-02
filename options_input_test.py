#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses
from testtest import sources_testcrypt
from cryptsetup_table import crypt_options_digest, test_crypt_options


def options_input():
    dictionary = {}
    print_curses(stdscr, "please enter the number of entries to enter n: ")
    n = int(input_string())
    dictionary = crypt_options_digest(stdscr,sources_testcrypt).split() for _ in range(int(n))
    print(dictionary)

def luks_process_prefab():              
    luks_process = subprocess.run(['sudo', 'cryptsetup', variable_one[0], variable_two[0], variable_three[0], variable_four[0], variable_five[0], variable_six[0], variable_seven[0], variable_eight[0], 'luksFormat', '/dev/sda'])

options_input()