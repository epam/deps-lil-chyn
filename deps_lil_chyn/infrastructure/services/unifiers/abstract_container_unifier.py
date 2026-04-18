import os
from abc import ABC, abstractmethod
from uuid import uuid4

from deps_object_storage import ObjectStorage

from deps_lil_chyn.domain.dto import FileData, UnifiedContainerData

__all__ = ["AbstractContainerUnifier"]


class AbstractContainerUnifier(ABC):
    extensions: set[str]
    supported_attachment_extensions: set[str]

    def __init__(self, object_storage: ObjectStorage):
        self._object_storage = object_storage

    @abstractmethod
    def unify(self, file_path: str) -> UnifiedContainerData:
        pass

    def _download_file_from_storage(self, file_path: str) -> FileData:
        file_content = self._object_storage.download(path=file_path)

        return FileData(path=file_path, content=file_content)

    def _upload_file_to_storage(self, file_data: FileData) -> str:
        return self._object_storage.upload(
            path=file_data.path,
            content=file_data.content,
            replace_if_exists=True,
        )

    @staticmethod
    def _get_file_extension(file_name: str) -> str:
        _, file_extension = os.path.splitext(file_name)

        return file_extension.lstrip(".").lower()

    @staticmethod
    def _generate_unique_file_name(file_name: str) -> str:
        _, ext = os.path.splitext(file_name)

        return str(uuid4().hex) + ext
