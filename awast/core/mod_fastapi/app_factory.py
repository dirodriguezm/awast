from fastapi import FastAPI


def create_app(*args, **kwargs):
    """Creates fastapi app object"""
    app = FastAPI(*args, **kwargs)
    add_root(app)
    add_metrics(app)
    add_ralidator(app)
    return app


def add_root(app):
    """Adds a root endpoint with simple message to the app"""

    @app.get("/")
    def root():
        return {"message": "Hello World"}


def add_metrics(app):
    """Adds metrics exporting to app"""
    pass


def add_ralidator(app):
    """Adds the Ralidator library extension to the app"""
    pass
