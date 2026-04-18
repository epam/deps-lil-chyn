import csv
from io import StringIO
from itertools import islice
from typing import Iterable, Type

__all__ = ["CsvReader"]


class CsvReader:
    def __init__(self, file: StringIO) -> None:
        self._file = file
        self._head = self._get_csv_head(file)
        self._reader = self._get_reader()

    @property
    def rows(self) -> Iterable[Iterable[str]]:
        return self._reader

    def _get_reader(self) -> Iterable[Iterable[str]]:
        return csv.reader(self._file, dialect=self._get_csv_dialect())

    def _get_csv_head(self, file: StringIO) -> str:
        rows_in_head = 3
        csv_head = "".join(islice(self._file, rows_in_head))
        file.seek(0)

        return csv_head

    def _get_csv_dialect(self) -> Type[csv.Dialect]:
        return csv.Sniffer().sniff(self._head)
