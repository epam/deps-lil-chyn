import os
from abc import ABC, abstractmethod

from deps_object_storage import ObjectStorage
from deps_unified_data.model import UnifiedData

from deps_lil_chyn.domain.dto import FileData

__all__ = ["AbstractUnifier"]

ORIGINAL_IMAGES_FOLDER = "original"


class AbstractUnifier(ABC):
    extensions: set[str]

    def __init__(self, object_storage: ObjectStorage):
        self._object_storage = object_storage

    @abstractmethod
    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        pass

    def _download_file_from_storage(self, file_path: str) -> FileData:
        file_content = self._object_storage.download(file_path)

        return FileData(path=file_path, content=file_content)

    def _upload_file_to_storage(self, file_data: FileData) -> str:
        return self._object_storage.upload(
            path=file_data.path,
            content=file_data.content,
            replace_if_exists=True,
        )

    @staticmethod
    def _get_original_image_path(file_name: str, image_name: str) -> str:
        return os.path.join(file_name, ORIGINAL_IMAGES_FOLDER, image_name)
