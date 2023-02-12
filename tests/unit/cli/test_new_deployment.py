from awast.cli.kubernetes.new_deployment import pathlib as tpathlib
from awast.cli.kubernetes.new_deployment import (
    new_deployment,
    create_deployment_file,
)
from awast.cli.utils import (
    CreateFileArguments,
    create_file_arguments,
    value_parser,
)
import pathlib
from pytest_mock import MockerFixture


TESTS_PATH = pathlib.Path.cwd() / "tests"
TESTS_OUTPUT_FILES = TESTS_PATH / "unit" / "cli" / "output_files"
TEMPLATE_PATH = (pathlib.Path.cwd() / "awast/templates/kubernetes").resolve()


def test_new_deployment_with_values(mocker: MockerFixture):
    create_deployment_file_mock = mocker.patch(
        "awast.cli.kubernetes.new_deployment.create_deployment_file"
    )
    getcwd = mocker.patch.object(tpathlib.Path, "cwd")
    getcwd.return_value = pathlib.Path("/tmp")
    mocker.patch.object(tpathlib.Path, "mkdir")
    new_deployment(
        "test-api",
        [
            "resources.requests.cpu=10m",
            "image.name=test",
            "nodegroup=test",
        ],
        value_parser,
        "",
    )
    create_deployment_file_mock.assert_called()
    call_args = create_deployment_file_mock.call_args[0][0]
    assert call_args().name == "test-api"
    assert call_args().parsed_values == {
        "name": "test-api",
        "resources": {"requests": {"cpu": "10m", "memory": None}},
        "image": {"name": "test", "version": "latest"},
        "containerPort": 8000,
        "namespace": "web-services",
        "nodegroup": "test",
    }


def test_create_deployment_file(tmp_path):
    (tmp_path / "test-api" / "deployment").mkdir(parents=True)
    values = {
        "name": "test-api",
        "containerPort": "8000",
        "resources": {"requests": {"memory": "10M", "cpu": "10m"}},
        "nodegroup": "test-nodegroup",
        "image": {"name": "test-api", "version": "latest"},
    }
    arguments = create_file_arguments(
        "test-api",
        tmp_path / "test-api",
        values,
        TEMPLATE_PATH,
        "deployment",
    )
    create_deployment_file(arguments)
    assert_deployment_values(
        tmp_path / "test-api" / "deployment" / "deployment.yaml"
    )


def assert_deployment_values(path):
    text = path.read_text()
    assert "name: test-api" in text
    assert "image: ghcr.io/alercebroker/test-api:latest" in text
    assert "test-nodegroup" in text
    assert "containerPort: 8000" in text
    assert "memory: 10M" in text
    assert "cpu: 10m" in text
