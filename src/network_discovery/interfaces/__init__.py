"""Interfaces layer for the network discovery tool.

This package contains the user interfaces for the application:
- CLI: Command-line interface using Typer
- API: REST API using FastAPI
- Dashboard: Material Design web dashboard
"""

from .cli import cli


__all__ = ["cli"]


def get_api_app():
    """Get the FastAPI application instance.

    Returns:
        The configured FastAPI application.
    """
    from .api import app  # noqa: PLC0415

    return app


def get_dashboard_app():
    """Get the FastAPI application with dashboard routes.

    Returns:
        The configured FastAPI application with Material Design dashboard.
    """
    from .api import app  # noqa: PLC0415
    from .dashboard import setup_dashboard  # noqa: PLC0415

    setup_dashboard(app)
    return app
