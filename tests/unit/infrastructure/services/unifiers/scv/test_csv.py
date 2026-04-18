import pytest
from deps_unified_data import Table, Cell
from deps_unified_data.model import UnifiedData

from deps_lil_chyn.infrastructure.services import CsvUnifier

FIRST_ELEMENT = 0


@pytest.mark.csv
def test_unify_csv(csv_unifier: CsvUnifier, fake_unifier_proxy, csv_unified_data: tuple[str, UnifiedData, list[Cell]]):
    file_path, unified_data, cells = csv_unified_data

    test_output = csv_unifier.unify(document_id=unified_data.document_id, files=[file_path])

    assert len(test_output.tables) == 1
    assert isinstance(test_output, UnifiedData)
    assert isinstance(test_output.tables[FIRST_ELEMENT], Table)

    for table, test_table in zip(unified_data.tables, test_output.tables):
        assert table.page == test_table.page

    assert len(cells) == len(fake_unifier_proxy._cells)

    for cell, test_cell in zip(cells, fake_unifier_proxy._cells):
        assert cell.value == test_cell.value
        assert cell.coordinates == test_cell.coordinates
