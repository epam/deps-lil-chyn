from deps_lil_chyn.domain.services.utils import MAX_RESULT_IMAGE_DIMENSION, convert_pdf_to_pil_images

TARGET_DPI = 300.0
DPI_THRESHOLD = 1.0


def compare_dpi_values(
    dpi: float, expected_dpi: float, threshold: float = DPI_THRESHOLD
):
    return expected_dpi - threshold <= dpi <= expected_dpi + threshold


def test_pdf_to_images_conversion():
    files = [
        {"path": "tests/data/test_dpi_1.pdf", "pages_number": 1},
        {
            "path": "tests/data/test_dpi_2.pdf",
            "pages_number": 9,
        },
    ]

    for file in files:
        with open(file["path"], "r+b") as pdf_file:
            images_number = 0

            for image in convert_pdf_to_pil_images(pdf_file, dpi=TARGET_DPI):
                images_number += 1

                assert compare_dpi_values(image.info["dpi"][0], TARGET_DPI)
                assert compare_dpi_values(image.info["dpi"][1], TARGET_DPI)
                assert image.height <= MAX_RESULT_IMAGE_DIMENSION
                assert image.width <= MAX_RESULT_IMAGE_DIMENSION

            assert images_number == file["pages_number"]
