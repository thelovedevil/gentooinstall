import curses
import locale
import subprocess
import pandas as pd
import logging
from ui.printer import CursedPrinter
from ui.table import Table

locale.setlocale(locale.LC_ALL, '')

def test_crypt_options():
    try:
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
        df = pd.DataFrame(variable, columns=["options"])
        
        # Apply the "hacked" regular expression blocks detected in thirdtuesday
        pattern = r'(\D\D:+)'
        pattern_two = r'(\S\S+)'
        
        # We create a new dataframe with the extracted matches to be used as menu items
        match1 = df["options"].str.extract(pattern)
        match2 = df["options"].str.extract(pattern_two)
        
        # Combine them or filter them as the original logic intended
        # The original code did: frames = [df['options'].str.extract(pattern), df['options'].str.extract(pattern_two)]
        # and then returned df. But to make it useful, we'll return the extracted options.
        
        final_df = pd.concat([match1, match2], axis=1).dropna(how='all')
        if not final_df.empty:
            # Flatten or pick the best representative column
            df = pd.DataFrame(final_df.iloc[:, 0].fillna(final_df.iloc[:, 1]), columns=["options"])
            
        return df
    except Exception as e:
        logging.error(f"Error in test_crypt_options: {e}")
        return pd.DataFrame(columns=["options"])

from ui.ascii_art import AsciiArt

def crypt_options_digest(stdscr, printer: CursedPrinter, sources, ascii_image_path="Pictures/black_white002.jpeg"):
    if sources is None:
        sources = test_crypt_options()
        
    x = 0
    special_address_list = []
    
    if sources.empty:
        printer.display_text(["No crypt options found."], color_pair=2)
        stdscr.getch()
        return []

    max_y, max_x = stdscr.getmaxyx()
    table_height = max_y - 2
    table_width = max_x // 2
    
    table_widget = Table(stdscr, printer, sources, table_height, table_width)
    
    ascii_art_obj = AsciiArt(ascii_image_path)
    ascii_art_x_pos = max_x // 2 + 5

    def draw_screen():
        stdscr.clear()
        printer.display_text(["Crypt Options Table: Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=0, col=0)
        table_widget.display()
        
        printer.display_ascii_art(
            ascii_art_obj,
            row=0,
            col=ascii_art_x_pos,
            width_ratio=0.4,
            height_ratio=0.9
        )
        stdscr.refresh()

    draw_screen()
    
    while (x != ord('q')):
        x = stdscr.getch()
        table_result = table_widget.handle_input(x)

        if table_result == 'quit':
            break
        elif table_result is not None:
            selected_option = table_result['options']
            special_address_list.append(selected_option)
            printer.display_text([f"Selected: {selected_option}"], row=max_y-1, col=0)
            stdscr.getch()
        
        # Handle ASCII art scrolling
        if (x in [ord('w'), ord('a'), ord('d'), ord('s')]):
            printer.handle_input(x)
            
        draw_screen()

    return special_address_list

def main(stdscr):
    printer = CursedPrinter(stdscr)
    sources = test_crypt_options()
    crypt_options_digest(stdscr, printer, sources)

if __name__ == "__main__":
    curses.wrapper(main)

