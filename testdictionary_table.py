#! /usr/bin/env python3

import curses 
import cursestable as curtable
import subprocess
import json
from cursesprint import print_curses
import itertools

process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)

def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

block_devices = return_blockdev_name()


def return_blockdev_name_two():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

dictionary_dev = return_blockdev_name_two()

print("/////////////////FIIIIIIIIIIIIIIIIIIIIIIIIIRRRRRRRRRRRRRRRSTTTTTTTTTTTT?????????????????")

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

class DictionaryDevice:
    def __init__(self, dictionary_devices):
        self.dictionary_devices = dictionary_devices.get("dictionary_devices",[])
        for device in self.dictionary_devices:
                for key, value in dictionary_devices.items():
                        setattr(self, key, value)

        def __iter__(self):
            for device in self.dictionary_devices:
                for value in self.dictionary_devices.values():
                        yield value
            
        def dictionarydeviceiter(self):
            return iter(self.dictionary_device.values())

       

        
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


for x, y in itertools.combinations(dictionary_table.block_devices, 2):
    print(x,y)
    test = str(print(y))
    print_variable = list(test.split() for _ in range(len(dictionary_table.block_devices)))
    print(print_variable)


print("///////////////////////////////////////////////////////////////////////////////////////")

# for (k, v) in enumerate(dictionary_table.block_devices):
#     print(k, v)

variable_dictionary = curtable.dictionary_test_table(dictionary_dev)
print(variable_dictionary.dictionary_devices)


print("//////////////////////////////////////////////////////////////////////////////////////")

dict_table = curtable.dictionary_test_table(block_devices)
print(dict_table.dictionary_devices)

for (k, v) in enumerate(dict_table.dictionary_devices):
     print(k, v)
     print(range(len(dict_table.dictionary_devices)))
 
m = 0
i = 1

print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYYYYYYYYYYYYY")
while (m < len(dict_table.dictionary_devices)):
    for key in dict_table.dictionary_devices[m]:
        print(dict_table.dictionary_devices[m][key])
    m += 1
print("THEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERRRRRE")
print(dict_table.dictionary_devices)

a = 0
b = 0
print("TEST 8:14 TRYING TO FIGURE OUT DIFFERENCE BETWEN [m] and [m]values OUTPUT AGAIN")
m = 0
print(dict_table.dictionary_devices[a].values())
print(dict_table.dictionary_devices[m].values())
print(dict_table.dictionary_devices[m])
print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYYYYYYYYYYYYY")

for n in dict_table.dictionary_devices[m].values():
    print(n)

print(len(dict_table.dictionary_devices[m].values()))
m = 0
for key in dict_table.dictionary_devices:
    print(key['name'])
    m += 1
    def index():
        index = 0
        list = []
        while index < len(dict_table.dictionary_devices):
            index += 1
            list.append(len(dict_table.dictionary_devices[index]))
            list.sort
            for x in list:
                if max(list) == len(dict_table.dictionary_devices[index].values()):
                    maximum_of_list = max(list)
                    return maximum_of_list
index = index()
print(index)

for key in dict_table.dictionary_devices[0].values():
    print(key)

print("////////////////////////////////////////////////////////////")
m = 0
print(dict_table.dictionary_devices[m])
key = dict_table.dictionary_devices[m]
print(key)

print("////////////////////////////////////////////////////////////")

print(dictionary_dev)



print("/////////////////////////////////////////////////////////////////////")

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]

for x in dict_generator(dictionary_dev):
    print (x)

print("/////////////////////////////////////////////////////////////////////")
#for key, value in block_devices['blockdevices']
while index < len(block_devices['blockdevices']):
    for key in block_devices['blockdevices'][index]:
        print(block_devices['blockdevices'][index][key])
print("?????????????????????????????????????????????????????????????????????")
print("?????????????????????????????????????????????????????????????????????")