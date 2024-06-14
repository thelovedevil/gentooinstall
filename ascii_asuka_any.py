#!/usr/bin/env python3

import curses
from PIL import Image
import numpy as np
import os, sys
from curses import panel
from curses_menu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem



# class Menu:
#     def __init__(self, items):
#         self.items = items
#         self.current_idx = 0

#     def draw_menu(self, stdscr):
#         h, w = stdscr.getmaxyx()
#         for idx, row in enumerate(self.items):
#             x = 1
#             y = idx + 1
#             if idx == self.current_idx:
#                 stdscr.attron(curses.color_pair(1))
#                 stdscr.addstr(y, x, row)
#                 stdscr.attroff(curses.color_pair(1))
#             else:
#                 stdscr.addstr(y, x, row)
#         stdscr.refresh()
    
#     def handle_input(self, key):
#         if key == curses.KEY_UP:
#             self.current_idx = (self.current_idx - 1) % len(self.items)
#         elif key == curses.KEY_DOWN:
#             self.current_idx = (self.current_idx + 1) % len(self.items)
#         elif key == curses.KEY_ENTER or key in [10, 13]:
#             return self.current_idx
#         return None


class AsciiArt:
    # stdscr.scrollok(0)
    # curses.curs_set(0)
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    # pad = curses.newpad(100, 100)
    # pad_position = 0

    # # Menu Items
    # menu_items = ["A", "B", "C", "EXIT"]
    # current_row_idx = 0


    ascii_chars = "@@@%%%###***+++===---:::...!!!/// "

    def __init__(self, image_path):
        self.image_path = image_path
        self.start_row = 0
        self.start_col = 0
        self.art_matrix = self.convert_ascii(image_path)
        self.art_height, self.art_width = self.art_matrix.shape

    # def map_luminosity_to_ascii(luminosity_matrix, ascii_chars):
    def convert_ascii(self, image_path):
        size = 100, 100
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
            




    # ascii_matrix = map_luminosity_to_ascii(luminosity_matrix, ascii_chars)


    
    # base_width = 128
    # img = Image.open('/home/adrian/Downloads/asuka_original.jpg')
    # wpercent = (base_width / float(img.size[0]))
    # hsize = int((float(img.size[1]) * float(wpercent)))
    # img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    # img.save('/home/adrian/Downloads/asuka_original_resized.jpg')


    # size = 100, 100

    # im = Image.open(jpeg)
    # im.thumbnail(size, Image.Resampling.LANCZOS)
    # im.save(jpeg + "original_resized.jpg")       

    # img = Image.open(jpeg + "original_resized.jpg")
    # pixel_matrix = np.array(img)

    # luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]


    # ascii_matrix = map_luminosity_to_ascii(luminosity_matrix, ascii_chars)


    #string_ascii = print_ascii_art(ascii_matrix)

    



    

    # Get the dimensions of the window

    # art_height, art_width = ascii_matrix.shape

    # start_row = 0
    # start_col = 0


    # stdscr.clear()
    # while True:
        
    # draw_menu(stdscr, current_row_idx, menu_items)
    def draw_menu(self, stdscr):
        pad = curses.newpad(self.art_height, self.art_width)
        # Draw the portion of the ASCII art that fits the screen
        for i in range(min(curses.LINES - 2, self.art_height - self.start_row)):
            for j in range(min(curses.COLS - 50, self.art_width - self.start_col)):
                pad.addch(i, j, self.art_matrix[self.start_row + i, self.start_col + j])
        
        pad.refresh(0,0, 1,100, curses.LINES - 2, curses.COLS - 1)

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
        

def main(stdscr):
    curses.curs_set(0)
    art = AsciiArt("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
    
    while True:
        art.draw_menu(stdscr)
        key = stdscr.getch()
        if key == ord('q'):
            break
        art.handle_input(key)

if __name__ == "__main__":
    curses.wrapper(main)