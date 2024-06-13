#!/usr/bin/env python
import curses
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem, SubmenuItem
from curses_menu import CursesMenu
from asuka_menu import AsciiArt



def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)

    # menu_items = ["A", "B", "C", "EXIT"]
    # menu = Menu(menu_items)


    art = AsciiArt("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
    menu = CursesMenu("Root Menu", "Root Menu Subtitle", width=curses.COLS // 2, ascii_art=art)
    item1 = MenuItem("basic Item doing nothing", menu)
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

    command_item_six = CommandItem(
        "Overwrite Drive Create Luks Key and Cryptsetup",
        f"python options_input_test.py"
    )

    command_item_seven = CommandItem(
        "Create LVM Data Structure On Disk", 
        f"python lvm_class.py"
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

    submenu_key_crypt = CursesMenu("Wipe Disk With Pseudo Random Data Create Key File and Cryptsetup", "Pseudo Key Crypt")
    submenu_key_crypt.items.append(command_item_six)
    submenu_item_key_crypt = SubmenuItem("Wipe Disk Create Key File & Set Cryptsetup", submenu=submenu_key_crypt, menu=menu)

    submenu_lvm_crypt = CursesMenu("Create Lvm Structure", "LVM Structure Creation")
    submenu_lvm_crypt.items.append(command_item_seven)
    submenu_item_lvm_crypt = SubmenuItem("LVM Structure Creation", submenu=submenu_lvm_crypt, menu=menu)

    submenu_four = CursesMenu("Part Four Submenu", "Part Four")
    submenu_four.items.append(submenu_item_fdisk)
    submenu_four.items.append(submenu_item_mkfsvfat)
    submenu_four.items.append(submenu_item_mkefidir)
    submenu_four.items.append(submenu_item_key_crypt)
    submenu_four.items.append(submenu_item_lvm_crypt)
    submenu_item_four = SubmenuItem("LUKS LVM ", submenu=submenu_four, menu=menu)

    menu.items.append(item1)
    menu.items.append(command_item)
    menu.items.append(submenu_item)
    menu.items.append(submenu_item_2)
    menu.items.append(submenu_item_options)
    menu.items.append(submenu_item_four)
    menu.start()
    _ = menu.join()
    
    
    # curses.wrapper(ascii_art, "/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")

    while True:
        #art.draw_menu(stdscr)
        # if menu.ascii_art:
        #     menu.ascii_art.draw_menu(stdscr)
        stdscr.refresh()
        #art.handle_input(key)

        # Add functionality for other menu items here
        
        if menu.should_exit:
            break


if __name__ == "__main__":
    curses.wrapper(main)
# app = CursedPrint()
# app.start()
# app.ascii_art("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
# app.start()
