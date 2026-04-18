from uuid import uuid4

import pytest
from deps_unified_data import UnifiedDataFactory, CellCoordinates
from tests.fakes import FakeObjectStorage


@pytest.fixture
def make_unified_data_1(fake_storage_service: FakeObjectStorage):
    """Expected unified data for doc_file_1.doc."""
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("The", 1.0),
                ("standard", 1.0),
                ("Lorem", 1.0),
                ("Ipsum", 1.0),
                ("passage,", 1.0),
                ("used", 1.0),
                ("since", 1.0),
                ("the", 1.0),
                ("1500s", 1.0),
            )
        )
        .build()
    )

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("\"Lorem", 1.0),
                ("ipsum", 1.0),
                ("dolor", 1.0),
                ("sit", 1.0),
                ("amet,", 1.0),
                ("consectetur", 1.0),
                ("adipiscing", 1.0),
                ("elit,", 1.0),
                ("sed", 1.0),
                ("do", 1.0),
                ("eiusmod", 1.0),
                ("tempor", 1.0),
                ("incididunt", 1.0),
                ("ut", 1.0),
                ("labore", 1.0),
                ("et", 1.0),
                ("dolore", 1.0),
                ("magna", 1.0),
                ("aliqua.", 1.0),
                ("Ut", 1.0),
                ("enim", 1.0),
                ("ad", 1.0),
                ("minim", 1.0),
                ("veniam,", 1.0),
                ("quis", 1.0),
                ("nostrud", 1.0),
                ("exercitation", 1.0),
                ("ullamco", 1.0),
                ("laboris", 1.0),
                ("nisi", 1.0),
                ("ut", 1.0),
                ("aliquip", 1.0),
                ("ex", 1.0),
                ("ea", 1.0),
                ("commodo", 1.0),
                ("consequat.", 1.0),
                ("Duis", 1.0),
                ("aute", 1.0),
                ("irure", 1.0),
                ("dolor", 1.0),
                ("in", 1.0),
                ("reprehenderit", 1.0),
                ("in", 1.0),
                ("voluptate", 1.0),
                ("velit", 1.0),
                ("esse", 1.0),
                ("cillum", 1.0),
                ("dolore", 1.0),
                ("eu", 1.0),
                ("fugiat", 1.0),
                ("nulla", 1.0),
                ("pariatur.", 1.0),
                ("Excepteur", 1.0),
                ("sint", 1.0),
                ("occaecat", 1.0),
                ("cupidatat", 1.0),
                ("non", 1.0),
                ("proident,", 1.0),
                ("sunt", 1.0),
                ("in", 1.0),
                ("culpa", 1.0),
                ("qui", 1.0),
                ("officia", 1.0),
                ("deserunt", 1.0),
                ("mollit", 1.0),
                ("anim", 1.0),
                ("id", 1.0),
                ("est", 1.0),
                ("laborum.\"", 1.0),
            )
        )
        .build()
    )

    blob_name = "original/1.png"
    with open("tests/data/docx_image_1.png", "rb") as file:
        fake_storage_service.upload(path=blob_name, content=file.read(), replace_if_exists=True)

    (
        unified_data.image_builder
        .for_page(1)
        .with_blob(blob_name)
        .with_shape(width=366, height=244)
        .build()
    )

    table = unified_data.table_builder.for_page(1).build()
    cells = [table.add_cell(
        content="First Name",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="Last Name",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="Email",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="Jane1",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="Doe1",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=1, column_span=1, row_span=2),
    ), table.add_cell(
        content="Sample1@example.org",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="Jane2",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="Sample2@example.org",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="Jane2",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="Doe2",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="Sample2@example.org",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=3, column_span=1, row_span=1),
    )]

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("\"Lorem", 1.0),
                ("ipsum", 1.0),
                ("dolor", 1.0),
                ("sit", 1.0),
                ("amet,", 1.0),
                ("consectetur", 1.0),
                ("adipiscing", 1.0),
                ("elit,", 1.0),
                ("sed", 1.0),
                ("do", 1.0),
                ("eiusmod", 1.0),
                ("tempor", 1.0),
                ("incididunt", 1.0),
                ("ut", 1.0),
                ("labore", 1.0),
                ("et", 1.0),
                ("dolore", 1.0),
                ("magna", 1.0),
                ("aliqua.", 1.0),
                ("Ut", 1.0),
                ("enim", 1.0),
                ("ad", 1.0),
                ("minim", 1.0),
                ("veniam,", 1.0),
                ("quis", 1.0),
                ("nostrud", 1.0),
                ("exercitation", 1.0),
                ("ullamco", 1.0),
                ("laboris", 1.0),
                ("nisi", 1.0),
                ("ut", 1.0),
                ("aliquip", 1.0),
                ("ex", 1.0),
                ("ea", 1.0),
                ("commodo", 1.0),
                ("consequat.", 1.0),
                ("Duis", 1.0),
                ("aute", 1.0),
                ("irure", 1.0),
                ("dolor", 1.0),
                ("in", 1.0),
                ("reprehenderit", 1.0),
                ("in", 1.0),
                ("voluptate", 1.0),
                ("velit", 1.0),
                ("esse", 1.0),
                ("cillum", 1.0),
                ("dolore", 1.0),
                ("eu", 1.0),
                ("fugiat", 1.0),
                ("nulla", 1.0),
                ("pariatur.", 1.0),
                ("Excepteur", 1.0),
                ("sint", 1.0),
                ("occaecat", 1.0),
                ("cupidatat", 1.0),
                ("non", 1.0),
                ("proident,", 1.0),
                ("sunt", 1.0),
                ("in", 1.0),
                ("culpa", 1.0),
                ("qui", 1.0),
                ("officia", 1.0),
                ("deserunt", 1.0),
                ("mollit", 1.0),
                ("anim", 1.0),
                ("id", 1.0),
                ("est", 1.0),
                ("laborum.\"", 1.0),
            )
        )
        .build()
    )

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("Adssa,", 1.0),
                ("dassd!", 1.0),
                ("Sdasdsa#", 1.0),
                ("dasds$", 1.0),
                ("sdsad%", 1.0),
                ("adsdas^", 1.0),
                ("asdsad&", 1.0),
                ("sdasdas", 1.0),
                ("{", 1.0),
                ("dsadsd}", 1.0),
                ("“adsdsad”", 1.0),
                ("{sadsda}", 1.0),
                ("[asdsadsaa]", 1.0),
            )
        )
        .build()
    )

    return unified_data, cells


