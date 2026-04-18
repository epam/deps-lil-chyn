import pytest
from deps_unified_data import UnifiedData, Cell

from deps_lil_chyn.infrastructure.services import ExcelUnifier
from tests.fakes import FakeUnifierProxy


@pytest.mark.excel
def test_unify_excel(excel_unifier: ExcelUnifier, excel_unified_data: tuple[str, UnifiedData, list[Cell]], fake_unifier_proxy: FakeUnifierProxy):
    file_path, unified_data, cells = excel_unified_data
    test_output = excel_unifier.unify(
        document_id=unified_data.document_id, files=[file_path]
    )

    assert len(unified_data.tables) == len(test_output.tables)

    for table, test_table in zip(unified_data.tables, test_output.tables):
        assert table.page == test_table.page
        assert table.name == test_table.name

    assert len(cells) == len(fake_unifier_proxy._cells)

    for cell, test_cell in zip(cells, fake_unifier_proxy._cells):
        assert cell.value == test_cell.value
        assert cell.coordinates == test_cell.coordinates
