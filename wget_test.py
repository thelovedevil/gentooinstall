#!/usr/bin/env python3

from url_table import special_address_list
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

def test_stage3_wget():
    try:
        url = "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/" + str(special_address_list[0])
        print(f"Attempting to download: {url}") # Informative message
        subprocess.run(["wget", "-c", url], check=True)
        print("Download successful.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Wget command failed with exit code {e.returncode}: {e.stderr.strip()}")
        print(f"Error: Download failed. Check logs for details. URL: {url}")
    except FileNotFoundError:
        logging.error("Wget command not found. Please ensure wget is installed and in your PATH.")
        print("Error: Wget not found. Please install wget.")
    except IndexError:
        logging.error("special_address_list is empty. Cannot construct download URL.")
        print("Error: Download URL not available. special_address_list is empty.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred during download: {e}")


if __name__ == "__main__":
    test_stage3_wget()