@pytest.fixture
def make_unified_data_2(fake_storage_service: FakeObjectStorage):
    """Expected unified data for doc_file_2.doc."""
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                (" 不用谢,", 1.0),
                (" 你好吗?", 1.0),
            )
        )
        .build()
    )

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("Wie", 1.0),
                ("heißt", 1.0),
                ("du?", 1.0),
                ("Wie", 1.0),
                ("geht", 1.0),
                ("es", 1.0),
                ("dir?", 1.0),
            )
        )
        .build()
    )

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("Ви", 1.0),
                ("говорите", 1.0),
                ("англійською? Скільки", 1.0),
                ("тобі", 1.0),
                ("років?", 1.0),
            )
        )
        .build()
    )

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("Говорите", 1.0),
                ("помедленнее.", 1.0),
            )
        )
        .build()
    )

    (
        unified_data.positonal_text_builder
        .for_page(1)
        .with_words(
            (
                ("Buenos", 1.0),
                ("días", 1.0),
                ("¿Cómo", 1.0),
                ("estás?", 1.0),
            )
        )
        .build()
    )

    table = unified_data.table_builder.for_page(1).build()
    cells = [table.add_cell(
        content="1",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="1234567890",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="!@#$$%#%^^$",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="ABCDEFG",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="<><<?",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="АБВГДЕЖЗИКЛМНО",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="一二三四五六七八九十",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="+][-",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="2",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="3",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="4",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=3, column_span=1, row_span=1),
    ), table.add_cell(
        content="5",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="6",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=5, column_span=1, row_span=1),
    ), table.add_cell(
        content="7",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=6, column_span=1, row_span=1),
    ), table.add_cell(
        content="8",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=3, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=4, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=5, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=6, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=7, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=8, row=7, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=9, row=7, column_span=1, row_span=1),
    )]

    return unified_data, cells


@pytest.fixture
def make_unified_data_3(fake_storage_service: FakeObjectStorage):
    """Expected unified data for doc_file_3.doc."""
    document_id = uuid4().hex
    unified_data = UnifiedDataFactory.make_unified_data(document_id)
    table = unified_data.table_builder.for_page(1).build()
    cells = [table.add_cell(
        content="1",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="2",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=0, column_span=1, row_span=1),
    ), table.add_cell(
        content="4",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="6",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=1, column_span=1, row_span=1),
    ), table.add_cell(
        content="7",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="8",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="9",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=2, column_span=1, row_span=1),
    ), table.add_cell(
        content="10",
        confidence=1.0,
        coordinates=CellCoordinates(column=0, row=3, column_span=1, row_span=2),
    ), table.add_cell(
        content="11",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=3, column_span=2, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=1, row=4, column_span=1, row_span=1),
    ), table.add_cell(
        content="",
        confidence=1.0,
        coordinates=CellCoordinates(column=2, row=4, column_span=1, row_span=1),
    )]

    return unified_data, cells


@pytest.fixture(
    scope="function",
    params=[
        ("tests/data/doc_file_1.doc", "make_unified_data_1"),
        ("tests/data/doc_file_2.doc", "make_unified_data_2"),
        ("tests/data/doc_file_3.doc", "make_unified_data_3"),
    ],
)
def doc_unified_data(request, fake_storage_service: FakeObjectStorage):
    """Fixture that provides doc file test data."""
    file_path, fixture = request.param
    unified_data, cells = request.getfixturevalue(fixture)
    
    try:
        with open(file_path, "r+b") as f:
            fake_storage_service.upload(path=file_path, content=f.read(), replace_if_exists=True)
    except FileNotFoundError:
        # If test file doesn't exist, skip this test
        pytest.skip(f"Test file {file_path} not found")

    yield file_path, unified_data, cells

