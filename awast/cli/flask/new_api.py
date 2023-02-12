import pathlib
from typing import List, Callable
from awast.cli.utils import new_api


def new_flask(
    name: str, values: List[str], value_parser: Callable, values_file: str
):
    module_path = pathlib.Path(__file__).parent.resolve()
    awast_path = (module_path / "../..").resolve()
    template_path = (awast_path / "templates/api").absolute()
    new_api(
        name,
        template_path,
        values,
        value_parser,
        "flask",
        values_file=values_file,
    )
