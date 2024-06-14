#!/usr/bin/env python3

import curses
from PIL import Image
import numpy as np
import os, sys
from curses import panel
from curses_menu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem
import curses
import subprocess
import pandas as pd
from PIL import Image
import numpy as np
import os, sys
from ascii_asuka_any import AsciiArt


stdscr = curses.initscr()

class AsukaPrint():
    def __init__(self):
        self.screen = None
        self.ascii_art = AsciiArt("/home/adrian/Downloads/tero.jpg")

    def start(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.screen = stdscr
        self.screen.scrollok(0)
        



    

    def print_curses(self, variable):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        self.screen.bkgd(' ', curses.color_pair(1))
        self.screen.clear()

        self.ascii_art.draw_menu(self.screen)
        

        #Print returned information left side of the console
        lines = str(variable).split('\n')
        max_width = curses.COLS // 2 - 2 # Adjust the width as needed
        for i, line in enumerate(lines):
            self.screen.addstr(i + 1, 1, line[:max_width])

        # #Draw the ascii art on the right side of the console
        # self.ascii_art.draw_menu(self.screen)
        # self.screen.refresh()
        self.screen.refresh()

        while True:
            self.ascii_art.draw_menu(self.screen)
            key = self.screen.getch()

            if key == ord('q'):
                break
            elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                self.ascii_art.handle_input(key)
                self.ascii_art.draw_menu(self.screen)

        #self.screen.addstr(str(variable))
        #self.screen.scrollok(1)
        self.screen.refresh()
        self.screen.getch()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
    


class AsciiArt:
    # stdscr.scrollok(0)
    # curses.curs_set(0)
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    # pad = curses.newpad(100, 100)
    # pad_position = 0

    # # Menu Items
    # menu_items = ["A", "B", "C", "EXIT"]
    # current_row_idx = 0


    ascii_chars = "@@@@@%%%%%#####*****+++++=====-----:::::.....!!!!!///// "

    def __init__(self, image_path):
        self.image_path = image_path
        self.start_row = 0
        self.start_col = 0
        self.art_matrix = self.convert_ascii(image_path)
        self.art_height, self.art_width = self.art_matrix.shape

    # def map_luminosity_to_ascii(luminosity_matrix, ascii_chars):
    def convert_ascii(self, image_path):
        size = 150, 150
        im = Image.open(image_path)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        im.save(image_path + "original_resized.jpg")       
        img = Image.open(image_path + "original_resized.jpg")
        pixel_matrix = np.array(img)
        luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]
        # Normalize luminosity values to the range of the ASCII characters
        normalized_luminosity = (luminosity_matrix - luminosity_matrix.min()) / (luminosity_matrix.max() - luminosity_matrix.min())
        indices = (normalized_luminosity * (len(self.ascii_chars) - 1)).astype(int)
        ascii_matrix = np.array([[self.ascii_chars[idx] for idx in row] for row in indices])
        return ascii_matrix
            




   

    # stdscr.clear()
    # while True:
        
    # draw_menu(stdscr, current_row_idx, menu_items)
    def draw_menu(self, stdscr):
        pad = curses.newpad(self.art_height, self.art_width)
        # Draw the portion of the ASCII art that fits the screen
        for i in range(min(curses.LINES - 2, self.art_height - self.start_row)):
            for j in range(min(curses.COLS - 20, self.art_width - self.start_col)):
                pad.addch(i, j, self.art_matrix[self.start_row + i, self.start_col + j])
        
        pad.refresh(0,0, 1,75, curses.LINES - 2, curses.COLS - 1)

        # Get user input for scrolling
        key = stdscr.getch()
        self.handle_input(key)

    def handle_input(self, key):
        if key == ord("w") and self.start_row > 0:
            self.start_row -= 1
        elif key == ord("s") and self.start_row < self.art_height - (curses.LINES - 2):
            self.start_row += 1
        elif key == ord("d") and self.start_col > 0:
            self.start_col -= 1
        elif key == ord("a") and self.start_col < self.art_width - (curses.COLS - 20):
            self.start_col += 1



if __name__ == "__main__":
    app = AsukaPrint()
    app.start()
    #app.print_curses(string)
    #app.print_curses()
    #app.start()
