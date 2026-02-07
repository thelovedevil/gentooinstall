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
            if ch == ord('
'):
                break
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    self.printer.display_text([prompt + input_str + " "], row=self.screen.getmaxyx()[0] // 2, col=0)
            else:
                input_str += chr(ch)
                self.printer.display_text([prompt + input_str], row=self.screen.getmaxyx()[0] // 2, col=0)
            self.screen.refresh()
        
        curses.noecho() # Disable echoing after input
        return input_str

if __name__ == "__main__":
    # Example usage (for testing ui/input.py directly)
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