from deps_lil_chyn.domain.services import PdfToImagesConverter


def test_pdf_to_images_converter():
    path_to_file = f"tests/data/raster.pdf"
    pages_number = 2

    with open(path_to_file, "r+b") as file:
        images = list(PdfToImagesConverter.convert(file))

    assert len(images) == pages_number
