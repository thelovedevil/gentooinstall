#! /usr/bin/env python3

import subprocess
import json
import curses
import pandas as pd
import sys
import io


def cryptsetup_help():
    process = subprocess.run("cryptsetup --help".split(), capture_output=True, text=True)
    #process_list = json.loads(process.stdout)
    print(process)
    process_list_output = process_list.decode('utf-8')
    #a = process_list_output.to_dict()
    #print(a)
    # names = ['Help', 'options', ' ']
    # df = pd.read_csv(io.StringIO(process_list_output), header = 2, names=['Help', 'options:', ' '], usecols = ['Help', 'options:', ' '], nrows=100)
    # print(df)
    # print(process_list_output.split('\n'))
    # process_list_output_split = process_list_output.split('\n')
    # json_list = json.dumps(process_list_output_split)
    # print(json_list)
    # data = json.loads(json_list)
    # df = pd.json_normalize(data)
    # print(df)

cryptsetup_help()