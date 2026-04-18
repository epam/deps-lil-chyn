import logging
from io import BytesIO
from typing import Any, Generator

from deps_object_storage import ObjectStorage
from deps_unified_data import Cell, CellCoordinates, Table
from deps_unified_data.model import UnifiedData, UnifiedDataFactory
from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import Cell as ExcelCell
from openpyxl.cell.cell import MergedCell
from openpyxl.worksheet.merge import MergedCellRange
from openpyxl.worksheet.worksheet import Worksheet
from xls2xlsx import XLS2XLSX

from deps_lil_chyn.infrastructure.services import UnifierProxy

from .abstract_unifier import AbstractUnifier

logger = logging.getLogger(__name__)

TARGET_DPI = 300

Confidence = float
Content = str
MergedCellRanges = dict[tuple[int, int], MergedCellRange]

__all__ = ["ExcelUnifier"]


class ExcelUnifier(AbstractUnifier):
    extensions: set[str] = {
        "xlsx",
        "xls",
    }

    def __init__(
        self,
        object_storage: ObjectStorage,
        unifier_proxy: UnifierProxy,
        *,
        cell_chunk_size: int = 5,
    ):
        super().__init__(object_storage=object_storage)

        self._unifier_proxy = unifier_proxy
        self._cell_chunk_size = cell_chunk_size

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)

        for file_path in files:
            self._unify_book(unified_data, file_path)

        return unified_data

    def _unify_book(self, unified_data: UnifiedData, file_path: str):
        for worksheet in self._produce_worksheets(self._get_workbook(file_path)):
            table = (
                unified_data.table_builder.for_page(worksheet.page)
                .with_name(worksheet.title)
                .build()
            )

            for cells in self._make_cells(table, self._produce_cells(worksheet)):
                self._unifier_proxy.save_cells(cells)

    def _get_workbook(self, file_path: str) -> Workbook:
        file_object = self._download_file_from_storage(file_path)
        with BytesIO(file_object.content) as file:
            if file_object.extension.lower() != ".xls":
                return load_workbook(file, data_only=True)

            with BytesIO() as target_obj:
                XLS2XLSX(file).to_xlsx(target_obj)
                return load_workbook(target_obj, data_only=True)

    def _produce_worksheets(
        self, workbook: Workbook
    ) -> Generator["ExcelUnifier._Worksheet", None, None]:
        for page, worksheet in enumerate(workbook, start=1):
            yield self._Worksheet(worksheet, page)

    def _produce_cells(
        self, worksheet: "ExcelUnifier._Worksheet"
    ) -> Generator["ExcelUnifier._Cell", None, None]:
        for row in worksheet.rows:
            for cell in row:
                unifier_cell = self._Cell(cell, worksheet.merged_cells_ranges)

                if unifier_cell.should_not_be_unified:
                    continue

                yield unifier_cell

    def _make_cells(
        self, table: Table, cells_producer: Generator["ExcelUnifier._Cell", None, None]
    ) -> Generator[list[Cell], None, None]:
        cells: list[Cell] = []

        for cell in cells_producer:
            if self._is_chunk_ready(cells):
                yield cells
                cells.clear()

            cells.append(table.add_cell(**cell.as_dict()))

        if cells:
            yield cells

    def _is_chunk_ready(self, cells: list[Cell]) -> bool:
        return len(cells) == self._cell_chunk_size

    class _Worksheet:
        def __init__(self, worksheet: Worksheet, page: int) -> None:
            self.worksheet = worksheet
            self.page = page

        @property
        def title(self) -> str:
            return self.worksheet.title

        @property
        def rows(self) -> Generator[tuple[ExcelCell, ...], None, None]:
            return self.worksheet.rows

        @property
        def merged_cells_ranges(self) -> MergedCellRange:
            return {
                (cell_range.min_col, cell_range.min_row): cell_range
                for cell_range in self.worksheet.merged_cells.ranges
            }

    class _Cell:
        DEFAULT_CONFIDENCE: float = 1.0

        def __init__(
            self,
            excel_cell: ExcelCell,
            merged_cells_ranges: dict[tuple[int, int], MergedCellRange],
        ) -> None:
            self._excel_cell = excel_cell
            self._merged_cells_ranges = merged_cells_ranges

        @property
        def should_not_be_unified(self) -> bool:
            return (
                isinstance(self._excel_cell, MergedCell)
                or self._excel_cell.value is None
            )

        @property
        def content(self) -> str:
            return str(self._excel_cell.value)

        @property
        def confidence(self) -> float:
            return self.DEFAULT_CONFIDENCE

        @property
        def coordinates(self) -> CellCoordinates:
            if merged_cell := self._merged_cells_ranges.get(
                (self._excel_cell.column, self._excel_cell.row)
            ):
                column_span = merged_cell.size["columns"]
                row_span = merged_cell.size["rows"]
            else:
                column_span = 1
                row_span = 1

            return CellCoordinates(
                column=self._excel_cell.column - 1,
                row=self._excel_cell.row - 1,
                column_span=column_span,
                row_span=row_span,
            )

        def as_dict(self) -> dict[str, Any]:
            return {
                "content": self.content,
                "confidence": self.confidence,
                "coordinates": self.coordinates,
            }
