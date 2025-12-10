#!/usr/bin/env python3
import curses as cur
import curses.panel as pan
import curses.ascii

import curses as cur
msg = "Just a string"

scr = cur.initscr()
rows,cols = scr.getmaxyx() # get number of rows & columns

# print messages at centre of screen
scr.addstr(rows//2, (cols-len(msg))//2,msg)

#print message at bottom of screen
scr.addstr(rows-2,0,
    "This screen has %d rows and %d columns\n" % (rows, cols)
)

scr.addstr("Try resizing your window (if possible) and " +
                "then run this program again"
            )
scr.refresh()
scr.getch()
cur.endwin()