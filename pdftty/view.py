from typing import TYPE_CHECKING, Optional, List

import urwid

from .ansi_widget import ANSIWidget

if TYPE_CHECKING:
    from .controller import Controller  # noqa: F401


class View(urwid.WidgetWrap):
    def __init__(self, controller: 'Controller') -> None:
        self.controller = controller

        self.content_view = None  # type: Optional[urwid.Widget]

        super().__init__(self.main_window)

    @property
    def main_window(self) -> urwid.Frame:
        self.content_view = ANSIWidget()

        w = urwid.Frame(self.content_view)
        return w

    def set_page_content(self, text_lines: List[str]) -> None:
        self.content_view.set_content(text_lines)
