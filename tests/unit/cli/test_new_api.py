import pathlib
from typer.testing import CliRunner
from awast.cli.main import app
from tests.unit.cli.utils import assert_app_created, assert_dockerfile_created
from awast.cli.utils import (
    create_unittest_action,
    create_build_action,
    create_build_staging_action,
    create_build_production_action,
    create_move_issue_action,
    create_github_actions,
    create_file_arguments,
)

runner = CliRunner()

TESTS_PATH = pathlib.Path.cwd() / "tests"
TESTS_OUTPUT_FILES = TESTS_PATH / "unit" / "cli" / "output_files"
TEMPLATE_PATH = (pathlib.Path.cwd() / "awast/templates/api").resolve()


def test_new_flask(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_path = pathlib.Path(td)
        result = runner.invoke(
            app, ["new-api", "test_api", "--framework", "Flask"]
        )
        assert result.exit_code == 0
        assert_app_created(test_path)
        assert_dockerfile_created(test_path)


def test_new_fastapi(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_path = pathlib.Path(td)
        result = runner.invoke(app, ["new-api", "test_api"])
        assert result.exit_code == 0
        assert_app_created(test_path)
        assert_dockerfile_created(test_path)


def test_create_unittest_action(tmp_path: pathlib.Path):
    arguments = create_file_arguments(
        "test-api",
        tmp_path,
        {
            "workflows": {
                "test": {
                    "coverage_source": "test_source",
                    "python_version": "3.10",
                    "poetry_version": "1.2.0",
                }
            }
        },
        template_path=TEMPLATE_PATH,
        framework="fastapi",
    )
    result_path = tmp_path / ".github" / "workflows"
    result_path.mkdir(parents=True)
    create_unittest_action(arguments)
    check_result_file("unit_test.yaml", result_path)


def test_create_build_action(tmp_path: pathlib.Path):
    arguments = create_file_arguments(
        "test-api", tmp_path, {}, TEMPLATE_PATH, "fastapi"
    )
    result_path = tmp_path / ".github" / "workflows"
    result_path.mkdir(parents=True)
    create_build_action(arguments)
    check_result_file("build.yaml", result_path)


def test_create_build_staging_action(tmp_path: pathlib.Path):
    arguments = create_file_arguments(
        "test-api",
        tmp_path,
        {"workflows": {"build": {"staging": {}}}},
        TEMPLATE_PATH,
        "fastapi",
    )
    result_path = tmp_path / ".github" / "workflows"
    result_path.mkdir(parents=True)
    create_build_staging_action(arguments)
    check_result_file("build_staging.yaml", result_path)


def test_create_build_production_action(tmp_path: pathlib.Path):
    arguments = create_file_arguments(
        "test-api",
        tmp_path,
        {"workflows": {"build": {"production": {}}}},
        TEMPLATE_PATH,
        "fastapi",
    )
    result_path = tmp_path / ".github" / "workflows"
    result_path.mkdir(parents=True)
    create_build_production_action(arguments)
    check_result_file("build_production.yaml", result_path)


def test_create_move_issue_action(tmp_path: pathlib.Path):
    arguments = create_file_arguments(
        "test-api", tmp_path, {}, TEMPLATE_PATH, "fastapi"
    )
    result_path = tmp_path / ".github" / "workflows"
    result_path.mkdir(parents=True)
    create_move_issue_action(arguments)
    check_result_file("move_issue.yaml", result_path)


def test_create_github_actions(tmp_path: pathlib.Path):
    arguments = create_file_arguments(
        "test-api",
        tmp_path,
        {
            "workflows": {
                "test": {
                    "coverage_source": "test_source",
                    "python_version": "3.10",
                    "poetry_version": "1.2.0",
                },
                "build": {"staging": {}, "production": {}},
            },
        },
        TEMPLATE_PATH,
        "fastapi",
    )
    result_path = tmp_path / ".github" / "workflows"
    create_github_actions(arguments)
    check_result_file("move_issue.yaml", result_path)
    check_result_file("build_production.yaml", result_path)
    check_result_file("build_staging.yaml", result_path)
    check_result_file("build.yaml", result_path)
    check_result_file("unit_test.yaml", result_path)


def check_result_file(file_name: str, result_path: pathlib.Path):
    expected_result_path = TESTS_OUTPUT_FILES / file_name
    actual_result_path = result_path / file_name
    assert result_path.exists()
    assert actual_result_path.exists()
    assert (
        expected_result_path.read_text()
        == actual_result_path.read_text() + "\n"
    )
