#!/usr/bin/env python
import curses
import locale
import os
import shutil
import sys

locale.setlocale(locale.LC_ALL, '')
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem, SubmenuItem
from cursesmenu.curses_menu import CursesMenu
from ui.ascii_art import AsciiArt



def change_art(menu, image_path):
    menu.ascii_art = AsciiArt(image_path)
    menu.draw()

def curses_input_wrapper(prompt):
    from ui.printer import CursedPrinter
    from ui.input import Input
    # CursesMenu.stdscr is a class variable
    if CursesMenu.stdscr:
        printer = CursedPrinter(CursesMenu.stdscr)
        input_handler = Input(printer)
        return input_handler.input_string(prompt)
    return input(prompt)

def main(stdscr):
    curses.curs_set(0)
    
    # Get terminal size
    terminal_width = shutil.get_terminal_size().columns
    art_width = int(terminal_width * 0.6) # Increase to 60%

    # Create the main menu with default art
    art_main = AsciiArt("Pictures/asuka_original_resized.jpg")
    menu = CursesMenu("Gentoo Installer", "Main Menu", ascii_art=art_main, ascii_art_width=art_width)
    
    # --- Installer Tools Submenu ---
    art_tools = AsciiArt("Pictures/asuka_original_resized.jpg")
    tools_menu = CursesMenu("Installer Tools", "Disk and System configuration", ascii_art=art_tools, ascii_art_width=art_width)

    # Submenu for LUKS and LVM
    art_luks = AsciiArt("Pictures/black_white002.jpeg")
    submenu_four = CursesMenu("LUKS & LVM Tools", "Part Four Operations", ascii_art=art_luks, ascii_art_width=art_width)
    
    # Commands for the tools
    command_item_three = CommandItem("Fdisk Process", f"{sys.executable} fdisk_process.py")
    command_item_four = CommandItem("Format Mkfs.Vfat", f"{sys.executable} mkfsvfat.py")
    command_item_five = CommandItem("Create EFI Directory", f"{sys.executable} create_efi.py")
    command_item_six = CommandItem("LUKS Key & Cryptsetup", f"{sys.executable} options_input_test.py")
    command_item_seven = CommandItem("LVM Structure Creation", f"{sys.executable} lvm_class.py")

    submenu_four.items.append(command_item_three)
    submenu_four.items.append(command_item_four)
    submenu_four.items.append(command_item_five)
    submenu_four.items.append(command_item_six)
    submenu_four.items.append(command_item_seven)
    
    submenu_item_four = SubmenuItem("LUKS & LVM Submenu", submenu=submenu_four, menu=tools_menu)
    
    # Other tools
    command_item_two = CommandItem("DD Operations Menu", f"{sys.executable} dd_class_table.py")
    submenu_options = CursesMenu("Options Submenu", "Options", ascii_art=art_tools, ascii_art_width=art_width)
    submenu_options.items.append(command_item_two)
    submenu_item_options = SubmenuItem("DD/Options Submenu", submenu=submenu_options, menu=tools_menu)

    tools_menu.items.append(submenu_item_four)
    tools_menu.items.append(submenu_item_options)
    
    tools_submenu_item = SubmenuItem("Installer Tools", submenu=tools_menu, menu=menu)

    # --- Extras Submenu ---
    art_extras = AsciiArt("Pictures/black_white003.jpg")
    extras_menu = CursesMenu("Extras", "Examples and Customization", ascii_art=art_extras, ascii_art_width=art_width)

    # Art selection
    art_select_menu = AsciiArt("Pictures/black_white004.jpg")
    art_submenu = CursesMenu("Select Art", "Select an image to display", ascii_art=art_select_menu, ascii_art_width=art_width)
    
    # Add items for all images in Pictures
    pictures_dir = "Pictures"
    for img_file in os.listdir(pictures_dir):
        if img_file.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            img_path = os.path.join(pictures_dir, img_file)
            art_submenu.items.append(FunctionItem(img_file, change_art, [menu, img_path]))

    art_submenu_item = SubmenuItem("Change ASCII Art", submenu=art_submenu, menu=extras_menu)

    # Selection Example
    submenu_selection = CursesMenu.make_selection_menu([f"item{x}" for x in(1, 10)], title="Selection Menu")
    submenu_item_selection = SubmenuItem("Long Selection Example", submenu=submenu_selection, menu=extras_menu)

    # Input Example
    art_input = AsciiArt("Pictures/black_white005.jpg")
    submenu_2 = CursesMenu("Input Test", "Testing curses-aware input", ascii_art=art_input, ascii_art_width=art_width)
    function_item_2 = FunctionItem("Test Input Function", curses_input_wrapper, ["Enter some text: "])
    submenu_2.items.append(function_item_2)
    submenu_item_input = SubmenuItem("Input Test Submenu", submenu=submenu_2, menu=extras_menu)

    extras_menu.items.append(art_submenu_item)
    extras_menu.items.append(submenu_item_selection)
    extras_menu.items.append(submenu_item_input)
    
    extras_submenu_item = SubmenuItem("Extras & Examples", submenu=extras_menu, menu=menu)

    # --- Main Menu Construction ---
    menu.items.append(tools_submenu_item)
    menu.items.append(extras_submenu_item)
    
    command_item_self = CommandItem("Open New Root Menu instance", f"{sys.executable} {__file__}")
    menu.items.append(command_item_self)

    menu.start()
    _ = menu.join()
    
    



if __name__ == "__main__":
    curses.wrapper(main)
# app = CursedPrint()
# app.start()
# app.ascii_art("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
# app.start()