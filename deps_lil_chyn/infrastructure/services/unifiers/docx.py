import contextlib
import logging
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Callable, Optional, Union

import PIL
from deps_object_storage import ObjectStorage
from deps_unified_data import UnifiedData, UnifiedDataFactory
from deps_unified_data.model import Cell, CellCoordinates, Table
from docx import Document as DocxDocument
from docx import ImagePart
from docx.image.exceptions import UnexpectedEndOfFileError, UnrecognizedImageError
from docx.oxml.table import CT_Tbl as DocxTableElement
from docx.oxml.table import CT_Tc as DocxCellElement
from docx.oxml.text.paragraph import CT_P as DocxParagraphElement  # noqa
from docx.oxml.xmlchemy import BaseOxmlElement as BaseDocxElement
from docx.shape import InlineShape as DocxInlineShape
from docx.table import Table as DocxTable
from docx.table import _Cell as DocxCell  # noqa
from docx.text.paragraph import Paragraph as DocxParagraph
from docx.text.run import Run as DocxRun
from PIL import Image as PILImage

from deps_lil_chyn.domain.dto import FileData, ImageData
from deps_lil_chyn.infrastructure.services import UnifierProxy

from .abstract_unifier import AbstractUnifier

__all__ = ["DocxUnifier"]

DEFAULT_PAGE = 1
DEFAULT_CONFIDENCE = 1.0

DocxParsableBlockType = Union[DocxTable, DocxParagraph]

logger = logging.getLogger(__name__)


class _DocxElementUnifier(ABC):
    _docx_cls: DocxParsableBlockType

    def __init__(
        self,
        docx_el: BaseDocxElement,
        docx_obj: DocxDocument,
        doc_name: str,
        parent_unifier: "DocxUnifier",
    ):
        self._docx_obj = docx_obj
        self._docx_elm = self._docx_cls(docx_el, docx_obj)
        self._doc_name = doc_name
        self._parent_unifier = parent_unifier

    @abstractmethod
    def unify(self, unified_data: UnifiedData) -> None:
        pass


class _DocxParagraphUnifier(_DocxElementUnifier):
    _docx_cls = DocxParagraph

    class _Paragraph:
        def __init__(self):
            self._texts = list()

        def add(self, text: str) -> None:
            self._texts.append(text)

        def unify(self, unified_data: UnifiedData) -> None:
            if not self._texts:
                return

            words = [
                (word, DEFAULT_CONFIDENCE)
                for word in "".join(text for text in self._texts).split(" ")
                if word
            ]

            if not words:
                self._texts.clear()
                return

            unified_data.positonal_text_builder.for_page(DEFAULT_PAGE).with_words(
                words
            ).build()

            self._texts.clear()

    def unify(self, unified_data: UnifiedData) -> None:
        paragraph = self._Paragraph()
        for run in self._docx_elm.runs:
            if run.text:
                paragraph.add(run.text)
            if inlines := self._get_inlines(run):
                paragraph.unify(unified_data)
                self._unify_images(unified_data, inlines)

        paragraph.unify(unified_data)

    @staticmethod
    def _get_inlines(run: DocxRun) -> list[DocxInlineShape]:
        return [
            DocxInlineShape(inline) for inline in run._r.xpath("w:drawing/wp:inline")
        ]  # noqa

    def _unify_images(
        self, unified_data: UnifiedData, inlines: list[DocxInlineShape]
    ) -> None:
        for inline in inlines:
            self._unify_image(unified_data, inline)

    def _unify_image(
        self, unified_data: UnifiedData, docx_inline_shape: DocxInlineShape
    ) -> None:
        related_id: str = (
            docx_inline_shape._inline.graphic.graphicData.pic.blipFill.blip.embed  # noqa
        )

        if (
            image_data := self._form_image_data_from_inline_shape(
                related_id, docx_inline_shape
            )
        ) is None:
            return

        blob_name = self._parent_unifier._upload_file_to_storage(  # noqa
            FileData(
                path=self._parent_unifier._get_original_image_path(  # noqa
                    self._doc_name, f"{related_id}.png"
                ),
                content=image_data.content,
            )
        )

        (
            unified_data.image_builder.for_page(DEFAULT_PAGE)
            .with_blob(blob_name)
            .with_shape(width=image_data.width, height=image_data.height)
            .build()
        )

    def _form_image_data_from_inline_shape(
        self,
        related_id: str,
        docx_inline_shape: DocxInlineShape,
    ) -> Optional[ImageData]:
        image_part: ImagePart = self._docx_elm.part.related_parts[related_id]

        image_detectors: list[Callable[[ImagePart, DocxInlineShape], ImageData]] = [
            self._image_from_docx,
            self._image_from_pil,
        ]

        for detector in image_detectors:
            with contextlib.suppress(
                UnrecognizedImageError,
                UnexpectedEndOfFileError,
                PIL.UnidentifiedImageError,
                OSError,
            ):
                return detector(image_part, docx_inline_shape)

        logger.warning(
            "Cannot recognize image format for `%s`... Skipping this image...",
            image_part.filename,
        )

        return None

    def _image_from_docx(
        self, img_part: ImagePart, docx_inline_shape: DocxInlineShape
    ) -> ImageData:
        return ImageData.from_docx_image(img_part.image, docx_inline_shape)

    def _image_from_pil(self, img_part: ImagePart, _: DocxInlineShape) -> ImageData:
        with BytesIO(img_part.blob) as image_stream:
            with PILImage.open(image_stream) as image:
                return ImageData.from_pil_image(image)


