import subprocess
import jinja2
import os


def create_poetry_project(name):
    subprocess.run(["poetry", "new", name], check=True)


def get_template(template_path: str, filename: str):
    loader = jinja2.FileSystemLoader(template_path)
    route = jinja2.Environment(loader=loader)
    return route.get_template(filename)


def create_file(
    template_path: str,
    template_name: str,
    app_path: str,
    filename: str,
    **template_args,
):
    with open(os.path.join(app_path, filename), "w", encoding="utf-8") as f:
        f.write(
            get_template(template_path, template_name).render(**template_args)
        )
