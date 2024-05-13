#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd


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

pandas_dict = return_blockdev_name()
new_table = pd.json_normalize(pandas_dict['blockdevices'])


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

    table = Table(stdscr, len(new_table), (len(new_table.columns)), 20, 100, 10, spacing=1, col_names=True)

    m = 0 
    while m < len(new_table.columns):
        table.set_column_header(new_table.columns[m], m)
        m += 1
    m = 0
    numpy_table = new_table.to_numpy()
    while m < len(new_table):
        n = 0
        while n < len(new_table.columns):
                table.set_cell(m, n, numpy_table[m][n])
                n += 1
        m += 1
    
    
    # m = 0
    # while m < len(dict_table.dictionary_devices):
    #     n = 0
    #     while n < len(dict_table.dictionary_devices):
    #         key = dict_table.dictionary_devices[m]
    #         table.set_cell(m, n, key['name'])
    #         n += 1
                                 
        m += 1
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
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
curses.wrapper(main)