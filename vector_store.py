import chromadb
from config import CHROMA_DIR, EMBEDDING_MODEL


client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(name):
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )


def reset_collection(name):
    try:
        client.delete_collection(name=name)
    except Exception:
        pass

    return get_collection(name)


def add_documents(collection, documents):
    if not documents:
        return

    collection.add(
        ids=[doc["id"] for doc in documents],
        documents=[doc["text"] for doc in documents],
        metadatas=[
            {
                "source": doc.get("source", "unknown"),
                "is_poisoned": bool(doc.get("is_poisoned", False))
            }
            for doc in documents
        ]
    )


def retrieve_documents(collection, query, top_k=3):
    result = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count())
    )

    retrieved = []

    if not result["documents"] or not result["documents"][0]:
        return retrieved

    for i, text in enumerate(result["documents"][0]):
        metadata = result["metadatas"][0][i]
        retrieved.append({
            "id": result["ids"][0][i],
            "text": text,
            "source": metadata.get("source", "unknown"),
            "is_poisoned": metadata.get("is_poisoned", False),
            "distance": (
                result["distances"][0][i]
                if result.get("distances") else None
            )
        })

    return retrieved