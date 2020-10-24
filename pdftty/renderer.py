from typing import Tuple, List

import numpy as np

import PIL
from colors import color


class Renderer:
    def __init__(self, image: PIL.Image) -> None:
        self.image = image

    def tuple2ansi(self, rgb: Tuple[int, int, int]) -> str:
        return color(' ', bg=f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})')

    def render(
        self,
        target_size: Tuple[int, int],
        source_region: Tuple[int, int, int, int] = None
    ) -> List[str]:
        # rescale image
        img_tmp = self.image.resize(target_size, box=source_region)
        pixels = np.asarray(img_tmp)

        # compute colors
        pixels_str = np.apply_along_axis(self.tuple2ansi, 2, pixels)
        return [''.join(row) for row in pixels_str]
