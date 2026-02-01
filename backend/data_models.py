from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()
embeding_model = get_registry().get("gemini-text").create(name="text-embedding-004")

EMBEDDING_DIM =768

class Person(LanceModel):
    doc_id: str
    file_path: str
    filename: str
    content: str = embeding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embeding_model.VectorField()


class Prompt(BaseModel):
    prompt: str = Field(description="prompt from user, if empty consider prompt as missing")

class RagResponse(BaseModel):
    filename: str = Field(description="filename of the retrieved file without suffix")
    filepath: str = Field(description="absolute path to the retrieved file")
    answer: str = Field(description="answer based on the retrieved file")
