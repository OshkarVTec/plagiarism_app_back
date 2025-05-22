import os
from typing import Any, Dict, List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.openapi.utils import get_openapi
from services import get_clusters, get_file_content, save_files

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

swagger_ui_params = {
    "docExpansion": "none",       # contrae los paths por defecto
    "persistAuthorization": True  # conserva el token si refrescas
}

app = FastAPI(
    title="Plagiarism Detector API",
    version="1.0.0",
    description=(
        "Sube uno o varios archivos (código o texto) y obtén los grupos "
        "de similitud/plagio detectados."
    ),
    docs_url="/docs",      # <- la página Swagger ahora vive aquí
    redoc_url=None,                 # <- desactiva ReDoc (opcional)
    openapi_url="/openapi.json",    # <- JSON crudo del esquema
    swagger_ui_parameters=swagger_ui_params,
)

@app.post(
    "/detect-plagiarism/",
    response_model=Dict[str, Any],
    summary="Detect plagiarism in uploaded files",
    description="Upload files and get plagiarism detection results.",
    tags=["Plagiarism"],
)
async def detect_plagiarism(files: List[UploadFile] = File(...)):
    await save_files(files)
    try:
        return get_clusters(UPLOAD_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/files/{filename}",
    summary="Retrieve uploaded file content as text",
    description="Return the content of a previously uploaded file as plain text.",
    tags=["Files"],
)
async def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        return get_file_content(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    schema["info"]["x-team"] = [
        {"name": "Cruz Daniel",   "email": "@tec.mx"},
        {"name": "Rogelio",  "email": "a01735819@tec.mx"},
        {"name": "Oskar",      "email": "@tec.mx"},
    ]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi