from typing import Any, List, Dict
from fastapi import APIRouter, File, UploadFile, HTTPException
from core.config import settings
from services.plagiarism_service import save_files, get_clusters

router = APIRouter(
    prefix="/plagiarism",
    tags=["Plagiarism"],
    responses={404: {"description": "Not found"}, 500: {"description": "Server error"}},
)

@router.post(
    "/",
    response_model=Dict[int, Any],
    summary="Detect plagiarism in uploaded files",
    description="Sube uno o varios archivos y devuelve los grupos de similitud/plagio.",
    tags=["Plagiarism"],
)
async def detect_plagiarism(files: List[UploadFile] = File(...)):
    """
    1. Limpia y guarda los archivos en disk.
    2. Ejecuta el clustering de similitud.
    3. Retorna un dict { cluster_id: Cluster }.
    """
    await save_files(files)
    try:
        return get_clusters(settings.upload_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
