#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json


class DictionaryDevice:
    def __init__(self, dictionary_devices):
        self.dictionary_devices = dictionary_devices.get("blockdevices",[])
        for device in self.dictionary_devices:
                for key, value in dictionary_devices.items():
                        setattr(self, key, value)

        def __iter__(self):
            for device in self.dictionary_devices:
                for value in self.dictionary_devices.values():
                        yield value

        def dictionarydeviceiter(self):
            return iter(self.dictionary_devices.values())

def dictionary_test_table(dictionary_command_line):
    return DictionaryDevice(dictionary_command_line)

def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)


def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

block_devices = return_blockdev_name()


dict_table = dictionary_test_table(block_devices)

def main(stdscr):
    x = 0
    stdscr = curses.initscr()
    m = 0
    def index():
        index = 0
        list = []
        while index < len(dict_table.dictionary_devices):
            index += 1
            list.append(len(dict_table.dictionary_devices[index]))
            list.sort()
            for x in list:
                if max(list) == len(dict_table.dictionary_devices[index].values()):
                    maximum_of_list = max(list)
                    return index
    
    indexed = index()

    table = Table(stdscr, len(dict_table.dictionary_devices), len(block_devices['blockdevices'][0]),20, 120, 20, spacing=1, col_names=True)

    m = 0 
    while m < len(dict_table.dictionary_devices):
        for n in dict_table.dictionary_devices[indexed].values():
            table.set_column_header("Col " + str(m + 1), m)
        m += 1
    m = 0
    for m in range(len(block_devices['blockdevices'])):
        n = 0
        index = 0
        key = 0
        while n < len(block_devices['blockdevices']):
            while index < len(block_devices['blockdevices']):
                for key in block_devices['blockdevices'][index]:
                    table.set_cell(m, n, block_devices['blockdevices'][index][key])
                    n += 1
                index += 1
        m += 1


    # m = 0
    # while m < len(dict_table.dictionary_devices):
    #     n = 0
    #     while n < len(dict_table.dictionary_devices):
    #         key = dict_table.dictionary_devices[m]
    #         table.set_cell(m, n, key['name'])
    #         n += 1
                                 
        m += 1
    table.delete_row(2)
    while ( x != 'q'):
        table.refresh()
        x = stdscr.getkey()
        if ( x == 'a'):
            table.cursor_left()
        elif ( x == 'd'):
            table.cursor_right()
        elif (x == 's'):
            table.cursor_down()
        elif (x == 'w'):
            table.cursor_up()
    


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

curses.wrapper(main)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()