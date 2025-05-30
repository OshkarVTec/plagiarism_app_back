import os
from fastapi import FastAPI
from core.config import settings
from routers import plagiarism, files
from core.openapi import custom_openapi
from core.middleware import setup_cors_middleware

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=(
        "Sube uno o varios archivos (código o texto) y obtén los grupos "
        "de similitud/plagio detectados."
    ),
    docs_url=settings.docs_url,
    openapi_url="/openapi.json",
    redoc_url=None,
    swagger_ui_parameters={"docExpansion": "none", "persistAuthorization": True},
)
setup_cors_middleware(app)
app.include_router(plagiarism.router, tags=["Plagiarism"])
app.include_router(files.router, tags=["Files"])

# crea carpeta si no existe
os.makedirs(settings.upload_dir, exist_ok=True)

app.openapi = lambda: custom_openapi(app)
