import urwid

from .model import Model
from .view import View


class Controller:
    def __init__(self, fname: str) -> None:
        self.model = Model(self)
        self.view = View(self)

        self.fname = fname

    def main(self) -> None:
        self.loop = urwid.MainLoop(
            self.view, unhandled_input=self._unhandled_input)

        # load pdf
        screen = urwid.raw_display.Screen()
        screen_size = screen.get_cols_rows()

        self.model.load_pdf(self.fname)
        img_lines = self.model.get_page_content(screen_size)
        self.view.set_page_content(img_lines)

        # start loop
        self.loop.run()

    def _unhandled_input(self, key: str) -> None:
        if key in ('Q', 'q', 'esc'):
            raise urwid.ExitMainLoop()
