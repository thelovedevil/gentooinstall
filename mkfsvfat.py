#!/usr/bin/env python3

from cursedprint import CursedPrint
import subprocess
from block_device_class_table import Block_Table
import json
import pandas as pd

block_dev = Block_Table()

print_app = CursedPrint()
print_app.start()

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
    return df

pandas_block_devices = return_pandas()

format_block_device = block_dev.block_digest(pandas_block_devices)

def mkfs_vfat():
        subprocess.run(['sudo', 'mkfs.vfat', '-F32', format_block_device[0]])
        print_app.print_curses("successfully formatted devie -F32")

mkfs_vfat()