#!/usr/bin/env python3

import curses as cur
import curses.panel as pan
from curses.ascii import ESC
import tkinter

NLINES=10
NCOLS=40

def main(scr):
    cur.init_pair(1, cur.COLOR_RED, cur.COLOR_BLACK)
    cur.init_pair(2, cur.COLOR_GREEN, cur.COLOR_BLACK)
    cur.init_pair(3, cur.COLOR_BLUE, cur.COLOR_BLACK)
    cur.init_pair(4, cur.COLOR_CYAN, cur.COLOR_BLACK)

    # attach a panel to each window. set all visible
    my_wins = init_wins(4) #create 4 windows
    my_panels = [pan.new_panel(w) for w in my_wins]

    # Show it on the screen
    scr.attron(cur.color_pair(4))
    scr.addstr(cur.LINES-3, 0, 
                "Use'1-4' to toggle visibility ")
    scr.addstr(cur.LINES-2,0, "ESC to Exit")
    pan.update_panels()
    cur.doupdate()

    while True:
        ch = scr.getch()
        if ch == ESC:
            break
        if ch in [ord('1'), ord('2'), ord('3'), ord('4')]:
            index = int(chr(ch)) - 1 # zero index!
        thePanel = my_panels[index]
        if thePanel.hidden():
            thePanel.show()
        else:
            thePanel.hide()
        pan.update_panels()
        cur.doupdate()

def init_wins(n_wins):
    y = 2
    x = 10
    wins = []
    for n in range(n_wins):
        win = cur.newwin(NLINES, NCOLS, y + (3*n), x + (7*n))
        lbl = "Window Number %d" % (n + 1 )
        win_show(win, lbl, n + 1)
        wins.append(win)
    return wins

def win_show(win, label, label_color):
    starty,startx = win.getbegyx()
    height,width = win.getmaxyx()
    win.box()
    win.addch(2, 0, cur.ACS_LTEE)
    win.hline(2, 1, cur.ACS_HLINE, width-2)
    win.addch(2, width-1, cur.ACS_RTEE)
    print_in_middle(win, 1, label,
            cur.color_pair(label_color))
    win.refresh()
def print_in_middle(win, line, label, col_pair):
    _,width = win.getmaxyx()
    length = len(label)
    x = (width-length) // 2
    win.addstr(line, x, label, col_pair)
    win.refresh
cur.wrapper(main)
