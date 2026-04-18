from io import BytesIO

from deps_unified_data.model import UnifiedData, UnifiedDataFactory
from PIL import Image

from deps_lil_chyn.domain.dto import ImageData

from .abstract_unifier import AbstractUnifier

__all__ = ["ImageUnifier"]


class ImageUnifier(AbstractUnifier):
    extensions: set[str] = {"png", "jpg", "jpeg"}
    extension_to_pil_fmt = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}

    def unify(self, document_id: str, files: list[str]) -> UnifiedData:
        unified_data = UnifiedDataFactory.make_unified_data(document_id)

        for file_path in files:
            self._unify_file(unified_data, file_path)

        return unified_data

    def _unify_file(self, unified_data: UnifiedData, file_path: str) -> None:
        file_data = self._download_file_from_storage(file_path)
        with BytesIO(file_data.content) as file:
            with Image.open(
                file, formats=[self.extension_to_pil_fmt[file_data.extension]]
            ) as img_pil:
                image = ImageData.from_pil_image(img_pil)

        unified_data_builder = (
            unified_data.image_builder.for_page(1)
            .with_blob(file_path)
            .with_shape(width=image.shape.width, height=image.shape.height)
        )
        unified_data_builder.build()
