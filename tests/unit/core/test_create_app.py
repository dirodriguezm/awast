from awast.core.mod_fastapi.app_factory import create_app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


def test_app_has_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_app_has_metrics(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200


def test_app_has_ralidator(client):
    raise NotImplementedError("Test not implemented yet")
