from typing import Tuple, List, Optional, Any, Iterable

import urwid


class ANSICanvas(urwid.canvas.Canvas):
    def __init__(self, size: Tuple[int, int], text_lines: List[str]) -> None:
        super().__init__()

        self.maxcols, self.maxrows = size

        self.text_lines = text_lines

    def cols(self) -> int:
        return self.maxcols

    def rows(self) -> int:
        return self.maxrows

    def content(
        self,
        trim_left: int = 0, trim_top: int = 0,
        cols: Optional[int] = None, rows: Optional[int] = None,
        attr_map: Optional[Any] = None
    ) -> Iterable[List[Tuple[None, str, bytes]]]:
        assert cols is not None
        assert rows is not None

        for i in range(rows):
            if i < len(self.text_lines):
                text = self.text_lines[i].encode('utf-8')
            else:
                text = b''

            padding = bytes().rjust(max(0, cols - len(text)))
            line = [(None, 'U', text + padding)]

            yield line


class ANSIWidget(urwid.Widget):
    _sizing = frozenset([urwid.widget.BOX])

    def __init__(self, text: str = '') -> None:
        self.lines = text.split('\n')

    def set_content(self, lines: List[str]) -> None:
        self.lines = lines
        self._invalidate()

    def render(
        self,
        size: Tuple[int, int], focus: bool = False
    ) -> urwid.canvas.Canvas:
        canvas = ANSICanvas(size, self.lines)

        return canvas


if __name__ == '__main__':
    txt = '\x1b[34;47mHello World\x1b[0m'

    urwid.MainLoop(urwid.Pile([
        urwid.Filler(urwid.Text(f'TextWidget: {txt}')),
        ANSIWidget(f'ANSIWidget: {txt}'),
    ])).run()
