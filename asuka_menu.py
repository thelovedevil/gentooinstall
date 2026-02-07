#!/usr/bin/env python3

import curses
import locale

locale.setlocale(locale.LC_ALL, '')
import subprocess
from curses import panel
from cryptsetup_class_table import sources, Crypt_Table
from curses_menu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem



# class Menu:
#     def __init__(self, items):
#         self.items = items
#         self.current_idx = 0

#     def draw_menu(self, stdscr):
#         h, w = stdscr.getmaxyx()
#         for idx, row in enumerate(self.items):
#             x = 1
#             y = idx + 1
#             if idx == self.current_idx:
#                 stdscr.attron(curses.color_pair(1))
#                 stdscr.addstr(y, x, row)
#                 stdscr.attroff(curses.color_pair(1))
#             else:
#                 stdscr.addstr(y, x, row)
#         stdscr.refresh()
    
#     def handle_input(self, key):
#         if key == curses.KEY_UP:
#             self.current_idx = (self.current_idx - 1) % len(self.items)
#         elif key == curses.KEY_DOWN:
#             self.current_idx = (self.current_idx + 1) % len(self.items)
#         elif key == curses.KEY_ENTER or key in [10, 13]:
#             return self.current_idx
#         return None


from ui.ascii_art import AsciiArt
        

        # if key == curses.KEY_UP and start_row > 0:
        #     start_row -= 1
        # elif key == curses.KEY_DOWN and start_row < art_height - (curses.LINES - 2):
        #     start_row += 1
        # elif key == curses.KEY_LEFT and start_col > 0:
        #     start_col -= 1
        # elif key == curses.KEY_RIGHT and start_col < art_width - (curses.COLS - 20):
        #     start_col += 1
        # elif key == curses.KEY_UP:
        #     current_row_idx = (current_row_idx - 1) % len(menu_items)
        # elif key == curses.KEY_DOWN:
        #     current_row_idx = (current_row_idx + 1) % len(menu_items)
        # elif key == curses.KEY_ENTER or key in [10, 13]:
        #     if current_row_idx == len(menu_items) - 1:
        #         break
        # elif key == ord('q'):
        #     break
# ///////////////////////////////////////////////////////////////////
#         art_height, art_width = ascii_matrix.shape

#         start_y = (height - art_height) // 2
#         start_x = (width - art_width) // 2
    
#         for i in range(art_height):
#             for j in range(art_width):
#                 stdscr.addstr(start_y + i, start_x + j, ascii_matrix[i, j])
    
#         self.screen.refresh()
    
#         self.screen.getch()
    
# ////////////////////////////////////////////////////////////////////////////////////

    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    # self.screen.bkgd(' ', curses.color_pair(1))
    # self.screen.clear()
    # self.screen.addstr(str(variable))
    # #self.screen.scrollok(1)
    # self.screen.refresh()
    # self.screen.getch()
    # curses.noecho()
    # curses.cbreak()
    # stdscr.keypad(True)

    
# def main(stdscr):
#     curses.curs_set(0)
#     curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)

#     # menu_items = ["A", "B", "C", "EXIT"]
#     # menu = Menu(menu_items)

#     dd = Dd_Table()
#     dd.start()

#     menu  = CursesMenu("Root Menu", "Root Menu Subtitle", width=curses.COLS // 2)
#     item1 = MenuItem("basic Item doing nothing", menu)
#     function_item = FunctionItem("dd", dd.dd_options_digest, dd_sources)
#     print(__file__)
#     command_item = CommandItem(
#         "CommandItem that opens another menu", 
#         f"python {__file__}", 
#     )

#     command_item_two = CommandItem(
#         "CommandItem that opens dd menu", 
#         f"python dd_class_table.py", 
#     )

#     command_item_three = CommandItem(
#         "Fdisk Process On Block Device",
#         f"python fdisk_process.py",
#     )

#     command_item_four = CommandItem(
#         "Format Block Device Mkfs.Vfat",
#         f"python mkfsvfat.py",
#     )

#     command_item_five = CommandItem(
#         "Create EFI Directory",
#         f"python create_efi.py"
#     )

#     command_item_six = CommandItem(
#         "Overwrite Drive Create Luks Key and Cryptsetup",
#         f"python options_input_test.py"
#     )

