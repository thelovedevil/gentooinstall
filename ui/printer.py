import curses
from .ascii_art import AsciiArt # Relative import
from .utils import truncate_to_display_width

class CursedPrinter:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0) # Hide the cursor
        self.stdscr.nodelay(False) # Wait for input in print_curses
        self.stdscr.keypad(True)

        # Initialize colors (Vermillion, Black, White)
        if curses.has_colors():
            vermillion = curses.COLOR_RED
            if curses.can_change_color():
                try:
                    curses.init_color(10, 890, 259, 204)
                    vermillion = 10
                except Exception: pass
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Normal: White on Black
            curses.init_pair(2, curses.COLOR_WHITE, vermillion) # Highlight: White on Vermillion
            curses.init_pair(3, vermillion, curses.COLOR_BLACK) # Accent: Vermillion on Black
        
        self.current_ascii_art = None
        self.ascii_start_row = 0
        self.ascii_start_col = 0
        self.text_start_row = 0

    def print_curses(self, variable, ascii_image_path="asuka_original_resized.jpg"):
        from .ascii_art import AsciiArt
        ascii_art = AsciiArt(ascii_image_path)
        x = 0
        
        # Set background
        self.stdscr.bkgd(' ', curses.color_pair(1))

        lines = str(variable).split('\n')
        max_y, max_x = self.stdscr.getmaxyx()
        
        text_cols = max_x // 2
        
        # Create a tall pad to accommodate natively wrapped text, including Japanese double-width characters
        text_pad = curses.newpad(2000, text_cols + 1)
        current_y = 0
        for line in lines:
            if current_y >= 1990: break # Prevent overflow
            stripped_line = line.strip()
            if stripped_line and all(c in '-=' for c in stripped_line):
                # Dynamically generate a neat, professional divider
                divider = " " * 4 + "═" * (text_cols - 8)
                try:
                    text_pad.addstr(current_y, 0, divider, curses.color_pair(1))
                    current_y += 1
                except curses.error: pass
            elif line == "":
                current_y += 1
            else:
                try:
                    # Let curses handle word wrap natively, which supports Japanese wide characters properly
                    text_pad.addstr(current_y, 0, line, curses.color_pair(1))
                    # Get the cursor's new Y position after wrapping
                    new_y, new_x = text_pad.getyx()
                    current_y = new_y
                    # If the cursor hasn't wrapped exactly to the start of a new line, advance Y manually
                    if new_x > 0:
                        current_y += 1
                except curses.error: 
                    current_y += 1
        
        total_text_rows = current_y
        
        while(x != ord('q')):
            self.stdscr.erase()
            
            # Draw ASCII Art on the right side
            art_width = max_x - text_cols
            art_height = max_y - 2
            ascii_art.convert_ascii(art_width, art_height)
            
            # Manual draw art logic from snippet structure
            art_lines = ascii_art.get_ascii_art_lines()
            art_start_row = getattr(ascii_art, 'start_row', 0)
            art_start_col = getattr(ascii_art, 'start_col', 0)
            
            for i in range(min(art_height, len(art_lines))):
                line_idx = i + art_start_row
                if line_idx < len(art_lines):
                    line = art_lines[line_idx]
                    visible_line = line[art_start_col : art_start_col + art_width]
                    try:
                        self.stdscr.addstr(i, text_cols, visible_line[:art_width-1], curses.color_pair(1))
                    except curses.error: pass

            # VERY IMPORTANT: Refresh stdscr FIRST so it clears the background and draws the art.
            # This marks stdscr as "clean", preventing stdscr.getch() from implicitly refreshing and overwriting the text pad.
            self.stdscr.refresh()

            # Refresh text pad on the left
            text_pad.refresh(self.text_start_row, 0, 0, 0, max_y - 2, text_cols - 1)

            x = self.stdscr.getch()

            if (x == curses.KEY_UP and self.text_start_row > 0):
                self.text_start_row -= 1
            elif (x == curses.KEY_DOWN and self.text_start_row < total_text_rows - (max_y - 2)):
                self.text_start_row += 1
        
            # Handle art scrolling (WASD)
            ascii_art.handle_input(x, art_width, art_height)
            
            # Restore state
            curses.noecho()
            curses.cbreak()
            self.stdscr.keypad(True)

    def display_text(self, text_lines, row=0, col=0, color_pair=1):
        max_y, max_x = self.stdscr.getmaxyx()
        for i, line in enumerate(text_lines):
            if row + i < max_y:
                try:
                    # Truncate to display width to avoid wrapping or multi-byte slicing issues
                    display_text = truncate_to_display_width(line, max_x - col)
                    self.stdscr.addstr(row + i, col, display_text, curses.color_pair(color_pair))
                except curses.error: pass
        self.stdscr.refresh()

    def display_ascii_art(self, ascii_art_obj, row=0, col=0, width_ratio=0.5, height_ratio=0.5):
        # Kept for compatibility with other parts
        max_y, max_x = self.stdscr.getmaxyx()
        available_height = max(1, int(max_y * height_ratio))
        available_width = max(1, int(max_x * width_ratio))
        ascii_art_obj.convert_ascii(available_width, available_height)
        art_lines = ascii_art_obj.get_ascii_art_lines()
        for i, line in enumerate(art_lines):
            if row + i < max_y:
                try:
                    self.stdscr.addstr(row + i, col, line[:available_width], curses.color_pair(1))
                except curses.error: pass
        self.stdscr.refresh()

    def handle_input(self, key):
        pass # Integrated into print_curses loop or CursesMenu

    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()
