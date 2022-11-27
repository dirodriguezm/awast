import os
from awast.cli.utils import create_poetry_project, create_file

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
AWAST_PATH = os.path.abspath(os.path.join(MODULE_PATH, "../.."))
TEMPLATE_PATH = os.path.abspath(os.path.join(AWAST_PATH, "templates/fastapi"))


def new_api(name: str):
    base = os.getcwd()

    output_path = os.path.join(base, name)
    if os.path.exists(output_path):
        raise Exception("Output directory already exist.")

    create_poetry_project(name)

    # Create the app.py file inside project
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="app.py",
        app_path=output_path,
        filename=f"{name}/app.py",
    )

    # Create Dockerfile inside project
    create_file(
        template_path=TEMPLATE_PATH,
        template_name="Dockerfile",
        app_path=output_path,
        filename="Dockerfile",
        package=name,
    )
