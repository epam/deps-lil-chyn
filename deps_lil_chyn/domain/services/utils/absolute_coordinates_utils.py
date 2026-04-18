from typing import Tuple

from deps_lil_chyn.domain.dto import Shape

__all__ = ["AbsoluteCoordinates"]


class AbsoluteCoordinates:
    @staticmethod
    def convert_to_relative_coordinates(
        x1: int, y1: int, x2: int, y2: int, page_shape: Shape
    ) -> Tuple[float, float, float, float]:
        return (
            x1 / page_shape.width,
            y1 / page_shape.height,
            x2 / page_shape.width,
            y2 / page_shape.height,
        )

    @classmethod
    def clip_coordinates(
        cls, x1: int, y1: int, x2: int, y2: int, page_shape: Shape
    ) -> Tuple[int, int, int, int]:
        return (
            cls.clip_x_coordinate(x1, page_shape.width),
            cls.clip_y_coordinate(y1, page_shape.height),
            cls.clip_x_coordinate(x2, page_shape.width),
            cls.clip_y_coordinate(y2, page_shape.height),
        )

    @staticmethod
    def clip_x_coordinate(x: int, page_width: int) -> int:
        return min(x if x > 0 else 0, page_width)

    @staticmethod
    def clip_y_coordinate(y: int, page_height: int) -> int:
        return min(y if y > 0 else 0, page_height)

    @staticmethod
    def are_valid_coordinates(
        x1: int, y1: int, x2: int, y2: int, page_shape: Shape
    ) -> bool:
        return (
            x1 >= 0
            and y1 >= 0
            and x2 >= 0
            and y2 >= 0
            and x2 <= page_shape.width
            and y2 <= page_shape.height
            and x1 <= x2
            and y1 <= y2
        )
