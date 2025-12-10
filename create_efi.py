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
from cursedprint_invred import CursedPrintInvRed
from cursedprint_redwhite import CursedPrintRedWhite
from cursedprint_cyanredgenkai import CursedPrintCyanRedGenkai
#from cursedprint_redwhite_userinput import CursedPrintRedWhiteUserInput
from testredwhite import CursedPrintRedWhiteUserInput

print_app = CursedPrint()
print_app.start()
input_app = Input()
input_app.start()

print_appinvred = CursedPrintInvRed()
print_appinvred.start()

print_appredwhite = CursedPrintRedWhite()
print_appredwhite.start()

print_appcyanredgenkai = CursedPrintCyanRedGenkai()
print_appcyanredgenkai.start()

print_appuserinput = CursedPrintRedWhiteUserInput()
print_appuserinput.start()

# app = CursedPrintRedWhiteUserInput()
#         app.start()
#         for dictionary in app.print_curses(sources):
#             # This will print each dictionary yielded by print_curses
#             print(dictionary)

def variable_dictionary():
    string = moby_dick.entries()
    print_appredwhite.print_curses(string)
    string_two = moby_dick.key_value()

    app = CursedPrintRedWhiteUserInput()
    app.start()

    for dictionary in app.print_curses(string_two):
        if dictionary:
            print_appredwhite.print_curses(f"Dictionary received: {dictionary}")
            # This will print each dictionary yielded by print_curses
            return dictionary
    
    print_appredwhite.print_curses("No dictionary recieved. Please enter manually.")
    n = input_app.input_string()
    if n.isdigit():
        n = int(n)
        dictionary = {}
        for _ in range(n):
            key = input_app.input_string()
            value = input_app.input_string()
            dictionary[key] = value

    else:
        try:
            dictionary = eval(n)

        except:
            print_appredwhite.print_curses("invalid input. returning empty dictionary.")
            dictionary = {}

    print_appredwhite.print_curses(f"Final dictionary: {dictionary}")
    return dictionary



def main():
    

    
    block_dev = Block_Table()
    string = moby_dick.following()
    print_appinvred.print_curses(string)
    

    mkdir()
    mount()

def mkdir():
    directory_list = variable_dictionary()
    print_appinvred.print_curses(f"Directory list for mkdir: {directory_list}")
    s = menu(directory_list)[0]
    print_appinvred.print_curses(f"Selected item: {s}")
    subprocess.run(['sudo', 'mkdir', '-v', '-p', s])
    print_appinvred.print_curses("mkdir run")

def mount():
    directory_list = variable_dictionary()
    print_appcyanredgenkai.print_curses(f"Directory list for mount: {directory_list}")
    s = menu(directory_list)[0]
    print_appcyanredgenkai.print_curses(f"Selected item: {s}")    
    subprocess.run(['sudo', 'mount', '-v', '-t', s])
    print_appcyanredgenkai.print_curses("mount run")


if __name__ == "__main__":
    main()
