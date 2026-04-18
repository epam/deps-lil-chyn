from deps_lil_chyn.domain.dto import FileData


def test_file_data():
    file_extension = ".pdf"
    file_name = "vector"
    path_to_file = f"tests/data/{file_name}{file_extension}"

    with open(path_to_file, "r+b") as file:
        file_content = file.read()
        file_data = FileData(content=file_content, path=path_to_file)

    assert file_data.extension == file_extension
    assert file_data.name == file_name
    assert file_data.content == file_content
