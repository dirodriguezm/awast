from awast.cli.kubernetes.new_deployment import (
    create_service_file,
    pathlib as tpathlib,
)
from awast.cli.kubernetes.new_deployment import (
    new_deployment,
    create_deployment_file,
)
from awast.cli.utils import (
    create_file_arguments,
    value_parser,
)
import pathlib
from pytest_mock import MockerFixture
from .utils import (
    assert_call_args,
    assert_deployment_values,
    assert_service_values,
)


TESTS_PATH = pathlib.Path.cwd() / "tests"
TESTS_OUTPUT_FILES = TESTS_PATH / "unit" / "cli" / "output_files"
TEMPLATE_PATH = (pathlib.Path.cwd() / "awast/templates/kubernetes").resolve()


def test_new_deployment_with_values(mocker: MockerFixture):
    create_deployment_file_mock = mocker.patch(
        "awast.cli.kubernetes.new_deployment.create_deployment_file"
    )
    create_service_file_mock = mocker.patch(
        "awast.cli.kubernetes.new_deployment.create_service_file"
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
    create_service_file_mock.assert_called()
    assert_call_args(create_deployment_file_mock.call_args[0][0])
    assert_call_args(create_service_file_mock.call_args[0][0])


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
        tmp_path / "test-api" / "deployment" / "test-api.yaml"
    )


def test_create_service_file(tmp_path):
    (tmp_path / "test-api" / "service").mkdir(parents=True)
    values = {"name": "test-api", "namespace": "test"}
    arguments = create_file_arguments(
        "test-api",
        tmp_path / "test-api",
        values,
        TEMPLATE_PATH,
        "service",
    )
    create_service_file(arguments)
    assert_service_values(tmp_path / "test-api" / "service" / "test-api.yaml")
