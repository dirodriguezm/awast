from typer.testing import CliRunner
from awast.cli.main import app
import pathlib
from awast.cli.utils import create_file_arguments
from awast.cli.fastapi.new_api import create_unittest_action

runner = CliRunner()


def test_new_fastapi(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_path = pathlib.Path(td)
        result = runner.invoke(app, ["new-api", "test_api"])
        assert result.exit_code == 0
        assert_app_created(test_path)
        assert_dockerfile_created(test_path)


def assert_app_created(tmp_path: pathlib.Path):
    app_path = tmp_path / "test_api" / "test_api" / "app.py"
    assert app_path.is_file()


def assert_dockerfile_created(tmp_path: pathlib.Path):
    app_path = tmp_path / "test_api" / "Dockerfile"
    assert app_path.is_file()


def test_new_flaskapi():
    with runner.isolated_filesystem():
        result = runner.invoke(
            app, ["new-api", "test-api", "--framework", "Flask"]
        )
        assert result.exit_code == 0


def test_create_unittest_action(tmp_path: pathlib.Path):
    arguments = create_file_arguments("test-api", tmp_path, {"test": "test"})
    create_unittest_action(arguments)
    result_path = tmp_path / ".github" / "workflows"
    assert result_path.exists()
    assert (result_path / "unit_test.yaml").exists()
