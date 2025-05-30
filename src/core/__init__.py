from fastapi import FastAPI
from .config import settings
from .openapi import custom_openapi
from .middleware import setup_cors_middleware

app = FastAPI()

setup_cors_middleware(app)

app.openapi = lambda: custom_openapi(app)

__all__ = ["settings", "custom_openapi", "app"]