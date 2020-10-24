from typing import TYPE_CHECKING, Optional, Tuple, List

from .pdf_handling import PDFViewer

if TYPE_CHECKING:
    from .controller import Controller  # noqa: F401


class Model:
    def __init__(self, controller: 'Controller') -> None:
        self.controller = controller

        self.pdf_viewer = None  # type: Optional[PDFViewer]

        self.page_region = None  # type: Optional[Tuple[int, int, int, int]]
        self.current_page_number = None  # type: Optional[int]

    def setup_viewer(self, fname: str, number: int, render_engine: str) -> None:
        self.current_page_number = number
        self.pdf_viewer = PDFViewer(fname, render_engine)

    def zoom_page_region(self, scale: float) -> None:
        if self.page_region is None:
            self.page_region = (
                0, 0,
                *self.pdf_viewer.get_image_size(self.current_page_number)
            )

        x, y, width, height = self.page_region

        # do scaling
        width *= scale
        height *= scale

        # check if we are out-of-bounds
        if width - x < 1 or height - y < 1:
            # TODO: who cares about floating number issues?
            width /= scale
            height /= scale

        orig_width, orig_height = self.pdf_viewer.get_image_size(self.current_page_number)
        if width > orig_width:
            width = orig_width
        if height > orig_height:
            height = orig_height

        # set new region
        if (width, height) == (orig_width, orig_height):
            # TODO: this is a bad way of checking this
            self.page_region = None
        else:
            self.page_region = (x, y, width, height)

    def move_page_region(self, dx: int, dy: int) -> None:
        if self.page_region is None:
            return

        # move region
        x, y, width, height = self.page_region
        x += dx
        y += dy
        width += dx
        height += dy

        # check bounds
        orig_width, orig_height = self.pdf_viewer.get_image_size(self.current_page_number)
        if x < 0 or y < 0 or width > orig_width or height > orig_height:
            return

        # update region
        self.page_region = (x, y, width, height)

    def get_page_content(
        self,
        target_size: Tuple[int, int],
        number: Optional[int] = None
    ) -> List[str]:
        assert self.pdf_viewer is not None, 'Viewer not loaded'

        if number is None:
            number = self.current_page_number

        return self.pdf_viewer.render_page(target_size, number, self.page_region)
