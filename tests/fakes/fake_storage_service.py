from multiprocessing import Manager

from deps_object_storage import FileAlreadyExists, FileNotFound

__all__ = ["FakeObjectStorage"]


class FakeObjectStorage:
    def __init__(self):
        manager = Manager()
        self.storage_dict = manager.dict()

    def upload(self, path: str, content: bytes, replace_if_exists: bool) -> str:
        if not replace_if_exists and path in self.storage_dict:
            raise FileAlreadyExists(path)
        self.storage_dict[path] = content
        return path

    def download(self, path: str) -> bytes:
        if path not in self.storage_dict:
            raise FileNotFound(path)
        return self.storage_dict[path]
