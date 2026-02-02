from backend.constants import DATA_PATH
import shutil
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    file_path = DATA_PATH / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

@app.delete("/deletefile/{filename}")
async def delete_file(filename: str):
    file_path = DATA_PATH / filename