#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursedprint import CursedPrint
from asuka_print import AsukaPrint
from PIL import Image
import numpy as np

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

#| awk '{print substr($0,3,35)}'| sed 's/,//' | sed '1, 4d' | head 

sources_testcrypt = test_crypt_options()


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
        pad.refresh(0, 0, 1, 75, curses.LINES - 2, curses.COLS - 1)

    def handle_input(self, key):
        if key == ord("w") and self.start_row > 0:
            self.start_row -= 1
        elif key == ord("s") and self.start_row < self.art_height - (curses.LINES - 2):
            self.start_row += 1
        elif key == ord("d") and self.start_col > 0:
            self.start_col -= 1
        elif key == ord("a") and self.start_col < self.art_width - (curses.COLS - 20):
            self.start_col += 1

class Crypt_Table():
    def __init__(self):
        self.screen = None

    def start(self):
        #curses.wrapper(self.main)
        
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
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.crypt_options_digest(sources_testcrypt)
        

    def crypt_options_digest(self, sources):
        x = 0
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        self.screen.keypad(True)

        special_address_list = []

        def return_options_dictionary():
            return sources
        
        dictionary_variable = return_options_dictionary()

        table = Table(stdscr, len(dictionary_variable), (len(dictionary_variable.columns)), 70, 100, 15, spacing=1, col_names=True)
        ascii_art = AsciiArt("/home/adrian/Downloads/keiko.jpg")

        m = 0 
        while m < len(dictionary_variable.columns):
            table.set_column_header(dictionary_variable.columns[m], m)
            m += 1
        numpy_table = dictionary_variable.to_numpy()
        m = 0
        while m < len(dictionary_variable):
            n = 0
            while n < (len(dictionary_variable.columns)):
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
            # if ( x == 'a'):
            #     table.cursor_left()
            # elif ( x == 'd'):
            #     table.cursor_right()
            # elif (x == 's'):
            #     table.cursor_down()
            # elif (x == 'w'):
            #     table.cursor_up()
            elif (x == ord('r')):
                table.user_input(stdscr)
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
            elif (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
                if ascii_art: 
                    ascii_art.handle_input(x)
        
        # stdscr = curses.initscr()
        # curses.noecho()
        # curses.cbreak()
        # stdscr.keypad(True)
        # curses.nocbreak()
        # stdscr.keypad(False)
        # curses.echo()
        # stdscr.clear()

        return (special_address_list)
        
if __name__ == "__main__": 
    app = Crypt_Table()
    app.start()
    
    
    
    