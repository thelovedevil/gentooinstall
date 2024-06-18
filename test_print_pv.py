#! /usr/bin/env python

import subprocess
from subprocess import Popen, PIPE
import curses
import cursesscrollmenu
from cursesscrollmenu import menu
from cursesprint import print_curses
from cursedinput import Input
from block_device_class_table import Block_Table, return_pandas
import moby_dick
from cursedprint_white import CursedPrintWhite


print_app = CursedPrintWhite()
print_app.start()

def pv_display():
    pv_display = subprocess.run([ 'sudo', 'pvdisplay'], check=True, capture_output=True, text=True).stdout
    print_app.print_curses(pv_display)


pv_display()