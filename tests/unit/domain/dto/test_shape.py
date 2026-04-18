from pdfminer.pdfpage import PDFPage

from deps_lil_chyn.domain.dto import Shape

FIRST_ELEMENT = 0


def test_shape():
    width = 100
    height = 300

    shape = Shape(width=width, height=height)

    assert shape.width == width
    assert shape.height == height


def test_from_page__without_rotation__ok():
    with open("tests/data/vector_3.pdf", "r+b") as f:
        pages = list(PDFPage.get_pages(f))

    shape = Shape.from_page(pages[FIRST_ELEMENT])

    assert shape.height < shape.width


def test_calculate_shape__rotation_90__ok():
    with open("tests/data/vector_4.pdf", "r+b") as f:
        pages = list(PDFPage.get_pages(f))

    shape = Shape.from_page(pages[FIRST_ELEMENT])

    assert shape.height < shape.width
