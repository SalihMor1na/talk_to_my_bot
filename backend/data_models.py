from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()
embeding_model = get_registry().get("gemini-text").create(name="gemini_embeding_001")

EMBEDDING_DIM =3072
