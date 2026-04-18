from deps_unified_data import Cell


__all__ = ["FakeUnifierProxy"]


class FakeUnifierProxy:
    def __init__(self) -> None:
        self._cells = []

    @property
    def saved_cells(self) -> list[Cell]:
        return self._cells

    def save_cells(self, cells: list[Cell]) -> None:
        self._cells += cells
