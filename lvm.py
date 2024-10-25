#!/usr/bin/env python3

''' objects and functions neccesary to create lvm structure '''
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

def test_process():
        subprocess.run(['sudo', 'cryptsetup', 'luksFormat', '/dev/sdb'])

test_process()

def test_processes():
        subprocess.run(['sudo', 'cryptsetup', 'luksOpen', '/dev/sdb', 'gentoo'])

test_processes()

def name_physical_volume():
    print_curses('please enter a name for a logical volume management (LVM) physical volume <: press enter >')
    name = input_string()
    return name

name_physical_volume = name_physical_volume()

def pvcreate_process():
    subprocess.run(['sudo', 'pvcreate', '/dev/mapper/'+name_physical_volume])

pvcreate_process()

def name_volume_group():
    print_curses('please enter a name for the volume group to lie within the physical volume <: press enter >')
    name = input_string()
    return name

name_volume_group = name_volume_group()

def vgcreate_process():
    subprocess.run(['sudo', 'vgcreate', name_volume_group, '/dev/mapper/'+name_physical_volume])

vgcreate_process()

def proc_meminfo():
    memory = subprocess.check_output(['grep', 'MemTotal', '/proc/meminfo'])
    print_curses(str(memory))

proc_meminfo()

class Lvcreate_Container():
        def __init__(self, lvcreateDictionary):
                self.lvcreateDictionary = lvcreateDictionary.get("lvcreateDictionary", [])
                for key, value in lvcreateDictionary.items():
                        setattr(self, key, value)
                
lvcreate_swap_prefab = {
    "size": "null",
    "name": "null",
    "extents": "null",
}

print_curses("please enter values for the size and name respectively of your swap partition <: press enter >")
print_curses("the format should be of the following. <: press enter >")
print_curses("size should be suffixed with M or G as Megs or Gigs respective ie. 10G for 10 Gigabytes <: press enter >")
print_curses("name is simply written as a simple input string. <: press enter > ")
print_curses("the extents options may be left null or simply skipped by pressing enter, it will be used later <: press enter >")
print_curses("hajime (begin) <: press enter >")

for key, value in lvcreate_swap_prefab.items():
                        if value == "null":
                                lvcreate_swap_prefab[key]=input_string()
                                print_curses(str(lvcreate_swap_prefab))

#print_curses("please enter values custom dictionary")
#n = 4
#lvcreateDictionary = dict(input().split() for _ in range(n))

lvcreate_swap_dictionary = Lvcreate_Container(lvcreate_swap_prefab)

print_curses("now please do the same for your root portion of the volume group you've named within your physical volume <: press enter >")
print_curses("size suffixed with M or G followed by category name again followed by extents which may be skipped <: press enter >")
print_curses("hajime (begin) <: press enter >")

lvcreate_root_prefab = {
    "size": "null",
    "name": "null",
    "extents": "null",
}

for key, value in lvcreate_root_prefab.items():
                        if value == "null":
                                lvcreate_root_prefab[key]=input_string()
                                print_curses(str(lvcreate_root_prefab))

lvcreate_root_dictionary = Lvcreate_Container(lvcreate_root_prefab)

print_curses("the last dictionary may skip size. <: press enter > ")
print_curses("lastly we will fill in our home directory. <: press enter > ")
print_curses("here we shall use the extents option with your input. <: press enter > ")
print_curses("note the format for extents is some 'NUM'%FREE i.e. 95%FREE <: press enter >")
print_curses("this is done to variably fill the remaining harddrive space on disk in order to fill either all or some. <: press enter >")
print_curses("hajime (begin) <: press enter >")

lvcreate_home_prefab = {
    "size": "null",
    "name": "null",
    "extents": "null",
}

for key, value in lvcreate_home_prefab.items():
                        if value == "null":
                                lvcreate_home_prefab[key]=input_string()
                                print_curses(str(lvcreate_home_prefab))

lvcreate_home_dictionary = Lvcreate_Container(lvcreate_home_prefab)


def lvcreate_swap():
        subprocess.run(['sudo', 'lvcreate', '--size', lvcreate_swap_dictionary.size, '--name', lvcreate_swap_dictionary.name, name_volume_group])

lvcreate_swap()

def lvcreate_root():
        subprocess.run(['sudo', 'lvcreate', '--size', lvcreate_root_dictionary.size, '--name', lvcreate_root_dictionary.name, name_volume_group])

lvcreate_root()

def lvcreate_home():
        subprocess.run(['sudo', 'lvcreate', '--extents', lvcreate_home_dictionary.extents, '--name', lvcreate_home_dictionary.name, name_volume_group])

lvcreate_home()

def pv_display():
    pv_display = subprocess.check_output([ 'sudo', 'pvdisplay'])
    print_curses(str(pv_display))

pv_display()

def vg_display():
    vg_display = subprocess.check_output(['sudo', 'vgdisplay'])
    print_curses(str(pv_display))

vg_display()

def lv_display():
    lv_display = subprocess.check_output(['sudo', 'lvdisplay'])
    print_curses(str(lv_display))

lv_display()

def vg_change():
        subprocess.run(['vgchange', '--available', 'y'])

def ls_devmapper():
        ls_devmapper = subprocess.check_output(['ls', '/dev/mapper'])
        print_curses(str(ls_devmapper))

def mk_swap():
    mk_swap = ["mkswap", "-L", lvcreate_swap_dictionary.name, "/dev/mapper/" + name_volume_group + "-" + lvcreate_swap_dictionary.name]
    subprocess.run(mk_swap)

mk_swap()

def mk_ext4_root():
    mk_ext4 = ["mkfs.ext4", "-L", lvcreate_root_dictionary.name, "/dev/mapper/" + name_volume_group + "-" + lvcreate_root_dictionary.name]
    subprocess.run(mk_ext4)

mk_ext4_root()

def mk_ext4_home():
    mk_ext4 = ["mkfs.ext4", "-m", "0", "-L", "home", "/dev/mapper/"+name_volume_group + "-" + lvcreate_home_dictionary.name]
    subprocess.run(mk_ext4)

mk_ext4_home()

def mk_swap_on():
    subprocess.run(["swapon", "-v", "/dev/mapper/"+ name_volume_group + "-" + lvcreate_swap_dictionary.name])

def mkdir_mnt_gentoo():
    subprocess.run(["sudo", "mkdir", "-v", "/mnt/gentoo/"])

mkdir_mnt_gentoo()

def mount_mnt_gentoo():
    subprocess.run(["sudo", "mount", "-v", "-t", "ext4", "/dev/mapper/" + name_volume_group + "-" +lvcreate_root_dictionary.name, "/mnt/gentoo"])

mount_mnt_gentoo()

def mkdir_home_boot_efi():
    subprocess.run(["sudo", "mkdir", "-v", "/mnt/gentoo/{home,boot,boot/efi}"])

mkdir_home_boot_efi()

def umount_efiboot():
    subprocess.run(["sudo", "umount", "-v", "/tmp/efiboot"])








