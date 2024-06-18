#! /usr/bin/env python 
from cursedprint import CursedPrint
import subprocess
from block_device_class_table import Block_Table
import json
import pandas as pd
from cursedinput import Input
from cursesscrollmenu import menu
import moby_dick

print_app = CursedPrint()
print_app.start()

input_app = Input()
input_app.start()

def variable_dictionary():
        dictionary = {}
        string = moby_dick.entries()
        print_app.print_curses(string)
        n = input_app.input_string()
        string_two = moby_dick.key_value()
        print_app.print_curses(string_two)
        dictionary = dict(input_app.input_string().split() for _ in range(int(n)))
        return dictionary

variable_dictionary()