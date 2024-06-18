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
from cursedinput import Input
from dd_class_table import Dd_Table, test_dd_options
from gpg_class_table import GpG_Table, test_gpg_options
import create_efi
from block_device_class_table import Block_Table, return_pandas
import moby_dick

input_app = Input()
input_app.start()

blockdevice_app = Block_Table()
blockdevice_app.start()

crypt_app = Crypt_Table()
crypt_app.start()

print_app = CursedPrint()
print_app.start()

dd_app = Dd_Table()
dd_app.start()

gpg_app = GpG_Table()
gpg_app.start()

crypt_sources = test_crypt_options()

block_sources = return_pandas()

def block_options_input():
    dictionary = {}
    # print_app.print_curses("filling in block_options process")
    # print_app.print_curses("please enter the number of entries to enter n:")
    # print_app.print_curses("enter range of list to create:<: as of now you may only create one list >")
    string = moby_dick.block_options()
    print_app.print_curses(string)
    n = int(input_app.input_string())

    for i in range(n):
        string = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = blockdevice_app.block_digest(block_sources)
        value = []
        string = moby_dick.enter_value()
        print_app.print_curses(string)
        value = blockdevice_app.block_digest(block_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

def crypt_options_input():
    dictionary = {}
    string = moby_dick.crypt_options()
    print_app.print_curses(strings)
    n = int(input_app.input_string())

    for i in range(n):
        string = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = crypt_app.crypt_options_digest(crypt_sources)
        value = []
        string_two = moby_dick.enter_value()
        print_app.print_curses(string_two)
        value = crypt_app.crypt_options_digest(crypt_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

dd_sources = test_dd_options()

def overwrite_options_input():
    dictionary = {}
    string = moby_dick.overwrite_options()
    print_app.print_curses(string)
    n = int(input_app.input_string())

    for i in range(n):
        string = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = dd_app.dd_options_digest(dd_sources)
        value = []
        string_two = moby_dick.enter_value()
        print_app.print_curses(string_two)
        value = dd_app.dd_options_digest(dd_sources)
        final = [j for i in zip(option, value) for j in i]
        prepend = lambda x: "="+x
        final[1::2] = map(prepend, final[1::2])
        final_fantasy_seven = [ ''.join(x) for x in zip(final[0::2], final[1::2]) ]
        print(final)
        print(final_fantasy_seven)
        return final_fantasy_seven

def dd_options_input():
    dictionary = {}
    string = moby_dick.dd_options()
    print_app.print_curses(string)
    n = int(input_app.input_string())

    for i in range(n):
        string = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = dd_app.dd_options_digest(dd_sources)
        value = []
        string_two = moby_dick.enter_value()
        print_app.print_curses(string_two)
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
    string = moby_dick.gpg_options()
    print_app.print_curses(string)
    n = int(input_app.input_string())

    for i in range(n):
        string = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = gpg_app.gpg_options_digest(gpg_sources)
        value = []
        string_two = moby_dick.enter_value()
        print_app.print_curses(string_two)
        value = gpg_app.gpg_options_digest(gpg_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

def key_file_input():
    dictionary = {}
    string = moby_dick.key_file()
    print_app.print_curses(string)
    n = int(input_app.input_string())

    for i in range(n):
        string_two = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = gpg_app.gpg_options_digest(crypt_sources)
        value = []
        string_two = moby_dick.enter_value()
        print_app.print_curses(string_two)
        value = gpg_app.gpg_options_digest(crypt_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

def name_physical_volume():
    string = moby_dick.physical_volume()
    print_app.print_curses(s)
    name = input_app.input_string()
    return name    

block_command = []
block_command = block_options_input()
print(block_command)

dd_command = []
dd_command = dd_options_input()
print(dd_command)

gpg_command = []
gpg_command = gpg_options_input()
print(gpg_command)

overwrite_command = []
overwrite_command = overwrite_options_input()
print(overwrite_command)

crypt_command = []  
crypt_command = crypt_options_input()
print(crypt_command)


key_file_command = []
key_file_command = key_file_input()
print(key_file_command)

name_physical_volume = name_physical_volume()

def gpg_tty(): 
    subprocess.run(['export', 'GPG_TTY=$(tty)'])

def over_write():
    overwrite_subprocess = subprocess.run(['sudo', 'dd'] + overwrite_command, stdout=subprocess.PIPE)
    subprocess.run(['&&', 'sync'], stdin=overwrite_subprocess)

over_write()

def luks_key():
    print_app.print_curses("running process for luks key creation")
    dd_subprocess = subprocess.run(['sudo', 'dd'] + dd_command, stdout=subprocess.PIPE)
    subprocess.run(['gpg'] + gpg_command + create_efi.s + '/luks-key.gpg', stdin=dd_subprocess)

luks_key()

def luks_process_one():              
    luks_process = subprocess.run(['sudo', 'cryptsetup'] + crypt_command + ['luksFormat'] + block_command)

luks_process_one()

def luks_process_two():
    luks_process = subprocess.run(['sudo', 'gpg', '--decrypt'] + create_efi.s + '/luks-key.gpg', stdout=subprocess.PIPE)
    subprocess.run(['cryptsetup'] + key_file_command + ['luksOpen'] + block_command + name_physical_volume)

luks_process_two()


