import functools
from typing import Tuple, List

import PIL
from pdf2image import convert_from_path

from .renderer import get_renderer


class PDFViewer:
    def __init__(self, fname: str, render_engine: str = 'ANSI') -> None:
        self.fname = fname

        self.Renderer = get_renderer(render_engine)

    def get_image_size(self, number: int) -> Tuple[int, int]:
        return self.get_image(number).size

    @functools.lru_cache(maxsize=50)
    def get_image(self, number: int) -> PIL.Image:
        if number < 1:  # TODO: also check for max number?
            return None

        images = convert_from_path(
            self.fname, first_page=number,
            last_page=number,
            fmt='JPEG')
        assert len(images) <= 1, f'Could not find page {number}, invalid page number?'

        if len(images) == 0:
            return None

        return images[0]

    def render_page(
        self,
        target_size: Tuple[int, int],
        number: int,
        source_region: Tuple[int, int, int, int]
    ) -> List[str]:
        img = self.get_image(number)

        if img is None:
            return None

        return self.Renderer(img).render(target_size, source_region)
