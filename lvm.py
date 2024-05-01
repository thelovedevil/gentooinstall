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
from cursesprint import print_curses\
from fdiskluks import variable_dictionary

def name_physical_volume():
    print_curses('please enter a name for a logical volume management (LVM) physical volume')
    name = input_string()
    return name

name_physical_volume = name_physical_volume()

def pvcreate_process():
    subprocess.run(['sudo', 'pvcreate', '/dev/mapper/'+name_physical_volume])

def name_volume_group():
    print_curses('please enter a name for the volume group to lie within the physical volume')
    name = input_string()
    return name



name_volume_group = name_volume_group()

def vgcreate_process():
    subprocess.run(['sudo', 'vgcreate', name_volume_group, '/dev/mapper/'+name_physical_volume])


def proc_meminfo():
   memory = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'])

proc_meminfo()

class Lvcreate_Container():
        def __init__(self, lvcreateDictionary):
                self.lvcreateDictionary = lvcreateDictionary.get("lvcreateDictionary", [])
                for key, value in lvcreateDictionary.items():
                        setattr(self, key, value)
                
lvcreate_swap_prefab = {
    'size' = 'null'
    'name' = 'null'
    'extents' = 'null'
}

for key, value in lvcreaet_swap_prefab.items():
                        if value == "null":
                                luksDictionaryPrefab[key]=input()
                                print(lvcreate_swap_prefab)

lvcreateDictionary = dict(input().split() for _ in range(n))

lvcreate_swap_dictionary = Lvcreate_Container(lvcreate_swap_prefab)

lvcreate_root_prefab = {
    'size' = 'null'
    'name' = 'null'
    'extents' = 'null'
}

for key, value in lvcreate_root_prefab.items():
                        if value == "null":
                                lvcreate_root_prefabPrefab[key]=input()
                                print(lvcreate_root_prefab)

lvcreate_root_dictionary = Lvcreate_Container(lvcreate_root_prefab)

lvcreate_home_prefab = {
    'size' = 'null'
    'name' = 'null'
    'extents' = 'null'
}

for key, value in lvcreate_home_prefab.items():
                        if value == "null":
                                lvcreate_home_prefab[key]=input()
                                print(lvcreate_home_prefab)


