import os
from awast.cli.utils import create_file

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
AWAST_PATH = os.path.abspath(os.path.join(MODULE_PATH, "../.."))
TEMPLATE_PATH = os.path.abspath(
    os.path.join(AWAST_PATH, "templates/kubernetes")
)


def create_deployment(name: str, version, mem_request, cpu_request):
    base = os.getcwd()
    output_path = os.path.join(base, name)
    if os.path.exists(output_path):
        raise Exception("Output directory already exist.")

    os.mkdir(name)
    os.mkdir(f"{name}/deployment")

    create_file(
        TEMPLATE_PATH,
        "deployment",
        output_path,
        "deployment/deployment.yaml",
        name=name,
        version=version,
        mem_request=mem_request,
        cpu_request=cpu_request,
    )
