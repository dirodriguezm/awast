import os
import subprocess
import jinja2

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
AWAST_PATH = os.path.abspath(os.path.join(MODULE_PATH, "../.."))
TEMPLATE_PATH = os.path.abspath(os.path.join(AWAST_PATH, "templates/fastapi"))


def new_api(name: str):
    print(f"Creating new API: {name}")
    print("Using templates for framework: FastAPI")
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


def create_poetry_project(name):
    subprocess.run(["poetry", "new", name])


def get_template(template_path: str, filename: str):
    loader = jinja2.FileSystemLoader(template_path)
    route = jinja2.Environment(loader=loader)
    return route.get_template(filename)


def create_file(
    template_path: str,
    template_name: str,
    app_path: str,
    filename: str,
    **template_args: dict,
):
    with open(os.path.join(app_path, filename), "w") as f:
        f.write(get_template(template_path, template_name).render(**template_args))
