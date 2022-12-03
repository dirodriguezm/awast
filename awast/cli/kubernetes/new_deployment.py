import os
from awast.cli.utils import create_file
from typing import Dict, List, Callable, Union
from pathlib import Path
import re
import yaml

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
AWAST_PATH = os.path.abspath(os.path.join(MODULE_PATH, "../.."))
TEMPLATE_PATH = os.path.abspath(
    os.path.join(AWAST_PATH, "templates/kubernetes")
)


def new_deployment(name: str, values: List[str], value_parser: Callable):
    base = os.getcwd()
    output_path = os.path.join(base, name)
    if os.path.exists(output_path):
        raise Exception("Output directory already exist.")
    os.mkdir(output_path)
    parsed_values = value_parser(values)
    create_deployment_file(name, output_path, parsed_values)


def create_deployment_file(
    deployment_name: str, output_path: str, values: dict
):
    if not os.path.exists(os.path.join(output_path, "deployment")):
        os.mkdir(os.path.join(output_path, "deployment"))

    values = merge_values(
        get_default_values(Path(TEMPLATE_PATH) / "deployment.values.yaml"),
        values,
    )
    values["name"] = deployment_name

    create_file(
        TEMPLATE_PATH,
        "deployment.jinja",
        output_path,
        "deployment/deployment.yaml",
        **values,
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
