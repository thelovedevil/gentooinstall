#!/usr/bin/env python3

import subprocess
import logging
import pandas as pd # test_dd_options returns a pandas DataFrame

from utils import test_dd_options # Import the utility function

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')


if __name__ == "__main__":
    logging.info("Starting dd options test...")
    try:
        # Call the utility function to get dd options
        dd_options_df = test_dd_options()
        
        if not dd_options_df.empty:
            print("\nSuccessfully retrieved DD options:")
            print(dd_options_df.to_string())
        else:
            print("\nNo DD options retrieved or an error occurred.")

    except Exception as e:
        logging.error(f"An error occurred while testing dd options: {e}")
        print(f"\nAn error occurred: {e}")
    
    print("\nDD options test completed.")