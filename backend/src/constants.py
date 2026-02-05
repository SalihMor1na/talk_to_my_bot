import os
from pathlib import Path

# Resolve project root:
# backend/src/constants.py -> backend/src -> backend -> project root
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data"
VECTOR_DATABASE_PATH = BASE_DIR / "knowledge_base"

# Ensure directories exist
DATA_PATH.mkdir(parents=True, exist_ok=True)
VECTOR_DATABASE_PATH.mkdir(parents=True, exist_ok=True)
