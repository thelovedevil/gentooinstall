#!/usr/bin/env python3

from cursedprint import CursedPrint
import subprocess
from block_device_class_table import Block_Table
import json
import pandas as pd
from cursedinput import input_string
from cursesscrollmenu import menu

block_dev = Block_Table()
block_dev.start()

print_app = CursedPrint()
print_app.start()

def variable_dictionary():
        dictionary = {}
        print_app.print_curses("please enter the number of entries to enter n: ")
        n = input_string()
        print_app.print_curses("now enter key value pair followed by <: enter > of each item in dictionary <: press enter >")
        dictionary = dict(input_string().split() for _ in range(int(n)))
        return dictionary

print_app.print_curses("//////////////////////////////////////////////////////////////////////////////////////////////")
print_app.print_curses("/ for the following few functions a menu will be filled by you with key value entries /")
print_app.print_curses("/ for the key value entries make sure to make all keys unique all values meaningful   /")                                                                                     
print_app.print_curses("//////////////////////////////////////////////////////////////////////////////////////////////")

print_app.print_curses("you must now enter a directory name to be made for our efi boot directory")     
directory_list = variable_dictionary()
print_app.print_curses(str(directory_list))
s = menu(directory_list)[0]
print_app.print_curses("here is the value selected for ")
print_app.print_curses(s)

def mkdir():
        subprocess.run(['mkdir', '-v', s])

mkdir()


def mount():
        subprocess.run(['mount', '-v', '-t', s])

mount()