import curses
from .printer import CursedPrinter

class Input:
    def __init__(self, printer: CursedPrinter):
        self.printer = printer
        self.screen = printer.stdscr # Use the stdscr from the printer
        curses.echo() # Enable echoing of characters for input

    def input_string(self, prompt: str = "entry: "):
        # The printer handles displaying text
        self.printer.display_text([prompt], row=self.screen.getmaxyx()[0] // 2, col=0)
        
        input_str = ""
        while True:
            ch = self.screen.getch()
            if ch == curses.ERR:
                continue
            if ch == ord('\n'):
                break
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    self.printer.display_text([prompt + input_str + " "], row=self.screen.getmaxyx()[0] // 2, col=0)
            elif 0 <= ch < 256:
                input_str += chr(ch)
                self.printer.display_text([prompt + input_str], row=self.screen.getmaxyx()[0] // 2, col=0)
            elif ch == curses.KEY_RESIZE:
                # Handle resize if needed, or just ignore to prevent chr() error
                pass
            self.screen.refresh()
        
        curses.noecho() # Disable echoing after input
        return input_str

class CursesTextScrollWithInput:
    def __init__(self, printer: CursedPrinter):
        self.printer = printer
        self.screen = printer.stdscr

    def display_and_get_dict(self, text_content: str, ascii_image_path="asuka_original_resized.jpg"):
        # First, display the instructions with scrolling using the printer's base logic
        # The user needs to press 'q' to finish reading instructions and move to input
        self.printer.print_curses(text_content, ascii_image_path=ascii_image_path)
        
        # Now collect the dictionary
        max_y, max_x = self.screen.getmaxyx()
        self.screen.erase()
        self.screen.addstr(max_y // 2, 2, "Enter number of entries (n): ")
        self.screen.refresh()
        
        n_str = self.input_string_internal("Enter number of entries (n): ")
        if n_str.isdigit():
            return self.input_dict_manual(int(n_str))
        return {n_str: n_str} if n_str else {}

    def input_dict_manual(self, n):
        dictionary = {}
        max_y, max_x = self.screen.getmaxyx()
        for i in range(n):
            key_prompt = f"Entry {i+1}/{n} - Key (e.g. partition name): "
            self.screen.erase()
            self.screen.addstr(max_y // 2, 2, key_prompt)
            self.screen.refresh()
            key = self.input_string_internal(key_prompt)
            
            val_prompt = f"Entry {i+1}/{n} - Value (e.g. mount point): "
            self.screen.erase()
            self.screen.addstr(max_y // 2, 2, val_prompt)
            self.screen.refresh()
            val = self.input_string_internal(val_prompt)
            
            dictionary[key] = val
        return dictionary

    def input_string_internal(self, prompt):
        import curses
        input_str = ""
        max_y, max_x = self.screen.getmaxyx()
        while True:
            ch = self.screen.getch()
            if ch == curses.ERR: continue
            if ch == ord('\n'):
                return input_str
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                input_str = input_str[:-1]
            elif 0 <= ch < 256:
                input_str += chr(ch)
            
            self.screen.erase()
            self.screen.addstr(max_y // 2, 2, prompt + input_str)
            self.screen.refresh()
    def test_input(stdscr):
        printer = CursedPrinter(stdscr)
        input_handler = Input(printer)
        
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter your name: ")
        name = input_handler.input_string("Name: ")
        stdscr.addstr(2, 0, f"Hello, {name}!")
        stdscr.addstr(3, 0, "Press any key to exit.")
        stdscr.getch()

    curses.wrapper(test_input)