#     command_item_seven = CommandItem(
#         "Create LVM Data Structure On Disk", 
#         f"python lvm_class.py"
#     )

#     submenu = CursesMenu.make_selection_menu([f"item{x}" for x in(1, 20)])
#     submenu_item = SubmenuItem("Long Selection SubMenu", submenu=submenu, menu=menu)


#     submenu_2 = CursesMenu("Submenu Title", "Submenu subtitle")
#     function_item_2 = FunctionItem("Fun item", input, ["enter an input"])
#     item2 = MenuItem("Another Item")
#     submenu_2.items.append(function_item_2)
#     submenu_2.items.append(item2)
#     submenu_item_2 = SubmenuItem("Short Submenu", submenu=submenu_2, menu=menu)

#     submenu_options = CursesMenu("Options Submenu", "Options")
#     submenu_options.items.append(command_item_two)
#     submenu_item_options = SubmenuItem("Options Submenu", submenu=submenu_options, menu=menu)

#     submenu_fdisk_process = CursesMenu("Fdisk Process", "Fdisk Process")
#     submenu_fdisk_process.items.append(command_item_three)
#     submenu_item_fdisk = SubmenuItem("Fdisk Process", submenu=submenu_fdisk_process, menu=menu)

#     submenu_mkfsvfat = CursesMenu("Format Mkfsvfat", "MKfsVfat")
#     submenu_mkfsvfat.items.append(command_item_four)
#     submenu_item_mkfsvfat = SubmenuItem("Format Mkfsvfat", submenu=submenu_mkfsvfat, menu=menu)

#     submenu_mkefidir = CursesMenu("Create EFI Directory", "Create EFI")
#     submenu_mkefidir.items.append(command_item_five)
#     submenu_item_mkefidir = SubmenuItem("Create EFI Directory", submenu=submenu_mkefidir, menu=menu)

#     submenu_key_crypt = CursesMenu("Wipe Disk With Pseudo Random Data Create Key File and Cryptsetup", "Pseudo Key Crypt")
#     submenu_key_crypt.items.append(command_item_six)
#     submenu_item_key_crypt = SubmenuItem("Wipe Disk Create Key File & Set Cryptsetup", submenu=submenu_key_crypt, menu=menu)

#     submenu_lvm_crypt = CursesMenu("Create Lvm Structure", "LVM Structure Creation")
#     submenu_lvm_crypt.items.append(command_item_seven)
#     submenu_item_lvm_crypt = SubmenuItem("LVM Structure Creation", submenu=submenu_lvm_crypt, menu=menu)

#     submenu_four = CursesMenu("Part Four Submenu", "Part Four")
#     submenu_four.items.append(submenu_item_fdisk)
#     submenu_four.items.append(submenu_item_mkfsvfat)
#     submenu_four.items.append(submenu_item_mkefidir)
#     submenu_four.items.append(submenu_item_key_crypt)
#     submenu_four.items.append(submenu_item_lvm_crypt)
#     submenu_item_four = SubmenuItem("LUKS LVM ", submenu=submenu_four, menu=menu)

#     menu.items.append(item1)
#     menu.items.append(function_item)
#     menu.items.append(command_item)
#     menu.items.append(submenu_item)
#     menu.items.append(submenu_item_2)
#     menu.items.append(submenu_item_options)
#     menu.items.append(submenu_item_four)
#     art = AsciiArt("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
#     menu.set_ascii_art(art)
#     menu.start()
    
#     # curses.wrapper(ascii_art, "/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")

#     while True:
#         stdscr.clear()
#         menu.draw()
#         art.draw_menu(stdscr)

#         key = stdscr.getch()
#         menu.process_user_input(key)
#         # selected_idx = menu.handle_input(key)
#         art.handle_input(key)

#         # if selected_idx is not None:
#         #     if menu.items[selected_idx] == 'EXIT':
#         #         break
#         # Add functionality for other menu items here

#         if menu.should_exit:
#             break


# if __name__ == "__main__":
#     curses.wrapper(main)
# # app = CursedPrint()
# # app.start()
# # app.ascii_art("/home/adrian/Documents/gentooinstall/asuka_original_resized.jpg")
# # app.start()
