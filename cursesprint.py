#! /usr/bin/env python3
import curses as cur

def print_curses(print):
    scr = cur.initscr()
    scr.erase()
    scr.addstr(print)
    scr.refresh()
    scr.getch()
    cur.endwin()
    