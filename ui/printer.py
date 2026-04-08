import curses
from .ascii_art import AsciiArt # Relative import

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

        import textwrap
        lines = str(variable).split('\n')
        max_y, max_x = self.stdscr.getmaxyx()
        
        text_cols = max_x // 2
        wrapped_lines = []
        for line in lines:
            wrapped_lines.extend(textwrap.wrap(line, width=text_cols - 4))

        # Pad for text
        text_pad = curses.newpad(len(wrapped_lines) + 1, text_cols)
        for i, line in enumerate(wrapped_lines):
            text_pad.addstr(i, 0, line, curses.color_pair(1))
        
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

            # Refresh text pad on the left
            text_pad.refresh(self.text_start_row, 0, 0, 0, max_y - 2, text_cols - 1)

            x = self.stdscr.getch()

            if (x == curses.KEY_UP and self.text_start_row > 0):
                self.text_start_row -= 1
            elif (x == curses.KEY_DOWN and self.text_start_row < len(wrapped_lines) - (max_y - 2)):
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
                    self.stdscr.addstr(row + i, col, line[:max_x - col], curses.color_pair(color_pair))
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
