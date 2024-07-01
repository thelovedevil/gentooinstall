#!/usr/bin/env python3

import curses
from testredwhite import CursedPrintRedWhiteUserInput

stdscr = curses.initscr()
red_white_input = CursedPrintRedWhiteUserInput()
red_white_input.start()

class Input():

    def __init__(self):
        self.screen = None
        self.red_white_input = CursedPrintRedWhiteUserInput()
        self.dict_generator = self.red_white_input.dictionary_generator()

    def start(self):
        #curses.wrapper(self.main)
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        if curses.has_colors():
            curses.start_color()
        self.main(self.screen)
        
    def main(self, stdscr):
        #self.screen = stdscr
        self.screen.clear()

    def input_string(self):
        prompt = "entry: "
        curses.echo()
        #x = self.screen.getstr()
        #while (x != ord('\n')):
        stdscr = curses.initscr()
        screen = stdscr
        rows,cols = screen.getmaxyx()
        screen.addstr(rows//2,(cols-len(prompt))// 2, prompt)
        screen.refresh()
        input_str = ""
        #bs = screen.getstr() #read the user input as a bytestring

        while True:
            ch = screen.getch()
            if ch == ord('\n'):
                if not input_str:
                    current_dict = next(self.dict_generator)
                    if current_dict:
                        return str(current_dict)
                #break
                    # input_str = str(current_dict)
                    # screen.addstr(rows // 2, (cols - len(prompt)) // 2 + len(prompt), input_str)
                    # screen.refresh()
                #red_white_input.print_curses("enter key pressed but no dictionary available")
                break
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    screen.addstr(rows // 2, (cols - len(prompt)) // 2 + len(prompt), " " * (cols - len(prompt) - len(input_str) - 2))
                    screen.refresh()
            else:
                input_str += chr(ch)
            screen.addstr(rows // 2, (cols - len(prompt)) // 2 + len(prompt), input_str)
            screen.refresh()

        return input_str

if __name__ == "__main__":
    app = Input()
    app.start()
    app.input_string()



