from enum import Enum
import typer
from awast.cli.fastapi.new_api import new_api as new_fastapi
from awast.cli.kubernetes.new_deployment import create_deployment


class Framework(str, Enum):
    fastapi = "FastAPI"
    flask = "Flask"


app = typer.Typer()


@app.command()
def new_api(name: str, framework: Framework = Framework.fastapi):
    print(f"Creating new API: {name}")
    print(f"Using templates for framework: {framework.value}")
    if framework.value == Framework.fastapi:
        new_fastapi(name)
    if framework.value == Framework.flask:
        raise NotImplementedError("Flask templates are not implemented yet")
    print("Success")


@app.command()
def new_deployment(
    name: str, version="latest", mem_request="128M", cpu_request="100m"
):
    print(f"Creating new deployment: {name}")
    create_deployment(name, version, mem_request, cpu_request)
    print("Success")


if __name__ == "__main__":
    app()
