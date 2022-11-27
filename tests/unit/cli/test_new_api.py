from typer.testing import CliRunner
from awast.cli.main import app
from pathlib import Path

runner = CliRunner()


def test_new_fastapi(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_path = Path(td)
        result = runner.invoke(app, ["new-api", "test_api"])
        assert result.exit_code == 0
        assert_app_created(test_path)
        assert_dockerfile_created(test_path)


def assert_app_created(tmp_path: Path):
    app_path = tmp_path / "test_api" / "test_api" / "app.py"
    assert app_path.is_file()


def assert_dockerfile_created(tmp_path: Path):
    app_path = tmp_path / "test_api" / "Dockerfile"
    assert app_path.is_file()


def test_new_flaskapi():
    with runner.isolated_filesystem():
        result = runner.invoke(
            app, ["new-api", "test-api", "--framework", "Flask"]
        )
        assert result.exit_code == 0
