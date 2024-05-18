#! /usr/bin/env python3

import subprocess
from cursesprint import print_curses
import curses
import json
import pandas as pd

import numpy
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

block_device_name = return_blockdev_name()



stdscr = curses.initscr()
pandas_block_devices = return_pandas()

print_curses(stdscr,block_device_name)
print_curses(stdscr, pandas_block_devices.to_numpy)