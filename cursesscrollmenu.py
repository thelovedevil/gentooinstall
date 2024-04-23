#! /usr/bin/env python3
import curses
from math import *


def menu(dictionary):
    screen = curses.initscr()
    screen.erase()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    highlightText = curses.color_pair( 1 )
    normalText = curses.A_NORMAL
    screen.border( 0 )
    curses.curs_set( 0 )
    max_row = 10 #max number of rows
    box = curses.newwin( max_row + 2, 64, 1, 1 )
    box.box()


    testdictionary = dictionary
    for value in testdictionary.values():
        strings = list(testdictionary.values())
    print(list(testdictionary.values()))

    for value in testdictionary.values():
        stringskey = list(testdictionary.values())
    stringskey = list(testdictionary)
    #strings = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n" ] #list of strings
    row_num = len( strings )

    pages = int( ceil( row_num / max_row ) )
    position = 1
    page = 1
    for i in range( 1, max_row + 1 ):
        if row_num == 0:
            box.addstr( 1, 1, "There aren't strings", highlightText )
        else:
            if (i == position):
                box.addstr( i, 2, str( i ) + " - " + stringskey[ i - 1 ] + " - " + strings[ i - 1 ], highlightText )
            else:
                box.addstr( i, 2, str( i ) + " - " + stringskey[ i - 1 ] + " - " + strings[ i - 1 ], normalText )
            if i == row_num:
                break

    screen.refresh()
    box.refresh()

    x = screen.getch()
    while x != 27:
        if x == curses.KEY_DOWN:
            if page == 1:
                if position < i:
                    position = position + 1
                else:
                    if pages > 1:
                        page = page + 1
                        position = 1 + ( max_row * ( page - 1 ) )
            elif page == pages:
                if position < row_num:
                    position = position + 1
            else:
                if position < max_row + ( max_row * ( page - 1 ) ):
                    position = position + 1
                else:
                    page = page + 1
                    position = 1 + ( max_row * ( page - 1 ) )
        if x == curses.KEY_UP:
            if page == 1:
                if position > 1:
                    position = position - 1
            else:
                if position > ( 1 + ( max_row * ( page - 1 ) ) ):
                    position = position - 1
                else:
                    page = page - 1
                    position = max_row + ( max_row * ( page - 1 ) )
        if x == curses.KEY_LEFT:
            if page > 1:
                page = page - 1
                position = 1 + ( max_row * ( page - 1 ) )

        if x == curses.KEY_RIGHT:
            if page < pages:
                page = page + 1
                position = ( 1 + ( max_row * ( page - 1 ) ) )
        if x == ord( "\n" ) and row_num != 0:
            screen.erase()
            screen.border( 0 )
            screen.addstr( 14, 3, "YOU HAVE PRESSED '" + stringskey[ i - 1 ] + strings[ position - 1 ] + "' ON POSITION " + str( position ) )
            log = []
            log.append(strings[ position - 1 ])
            curses.endwin()
            return log
            
        box.erase()
        screen.border( 0 )
        box.border( 0 )

        for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
            if row_num == 0:
                box.addstr( 1, 1, "There aren't strings",  highlightText )
            else:
                if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
                    box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + stringskey[ i - 1 ] + " - " + strings[ i - 1 ], highlightText )
                else:
                    box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + stringskey[ i - 1 ] + " - " + strings[ i - 1 ], normalText )
                if i == row_num:
                    break



        screen.refresh()
        box.refresh()
        x = screen.getch()

    curses.endwin()
    exit()
    