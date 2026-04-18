from dataclasses import dataclass

from pdfminer.pdfpage import PDFPage

__all__ = ["Shape"]


@dataclass
class Shape:
    width: int
    height: int

    @classmethod
    def from_page(cls, page: PDFPage) -> "Shape":
        if page.rotate in {90, 270}:
            height = int(page.cropbox[2] - page.cropbox[0])
            width = int(page.cropbox[3] - page.cropbox[1])
        else:
            width = int(page.cropbox[2] - page.cropbox[0])
            height = int(page.cropbox[3] - page.cropbox[1])

        return cls(height=height, width=width)
