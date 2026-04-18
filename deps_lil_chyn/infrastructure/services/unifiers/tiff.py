import logging
from io import BytesIO

from deps_unified_data.model import UnifiedData, UnifiedDataFactory
from PIL import Image

from deps_lil_chyn.domain.dto import FileData, ImageData

from .abstract_unifier import AbstractUnifier

__all__ = ["TiffUnifier"]

_logger = logging.getLogger(__name__)


class TiffUnifier(AbstractUnifier):
    extensions: set[str] = {"tiff", "tif"}

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)

        for file_path in files:
            self._unify_file(unified_data, file_path)

        return unified_data

    def _unify_file(self, unified_data: UnifiedData, file_path: str) -> None:
        _logger.info(
            f"Downloading source file for document `{unified_data.document_id}` from `{file_path}`..."
        )

        file_data: FileData = self._download_file_from_storage(file_path)

        with BytesIO(file_data.content) as file:
            with Image.open(file, formats=["tiff"]) as pil_object:
                _logger.info(
                    f"Document's `{unified_data.document_id}` TIFF file has {pil_object.n_frames} pages."
                )

                for inner_image_link in range(pil_object.n_frames):
                    _logger.info(
                        f"Processing page `{inner_image_link + 1}` for document `{unified_data.document_id}`"
                    )

                    pil_object.seek(inner_image_link)

                    image_data = ImageData.from_pil_image(pil_object)

                    blob_name: str = self._upload_file_to_storage(
                        FileData(
                            path=self._get_original_image_path(
                                file_name=file_data.name,
                                image_name=f"{inner_image_link}.png",
                            ),
                            content=image_data.content,
                        )
                    )

                    (
                        unified_data.image_builder.for_page(inner_image_link + 1)
                        .with_blob(blob_name)
                        .with_shape(width=image_data.width, height=image_data.height)
                        .build()
                    )
