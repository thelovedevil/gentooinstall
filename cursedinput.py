#!/usr/bin/env python3

import curses as cur

def input_string():

    prompt = "Enter a string: "

    screen = cur.initscr()
    rows,cols = screen.getmaxyx()

    screen.addstr(rows//2,(cols-len(prompt))// 2, prompt)
    bs = screen.getstr() #read the user input as a bytestring

    screen.addstr(cur.LINES-2,0,
        "You entered: %s" % bs.decode('utf-8'))
    
    return bs.decode(encoding='utf-8')
        
    screen.getch()


    cur.endwin()



