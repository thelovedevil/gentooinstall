#!/usr/bin/env python3

# from cursedprint import CursedPrint
# import subprocess
# from block_device_class_table import Block_Table
# import json
# import pandas as pd
# from cursedinput import Input
# from cursesscrollmenu import menu
# import moby_dick

# input_app = Input()
# input_app.start()

# block_dev = Block_Table()
# block_dev.start()

# print_app = CursedPrint()
# print_app.start()

# def variable_dictionary():
#         dictionary = {}
#         string = moby_dick.entries()
#         print_app.print_curses(string)
#         n = input_app.input_string()
#         string_two = moby_dick.key_value()
#         print_app.print_curses(string_two)
#         dictionary = dict(input_app.input_string().split() for _ in range(int(n)))
#         return dictionary

# string = moby_dick.following()
# print_app.print_curses(string)
# directory_list = variable_dictionary()
# print_app.print_curses(str(directory_list))
# s = menu(directory_list)[0]

# #value_selected_for = moby_dick.value_selected()
# #print_app.print_curses(value_selected_for)
# #print_app.print_curses(s)

# def mkdir():
#         subprocess.run(['sudo', 'mkdir', '-v', '-p', s])

# mkdir()


# def mount():
#         subprocess.run(['sudo', 'mount', '-v', '-t', s])

# mount()

from cursedprint import CursedPrint
import subprocess
from block_device_class_table import Block_Table
import json
import pandas as pd
from cursedinput import Input
from cursesscrollmenu import menu
import moby_dick

def variable_dictionary():
    dictionary = {}
    string = moby_dick.entries()
    print_app.print_curses(string)
    n = input_app.input_string()
    string_two = moby_dick.key_value()
    print_app.print_curses(string_two)
    dictionary = dict(input_app.input_string().split() for _ in range(int(n)))
    return dictionary

def mkdir():
    subprocess.run(['sudo', 'mkdir', '-v', '-p', s])

def mount():
    subprocess.run(['sudo', 'mount', '-v', '-t', s])

def main():
    input_app = Input()
    input_app.start()
    block_dev = Block_Table()
    print_app = CursedPrint()
    print_app.start()

    string = moby_dick.following()
    print_app.print_curses(string)
    directory_list = variable_dictionary()
    print_app.print_curses(str(directory_list))
    s = menu(directory_list)[0]

    mkdir()
    mount()

if __name__ == "__main__":
    main()