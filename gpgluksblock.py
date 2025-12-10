#!/usr/bin/env python3

from cursedprint import CursedPrint
import subprocess
from block_device_class_table import Block_Table
import json
import pandas as pd
from cursedinput import input_string
from cursesscrollmenu import menu
import create_efi

block_dev = Block_Table()
block_dev.start()

print_app = CursedPrint()
print_app.start()

def return_pandas():
    process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
    data = json.loads(process.stdout)
    df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
    df = (pd 
        .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
        .drop(columns=[0, "children"])
        .fillna("")
        .reset_index(drop=True)
        ) 
    return df

stdscr = curses.initscr()
pandas_block_devices = return_pandas()

def block_device_selection():
        #block_device_selection = input("select a blockdevice : \n")
        dictionary = block_dev.block_digest(pandas_block_devices)
        block_device_selection = dictionary[0]
        return block_device_selection

block_device = block_device_selection()

luks = block_device
print_app.print_curses(luks)

def gpg_tty(): 
        subprocess.run(['export', 'GPG_TTY=$(tty)'])

def luks_key():
        subprocess.run('dd', 'if=/dev/urandom', 'bs=8388607', 'count=1', '|', 'gpg', '--symmetric', '--cipher-algo', 'AES256', '--output', create_efi.s+'/luks-key.gpg')

print_app.print_curses(str(luks_dictionary.cipher))
def luks_process_prefab():              
        luks_process = subprocess.run(['cryptsetup', '--cipher', luks_dictionary.cipher, '--key-size', luks_dictionary.keysize, '--hash', luks_dictionary.hash, '--key-file', luks_dictionary.keyfile, 'luksFormat', luks])

luks_process_prefab()

def name_physical_volume():
    print_app.print_curses('please enter a name for a logical volume management (LVM) physical volume <: press enter >')
    name = input_string()
    return name

name_physical_volume = name_physical_volume()

crypt_options = test_crypt_options()
variable = crypt_options_digest()


def luks_key_decrypt():
        luks_key_decrypt_process = subprocess.run(['sudo', 'gpg', '--decrypt', s+'/luks-key.gpg', '|', 'cryptsetup', variable[0], 'luksOpen', luks, name_physical_volume])

def luks_sub_prefab():
    command = []
    command = crypt_options_digest(crypt_options)
    process = subprocess.Popen(['sudo', 'cryptsetup'] + command, stdout = subprocess.PIPE, shell=False)
