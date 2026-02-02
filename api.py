from fastapi import UploadFile
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return file