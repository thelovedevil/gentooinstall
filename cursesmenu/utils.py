"""Utility functions for curses-menu."""

from __future__ import annotations

import os
import sys
import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


def null_input_factory() -> Callable[[int], None]:
    """Create a lambda that takes a single input and does nothing."""
    return lambda _: None

def get_display_width(text: str) -> int:
    """Get the display width of a string, accounting for wide characters."""
    if not isinstance(text, str):
        text = str(text)
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ('W', 'F'):
            width += 2
        else:
            width += 1
    return width

def pad_to_display_width(text: str, total_width: int, side: str = 'left') -> str:
    """Pad a string to a specific display width."""
    if not isinstance(text, str):
        text = str(text)
    current_width = get_display_width(text)
    padding = max(0, total_width - current_width)
    if side == 'left':
        return text + (' ' * padding)
    else:
        return (' ' * padding) + text

def truncate_to_display_width(text: str, max_width: int) -> str:
    """Truncate a string to a specific display width."""
    if not isinstance(text, str):
        text = str(text)
    current_width = 0
    truncated_text = ""
    for char in text:
        char_width = 2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1
        if current_width + char_width > max_width:
            break
        truncated_text += char
        current_width += char_width
    return truncated_text


def clear_terminal() -> None:
    """
    Call the platform specific function to clear the terminal.

    Cls on windows, reset otherwise.
    """
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("reset")


def soft_clear_terminal() -> None:
    """Use ANSI control sequences to clear the terminal."""
    if sys.platform.startswith("win"):  # pragma: no cover all
        # enables ANSI escape codes to work properly in bare cmd.exe
        os.system("")
    print(chr(27) + "[2J", end="")  # noqa: T201
    print(chr(27) + "[1;1H", end="")  # noqa: T201
