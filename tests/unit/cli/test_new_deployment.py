from typer.testing import CliRunner
from awast.cli.main import app
from pathlib import Path

runner = CliRunner()


def test_new_deployment_without_values(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_path = Path(td)
        result = runner.invoke(app, ["new-deployment", "test_api"])
        assert result.exit_code == 0
        assert_deployment_created(test_path)


def assert_deployment_created(path):
    pass


def test_new_deployment_with_values(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_path = Path(td)
        result = runner.invoke(
            app, ["new-deployment", "test-api", "--set version: 1"]
        )
        assert json_parser()
