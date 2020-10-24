import tempfile
import subprocess
from abc import ABC, abstractmethod

from typing import Tuple, List

import numpy as np

import PIL
from colors import color


class BaseRenderer(ABC):
    def __init__(self, image: PIL.Image) -> None:
        self.image = image

    @abstractmethod
    def render(
        self,
        target_size: Tuple[int, int],
        source_region: Tuple[int, int, int, int] = None
    ) -> List[str]:
        ...


class ANSIRenderer(BaseRenderer):
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


class CACARenderer(BaseRenderer):
    def render(
        self,
        target_size: Tuple[int, int],
        source_region: Tuple[int, int, int, int] = None
    ) -> List[str]:
        tmp_image = self.image.crop(source_region)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
            fname = temp_file.name
            tmp_image.save(fname)

            width, height = target_size
            pixels_str = subprocess.check_output([
                'img2txt',
                '-f', 'utf8',
                '--width', str(width),
                '--height', str(height),
                fname
            ])

        return pixels_str.decode('utf8').split('\n')


def get_renderer(render_engine: str) -> BaseRenderer:
    if render_engine == 'ANSI':
        return ANSIRenderer
    elif render_engine == 'CACA':
        return CACARenderer
    else:
        raise RuntimeError(f'Invalid render engine: {render_engine}')
