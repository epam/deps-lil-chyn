from uuid import uuid4

import pytest
from deps_unified_data import UnifiedDataFactory, CellCoordinates
from tests.fakes import FakeObjectStorage


def make_unified_data_1():
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    cells = []

    table = unified_data.table_builder.for_page(1).build()

    cells.append(
        table.add_cell(
            content="oh",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="hi",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="mark",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="1",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="2",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="3",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="4",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=2, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="5",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=2, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="6",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=2, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="7",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=3, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="8",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=3, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="9",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=3, column_span=1, row_span=1),
        )
    )

    return unified_data, cells


def make_unified_data_2():
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    cells = []

    table = unified_data.table_builder.for_page(1).with_name("Merge").build()

    cells.append(
        table.add_cell(
            content="a",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="b",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="c",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="d",
            confidence=1.0,
            coordinates=CellCoordinates(column=3, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="e",
            confidence=1.0,
            coordinates=CellCoordinates(column=4, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="f",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="g",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="h",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="i",
            confidence=1.0,
            coordinates=CellCoordinates(column=3, row=1, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="j",
            confidence=1.0,
            coordinates=CellCoordinates(column=4, row=1, column_span=1, row_span=1),
        )
    )

    return unified_data, cells


def make_unified_data_3():
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    cells = []

    table = unified_data.table_builder.for_page(1).with_name("Merge").build()

    cells.append(
        table.add_cell(
            content="伊凡生下一个女孩被命令拖尿布",
            confidence=1.0,
            coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="院子里草地上的柴火",
            confidence=1.0,
            coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="这个词不是麻雀：它会飞出去——你不会抓住它",
            confidence=1.0,
            coordinates=CellCoordinates(column=2, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="没有俄语，您将无法战胜最危险的敌人",
            confidence=1.0,
            coordinates=CellCoordinates(column=3, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="不要给任何人找麻烦，否则你自己将来可能会失去支持",
            confidence=1.0,
            coordinates=CellCoordinates(column=4, row=0, column_span=1, row_span=1),
        )
    )
    cells.append(
        table.add_cell(
            content="如果什么都不做，事情就不会向前发展",
            confidence=1.0,
            coordinates=CellCoordinates(column=5, row=0, column_span=1, row_span=1),
        )
    )

    for column in range(6, 36):
        cells.append(
            table.add_cell(
                content="一粒塵埃升起，整個大地都在其中；一朵花開，整個世界就顯露出來",
                confidence=1.0,
                coordinates=CellCoordinates(column=column, row=0, column_span=1, row_span=1),
            )
        )

    return unified_data, cells


def make_unified_data_4():
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    cells = []

    table = unified_data.table_builder.for_page(1).with_name("Merge").build()

    for column in range(8):
        cells.append(
            table.add_cell(
                content="一粒塵埃升起，整個大地都在其中；一朵花開，整個世界就顯露出來",
                confidence=1.0,
                coordinates=CellCoordinates(column=column, row=0, column_span=1, row_span=1),
            )
        )

    for column in range(8, 10):
        cells.append(
            table.add_cell(
                content=(
                    "一粒塵埃升起，整個大地都在其中；一朵花開，整個世界就顯露出來一粒塵埃升起，"
                    "整個大地都在其中；一朵花開，整個世界就顯露出來"
                ),
                confidence=1.0,
                coordinates=CellCoordinates(column=column, row=0, column_span=1, row_span=1),
            )
        )

    for column in range(10):
        cells.append(
            table.add_cell(
                content="a",
                confidence=1.0,
                coordinates=CellCoordinates(column=column, row=1, column_span=1, row_span=1),
            )
        )

    return unified_data, cells


@pytest.fixture(
    scope="function",
    params=[
        ("tests/data/csv/csv_file_1.csv", make_unified_data_1()),
        ("tests/data/csv/csv_file_2.csv", make_unified_data_2()),
        ("tests/data/csv/csv_file_3.csv", make_unified_data_3()),
        ("tests/data/csv/csv_file_4.csv", make_unified_data_4()),
    ],
)
def csv_unified_data(request, fake_storage_service: FakeObjectStorage):
    file_path, (unified_data, cells) = request.param
    with open(file_path, "r+b") as f:
        fake_storage_service.upload(path=file_path, content=f.read(), replace_if_exists=True)

        yield file_path, unified_data, cells
