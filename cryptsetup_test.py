#!/usr/bin/env python3
from testtest import sources_testcrypt
from cryptsetup_table import crypt_options_digest
from utils import test_crypt_options
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

crypt_options = test_crypt_options()
variable_one = []
variable_two = []
variable_three = []
variable_four = []


# print_curses(stdscr, "now select a crypt option")
# variable_one = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "good, now write an option value")
# variable_two = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "now select a crypt option")

# variable_three = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "good, now write an option value")

# variable_four = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "now select a crypt option")

# variable_five = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "good, now write an option value")
# variable_six = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "now select a crypt option")
# variable_seven = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "good, now write an option value")
# variable_eight = crypt_options_digest(stdscr, crypt_options)
# print_curses(stdscr, "now select a crypt option")

def luks_process_prefab():              
    try:
        luks_process = subprocess.run(['sudo', 'cryptsetup', variable_one[0], variable_two[0], variable_three[0], variable_four[0], variable_five[0], variable_six[0], variable_seven[0], variable_eight[0], 'luksFormat', '/dev/sda'], check=True, capture_output=True, text=True)
        print("LUKS format successful.") # Using print for now, no curses context
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during LUKS format (exit code {e.returncode}): {e.stderr.strip()}")
        print(f"Error during LUKS format: {e.stderr.strip()}")
    except IndexError:
        logging.error("IndexError: Not enough variables provided for LUKS format command.")
        print("Error: Not enough variables provided for LUKS format command.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during LUKS format: {e}")
        print(f"An unexpected error occurred during LUKS format: {e}")

#luks_process_prefab()

def luks_sub_prefab():
    command = []
    # crypt_options_digest needs stdscr and printer, currently not available
    # This will likely fail without proper curses context
    # For now, assuming crypt_options_digest returns a list of strings
    # TODO: Refactor crypt_options_digest to not require stdscr/printer if used outside curses context
    # Or ensure a mock stdscr/printer is passed for testing/non-curses execution
    try:
        # Assuming crypt_options_digest can be called without stdscr/printer for getting command options
        # This is a temporary bypass and needs proper resolution
        command = crypt_options_digest(None, None, crypt_options) # Passing None for stdscr and printer temporarily
        
        process = subprocess.run(['sudo', 'cryptsetup'] + command, capture_output=True, text=True, check=True)
        print("LUKS sub-prefab process successful.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during LUKS sub-prefab process (exit code {e.returncode}): {e.stderr.strip()}")
        print(f"Error during LUKS sub-prefab process: {e.stderr.strip()}")
    except IndexError:
        logging.error("IndexError: Crypt options not properly formed for LUKS sub-prefab process.")
        print("Error: Crypt options not properly formed for LUKS sub-prefab process.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during LUKS sub-prefab process: {e}")
        print(f"An unexpected error occurred during LUKS sub-prefab process: {e}")

luks_sub_prefab()