from io import BytesIO
from typing import Dict, List

from deps_unified_data.model import Bbox, Word, WordBox
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTAnno,
    LTChar,
    LTContainer,
    LTFigure,
    LTTextBox,
    LTTextLine,
)
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from deps_lil_chyn.domain.dto import Shape

from .utils import AbsoluteCoordinates

Page = int

__all__ = ["VectorPdfExtractor"]


class VectorPdfExtractor:
    def __init__(self):
        self._resource_manager = PDFResourceManager(caching=False)
        self._device = PDFPageAggregator(
            self._resource_manager,
            laparams=LAParams(detect_vertical=True, all_texts=True),
        )
        self._interpreter = PDFPageInterpreter(self._resource_manager, self._device)

    def extract_wordboxes(self, file: BytesIO) -> Dict[Page, List[WordBox]]:
        page_to_extracted_wordboxes_mapping: Dict[Page, List[WordBox]] = {}

        pages = PDFPage.get_pages(file)

        for page_index, page in enumerate(pages):
            page_shape = Shape.from_page(page)

            self._interpreter.process_page(page)
            layout = self._device.get_result()

            page_to_extracted_wordboxes_mapping[
                page_index
            ] = self._extract_wordboxes_from_container(
                container=layout, page_shape=page_shape
            )

        return page_to_extracted_wordboxes_mapping

    def _extract_wordboxes_from_container(
        self, container: LTContainer, page_shape: Shape
    ) -> List[WordBox]:
        wordboxes = []

        for item in container:
            if isinstance(item, LTTextBox):
                for line in item:
                    wordboxes.extend(
                        self._extract_wordboxes_from_line(
                            line=line, page_shape=page_shape
                        )
                    )
            elif isinstance(item, LTFigure):
                wordboxes.extend(
                    self._extract_wordboxes_from_container(
                        container=item, page_shape=page_shape
                    )
                )

        return wordboxes

    def _extract_wordboxes_from_line(
        self, line: LTTextLine, page_shape: Shape
    ) -> List[WordBox]:
        x1 = y1 = x2 = y2 = -1  # noqa: WPS429
        chars: List[str] = []
        wordboxes = []

        for char in line:
            if self._is_end_of_word(char):
                if AbsoluteCoordinates.are_valid_coordinates(
                    x1, y1, x2, y2, page_shape
                ):
                    wordbox = self._create_wordbox(
                        content="".join(chars),
                        confidence=1.0,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        page_shape=page_shape,
                    )
                    wordboxes.append(wordbox)

                x1 = y1 = x2 = y2 = -1  # noqa: WPS429
                chars = []

            elif self._is_current_word(char):
                chars.append(char.get_text())

                if x1 == -1:
                    x1 = char.bbox[0]

                x2 = char.bbox[2]
                y1 = (
                    page_shape.height - char.bbox[3]
                    if y1 == -1
                    else min(y1, page_shape.height - char.bbox[3])
                )
                y2 = (
                    page_shape.height - char.bbox[1]
                    if y1 == -1
                    else max(y2, page_shape.height - char.bbox[1])
                )

                x1, y1, x2, y2 = AbsoluteCoordinates.clip_coordinates(
                    x1, y1, x2, y2, page_shape
                )

        if AbsoluteCoordinates.are_valid_coordinates(x1, y1, x2, y2, page_shape):
            wordbox = self._create_wordbox(
                content="".join(chars),
                confidence=1.0,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                page_shape=page_shape,
            )
            wordboxes.append(wordbox)

        return wordboxes

    @staticmethod
    def _is_end_of_word(char):
        # If the char is a line-break or an empty space, the word is complete
        return isinstance(char, LTAnno) or char.get_text() == " "

    @staticmethod
    def _is_current_word(char):
        return isinstance(char, LTChar)

    @staticmethod
    def _create_bbox(x1: int, y1: int, x2: int, y2: int, page_shape: Shape) -> Bbox:
        r_x1, r_y1, r_x2, r_y2 = AbsoluteCoordinates.convert_to_relative_coordinates(
            x1, y1, x2, y2, page_shape
        )

        return Bbox(
            x=r_x1,
            y=r_y1,
            w=r_x2 - r_x1,
            h=r_y2 - r_y1,
        )

    @classmethod
    def _create_wordbox(
        cls,
        content: str,
        confidence: float,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        page_shape: Shape,
    ) -> WordBox:
        bbox = cls._create_bbox(x1=x1, y1=y1, x2=x2, y2=y2, page_shape=page_shape)
        word = Word(content=content, confidence=confidence)

        return WordBox.with_bbox(word=word, bbox=bbox)
