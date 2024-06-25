#!/usr/bin/env python3
import curses

class Input:
    def __init__(self):
        self.screen = None
        self.print_pad = None
        self.print_rows = 0
        self.print_cols = 0

    def start(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        if curses.has_colors():
            curses.start_color()
        self.main(self.screen)

    def main(self, stdscr):
        self.screen.clear()
        self.print_rows, self.print_cols = self.screen.getmaxyx()
        self.print_pad = curses.newpad(self.print_rows, self.print_cols)

    def input_string(self):
        prompt = "entry: "
        curses.echo()
        stdscr = self.screen
        rows, cols = stdscr.getmaxyx()
        input_str = ""

        while True:
            stdscr.clear()
            stdscr.addstr(rows // 2, (cols - len(prompt)) // 2, prompt)
            stdscr.refresh()

            self.print_pad.clear()
            self.print_pad.addstr(0, 0, "User Input:")
            self.print_pad.addstr(1, 0, input_str)
            self.print_pad.refresh(0, 0, 0, 0, self.print_rows - 1, self.print_cols - 1)

            ch = stdscr.getch()
            if ch == ord('\n'):
                break
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
            else:
                input_str += chr(ch)

        return input_str

if __name__ == "__main__":
    try:
        app = Input()
        app.start()
        user_input = app.input_string()
        print("User input:", user_input)
    finally:
        curses.nocbreak()
        app.screen.keypad(False)
        curses.echo()
        curses.endwin()