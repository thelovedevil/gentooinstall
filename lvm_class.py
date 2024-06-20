#!/usr/bin/env python3

''' objects and functions neccesary to create lvm structure '''
import subprocess
from subprocess import Popen, PIPE
import curses
import cursesscrollmenu
from cursesscrollmenu import menu
from cursesprint import print_curses
from cursedinput import Input
from cursedprint import CursedPrint
from block_device_class_table import Block_Table, return_pandas
import moby_dick
from cursedprint_white import CursedPrintWhite\

block_sources = return_pandas()

input_app = Input()
input_app.start()

print_app = CursedPrint()
print_app.start()

print_app_white = CursedPrintWhite()
print_app_white.start()

blockdevice_app = Block_Table()
blockdevice_app.start()

def block_options_input():
    dictionary = {}
    string = moby_dick.block_options()
    print_app.print_curses(string)
    n = int(input_app.input_string())

    for i in range(n):
        string = moby_dick.instructions()
        print_app.print_curses(string)
        option = []
        option = blockdevice_app.block_digest(block_sources)
        value = []
        string_two = moby_dick.enter_value()
        print_app.print_curses(string_two)
        value = blockdevice_app.block_digest(block_sources)
        final = [j for i in zip(option, value) for j in i]
        print(final)
        return final

block_command = []
block_command = block_options_input()
print(block_command)

def name_physical_volume(): 
    string = moby_dick.physical_volume()
    print_app.print_curses(string)
    name = input_app.input_string()
    return name   

# def name_physical_volume():
#     print_app.print_curses('please enter a name for a logical volume management (LVM) physical volume <: press enter >')
#     name = input_app.input_string()
#     return name

name_physical_volume = name_physical_volume()

def pvcreate_process():
    subprocess.run(['sudo', 'pvcreate', '/dev/mapper/'+name_physical_volume])

pvcreate_process()

def name_volume_group():
    string = moby_dick.volume_group()
    print_app.print_curses(string)
    name = input_app.input_string()
    return name

name_volume_group = name_volume_group()

def vgcreate_process():
    subprocess.run(['sudo', 'vgcreate', name_volume_group, '/dev/mapper/'+name_physical_volume])

vgcreate_process()

def proc_meminfo():
    memory = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], check=True, capture_output=True, text=True).stdout
    print_app.print_curses(memory)

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
lvm_string = moby_dick.lvm_instructions()

print_app.print_curses(lvm_string)

for key, value in lvcreate_swap_prefab.items():
                        if value == "null":
                                print_app.print_curses(lvcreate_swap_prefab)
                                lvcreate_swap_prefab[key]=input_app.input_string()
                                print_app.print_curses(str(lvcreate_swap_prefab))

#print_curses("please enter values custom dictionary")
#n = 4
#lvcreateDictionary = dict(input().split() for _ in range(n))

lvcreate_swap_dictionary = Lvcreate_Container(lvcreate_swap_prefab)

lvm_string_two = moby_dick.sec_lvm_instructions()

print_app.print_curses(lvm_string_two)

lvcreate_root_prefab = {
    "size": "null",
    "name": "null",
    "extents": "null",
}

for key, value in lvcreate_root_prefab.items():
                        if value == "null":
                                print_app.print_curses(lvcreate_root_prefab)
                                lvcreate_root_prefab[key]=input_app.input_string()
                                print_app.print_curses(str(lvcreate_root_prefab))

lvcreate_root_dictionary = Lvcreate_Container(lvcreate_root_prefab)

lvm_string_three = moby_dick.third_lvm_instructions()

print_app.print_curses(lvm_string_two)

lvcreate_home_prefab = {
    "size": "null",
    "name": "null",
    "extents": "null",
}

for key, value in lvcreate_home_prefab.items():
                        if value == "null":
                                print_app.print_curses(lvcreate_home_prefab)
                                lvcreate_home_prefab[key]=input_app.input_string()
                                print_app.print_curses(lvcreate_home_prefab)

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
    pv_display = subprocess.run([ 'sudo', 'pvdisplay'], check=True, capture_output=True, text=True).stdout
    print_app_white.print_curses(str(pv_display))

pv_display()

def vg_display():
    vg_display = subprocess.run(['sudo', 'vgdisplay'], check=True, capture_output=True, text=True).stdout
    print_app_white.print_curses(str(pv_display))

vg_display()

def lv_display():
    lv_display = subprocess.run(['sudo', 'lvdisplay'], check=True, capture_output=True, text=True).stdout
    print_app_white.print_curses(str(lv_display))

lv_display()

def vg_change():
        subprocess.run(['vgchange', '--available', 'y'])

def ls_devmapper():
        ls_devmapper = subprocess.run(['ls', '/dev/mapper'], check=True, capture_output=True, text=True).stdout
        print_app_white.print_curses(str(ls_devmapper))

def mk_swap():
    mk_swap = ["mkswap", "-L", lvcreate_swap_dictionary.name, "/dev/mapper/" + name_volume_group[0] + "-" + lvcreate_swap_dictionary.name]
    subprocess.run(mk_swap)

mk_swap()

def mk_ext4_root():
    mk_ext4 = ["mkfs.ext4", "-L", lvcreate_root_dictionary.name, "/dev/mapper/" + name_volume_group[0] + "-" + lvcreate_root_dictionary.name]
    subprocess.run(mk_ext4)

mk_ext4_root()

def mk_ext4_home():
    mk_ext4 = ["mkfs.ext4", "-m", "0", "-L", "home", "/dev/mapper/"+ name_volume_group[0] + "-" + lvcreate_home_dictionary.name]
    subprocess.run(mk_ext4)

mk_ext4_home()

def mk_swap_on():
    subprocess.run(["swapon", "-v", "/dev/mapper/"+ name_volume_group[0] + "-" + lvcreate_swap_dictionary.name])

def mkdir_mnt_gentoo():
    subprocess.run(["sudo", "mkdir", "-v", "/mnt/gentoo/"])

mkdir_mnt_gentoo()

def mount_mnt_gentoo():
    subprocess.run(["sudo", "mount", "-v", "-t", "ext4", "/dev/mapper/" + name_volume_group[0] + "-" + lvcreate_root_dictionary.name, "/mnt/gentoo"])

mount_mnt_gentoo()

def mkdir_home_boot_efi():
    subprocess.run(["sudo", "mkdir", "-v", "/mnt/gentoo/{home,boot,boot/efi}"])

mkdir_home_boot_efi()

def umount_efiboot():
    subprocess.run(["sudo", "umount", "-v", "/tmp/efiboot"])








