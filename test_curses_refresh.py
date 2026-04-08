import curses
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.erase()
    stdscr.addstr(0, 0, "This is stdscr")
    
    pad = curses.newpad(10, 10)
    pad.addstr(0, 0, "This is pad")
    
    stdscr.refresh()
    pad.refresh(0, 0, 5, 5, 10, 15)
    
    stdscr.getch()

curses.wrapper(main)
