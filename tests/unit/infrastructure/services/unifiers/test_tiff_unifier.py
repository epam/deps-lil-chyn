from uuid import uuid4

from deps_unified_data.model import UnifiedData


def test_unify_tiff(tiff_unifier, fake_storage_service):
    files = ["tests/data/basic-14-pages.TIF"]
    expected_images_paths: list[str] = [
        f"basic-14-pages/original/{idx}.png"
        for idx in range(14)
    ]

    document_id = uuid4().hex

    for file_path in files:
        with open(file_path, "r+b") as f:
            fake_storage_service.upload(path=file_path, content=f.read(), replace_if_exists=True)

    unified_data = tiff_unifier.unify(document_id=document_id, files=files)

    assert isinstance(unified_data, UnifiedData)
    assert unified_data.document_id == document_id

    assert len(unified_data.images) == 14

    first_page = unified_data.images[0]
    assert first_page.page == 1
    assert first_page.width == 2550
    assert first_page.height == 3300

    for image_path in expected_images_paths:
        try:
            fake_storage_service.download(image_path)
        except Exception as e:
            assert False, f"FakeStorageService.download_content: {e}"
