from enum import Enum
import typer
from awast.cli.fastapi.new_api import new_api as new_fastapi


class Framework(str, Enum):
    fastapi = "FastAPI"
    flask = "Flask"


app = typer.Typer()


@app.command()
def new_api(name: str, framework: Framework = Framework.fastapi):
    if framework.value == Framework.fastapi:
        new_fastapi(name)
    if framework.value == Framework.flask:
        raise NotImplementedError("Flask templates are not implemented yet")
    print("Success")


@app.command()
def new_deployment():
    print("Creating new deployment")


if __name__ == "__main__":
    app()
