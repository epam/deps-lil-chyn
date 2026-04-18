from uuid import uuid4

import pytest

from deps_unified_data import CellCoordinates, UnifiedDataFactory

from tests.fakes import FakeObjectStorage


def make_unified_data_1():
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    cells = []

    table_1 = unified_data.table_builder.for_page(1).with_name("Sheet1").build()

    cells.append(
        table_1.add_cell(
            content="column1",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="column2",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="1",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="A",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="2",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=2, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="B",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=2, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="3",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=3, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="C",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=3, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="4",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=4, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="D",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=4, column_span=1, row_span=1),
        )
    )

    table_2 = unified_data.table_builder.for_page(2).with_name("Sheet2").build()

    cells.append(
        table_2.add_cell(
            content="1",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=2, column_span=1, row_span=1),
        )
    )
    cells.append(
        table_2.add_cell(
            content="2",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=2, column_span=1, row_span=1),
        )
    )
    return unified_data, cells


def make_unified_data_2():
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    cells = []

    table_1 = unified_data.table_builder.for_page(1).with_name("Merge").build()

    cells.append(
        table_1.add_cell(
            content="1",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=0, column_span=2, row_span=1),
        )
    )
    cells.append(
        table_1.add_cell(
            content="6",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=0, column_span=2, row_span=13),
        )
    )
    cells.append(
        table_1.add_cell(
            content="2",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=2),
        )
    )
    cells.append(
        table_1.add_cell(
            content="3",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=3, column_span=2, row_span=2),
        )
    )
    cells.append(
        table_1.add_cell(
            content="4",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=5, column_span=2, row_span=7),
        )
    )
    cells.append(
        table_1.add_cell(
            content="5",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=13, column_span=4, row_span=2),
        )
    )
    return unified_data, cells


@pytest.fixture(
    scope="function",
    params=[
        ("tests/data/excel_file_1.xlsx", make_unified_data_1()),
        ("tests/data/excel_file_2.xlsx", make_unified_data_2()),
    ],
)
def excel_unified_data(request, fake_storage_service: FakeObjectStorage):
    file_path, (unified_data, cells) = request.param
    with open(file_path, "r+b") as f:
        fake_storage_service.upload(path=file_path, content=f.read(), replace_if_exists=True)

        yield file_path, unified_data, cells
