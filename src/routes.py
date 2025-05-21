import os
from typing import Any, Dict, List
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from services.plagiarism_clusters import plagiarism_detection_clusters
from services.plagiarism_difflib import detect_type_from_files
from fastapi.encoders import jsonable_encoder

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
    file_paths = []
    for file in files:
        filename = file.filename or "unnamed_file"
        file_location = os.path.join(UPLOAD_DIR, filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        file_paths.append(file_location)

    try:
        clustering_results = plagiarism_detection_clusters(UPLOAD_DIR)
        return jsonable_encoder(clustering_results)
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
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
