import lancedb 
from backend.src.constants import VECTOR_DATABASE_PATH,DATA_PATH
from data_models import Person
import time
def setup_vector_db(path):
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("persons", schema=Person, exist_ok=True)
    
    return vector_db

def ingest_docs_to_vector_db(table):
    for file in DATA_PATH.glob("*.txt"):
        with open(file,"r") as f:
            content = f.read()
        
        doc_id = file.stem
        table.delete(f"doc_id = '{doc_id}'")

        table.add([
            {
                "doc_id": doc_id,
                "file_path":str(file),
                "filename":file.stem,
                "content":content
            }
        ])
        print(table.to_pandas()["filename"])
        time.sleep(30)


if __name__ == "__main__":
    vector_db = setup_vector_db(VECTOR_DATABASE_PATH)
    ingest_docs_to_vector_db(vector_db["persons"])