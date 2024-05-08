#!/usr/bin/env python3
import curses
from curseXcel import Table
import subprocess
import json


class DictionaryDevices:
	def __init__(self, dictionary_devices):
		self.dictionary_devices = dictionary_devices.get("dictionarydevices",[])
		for device in self.dictionary_devices:
				for key, value in dictionary_devices.items():
						setattr(self, key, value)

		def __iter__(self):
			for device in self.dictionary_devices:
				for value in self.dictionary_devices.values():
						yield value

		def dictionaryiter(self):
				return iter(self.dictionary_devices.values())

def dictionary_test_table(dictionary_command_line):
	return DictionaryDevices(dictionary_command_line)

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


def block_test_table(dictionary_command_line):
	return BlockDevice(dictionary_command_line)




def return_blockdev_name():
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True)
        return json.loads(process.stdout)

block_devices = return_blockdev_name()


dict_table = dictionary_test_table(block_devices)

def main(stdscr):
	x = 0
	stdscr = curses.initscr()
	rows, cols = stdscr.getmaxyx()
	table = Table(stdscr, 4, 6, 5, 50, 10, spacing=1, col_names=True)
	m = 0
	while m < 6:
		table.set_column_header("Col " + str(m + 1), m)
		m += 1
	m = 0
	while m < 4:
		n = 0
		while n < 6:
			table.set_cell(m, n, n+m)
			n += 1
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