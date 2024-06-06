#!/usr/bin/env python

import curses
from curses import panel
from dd_class_table import dd_sources, Dd_Table
from cryptsetup_class import sources, Crypt_Table
from cursedprint import CursedPrint
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem, SubmenuItem


dd = Dd_Table()
dd.start()

menu  = CursesMenu("Root Menu", "Root Menu Subtitle")
item1 = MenuItem("basic Item doing nothing", menu)
function_item = FunctionItem("dd", dd.dd_options_digest, dd_sources)
print(__file__)
command_item = CommandItem(
    "CommandItem that opens another menu", 
    f"python {__file__}", 
)

command_item_two = CommandItem(
    "CommandItem that opens dd menu", 
    f"python dd_class_table.py", 
)

command_item_three = CommandItem(
    "Fdisk Process On Block Device",
    f"python fdisk_process.py",
)

command_item_four = CommandItem(
    "Format Block Device Mkfs.Vfat",
    f"python mkfsvfat.py",
)

command_item_five = CommandItem(
    "Create EFI Directory",
    f"python create_efi.py"
)

submenu = CursesMenu.make_selection_menu([f"item{x}" for x in(1, 20)])
submenu_item = SubmenuItem("Long Selection SubMenu", submenu=submenu, menu=menu)


submenu_2 = CursesMenu("Submenu Title", "Submenu subtitle")
function_item_2 = FunctionItem("Fun item", input, ["enter an input"])
item2 = MenuItem("Another Item")
submenu_2.items.append(function_item_2)
submenu_2.items.append(item2)
submenu_item_2 = SubmenuItem("Short Submenu", submenu=submenu_2, menu=menu)

submenu_options = CursesMenu("Options Submenu", "Options")
submenu_options.items.append(command_item_two)
submenu_item_options = SubmenuItem("Options Submenu", submenu=submenu_options, menu=menu)

submenu_fdisk_process = CursesMenu("Fdisk Process", "Fdisk Process")
submenu_fdisk_process.items.append(command_item_three)
submenu_item_fdisk = SubmenuItem("Fdisk Process", submenu=submenu_fdisk_process, menu=menu)

submenu_mkfsvfat = CursesMenu("Format Mkfsvfat", "MKfsVfat")
submenu_mkfsvfat.items.append(command_item_four)
submenu_item_mkfsvfat = SubmenuItem("Format Mkfsvfat", submenu=submenu_mkfsvfat, menu=menu)

submenu_mkefidir = CursesMenu("Create EFI Directory", "Create EFI")
submenu_mkefidir.items.append(command_item_five)
submenu_item_mkefidir = SubmenuItem("Create EFI Directory", submenu=submenu_mkefidir, menu=menu)

submenu_four = CursesMenu("Part Four Submenu", "Part Four")
submenu_four.items.append(submenu_item_fdisk)
submenu_four.items.append(submenu_item_mkfsvfat)
submenu_four.items.append(submenu_item_mkefidir)
submenu_item_four = SubmenuItem("Part Four Submenu", submenu=submenu_four, menu=menu)




menu.items.append(item1)
menu.items.append(function_item)
menu.items.append(command_item)
menu.items.append(submenu_item)
menu.items.append(submenu_item_2)
menu.items.append(submenu_item_options)
menu.items.append(submenu_item_four)
menu.start()
_ = menu.join()