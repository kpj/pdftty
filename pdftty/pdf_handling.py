from typing import Tuple, List

import PIL
from pdf2image import convert_from_path

from .renderer import Renderer


class PDFPage:
    def __init__(self, fname: str, number: int) -> None:
        self.fname = fname
        self.number = number

        self._img = None  # type: PIL.Image

    @property
    def image(self) -> PIL.Image:
        if self._img is not None:
            return self._img

        images = convert_from_path(
            self.fname, first_page=self.number,
            last_page=self.number,
            fmt='JPEG')
        assert len(images) == 1

        self._img = images[0]
        return self._img

    def display(self) -> None:
        self.image.show()

    def render(self, size: Tuple[int, int]) -> List[str]:
        rend = Renderer(self.image)
        return rend.render(size)


class PDFViewer:
    def __init__(self, fname: str) -> None:
        self.fname = fname

    def get_page(self, number: int) -> PDFPage:
        return PDFPage(self.fname, number)