from fastapi import FastAPI
from .config import settings
from .openapi import custom_openapi

__all__ = ["settings", "custom_openapi", "app"]