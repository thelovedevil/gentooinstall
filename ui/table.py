import curses
import pandas as pd
from .printer import CursedPrinter
from .utils import pad_to_display_width

class Table:
    def __init__(self, stdscr, printer: CursedPrinter, data_frame: pd.DataFrame, height: int, width: int):
        self.stdscr = stdscr
        self.printer = printer
        self.data_frame = data_frame
        self.height = height
        self.width = width
        self.start_row = 0
        self.current_selection = 0
        self.pad = curses.newpad(self.data_frame.shape[0] + 2, self.data_frame.shape[1] * 15) # +2 for header, *15 for col width approx

        self._draw_table()

    def _draw_table(self):
        self.pad.clear()
        # Draw headers - Use Accent color (Vermillion)
        for i, col_name in enumerate(self.data_frame.columns):
            try:
                # Use pad_to_display_width for alignment of Japanese characters
                text = pad_to_display_width(str(col_name), 14)
                self.pad.addstr(0, i * 15, text, curses.color_pair(3) | curses.A_BOLD)
            except curses.error: pass

        # Draw data rows
        for r_idx, row in self.data_frame.iterrows():
            for c_idx, cell_value in enumerate(row):
                # Use pad_to_display_width for alignment of Japanese characters
                text = pad_to_display_width(str(cell_value), 14)
                try:
                    if r_idx == self.current_selection:
                        # Use Highlight color (White on Vermillion)
                        self.pad.addstr(r_idx + 1, c_idx * 15, text, curses.color_pair(2))
                    else:
                        # Use Normal color (White on Black)
                        self.pad.addstr(r_idx + 1, c_idx * 15, text, curses.color_pair(1))
                except curses.error: pass
        
        # Refresh the pad to the main screen
        # Arguments: pad_begin_y, pad_begin_x, screen_begin_y, screen_begin_x, screen_end_y, screen_end_x
        self.pad.refresh(self.start_row, 0, 0, 0, self.height - 1, self.width - 1)

    def handle_input(self, key):
        if key == curses.KEY_UP:
            self.current_selection = max(0, self.current_selection - 1)
            self._adjust_scroll()
        elif key == curses.KEY_DOWN:
            self.current_selection = min(self.data_frame.shape[0] - 1, self.current_selection + 1)
            self._adjust_scroll()
        elif key == ord('q'):
            return 'quit'
        elif key == ord('\n'):
            return self.get_selected_row()

        self._draw_table() # Redraw after input

    def _adjust_scroll(self):
        # Adjust start_row for scrolling if selection goes out of view
        if self.current_selection < self.start_row:
            self.start_row = self.current_selection
        elif self.current_selection >= self.start_row + self.height - 2: # -2 for header
            self.start_row = self.current_selection - (self.height - 3) # -3 for header and 1 visible line
        self.start_row = max(0, self.start_row)
        self.start_row = min(self.start_row, self.data_frame.shape[0] - (self.height - 2)) # Ensure not to scroll past end

    def get_selected_row(self):
        if not self.data_frame.empty:
            return self.data_frame.iloc[self.current_selection]
        return None

    def display(self):
        self._draw_table()
        
    
if __name__ == "__main__":
    # Example Usage
    def test_table(stdscr):
        printer = CursedPrinter(stdscr)
        
        # Sample DataFrame
        data = {'col1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                'col2': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']}
        df = pd.DataFrame(data)

        max_y, max_x = stdscr.getmaxyx()
        
        table_height = max_y - 2 # Leave space for messages
        table_width = max_x
        
        table_widget = Table(stdscr, printer, df, table_height, table_width)
        
        printer.display_text(["Use UP/DOWN to navigate, ENTER to select, 'q' to quit."], row=max_y - 1, col=0)
        
        while True:
            table_widget.display()
            key = stdscr.getch()
            result = table_widget.handle_input(key)
            
            if result == 'quit':
                break
            elif result is not None:
                printer.display_text([f"Selected: {result.to_string()}"], row=max_y - 2, col=0)
                stdscr.getch() # Pause to show selection
                printer.display_text([" " * max_x], row=max_y - 2, col=0) # Clear message

            stdscr.refresh()

    curses.wrapper(test_table)
