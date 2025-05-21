import os
from typing import Any, Dict, List
from fastapi import FastAPI, File, UploadFile, HTTPException
from services import get_clusters, get_file_content, save_files

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post(
    "/detect-plagiarism/",
    response_model=Dict[str, Any],
    summary="Detect plagiarism in uploaded files",
    description="Upload files and get plagiarism detection results.",
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
)
async def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        return get_file_content(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
