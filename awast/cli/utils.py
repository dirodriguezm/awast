import subprocess
import jinja2
from typing import List, Callable
import re
import yaml
from pathlib import Path
from dataclasses import dataclass


def create_poetry_project(name):
    subprocess.run(["poetry", "new", name], check=True)


def update_poetry_project(name):
    subprocess.run(["poetry", "update"], check=True, cwd=Path.cwd() / name)


def get_template(template_path: str, filename: str):
    loader = jinja2.FileSystemLoader(template_path)
    route = jinja2.Environment(loader=loader)
    return route.get_template(filename)


def create_file(
    template_path: Path,
    template_name: str,
    app_path: Path,
    filename: str,
    **template_args,
):
    final_path = app_path / filename
    final_path.touch()
    final_path.write_text(
        get_template(str(template_path), template_name).render(
            **template_args
        ),
        "utf-8",
    )


def value_parser(values: List[str]):
    result = {}
    for val in values:
        nested = val.split(".")
        is_nested = len(nested) > 1
        if is_nested:
            parse_nested(nested, result)
        else:
            valid = re.search(r"^\w+\=\w+$", val)
            if valid:
                splitted = val.split("=")
                key = splitted[0]
                value = splitted[1]
                result[key] = value
            else:
                raise ValueError(f"Provided value {val} is invalid")
    return result


def parse_nested(nested: List[str], result: dict):
    key = nested.pop(0)
    assignment = re.search(r"^\w+\=\w+$", key)
    if not assignment:
        if key not in result:
            result[key] = {}
        parse_nested(nested, result[key])
    else:
        var = key.split("=")[0]
        value = key.split("=")[1]
        result[var] = value


def get_default_values(values_file: Path) -> dict:
    return yaml.load(values_file.read_text(), yaml.CLoader)


def merge_values(dict1: dict, dict2: dict):
    return dict1 | dict2


@dataclass
class CreateFileArguments:
    """
    Arguments for the create file function
    """

    name: str
    output_path: Path
    parsed_values: dict
    template_path: Path
    framework: str


def create_file_arguments(
    name: str,
    output_path: Path,
    parsed_values: dict,
    template_path: Path,
    framework: str,
) -> Callable:
    def unpack_arguments() -> CreateFileArguments:
        return CreateFileArguments(
            name, output_path, parsed_values, template_path, framework
        )

    return unpack_arguments


def create_pyproject_file(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        template_path=args.template_path,
        template_name="pyproject.toml.jinja",
        app_path=args.output_path,
        filename="pyproject.toml",
        name=args.name,
    )


def create_app_file(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    values = args.parsed_values["app"]
    create_file(
        template_path=args.template_path / args.framework,
        template_name="app.py.jinja",
        app_path=args.output_path,
        filename=f"{args.name}/app.py",
        **values,
    )


def create_dockerfile(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    values = args.parsed_values["dockerfile"]
    values["package"] = args.name
    create_file(
        template_path=args.template_path / args.framework,
        template_name="Dockerfile.jinja",
        app_path=args.output_path,
        filename="Dockerfile",
        **values,
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
    values = args.parsed_values["workflows"]["test"]
    print(values)
    create_file(
        args.template_path,
        "unit_test.yaml.jinja",
        args.output_path,
        ".github/workflows/unit_test.yaml",
        **values,
    )


def create_build_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        args.template_path,
        "build.yaml.jinja",
        args.output_path,
        ".github/workflows/build.yaml",
    )


def create_build_staging_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    values = args.parsed_values["workflows"]["build"]["staging"]
    values["name"] = args.name
    create_file(
        args.template_path,
        "build_staging.yaml.jinja",
        args.output_path,
        ".github/workflows/build_staging.yaml",
        **values,
    )


def create_build_production_action(
    arguments: Callable[[], CreateFileArguments]
):
    args = arguments()
    values = args.parsed_values["workflows"]["build"]["production"]
    values["name"] = args.name
    create_file(
        args.template_path,
        "build_production.yaml.jinja",
        args.output_path,
        ".github/workflows/build_production.yaml",
        **values,
    )


def create_move_issue_action(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    create_file(
        args.template_path,
        "move_issue.yaml.jinja",
        args.output_path,
        ".github/workflows/move_issue.yaml",
    )


def parse_default_values(
    template_path: Path, values_file: str, parsed_values: dict
) -> dict:
    default_values_path = template_path / "values.yaml"
    if values_file != "":
        default_values_path = Path(values_file)

    return merge_values(
        get_default_values(default_values_path),
        parsed_values,
    )


def new_api(
    name: str,
    template_path: Path,
    values: List[str],
    value_parser: Callable,
    framework: str,
    values_file: str,
):
    base = Path.cwd()

    output_path = base / name
    if output_path.exists():
        raise Exception("Output directory already exist.")

    parsed_values = value_parser(values)

    parsed_values = parse_default_values(
        template_path, values_file, parsed_values
    )

    arguments = create_file_arguments(
        name, output_path, parsed_values, template_path, framework
    )

    create_poetry_project(name)

    create_pyproject_file(arguments)

    update_poetry_project(name)

    # Create the app.py file inside project
    create_app_file(arguments)

    # Create Dockerfile inside project
    create_dockerfile(arguments)

    # Create github actions for tests
    create_github_actions(arguments)
