#!/usr/bin/env python3

import curses

stdscr = curses.initscr()

class Input():

    def __init__(self):
        self.screen = None

    def start(self):
        curses.wrapper(self.main)
        
    def main(self, stdscr):
        self.screen = stdscr
        self.screen.clear()

    def input_string(self):
        prompt = "Please Enter Your Information: "
        curses.echo()
        stdscr = curses.initscr()
        screen = stdscr
        rows,cols = screen.getmaxyx()
        screen.addstr(rows//2,(cols-len(prompt))// 2, prompt)
        bs = screen.getstr() #read the user input as a bytestring
        self.screen.clear()
        screen.addstr(curses.LINES-2,0,
            "You entered: %s" % bs.decode('utf-8'))
        return bs.decode(encoding='utf-8')  
        screen.getch()

if __name__ == "__main__":
    app = Input()
    app.start()
    app.input_string()



