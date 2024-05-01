#!/usr/bin/env python3

''' gentoo building basic of the distribution '''

import logging
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
from lvm import name_physical_volume
print_curses("testing whether booted in uefi or bios")


def check_uefi():
        booted = "UEFI" 
        if os.path.exists("/sys/firmware/efi"): 
                print_curses("booted UEFI")
        else: 
                print_curses("booted BIOS")

check_uefi()

def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

block_devices = return_blockdev_name()

print_curses("showing all available block devices")
print_curses(str(block_devices.items()))

class BlockDevice:
    def __init__(self, block_devices):
        self.block_devices = block_devices.get("blockdevices",[])
        for device in self.block_devices:
                for key, value in block_devices.items():
                        setattr(self, key, value)

        def __iter__(
                self):
                for value in self.block_devices.values():
                        yield value

        def blockdeviceiter(self):
                return iter(self.block_device.values())

                
block_device_selection_list = BlockDevice(block_devices)
print_curses(str(block_device_selection_list.block_devices))


def fdisk_process(): 
        print_curses("fdisk process about to be run on selected block device")
        print_curses("after pressing enter please enter a block device path for selection")
        block_device_selection = input_string()
        for item in block_device_selection_list.block_devices:
                if item['path'] == block_device_selection:
                        print_curses("successfully matched input string to device path")
                        print_curses(str(item))
                        print_curses(str(item['path']))
                        args = item['path']
                        subprocess.run(['fdisk', args])
                else:
                        print_curses("no match <press enter>")

def block_device_selection():
        print_curses("please enter a block device path for block device selection < press enter >")
        block_device_selection = input_string()
        selected = {}
        for item in block_device_selection_list.block_devices:
                if item['path'] == block_device_selection:
                        print("success")
                        selected = {}
                        print(item)
                        print(item['path'])
                        selected['path'] = item['path']
                        return selected['path']
                else:
                        print("no matching block device found")

print_curses("you will now be asked by an fdisk function to select a block device for paritioning")
print_curses("this block device will be used for your usb key")
fdisk_process()

print_curses("the selected usb key will now be formatted to fat32 using mkfs")
print_curses("you'll now be asked again to enter the path to said block device for formatting")

format_block_device = block_device_selection()

def mkfs_vfat():
        subprocess.run(['mkfs.vfat', '-F32', format_block_device])
        print_curses("successfully formatted devie -F32")

def variable_dictionary():
        dictionary = {}
        print_curses("please enter the number of entries to enter n: ")
        n = int(input_string())
        print_curses("now enter key value pair followed by <: enter > of each item in dictionary <: press enter >")
        dictionary = dict(input().split() for _ in range(int(n)))
        return dictionary

print("//////////////////////////////////////////////////////////////////////////////////////////////")
print_curses("/ for the following few functions a menu will be filled by you with key value entries /")
print_curses("/ for the key value entries make sure to make all keys unique all values meaningful   /")                                                                                     
print("//////////////////////////////////////////////////////////////////////////////////////////////")

print_curses("you must now enter a directory name to be made for our efi boot directory")     
directory_list = variable_dictionary()
print_curses(str(directory_list))
s = menu(directory_list)[0]
print_curses("here is the value selected for ")
print_curses(s)
def mkdir():
        subprocess.run(['mkdir', '-v', s])

mkdir()


def mount():
        subprocess.run(['mount', '-v', '-t', s])

print_curses("enter the main drive to parition")

fdisk_process()

print_curses("please enter values for a luks dictionary of custom key value pairs for formatting input")
print_curses("you will now fill created class luksContainer with correct --cipher --keysize --hash --keyfile options")

n = 4
luksDictionary = dict(input().split() for _ in range(n))
print_curses(str(luksDictionary))

print_curses("please enter values for a luks dictionary of prefabricated key values for formatting input")
luksDictionaryPrefab = {
        "cipher": "null",
        "keysize": "null",
        "hash" : "null",
        "keyfile" : "null",
}

for key, value in luksDictionaryPrefab.items():
                        if value == "null":
                                luksDictionaryPrefab[key]=input()
                                print(luksDictionaryPrefab)
                        
print_curses(str(luksDictionaryPrefab))
 
class LuksContainer:
        def __init__(self, luksDictionary):
                self.luksDictionary = luksDictionary.get("luksDictionary", [])
                for key, value in luksDictionary.items():
                        setattr(self, key, value)

luks_dictionary = LuksContainer(luksDictionaryPrefab)

print_curses(str(block_device_selection_list.blockdevices))

print_curses("select a block device to format with cryptsetup")

def block_device_selection_two():
        print_curses(str(block_devices.items()))
        #block_device_selection = input("select a blockdevice : \n")
        dictionary = variable_dictionary()
        block_device_selection = menu(dictionary)[0]
        for item in block_device_selection_list.block_devices:
                if item['path'] == block_device_selection:
                        print("success")
                        selected = {}
                        print(item)
                        print(item['path'])
                        selected['path'] = item['path']
                        return selected['path']
                else:
                        print("no matching block device found")

luks = block_device_selection_two()
print_curses(str(block_device_selection_list.blockdevices))

def gpg_tty(): 
        subprocess.run(['export', 'GPG_TTY=$(tty)'])

def luks_key():
        subprocess.run('dd', 'if=/dev/urandom', 'bs=8388607', 'count=1', '|', 'gpg', '--symmetric', '--cipher-algo', 'AES256', '--output', s+'/luks-key.gpg')

print_curses(str(luks_dictionary.cipher))
def luks_process_prefab():              
        luks_process = subprocess.run(['cryptsetup', '--cipher', luks_dictionary.cipher, '--key-size', luks_dictionary.keysize, '--hash', luks_dictionary.hash, '--key-file', luks_dictionary.keyfile, 'luksFormat', luks])

luks_process_prefab()

name_physical_volume = name_physical_volume()

def luks_key_decrypt():
        luks_key_decrypt_process = subprocess.run(['gpg', '--decrypt', s+'/luks-key.gpg', '|', 'cryptsetup', '--key-file', luks_dictionary.keyfile, 'luksOpen', luks, name_physical_volume])







