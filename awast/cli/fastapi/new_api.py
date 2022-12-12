import os
from re import TEMPLATE
from awast.cli.utils import (
    create_poetry_project,
    create_file,
    create_file_arguments,
    get_default_values,
    merge_values,
    update_poetry_project,
)
from typing import Callable, List
import pathlib

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
AWAST_PATH = os.path.abspath(os.path.join(MODULE_PATH, "../.."))
TEMPLATE_PATH = os.path.abspath(os.path.join(AWAST_PATH, "templates/fastapi"))


def new_api(name: str, values: List[str], value_parser: Callable):
    base = os.getcwd()

    output_path = os.path.join(base, name)
    if os.path.exists(output_path):
        raise Exception("Output directory already exist.")

    parsed_values = value_parser(values)

    arguments = create_file_arguments(name, output_path, parsed_values)

    create_poetry_project(name)

    create_pyproject_file(arguments)

    update_poetry_project(name)

    # Create the app.py file inside project
    create_app_file(arguments)

    # Create Dockerfile inside project
    create_dockerfile(arguments)

    # Create github actions for tests
    create_github_actions(arguments)


def create_pyproject_file(arguments: Callable):
    name, output_path, values = arguments()
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="pyproject.toml.jinja",
        app_path=output_path,
        filename="pyproject.toml",
        name=name,
    )


def create_app_file(arguments: Callable):
    name, output_path, values = arguments()
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="app.py.jinja",
        app_path=output_path,
        filename=f"{name}/app.py",
        **values,
    )


def create_dockerfile(arguments: Callable):
    name, output_path, values = arguments()
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="Dockerfile.jinja",
        app_path=output_path,
        filename="Dockerfile",
        package=name,
        **values,
    )


def create_github_actions(arguments: Callable):
    _, output_path, _ = arguments()
    if not os.path.exists(os.path.join(output_path, ".github", "workflows")):
        os.makedirs(os.path.join(output_path, ".github", "workflows"))
    create_unittest_action(arguments)
    create_build_action(arguments)
    create_build_staging_action(arguments)
    create_build_production_action(arguments)
    create_move_issue_action(arguments)


def create_unittest_action(arguments: Callable):
    _, output_path, values = arguments()
    values = merge_values(
        get_default_values(
            pathlib.Path(TEMPLATE_PATH) / "unit_test.values.yaml"
        ),
        values,
    )
    create_file(
        TEMPLATE_PATH,
        "unit_test.yaml.jinja",
        output_path,
        ".github/workflows/unit_test.yaml",
        **values,
    )


def create_build_action(arguments: Callable):
    _, output_path, _ = arguments()
    create_file(
        TEMPLATE_PATH,
        "build.yaml.jinja",
        output_path,
        ".github/workflows/build.yaml",
    )


def create_build_staging_action(arguments: Callable):
    name, output_path, values = arguments()
    values = merge_values(
        get_default_values(
            pathlib.Path(TEMPLATE_PATH) / "build_staging.values.yaml"
        ),
        values,
    )
    values["name"] = name
    create_file(
        TEMPLATE_PATH,
        "build_staging.yaml.jinja",
        output_path,
        ".github/workflows/build_staging.yaml",
        **values,
    )


def create_build_production_action(arguments: Callable):
    name, output_path, values = arguments()
    values = merge_values(
        get_default_values(
            pathlib.Path(TEMPLATE_PATH) / "build_production.values.yaml"
        ),
        values,
    )
    values["name"] = name
    create_file(
        TEMPLATE_PATH,
        "build_production.yaml.jinja",
        output_path,
        ".github/workflows/build_production.yaml",
        **values,
    )


def create_move_issue_action(arguments: Callable):
    _, output_path, _ = arguments()
    create_file(
        TEMPLATE_PATH,
        "move_issue.yaml.jinja",
        output_path,
        ".github/workflows/move_issue.yaml",
    )
