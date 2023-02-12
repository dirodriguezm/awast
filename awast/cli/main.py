from enum import Enum
from typing import List, Optional
import typer
from awast.cli.fastapi.new_api import new_fastapi
from awast.cli.flask.new_api import new_flask
from awast.cli.kubernetes.new_deployment import new_deployment
from awast.cli.utils import value_parser


class Framework(str, Enum):
    fastapi = "FastAPI"
    flask = "Flask"


app = typer.Typer()


@app.command(name="new-api")
def new_api_cli(
    name: str,
    framework: Framework = Framework.fastapi,
    set: List[str] = typer.Option([]),
    values_file: str = "",
):
    print(f"Creating new API: {name}")
    print(f"Using templates for framework: {framework.value}")
    if framework.value == Framework.fastapi:
        new_fastapi(name, set, value_parser, values_file)
    if framework.value == Framework.flask:
        new_flask(name, set, value_parser, values_file)
    print("Success")


@app.command(name="new-deployment")
def new_deployment_cli(
    name: str, set: List[str] = typer.Option([]), values_file: str = ""
):
    print(f"Creating new deployment: {name}")
    new_deployment(name, set, value_parser, values_file)
    print("Success")


if __name__ == "__main__":
    app()
