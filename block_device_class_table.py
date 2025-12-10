#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from cursesprint import print_curses
from cursedprint import CursedPrint
from PIL import Image
import numpy as np

def return_pandas():
    process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
    data = json.loads(process.stdout)
    df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
    df = (pd 
        .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
        .drop(columns=[0, "children"])
        .fillna("")
        .reset_index(drop=True)
        )
    return df

stdscr = curses.initscr()
sources = return_pandas()

class AsciiArt:
    ascii_chars = "@@@@@%%%%%#####*****+++++=====-----:::::.....!!!!!///// "

    def __init__(self, image_path):
        self.image_path = image_path
        self.start_row = 0
        self.start_col = 0
        self.art_matrix = self.convert_ascii(image_path)
        self.art_height, self.art_width = self.art_matrix.shape

    def convert_ascii(self, image_path):
        size = 150, 150
        im = Image.open(image_path)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        im.save(image_path + "original_resized.jpg")      
        img = Image.open(image_path + "original_resized.jpg")
        pixel_matrix = np.array(img)
        luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]
        normalized_luminosity = (luminosity_matrix - luminosity_matrix.min()) / (luminosity_matrix.max() - luminosity_matrix.min())
        indices = (normalized_luminosity * (len(self.ascii_chars) - 1)).astype(int)
        ascii_matrix = np.array([[self.ascii_chars[idx] for idx in row] for row in indices])
        return ascii_matrix

    def draw_menu(self, stdscr):
        pad = curses.newpad(self.art_height, self.art_width)
        for i in range(min(curses.LINES - 2, self.art_height - self.start_row)):
            for j in range(min(curses.COLS - 20, self.art_width - self.start_col)):
                pad.addch(i, j, self.art_matrix[self.start_row + i, self.start_col + j])
        pad.refresh(0, 0, 6, 75, curses.LINES - 2, curses.COLS - 1)

    def handle_input(self, key):
        if key == ord("w") and self.start_row > 0:
            self.start_row -= 1
        elif key == ord("s") and self.start_row < self.art_height - (curses.LINES - 2):
            self.start_row += 1
        elif key == ord("d") and self.start_col > 0:
            self.start_col -= 1
        elif key == ord("a") and self.start_col < self.art_width - (curses.COLS - 20):
            self.start_col += 1


class Block_Table():

    def __init__(self):
        self.screen = None

    def start(self):
        # curses.wrapper(self.main)
        

        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(True)
            self.main(self.screen)
        finally:

            self.screen.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()



    def main(self, stdscr):
        self.screen = stdscr
        self.screen.clear()
        # curses.noecho()
        # curses.cbreak()
        # self.screen.keypad(True)
        self.block_digest(sources)

    def block_digest(self, sources):
        x = 0
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        
        special_address_list = []

        def return_block():
            return sources
        
        new_table = return_block()

        table = Table(stdscr, len(new_table), (len(new_table.columns)), 20, 100, 10, spacing=1, col_names=True)

        ascii_art = AsciiArt("/home/adrian/Downloads/keiko.jpg")

        
        m = 0 
        while m < len(new_table.columns):
            table.set_column_header(new_table.columns[m], m)
            m += 1
        numpy_table = new_table.to_numpy()
        m = 0
        while m < len(new_table):
            n = 0
            while n < (len(new_table.columns)):
                    table.set_cell(m, n, numpy_table[m][n])
                    n += 1      
            
            m += 1
        while ( x != ord('q')):
            table.refresh()
            ascii_art.draw_menu(stdscr)
            x = stdscr.getch()
            if ( x == curses.KEY_LEFT):
                table.cursor_left()
            elif ( x == curses.KEY_RIGHT):
                table.cursor_right()
            elif (x == curses.KEY_DOWN):
                table.cursor_down()
            elif (x == curses.KEY_UP):
                table.cursor_up()
            elif (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                if ascii_art: 
                    ascii_art.handle_input(x)
            elif (x == ord('r')):
                table.user_input(stdscr)
            # if ( x == 'a'):
            #     table.cursor_left()
            # elif ( x == 'd'):
            #     table.cursor_right()
            # elif (x == 's'):
            #     table.cursor_down()
            # elif (x == 'w'):
            #     table.cursor_up()
            elif (x == ord('\n')):
                table_sources = table.select(stdscr)
                print_app = CursedPrint()
                print_app.start()
                print_app.print_curses(table_sources)
                #print_curses(stdscr, str(table.select(stdscr)))
                special_address = str(table.select(stdscr))
                special_address_list.append(special_address)
                print_app.print_curses(special_address_list)
                #print_curses(stdscr, str(special_address_list))
                
                
        # stdscr = curses.initscr()
        # curses.noecho()
        # curses.cbreak()
        # stdscr.keypad(True)
        # curses.nocbreak()
        # stdscr.keypad(False)
        # curses.noecho()
        # stdscr.clear()
        
        
        return (special_address_list)


if __name__ == "__main__":
    app = Block_Table()
    app.start()