#! /usr/bin/env python3

import subprocess
from subprocess import Popen, PIPE
#from cursesprint import print_curses
import curses
import json
import pandas as pd
import ast
import re

import numpy
# def return_pandas():
#     process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE".split(), capture_output=True, text=True)
#     data = json.loads(process.stdout)
#     df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
#     df = (pd 
#         .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
#         .drop(columns=[0, "children"])
#         .fillna("")
#         .reset_index(drop=True)
#         )
#     print(df) ,
#     return df

# def return_blockdev_name():
#         process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
#         return json.loads(process.stdout)

# block_device_name = return_blockdev_name()



# stdscr = curses.initscr()
# pandas_block_devices = return_pandas()

# print_curses(stdscr, block_device_name)
# print_curses(stdscr, pandas_block_devices.to_numpy)


def test_crypt():
    command = ["cryptsetup", "--help"]
    cryptsetup_process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE)
    awk_command = ["awk", "{print substr($0,3,35)}"]
    awk_process = subprocess.Popen(awk_command, text=True, stdin=cryptsetup_process.stdout, stdout=subprocess.PIPE)
    sed_one_command = ["sed", "s/,/:/"]
    sed_one_process = subprocess.Popen(sed_one_command, text=True, stdin=awk_process.stdout, stdout=subprocess.PIPE)
    sed_two_command = ["sed", "1, 4d"]
    sed_two_process = subprocess.Popen(sed_two_command, text=True, stdin=sed_one_process.stdout, stdout=subprocess.PIPE)
    head_command = ["head", "-n-80"]
    head_process = subprocess.Popen(head_command, text=True, stdin=sed_two_process.stdout, stdout=subprocess.PIPE)
    # print(cryptsetup_process.stdout)
    # print(awk_process)
    # print(sed_one_process)
    # print(sed_two_process)
    # print(head_process)
    output, error = head_process.communicate()
    print(output.split())
    variable = output.split()
    df = pd.Series(variable)
    print(df)
    pattern = r'(\D\D:+)'
    match = df.str.extract(pattern)
    print(match)
    pattern_two = r'(\S\S+)'
    match_two = df.str.extract(pattern_two)
    print(match_two)
    frames = [df.str.extract(pattern), df.str.extract(pattern_two)]
    print(pd.concat(frames, axis = 1))
#| awk '{print substr($0,3,35)}'| sed 's/,//' | sed '1, 4d' | head -n-80"
test_crypt()