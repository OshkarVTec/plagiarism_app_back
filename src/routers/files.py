import os
from fastapi import APIRouter, HTTPException
from core.config import settings
from services.file_service import get_file_content

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    responses={404: {"description": "File not found"}, 500: {"description": "Server error"}},
)

@router.get(
    "/{filename}",
    summary="Retrieve uploaded file content as text",
    description="Devuelve el contenido de un archivo previamente subido.",
    tags=["Files"],
)
async def get_uploaded_file(filename: str):
    """
    Lee el archivo del disco y retorna:
    { filename: str, content: str }
    """
    file_path = os.path.join(settings.upload_dir, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        return get_file_content(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
