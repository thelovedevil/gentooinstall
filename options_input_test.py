#!/usr/bin/env python3
import curses as cur
from curseXcel import Table
import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from cursesprint import print_curses
from testtest import sources_testcrypt
from cryptsetup_table import crypt_options_digest, test_crypt_options
import itertools
from cryptsetup_class import Crypt_Table
from cursedprint import CursedPrint
from cursedinput import input_string
from dd_class_table import Dd_Table, test_dd_options
from gpg_class_table import GpG_Table


crypt_app = Crypt_Table()
crypt_app.start()

print_app = CursedPrint()
print_app.start()

dd_app = Dd_Table()
dd_app.start()

gpg_app = Gpg_Table()
gpg_app.start()

crypt_sources = test_crypt_options()

def crypt_options_input():
    dictionary = {}
    print_app.print_curses("please enter the number of entries to enter n:")
    print_app.print_curses("enter range of list to create: <should only need value (1) >")
    n = int(input_string())

    for i in range(n):
        print_app.print_curses("enter options by scrolling selecting with enter then looping back through and selecting again")
        option = []
        option = crypt_app.crypt_options_digest(crypt_sources)
        value = []
        print_app.print_curses("enter the value for that option in the same manner by pressing r filling and selecting with enter")
        value = crypt_app.crypt_options_digest(crypt_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

dd_sources = test_dd_options()

def dd_options_input():
    dictionary = {}
    print_app.print_curses("please enter the number of entries to enter n:")
    print_app.print_curses("in other words enter range of list to create: < should only need value (1) >")
    n = int(input_string())

    for i in range(n):
        print_app.print_curses("enter options by scrolling selecting with enter then looping back through and selecting again")
        option = []
        option = dd_app.dd_options_digest(dd_sources)
        value = []
        print_app.print_curses("enter the value for that option in the same manner by pressing r filling and selecting with enter")
        value = dd_app.dd_options_digest(dd_sources)
        final = [j for i in zip(option, value) for j in i]
        prepend = lambda x: "="+x
        final[1::2] = map(prepend, final[1::2])
        final_fantasy_seven = [ ''.join(x) for x in zip(final[0::2], final[1::2]) ]
        print(final)
        print(final_fantasy_seven)
        return final_fantasy_seven

gpg_sources = test_gpg_options()

def gpg_options_input():
    dictionary = {}
    print_app.print_curses("please enter the number of entries to enter n:")
    print_app.print_curses("in other words enter range of list to create: < should only need value (1) >")
    n = int(input_string())

    for i in range(n):
        print_app.print_curses("enter options by scrolling selecting with enter then looping back through and selecting again")
        option = []
        option = gpg_app.gpg_options_digest(dd_sources)
        value = []
        print_app.print_curses("enter the value for that option in the same manner by pressing r filling and selecting with enter")
        value = dd_app.gpg_options_digest(dd_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        print(final)
        return final

crypt_command = []  
crypt_command = crypt_options_input()
print(crypt_command)
 
dd_command = []
dd_command = dd_options_input()
print(dd_command)

overwrite_command = []
overwrite_command = dd_options_input()
print(overwrite_command)

gpg_command = []
gpg_command = gpg_options_input()
print(gpg_command)

def gpg_tty(): 
    subprocess.run(['export', 'GPG_TTY=$(tty)'])

def luks_key():
    dd_subprocess = subprocess.run(['sudo', 'dd'] + dd_command, stdout=subprocess.PIPE))
    subprocess.run(['sudo', 'gpg'])


dd if=/dev/urandom bs=8388607 count=1 | gpg --symmetric --cipher-algo AES256 --output /tmp/efiboot/luks-key.gpg

def over_write():
    overwrite_subprocess = subprocess.run(['sudo', 'dd'] + overwrite_command, stdout=subprocess.PIPE)
    subprocess.run(['&&', 'sync'], stdin=overwrite_subprocess)

over_write()
        
        #subpro'|', 'gpg', '--symmetric', '--cipher-algo', 'AES256', '--output', create_efi.s+'/luks-key.gpg')

def luks_process_prefab():              
    luks_process = subprocess.run(['sudo', 'cryptsetup'] + crypt_command + ['luksFormat', '/dev/sda'])

luks_process_prefab()
