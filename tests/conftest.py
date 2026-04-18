import factory
import pytest

from deps_lil_chyn import init_containers
from deps_lil_chyn.domain.interfaces import IUnifierPlugin
from deps_lil_chyn.infrastructure.access_management.context_vars import user

from .fakes import FakeObjectStorage


@pytest.fixture
def containers():
    return init_containers()


@pytest.fixture
def external_services(containers):
    return containers.external_services


@pytest.fixture
def config(app):
    return app.config


@pytest.fixture
def set_none_api_key(config):
    config.api_key.override(None)
    yield
    config.reset_override()


@pytest.fixture
def set_test_api_key(config):
    config.api_key.override("test-api-key")
    yield
    config.reset_override()


@pytest.fixture
def set_test_api_url(config):
    config.api_url.override("http://test")
    yield
    config.reset_override()


@pytest.fixture
def test_user():
    return {
        "subject": "some_user_id",
        "roles": [],
        "groups": ["deps-users"],
        "token": "token",
    }


@pytest.fixture
def set_test_user(test_user):
    user.set(test_user)


@pytest.fixture
def test_user_deps_token():
    return {
        "subject": "some_user_id",
        "roles": [],
        "groups": ["deps-users"],
        "deps_token": "token",
    }


@pytest.fixture
def set_test_user_deps_token(test_user_deps_token):
    user.set(test_user_deps_token)


@pytest.fixture
def test_user_auth_and_deps_token():
    return {
        "subject": "some_user_id",
        "roles": [],
        "groups": ["deps-users"],
        "token": "token",
        "deps_token": "token",
    }


@pytest.fixture
def set_test_user_auth_and_deps_token(test_user_auth_and_deps_token):
    user.set(test_user_auth_and_deps_token)


@pytest.fixture
def set_test_user_with_empty_token(test_user):
    test_user["token"] = ""
    user.set(test_user)


@pytest.fixture
def mocked_plugin():
    class MockedPlugin(IUnifierPlugin):
        def __init__(self, doc_type: str):
            self.document_type = doc_type

        def unify(self, document_id: int, files: list[str]) -> None:
            pass

    return MockedPlugin(factory.Faker("name"))


@pytest.fixture
def fake_storage_service():
    return FakeObjectStorage()


@pytest.fixture(autouse=True)
def set_fake_storage_service(containers, fake_storage_service):
    with containers.external_services.object_storage.override(fake_storage_service):
        yield


@pytest.fixture
def pdf_unifier(containers):
    yield containers.unifiers.pdf()


@pytest.fixture
def vector_pdf_extractor(containers):
    yield containers.domain_services.vector_pdf_extractor()


@pytest.fixture
def image_unifier(containers):
    yield containers.unifiers.image()


@pytest.fixture
def tiff_unifier(containers):
    yield containers.unifiers.tiff()


@pytest.fixture
def excel_unifier(containers):
    yield containers.unifiers.excel()


@pytest.fixture
def doc_unifier(containers):
    yield containers.unifiers.doc()


@pytest.fixture
def docx_unifier(containers):
    yield containers.unifiers.docx()


@pytest.fixture
def eml_unifier(containers):
    yield containers.unifiers.eml()


@pytest.fixture
def msg_unifier(containers):
    yield containers.unifiers.msg()


@pytest.fixture
def csv_unifier(containers):
    yield containers.unifiers.csv()
