"""Utility functions for curses-menu."""
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import subprocess
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer # Include for now


if TYPE_CHECKING:
    from typing import Callable


def null_input_factory() -> Callable[[int], None]:
    """Create a lambda that takes a single input and does nothing."""
    return lambda _: None


def clear_terminal() -> None:
    """
    Call the platform specific function to clear the terminal.

    Cls on windows, reset otherwise.
    """
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("reset")


def soft_clear_terminal() -> None:
    """Use ANSI control sequences to clear the terminal."""
    if sys.platform.startswith("win"):  # pragma: no cover all
        # enables ANSI escape codes to work properly in bare cmd.exe
        os.system("")
    print(chr(27) + "[2J", end="")  # noqa: T201
    print(chr(27) + "[1;1H", end="")  # noqa: T201

def return_pandas():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        data = json.loads(process.stdout)
        if not data or not data.get("blockdevices"):
            return pd.DataFrame()
        
        devices = data.get("blockdevices")
        df = pd.json_normalize(devices)
        
        if "children" in df.columns:
            # If there are children, we can try to explode them
            df_exploded = df.explode(column="children")
            # Only proceed with concat if children exist and are not all NaN
            if not df_exploded["children"].isna().all():
                children_series = df_exploded.children.apply(func=lambda x: pd.Series(x) if isinstance(x, dict) else pd.Series(dtype=float))
                df = pd.concat(objs=[df_exploded.drop(columns=["children"]), children_series], axis=1)
            else:
                df = df_exploded.drop(columns=["children"])
        
        df = df.fillna("").reset_index(drop=True)
        return df
    except Exception as e:
        import logging
        logging.error(f"Error in return_pandas: {e}")
        return pd.DataFrame()

def test_crypt_options():
    command = ["cryptsetup", "--help"]
    cryptsetup_process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE)
    awk_command = ["awk", "{print substr($0,3,30)}"]
    awk_process = subprocess.Popen(awk_command, text=True, stdin=cryptsetup_process.stdout, stdout=subprocess.PIPE)
    sed_one_command = ["sed", "s/,/:/"]
    sed_one_process = subprocess.Popen(sed_one_command, text=True, stdin=awk_process.stdout, stdout=subprocess.PIPE)
    sed_two_command = ["sed", "1, 4d"]
    sed_two_process = subprocess.Popen(sed_two_command, text=True, stdin=sed_one_process.stdout, stdout=subprocess.PIPE)
    head_command = ["head", "-n-54"]
    head_process = subprocess.Popen(head_command, text=True, stdin=sed_two_process.stdout, stdout=subprocess.PIPE)
    sed_three_command = ["sed", "-e", "s/-[?a-zA-Z]: / /g"]
    sed_three_process = subprocess.Popen(sed_three_command, text=True, stdin=head_process.stdout, stdout=subprocess.PIPE)
    sed_four_command = ["sed", "-e", "s/=[a-zA-Z]*/ /g"]
    sed_four_process = subprocess.Popen(sed_four_command, text=True, stdin=sed_three_process.stdout, stdout=subprocess.PIPE)
    output, error = sed_four_process.communicate()
    variable = output.split()
    df = pd.DataFrame(variable)
    pattern = r'(\D\D:+)'
    df.columns = ["options"]
    match = df["options"].str.extract(pattern)
    pattern_two = r'(\S\S+)'
    match_two = df['options'].str.extract(pattern_two)
    frames = [df['options'].str.extract(pattern), df['options'].str.extract(pattern_two)]
    return df

def test_gpg_options():
    command = ["gpg", "--help"]
    gpg_process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE)
    awk_command = ["awk", "{print substr($0,0,30)}"]
    awk_process = subprocess.Popen(awk_command, text=True, stdin=gpg_process.stdout, stdout=subprocess.PIPE)
    sed_one_command = ["sed", "s/,/:/"]
    sed_one_process = subprocess.Popen(sed_one_command, text=True, stdin=awk_process.stdout, stdout=subprocess.PIPE)
    sed_two_command = ["sed", "1, 21d"]
    sed_two_process = subprocess.Popen(sed_two_command, text=True, stdin=sed_one_process.stdout, stdout=subprocess.PIPE)
    head_command = ["head", "-n-54"]
    head_process = subprocess.Popen(head_command, text=True, stdin=sed_two_process.stdout, stdout=subprocess.PIPE)
    sed_three_command = ["sed", "-e", "s/-[?a-zA-Z]: / /g"]
    sed_three_process = subprocess.Popen(sed_three_command, text=True, stdin=head_process.stdout, stdout=subprocess.PIPE)
    sed_four_command = ["sed", "-e", "s/=[a-zA-Z]*/ /g"]
    sed_four_process = subprocess.Popen(sed_four_command, text=True, stdin=sed_three_process.stdout, stdout=subprocess.PIPE)
    output, error = sed_four_process.communicate()
    variable = output.split()
    df = pd.DataFrame(variable)
    df.columns = ['options']
    return df

def test_dd_options():
    command = ["dd", "--help"]
    dd_process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE)
    awk_command = ["awk", "{print substr($0,3,15)}"]
    awk_process = subprocess.Popen(awk_command, text=True, stdin=dd_process.stdout, stdout=subprocess.PIPE)
    sed_one_command = ["sed", "1, 4d"]
    sed_one_process = subprocess.Popen(sed_one_command, text=True, stdin=awk_process.stdout, stdout=subprocess.PIPE)
    sed_two_command = ["head", "-n-51"]
    sed_two_process = subprocess.Popen(sed_two_command, text=True, stdin=sed_one_process.stdout, stdout=subprocess.PIPE)
    head_command = ["sed", "-e", "s/=[a-zA-Z]*/ /g"]
    head_process = subprocess.Popen(head_command, text=True, stdin=sed_two_process.stdout, stdout=subprocess.PIPE)
    output, error = head_process.communicate()
    variable = output.split()
    df = pd.DataFrame(variable)
    df.columns = ['options']
    return df
