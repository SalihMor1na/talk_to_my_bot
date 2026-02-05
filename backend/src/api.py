from backend.src.rag import rag_agent
from backend.src.data_models import Prompt
from backend.src.constants import DATA_PATH
import shutil
from fastapi import FastAPI, UploadFile, HTTPException
import os
import time

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    file_path = DATA_PATH / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    os.system("python backend/src/pdfs_to_text.py")
    os.system("python ingestion.py")
    return {"status": "ok", "filename": file.filename}

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

@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result = await rag_agent.run(query.prompt)

    return result.output
