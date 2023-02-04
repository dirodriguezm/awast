from fastapi import FastAPI
from dataclasses import dataclass
from starlette_prometheus import metrics, PrometheusMiddleware
from ralidator_fastapi.ralidator_fastapi import RalidatorStarlette


def create_app(*args, **kwargs):
    """Creates fastapi app object"""
    app = FastAPI(*args, **kwargs)
    add_root(app)
    add_metrics(app)
    add_ralidator(
        app,
        config=kwargs["ralidator_config"],
        filters_map=kwargs["ralidator_filters_map"],
        ignore_paths=kwargs["ralidator_ignore_paths"],
    )
    return app


@dataclass
class RootResponse:
    message: str


def add_root(app):
    """Adds a root endpoint with simple message to the app"""

    @app.get("/", response_model=RootResponse)
    def root():
        return {"message": "Hello World"}


def add_metrics(app: FastAPI):
    """Adds metrics exporting to app"""
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)


def add_ralidator(
    app: FastAPI, config: dict, filters_map: dict, ignore_paths: list
):
    """Adds the Ralidator library extension to the app"""
    app.add_middleware(
        RalidatorStarlette,
        config=config,
        filters_map=filters_map,
        ignore_paths=ignore_paths,
    )
