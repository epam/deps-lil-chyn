import subprocess
import tempfile
from typing import Optional

from deps_object_storage import ObjectStorage

from deps_lil_chyn.domain.dto import UnifiedContainerData
from deps_lil_chyn.domain.exceptions import MsgUnificationError

from .eml import EmlUnifier

__all__ = ["MsgUnifier"]


class MsgUnifier(EmlUnifier):
    extensions: set[str] = {"msg"}

    def __init__(
        self,
        object_storage: ObjectStorage,
        converter_script_path: str,
        supported_attachment_extensions: Optional[set[str]] = None,
    ):
        super().__init__(
            object_storage=object_storage,
            supported_attachment_extensions=supported_attachment_extensions or set(),
        )
        self._converter_script_path = converter_script_path

    def unify(self, file_path: str) -> UnifiedContainerData:
        file_data = self._download_file_from_storage(file_path)

        return self._unify(self._convert_msg_to_eml(file_data.content))

    def _convert_msg_to_eml(self, file_content: bytes) -> bytes:
        with tempfile.NamedTemporaryFile(mode="wb") as tmp_msg_file:
            tmp_msg_file.write(file_content)
            convert_process = subprocess.Popen(
                (self._converter_script_path, "--outfile", "-", tmp_msg_file.name),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
            )
            converted_file_content, error = convert_process.communicate()

        if convert_process.returncode != 0:
            raise MsgUnificationError(f"Converting msg file error: {str(error)}")

        return converted_file_content
