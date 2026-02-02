from backend.constants import DATA_PATH
import shutil
from fastapi import FastAPI, UploadFile, HTTPException
import os

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    file_path = DATA_PATH / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

@app.delete("/deletefile/{filename}")
async def delete_file(filename: str):
    file_path = DATA_PATH / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(file_path)
    
    return {
        "filename": filename,
        "message": "File deleted successfully"
    }