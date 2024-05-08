#!/usr/bin/env python3

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


def test_wget():
    url = "wget -c https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.DIGESTS"
    subprocess.Popen(url, shell=True, executable='/bin/bash')

test_wget()