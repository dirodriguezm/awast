import subprocess
import jinja2
import os
from typing import List
import re
import yaml
from pathlib import Path


def create_poetry_project(name):
    subprocess.run(["poetry", "new", name], check=True)
    subprocess.run(
        ["poetry", "add", "https://github.com/dirodriguezm/awast}"], check=True
    )


def get_template(template_path: str, filename: str):
    loader = jinja2.FileSystemLoader(template_path)
    route = jinja2.Environment(loader=loader)
    return route.get_template(filename)


def create_file(
    template_path: str,
    template_name: str,
    app_path: str,
    filename: str,
    **template_args,
):
    with open(os.path.join(app_path, filename), "w", encoding="utf-8") as f:
        f.write(
            get_template(template_path, template_name).render(**template_args)
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


def create_file_arguments(name, output_path, parsed_values):
    def unpack_arguments():
        return name, output_path, parsed_values

    return unpack_arguments
