from io import StringIO
from typing import Generator

import chardet
from deps_object_storage import ObjectStorage
from deps_unified_data import (
    Cell,
    CellCoordinates,
    Table,
    UnifiedData,
    UnifiedDataFactory,
)

from ...proxies import UnifierProxy
from ..abstract_unifier import AbstractUnifier
from .csv_reader import CsvReader

__all__ = ["CsvUnifier"]


class CsvUnifier(AbstractUnifier):
    extensions: set[str] = {"csv"}
    DEFAULT_PAGE = 1
    DEFAULT_CONFIDENCE = 1.0
    DEFAULT_ROW_SPAN = 1
    DEFAULT_COLUMN_SPAN = 1

    def __init__(
        self,
        object_storage: ObjectStorage,
        unifier_proxy: UnifierProxy,
        *,
        cell_chunk_size: int = 5,
    ) -> None:
        super().__init__(object_storage=object_storage)

        self._unifier_proxy = unifier_proxy
        self._cell_chunk_size = cell_chunk_size

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)
        for file_path in files:
            self._make_table(unified_data, file_path)

        return unified_data

    def _make_table(self, unified_data: UnifiedData, file_path: str) -> None:
        file_object = self._download_file_from_storage(file_path)
        encoding = chardet.detect(file_object.content)["encoding"]
        with StringIO(
            file_object.content.decode(encoding=encoding, errors="ignore")
        ) as file:
            table = unified_data.table_builder.for_page(self.DEFAULT_PAGE).build()

            for cells in self._make_cells(table, CsvReader(file)):
                self._unifier_proxy.save_cells(cells)

    def _make_cells(
        self, table: Table, reader: CsvReader
    ) -> Generator[list[Cell], None, None]:
        cells: list[Cell] = []

        for row_index, row in enumerate(reader.rows):
            for column_index, cell in enumerate(row):
                if self._is_chunk_ready(cells):
                    yield cells
                    cells.clear()

                cells.append(
                    table.add_cell(
                        coordinates=CellCoordinates(
                            column=column_index,
                            row=row_index,
                            column_span=self.DEFAULT_COLUMN_SPAN,
                            row_span=self.DEFAULT_ROW_SPAN,
                        ),
                        content=cell,
                        confidence=self.DEFAULT_CONFIDENCE,
                    ),
                )

        if cells:
            yield cells

    def _is_chunk_ready(self, cells: list[Cell]) -> bool:
        return len(cells) == self._cell_chunk_size
