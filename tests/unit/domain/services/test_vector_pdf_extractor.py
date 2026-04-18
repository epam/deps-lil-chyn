from io import BytesIO

import pytest
from deps_unified_data.model import WordBox, Word, Bbox


@pytest.mark.parametrize(
    "file, expected_wordboxes",
    [
        (
            "tests/data/vector_2.pdf",
            [
                WordBox.with_bbox(
                    word=Word(content="Hello,", confidence=1.0),
                    bbox=Bbox(x=0.11768627450980393, y=0.09366161616161624, w=0.04254901960784313,
                              h=0.013939393939393904),
                ),
                WordBox.with_bbox(
                    word=Word(content="World!", confidence=1.0),
                    bbox=Bbox(x=0.11768627450980393, y=0.1219949494949495, w=0.051363137254901964,
                              h=0.013939393939393904),
                ),
            ]
        ),
        (
            "tests/data/vector_3.pdf",
            [
                WordBox.with_bbox(
                    word=Word(content="et", confidence=1.0),
                    bbox=Bbox(x=0.31170826086956527, y=0.0, w=0.02331521739130432, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="al", confidence=1.0),
                    bbox=Bbox(x=0.34089304347826094, y=0.0, w=0.02311956521739128, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="847348", confidence=1.0),
                    bbox=Bbox(x=0.3116934782608696, y=0.0, w=0.09547826086956518, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="0", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0)
                ),
                WordBox.with_bbox(
                    word=Word(content="Qu", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content=".", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content=".", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="9828.", confidence=1.0),
                    bbox=Bbox(x=0.585896739130435, y=0.0, w=0.06932608695652176, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="The", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="Only", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="Thing", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="They", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="Fear", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="Is", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="You", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="•", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="fast,", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="convenient", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="online", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
                WordBox.with_bbox(
                    word=Word(content="submission", confidence=1.0),
                    bbox=Bbox(x=1.0, y=0.0, w=0.0, h=0.0),
                ),
            ]
        ),
    ]
)
def test_vector_pdf_extractor(file, expected_wordboxes, vector_pdf_extractor):
    with open(file, "r+b") as f:
        page_to_extracted_wordboxes_mapping = vector_pdf_extractor.extract_wordboxes(BytesIO(f.read()))

    assert len(page_to_extracted_wordboxes_mapping) == 1
    assert len(page_to_extracted_wordboxes_mapping[0]) == len(expected_wordboxes)
    assert page_to_extracted_wordboxes_mapping[0] == expected_wordboxes
