from typing import Optional

import urwid

from .model import Model
from .view import View


class Controller:
    def __init__(self) -> None:
        self.model = Model(self)
        self.view = View(self)

        # setup communication
        urwid.register_signal(View, ['move'])
        urwid.connect_signal(self.view, 'move', self.handle_move)

        # setup remaining things
        screen = urwid.raw_display.Screen()
        self.screen_size = screen.get_cols_rows()

    def main(self, fname: str, page_number: int = 1) -> None:
        self.loop = urwid.MainLoop(
            self.view, unhandled_input=self._unhandled_input)

        # setup PDF viewer
        self.model.setup_viewer(fname, page_number)

        # display initial page
        self.display_page()

        # start loop
        self.loop.run()

    def display_page(self, number: Optional[int] = None) -> None:
        """Update page content and current page number, if possible."""
        img_lines = self.model.get_page_content(
            target_size=self.screen_size, number=number)

        if img_lines is not None:
            self.view.set_page_content(img_lines)

            if number is not None:
                self.model.current_page_number = number

    def handle_move(self, key: str) -> None:
        if key in ('left', 'right'):
            step = 1 if key == 'right' else -1
            new_number = self.model.current_page_number + step

            self.display_page(new_number)

    def _unhandled_input(self, key: str) -> None:
        if key in ('Q', 'q', 'esc'):
            raise urwid.ExitMainLoop()
