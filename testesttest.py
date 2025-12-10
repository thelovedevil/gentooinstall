#!/usr/bin/env python3

import curses as cur
from beautiful_soup_test import sources_
import block_device_table
import subprocess



stdscr = cur.initscr()

def test_list():
    test_list = block_device_table.block_digest(stdscr, sources_)
    return test_list

test_list = test_list()

def stty():
    subprocess.run(['stty', 'sane'])

stty()

def test_list_two():
    test_list_two = block_device_table.block_digest(stdscr, sources_)
    return test_list_two

test_list_two = test_list_two()