import pathlib


def assert_app_created(tmp_path: pathlib.Path):
    app_path = tmp_path / "test_api" / "test_api" / "app.py"
    assert app_path.is_file()


def assert_dockerfile_created(tmp_path: pathlib.Path):
    app_path = tmp_path / "test_api" / "Dockerfile"
    assert app_path.is_file()
