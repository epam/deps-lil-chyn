import os
from dataclasses import dataclass

__all__ = ["FileData"]


@dataclass
class FileData:
    path: str
    content: bytes

    @property
    def extension(self) -> str:
        return os.path.splitext(self.path)[1]

    @property
    def name(self):
        return os.path.splitext(os.path.basename(self.path))[0]
