from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

CLEAN_FILE = DATA_DIR / "clean_documents.json"
POISONED_FILE = DATA_DIR / "poisoned_documents.json"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 3

DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)