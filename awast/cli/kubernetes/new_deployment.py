from awast.cli.utils import (
    CreateFileArguments,
    create_file,
    create_file_arguments,
    merge_values,
    get_default_values,
    parse_default_values,
)
import pathlib
from typing import List, Callable


def new_deployment(
    name: str, values: List[str], value_parser: Callable, values_file: str
):
    module_path = pathlib.Path(__file__).parent.resolve()
    awast_path = (module_path / "../..").resolve()
    template_path = (awast_path / "templates/kubernetes").absolute()

    base = pathlib.Path.cwd()
    output_path = base / name

    if not (output_path / "deployment").exists():
        (output_path / "deployment").mkdir()

    parsed_values = value_parser(values)
    parsed_values = parse_default_values(
        template_path, values_file, parsed_values
    )
    parsed_values["name"] = name

    arguments = create_file_arguments(
        name, output_path, parsed_values, template_path, "deployment"
    )

    create_deployment_file(arguments)


def create_deployment_file(arguments: Callable[[], CreateFileArguments]):
    args = arguments()
    print(args)
    create_file(
        template_path=args.template_path,
        template_name="deployment.jinja",
        app_path=args.output_path,
        filename="deployment/deployment.yaml",
        **args.parsed_values,
    )
