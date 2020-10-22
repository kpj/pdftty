from typing import TYPE_CHECKING, Optional, Tuple, List

from .pdf_handling import PDFViewer

if TYPE_CHECKING:
    from .controller import Controller  # noqa: F401


class Model:
    def __init__(self, controller: 'Controller') -> None:
        self.controller = controller

        self.viewer = None

        self.current_page_number = 1

    def load_pdf(self, fname: str) -> None:
        self.viewer = PDFViewer(fname)

    def get_page_content(
        self,
        size: Tuple[int, int], number: Optional[int] = None
    ) -> List[str]:
        assert self.viewer is not None, 'Viewer not loaded'

        number = number or self.current_page_number
        page = self.viewer.get_page(number)
        return page.render(size)
