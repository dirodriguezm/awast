import pathlib


def assert_app_created(tmp_path: pathlib.Path):
    app_path = tmp_path / "test_api" / "test_api" / "app.py"
    assert app_path.is_file()


def assert_dockerfile_created(tmp_path: pathlib.Path):
    app_path = tmp_path / "test_api" / "Dockerfile"
    assert app_path.is_file()


def assert_call_args(call_args):
    assert call_args().name == "test-api"
    assert call_args().parsed_values == {
        "name": "test-api",
        "resources": {"requests": {"cpu": "10m", "memory": None}},
        "image": {"name": "test", "version": "latest"},
        "containerPort": 8000,
        "namespace": "web-services",
        "nodegroup": "test",
    }


def assert_deployment_values(path):
    text = path.read_text()
    assert "name: test-api" in text
    assert "image: ghcr.io/alercebroker/test-api:latest" in text
    assert "test-nodegroup" in text
    assert "containerPort: 8000" in text
    assert "memory: 10M" in text
    assert "cpu: 10m" in text


def assert_service_values(path):
    text = path.read_text()
    assert "name: test-api" in text
    assert "namespace: test" in text
