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

    def ascii_art(self, jpeg):


        ascii_chars = "@@@%%%###***+++===---:::...!!!/// "

        def map_luminosity_to_ascii(luminosity_matrix, ascii_chars):
            # Normalize luminosity values to the range of the ASCII characters
            normalized_luminosity = (luminosity_matrix - luminosity_matrix.min()) / (luminosity_matrix.max() - luminosity_matrix.min())
            indices = (normalized_luminosity * (len(ascii_chars) - 1)).astype(int)
            ascii_matrix = np.array([[ascii_chars[idx] for idx in row] for row in indices])
            return ascii_matrix


        
        # base_width = 128
        # img = Image.open('/home/adrian/Downloads/asuka_original.jpg')
        # wpercent = (base_width / float(img.size[0]))
        # hsize = int((float(img.size[1]) * float(wpercent)))
        # img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
        # img.save('/home/adrian/Downloads/asuka_original_resized.jpg')


        size = 100, 100

        im = Image.open(jpeg)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        im.save(jpeg + "original_resized.jpg")       

        img = Image.open(jpeg + "original_resized.jpg")
        pixel_matrix = np.array(img)

        luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]


        ascii_matrix = map_luminosity_to_ascii(luminosity_matrix, ascii_chars)

        def print_ascii_art(ascii_matrix):
            for row in ascii_matrix:
                print(str("".join(row)))

        #string_ascii = print_ascii_art(ascii_matrix)

        


        height, width = stdscr.getmaxyx()


        start_row = 0
        start_col = -50

        # Get the dimensions of the window
        height, width = stdscr.getmaxyx()

        while True:
            stdscr.clear()
            
            # Draw the portion of the ASCII art that fits the screen
            for i in range(min(height, ascii_matrix.shape[0] - start_row)):
                for j in range(min(width, ascii_matrix.shape[1] - start_col)):
                    stdscr.addch(i, j, ascii_matrix[start_row + i, start_col + j])
            
            stdscr.refresh()

            # Get user input for scrolling
            key = stdscr.getch()
            
            if key == curses.KEY_UP and start_row > 0:
                start_row -= 1
            elif key == curses.KEY_DOWN and start_row < ascii_matrix.shape[0] - height:
                start_row += 1
            elif key == curses.KEY_LEFT and start_col > 0:
                start_col -= 1
            elif key == curses.KEY_RIGHT and start_col < ascii_matrix.shape[1] - width:
                start_col += 1
            elif key == ord('q'):
                break
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
