from flask import Flask


def create_app(*args, **kwargs):
    """Creates fastapi app object"""
    return Flask(*args, **kwargs)


def add_root(app):
    """Adds a root endpoint with simple message to the app"""

    @app.get("/")
    def root():
        return {"message", "Hello World"}


def add_metrics(app):
    """Adds metrics exporting to app"""
    pass


def add_ralidator(app):
    """Adds the Ralidator library extension to the app"""
    pass
