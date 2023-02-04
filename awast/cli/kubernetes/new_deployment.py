from awast.cli.utils import create_file, merge_values, get_default_values
import pathlib
from typing import List, Callable


def new_deployment(name: str, values: List[str], value_parser: Callable):
    base = pathlib.Path.cwd()
    output_path = base / name
    if output_path.exists():
        raise Exception("Output directory already exist.")
    parsed_values = value_parser(values)
    create_deployment_file(name, output_path, parsed_values)


def create_deployment_file(
    deployment_name: str,
    output_path: pathlib.Path,
    values: dict,
):
    if not (output_path / "deployment").exists():
        (output_path / "deployment").mkdir()

    module_path = pathlib.Path(__file__).parent.resolve()
    awast_path = (module_path / "../..").resolve()
    template_path = (awast_path / "templates/kubernetes").absolute()

    values = merge_values(
        get_default_values(template_path / "values.yaml"),
        values,
    )
    values["name"] = deployment_name

    create_file(
        template_path=template_path,
        template_name="deployment.jinja",
        app_path=output_path,
        filename="deployment/deployment.yaml",
        **values,
    )
