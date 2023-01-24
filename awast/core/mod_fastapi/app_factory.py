from fastapi import FastAPI
from dataclasses import dataclass
from starlette_prometheus import metrics, PrometheusMiddleware


def create_app(*args, **kwargs):
    """Creates fastapi app object"""
    app = FastAPI(*args, **kwargs)
    add_root(app)
    add_metrics(app)
    add_ralidator(app)
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
    app.add_route("/metrics/", metrics)


def add_ralidator(app):
    """Adds the Ralidator library extension to the app"""
    pass
