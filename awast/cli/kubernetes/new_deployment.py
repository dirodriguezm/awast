import os
from awast.cli.utils import create_file, merge_values, get_default_values
from pathlib import Path
from typing import List, Callable

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
