#!/usr/bin/env python3

import subprocess
import json
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

# Removed redundant global subprocess.run call

def run_lsblk():
    try:
        process = subprocess.run("lsblk --json -o NAME,SIZE,UUID,MOUNTPOINT,PATH,FSTYPE ".split(), capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running lsblk: {e.stderr}")
        return {"blockdevices": []}
    except json.JSONDecodeError:
        logging.error("Error decoding lsblk JSON output.")
        return {"blockdevices": []}
    except FileNotFoundError:
        logging.error("lsblk command not found. Please ensure lsblk is installed and in your PATH.")
        return {"blockdevices": []}

def return_blockdev_name():
    return run_lsblk()

def return_pandas():
    data = run_lsblk()
    if not data or not data.get("blockdevices"):
        return pd.DataFrame() # Return empty DataFrame if no data
    
    df = pd.json_normalize(data=data.get("blockdevices")).explode(column="children")
    df = (pd 
        .concat(objs=[df, df.children.apply(func=pd.Series)], axis=1)
        .drop(columns=[0, "children"])
        .fillna("")
        .reset_index(drop=True)
        )
    # Removed print(df)
    return df  

block_devices = return_blockdev_name()
testpandas = return_blockdev_name() # Potentially redundant, keeping for now if used elsewhere
json_pandas = return_pandas()

# new_table = pd.json_normalize(testpandas['blockdevices'], meta=['name', 'size', 'uuid', 'mountpoint', 'path', 'fstype', ['children', 'name', 'size', 'uuid', 'mountpoint', 'path', 'fstype']])
# The above line is commented out as new_table is used in the old debugging prints which are removed
# Also, testpandas['blockdevices'] might be empty, leading to errors.

def return_blockdev_name_two(): # Redundant, use return_blockdev_name()
    return run_lsblk()

dictionary_dev = return_blockdev_name_two()


# Removed nested function as it was unused.
# Removed many debugging prints.

def test():
    data = run_lsblk()
    print("Test output for lsblk data:")
    print(json.dumps(data, indent=2))

test()

ctest_variable = return_pandas()
print("ctest_variable (pandas DataFrame to numpy array):")
print(ctest_variable.to_numpy())

# Removed the variables m, n, a, b, numpy_table, haha(), something as they were only used for debugging prints.
# The code seems to be an experimental script, so keeping minimal output.
