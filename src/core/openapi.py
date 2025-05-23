from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from core.config import settings


def custom_openapi(app: FastAPI):
    """
    Generate a custom OpenAPI schema including vendor extensions (x-logo, x-team).
    This function should be assigned to app.openapi in main.py:

        app.openapi = lambda: custom_openapi(app)

    """
    # If schema was already generated, return it
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the base schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add vendor-specific extensions
    # openapi_schema["info"]["x-logo"] = {
    #     "url": settings.x_logo_url
    # }
    # openapi_schema["info"]["x-team"] = settings.x_team

    # Cache and return
    app.openapi_schema = openapi_schema
    return app.openapi_schema
