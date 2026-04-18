from uuid import uuid4

from deps_unified_data.model import Image, UnifiedData


def test_unify_image(image_unifier, fake_storage_service):
    files = ["tests/data/image.png"]
    document_id = uuid4().hex

    for file_path in files:
        with open(file_path, "r+b") as f:
            fake_storage_service.upload(path=file_path, content=f.read(), replace_if_exists=True)

    unified_data = image_unifier.unify(document_id=document_id, files=files)

    assert len(unified_data.images) == len(files)
    assert isinstance(unified_data, UnifiedData)
    assert isinstance(unified_data.images[0], Image)
