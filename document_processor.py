import json
from config import CLEAN_FILE


def load_documents(file_path=CLEAN_FILE):
    with open(file_path, "r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError("The document file must contain a JSON list.")

    return documents


def chunk_text(text, chunk_size=80, overlap=15):
    words = text.split()

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size.")

    chunks = []
    start = 0

    while start < len(words):
        chunk = words[start:start + chunk_size]
        chunks.append(" ".join(chunk))

        if start + chunk_size >= len(words):
            break

        start += chunk_size - overlap

    return chunks



def process_documents(documents):
    processed = []

    for document in documents:
        chunks = chunk_text(document["text"])

        for index, chunk in enumerate(chunks):
            processed.append({
                "id": f'{document["id"]}_chunk_{index}',
                "source": document.get("source", "unknown"),
                "text": chunk,
                "is_poisoned": document.get("is_poisoned", False)
            })

    return processed