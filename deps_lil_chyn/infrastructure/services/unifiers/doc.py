import os
import shutil
import subprocess
import tempfile
from io import BytesIO

from deps_object_storage import ObjectStorage
from deps_unified_data import UnifiedData, UnifiedDataFactory
from docx import Document as DocxDocument
from docx.oxml.table import CT_Tbl as DocxTableElement
from docx.oxml.text.paragraph import CT_P as DocxParagraphElement

from deps_lil_chyn.domain.exceptions import DocUnificationError
from deps_lil_chyn.infrastructure.services import UnifierProxy

from .docx import DocxUnifier

__all__ = ["DocUnifier"]


class DocUnifier(DocxUnifier):
    extensions: set[str] = {"doc"}

    def __init__(
        self,
        object_storage: ObjectStorage,
        unifier_proxy: UnifierProxy,
    ):
        super().__init__(
            object_storage=object_storage,
            unifier_proxy=unifier_proxy,
        )
        if not shutil.which("soffice"):
            raise RuntimeError(
                "LibreOffice (soffice) is not installed. "
                "Please install libreoffice package to convert .doc files."
            )

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)

        for file_path in files:
            file_object = self._download_file_from_storage(file_path)
            converted_docx_content = self._convert_doc_to_docx(file_object.content)
            self._unify_docx_content(
                unified_data, converted_docx_content, file_object.name
            )

        return unified_data

    def _convert_doc_to_docx(self, file_content: bytes) -> bytes:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.doc")
            with open(input_file, "wb") as f:
                f.write(file_content)

            convert_process = subprocess.Popen(
                [
                    "soffice",
                    "--headless",
                    "--invisible",
                    "--nologo",
                    "--norestore",
                    "--convert-to",
                    "docx",
                    "--outdir",
                    temp_dir,
                    input_file,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
            )
            stdout, stderr = convert_process.communicate()

            if convert_process.returncode != 0:
                raise DocUnificationError(
                    f"Converting doc file error: {stderr.decode('utf-8', errors='replace')}"
                )

            output_file = os.path.join(temp_dir, "input.docx")
            if not os.path.exists(output_file):
                raise DocUnificationError(
                    f"Converted file not found. LibreOffice output: {stdout.decode('utf-8', errors='replace')}"
                )

            with open(output_file, "rb") as f:
                return f.read()

    def _unify_docx_content(
        self, unified_data: UnifiedData, docx_content: bytes, original_file_name: str
    ) -> None:
        with BytesIO(docx_content) as file:
            docx_obj = DocxDocument(file)

        parent_element = docx_obj.element.body

        for element in parent_element.iterchildren():
            if isinstance(element, DocxParagraphElement):
                from .docx import _DocxParagraphUnifier

                _DocxParagraphUnifier(
                    element, docx_obj, original_file_name, self
                ).unify(unified_data)
            elif isinstance(element, DocxTableElement):
                from .docx import _DocxTableUnifier

                _DocxTableUnifier(element, docx_obj, original_file_name, self).unify(
                    unified_data
                )
