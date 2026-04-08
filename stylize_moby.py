import re

with open("moby_dick.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_instruction_block = False

# A very stylized line to replace the top dash or bottom dash
# Let's standardize the dashes to exactly 50 characters to prevent awkward wrapping on standard terminals.
dash_line = "    " + "="*50 + "\n"

for line in lines:
    if "【" in line and "】" in line:
        # It's an instruction line
        content = line[line.find("【")+1 : line.rfind("】")].strip()
        # Add some cyber angel / english / german / japanese flair randomly or systematically
        if "following few functions" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.SYS_INIT ⍚ // ]\n")
            new_lines.append("    [ ACHTUNG: MANUELLE EINGABE ERFORDERLICH ]\n")
            new_lines.append(f"    [ SYS.MSG ]: {content}\n")
        elif "number of entries" in content and "on the next page" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.DATA_ENTRY ⍚ // ]\n")
            new_lines.append("    [ EINGABE: NUMBER OF ENTRIES ]\n")
            new_lines.append("    [ 指示 ]: ONLY ONE ENTRY MAY BE SELECTED FOR NOW\n")
        elif "now enter key value pair" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.KEY_VAL_MAP ⍚ // ]\n")
            new_lines.append("    [ SCHLÜSSEL-WERT-PAAR EINGEBEN ]\n")
            new_lines.append("    [ 指示 ]: ENTER KEY VALUE PAIR FOLLOWED BY <: ENTER >\n")
        elif "here is the value selected" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.SELECTION_OK ⍚ // ]\n")
            new_lines.append("    [ AUSWAHL BESTÄTIGT ]\n")
            new_lines.append("    [ 状態 ]: HERE IS THE VALUE SELECTED FOR\n")
        elif "block options process" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.BLOCK_DEVICE_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: FILLING IN BLOCK OPTIONS PROCESS ]\n")
            new_lines.append("    [ 指示 ]: PLEASE ENTER THE NUMBER OF ENTRIES N\n")
        elif "crypt options process" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.CRYPTSETUP_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: FILLING IN CRYPT OPTIONS PROCESS ]\n")
            new_lines.append("    [ VERSCHLÜSSELUNG ]: SECURE PAYLOAD PREPARATION\n")
        elif "overwrite options" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.DD_OVERWRITE_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: FILLING IN OVERWRITE OPTIONS PROCESS ]\n")
            new_lines.append("    [ DATENVERNICHTUNG ]: WIPE DISK SECURELY\n")
        elif "dd options process" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.DD_OPTIONS_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: FILLING IN DD OPTIONS PROCESS ]\n")
            new_lines.append("    [ DATENTRANSFER ]: CONFIGURE DD PARAMETERS\n")
        elif "gpg options process" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.GPG_OPTIONS_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: FILLING IN GPG OPTIONS PROCESS ]\n")
            new_lines.append("    [ KRYPTOGRAPHIE ]: ASYMMETRIC / SYMMETRIC ENCRYPTION\n")
        elif "key file input from prior" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.KEYFILE_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: ENTERING KEY FILE INPUT FROM PRIOR CRYPTSETUP ]\n")
            new_lines.append("    [ SCHLÜSSEL ]: SIMPLY ENTER THE SAME VALUE AS USED FOR PRIOR KEY FILE\n")
        elif "name for a logical volume management" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.LVM_PV_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: ENTER NAME FOR LOGICAL VOLUME MANAGEMENT (LVM) PHYSICAL VOLUME ]\n")
            new_lines.append("    [ PHYSISCHES VOLUMEN ]: <: PRESS ENTER >\n")
        elif "name for the volume group" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.LVM_VG_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: ENTER NAME FOR THE VOLUME GROUP WITHIN THE PHYSICAL VOLUME ]\n")
            new_lines.append("    [ VOLUMENGRUPPE ]: <: PRESS ENTER >\n")
        elif "size and name" in content and "swap" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.LVM_SWAP_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: ENTER VALUES FOR SIZE AND NAME OF SWAP PARTITION ]\n")
            new_lines.append("    [ FORMAT ]: SUFFIX WITH M OR G (e.g. 10G) <: PRESS ENTER >\n")
            new_lines.append("    [ EXTENTS ]: MAY BE LEFT NULL OR SKIPPED\n")
            new_lines.append("    [ 状態 ]: HAJIME (BEGIN)\n")
        elif "root portion" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.LVM_ROOT_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: CONFIGURE ROOT PORTION OF THE VOLUME GROUP ]\n")
            new_lines.append("    [ FORMAT ]: SIZE SUFFIXED WITH M OR G, THEN NAME, THEN EXTENTS\n")
            new_lines.append("    [ 状態 ]: HAJIME (BEGIN)\n")
        elif "home directory" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.LVM_HOME_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: CONFIGURE HOME DIRECTORY USING EXTENTS OPTION ]\n")
            new_lines.append("    [ FORMAT ]: EXTENTS SHOULD BE 'NUM'%FREE (e.g. 95%FREE)\n")
            new_lines.append("    [ 状態 ]: HAJIME (BEGIN)\n")
        elif "fdisk process about to be run" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.FDISK_MGR ⍚ // ]\n")
            new_lines.append("    [ SYSTEM: FDISK PROCESS ABOUT TO RUN ON SELECTED BLOCK DEVICE ]\n")
            new_lines.append("    [ ACHTUNG ]: PLEASE SELECT EXACTLY ONE BLOCK DEVICE\n")
        elif "now enter options" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.OPTION_SELECT ⍚ // ]\n")
            new_lines.append("    [ EINGABE ]: NOW ENTER OPTIONS BY SCROLLING AND SELECTING\n")
            new_lines.append("    [ 指示 ]: SELECT VIA USING ENTER. PRESS 'q' TO FINISH.\n")
        elif "enter the value for that option" in content:
            new_lines.append("    [ // ⍚ CYBER_ANGEL_OS.VALUE_SELECT ⍚ // ]\n")
            new_lines.append("    [ EINGABE ]: ENTER THE VALUE FOR THAT OPTION\n")
            new_lines.append("    [ 指示 ]: SELECT WITH ENTER.\n")
        else:
            new_lines.append(f"    [ SYS.MSG ]: {content}\n")
    elif re.match(r'^\s*-{10,}\s*$', line):
        # Replace dashed lines with standard 75 char width stylized line
        new_lines.append(dash_line)
    else:
        new_lines.append(line)

with open("moby_dick.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
