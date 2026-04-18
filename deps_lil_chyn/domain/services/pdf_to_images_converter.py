from typing import IO, Any, Generator

from ..dto import ImageData, ImageExtension
from .utils import DEFAULT_TARGET_DPI, convert_pdf_to_pil_images

__all__ = ["PdfToImagesConverter"]


class PdfToImagesConverter:
    @staticmethod
    def convert(
        file: IO[Any],
        dpi: int = DEFAULT_TARGET_DPI,
        extension: ImageExtension = ImageExtension.PNG,
    ) -> Generator[ImageData, None, None]:
        for pil_image in convert_pdf_to_pil_images(file_object=file, dpi=dpi):
            yield ImageData.from_pil_image(image=pil_image, extension=extension)
