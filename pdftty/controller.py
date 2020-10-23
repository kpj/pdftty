import urwid

from .model import Model
from .view import View


class Controller:
    def __init__(self, fname: str) -> None:
        self.fname = fname

        self.model = Model(self)
        self.view = View(self)

        # setup communication
        urwid.register_signal(View, ['move'])
        urwid.connect_signal(self.view, 'move', self.handle_move)

        # setup remaining things
        screen = urwid.raw_display.Screen()
        self.screen_size = screen.get_cols_rows()

    def main(self, page_number: int = 1) -> None:
        self.loop = urwid.MainLoop(
            self.view, unhandled_input=self._unhandled_input)

        # load pdf
        self.model.current_page_number = page_number
        self.model.load_pdf(self.fname)
        img_lines = self.model.get_page_content(target_size=self.screen_size)
        self.view.set_page_content(img_lines)

        # start loop
        self.loop.run()

    def handle_move(self, key: str) -> None:
        if key in ('left', 'right'):
            new_number = self.model.current_page_number + (1 if key == 'right' else -1)

            img_lines = self.model.get_page_content(target_size=self.screen_size, number=new_number)

            if img_lines is not None:
                self.model.current_page_number = new_number
                self.view.set_page_content(img_lines)

    def _unhandled_input(self, key: str) -> None:
        if key in ('Q', 'q', 'esc'):
            raise urwid.ExitMainLoop()
