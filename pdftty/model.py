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

    def setup_viewer(self, fname: str, number: int) -> None:
        self.current_page_number = number
        self.pdf_viewer = PDFViewer(fname)

    def get_page_content(
        self,
        target_size: Tuple[int, int],
        number: Optional[int] = None
    ) -> List[str]:
        assert self.pdf_viewer is not None, 'Viewer not loaded'

        if number is None:
            number = self.current_page_number

        return self.pdf_viewer.render_page(target_size, number, self.page_region)
