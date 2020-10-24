import os
from typing import Optional

import urwid

from .model import Model
from .view import View


class Controller:
    def __init__(self) -> None:
        self.model = Model(self)
        self.view = View(self)

        # setup communication
        urwid.register_signal(View, ['move', 'zoom'])
        urwid.connect_signal(self.view, 'move', self.handle_move)
        urwid.connect_signal(self.view, 'zoom', self.handle_zoom)

        # setup remaining things
        screen = urwid.raw_display.Screen()
        self.screen_size = screen.get_cols_rows()

    def main(
        self,
        fname: str, page_number: int = 1,
        render_engine: str = 'ANSI'
    ) -> None:
        self.loop = urwid.MainLoop(
            self.view, unhandled_input=self._unhandled_input)

        # setup PDF viewer
        self.model.setup_viewer(fname, page_number, render_engine)
        self.view.set_title(os.path.basename(fname))
        self.view.set_title_pagecount(page_number)

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
                self.view.set_title_pagecount(number)

                self.model.page_region = None  # reset cropping

    def handle_move(self, key: str) -> None:
        if self.model.page_region is None:
            # change pages
            if key in ('left', 'right'):
                if self.model.page_region is not None:
                    # can only change page if zoomed out
                    return

                step = 1 if key == 'right' else -1
                new_number = self.model.current_page_number + step

                self.display_page(new_number)
        else:
            # move page crop around
            step_size = 100  # TODO: make this dependend on page size
            move_coords = {
                'up': (0, -step_size),
                'down': (0, step_size),
                'left': (-step_size, 0),
                'right': (step_size, 0)
            }.get(key, None)

            if move_coords is not None:
                self.model.move_page_region(*move_coords)
                self.display_page()

    def handle_zoom(self, key: str) -> None:
        if key == '=':
            self.model.page_region = None
        else:
            scale = 1.2 if key == '-' else 0.8
            self.model.zoom_page_region(scale)

        self.display_page()

    def _unhandled_input(self, key: str) -> None:
        if key in ('Q', 'q', 'esc'):
            raise urwid.ExitMainLoop()
