from awast.cli.utils import (
    CreateFileArguments,
    create_poetry_project,
    create_file,
    create_file_arguments,
    get_default_values,
    merge_values,
    update_poetry_project,
)
from typing import Callable, List
import pathlib

MODULE_PATH = pathlib.Path(__file__).parent.resolve()
AWAST_PATH = (MODULE_PATH / "../..").resolve()
TEMPLATE_PATH = (AWAST_PATH / "templates/fastapi").absolute()


def new_api(name: str, values: List[str], value_parser: Callable):
    base = pathlib.Path.cwd()
    print(TEMPLATE_PATH)

    output_path = base / name
    if output_path.exists():
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


def create_pyproject_file(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="pyproject.toml.jinja",
        app_path=args.output_path,
        filename="pyproject.toml",
        name=args.name,
    )


def create_app_file(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="app.py.jinja",
        app_path=args.output_path,
        filename=f"{args.name}/app.py",
        **args.parsed_values,
    )


def create_dockerfile(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="Dockerfile.jinja",
        app_path=args.output_path,
        filename="Dockerfile",
        package=args.name,
        **args.parsed_values,
    )


def create_github_actions(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    if not (args.output_path / ".github/workflows").exists():
        (args.output_path / ".github/workflows").mkdir(parents=True)
    create_unittest_action(arguments)
    create_build_action(arguments)
    create_build_staging_action(arguments)
    create_build_production_action(arguments)
    create_move_issue_action(arguments)


def create_unittest_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    values = merge_values(
        get_default_values(
            pathlib.Path(TEMPLATE_PATH) / "unit_test.values.yaml"
        ),
        args.parsed_values,
    )
    create_file(
        TEMPLATE_PATH,
        "unit_test.yaml.jinja",
        args.output_path,
        ".github/workflows/unit_test.yaml",
        **values,
    )


def create_build_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        TEMPLATE_PATH,
        "build.yaml.jinja",
        args.output_path,
        ".github/workflows/build.yaml",
    )


def create_build_staging_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    values = merge_values(
        get_default_values(
            pathlib.Path(TEMPLATE_PATH) / "build_staging.values.yaml"
        ),
        args.parsed_values,
    )
    values["name"] = args.name
    create_file(
        TEMPLATE_PATH,
        "build_staging.yaml.jinja",
        args.output_path,
        ".github/workflows/build_staging.yaml",
        **values,
    )


def create_build_production_action(
    arguments: Callable[[], CreateFileArguments]
):
    args = arguments()
    values = merge_values(
        get_default_values(
            pathlib.Path(TEMPLATE_PATH) / "build_production.values.yaml"
        ),
        args.parsed_values,
    )
    values["name"] = args.name
    create_file(
        TEMPLATE_PATH,
        "build_production.yaml.jinja",
        args.output_path,
        ".github/workflows/build_production.yaml",
        **values,
    )


def create_move_issue_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        TEMPLATE_PATH,
        "move_issue.yaml.jinja",
        args.output_path,
        ".github/workflows/move_issue.yaml",
    )
