from awast.cli.kubernetes.new_deployment import (
    new_deployment,
    value_parser,
    parse_nested,
    create_deployment_file,
)
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


def test_parse_nested():
    result = {}
    parse_nested(["resources", "requests", "cpu=10m"], result)
    assert result == {"resources": {"requests": {"cpu": "10m"}}}


def test_parse_nested_chained():
    result = {}
    parse_nested(["uno", "dos", "tres=1"], result)
    parse_nested(["uno", "dos", "cuatro=2"], result)
    parse_nested(["uno", "cinco=3"], result)
    assert result == {
        "uno": {"dos": {"tres": "1", "cuatro": "2"}, "cinco": "3"}
    }


def test_parse_nested_chained_repeaeted():
    result = {}
    parse_nested(["uno", "dos", "tres=1"], result)
    parse_nested(["uno", "dos", "tres=2"], result)
    assert result == {"uno": {"dos": {"tres": "2"}}}


def test_value_parser():
    result = value_parser(["version=1"])
    assert result == {"version": "1"}


def test_value_parser_with_nested():
    result = value_parser(
        [
            "version=1",
            "resources.requests.cpu=10m",
            "resources.requests.mem=10M",
        ]
    )
    assert result == {
        "version": "1",
        "resources": {"requests": {"cpu": "10m", "mem": "10M"}},
    }


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
