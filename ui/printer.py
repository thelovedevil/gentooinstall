import curses
from .ascii_art import AsciiArt # Relative import

class CursedPrinter:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0) # Hide the cursor
        self.stdscr.nodelay(True) # Make getch non-blocking

        # Initialize default color pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Default text
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Error/highlight
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Info

        self.current_ascii_art = None
        self.ascii_start_row = 0
        self.ascii_start_col = 0
        self.display_text_lines = []
        self.text_start_row = 0
        self.text_start_col = 0

    def display_text(self, text_lines, row=0, col=0, color_pair=1):
        """Displays text lines on the screen."""
        self.display_text_lines = text_lines
        self.text_start_row = row
        self.text_start_col = col
        self._draw_text(row, col, color_pair)

    def _draw_text(self, row, col, color_pair):
        """Internal method to draw the current text lines."""
        max_y, max_x = self.stdscr.getmaxyx()
        for i, line in enumerate(self.display_text_lines):
            if row + i < max_y:
                self.stdscr.addstr(row + i, col, line[:max_x - col], curses.color_pair(color_pair))

    def display_ascii_art(self, ascii_art_obj: AsciiArt, row=0, col=0, width_ratio=0.5, height_ratio=0.5):
        """
        Displays ASCII art on a portion of the screen.
        width_ratio and height_ratio determine the size of the ASCII art relative to the terminal.
        """
        self.current_ascii_art = ascii_art_obj
        self.ascii_start_row = row
        self.ascii_start_col = col

        max_y, max_x = self.stdscr.getmaxyx()
        
        # Calculate available space for ASCII art
        available_height = int(max_y * height_ratio)
        available_width = int(max_x * width_ratio)

        # Regenerate ASCII art with new dimensions
        self.current_ascii_art.convert_ascii(available_width, available_height)
        
        self._draw_ascii_art()

    def _draw_ascii_art(self):
        """Internal method to draw the current ASCII art."""
        if not self.current_ascii_art or not self.current_ascii_art.art_matrix.size > 0:
            return

        max_y, max_x = self.stdscr.getmaxyx()
        art_lines = self.current_ascii_art.get_ascii_art_lines()

        art_display_height = len(art_lines)
        art_display_width = len(art_lines[0]) if art_lines else 0

        # Create a new pad for the ASCII art to allow scrolling
        # Pad size should be the full size of the ASCII art
        pad = curses.newpad(art_display_height + 1, art_display_width + 1)
        
        for r_idx, line in enumerate(art_lines):
            pad.addstr(r_idx, 0, line)

        # Calculate the visible window for the pad
        # This will be the area where the ASCII art is drawn on the stdscr
        # We need to consider self.ascii_start_row/col as the top-left corner on stdscr
        # And the size of the pad display area on stdscr
        display_height = min(art_display_height - self.ascii_start_row, max_y - self.ascii_start_row)
        display_width = min(art_display_width - self.ascii_start_col, max_x - self.ascii_start_col)

        if display_height > 0 and display_width > 0:
            pad.refresh(
                self.ascii_start_row, # Pad's row to start copying from
                self.ascii_start_col, # Pad's col to start copying from
                self.ascii_start_row, # Screen's row to paste to
                self.ascii_start_col, # Screen's col to paste to
                self.ascii_start_row + display_height - 1, # Screen's bottom-right row
                self.ascii_start_col + display_width - 1 # Screen's bottom-right col
            )

    def handle_input(self, key):
        """Handles scrolling input for ASCII art."""
        if not self.current_ascii_art:
            return

        art = self.current_ascii_art
        art_height, art_width = art.art_height, art.art_width
        max_y, max_x = self.stdscr.getmaxyx()

        # Define bounds for scrolling based on actual displayed area and terminal size
        # This needs to be carefully adjusted based on how the art is positioned and scaled.
        # For simplicity, let's assume it takes up the full screen for scrolling purposes for now.
        # This logic will need refinement when integrating with the menu.
        
        # Example scrolling logic (simplified)
        if key == curses.KEY_UP or key == ord('k'):
            if art.start_row > 0:
                art.start_row -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            # Prevent scrolling past the bottom of the art
            if art.start_row < art_height - 1: # (max_y - self.ascii_start_row) might be needed here
                art.start_row += 1
        elif key == curses.KEY_LEFT or key == ord('h'):
            if art.start_col > 0:
                art.start_col -= 1
        elif key == curses.KEY_RIGHT or key == ord('l'):
            # Prevent scrolling past the right edge of the art
            if art.start_col < art_width - 1: # (max_x - self.ascii_start_col) might be needed here
                art.start_col += 1

        self._draw_ascii_art() # Redraw after scroll
        self.stdscr.refresh() # Refresh the screen

    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()
