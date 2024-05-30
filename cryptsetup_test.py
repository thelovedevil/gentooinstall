#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses
from testtest import sources_testcrypt
from cryptsetup_table_opt import crypt_options_digest, test_crypt_options

crypt_options = test_crypt_options()
variable_one = []
variable_two = []
variable_three = []
variable_four = []

stdscr = curses.initscr()
print_curses(stdscr, "now select a crypt option")
variable_one = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "good, now write an option value")
variable_two = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "now select a crypt option")

variable_three = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "good, now write an option value")

variable_four = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "now select a crypt option")

variable_five = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "good, now write an option value")
variable_six = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "now select a crypt option")
variable_seven = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "good, now write an option value")
variable_eight = crypt_options_digest(stdscr, crypt_options)
print_curses(stdscr, "now select a crypt option")

def luks_process_prefab():              
        luks_process = subprocess.run(['sudo', 'cryptsetup', variable_one[0], variable_two[0], variable_three[0], variable_four[0], variable_five[0], variable_six[0], variable_seven[0], variable_eight[0], 'luksFormat', '/dev/sda'])

luks_process_prefab()