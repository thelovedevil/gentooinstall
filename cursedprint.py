#!/usr/bin/env python3

import curses
import subprocess
import pandas as pd
from PIL import Image
import numpy as np
import os, sys


def test_crypt_options():
    command = ["cryptsetup", "--help"]
    cryptsetup_process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE)
    awk_command = ["awk", "{print substr($0,3,30)}"]
    awk_process = subprocess.Popen(awk_command, text=True, stdin=cryptsetup_process.stdout, stdout=subprocess.PIPE)
    sed_one_command = ["sed", "s/,/:/"]
    sed_one_process = subprocess.Popen(sed_one_command, text=True, stdin=awk_process.stdout, stdout=subprocess.PIPE)
    sed_two_command = ["sed", "1, 4d"]
    sed_two_process = subprocess.Popen(sed_two_command, text=True, stdin=sed_one_process.stdout, stdout=subprocess.PIPE)
    head_command = ["head", "-n-54"]
    head_process = subprocess.Popen(head_command, text=True, stdin=sed_two_process.stdout, stdout=subprocess.PIPE)
    sed_three_command = ["sed", "-e", "s/-[?a-zA-Z]: / /g"]
    sed_three_process = subprocess.Popen(sed_three_command, text=True, stdin=head_process.stdout, stdout=subprocess.PIPE)
    sed_four_command = ["sed", "-e", "s/=[a-zA-Z]*/ /g"]
    sed_four_process = subprocess.Popen(sed_four_command, text=True, stdin=sed_three_process.stdout, stdout=subprocess.PIPE)
    # print(cryptsetup_process.stdout)
    # print(awk_process)
    # print(sed_one_process)
    # print(sed_two_process)
    # print(head_process)
    output, error = sed_four_process.communicate()
    variable = output.split()
    df = pd.DataFrame(variable)
    pattern = r'(\D\D:+)'
    df.columns = ["options"]
    match = df["options"].str.extract(pattern)
    pattern_two = r'(\S\S+)'
    match_two = df['options'].str.extract(pattern_two)
    frames = [df['options'].str.extract(pattern), df['options'].str.extract(pattern_two)]
    return df

sources = test_crypt_options()
stdscr = curses.initscr()

class CursedPrint():
    def __init__(self):
        self.screen = None

    def start(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.screen = stdscr
        self.screen.scrollok(0)
    
    def start_print(self):
        curses.wrapper(self.print_curses)

# ///////////////////////////////////////////////////////////////////
#         art_height, art_width = ascii_matrix.shape

#         start_y = (height - art_height) // 2
#         start_x = (width - art_width) // 2
        
#         for i in range(art_height):
#             for j in range(art_width):
#                 stdscr.addstr(start_y + i, start_x + j, ascii_matrix[i, j])
        
#         self.screen.refresh()
       
#         self.screen.getch()
        
# ////////////////////////////////////////////////////////////////////////////////////

    def print_curses(self, variable):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        self.screen.bkgd(' ', curses.color_pair(1))
        self.screen.clear()
        self.screen.addstr(str(variable))
        #self.screen.scrollok(1)
        self.screen.refresh()
        self.screen.getch()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
    
        

if __name__ == "__main__":
    app = CursedPrint()
    app.start()
    app.print_curses(sources)
    app.ascii_art("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
    app.start()
