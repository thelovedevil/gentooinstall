#!/usr/bin/env python3

import curses as cur


stdscr = cur.initscr()
def print_curses(stdscr, print):
    scr = cur.initscr()
    scr.erase()
    scr.addstr(str(print))
    scr.scrollok(1)
    scr.refresh()
    scr.getch()
    cur.endwin()    
if __name__ == "__print_curses__":
    cur.wrapper(print_curses)
    