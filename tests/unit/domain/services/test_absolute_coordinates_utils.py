from deps_lil_chyn.domain.dto import Shape
from deps_lil_chyn.domain.services.utils import AbsoluteCoordinates


def test_convert_to_relative_coordinates():
    x1 = 0
    y1 = 1
    x2 = 10
    y2 = 20
    page_shape = Shape(width=100, height=200)

    r_x1, r_y1, r_x2, r_y2 = AbsoluteCoordinates.convert_to_relative_coordinates(
        x1=x1, y1=y1, x2=x2, y2=y2, page_shape=page_shape
    )

    assert r_x1 == x1 / page_shape.width
    assert r_y1 == y1 / page_shape.height
    assert r_x2 == x2 / page_shape.width
    assert r_y2 == y2 / page_shape.height


def test_clip_coordinates():
    page_shape = Shape(width=100, height=200)
    x1 = -1
    y1 = 8
    x2 = page_shape.width + 10
    y2 = page_shape.height + 400

    x1, y1, x2, y2 = AbsoluteCoordinates.clip_coordinates(
        x1=x1, y1=y1, x2=x2, y2=y2, page_shape=page_shape
    )

    assert x1 == 0
    assert y1 == y1
    assert x2 == page_shape.width
    assert y2 == page_shape.height


def test_are_valid_coordinates():
    x1 = 10
    y1 = -1
    x2 = 3
    y2 = 20
    page_shape = Shape(width=100, height=200)

    assert not AbsoluteCoordinates.are_valid_coordinates(
        x1=x1, y1=y1, x2=x2, y2=y2, page_shape=page_shape
    )

    y1 = 0
    x2 = 13

    assert AbsoluteCoordinates.are_valid_coordinates(
        x1=x1, y1=y1, x2=x2, y2=y2, page_shape=page_shape
    )

    y2 = 700

    assert not AbsoluteCoordinates.are_valid_coordinates(
        x1=x1, y1=y1, x2=x2, y2=y2, page_shape=page_shape
    )
