#!/usr/bin/env python3
import curses as cur 
import curses.panel as pan
from curses.ascii import ESC

NLINES=10
NCOLS=40
KEY_TAB=9

def main(scr):
    my_panels = []
    scr.keypad(True)
    cur.start_color()
    cur.init_pair(1, cur.COLOR_RED, cur.COLOR_BLACK)
    cur.init_pair(2, cur.COLOR_GREEN, cur.COLOR_BLACK)
    cur.init_pair(3, cur.COLOR_BLUE,cur.COLOR_BLACK)
    cur.init_pair(4, cur.COLOR_CYAN, cur.COLOR_BLACK)
    my_wins = init_wins(3)

    my_panels.append(pan.new_panel(my_wins[0]))
    my_panels.append(pan.new_panel(my_wins[1]))
    my_panels.append(pan.new_panel(my_wins[2]))

    scr.attron(cur.color_pair(4))
    scr.addstr(cur.LINES-3, 1,
        "Use tab to browse through the window\n" +
            "or number(1-3) to bring to top.(ESC to Exit)")
    scr.attroff(cur.color_pair(4))
    pan.update_panels()
    cur.doupdate()

    while True:
        top = pan.top_panel()
        ch = scr.getch()
        if ch == cur.ascii.ESC:
            break # exit event loop
        if ch == KEY_TAB:
            top.bottom()
        if chr(ch)in('1','2','3'):
            my_panels[int(chr(ch))-1].top()
        pan.update_panels()
        cur.doupdate()

def init_wins(n_wins):
    y = 2
    x = 10
    wins = []
    for n in range(n_wins):
        win = cur.newwin(NLINES, NCOLS, y+(3*n), x+(7*n))
        lbl ="Window Number %d" % (n+1)
        win_show(win, lbl, n + 1)
        wins.append(win)
    return wins

def win_show(win, label, label_color):
    starty, startx = win.getbegyx()
    height,width = win.getmaxyx()
    win.box()
    win.addch(2, 0, cur.ACS_LTEE)
    win.hline(2, 1, cur.ACS_HLINE, width-2)
    win.addch(2, width-1, cur.ACS_RTEE)
    print_in_middle(win, 1, label, cur.color_pair(label_color))

def print_in_middle(win, line, label, col_pair):
    _,width = win.getmaxyx()
    length = len(label)
    x = (width-length) // 2
    win.addstr(line, x, label, col_pair)
    win.refresh()

cur.wrapper(main)




