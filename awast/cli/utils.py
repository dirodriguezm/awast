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


def create_file_arguments(
    name: str, output_path: Path, parsed_values: dict
) -> Callable:
    def unpack_arguments() -> CreateFileArguments:
        return CreateFileArguments(name, output_path, parsed_values)

    return unpack_arguments
