"""A menu item that opens a submenu."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cursesmenu.items.menu_item import MenuItem

if TYPE_CHECKING:
    from typing import Any

    from cursesmenu.curses_menu import CursesMenu


class SubmenuItem(MenuItem):
    """
    A menu item that opens a submenu.

    :param text: The text of the item
    :param submenu: A CursesMenu to be displayed when the item is selected
    :param menu: The menu that this item belongs to
    :param should_exit: Whether the menu will exit when this item is selected
    """

    def __init__(
        self,
        text: str,
        submenu: CursesMenu | None = None,
        menu: CursesMenu | None = None,
        *,
        should_exit: bool = False,
        override_index: str | None = None,
    ) -> None:
        """Initialize the item."""
        self._submenu: CursesMenu | None = submenu
        self._menu: CursesMenu | None = menu
        if self._submenu:
            self._submenu.parent = menu
        super().__init__(
            text=text,
            menu=menu,
            should_exit=should_exit,
            override_index=override_index,
        )

    @property
    def submenu(self) -> CursesMenu | None:
        """Get the submenu associated with this item."""
        return self._submenu

    @submenu.setter
    def submenu(self, submenu: CursesMenu | None) -> None:
        """Set the submenu and update its parent."""
        self._submenu = submenu
        if self._submenu is not None:
            self._submenu.parent = self._menu

    @property  # type: ignore[override]
    def menu(self) -> CursesMenu | None:  # type: ignore[override]
        """Get the menu that this item belongs to."""
        return self._menu

    @menu.setter
    def menu(self, menu: CursesMenu | None) -> None:
        """Set the menu for the item and update the submenu's parent."""
        self._menu = menu
        if self._submenu is not None:
            self._submenu.parent = menu

    def set_up(self) -> None:
        """Set the screen up for the submenu."""
        assert self.menu is not None
        self.menu.pause()
        self.menu.clear_screen()

    def action(self) -> None:
        """Start the submenu."""
        assert self.submenu is not None
        self.submenu.start()

    def clean_up(self) -> None:
        """Block until the submenu is done and then return to the parent."""
        assert self.menu is not None
        assert self.submenu is not None
        self.submenu.join()
        self.submenu.clear_screen()
        self.menu.resume()

    def get_return(self) -> Any:  # noqa: ANN401
        """Get the returned value from the submenu."""
        if self.submenu is not None:
            return self.submenu.returned_value
        return None
