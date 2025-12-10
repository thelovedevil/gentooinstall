#!/usr/bin/env python3

import curses
import subprocess
import pandas as pd
from PIL import Image
import numpy as np
import os, sys
from moby_dick import output_crime
import textwrap
#from cursedinputpad import input_string


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
                pad.addch(i, j, self.art_matrix[self.start_row + i, self.start_col + j], curses.color_pair(1))
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

class CursedPrintRedWhiteUserInput():
    def __init__(self):
        self.screen = None
        self.print_pad = None
        self.input_pad = None
        self.print_rows = 0
        self.print_cols = 0
        self.print_start_row = 0
        self.max_input_length = 1

    def start(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        if curses.has_colors():
            curses.start_color()
        self.main(self.screen)

    def stop(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def main(self, stdscr):
        self.screen.clear()
        self.print_rows, self.print_cols = self.screen.getmaxyx()
        self.print_pad = curses.newpad(self.print_rows, self.print_cols)
        self.input_pad = curses.newpad(5, self.print_cols)
        self.screen.keypad(True)

    def input_dict(self, n):
        dict_input = ""
        for i in range(n):
            self.input_pad.clear()
            self.input_pad.addstr(0, 0, f"Enter key-value pair {i + 1}: ", curses.color_pair(1))
            self.input_pad.refresh(0, 0, 2, 0, 2, self.print_cols - 1)

            while True:
                x = self.screen.getch()
                if x == ord('\n'):
                    break
                elif x == curses.KEY_BACKSPACE or x == 127:
                    if len(dict_input) > 0:
                        dict_input = dict_input[:-1]
                        self.input_pad.addstr(1, 0, " " * (self.print_cols - 1), curses.color_pair(1))
                        self.input_pad.addstr(1, 0, dict_input, curses.color_pair(1))
                        self.input_pad.refresh(0, 0, 2, 0, 3, self.print_cols - 1)
                else:
                    if len(dict_input) < self.print_cols - 1:
                        dict_input += chr(x)
                        self.input_pad.addstr(1, 0, dict_input, curses.color_pair(1))
                        self.input_pad.refresh(0, 0, 2, 0, 3, self.print_cols - 1)
            
            yield dict_input.split()
            dict_input = ""

    def dictionary_generator(self):
        while True:
            if hasattr(self, 'current_dictionary'):
                yield self.current_dictionary
            else:
                yield None

    def print_curses(self, variable):
        ascii_art = AsciiArt("/home/adrian/Downloads/genkai.jpg")
        x = 0
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        self.screen.bkgd(' ', curses.color_pair(1))

        lines = str(variable).split('\n')
        max_line_length = max(len(line) for line in lines)
        self.print_rows = len(lines)
        self.print_cols = max(max_line_length, 70)
        self.print_pad = curses.newpad(self.print_rows + 2, self.print_cols)

        wrapped_lines = []
        for line in lines:
            if len(line) > self.print_cols - 10:
                wrapped_lines.extend(textwrap.wrap(line, width=self.print_cols))
            else:
                wrapped_lines.append(line)

        for i, line in enumerate(wrapped_lines):
            if i == 0:
                line = line[:self.print_cols - 10]
            self.print_pad.addstr(i + 2, 0, line.ljust(self.print_cols - 10), curses.color_pair(1))

        prompt = "entry: "
        test_prompt = "test:"
        input_str = ""
        dict_prompt = "Enter dictionary (key1 value1 key2 value2 ...): "
        dict_input = ""

        while x != ord('q'):
            self.screen.refresh()
            ascii_art.draw_menu(self.screen)

            max_start_row = max(0, len(wrapped_lines) - (curses.LINES - 6))  # Adjusted to accommodate input_pad
            self.print_start_row = min(self.print_start_row, max_start_row)

            self.print_pad.refresh(self.print_start_row, 0, 5, 0, min(len(wrapped_lines) + 5, curses.LINES - 2), max(len(line), curses.COLS - 1))  # Adjusted to accommodate input_pad

            self.print_pad.addstr(0, 0, prompt + input_str.ljust(self.max_input_length), curses.color_pair(1))
            self.print_pad.refresh(0, 0, 0, 0, 1, self.print_cols - 1)

            self.input_pad.addstr(0, 0, dict_prompt, curses.color_pair(1))
            self.input_pad.addstr(1, 0, dict_input, curses.color_pair(1))
            self.input_pad.refresh(0, 0, 2, 0, 6, self.print_cols - 1) 

            x = self.screen.getch()

            if x == ord('\n'):
                try:
                    if len(input_str.strip()) <= 1:
                        n = int(input_str.strip()) 
                        dictionary = dict(pair for pair in self.input_dict(n))
                        self.current_dictionary = dictionary
                        self.input_pad.clear()

                        dict_lines = textwrap.wrap("Dictionary: " + str(dictionary), width=self.print_cols - 1)
                        for i, line in enumerate(dict_lines):
                            self.input_pad.addstr(2 + i, 0, line, curses.color_pair(1))

                        self.input_pad.refresh(0, 0, 2, 0, 2 + len(dict_lines), self.print_cols - 1) # Adjusted to display input_pad
                        yield dictionary
                        input_str = ""
                        dict_input = ""
                        return
                except (ValueError, IndexError):
                    pass

            elif x == curses.KEY_BACKSPACE or x == 127:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    self.print_pad.addstr(0, len(prompt), " " * (self.max_input_length - len(prompt) - len(input_str)), curses.color_pair(1))
                    self.print_pad.refresh(0, 0, 0, 0, 1, self.print_cols - 1)
                elif len(dict_input) > 0:
                    dict_input = dict_input[:-1]
                    self.input_pad.addstr(1, 0, " " * (self.print_cols - 1), curses.color_pair(1))
                    self.input_pad.addstr(1, 0, dict_input, curses.color_pair(1))
                    self.input_pad.refresh(0, 0, 2, 0, 6, self.print_cols - 1)  # Adjusted to display input_pad
            elif x == curses.KEY_UP and self.print_start_row > 0:
                self.print_start_row -= 1
            elif x == curses.KEY_DOWN and self.print_start_row < len(wrapped_lines) - min(self.print_rows, curses.LINES - 6):  # Adjusted to accommodate input_pad
                self.print_start_row += 1
            else:
                if len(input_str) < self.max_input_length:
                    input_str += chr(x)
                elif len(dict_input) < self.print_cols - 1:
                    dict_input += chr(x)

            ascii_art.handle_input(x)
            self.screen.clear()

            curses.noecho()
            curses.cbreak()
            self.screen.keypad(True)

string = output_crime()
sources = string
# if __name__ == "__main__":
#     app = CursedPrintRedWhiteUserInput()
#     app.start()
#     app.print_curses(sources)

if __name__ == "__main__":
    try:
        app = CursedPrintRedWhiteUserInput()
        app.start()
        for dictionary in app.print_curses(sources):
            # This will print each dictionary yielded by print_curses
            print(dictionary)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        curses.endwin() 


    



