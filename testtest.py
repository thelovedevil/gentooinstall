#! /usr/bin/env python3

import subprocess
from cursesprint import print_curses

def lv_display():
    lv_display = subprocess.check_output(['sudo', 'lvdisplay'])
    print_curses(str(lv_display))

lv_display()