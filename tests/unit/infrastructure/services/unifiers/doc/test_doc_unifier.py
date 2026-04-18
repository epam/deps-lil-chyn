import shutil
from uuid import uuid4

import pytest
from tests.fakes import FakeUnifierProxy, FakeObjectStorage

from deps_unified_data import UnifiedData, Cell

from deps_lil_chyn.infrastructure.services import DocUnifier


@pytest.mark.doc
def test_unifier_doc(
    doc_unifier: DocUnifier,
    doc_unified_data: tuple[str, UnifiedData, list[Cell]],
    fake_unifier_proxy: FakeUnifierProxy,
    fake_storage_service: FakeObjectStorage,
):
    document_id = uuid4().hex
    file_path, expected_unified_data, cells = doc_unified_data
    unified_data = doc_unifier.unify(document_id=document_id, files=[file_path])

    assert len(unified_data.order) == len(expected_unified_data.order)
    for unified_order, expected_order in zip(unified_data.order, expected_unified_data.order):
        assert unified_order.type_ == expected_order.type_
        assert unified_order.index == expected_order.index

    assert len(unified_data.positional_texts) == len(expected_unified_data.positional_texts)
    texts = zip(unified_data.positional_texts, expected_unified_data.positional_texts)
    for unified_positional_text, expected_positional_text in texts:
        assert len(unified_positional_text.wordboxes) == len(expected_positional_text.wordboxes)
        for unified_wordbox, expected_wordbox in zip(unified_positional_text.wordboxes, expected_positional_text.wordboxes):
            unified_content = unified_wordbox.word.content.replace('\xa0', ' ').replace('\u00a0', ' ')
            expected_content = expected_wordbox.word.content.replace('\xa0', ' ').replace('\u00a0', ' ')
            assert unified_content == expected_content
            assert unified_wordbox.word.confidence == expected_wordbox.word.confidence
            assert unified_wordbox.bbox == expected_wordbox.bbox

    assert len(unified_data.images) == len(expected_unified_data.images)
    if unified_data.images:
        images = zip(unified_data.images, expected_unified_data.images)
        for unified_image, expected_image in images:
            assert unified_image.width == expected_image.width
            assert unified_image.height == expected_image.height
            unified_image_content = fake_storage_service.download(unified_image.blob_name)
            expected_image_content = fake_storage_service.download(expected_image.blob_name)
            assert unified_image_content == expected_image_content

    assert len(cells) == len(fake_unifier_proxy._cells)
    if cells:
        for cell, expected_cell in zip(cells, fake_unifier_proxy._cells):
            assert cell.value == expected_cell.value
            assert cell.coordinates == expected_cell.coordinates


@pytest.mark.doc
def test_soffice_is_available(doc_unifier: DocUnifier):
    assert shutil.which("soffice") is not None, "soffice command must be available in PATH"
