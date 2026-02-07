#!/usr/bin/env python3

''' objects and functions neccesary to create lvm structure '''
import subprocess
import curses
import logging
import json # For parsing lsblk output if needed elsewhere
import pandas as pd # For processing lsblk output if needed elsewhere

from ui.printer import CursedPrinter
from ui.input import Input
import moby_dick # Assuming moby_dick provides text strings
# from block_device_class_table import Block_Table, return_pandas # Block_Table might be useful for device selection

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

# Helper to run lsblk and return pandas DataFrame, similar to block_device_table
def run_lsblk_pandas():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk for pandas: {e.stderr}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output for pandas.")
        return pd.DataFrame()
    except FileNotFoundError:
        logging.error("lsblk command not found. Ensure lsblk is installed and in your PATH.")
        return pd.DataFrame()


def name_physical_volume(printer: CursedPrinter, input_handler: Input): 
    string = moby_dick.physical_volume()
    printer.display_text(string.splitlines())
    name = input_handler.input_string("LVM physical volume name: ")
    return name   

def pvcreate_process(printer: CursedPrinter, name_pv: str):
    printer.display_text([f"Creating physical volume: {name_pv}"])
    try:
        subprocess.run(['sudo', 'pvcreate', f'/dev/mapper/{name_pv}'], check=True)
        printer.display_text([f"Physical volume {name_pv} created successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating PV {name_pv}: {e.stderr.strip()}")
        printer.display_text([f"Error creating PV {name_pv}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("pvcreate command not found. Is LVM2 installed?")
        printer.display_text(["Error: pvcreate command not found. Is LVM2 installed?"], color_pair=2)


def name_volume_group(printer: CursedPrinter, input_handler: Input):
    string = moby_dick.volume_group()
    printer.display_text(string.splitlines())
    name = input_handler.input_string("LVM volume group name: ")
    return name

def vgcreate_process(printer: CursedPrinter, name_vg: str, name_pv: str):
    printer.display_text([f"Creating volume group {name_vg} on {name_pv}"])
    try:
        subprocess.run(['sudo', 'vgcreate', name_vg, f'/dev/mapper/{name_pv}'], check=True)
        printer.display_text([f"Volume group {name_vg} created successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating VG {name_vg}: {e.stderr.strip()}")
        printer.display_text([f"Error creating VG {name_vg}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("vgcreate command not found. Is LVM2 installed?")
        printer.display_text(["Error: vgcreate command not found. Is LVM2 installed?"], color_pair=2)

def proc_meminfo(printer: CursedPrinter):
    printer.display_text(["Fetching memory information..."])
    try:
        memory = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], check=True, capture_output=True, text=True).stdout
        printer.display_text(memory.strip().splitlines())
    except subprocess.CalledProcessError as e:
        logging.error(f"Error reading /proc/meminfo: {e.stderr.strip()}")
        printer.display_text([f"Error reading /proc/meminfo: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("grep command not found. Ensure it is installed.")
        printer.display_text(["Error: grep command not found."], color_pair=2)


class Lvcreate_Container():
    def __init__(self, lvcreateDictionary):
        self.size = lvcreateDictionary.get("size")
        self.name = lvcreateDictionary.get("name")
        self.extents = lvcreateDictionary.get("extents")
                

def collect_lv_info(printer: CursedPrinter, input_handler: Input, prompt_string: str) -> dict:
    printer.display_text(prompt_string.splitlines())
    lv_info = {}
    lv_info["size"] = input_handler.input_string("Enter size (e.g., 8G or 'null' if using extents): ")
    lv_info["name"] = input_handler.input_string("Enter name (e.g., swap): ")
    lv_info["extents"] = input_handler.input_string("Enter extents (e.g., 100%FREE or 'null' if using size): ")
    return lv_info


def lvcreate_swap(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str):
    printer.display_text([f"Creating logical volume '{lv_info.name}' for swap..."])
    cmd = ['sudo', 'lvcreate']
    if lv_info.size and lv_info.size != 'null':
        cmd.extend(['--size', lv_info.size])
    elif lv_info.extents and lv_info.extents != 'null':
        cmd.extend(['--extents', lv_info.extents])
    cmd.extend(['--name', lv_info.name, name_vg])
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"Logical volume '{lv_info.name}' created successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating LV '{lv_info.name}': {e.stderr.strip()}")
        printer.display_text([f"Error creating LV '{lv_info.name}': {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("lvcreate command not found. Is LVM2 installed?")
        printer.display_text(["Error: lvcreate command not found. Is LVM2 installed?"], color_pair=2)

def lvcreate_root(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str):
    printer.display_text([f"Creating logical volume '{lv_info.name}' for root..."])
    cmd = ['sudo', 'lvcreate']
    if lv_info.size and lv_info.size != 'null':
        cmd.extend(['--size', lv_info.size])
    elif lv_info.extents and lv_info.extents != 'null':
        cmd.extend(['--extents', lv_info.extents])
    cmd.extend(['--name', lv_info.name, name_vg])
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"Logical volume '{lv_info.name}' created successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating LV '{lv_info.name}': {e.stderr.strip()}")
        printer.display_text([f"Error creating LV '{lv_info.name}': {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("lvcreate command not found. Is LVM2 installed?")
        printer.display_text(["Error: lvcreate command not found. Is LVM2 installed?"], color_pair=2)

def lvcreate_home(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str):
    printer.display_text([f"Creating logical volume '{lv_info.name}' for home..."])
    cmd = ['sudo', 'lvcreate']
    if lv_info.size and lv_info.size != 'null':
        cmd.extend(['--size', lv_info.size])
    elif lv_info.extents and lv_info.extents != 'null':
        cmd.extend(['--extents', lv_info.extents])
    cmd.extend(['--name', lv_info.name, name_vg])
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"Logical volume '{lv_info.name}' created successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating LV '{lv_info.name}': {e.stderr.strip()}")
        printer.display_text([f"Error creating LV '{lv_info.name}': {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("lvcreate command not found. Is LVM2 installed?")
        printer.display_text(["Error: lvcreate command not found. Is LVM2 installed?"], color_pair=2)


def pv_display_info(printer: CursedPrinter):
    printer.display_text(["Physical Volume Information:"])
    try:
        pv_output = subprocess.run([ 'sudo', 'pvdisplay'], check=True, capture_output=True, text=True).stdout
        printer.display_text(pv_output.splitlines())
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running pvdisplay: {e.stderr.strip()}")
        printer.display_text([f"Error running pvdisplay: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("pvdisplay command not found.")
        printer.display_text(["Error: pvdisplay command not found."], color_pair=2)


def vg_display_info(printer: CursedPrinter):
    printer.display_text(["Volume Group Information:"])
    try:
        vg_output = subprocess.run(['sudo', 'vgdisplay'], check=True, capture_output=True, text=True).stdout
        printer.display_text(vg_output.splitlines())
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running vgdisplay: {e.stderr.strip()}")
        printer.display_text([f"Error running vgdisplay: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("vgdisplay command not found.")
        printer.display_text(["Error: vgdisplay command not found."], color_pair=2)


def lv_display_info(printer: CursedPrinter):
    printer.display_text(["Logical Volume Information:"])
    try:
        lv_output = subprocess.run(['sudo', 'lvdisplay'], check=True, capture_output=True, text=True).stdout
        printer.display_text(lv_output.splitlines())
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lvdisplay: {e.stderr.strip()}")
        printer.display_text([f"Error running lvdisplay: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("lvdisplay command not found.")
        printer.display_text(["Error: lvdisplay command not found."], color_pair=2)


def vg_change(printer: CursedPrinter):
    printer.display_text(["Activating volume groups..."])
    try:
        subprocess.run(['vgchange', '--available', 'y'], check=True)
        printer.display_text(["Volume groups activated successfully."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error activating volume groups: {e.stderr.strip()}")
        printer.display_text([f"Error activating volume groups: {e.stderr.strip()}"], color_pair=2)


def ls_devmapper(printer: CursedPrinter):
    printer.display_text(["Listing /dev/mapper..."])
    try:
        ls_output = subprocess.run(['ls', '/dev/mapper'], check=True, capture_output=True, text=True).stdout
        printer.display_text(ls_output.splitlines())
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing /dev/mapper: {e.stderr.strip()}")
        printer.display_text([f"Error listing /dev/mapper: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("ls command not found.")
        printer.display_text(["Error: ls command not found."], color_pair=2)


def mk_swap(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str):
    printer.display_text([f"Creating swap filesystem for {lv_info.name}..."])
    cmd = ["mkswap", "-L", lv_info.name, f"/dev/mapper/{name_vg}-{lv_info.name}"]
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"Swap filesystem for {lv_info.name} created."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating swap for {lv_info.name}: {e.stderr.strip()}")
        printer.display_text([f"Error creating swap for {lv_info.name}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("mkswap command not found.")
        printer.display_text(["Error: mkswap command not found."], color_pair=2)


def mk_ext4(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str, label: str = None, m_option: str = None):
    printer.display_text([f"Creating ext4 filesystem for {lv_info.name}..."])
    cmd = ["mkfs.ext4"]
    if label:
        cmd.extend(["-L", label])
    if m_option:
        cmd.extend(["-m", m_option])
    cmd.extend([f"/dev/mapper/{name_vg}-{lv_info.name}"])
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"ext4 filesystem for {lv_info.name} created."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating ext4 for {lv_info.name}: {e.stderr.strip()}")
        printer.display_text([f"Error creating ext4 for {lv_info.name}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("mkfs.ext4 command not found.")
        printer.display_text(["Error: mkfs.ext4 command not found."], color_pair=2)


def mk_swap_on(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str):
    printer.display_text([f"Activating swap for {lv_info.name}..."])
    cmd = ["swapon", "-v", f"/dev/mapper/{name_vg}-{lv_info.name}"]
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"Swap for {lv_info.name} activated."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error activating swap for {lv_info.name}: {e.stderr.strip()}")
        printer.display_text([f"Error activating swap for {lv_info.name}: {e.stderr.strip()}"], color_pair=2)
    except FileNotFoundError:
        logging.error("swapon command not found.")
        printer.display_text(["Error: swapon command not found."], color_pair=2)


def mkdir_mnt_gentoo(printer: CursedPrinter):
    printer.display_text(["Creating /mnt/gentoo..."])
    try:
        subprocess.run(["sudo", "mkdir", "-v", "/mnt/gentoo/"], check=True)
        printer.display_text(["/mnt/gentoo created."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating /mnt/gentoo: {e.stderr.strip()}")
        printer.display_text([f"Error creating /mnt/gentoo: {e.stderr.strip()}"], color_pair=2)


def mount_mnt_gentoo(printer: CursedPrinter, lv_info: Lvcreate_Container, name_vg: str):
    printer.display_text([f"Mounting {lv_info.name} to /mnt/gentoo..."])
    cmd = ["sudo", "mount", "-v", "-t", "ext4", f"/dev/mapper/{name_vg}-{lv_info.name}", "/mnt/gentoo"]
    try:
        subprocess.run(cmd, check=True)
        printer.display_text([f"{lv_info.name} mounted to /mnt/gentoo."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error mounting {lv_info.name} to /mnt/gentoo: {e.stderr.strip()}")
        printer.display_text([f"Error mounting {lv_info.name} to /mnt/gentoo: {e.stderr.strip()}"], color_pair=2)


def mkdir_home_boot_efi(printer: CursedPrinter):
    printer.display_text(["Creating /mnt/gentoo/{home,boot,boot/efi}..."])
    try:
        subprocess.run(["sudo", "mkdir", "-v", "/mnt/gentoo/{home,boot,boot/efi}"], check=True, shell=True) # shell=True for brace expansion
        printer.display_text(["/mnt/gentoo/{home,boot,boot/efi} created."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating /mnt/gentoo subdirs: {e.stderr.strip()}")
        printer.display_text([f"Error creating /mnt/gentoo subdirs: {e.stderr.strip()}"], color_pair=2)


def umount_efiboot(printer: CursedPrinter):
    printer.display_text(["Unmounting /tmp/efiboot..."])
    try:
        subprocess.run(["sudo", "umount", "-v", "/tmp/efiboot"], check=True)
        printer.display_text(["/tmp/efiboot unmounted."])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error unmounting /tmp/efiboot: {e.stderr.strip()}")
        printer.display_text([f"Error unmounting /tmp/efiboot: {e.stderr.strip()}"], color_pair=2)


# Main entry point for the curses application
def main_curses(stdscr):
    printer = CursedPrinter(stdscr)
    input_handler = Input(printer)

    printer.display_text([moby_dick.welcome_message()]) # Assuming moby_dick provides a welcome message
    printer.display_text(["Starting LVM setup..."])

    # 1. Name Physical Volume
    name_pv = name_physical_volume(printer, input_handler)
    if not name_pv:
        printer.display_text(["Physical Volume name cannot be empty. Exiting."], color_pair=2)
        stdscr.getch()
        return

    # 2. Create Physical Volume
    pvcreate_process(printer, name_pv)

    # 3. Name Volume Group
    name_vg = name_volume_group(printer, input_handler)
    if not name_vg:
        printer.display_text(["Volume Group name cannot be empty. Exiting."], color_pair=2)
        stdscr.getch()
        return

    # 4. Create Volume Group
    vgcreate_process(printer, name_vg, name_pv)

    # 5. Proc meminfo
    proc_meminfo(printer)

    # 6. Collect LV info for swap, root, home
    swap_lv_info_dict = collect_lv_info(printer, input_handler, moby_dick.lvm_instructions())
    lvcreate_swap_dictionary = Lvcreate_Container(swap_lv_info_dict)

    root_lv_info_dict = collect_lv_info(printer, input_handler, moby_dick.sec_lvm_instructions())
    lvcreate_root_dictionary = Lvcreate_Container(root_lv_info_dict)

    home_lv_info_dict = collect_lv_info(printer, input_handler, moby_dick.third_lvm_instructions())
    lvcreate_home_dictionary = Lvcreate_Container(home_lv_info_dict)

    # 7. Create Logical Volumes
    lvcreate_swap(printer, lvcreate_swap_dictionary, name_vg)
    lvcreate_root(printer, lvcreate_root_dictionary, name_vg)
    lvcreate_home(printer, lvcreate_home_dictionary, name_vg)

    # 8. Display LVM info
    pv_display_info(printer)
    vg_display_info(printer)
    lv_display_info(printer)

    # 9. Activate Volume Groups
    vg_change(printer)

    # 10. List /dev/mapper
    ls_devmapper(printer)

    # 11. Create Filesystems
    mk_swap(printer, lvcreate_swap_dictionary, name_vg)
    mk_ext4(printer, lvcreate_root_dictionary, name_vg, label=lvcreate_root_dictionary.name)
    mk_ext4(printer, lvcreate_home_dictionary, name_vg, label="home", m_option="0")

    # 12. Activate Swap
    mk_swap_on(printer, lvcreate_swap_dictionary, name_vg)

    # 13. Mount filesystems
    mkdir_mnt_gentoo(printer)
    mount_mnt_gentoo(printer, lvcreate_root_dictionary, name_vg)
    mkdir_home_boot_efi(printer)
    # Placeholder for mounting home, boot, efi - needs specific device info
    # For now, just mkdir

    umount_efiboot(printer) # This was hardcoded to /tmp/efiboot, review usage

    printer.display_text(["LVM setup completed. Press any key to exit."])
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main_curses)