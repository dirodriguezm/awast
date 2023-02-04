from starlette.responses import JSONResponse
from awast.core.mod_fastapi.app_factory import create_app, RalidatorStarlette
from fastapi.testclient import TestClient
import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock

ralidator_config = {"SECRET_KEY": "test"}
ralidator_filters_map = {}


@pytest.fixture
def client():
    app = create_app(
        ralidator_config=ralidator_config,
        ralidator_filters_map=ralidator_filters_map,
        ralidator_ignore_paths=["/metrics"],
    )
    yield TestClient(app)


def test_app_has_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_app_has_metrics(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200


def test_app_has_ralidator(mocker: MockerFixture):
    ralidator = mocker.patch.object(
        RalidatorStarlette,
        "apply_ralidator_filters",
        new_callable=AsyncMock,
    )

    ralidator.return_value = JSONResponse({"message": "Hello World"})
    app = create_app(
        ralidator_config=ralidator_config,
        ralidator_filters_map=ralidator_filters_map,
        ralidator_ignore_paths=["metrics"],
    )
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    ralidator.assert_called_once()
