from uuid import uuid4

import pytest
from tests.fakes import FakeUnifierProxy, FakeObjectStorage

from deps_unified_data import UnifiedData, Cell

from deps_lil_chyn.infrastructure.services import DocxUnifier


@pytest.mark.docx
def test_unifier_docx(
    docx_unifier: DocxUnifier,
    docx_unified_data: tuple[str, UnifiedData, list[Cell]],
    fake_unifier_proxy: FakeUnifierProxy,
    fake_storage_service: FakeObjectStorage,
):
    document_id = uuid4().hex
    file_path, expected_unified_data, cells = docx_unified_data
    unified_data = docx_unifier.unify(document_id=document_id, files=[file_path])

    assert unified_data.order == expected_unified_data.order

    texts = zip(unified_data.positional_texts, expected_unified_data.positional_texts)
    for unified_positional_text, expected_positional_text in texts:
        assert unified_positional_text.wordboxes == expected_positional_text.wordboxes

    images = zip(unified_data.images, expected_unified_data.images)
    for unified_image, expected_image in images:
        assert unified_image.width == expected_image.width
        assert unified_image.height == expected_image.height
        unified_image_content = fake_storage_service.download(unified_image.blob_name)
        expected_image_content = fake_storage_service.download(expected_image.blob_name)
        assert unified_image_content == expected_image_content

    assert len(cells) == len(fake_unifier_proxy._cells)

    for cell, expected_cell in zip(cells, fake_unifier_proxy._cells):
        assert cell.value == expected_cell.value
        assert cell.coordinates == expected_cell.coordinates
