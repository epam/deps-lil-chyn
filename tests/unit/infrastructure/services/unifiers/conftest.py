import pytest
from tests.fakes import FakeUnifierProxy


@pytest.fixture
def fake_unifier_proxy():
    return FakeUnifierProxy()


@pytest.fixture(autouse=True)
def set_fake_unifier_proxy(containers, fake_unifier_proxy):
    with containers.external_services.unifier_proxy.override(fake_unifier_proxy):
        yield
