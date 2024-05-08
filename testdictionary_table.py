#! /usr/bin/env python3

import curses 
import cursestable as curtable
import subprocess
import json
from cursesprint import print_curses
import itertools

def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

block_devices = return_blockdev_name()


def return_blockdev_name_two():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

hello = return_blockdev_name_two()

class BlockDevice:
    def __init__(self, block_devices):
        self.block_devices = block_devices.get("blockdevices",[])
        for device in self.block_devices:
                for key, value in block_devices.items():
                        setattr(self, key, value)

        def __iter__(self):
            for device in self.block_devices:
                for value in self.block_devices.values():
                        yield value

        def blockdeviceiter(self):
                return iter(self.block_device.values())

        
dictionary_table = BlockDevice(block_devices)

entries = range(len(dictionary_table.block_devices))
used = []
updated = []

index = 0
for index in range(len(dictionary_table.block_devices)):
    for key in dictionary_table.block_devices[index]:
        if key not in used:
            updated.append(key)
            used.append(key)
    index+=1


entree = range(len(dictionary_table.block_devices))
used = []
updated = []

windex = 0
for windex in range(len(dictionary_table.block_devices)):
    for value in dictionary_table.block_devices[windex].values():
        if value not in used:
            updated.append(value)
            used.append(value)
    #print(updated)
    windex+=1  


# for x, y in itertools.combinations(dictionary_table.block_devices, 2):
#     print(x,y)
#     test = str(print(y))
#     print_variable = list(test.split() for _ in range(len(dictionary_table.block_devices)))
#     print(print_variable)


print("///////////////////////////////////////////////////////////////////////////////////////")

for (k, v) in enumerate(dictionary_table.block_devices):
    print(k, v)

test_dictionary = curtable.dictionary_test_table(hello)

print(test_dictionary.dictionary_devices)

dictionary_test = curtable.block_test_table(block_devices)

print(dictionary_test.block_devices)
	





    