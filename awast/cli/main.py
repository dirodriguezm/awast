from enum import Enum
from typing import List, Optional
import typer
from awast.cli.fastapi.new_api import new_api as new_fastapi
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
):
    print(f"Creating new API: {name}")
    print(f"Using templates for framework: {framework.value}")
    if framework.value == Framework.fastapi:
        new_fastapi(name, set, value_parser)
    if framework.value == Framework.flask:
        raise NotImplementedError("Flask templates are not implemented yet")
    print("Success")


@app.command(name="new-deployment")
def new_deployment_cli(name: str, set: List[str] = typer.Option([])):
    print(f"Creating new deployment: {name}")
    new_deployment(name, set, value_parser)
    print("Success")


if __name__ == "__main__":
    app()
