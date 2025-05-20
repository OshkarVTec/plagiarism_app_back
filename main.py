from typing import List, Union

from fastapi import FastAPI, File, Request, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(
    "/upload-files/",
    summary="Upload multiple files",
    description="Upload one or more files and get their filenames and sizes.",
    response_description="A list of uploaded files with their names and sizes.",
)
async def upload_files(
    files: List[UploadFile] = File(..., description="Multiple files to upload")
):
    """
    Upload one or more files and return their filenames and sizes.

    - **files**: List of files to upload.
    """
    results = []
    for file in files:
        content = await file.read()
        # Process the file content as needed

        # Example return
        results.append({"filename": file.filename, "size": len(content)})
    return {"files": results}
