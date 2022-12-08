from awast.cli.kubernetes.new_deployment import (
    new_deployment,
    create_deployment_file,
)
from awast.cli.utils import value_parser
import os


def test_new_deployment_with_values(mocker):
    create_deployment_file_mock = mocker.patch(
        "awast.cli.kubernetes.new_deployment.create_deployment_file"
    )
    getcwd = mocker.patch("os.getcwd")
    getcwd.return_value = "/tmp"
    mocker.patch("os.mkdir")
    new_deployment(
        "test-api", ["version=1", "resources.requests.cpu=10m"], value_parser
    )
    create_deployment_file_mock.assert_called_with(
        "test-api",
        "/tmp/test-api",
        {"version": "1", "resources": {"requests": {"cpu": "10m"}}},
    )


def test_create_deployment_file(tmp_path):
    os.mkdir(tmp_path / "test-api")
    values = {
        "environment": "test",
        "version": "1",
        "port": "8000",
        "resources": {"requests": {"mem": "10M", "cpu": "10m"}},
    }
    create_deployment_file("test-api", tmp_path / "test-api", values)
    assert_deployment_values(
        tmp_path / "test-api" / "deployment" / "deployment.yaml"
    )


def assert_deployment_values(path):
    text = path.read_text()
    assert "name: test-api" in text
    assert "image: ghcr.io/alercebroker/test-api:1" in text
    assert "test-web-services" in text
    assert "containerPort: 8000" in text
    assert "memory: 10M" in text
    assert "cpu: 10m" in text
