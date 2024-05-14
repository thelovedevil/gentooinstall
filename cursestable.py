#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json
import pandas as pd
from cursesprint import print_curses


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

def return_pandas():
    process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
    data = json.loads(process.stdout)
    df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
    df = (pd 
        .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
        .drop(columns=[0, "children"])
        .fillna("")
        .reset_index(drop=True)
        )
    print(df) 
    return df

def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

new_table = return_pandas()


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
    numpy_table = new_table.to_numpy()
    m = 0
    while m < len(new_table):
        n = 0
        while n < (len(new_table.columns)):
                table.set_cell(m, n, numpy_table[m][n])
                n += 1
           
           
        m += 1
    table.refresh()
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
        elif (x == '\n'):
            print_curses(str(table.select(stdscr)))
            
            
    
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
curses.wrapper(main)