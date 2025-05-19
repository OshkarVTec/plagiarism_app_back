from typing import List, Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload-files/")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        # Process the file content as needed

        # Example return
        results.append({"filename": file.filename, "size": len(content)})
    return {"files": results}
