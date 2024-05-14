#! /usr/bin/env python3

import logging
import glob
import os
import sys
import shutil
import subprocess
from subprocess import Popen, PIPE
import json
import operator
import signal
import curses
import cursesscrollmenu
from cursesscrollmenu import menu
from inputastring import input_string
from cursesprint import print_curses
from url_table import url_address


def test_stage3_wget():
    os.chdir('/home/adrian/Documents/gentooinstall/testingwget')
    subprocess.run(["wget", "-c", url_address])