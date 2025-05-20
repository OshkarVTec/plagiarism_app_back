import os
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class PlagiarismResult(BaseModel):
    filename: str
    plagiarism_score: float
    details: str


@app.post(
    "/detect-plagiarism/",
    response_model=List[PlagiarismResult],
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
        # Aquí llamas a tu función de detección de plagio
        # Ejemplo: results = detect_plagiarism_from_paths(file_paths)
        # Debes implementar detect_plagiarism_from_paths
        results = []
        for path in file_paths:
            # Simulación de resultado
            results.append(
                {
                    "filename": os.path.basename(path),
                    "plagiarism_score": 0.5,  # Reemplaza con tu lógica
                    "details": "50% similar to another file",
                }
            )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
