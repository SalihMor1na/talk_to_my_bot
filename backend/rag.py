from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constants import VECTOR_DATABASE_PATH
import lancedb


vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)


rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are impersonating the person described in the CV. "
        "Speak in first person. Use only information from the CV. "
        "If the question is in english answer in english and same goes if it is in swedish."
        "Do not make anything up. If the answer is not in the CV,"
        " say: “That is not mentioned in my CV.”"
        " Context: {context} "
        "Question:{question}",
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching documents to the query
    """
    results = vector_db["persons"].search(query=query).limit(k).to_list()

    return f"""
    
    Filename: {results[0]["filename"]},
    
    Filepath: {results[0]["file_path"]},

    Content: {results[0]["content"]}
    
    """