class _DocxTableUnifier(_DocxElementUnifier):
    _docx_cls = DocxTable

    def unify(self, unified_data: UnifiedData) -> None:
        table = unified_data.table_builder.for_page(DEFAULT_PAGE).build()

        cells = self._unify_cells(
            table, (cell for row in self._docx_elm.rows for cell in row.cells)
        )
        self._parent_unifier._unifier_proxy.save_cells(cells)  # noqa

    def _unify_cells(self, table: Table, cells) -> list[Cell]:
        merged_cells: set[DocxCellElement] = set()
        unified_cells = []

        for cell in cells:
            if self._is_cell_merged(cell, merged_cells):
                continue

            cell_element = cell._tc  # noqa
            merged_cells.add(cell_element)

            unified_cell = table.add_cell(
                content=cell.text,
                confidence=DEFAULT_CONFIDENCE,
                coordinates=CellCoordinates(
                    column=cell_element.left,
                    row=cell_element.top,
                    column_span=cell_element.right - cell_element.left,
                    row_span=cell_element.bottom - cell_element.top,
                ),
            )
            unified_cells.append(unified_cell)

        return unified_cells

    @staticmethod
    def _is_cell_merged(cell: DocxCell, merged_cells: set[DocxCellElement]) -> bool:
        _cell_element = cell._tc  # noqa
        return (
            _cell_element.vMerge or _cell_element.grid_span != 1
        ) and _cell_element in merged_cells


class DocxUnifier(AbstractUnifier):
    extensions: set[str] = {
        "docx",
    }

    def __init__(
        self,
        object_storage: ObjectStorage,
        unifier_proxy: UnifierProxy,
    ):
        self._unifier_proxy = unifier_proxy

        super().__init__(object_storage=object_storage)

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)

        for file_path in files:
            self._unify_file(unified_data, file_path)

        return unified_data

    def _unify_file(self, unified_data: UnifiedData, file_path: str) -> None:
        file_object = self._download_file_from_storage(file_path)

        with BytesIO(file_object.content) as file:
            docx_obj = DocxDocument(file)

        parent_element = docx_obj.element.body
        for element in parent_element.iterchildren():
            if isinstance(element, DocxParagraphElement):
                _DocxParagraphUnifier(element, docx_obj, file_object.name, self).unify(
                    unified_data
                )
            elif isinstance(element, DocxTableElement):
                _DocxTableUnifier(element, docx_obj, file_object.name, self).unify(
                    unified_data
                )
            else:
                logger.debug(
                    "Got unknown block type: %s, cannot parse, will be skipped.",
                    type(element),
                )
